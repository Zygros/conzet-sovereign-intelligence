# Verification State Machine

Status: IMPLEMENTED

## Contract
Prevent unsupported promotion between evidence states.

## Allowed progression
`IDEA → STAGED → IMPLEMENTED → EXECUTED → TESTED → BENCHMARKED → REPRODUCED → VERIFIED`

Terminal states: `BLOCKED`, `FAILED`.

Backward transitions require a new execution or explicit invalidation record.

## Completion condition
No record may become VERIFIED solely because an artifact exists.
