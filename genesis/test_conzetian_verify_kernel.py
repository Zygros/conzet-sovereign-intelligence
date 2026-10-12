import hashlib
import tempfile
import unittest
from pathlib import Path
import conzetian_verify_kernel as kernel

class KernelTests(unittest.TestCase):
    def test_hash_matches_stdlib(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "sample.bin"
            p.write_bytes(b"conzetian evidence")
            digest, size = kernel.sha256_file(p)
            self.assertEqual(digest, hashlib.sha256(p.read_bytes()).hexdigest())
            self.assertEqual(size, len(p.read_bytes()))

    def test_inventory_is_read_only_and_sorted(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "b.txt").write_text("b")
            (root / "a.txt").write_text("a")
            before = {p.name: p.read_bytes() for p in root.iterdir()}
            rows = kernel.inventory(root)
            self.assertEqual([r["path"] for r in rows], ["a.txt", "b.txt"])
            self.assertEqual(before, {p.name: p.read_bytes() for p in root.iterdir()})

    def test_append_and_validate(self):
        with tempfile.TemporaryDirectory() as td:
            ledger = Path(td) / "ledger.jsonl"
            kernel.append_event(ledger, "TEST", {"result": "PASS"})
            count, errors = kernel.validate_ledger(ledger)
            self.assertEqual(count, 1)
            self.assertEqual(errors, [])

    def test_malformed_ledger_is_detected(self):
        with tempfile.TemporaryDirectory() as td:
            ledger = Path(td) / "bad.jsonl"
            ledger.write_text("{broken}\n")
            count, errors = kernel.validate_ledger(ledger)
            self.assertEqual(count, 0)
            self.assertTrue(errors)

if __name__ == "__main__":
    unittest.main(verbosity=2)
