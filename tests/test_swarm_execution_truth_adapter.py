import unittest

from genesis.swarm_execution_truth_adapter import build_evidence_gated_report

class SwarmExecutionTruthAdapterTests(unittest.TestCase):
    def test_legacy_swarm_and_channel_labels_are_not_trusted(self):
        result = build_evidence_gated_report()
        self.assertEqual(result["report"]["verdict"], "EVIDENCE_GATED_REVIEW_REQUIRED")
        self.assertEqual(result["report"]["swarms_reported"], 10)
        self.assertEqual(result["report"]["swarms_without_acceptable_receipts"], 10)
        self.assertEqual(result["report"]["channels_propagated_verified"], 0)
        self.assertTrue(all(x["status"] == "SIMULATED" for x in result["swarms"].values()))
        self.assertTrue(all(x["status"] == "SIMULATED" for x in result["channels"].values()))

    def test_adapter_preserves_legacy_claim_as_audit_field(self):
        result = build_evidence_gated_report()
        self.assertEqual(result["report"]["legacy_report_verdict"], "ALL SWARMS ONLINE — LATTICE COHERENT")

    def test_valid_shaped_receipt_does_not_claim_final_verification(self):
        receipt = {
            "schema": "conzetian-execution-receipt/1.0",
            "action_id": "swarm:1",
            "adapter_id": "reviewed-adapter",
            "execution": True,
            "verification_status": "PASSED",
            "evidence_refs": ["artifact://receipt-1"],
        }
        result = build_evidence_gated_report({"swarm:1": receipt})
        first = result["swarms"]["ArXiv-Automaton"]
        self.assertEqual(first["status"], "EXECUTED_PENDING_EVIDENCE_REVIEW")
        self.assertEqual(result["report"]["swarms_with_receipts_pending_review"], 1)

if __name__ == "__main__":
    unittest.main()
