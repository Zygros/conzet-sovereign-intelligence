import copy
import json
import tempfile
import unittest
from pathlib import Path

from scripts.scout_duplicate_audit import audit_document, canonicalize_url, normalize_title

LONG_DESCRIPTION = (
    "A protocol-first interoperability layer for agent systems with cross-vendor governance "
    "and tamper-evident review metadata, designed to preserve provenance and independent auditability."
)


class ScoutDuplicateAuditTests(unittest.TestCase):
    def test_github_repository_url_canonicalization(self):
        self.assertEqual(
            canonicalize_url("HTTPS://GitHub.com/Owner/Repo.git/?tab=readme#top"),
            "https://github.com/owner/repo",
        )

    def test_invalid_or_non_http_url_is_ignored(self):
        self.assertIsNone(canonicalize_url("javascript:alert(1)"))
        self.assertIsNone(canonicalize_url(""))
        self.assertIsNone(canonicalize_url(None))

    def test_canonical_url_duplicate_is_review_signal_only(self):
        report = audit_document({"records": [
            {"title": "Repo A", "url": "https://github.com/OWNER/Repo"},
            {"title": "Different title", "url": "https://github.com/owner/repo.git/"},
        ]})
        self.assertEqual(report["summary"]["canonical_url_duplicate_groups"], 1)
        group = next(x for x in report["signals"] if x["signal_type"] == "canonical_url_duplicate")
        self.assertEqual(group["classification"], "REVIEW_SIGNAL_ONLY")
        self.assertEqual(group["record_count"], 2)

    def test_exact_url_duplicate_is_separately_reported(self):
        report = audit_document({"records": [
            {"title": "A", "url": "https://example.test/repo"},
            {"title": "B", "url": "https://example.test/repo"},
        ]})
        self.assertEqual(report["summary"]["exact_url_duplicate_groups"], 1)
        self.assertEqual(report["summary"]["canonical_url_duplicate_groups"], 1)

    def test_normalized_title_duplicate_is_found(self):
        self.assertEqual(normalize_title("  AGENT-Bridge! "), "agent bridge")
        report = audit_document({"records": [
            {"title": "Agent-Bridge!", "url": "https://example.test/a"},
            {"title": "AGENT bridge", "url": "https://example.test/b"},
        ]})
        self.assertEqual(report["summary"]["normalized_title_duplicate_groups"], 1)

    def test_identical_long_description_is_found(self):
        report = audit_document({"records": [
            {"title": "A", "url": "https://example.test/a", "description": LONG_DESCRIPTION},
            {"title": "B", "url": "https://example.test/b", "description": LONG_DESCRIPTION.upper()},
        ]})
        self.assertEqual(report["summary"]["identical_long_description_groups"], 1)

    def test_cross_owner_same_slug_and_description_is_flagged(self):
        report = audit_document({"records": [
            {"title": "A", "url": "https://github.com/owner-one/agent-bridge", "description": LONG_DESCRIPTION},
            {"title": "B", "url": "https://github.com/owner-two/AGENT-BRIDGE.git", "description": LONG_DESCRIPTION},
        ]})
        self.assertEqual(report["summary"]["same_github_slug_and_long_description_groups"], 1)

    def test_short_generic_descriptions_are_not_flagged(self):
        report = audit_document({"records": [
            {"title": "A", "url": "https://example.test/a", "description": "AI agent tools"},
            {"title": "B", "url": "https://example.test/b", "description": "AI agent tools"},
        ]})
        self.assertEqual(report["summary"]["identical_long_description_groups"], 0)
        self.assertEqual(report["summary"]["same_github_slug_and_long_description_groups"], 0)

    def test_input_is_not_mutated_and_output_is_deterministic(self):
        document = {"generated_at": "2026-10-24T00:00:00Z", "records": [
            {"title": "A", "url": "https://example.test/a"},
            {"title": "B", "url": "https://example.test/b"},
        ]}
        original = copy.deepcopy(document)
        self.assertEqual(audit_document(document), audit_document(document))
        self.assertEqual(document, original)

    def test_missing_records_array_is_rejected(self):
        with self.assertRaises(ValueError):
            audit_document({"generated_at": "2026-10-24"})

    def test_invalid_record_object_is_rejected(self):
        with self.assertRaises(ValueError):
            audit_document({"records": [{"title": "A"}, "not-a-record"]})

    def test_output_is_json_serializable(self):
        report = audit_document({"records": []})
        parsed = json.loads(json.dumps(report, sort_keys=True))
        self.assertEqual(parsed["summary"]["records_scanned"], 0)

    def test_cli_style_file_output_preserves_input(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "input.json"
            output = root / "audit.json"
            source_document = {"records": [{"title": "A", "url": "https://example.test/a"}]}
            source_text = json.dumps(source_document)
            source.write_text(source_text, encoding="utf-8")
            report = audit_document(json.loads(source.read_text(encoding="utf-8")))
            output.write_text(json.dumps(report), encoding="utf-8")
            self.assertEqual(source.read_text(encoding="utf-8"), source_text)
            self.assertEqual(json.loads(output.read_text(encoding="utf-8"))["summary"]["records_scanned"], 1)


if __name__ == "__main__":
    unittest.main()
