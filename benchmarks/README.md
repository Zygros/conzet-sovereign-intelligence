# CIS Verification Benchmark — First Reproducible Run

This directory contains an evaluation harness for the verification layer in the Conzet Intelligence System (CIS).

## What it does
- Accepts JSONL test cases with explicit expected output/action, observed output/action, detector flag, and corrected output/action.
- Computes task success before and after correction, detector precision/recall, false-positive rate, and correction success among flagged cases.
- Produces canonical SHA-256 digests of the input cases and the run report.
- Can append reports to a JSONL ledger rather than overwrite existing records.

## What it does not do
- It does not itself run a language model or detect faults.
- The bundled cases are synthetic fixtures for testing the metric implementation, not evidence of real-world agent performance.
- Hashes establish integrity of the serialized record, not truthfulness of the record or an external timestamp.

## Run locally

From the repository root:

```bash
python -m pytest -q tests/test_cis_verification_harness.py
python benchmarks/cis_verification_harness.py benchmarks/data/cis_synthetic_cases.jsonl
python benchmarks/cis_verification_harness.py benchmarks/data/cis_synthetic_cases.jsonl --ledger artifacts/cis_runs.jsonl
```

The final command appends one result line to the ledger. Do not delete or replace earlier ledger entries. Store raw inputs and execution context alongside the report for meaningful provenance.

## Synthetic fixture expected results
- Cases: 4
- Task success before: 0.50
- Task success after: 0.75
- Detection precision: 0.50
- Detection recall: 0.50
- False-positive rate: 0.50
- Successful repairs of actual errors: 1

These values validate metric plumbing only. They are not estimates of the CIS's real-world performance.

## Next benchmark phase
Replace or augment synthetic cases with versioned, representative tasks and ground truth. Record model/version, prompt or policy hash, tool version, task category, fault injection method, expected state transition, observed state transition, latency, resource use, and reviewer adjudication. Pre-register scoring rules before running the evaluation. Report confidence intervals and stratify by failure type.
