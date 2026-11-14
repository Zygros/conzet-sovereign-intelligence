import hashlib
import os
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

import genesis.plugin_trust_policy as policy
from genesis.plugin_trust_policy import read_trusted_plugin_source

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
        self.assertIn(result["reason"], ("PATH_TRAVERSAL", "PATH_OUTSIDE_TRUSTED_ROOT"))

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


    def _with_uid(self, info, uid):
        return SimpleNamespace(
            st_mode=info.st_mode,
            st_uid=uid,
            st_dev=info.st_dev,
            st_ino=info.st_ino,
            st_size=info.st_size,
            st_mtime_ns=info.st_mtime_ns,
            st_ctime_ns=info.st_ctime_ns,
        )

    def test_read_returns_the_exact_bytes_hashed_from_the_descriptor(self):
        result = read_trusted_plugin_source(
            "safe_plugin.py", str(self.root), ["safe_plugin.py"],
            hashlib.sha256(self.payload).hexdigest(),
        )
        self.assertTrue(result["allowed"])
        self.assertEqual(result["source_bytes"], self.payload)
        self.assertEqual(result["sha256"], hashlib.sha256(self.payload).hexdigest())

    def test_untrusted_plugin_file_owner_is_rejected(self):
        if not callable(getattr(os, "geteuid", None)):
            self.skipTest("POSIX ownership checks are unavailable")
        untrusted_uid = os.geteuid() + 100000
        real_stat = os.stat

        def fake_stat(path, *args, **kwargs):
            info = real_stat(path, *args, **kwargs)
            if os.path.abspath(os.fspath(path)) == os.path.abspath(self.plugin):
                return self._with_uid(info, untrusted_uid)
            return info

        with mock.patch.object(policy.os, "stat", side_effect=fake_stat):
            result = read_trusted_plugin_source(
                "safe_plugin.py", str(self.root), ["safe_plugin.py"]
            )
        self.assertFalse(result["allowed"])
        self.assertEqual(result["reason"], "UNTRUSTED_PLUGIN_OWNER")

    def test_untrusted_descendant_directory_owner_is_rejected(self):
        if not callable(getattr(os, "geteuid", None)):
            self.skipTest("POSIX ownership checks are unavailable")
        untrusted_uid = os.geteuid() + 100000
        nested = self.root / "nested"
        nested.mkdir()
        plugin = nested / "safe.py"
        plugin.write_bytes(self.payload)
        real_stat = os.stat

        def fake_stat(path, *args, **kwargs):
            info = real_stat(path, *args, **kwargs)
            if os.path.abspath(os.fspath(path)) == os.path.abspath(nested):
                return self._with_uid(info, untrusted_uid)
            return info

        with mock.patch.object(policy.os, "stat", side_effect=fake_stat):
            result = read_trusted_plugin_source(
                "nested/safe.py", str(self.root), ["nested/safe.py"]
            )
        self.assertFalse(result["allowed"])
        self.assertEqual(result["reason"], "UNTRUSTED_PATH_OWNER")

    def test_untrusted_ancestor_owner_is_rejected(self):
        if not callable(getattr(os, "geteuid", None)):
            self.skipTest("POSIX ownership checks are unavailable")
        untrusted_uid = os.geteuid() + 100000
        ancestor = self.root.parent
        real_stat = os.stat

        def fake_stat(path, *args, **kwargs):
            info = real_stat(path, *args, **kwargs)
            if os.path.abspath(os.fspath(path)) == os.path.abspath(ancestor):
                return self._with_uid(info, untrusted_uid)
            return info

        with mock.patch.object(policy.os, "stat", side_effect=fake_stat):
            result = read_trusted_plugin_source(
                "safe_plugin.py", str(self.root), ["safe_plugin.py"]
            )
        self.assertFalse(result["allowed"])
        self.assertEqual(result["reason"], "UNTRUSTED_PATH_OWNER")

    def test_untrusted_open_descriptor_owner_is_rejected(self):
        if not callable(getattr(os, "geteuid", None)):
            self.skipTest("POSIX ownership checks are unavailable")
        untrusted_uid = os.geteuid() + 100000
        real_fstat = os.fstat

        def fake_fstat(fd):
            return self._with_uid(real_fstat(fd), untrusted_uid)

        with mock.patch.object(policy.os, "fstat", side_effect=fake_fstat):
            result = read_trusted_plugin_source(
                "safe_plugin.py", str(self.root), ["safe_plugin.py"]
            )
        self.assertFalse(result["allowed"])
        self.assertEqual(result["reason"], "UNTRUSTED_DESCRIPTOR_OWNER")

    def test_path_replacement_after_open_is_rejected(self):
        replacement = self.root / "replacement.py"
        replacement.write_text("# replacement\n", encoding="utf-8")
        real_open = os.open
        swapped = {"value": False}

        def racing_open(path, flags, *args, **kwargs):
            descriptor = real_open(path, flags, *args, **kwargs)
            if os.path.abspath(os.fspath(path)) == os.path.abspath(self.plugin):
                os.replace(replacement, self.plugin)
                swapped["value"] = True
            return descriptor

        with mock.patch.object(policy.os, "open", side_effect=racing_open):
            result = read_trusted_plugin_source(
                "safe_plugin.py", str(self.root), ["safe_plugin.py"]
            )
        self.assertTrue(swapped["value"])
        self.assertFalse(result["allowed"])
        self.assertIn(result["reason"], ("FILE_PATH_REPLACED", "FILE_IDENTITY_CHANGED"))

if __name__ == "__main__":
    unittest.main()
