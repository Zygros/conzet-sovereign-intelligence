# Execution Receipt Emitter

Status: IMPLEMENTED

## Contract
Transform a real tool/workflow operation into a structured execution receipt without upgrading its verification state.

## Receipt fields
`intent`, `operation`, `actor_tool`, `inputs`, `outputs`, `timestamp`, `status`, `evidence_refs`, `commit_or_file_ids`, `content_hash`, `verification_state`, `failure_blocker`, `next_hypothesis`.

## Invariant
An emitted receipt records execution; it does not itself prove correctness.

## Completion condition
Every meaningful Cycle 02 operation can be represented by this schema.
