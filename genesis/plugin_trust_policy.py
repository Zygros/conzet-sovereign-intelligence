"""Descriptor-bound trust gate for M.A.I.A. Python plugin paths.

This module validates the exact file object that is read and later compiled.
A passing gate is not a sandbox or a safety verdict: trusted plugin code still
executes with the orchestrator process privileges.
"""
from __future__ import annotations

import hashlib
import os
import stat
from pathlib import Path
from typing import Any, Dict, Iterable, Optional


def _owner_is_trusted(info: os.stat_result, effective_uid: Optional[int]) -> bool:
    if effective_uid is None:
        return True
    return getattr(info, "st_uid", None) in (0, effective_uid)


def _stat_signature(info: os.stat_result) -> tuple:
    return (
        info.st_dev,
        info.st_ino,
        info.st_size,
        info.st_mtime_ns,
        info.st_ctime_ns,
        getattr(info, "st_uid", None),
        stat.S_IMODE(info.st_mode),
    )


def _validate_directory(
    path: Path,
    effective_uid: Optional[int],
    *,
    allow_sticky_writable: bool,
) -> Optional[str]:
    try:
        info = os.stat(path, follow_symlinks=False)
    except OSError:
        return "TRUSTED_DIRECTORY_NOT_FOUND"

    if not stat.S_ISDIR(info.st_mode):
        return "TRUST_PATH_NOT_DIRECTORY"
    if not _owner_is_trusted(info, effective_uid):
        return "UNTRUSTED_PATH_OWNER"

    writable = info.st_mode & (stat.S_IWGRP | stat.S_IWOTH)
    sticky = info.st_mode & getattr(stat, "S_ISVTX", 0)
    if writable and not (allow_sticky_writable and sticky):
        return "WRITABLE_TRUSTED_DIRECTORY"
    return None


def _validate_root_ancestors(root: Path, effective_uid: Optional[int]) -> Optional[str]:
    current = os.fspath(root)
    while True:
        try:
            info = os.stat(current, follow_symlinks=False)
        except OSError:
            return "TRUSTED_ANCESTOR_NOT_FOUND"

        if not stat.S_ISDIR(info.st_mode):
            return "TRUST_PATH_NOT_DIRECTORY"
        if not _owner_is_trusted(info, effective_uid):
            return "UNTRUSTED_PATH_OWNER"

        writable = info.st_mode & (stat.S_IWGRP | stat.S_IWOTH)
        sticky = info.st_mode & getattr(stat, "S_ISVTX", 0)
        if current == os.fspath(root):
            if writable:
                return "WRITABLE_TRUSTED_DIRECTORY"
        elif writable and not sticky:
            return "WRITABLE_ANCESTOR_DIRECTORY"

        parent = os.path.dirname(current)
        if parent == current:
            return None
        current = parent


