# Evolution Gatekeeper

Status: IMPLEMENTED

## Contract
Require evidence, compatibility status, and a next hypothesis before an architectural patch is promoted.

## Gate inputs
`patch`, `evidence_refs`, `verification_state`, `compatibility`, `regression_status`, `next_hypothesis`.

## Promotion rule
A patch may advance only when the evidence boundary is explicit, compatibility is declared, regressions are accounted for, and a next hypothesis exists.

## Completion condition
Architectural evolution becomes an evidence-gated transition rather than an assertion of improvement.
