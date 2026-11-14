import hashlib
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import scripts.maia_framework_orchestrator as orchestrator_module
from scripts.maia_framework_orchestrator import MAIAFrameworkOrchestrator


class MAIATrustGateIntegrationTests(unittest.TestCase):
    def test_missing_policy_blocks_plugin_before_import(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            marker = root / "executed.txt"
            plugin = root / "untrusted.py"
            plugin.write_text(
                "from pathlib import Path\n"
                + "Path(" + repr(str(marker)) + ").write_text('executed')\n"
                + "def get_plugin_manifest(): return {'name': 'untrusted'}\n",
                encoding="utf-8",
            )
            with patch.dict(os.environ, {}, clear=True):
                result = MAIAFrameworkOrchestrator().act(
                    "DISCOVER_AND_REGISTER_PLUGIN", plugin_path=str(plugin)
                )
            self.assertFalse(result["success"])
            self.assertEqual(
                result["trust_gate"]["reason"], "TRUST_POLICY_NOT_CONFIGURED"
            )
            self.assertFalse(marker.exists(), "Plugin code executed before policy check")

    def test_allowlisted_plugin_loads_only_after_gate(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            plugin = root / "safe.py"
            plugin.write_text(
                "def get_plugin_manifest(): return {'name': 'safe'}\n"
                "def ping(): return 'pong'\n",
                encoding="utf-8",
            )
            env = {
                "MAIA_PLUGIN_TRUST_ROOT": str(root),
                "MAIA_PLUGIN_ALLOWLIST": "safe.py",
                "MAIA_PLUGIN_SHA256_ALLOWLIST": "safe.py=" + hashlib.sha256(plugin.read_bytes()).hexdigest(),
            }
            with patch.dict(os.environ, env, clear=True):
                orchestrator = MAIAFrameworkOrchestrator()
                result = orchestrator.act(
                    "DISCOVER_AND_REGISTER_PLUGIN", plugin_path=str(plugin)
                )
                self.assertTrue(result["success"])
                invoked = orchestrator.act(
                    "INVOKE_PLUGIN_CAPABILITY",
                    plugin_name="safe",
                    capability_name="ping",
                )
            self.assertEqual(invoked["result"], "pong")


    def test_allowlisted_plugin_without_pinned_digest_is_blocked(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            plugin = root / "safe.py"
            plugin.write_text(
                "def get_plugin_manifest(): return {'name': 'safe'}\n",
                encoding="utf-8",
            )
            env = {
                "MAIA_PLUGIN_TRUST_ROOT": str(root),
                "MAIA_PLUGIN_ALLOWLIST": "safe.py",
            }
            with patch.dict(os.environ, env, clear=True):
                result = MAIAFrameworkOrchestrator().act(
                    "DISCOVER_AND_REGISTER_PLUGIN", plugin_path=str(plugin)
                )
            self.assertFalse(result["success"])
            self.assertEqual(
                result["trust_gate"]["reason"], "TRUST_POLICY_NOT_CONFIGURED"
            )



    def test_loader_executes_validated_bytes_without_reopening_replaced_path(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            marker = root / "executed.txt"
            plugin = root / "safe.py"
            replacement = root / "replacement.py"
            newline = chr(10)
            original_source = newline.join(
                [
                    "from pathlib import Path",
                    f"Path({str(marker)!r}).write_text('original')",
                    "def get_plugin_manifest(): return {'name': 'original'}",
                ]
            ) + newline
            replacement_source = newline.join(
                [
                    "from pathlib import Path",
                    f"Path({str(marker)!r}).write_text('replacement')",
                    "def get_plugin_manifest(): return {'name': 'replacement'}",
                ]
            ) + newline
            plugin.write_text(original_source, encoding="utf-8")
            replacement.write_text(replacement_source, encoding="utf-8")
            env = {
                "MAIA_PLUGIN_TRUST_ROOT": str(root),
                "MAIA_PLUGIN_ALLOWLIST": "safe.py",
                "MAIA_PLUGIN_SHA256_ALLOWLIST": (
                    "safe.py=" + hashlib.sha256(plugin.read_bytes()).hexdigest()
                ),
            }

            real_reader = orchestrator_module.read_trusted_plugin_source

            def read_then_replace(*args, **kwargs):
                result = real_reader(*args, **kwargs)
                os.replace(replacement, plugin)
                return result

            with patch.dict(os.environ, env, clear=True):
                with patch.object(
                    orchestrator_module,
                    "read_trusted_plugin_source",
                    side_effect=read_then_replace,
                ):
                    orchestrator = MAIAFrameworkOrchestrator()
                    result = orchestrator.act(
                        "DISCOVER_AND_REGISTER_PLUGIN", plugin_path=str(plugin)
                    )

            self.assertTrue(result["success"])
            self.assertEqual(result["plugin_name"], "original")
            self.assertEqual(marker.read_text(encoding="utf-8"), "original")

    def test_duplicate_plugin_name_cannot_overwrite_registered_plugin(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            first = root / "first.py"
            second = root / "second.py"
            first.write_text(
                "def get_plugin_manifest(): return {'name': 'shared'}\n"
                "def ping(): return 'first'\n",
                encoding="utf-8",
            )
            second.write_text(
                "def get_plugin_manifest(): return {'name': 'shared'}\n"
                "def ping(): return 'second'\n",
                encoding="utf-8",
            )
            env = {
                "MAIA_PLUGIN_TRUST_ROOT": str(root),
                "MAIA_PLUGIN_ALLOWLIST": "first.py,second.py",
                "MAIA_PLUGIN_SHA256_ALLOWLIST": (
                    "first.py=" + hashlib.sha256(first.read_bytes()).hexdigest()
                    + ",second.py=" + hashlib.sha256(second.read_bytes()).hexdigest()
                ),
            }
            with patch.dict(os.environ, env, clear=True):
                orchestrator = MAIAFrameworkOrchestrator()
                accepted = orchestrator.act(
                    "DISCOVER_AND_REGISTER_PLUGIN", plugin_path=str(first)
                )
                original_module = orchestrator.loaded_plugins["shared"]
                rejected = orchestrator.act(
                    "DISCOVER_AND_REGISTER_PLUGIN", plugin_path=str(second)
                )
                invoked = orchestrator.act(
                    "INVOKE_PLUGIN_CAPABILITY",
                    plugin_name="shared",
                    capability_name="ping",
                )
            self.assertTrue(accepted["success"])
            self.assertFalse(rejected["success"])
            self.assertIn("Duplicate plugin name rejected", rejected["error"])
            self.assertIs(orchestrator.loaded_plugins["shared"], original_module)
            self.assertEqual(invoked["result"], "first")



if __name__ == "__main__":
    unittest.main()