def read_trusted_plugin_source(
    plugin_path: str,
    trusted_root: str,
    allowed_plugins: Iterable[str],
    expected_sha256: Optional[str] = None,
) -> Dict[str, Any]:
    """Validate and read an allowlisted plugin through one opened descriptor.

    The returned source_bytes are the exact bytes whose SHA-256 is checked.
    Callers must compile those bytes directly and must not reopen plugin_path.
    """
    try:
        root = Path(trusted_root).resolve(strict=True)
    except (OSError, RuntimeError):
        return {"allowed": False, "reason": "TRUSTED_ROOT_NOT_FOUND"}

    raw = Path(plugin_path)
    candidate = raw if raw.is_absolute() else root / raw

    try:
        lexical = candidate.absolute()
        relative_lexical = lexical.relative_to(root)
    except (ValueError, OSError):
        return {"allowed": False, "reason": "PATH_OUTSIDE_TRUSTED_ROOT"}

    if not relative_lexical.parts or any(
        part in ("", ".", "..") for part in relative_lexical.parts
    ):
        return {"allowed": False, "reason": "PATH_TRAVERSAL"}

    # Reject symlinks in each component before canonical resolution.
    cursor = root
    for part in relative_lexical.parts:
        cursor = cursor / part
        try:
            if cursor.is_symlink():
                return {"allowed": False, "reason": "SYMLINK_NOT_ALLOWED"}
        except OSError:
            return {"allowed": False, "reason": "PLUGIN_FILE_NOT_FOUND"}

    try:
        resolved = candidate.resolve(strict=True)
        relative = resolved.relative_to(root).as_posix()
    except FileNotFoundError:
        return {"allowed": False, "reason": "PLUGIN_FILE_NOT_FOUND"}
    except (ValueError, OSError, RuntimeError):
        return {"allowed": False, "reason": "PATH_OUTSIDE_TRUSTED_ROOT"}

    allowlist = set()
    for item in allowed_plugins:
        allowed_path = Path(item)
        if allowed_path.is_absolute() or ".." in allowed_path.parts:
            continue
        allowlist.add(allowed_path.as_posix())

    if relative not in allowlist:
        return {"allowed": False, "reason": "PLUGIN_NOT_ALLOWLISTED"}
    if resolved.suffix != ".py":
        return {"allowed": False, "reason": "NOT_A_PYTHON_PLUGIN"}

    effective_uid_fn = getattr(os, "geteuid", None)
    effective_uid = effective_uid_fn() if callable(effective_uid_fn) else None

    # The configured root and every descendant directory must be private.
    directories = [root]
    parent = root
    for part in relative_lexical.parts[:-1]:
        parent = parent / part
        directories.append(parent)
    for directory in directories:
        reason = _validate_directory(
            directory, effective_uid, allow_sticky_writable=False
        )
        if reason:
            return {"allowed": False, "reason": reason}

    ancestor_reason = _validate_root_ancestors(root, effective_uid)
    if ancestor_reason:
        return {"allowed": False, "reason": ancestor_reason}

    try:
        path_info = os.stat(resolved, follow_symlinks=False)
    except OSError:
        return {"allowed": False, "reason": "PLUGIN_FILE_NOT_FOUND"}

    if not stat.S_ISREG(path_info.st_mode):
        return {"allowed": False, "reason": "PLUGIN_FILE_NOT_REGULAR"}
    if not _owner_is_trusted(path_info, effective_uid):
        return {"allowed": False, "reason": "UNTRUSTED_PLUGIN_OWNER"}
    if path_info.st_mode & (stat.S_IWGRP | stat.S_IWOTH):
        return {"allowed": False, "reason": "PLUGIN_FILE_WRITABLE"}

    descriptor = None
    try:
        flags = os.O_RDONLY | getattr(os, "O_BINARY", 0)
        flags |= getattr(os, "O_NOFOLLOW", 0)
        descriptor = os.open(os.fspath(resolved), flags)
        opened_info = os.fstat(descriptor)

        if not stat.S_ISREG(opened_info.st_mode):
            return {"allowed": False, "reason": "OPENED_FILE_NOT_REGULAR"}
        if not _owner_is_trusted(opened_info, effective_uid):
            return {"allowed": False, "reason": "UNTRUSTED_DESCRIPTOR_OWNER"}
        if opened_info.st_mode & (stat.S_IWGRP | stat.S_IWOTH):
            return {"allowed": False, "reason": "DESCRIPTOR_FILE_WRITABLE"}

        if (
            opened_info.st_dev,
            opened_info.st_ino,
            getattr(opened_info, "st_uid", None),
        ) != (
            path_info.st_dev,
            path_info.st_ino,
            getattr(path_info, "st_uid", None),
        ):
            return {"allowed": False, "reason": "FILE_IDENTITY_CHANGED"}

        current_path_info = os.stat(resolved, follow_symlinks=False)
        if (
            current_path_info.st_dev,
            current_path_info.st_ino,
            getattr(current_path_info, "st_uid", None),
        ) != (
            opened_info.st_dev,
            opened_info.st_ino,
            getattr(opened_info, "st_uid", None),
        ):
            return {"allowed": False, "reason": "FILE_PATH_REPLACED"}

        with os.fdopen(descriptor, "rb") as stream:
            descriptor = None
            source_bytes = stream.read()
            after_read = os.fstat(stream.fileno())

        if not _owner_is_trusted(after_read, effective_uid):
            return {"allowed": False, "reason": "DESCRIPTOR_OWNER_CHANGED"}
        if _stat_signature(opened_info) != _stat_signature(after_read):
            return {"allowed": False, "reason": "FILE_CHANGED_DURING_READ"}

        final_path_info = os.stat(resolved, follow_symlinks=False)
        if (
            final_path_info.st_dev,
            final_path_info.st_ino,
            getattr(final_path_info, "st_uid", None),
        ) != (
            after_read.st_dev,
            after_read.st_ino,
            getattr(after_read, "st_uid", None),
        ):
            return {"allowed": False, "reason": "FILE_PATH_REPLACED"}

        digest = hashlib.sha256(source_bytes).hexdigest()
        if expected_sha256 is not None and digest.lower() != expected_sha256.lower():
            return {
                "allowed": False,
                "reason": "SHA256_MISMATCH",
                "sha256": digest,
            }

        return {
            "allowed": True,
            "reason": "ALLOWLIST_AND_INTEGRITY_CHECKS_PASSED",
            "relative_path": relative,
            "resolved_path": os.fspath(resolved),
            "sha256": digest,
            "source_bytes": source_bytes,
            "execution_performed": False,
            "safety_verdict": "NOT_ASSESSED",
        }
    except OSError:
        return {"allowed": False, "reason": "PLUGIN_READ_FAILED"}
    finally:
        if descriptor is not None:
            os.close(descriptor)


def validate_plugin_path(
    plugin_path: str,
    trusted_root: str,
    allowed_plugins: Iterable[str],
    expected_sha256: Optional[str] = None,
) -> Dict[str, Any]:
    """Compatibility wrapper returning metadata without the source bytes."""
    result = read_trusted_plugin_source(
        plugin_path=plugin_path,
        trusted_root=trusted_root,
        allowed_plugins=allowed_plugins,
        expected_sha256=expected_sha256,
    )
    result.pop("source_bytes", None)
    return result
