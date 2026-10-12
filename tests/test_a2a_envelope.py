import unittest

from scripts.a2a_envelope import validate_envelope


def valid_envelope():
    return {
        "protocol_version": "1.0",
        "message_id": "msg-001",
        "task_id": "task-001",
        "parent_task_id": None,
        "sender": "scout",
        "recipient": "verifier",
        "task_type": "verify_source",
        "created_at": "2026-10-12T23:30:00Z",
        "deadline": "2026-10-12T23:35:00+00:00",
        "permissions": {
            "scopes": ["source:read", "evidence:write"],
            "sensitive_action_confirmation": True,
        },
        "payload": {"url": "https://example.org/spec"},
        "evidence": [
            {
                "kind": "source",
                "uri": "https://example.org/spec",
                "sha256": "a" * 64,
            }
        ],
        "provenance": {
            "source_refs": ["https://example.org/spec"],
            "producer": "Sovereign Opportunity Scout",
            "schema_version": "1.0",
            "repository_commit": "abc123",
        },
        "status": "submitted",
    }


class A2AEnvelopeTests(unittest.TestCase):
    def test_valid_envelope_passes(self):
        self.assertEqual(validate_envelope(valid_envelope()), [])

    def test_missing_task_id_fails(self):
        envelope = valid_envelope()
        del envelope["task_id"]
        self.assertTrue(any("task_id" in error for error in validate_envelope(envelope)))

    def test_timezone_required(self):
        envelope = valid_envelope()
        envelope["created_at"] = "2026-10-12T23:30:00"
        self.assertTrue(any("timezone" in error for error in validate_envelope(envelope)))

    def test_duplicate_permission_scopes_fail(self):
        envelope = valid_envelope()
        envelope["permissions"]["scopes"] = ["source:read", "source:read"]
        self.assertTrue(any("duplicates" in error for error in validate_envelope(envelope)))

    def test_malformed_evidence_hash_fails(self):
        envelope = valid_envelope()
        envelope["evidence"][0]["sha256"] = "not-a-hash"
        self.assertTrue(any("sha256" in error for error in validate_envelope(envelope)))

    def test_unknown_top_level_field_fails(self):
        envelope = valid_envelope()
        envelope["execute_arbitrary_code"] = True
        self.assertTrue(any("unknown fields" in error for error in validate_envelope(envelope)))

    def test_sensitive_confirmation_must_be_boolean(self):
        envelope = valid_envelope()
        envelope["permissions"]["sensitive_action_confirmation"] = "yes"
        self.assertTrue(any("must be boolean" in error for error in validate_envelope(envelope)))


if __name__ == "__main__":
    unittest.main()
