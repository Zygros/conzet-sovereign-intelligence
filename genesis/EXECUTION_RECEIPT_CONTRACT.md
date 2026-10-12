# Execution Receipt Contract

The contract separates an action's lifecycle label from evidence that can be inspected.

- `PLANNED`: no execution claimed.
- `REQUESTED`: submitted or queued; no execution claimed.
- `EXECUTED`: the caller reports that the action ran; verification may still be pending.
- `FAILED`: the action or its acceptance criteria failed.
- `VERIFIED`: execution is reported, a verification method passed, and at least one evidence reference is attached.

`genesis.execution_receipts.validate_receipt` checks schema and status invariants. It does **not** authenticate evidence references, establish the truth of a claim, or independently verify external systems. A trusted adapter and verifier must do that. Never construct a `VERIFIED` receipt from a generated hash or timestamp alone.

Run tests from the repository root:

```sh
python -m unittest discover -s tests -v
```
