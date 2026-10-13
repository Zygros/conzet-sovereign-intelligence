"""Bounded local A2A round-trip acceptance test.

This exercises envelope validation and evidence linkage with deterministic mock
agents. It deliberately does not claim network transport or external-model execution.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone

from scripts.a2a_envelope import validate_envelope


def _envelope(*, message_id: str, task_id: str, sender: str, recipient: str,
              task_type: str, payload: dict, source_sha256: str,
              status: str) -> dict:
    return {
        "protocol_version": "1.0",
        "message_id": message_id,
        "task_id": task_id,
        "sender": sender,
        "recipient": recipient,
        "task_type": task_type,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "permissions": {
            "scopes": ["source:read", "evidence:write"],
            "sensitive_action_confirmation": True,
        },
        "payload": payload,
        "evidence": [{
            "kind": "sha256",
            "uri": "urn:sha256:" + source_sha256,
            "sha256": source_sha256,
        }],
        "provenance": {
            "source_refs": ["urn:conzetian:a2a-roundtrip-fixture"],
            "producer": sender,
            "schema_version": "1.0",
            "repository_commit": None,
        },
        "status": status,
    }


def test_mock_a2a_round_trip_preserves_task_and_evidence():
    task = {"objective": "classify fixture", "execution_allowed": False}
    canonical = json.dumps(task, sort_keys=True, separators=(",", ":")).encode()
    source_hash = hashlib.sha256(canonical).hexdigest()

    request = _envelope(
        message_id="msg-request-001", task_id="task-001",
        sender="opportunity-scout", recipient="mock-evidence-verifier",
        task_type="review_discovery_candidate", payload=task,
        source_sha256=source_hash, status="submitted",
    )
    assert validate_envelope(request) == []

    # Deterministic mock receiver response, linked to the same task and source.
    response_payload = {
        "task_id": request["task_id"],
        "decision": "needs_review",
        "independent_review_completed": False,
        "reason": "Mock receiver cannot claim independent review.",
    }
    response = _envelope(
        message_id="msg-response-001", task_id=request["task_id"],
        sender="mock-evidence-verifier", recipient="opportunity-scout",
        task_type="review_discovery_candidate.result", payload=response_payload,
        source_sha256=source_hash, status="completed",
    )
    assert validate_envelope(response) == []
    assert response["task_id"] == request["task_id"]
    assert response["evidence"][0]["sha256"] == request["evidence"][0]["sha256"]
    assert response["payload"]["independent_review_completed"] is False
    assert request["permissions"]["sensitive_action_confirmation"] is True
    assert request["payload"]["execution_allowed"] is False


def test_a2a_round_trip_rejects_malformed_evidence_digest():
    task = {"objective": "test", "execution_allowed": False}
    envelope = _envelope(
        message_id="msg-bad-001", task_id="task-bad-001",
        sender="mock-a", recipient="mock-b", task_type="test",
        payload=task, source_sha256="not-a-digest", status="submitted",
    )
    assert any("sha256" in error for error in validate_envelope(envelope))
