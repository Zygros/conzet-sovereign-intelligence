import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "agent_activation_plan.py"
REGISTRY = ROOT / "agents" / "registry.json"


class AgentActivationPlanTests(unittest.TestCase):
    def test_registry_validates_and_plan_is_explicitly_non_running(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--registry", str(REGISTRY)],
            check=True, capture_output=True, text=True,
        )
        plan = json.loads(result.stdout)
        self.assertEqual(plan["status"], "PLAN_GENERATED_NO_WORKERS_STARTED")
        self.assertGreaterEqual(plan["agent_count"], 8)
        self.assertTrue(all(
            item["status"] == "DEFINED_READY_FOR_RUNTIME_BINDING"
            for item in plan["dispatch_plan"]
        ))
        self.assertTrue(all(
            item["requires_approval_for_side_effects"]
            for item in plan["dispatch_plan"]
        ))

    def test_duplicate_agent_ids_are_rejected(self):
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        registry["agents"].append(dict(registry["agents"][0]))
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "registry.json"
            path.write_text(json.dumps(registry), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--registry", str(path), "--validate-only"],
                capture_output=True, text=True,
            )
        self.assertEqual(result.returncode, 2)
        self.assertIn("agent IDs must be unique", result.stdout)

    def test_unknown_dependency_is_rejected(self):
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        registry["agents"][0]["depends_on"] = ["missing_agent"]
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "registry.json"
            path.write_text(json.dumps(registry), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--registry", str(path), "--validate-only"],
                capture_output=True, text=True,
            )
        self.assertEqual(result.returncode, 2)
        self.assertIn("unknown dependency", result.stdout)


if __name__ == "__main__":
    unittest.main()
