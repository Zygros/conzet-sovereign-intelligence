"""Evidence-gated status classification for legacy swarm records.

This module does not execute tasks. It prevents synthetic bookkeeping from being
mistaken for execution by classifying legacy records as SIMULATED unless a
structured execution receipt is supplied. A receipt alone is not proof of truth;
its evidence references still require independent inspection.
"""
from __future__ import annotations

from typing import Any, Dict, Optional

RECEIPT_SCHEMA = "conzetian-execution-receipt/1.0"

def classify_record(record: Dict[str, Any], receipt: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Return a copy with a conservative status and an explicit evidence verdict."""
    result = dict(record)
    if not isinstance(receipt, dict):
        result["status"] = "SIMULATED"
        result["evidence_verdict"] = "NO_EXECUTION_RECEIPT"
        return result

    evidence = receipt.get("evidence_refs")
    structurally_valid = (
        receipt.get("schema") == RECEIPT_SCHEMA
        and isinstance(receipt.get("action_id"), str) and bool(receipt["action_id"].strip())
        and isinstance(receipt.get("adapter_id"), str) and bool(receipt["adapter_id"].strip())
        and receipt.get("execution") is True
        and receipt.get("verification_status") == "PASSED"
        and isinstance(evidence, list) and len(evidence) > 0
        and all(isinstance(item, str) and item.strip() for item in evidence)
    )
    if not structurally_valid:
        result["status"] = "SIMULATED"
        result["evidence_verdict"] = "RECEIPT_INVALID_OR_INCOMPLETE"
        return result

    result["status"] = "EXECUTED_PENDING_EVIDENCE_REVIEW"
    result["evidence_verdict"] = "RECEIPT_SHAPE_VALID_NOT_INDEPENDENTLY_VERIFIED"
    result["execution_receipt"] = {
        "schema": receipt["schema"],
        "action_id": receipt["action_id"],
        "adapter_id": receipt["adapter_id"],
        "evidence_refs": list(evidence),
    }
    return result
