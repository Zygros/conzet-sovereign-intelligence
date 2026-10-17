# Contract Validator Engine

Status: IMPLEMENTED

## Contract
Validate Ω-cycle records against required fields and allowed execution states.

## Required fields
`intent`, `operation`, `actor_tool`, `inputs`, `outputs`, `timestamp`, `status`, `evidence_refs`, `identifiers`, `verification_state`, `failure_blocker`, `next_hypothesis`.

## Allowed states
`IDEA`, `STAGED`, `IMPLEMENTED`, `EXECUTED`, `TESTED`, `BENCHMARKED`, `REPRODUCED`, `VERIFIED`, `BLOCKED`, `FAILED`.

## Completion condition
A validator must reject missing required fields and unknown execution states. Runtime verification remains TESTED only after an actual validator run.
