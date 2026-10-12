import hashlib
import tempfile
import unittest
from pathlib import Path

from genesis.plugin_trust_policy import validate_plugin_path


class PluginTrustPolicyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "trusted"
        self.root.mkdir()
        self.plugin = self.root / "safe_plugin.py"
        self.payload = b"def get_plugin_manifest():\n    return {'name': 'safe'}\n"
        self.plugin.write_bytes(self.payload)

    def tearDown(self):
        self.temp.cleanup()

    def test_allowlisted_file_passes_without_execution(self):
        result = validate_plugin_path(
            "safe_plugin.py", str(self.root), ["safe_plugin.py"],
            hashlib.sha256(self.payload).hexdigest(),
        )
        self.assertTrue(result["allowed"])
        self.assertFalse(result["execution_performed"])
        self.assertEqual(result["safety_verdict"], "NOT_ASSESSED")

    def test_unlisted_plugin_is_rejected(self):
        result = validate_plugin_path(
            "safe_plugin.py", str(self.root), ["other.py"]
        )
        self.assertFalse(result["allowed"])
        self.assertEqual(result["reason"], "PLUGIN_NOT_ALLOWLISTED")

    def test_digest_mismatch_is_rejected(self):
        result = validate_plugin_path(
            "safe_plugin.py", str(self.root), ["safe_plugin.py"], "0" * 64
        )
        self.assertFalse(result["allowed"])
        self.assertEqual(result["reason"], "SHA256_MISMATCH")

    def test_parent_traversal_is_rejected(self):
        outside = Path(self.temp.name) / "outside.py"
        outside.write_text("# outside", encoding="utf-8")
        result = validate_plugin_path(
            "../outside.py", str(self.root), ["../outside.py"]
        )
        self.assertFalse(result["allowed"])
        self.assertEqual(result["reason"], "PATH_OUTSIDE_TRUSTED_ROOT")

    def test_symlink_is_rejected(self):
        target = self.root / "target.py"
        target.write_text("# target", encoding="utf-8")
        link = self.root / "linked.py"
        try:
            link.symlink_to(target)
        except (OSError, NotImplementedError):
            self.skipTest("Symlinks are not available on this platform")
        result = validate_plugin_path("linked.py", str(self.root), ["linked.py"])
        self.assertFalse(result["allowed"])
        self.assertEqual(result["reason"], "SYMLINK_NOT_ALLOWED")

    def test_missing_file_is_rejected(self):
        result = validate_plugin_path(
            "missing.py", str(self.root), ["missing.py"]
        )
        self.assertFalse(result["allowed"])
        self.assertEqual(result["reason"], "PLUGIN_FILE_NOT_FOUND")


if __name__ == "__main__":
    unittest.main()
