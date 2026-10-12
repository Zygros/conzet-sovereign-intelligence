import unittest

from genesis.execution_receipts import validate_receipt


def sample(**overrides):
    receipt = {
        "receipt_version": "conzetian-execution-receipt/1.0",
        "action_id": "test-001",
        "action": "run_unit_tests",
        "status": "VERIFIED",
        "executed": True,
        "result": {"tests_passed": 3},
        "evidence_refs": ["ci://run/123"],
        "verification": {"method": "CI run and test summary", "passed": True},
    }
    receipt.update(overrides)
    return receipt


class ExecutionReceiptTests(unittest.TestCase):
    def test_valid_verified_receipt(self):
        self.assertEqual(validate_receipt(sample()), [])

    def test_verified_without_execution_is_rejected(self):
        errors = validate_receipt(sample(executed=False))
        self.assertTrue(any("requires executed=true" in error for error in errors))

    def test_verified_without_evidence_is_rejected(self):
        errors = validate_receipt(sample(evidence_refs=[]))
        self.assertTrue(any("evidence reference" in error for error in errors))

    def test_verified_without_passed_verification_is_rejected(self):
        errors = validate_receipt(sample(verification={"method": "manual", "passed": False}))
        self.assertTrue(any("verification.passed=true" in error for error in errors))

    def test_planned_cannot_claim_execution(self):
        errors = validate_receipt(sample(status="PLANNED", executed=True))
        self.assertTrue(any("cannot claim executed=true" in error for error in errors))

    def test_bad_evidence_shape_is_rejected(self):
        errors = validate_receipt(sample(evidence_refs=["", 7]))
        self.assertTrue(any("non-empty strings" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
