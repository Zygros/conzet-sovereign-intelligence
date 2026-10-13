# Sovereign API Layer v0.1

**Status:** SPEC ONLY. Not implemented. This is the contract.

## Endpoint

`POST /api/v1/genesis/execute`

## Request

```json
{
  "task": "string — the input to process",
  "depth": "int — bounded recursion depth, default 5, max 840"
}
```

## Response

```json
{
  "final_state_hash": "sha256 hex",
  "trace": [{"depth": 0, "hash": "...", "scaling": 1.309017}],
  "duration_seconds": 0.000045,
  "verdict": "DEMONSTRATION_ZERO_COMPLETE"
}
```

## Law

Always add. Never take. The API adds a processing round; it never removes or mutates prior state.

## Acceptance

- Deterministic: same input + depth = same hash.
- Bounded: depth cannot exceed 840.
- Transparent: full trace returned.
- Fast: sub-millisecond for depth <= 5 on reference hardware.

## Next Step

Implement as a single-file Flask/FastAPI server wrapping demos/demonstration_zero.py.
