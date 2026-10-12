import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

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


if __name__ == "__main__":
    unittest.main()
