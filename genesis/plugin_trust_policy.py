"""Non-executing trust gate for M.A.I.A. Python plugin paths.

This module deliberately does not import or execute plugins. Call it before any
dynamic import, and treat a passing result as path/integrity validation only,
not as proof that plugin code is safe. Process isolation is still required for
untrusted code.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Iterable, Optional, Dict, Any


def validate_plugin_path(
    plugin_path: str,
    trusted_root: str,
    allowed_plugins: Iterable[str],
    expected_sha256: Optional[str] = None,
) -> Dict[str, Any]:
    """Validate an exact allowlisted .py file without importing it.

    Allowlist entries must be relative paths beneath trusted_root. Symlinks,
    traversal, non-Python files, missing files, and optional digest mismatches
    are rejected. A successful result is a gate decision, not a safety verdict.
    """
    root = Path(trusted_root).resolve()
    raw = Path(plugin_path)
    candidate = raw if raw.is_absolute() else root / raw

    try:
        lexical = candidate.absolute()
        relative_lexical = lexical.relative_to(root)
    except (ValueError, OSError):
        return {"allowed": False, "reason": "PATH_OUTSIDE_TRUSTED_ROOT"}

    if any(part in ("", ".", "..") for part in relative_lexical.parts):
        return {"allowed": False, "reason": "PATH_TRAVERSAL"}

    # Refuse symlinks in every component, including the final plugin file.
    cursor = root
    for part in relative_lexical.parts:
        cursor = cursor / part
        if cursor.is_symlink():
            return {"allowed": False, "reason": "SYMLINK_NOT_ALLOWED"}

    resolved = candidate.resolve()
    try:
        relative = resolved.relative_to(root).as_posix()
    except ValueError:
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
    if not resolved.is_file():
        return {"allowed": False, "reason": "PLUGIN_FILE_NOT_FOUND"}

    digest = hashlib.sha256(resolved.read_bytes()).hexdigest()
    if expected_sha256 is not None and digest.lower() != expected_sha256.lower():
        return {"allowed": False, "reason": "SHA256_MISMATCH", "sha256": digest}

    return {
        "allowed": True,
        "reason": "ALLOWLIST_AND_INTEGRITY_CHECKS_PASSED",
        "relative_path": relative,
        "sha256": digest,
        "execution_performed": False,
        "safety_verdict": "NOT_ASSESSED",
    }
