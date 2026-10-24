#!/usr/bin/env python3
"""Audit Scroll 476 hash-field consistency without changing source artifacts.

This tool computes hashes over the exact bytes of the local files supplied by
an operator. It does not rewrite the Markdown/JSON, create timestamp proofs,
or treat the presence of an .ots file as verification. Original artifacts must
be preserved; corrections should be written as separate additive records.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import sys
from typing import Any, Dict, Optional

EMPTY_SHA256 = hashlib.sha256(b"").hexdigest()
MARKDOWN_HASH = re.compile(
    r"\*\*Verification Hash:\*\*\s*`([0-9a-fA-F]{64})`", re.IGNORECASE
)
SCOPE_MARKER = re.compile(
    r"\b(?:verification|source|payload|content)\s+hash\s+scope\b", re.IGNORECASE
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _proof_status(path_text: Optional[str]) -> Dict[str, Any]:
    if not path_text:
        return {"path": None, "present": False, "state": "NOT_PROVIDED", "verified": False}
    path = pathlib.Path(path_text)
    if not path.is_file():
        return {"path": str(path), "present": False, "state": "NOT_FOUND", "verified": False}
    data = path.read_bytes()
    if data.startswith(b"OpenTimestamps placeholder"):
        state = "PLACEHOLDER_NOT_A_VALID_PROOF"
    elif data.startswith(b"\x00OpenTimestamps\x00\x00Proof") or data.startswith(b"\x00OpenTimestamps\x00Proof"):
        state = "OTS_FORMAT_CANDIDATE_UNVERIFIED"
    else:
        state = "PRESENT_UNVERIFIED_FORMAT_UNKNOWN"
    return {
        "path": str(path),
        "present": True,
        "bytes": len(data),
        "sha256": sha256(data),
        "state": state,
        "verified": False,
        "note": "Presence or a recognizable header is not proof verification.",
    }


def audit(markdown_path: str, json_path: str,
          placeholder_proof_path: Optional[str] = None,
          candidate_proof_path: Optional[str] = None) -> Dict[str, Any]:
    md_file = pathlib.Path(markdown_path)
    json_file = pathlib.Path(json_path)
    md_bytes = md_file.read_bytes()
    json_bytes = json_file.read_bytes()
    md_text = md_bytes.decode("utf-8", errors="replace")
    parsed = json.loads(json_bytes.decode("utf-8-sig"))

    md_match = MARKDOWN_HASH.search(md_text)
    md_hash = md_match.group(1).lower() if md_match else None
    json_value = parsed.get("verification_hash") if isinstance(parsed, dict) else None
    json_hash = json_value.lower() if isinstance(json_value, str) and re.fullmatch(
        r"[0-9a-fA-F]{64}", json_value
    ) else None

    proposal_text = parsed.get("proposal_text") if isinstance(parsed, dict) else None
    candidate_hashes = {
        "markdown_file_sha256": sha256(md_bytes),
        "json_file_sha256": sha256(json_bytes),
    }
    if isinstance(proposal_text, str):
        candidate_hashes["json_proposal_text_utf8_sha256"] = sha256(proposal_text.encode("utf-8"))

    scope_declared = bool(
        SCOPE_MARKER.search(md_text)
        or (isinstance(parsed, dict) and any(
            isinstance(parsed.get(key), str) and parsed.get(key).strip()
            for key in ("hash_scope", "verification_hash_scope", "hash_scope_description")
        ))
    )
    source_files_nonempty = bool(md_bytes.strip() and json_bytes.strip())
    fields_match = bool(md_hash and json_hash and md_hash == json_hash)
    field_hashes = [value for value in (md_hash, json_hash) if value]
    is_empty_hash = any(value == EMPTY_SHA256 for value in field_hashes)
    matches_candidate = bool(field_hashes) and any(
        value in set(candidate_hashes.values()) for value in field_hashes
    )

    if not md_hash or not json_hash:
        status = "CORRECTION_REQUIRED_MISSING_OR_INVALID_HASH_FIELD"
    elif not fields_match:
        status = "CORRECTION_REQUIRED_FIELDS_DISAGREE"
    elif is_empty_hash and source_files_nonempty:
        status = "CORRECTION_REQUIRED_EMPTY_PAYLOAD_DIGEST_ON_NONEMPTY_ARTIFACTS"
    elif not scope_declared:
        status = "REVIEW_REQUIRED_HASH_SCOPE_UNDECLARED"
    elif not matches_candidate:
        status = "REVIEW_REQUIRED_FIELD_DOES_NOT_MATCH_TESTED_CANDIDATE_SCOPES"
    else:
        status = "REVIEW_REQUIRED_EVEN_IF_CANDIDATE_HASH_MATCHES"

    result = {
        "schema_version": "conzetian-scroll476-integrity-audit/v1",
        "audit_mode": "read_only_exact_local_bytes",
        "status": status,
        "source_files": {
            "markdown": {"path": str(md_file), "bytes": len(md_bytes), "sha256": candidate_hashes["markdown_file_sha256"]},
            "json": {"path": str(json_file), "bytes": len(json_bytes), "sha256": candidate_hashes["json_file_sha256"]},
            "nonempty": source_files_nonempty,
        },
        "verification_hash_fields": {
            "markdown_value": md_hash,
            "json_value": json_hash,
            "values_match": fields_match,
            "equals_sha256_of_empty_bytes": is_empty_hash,
            "empty_bytes_sha256": EMPTY_SHA256,
            "declared_scope_found": scope_declared,
            "matches_any_tested_candidate_scope": matches_candidate,
            "candidate_scopes": candidate_hashes,
        },
        "timestamp_proofs": {
            "placeholder_receipt": _proof_status(placeholder_proof_path),
            "markdown_receipt_candidate": _proof_status(candidate_proof_path),
        },
        "limitations": [
            "A hash match establishes byte identity only, not semantic truth or authorization.",
            "A recognized OpenTimestamps file header does not establish Bitcoin confirmation.",
            "An unverified or placeholder receipt is not counted as an external anchor.",
        ],
    }
    return result


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("markdown", help="path to the original proposal Markdown bytes")
    parser.add_argument("json_file", help="path to the paired proposal JSON bytes")
    parser.add_argument("--placeholder-proof", help="path to a receipt suspected to be a placeholder")
    parser.add_argument("--candidate-proof", help="path to a separate .ots proof candidate")
    parser.add_argument("--output", help="write report to a new path; existing files are never overwritten")
    args = parser.parse_args(argv)
    try:
        report = audit(args.markdown, args.json_file, args.placeholder_proof, args.candidate_proof)
        rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
        if args.output:
            out = pathlib.Path(args.output)
            if out.exists():
                raise FileExistsError("refusing to overwrite existing output: " + str(out))
            out.write_text(rendered, encoding="utf-8")
        else:
            sys.stdout.write(rendered)
        if report["status"].startswith("CORRECTION_REQUIRED"):
            return 2
        if report["status"].startswith("REVIEW_REQUIRED"):
            return 1
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print("audit failed: " + str(exc), file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
