"""Reproducible, ground-truth-based evaluation scaffold for the CIS verification loop.

This harness scores supplied detector flags and correction outputs against explicit
expected outcomes. It does not itself provide an intelligent detector, and a passing
synthetic test does not establish production performance.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def _matches(case: Dict[str, Any], prefix: str) -> bool:
    expected_output = case["expected_output"]
    observed_output = case[f"{prefix}_output"]
    expected_action = case["expected_action"]
    observed_action = case[f"{prefix}_action"]
    return (
        observed_output == expected_output
        and observed_action == expected_action
    )


def evaluate_cases(cases: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    """Evaluate supplied cases and produce deterministic metrics plus hashes."""
    materialized: List[Dict[str, Any]] = [dict(case) for case in cases]
    required = {
        "case_id",
        "expected_output",
        "observed_output",
        "expected_action",
        "observed_action",
        "detector_flag",
        "corrected_output",
        "corrected_action",
    }
    seen = set()
    for case in materialized:
        missing = required.difference(case)
        if missing:
            raise ValueError(
                "case missing required fields: " + ", ".join(sorted(missing))
            )
        if case["case_id"] in seen:
            raise ValueError("duplicate case_id: " + str(case["case_id"]))
        seen.add(case["case_id"])
        if not isinstance(case["detector_flag"], bool):
            raise ValueError("detector_flag must be a boolean")

    materialized.sort(key=lambda item: str(item["case_id"]))
    records = []
    tp = fp = fn = tn = 0
    before_success = after_success = corrections_attempted = corrections_successful = 0

    for case in materialized:
        observed_correct = _matches(case, "observed")
        corrected_correct = _matches(case, "corrected")
        actual_error = not observed_correct
        detected = case["detector_flag"]

        if detected and actual_error:
            tp += 1
        elif detected and not actual_error:
            fp += 1
        elif not detected and actual_error:
            fn += 1
        else:
            tn += 1

        before_success += int(observed_correct)
        after_success += int(corrected_correct)
        if detected:
            corrections_attempted += 1
            corrections_successful += int(corrected_correct)

        records.append(
            {
                "case_id": case["case_id"],
                "actual_error": actual_error,
                "detector_flag": detected,
                "correct_before": observed_correct,
                "correct_after": corrected_correct,
                "correction_improved": (not observed_correct) and corrected_correct,
            }
        )

    total = len(materialized)

    def ratio(numerator: int, denominator: int) -> float:
        return numerator / denominator if denominator else 0.0

    report: Dict[str, Any] = {
        "schema_version": "cis-verification-benchmark/1.0",
        "case_count": total,
        "metrics": {
            "task_success_before": ratio(before_success, total),
            "task_success_after": ratio(after_success, total),
            "error_detection_precision": ratio(tp, tp + fp),
            "error_detection_recall": ratio(tp, tp + fn),
            "false_positive_rate": ratio(fp, fp + tn),
            "correction_success_rate_when_flagged": ratio(
                corrections_successful, corrections_attempted
            ),
            "corrections_attempted": corrections_attempted,
            "corrections_successful": corrections_successful,
        },
        "confusion_matrix": {
            "true_positive": tp,
            "false_positive": fp,
            "false_negative": fn,
            "true_negative": tn,
        },
        "cases": records,
        "input_sha256": hashlib.sha256(_canonical_bytes(materialized)).hexdigest(),
    }
    report["run_sha256"] = hashlib.sha256(_canonical_bytes(report)).hexdigest()
    return report


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    cases = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if line.strip():
                try:
                    value = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise ValueError(
                        f"invalid JSON on line {line_number}: {exc}"
                    ) from exc
                if not isinstance(value, dict):
                    raise ValueError(f"line {line_number} must contain a JSON object")
                cases.append(value)
    return cases


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="JSONL file containing benchmark cases")
    parser.add_argument(
        "--ledger",
        type=Path,
        help="optional append-only JSONL evidence ledger; existing records are never replaced",
    )
    args = parser.parse_args()
    report = evaluate_cases(read_jsonl(args.input))
    serialized = json.dumps(report, sort_keys=True, indent=2, ensure_ascii=False)
    print(serialized)
    if args.ledger:
        args.ledger.parent.mkdir(parents=True, exist_ok=True)
        with args.ledger.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(report, sort_keys=True, ensure_ascii=False) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
