import json, tempfile, unittest
from pathlib import Path
from genesis.daemon_endowment import load_registry, plan_cycle

def registry(daemons):
    return {"schema": "conzetian-daemon-registry/1.0", "daemons": daemons}

class DaemonEndowmentTests(unittest.TestCase):
    def test_cycle_only_plans_enabled_daemons(self):
        r = registry([{"id":"a","purpose":"observe","mode":"observe","enabled":True},{"id":"b","purpose":"off","mode":"plan","enabled":False}])
        tasks = plan_cycle(r, "cycle-1")
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["state"], "PLANNED")
        self.assertFalse(tasks[0]["automatic_execution"])
    def test_verify_mode_starts_blocked(self):
        r = registry([{"id":"v","purpose":"verify","mode":"verify","enabled":True}])
        self.assertEqual(plan_cycle(r, "cycle-2")[0]["state"], "BLOCKED")
    def test_duplicate_ids_rejected(self):
        r = registry([{"id":"x","purpose":"a","mode":"plan","enabled":True},{"id":"x","purpose":"b","mode":"plan","enabled":True}])
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "registry.json"
            p.write_text(json.dumps(r))
            with self.assertRaisesRegex(ValueError, "duplicate daemon id"): load_registry(p)
    def test_external_adapter_cannot_be_declared_in_json(self):
        r = registry([{"id":"x","purpose":"a","mode":"plan","enabled":True,"adapter":"arbitrary-shell"}])
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "registry.json"
            p.write_text(json.dumps(r))
            with self.assertRaisesRegex(ValueError, "trusted runtime"): load_registry(p)
    def test_bad_cycle_id_rejected(self):
        with self.assertRaises(ValueError): plan_cycle(registry([]), "")

if __name__ == "__main__": unittest.main()