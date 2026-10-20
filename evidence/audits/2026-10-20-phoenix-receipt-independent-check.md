# Independent Phoenix Receipt Integrity Check — 2026-10-20

## Scope

Downloaded GitHub Actions artifact `phoenix-proof-cycle-receipts` from [Phoenix proof-cycle run 38952339627](https://github.com/Zygros/PHOENIX-PROTOCOL-ULTIMATE/actions/runs/38952339627), extracted the three JSON receipts, and ran a separate local Python validation using Python's `hashlib` and canonical JSON serialization (`sort_keys=True`, separators `(',', ':')`). This check did not invoke the repository's receipt verifier, so it is a separate implementation of the hash checks.

## Artifact identity

- Artifact ID: `12067868939`
- Downloaded ZIP: 3,175 bytes
- Expected GitHub artifact digest: `1234416a4098729b5f9a58241dcd9bb15963eee5f77c99b69456c29f24b0f366`
- Independently computed ZIP SHA-256: `1234416a4098729b5f9a58241dcd9bb15963eee5f77c99b69456c29f24b0f366`
- Result: **MATCH**

## Receipt checks

For each receipt, the independent validator checked:
- recorded `ledger_valid` flag;
- SHA-256 of canonical `finding` object against `finding_sha256`;
- SHA-256 of the complete receipt object excluding `export_sha256`;
- contiguous event sequence numbers starting at 1;
- each event's `previous_hash` link, beginning with 64 zeroes;
- recomputed SHA-256 of every event excluding its `hash` field;
- final `cycle.finished` status agrees with the top-level status;
- final event's finding hash agrees with top-level `finding_sha256`.

| Receipt | Status | Events | Independent checks |
|---|---|---:|---|
| `phoenix-proof-cycle.json` | `PASS` | 4 | All 8 checks passed |
| `phoenix-proof-cycle-repaired.json` | `REPAIRED` | 6 | All 8 checks passed |
| `phoenix-proof-cycle-failed.json` | `FAIL` | 4 | All 8 checks passed |

### Receipt file SHA-256

- `phoenix-proof-cycle.json`: `5a50028e2b7153e599dbd7798008e8d05abf5d58c77fdc4fedaedfa6a99e7556`
- `phoenix-proof-cycle-repaired.json`: `f21f5c552aba8c45b11ac474a9b9737e4961b5dc39d140716b050b5d08192a28`
- `phoenix-proof-cycle-failed.json`: `998e7249917e9307b75a5a47c6ac3c5317873dad74ede789c996f29fa9943c3e`

## Result and boundary

**Integrity result: PASS for the downloaded artifact and all three receipt structures.** This independently reproduces the archive digest and the receipt/event hash relationships.

The fixture semantics remain bounded: the Scout source is explicitly `deterministic-local-fixture`; the evidence field says no external research was performed. This validates deterministic test fixtures and their tamper-evident structure, not the truth of external claims, external AI work, production readiness, mobile-device execution, or a live distributed swarm. It does not verify OpenTimestamps/Bitcoin anchoring.

## Reproduction

Python 3 with standard library only:

```python
import hashlib, json, zipfile
from pathlib import Path

def canonical_hash(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()

# For each extracted receipt dictionary d:
assert canonical_hash(d["finding"]) == d["finding_sha256"]
assert canonical_hash({k:v for k,v in d.items() if k != "export_sha256"}) == d["export_sha256"]
previous = "0" * 64
for sequence, event in enumerate(d["ledger"], 1):
    assert event["sequence"] == sequence
    assert event["previous_hash"] == previous
    assert canonical_hash({k:v for k,v in event.items() if k != "hash"}) == event["hash"]
    previous = event["hash"]
assert d["ledger"][-1]["payload"]["status"] == d["status"]
```

*Recorded 2026-10-20. Independent implementation refers to the separate validation code used for this checkpoint; a third-party reviewer has not yet reproduced this result.*
