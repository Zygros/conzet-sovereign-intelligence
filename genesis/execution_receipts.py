"""Conzetian execution-receipt contract.

This module validates receipt structure and status invariants only. It cannot prove
that a claimed external action occurred; callers must supply trustworthy evidence
and independently verify it.
"""
from __future__ import annotations

from typing import Any

STATUSES = {"PLANNED", "REQUESTED", "EXECUTED", "FAILED", "VERIFIED"}


def validate_receipt(receipt: dict[str, Any]) -> list[str]:
    """Return structural/invariant errors for one action receipt."""
    errors: list[str] = []
    if not isinstance(receipt, dict):
        return ["receipt must be an object"]

    required = ("receipt_version", "action_id", "action", "status", "executed",
                "result", "evidence_refs", "verification")
    for field in required:
        if field not in receipt:
            errors.append(f"missing required field: {field}")

    if receipt.get("receipt_version") != "conzetian-execution-receipt/1.0":
        errors.append("unsupported receipt_version")

    status = receipt.get("status")
    if status not in STATUSES:
        errors.append("status must be one of: " + ", ".join(sorted(STATUSES)))

    if not isinstance(receipt.get("executed"), bool):
        errors.append("executed must be a boolean")
    elif status in {"EXECUTED", "VERIFIED"} and receipt["executed"] is not True:
        errors.append(f"{status} requires executed=true")
    elif status in {"PLANNED", "REQUESTED"} and receipt["executed"] is True:
        errors.append(f"{status} cannot claim executed=true")

    evidence = receipt.get("evidence_refs")
    if not isinstance(evidence, list) or any(not isinstance(item, str) or not item.strip() for item in evidence):
        errors.append("evidence_refs must be a list of non-empty strings")

    verification = receipt.get("verification")
    if not isinstance(verification, dict):
        errors.append("verification must be an object")
    elif status == "VERIFIED":
        if not isinstance(verification.get("method"), str) or not verification["method"].strip():
            errors.append("VERIFIED requires a non-empty verification.method")
        if verification.get("passed") is not True:
            errors.append("VERIFIED requires verification.passed=true")
        if not isinstance(evidence, list) or not evidence:
            errors.append("VERIFIED requires at least one evidence reference")

    for field in ("action_id", "action"):
        if not isinstance(receipt.get(field), str) or not receipt[field].strip():
            errors.append(f"{field} must be a non-empty string")

    return errors
