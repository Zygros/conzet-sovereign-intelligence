import hashlib
import json
from pathlib import Path

from scripts.audit_scroll476_integrity import EMPTY_SHA256, audit, sha256


def _fixture(tmp_path: Path, digest: str = EMPTY_SHA256):
    markdown = tmp_path / "proposal.md"
    payload = tmp_path / "proposal.json"
    markdown.write_text(
        "# Scroll 476\n\n**Verification Hash:** `" + digest + "`\n\nNon-empty proposal body.\n",
        encoding="utf-8",
    )
    payload.write_text(json.dumps({
        "verification_hash": digest,
        "proposal_text": "Non-empty proposal body.",
    }, indent=2) + "\n", encoding="utf-8")
    return markdown, payload


def test_empty_digest_on_nonempty_sources_requires_correction(tmp_path):
    markdown, payload = _fixture(tmp_path)
    report = audit(str(markdown), str(payload))
    assert report["status"] == "CORRECTION_REQUIRED_EMPTY_PAYLOAD_DIGEST_ON_NONEMPTY_ARTIFACTS"
    assert report["source_files"]["nonempty"] is True
    assert report["verification_hash_fields"]["equals_sha256_of_empty_bytes"] is True
    assert report["source_files"]["markdown"]["sha256"] == sha256(markdown.read_bytes())
    assert report["source_files"]["json"]["sha256"] == sha256(payload.read_bytes())


def test_placeholder_receipt_is_never_counted_as_proof(tmp_path):
    markdown, payload = _fixture(tmp_path)
    placeholder = tmp_path / "placeholder.ots"
    placeholder.write_bytes(b"OpenTimestamps placeholder\nSHA256 digest:\n")
    report = audit(str(markdown), str(payload), placeholder_proof_path=str(placeholder))
    proof = report["timestamp_proofs"]["placeholder_receipt"]
    assert proof["state"] == "PLACEHOLDER_NOT_A_VALID_PROOF"
    assert proof["verified"] is False


def test_ots_header_candidate_is_still_unverified(tmp_path):
    markdown, payload = _fixture(tmp_path)
    candidate = tmp_path / "candidate.ots"
    candidate.write_bytes(b"\x00OpenTimestamps\x00\x00Proof\x00fixture")
    report = audit(str(markdown), str(payload), candidate_proof_path=str(candidate))
    proof = report["timestamp_proofs"]["markdown_receipt_candidate"]
    assert proof["state"] == "OTS_FORMAT_CANDIDATE_UNVERIFIED"
    assert proof["verified"] is False


def test_known_empty_sha256_constant():
    assert EMPTY_SHA256 == hashlib.sha256(b"").hexdigest()
    assert EMPTY_SHA256 == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
