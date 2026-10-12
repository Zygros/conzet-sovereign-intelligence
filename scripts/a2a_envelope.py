"""Standard-library validator for the Sovereign A2A task envelope prototype.

This validates the local envelope contract only; it does not implement A2A transport,
authentication, remote agent discovery, or JSON Schema format validation.
"""
from __future__ import annotations

import re
from datetime import datetime
from typing import Any

STATUSES = {
    "submitted", "accepted", "running", "completed", "failed",
    "rejected", "timed_out", "cancelled",
}
_SHA256 = re.compile(r"^[a-fA-F0-9]{64}$")
_REQUIRED = {
    "protocol_version", "message_id", "task_id", "sender", "recipient",
    "task_type", "created_at", "permissions", "payload", "provenance",
}
_ALLOWED = _REQUIRED | {
    "parent_task_id", "deadline", "evidence", "status",
}


def _timestamp(value: Any, field: str, errors: list[str]) -> None:
    if not isinstance(value, str) or not value:
        errors.append(f"{field} must be an ISO-8601 timestamp string")
        return
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.tzinfo is None or parsed.utcoffset() is None:
            errors.append(f"{field} must include a timezone")
    except ValueError:
        errors.append(f"{field} must be a valid ISO-8601 timestamp")


def validate_envelope(envelope: Any) -> list[str]:
    """Return an empty list for a valid local envelope, otherwise error messages."""
    errors: list[str] = []
    if not isinstance(envelope, dict):
        return ["envelope must be an object"]
    missing = sorted(_REQUIRED - envelope.keys())
    unknown = sorted(envelope.keys() - _ALLOWED)
    if missing:
        errors.append("missing required fields: " + ", ".join(missing))
    if unknown:
        errors.append("unknown fields: " + ", ".join(unknown))
    if envelope.get("protocol_version") != "1.0":
        errors.append("protocol_version must equal '1.0'")
    for field in ("message_id", "task_id", "sender", "recipient", "task_type"):
        if field in envelope and (not isinstance(envelope[field], str) or not envelope[field].strip()):
            errors.append(f"{field} must be a non-empty string")
    if "parent_task_id" in envelope and envelope["parent_task_id"] is not None and not isinstance(envelope["parent_task_id"], str):
        errors.append("parent_task_id must be a string or null")
    if "created_at" in envelope:
        _timestamp(envelope["created_at"], "created_at", errors)
    if envelope.get("deadline") is not None:
        _timestamp(envelope["deadline"], "deadline", errors)
    permissions = envelope.get("permissions")
    if not isinstance(permissions, dict):
        errors.append("permissions must be an object")
    else:
        if set(permissions) != {"scopes", "sensitive_action_confirmation"}:
            errors.append("permissions must contain only scopes and sensitive_action_confirmation")
        scopes = permissions.get("scopes")
        if not isinstance(scopes, list) or any(not isinstance(x, str) or not x.strip() for x in scopes):
            errors.append("permissions.scopes must be an array of non-empty strings")
        elif len(scopes) != len(set(scopes)):
            errors.append("permissions.scopes must not contain duplicates")
        if not isinstance(permissions.get("sensitive_action_confirmation"), bool):
            errors.append("permissions.sensitive_action_confirmation must be boolean")
    if not isinstance(envelope.get("payload"), dict):
        errors.append("payload must be an object")
    if "evidence" in envelope:
        evidence = envelope["evidence"]
        if not isinstance(evidence, list):
            errors.append("evidence must be an array")
        else:
            for i, item in enumerate(evidence):
                if not isinstance(item, dict) or not isinstance(item.get("kind"), str) or not item.get("kind") or not isinstance(item.get("uri"), str) or not item.get("uri"):
                    errors.append(f"evidence[{i}] must include non-empty kind and uri")
                elif "sha256" in item and (not isinstance(item["sha256"], str) or not _SHA256.fullmatch(item["sha256"])):
                    errors.append(f"evidence[{i}].sha256 must be 64 hexadecimal characters")
    provenance = envelope.get("provenance")
    if not isinstance(provenance, dict):
        errors.append("provenance must be an object")
    else:
        if set(provenance) - {"source_refs", "producer", "schema_version", "repository_commit"}:
            errors.append("provenance contains unknown fields")
        if not isinstance(provenance.get("source_refs"), list) or any(not isinstance(x, str) or not x.strip() for x in provenance.get("source_refs", [])):
            errors.append("provenance.source_refs must be an array of non-empty strings")
        if not isinstance(provenance.get("producer"), str) or not provenance.get("producer", "").strip():
            errors.append("provenance.producer must be a non-empty string")
        if provenance.get("schema_version") != "1.0":
            errors.append("provenance.schema_version must equal '1.0'")
        commit = provenance.get("repository_commit")
        if commit is not None and (not isinstance(commit, str) or not commit.strip()):
            errors.append("provenance.repository_commit must be a non-empty string or null")
    if "status" in envelope and envelope["status"] not in STATUSES:
        errors.append("status is not a supported envelope status")
    return errors
