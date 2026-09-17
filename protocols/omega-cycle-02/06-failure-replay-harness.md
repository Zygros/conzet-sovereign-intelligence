# Failure Replay Harness

Status: IMPLEMENTED

## Contract
Replay a recorded failure under a materially changed hypothesis and preserve both the original and retry outcomes.

## Replay record
`original_receipt`, `hypothesis`, `changed_parameters`, `retry_receipt`, `comparison`, `next_hypothesis`.

## Invariant
A retry is valid only when the hypothesis or execution parameters materially differ from the failed attempt.

## Completion condition
Failures remain immutable evidence and are never overwritten by successful retries.
