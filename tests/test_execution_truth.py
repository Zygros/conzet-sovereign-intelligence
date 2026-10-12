import unittest

from genesis.execution_truth import classify_record, RECEIPT_SCHEMA

class ExecutionTruthTests(unittest.TestCase):
    def test_legacy_executed_label_is_downgraded_without_receipt(self):
        result = classify_record({"status": "EXECUTED", "name": "legacy"})
        self.assertEqual(result["status"], "SIMULATED")
        self.assertEqual(result["evidence_verdict"], "NO_EXECUTION_RECEIPT")

    def test_invalid_receipt_does_not_upgrade_status(self):
        result = classify_record({"status": "PROPAGATED"}, {"execution": True})
        self.assertEqual(result["status"], "SIMULATED")
        self.assertEqual(result["evidence_verdict"], "RECEIPT_INVALID_OR_INCOMPLETE")

    def test_structurally_valid_receipt_stays_pending_review(self):
        receipt = {
            "schema": RECEIPT_SCHEMA, "action_id": "a-1", "adapter_id": "trusted-adapter-1",
            "execution": True, "verification_status": "PASSED", "evidence_refs": ["https://example.invalid/evidence/1"]
        }
        result = classify_record({"status": "EXECUTED"}, receipt)
        self.assertEqual(result["status"], "EXECUTED_PENDING_EVIDENCE_REVIEW")
        self.assertIn("NOT_INDEPENDENTLY_VERIFIED", result["evidence_verdict"])

    def test_empty_evidence_is_rejected(self):
        receipt = {
            "schema": RECEIPT_SCHEMA, "action_id": "a-1", "adapter_id": "adapter",
            "execution": True, "verification_status": "PASSED", "evidence_refs": []
        }
        self.assertEqual(classify_record({}, receipt)["status"], "SIMULATED")

    def test_input_record_is_not_mutated(self):
        source = {"status": "EXECUTED"}
        classify_record(source)
        self.assertEqual(source["status"], "EXECUTED")

if __name__ == "__main__":
    unittest.main()
