#!/usr/bin/env python3
"""Create provenance receipts for Scout candidates without executing their contents.

This is a local handoff prototype, not a networked A2A transport or source-truth
verifier. A receipt records what was received and what remains unverified.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

try:
    from scripts.a2a_envelope import validate_envelope
except ModuleNotFoundError:  # Direct script execution places scripts/ on sys.path.
    from a2a_envelope import validate_envelope

SCHEMA_VERSION = "1.0"


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_hex(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def is_http_url(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def candidate_to_receipt(record: dict[str, Any], generated_at: str | None = None) -> dict[str, Any]:
    """Turn one untrusted discovery record into a review-pending evidence receipt."""
    timestamp = generated_at or datetime.now(timezone.utc).isoformat()
    url = record.get("url")
    if not is_http_url(url):
        raise ValueError("candidate url must be an absolute HTTP(S) URL")

    candidate_id = "cand-" + sha256_hex(url.encode("utf-8"))[:24]
    record_digest = sha256_hex(canonical_json(record))
    envelope = {
        "protocol_version": "1.0",
        "message_id": "msg-" + sha256_hex((candidate_id + timestamp).encode("utf-8"))[:24],
        "task_id": "task-" + candidate_id[5:],
        "sender": "opportunity-scout",
        "recipient": "evidence-verifier",
        "task_type": "review_discovery_candidate",
        "created_at": timestamp,
        "permissions": {
            "scopes": ["source:read", "evidence:write"],
            "sensitive_action_confirmation": True,
        },
        "payload": {
            "candidate_id": candidate_id,
            "title": record.get("title"),
            "source_type": record.get("source_type", "unknown"),
            "discovery_query": record.get("query"),
            "review_state": "pending",
            "execution_allowed": False,
        },
        "evidence": [
            {"kind": "discovery_record", "uri": url, "sha256": record_digest}
        ],
        "provenance": {
            "source_refs": [url],
            "producer": "Sovereign Opportunity Scout",
            "schema_version": SCHEMA_VERSION,
        },
        "status": "submitted",
    }
    errors = validate_envelope(envelope)
    if errors:
        raise ValueError("generated envelope failed validation: " + "; ".join(errors))
    return {
        "receipt_version": SCHEMA_VERSION,
        "candidate_id": candidate_id,
        "received_at": timestamp,
        "source_url": url,
        "record_sha256": record_digest,
        "review_status": "pending_independent_review",
        "claims_verified": False,
        "source_content_fetched": False,
        "discovered_code_executed": False,
        "disposition": "unreviewed_candidate",
        "a2a_envelope": envelope,
        "limitations": [
            "URL and metadata are not proof that a claim is true.",
            "The source content has not been fetched or independently corroborated.",
            "This receipt is local provenance bookkeeping, not a digital signature or external anchor.",
        ],
    }


def build_receipts(document: dict[str, Any], generated_at: str | None = None) -> dict[str, Any]:
    records = document.get("records")
    if not isinstance(records, list):
        raise ValueError("Scout document must contain a records array")
    receipts = []
    rejected = []
    for index, record in enumerate(records):
        if not isinstance(record, dict) or record.get("error"):
            rejected.append({"index": index, "reason": "record is not a candidate or contains a source error"})
            continue
        try:
            receipts.append(candidate_to_receipt(record, generated_at))
        except ValueError as exc:
            rejected.append({"index": index, "reason": str(exc)})
    return {
        "receipt_manifest_version": SCHEMA_VERSION,
        "generated_at": generated_at or datetime.now(timezone.utc).isoformat(),
        "input_generated_at": document.get("generated_at"),
        "input_record_count": len(records),
        "receipt_count": len(receipts),
        "rejected_count": len(rejected),
        "review_gate": "human_or_independent_review_required",
        "receipts": receipts,
        "rejected_records": rejected,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Scout JSON artifact")
    parser.add_argument("--output", type=Path, default=Path("scout-output/verification-receipts.json"))
    args = parser.parse_args()
    document = json.loads(args.input.read_text(encoding="utf-8"))
    manifest = build_receipts(document)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {manifest['receipt_count']} review-pending receipts; rejected {manifest['rejected_count']} records")
    return 0 if manifest["receipt_count"] > 0 or manifest["input_record_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
