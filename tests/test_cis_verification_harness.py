from benchmarks.cis_verification_harness import evaluate_cases


def sample_cases():
    return [
        {
            "case_id": "good-1",
            "expected_output": "42",
            "observed_output": "42",
            "expected_action": "save",
            "observed_action": "save",
            "detector_flag": False,
            "corrected_output": "42",
            "corrected_action": "save",
        },
        {
            "case_id": "bad-fixed",
            "expected_output": "blue",
            "observed_output": "red",
            "expected_action": "open",
            "observed_action": "close",
            "detector_flag": True,
            "corrected_output": "blue",
            "corrected_action": "open",
        },
        {
            "case_id": "bad-missed",
            "expected_output": "ready",
            "observed_output": "not-ready",
            "expected_action": "commit",
            "observed_action": "commit",
            "detector_flag": False,
            "corrected_output": "not-ready",
            "corrected_action": "commit",
        },
        {
            "case_id": "false-alarm",
            "expected_output": "safe",
            "observed_output": "safe",
            "expected_action": "hold",
            "observed_action": "hold",
            "detector_flag": True,
            "corrected_output": "safe",
            "corrected_action": "hold",
        },
    ]


def test_benchmark_reports_detection_and_correction_metrics():
    report = evaluate_cases(sample_cases())
    assert report["case_count"] == 4
    assert report["confusion_matrix"] == {
        "true_positive": 1,
        "false_positive": 1,
        "false_negative": 1,
        "true_negative": 1,
    }
    assert report["metrics"]["task_success_before"] == 0.5
    assert report["metrics"]["task_success_after"] == 0.75
    assert report["metrics"]["error_detection_precision"] == 0.5
    assert report["metrics"]["error_detection_recall"] == 0.5
    assert report["metrics"]["correction_success_rate_when_flagged"] == 0.5
    assert len(report["input_sha256"]) == 64
    assert len(report["run_sha256"]) == 64


def test_benchmark_is_order_independent_and_repeatable():
    cases = sample_cases()
    first = evaluate_cases(cases)
    second = evaluate_cases(list(reversed(cases)))
    assert first == second


def test_duplicate_case_ids_are_rejected():
    cases = sample_cases()
    cases.append(dict(cases[0]))
    try:
        evaluate_cases(cases)
    except ValueError as exc:
        assert "duplicate case_id" in str(exc)
    else:
        raise AssertionError("duplicate case IDs must be rejected")


def test_missing_fields_are_rejected():
    try:
        evaluate_cases([{"case_id": "incomplete"}])
    except ValueError as exc:
        assert "missing required fields" in str(exc)
    else:
        raise AssertionError("incomplete cases must be rejected")


def test_committed_synthetic_fixture_is_reproducible():
    from pathlib import Path

    from benchmarks.cis_verification_harness import read_jsonl

    fixture = Path(__file__).resolve().parents[1] / "benchmarks" / "data" / "cis_synthetic_cases.jsonl"
    report = evaluate_cases(read_jsonl(fixture))
    assert report["case_count"] == 4
    assert report["metrics"]["task_success_before"] == 0.5
    assert report["metrics"]["task_success_after"] == 0.75
    assert report["metrics"]["error_detection_precision"] == 0.5
    assert report["metrics"]["error_detection_recall"] == 0.5
    assert report["metrics"]["false_positive_rate"] == 0.5
    assert report["metrics"]["corrections_successful"] == 1


def test_zero_denominators_are_defined_as_zero():
    all_correct = [
        {
            "case_id": "only-correct-case",
            "expected_output": "ok",
            "observed_output": "ok",
            "expected_action": "hold",
            "observed_action": "hold",
            "detector_flag": False,
            "corrected_output": "ok",
            "corrected_action": "hold",
        }
    ]
    report = evaluate_cases(all_correct)
    assert report["metrics"]["error_detection_precision"] == 0.0
    assert report["metrics"]["error_detection_recall"] == 0.0
    assert report["metrics"]["false_positive_rate"] == 0.0
    assert report["metrics"]["correction_success_rate_when_flagged"] == 0.0


def test_jsonl_reader_rejects_non_object_records(tmp_path):
    from benchmarks.cis_verification_harness import read_jsonl

    fixture = tmp_path / "bad.jsonl"
    fixture.write_text('["not", "an", "object"]\n', encoding="utf-8")
    try:
        read_jsonl(fixture)
    except ValueError as exc:
        assert "must contain a JSON object" in str(exc)
    else:
        raise AssertionError("non-object JSONL records must be rejected")


def test_jsonl_reader_reports_invalid_json_line(tmp_path):
    from benchmarks.cis_verification_harness import read_jsonl

    fixture = tmp_path / "bad.jsonl"
    fixture.write_text('{"case_id": "valid"}\n{invalid json}\n', encoding="utf-8")
    try:
        read_jsonl(fixture)
    except ValueError as exc:
        assert "invalid JSON on line 2" in str(exc)
    else:
        raise AssertionError("invalid JSON must be rejected with its line number")



def test_cli_appends_to_existing_ledger_without_replacing_history(tmp_path):
    import json
    import subprocess
    import sys
    from pathlib import Path

    repo_root = Path(__file__).resolve().parents[1]
    fixture = repo_root / "benchmarks" / "data" / "cis_synthetic_cases.jsonl"
    ledger = tmp_path / "evidence" / "runs.jsonl"
    ledger.parent.mkdir(parents=True)
    ledger.write_text(json.dumps({"prior_record": "preserve-me"}) + chr(10), encoding="utf-8")

    command = [
        sys.executable,
        str(repo_root / "benchmarks" / "cis_verification_harness.py"),
        str(fixture),
        "--ledger",
        str(ledger),
    ]
    first = subprocess.run(command, check=True, capture_output=True, text=True)
    second = subprocess.run(command, check=True, capture_output=True, text=True)

    records = [json.loads(line) for line in ledger.read_text(encoding="utf-8").splitlines()]
    assert len(records) == 3
    assert records[0] == {"prior_record": "preserve-me"}
    assert records[1]["run_sha256"] == records[2]["run_sha256"]
    assert json.loads(first.stdout)["run_sha256"] == json.loads(second.stdout)["run_sha256"]
