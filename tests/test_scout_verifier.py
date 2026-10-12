import json
import tempfile
import unittest
from pathlib import Path

from scripts.scout_verifier import build_receipts, candidate_to_receipt
try:
    from scripts.a2a_envelope import validate_envelope
except ModuleNotFoundError:
    from a2a_envelope import validate_envelope


class ScoutVerifierTests(unittest.TestCase):
    def test_candidate_receipt_has_valid_envelope_and_pending_gate(self):
        record = {"source_type":"github_repository","title":"Example research","url":"https://example.org/research","query":"open science"}
        receipt = candidate_to_receipt(record, "2026-10-12T12:00:00+00:00")
        self.assertEqual(validate_envelope(receipt["a2a_envelope"]), [])
        self.assertEqual(receipt["review_status"], "pending_independent_review")
        self.assertFalse(receipt["claims_verified"])
        self.assertFalse(receipt["discovered_code_executed"])
        self.assertEqual(len(receipt["record_sha256"]), 64)

    def test_candidate_id_stable_for_same_url(self):
        a = candidate_to_receipt({"url":"https://example.org/x"}, "2026-10-12T12:00:00Z")
        b = candidate_to_receipt({"url":"https://example.org/x","title":"different metadata"}, "2026-10-12T12:01:00Z")
        self.assertEqual(a["candidate_id"], b["candidate_id"])

    def test_rejects_non_http_url(self):
        with self.assertRaisesRegex(ValueError, "absolute HTTP"):
            candidate_to_receipt({"url":"file:///etc/passwd"})

    def test_manifest_separates_candidates_and_source_errors(self):
        manifest = build_receipts({"generated_at":"2026-10-12T12:00:00Z","records":[
            {"url":"https://example.org/ok","title":"ok"},
            {"url":"javascript:alert(1)","title":"bad"},
            {"error":"timeout","query":"failed query"},
        ]}, "2026-10-12T12:01:00Z")
        self.assertEqual(manifest["input_record_count"], 3)
        self.assertEqual(manifest["receipt_count"], 1)
        self.assertEqual(manifest["rejected_count"], 2)
        self.assertEqual(manifest["review_gate"], "human_or_independent_review_required")

    def test_requires_records_array(self):
        with self.assertRaisesRegex(ValueError, "records array"):
            build_receipts({})

    def test_real_scout_schema_records_are_receipted_and_errors_preserved(self):
        document = {"generated_at":"2026-10-12T12:00:00Z","records":[
            {"source_type":"github_repository","title":"org/repo","url":"https://github.com/org/repo","query":"agent"},
            {"source_type":"arxiv_paper","title":"Example paper","url":"https://arxiv.org/abs/1234.56789","summary":"metadata","query":"memory"},
            {"source_type":"github_repository","query":"failed query","error":"HTTPError: 403"},
        ]}
        manifest = build_receipts(document, "2026-10-12T12:01:00Z")
        self.assertEqual(manifest["receipt_count"], 2)
        self.assertEqual(manifest["rejected_count"], 1)
        self.assertTrue(all(x["review_status"] == "pending_independent_review" for x in manifest["receipts"]))

    def test_receipt_cli_direct_script_import_smoke(self):
        import subprocess
        import sys
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            inp = root / "input.json"
            out = root / "out.json"
            inp.write_text(json.dumps({"records":[{"url":"https://example.org"}]}), encoding="utf-8")
            proc = subprocess.run([sys.executable, "scripts/scout_verifier.py", str(inp), "--output", str(out)], capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            result = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(result["receipt_count"], 1)


if __name__ == "__main__":
    unittest.main()
