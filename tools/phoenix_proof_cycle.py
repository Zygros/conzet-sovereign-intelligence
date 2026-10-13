#!/usr/bin/env python3
"""Local deterministic Phoenix proof cycle with a tamper-evident ledger.

This fixture verifies the verification machinery only. It does not claim external
AI execution, web research, Bitcoin/Arweave anchoring, or production deployment.
"""
import argparse
import hashlib
import json
import sys
import unittest
from datetime import datetime, timezone

SCHEMA = "phoenix-proof-cycle/1.0"
GENESIS = "0" * 64

def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

def digest(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()

def append(ledger, event, payload):
    body = {"sequence": len(ledger) + 1,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": event, "payload": payload,
            "previous_hash": ledger[-1]["hash"] if ledger else GENESIS,
            "schema": SCHEMA}
    record = dict(body, hash=digest(canonical(body)))
    ledger.append(record)
    return record

def verify_ledger(ledger):
    previous = GENESIS
    for index, record in enumerate(ledger, 1):
        if record.get("sequence") != index:
            return False, f"sequence mismatch at {index}"
        if record.get("previous_hash") != previous:
            return False, f"chain link mismatch at {index}"
        body = {key: value for key, value in record.items() if key != "hash"}
        if record.get("hash") != digest(canonical(body)):
            return False, f"content hash mismatch at {index}"
        previous = record["hash"]
    return True, f"verified {len(ledger)} events"

def validate(finding):
    if not isinstance(finding, dict):
        return ["finding must be an object"]
    errors = [f"{key} must be a non-empty string"
              for key in ("id", "title", "evidence")
              if not isinstance(finding.get(key), str) or not finding[key].strip()]
    if "confidence" in finding:
        value = finding["confidence"]
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not 0 <= value <= 1:
            errors.append("confidence must be a number in [0, 1]")
    return errors

def run_cycle(task, inject_defect=False, repair=True):
    if not isinstance(task, str) or not task.strip():
        raise ValueError("task must be a non-empty string")
    ledger = []
    append(ledger, "cycle.started", {"task": task.strip()})
    finding = {"id": "finding-001", "title": f"Execution candidate: {task.strip()}",
               "evidence": "Deterministic local fixture; no external research performed.",
               "confidence": 0.5}
    if inject_defect:
        finding["evidence"] = ""
    append(ledger, "scout.completed", {"source": "deterministic-local-fixture", "count": 1})
    errors = validate(finding)
    append(ledger, "verifier.completed", {"valid": not errors, "errors": errors})
    status = "PASS"
    original_errors = list(errors)
    if errors:
        status = "FAIL"
        if repair:
            if not finding.get("id", "").strip():
                finding["id"] = "repaired-001"
            if not finding.get("title", "").strip():
                finding["title"] = "Repaired finding title"
            if not finding.get("evidence", "").strip():
                finding["evidence"] = "Repair applied; original evidence was empty."
            append(ledger, "repair.applied", {"repair_count": 1})
            errors_after = validate(finding)
            append(ledger, "verifier.recheck", {"valid": not errors_after, "errors": errors_after})
            status = "REPAIRED" if not errors_after else "FAIL"
    append(ledger, "cycle.finished", {"status": status})
    valid, message = verify_ledger(ledger)
    payload = {"schema": SCHEMA, "status": status, "finding": finding,
               "errors_before_repair": original_errors, "ledger": ledger,
               "ledger_valid": valid, "ledger_message": message,
               "evidence_boundary": {"external_ai": False, "web_research": False,
                 "bitcoin_anchor": False, "arweave_anchor": False, "ots_anchor": False}}
    payload["export_sha256"] = digest(canonical(payload))
    return payload

def verify_export(raw):
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        return False, f"invalid JSON: {exc}"
    supplied = payload.pop("export_sha256", None)
    if not isinstance(supplied, str) or supplied != digest(canonical(payload)):
        return False, "export hash mismatch"
    ok, message = verify_ledger(payload.get("ledger", []))
    return (ok, f"export and {message}" if ok else message)

class Tests(unittest.TestCase):
    def test_clean_cycle(self):
        result = run_cycle("baseline")
        self.assertEqual(result["status"], "PASS")
        self.assertTrue(result["ledger_valid"])
    def test_seeded_defect_repaired_and_reverified(self):
        result = run_cycle("seeded fault", inject_defect=True)
        self.assertEqual(result["status"], "REPAIRED")
        self.assertIn("evidence must be a non-empty string", result["errors_before_repair"])
        self.assertFalse(validate(result["finding"]))
    def test_no_repair_fails_visibly(self):
        self.assertEqual(run_cycle("seeded fault", True, False)["status"], "FAIL")
    def test_ledger_tampering_detected(self):
        result = run_cycle("tamper")
        altered = json.loads(json.dumps(result["ledger"]))
        altered[0]["payload"]["task"] = "changed"
        self.assertFalse(verify_ledger(altered)[0])
    def test_export_roundtrip_and_tamper(self):
        result = run_cycle("export")
        raw = json.dumps(result)
        self.assertTrue(verify_export(raw)[0])
        altered = json.loads(raw)
        altered["finding"]["title"] = "tampered"
        self.assertFalse(verify_export(json.dumps(altered))[0])
    def test_empty_task_rejected(self):
        with self.assertRaises(ValueError):
            run_cycle("  ")

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", default="Phoenix proof-to-product cycle")
    parser.add_argument("--inject-defect", action="store_true")
    parser.add_argument("--no-repair", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--output")
    args = parser.parse_args()
    if args.self_test:
        result = unittest.TextTestRunner(verbosity=2).run(
            unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
        return 0 if result.wasSuccessful() else 1
    result = run_cycle(args.task, args.inject_defect, not args.no_repair)
    raw = json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(raw + "\n")
    else:
        print(raw)
    print(f"Cycle={result['status']} | {result['ledger_message']}", file=sys.stderr)
    return 0 if result["status"] in ("PASS", "REPAIRED") and result["ledger_valid"] else 2

if __name__ == "__main__":
    raise SystemExit(main())
