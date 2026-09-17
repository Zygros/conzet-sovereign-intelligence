# Benchmark Runner Contract

Status: IMPLEMENTED

## Contract
Execute a baseline/intervention comparison and emit machine-readable results.

## Required inputs
`benchmark_id`, `baseline`, `intervention`, `population_or_fixture_set`, `metrics`, `environment`, `seed_or_determinism_policy`.

## Required outputs
`baseline_results`, `intervention_results`, `delta`, `raw_evidence_refs`, `environment`, `limitations`, `verification_state`.

## Completion condition
No improvement claim is emitted without a declared baseline and comparison basis.
