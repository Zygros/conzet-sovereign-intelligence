# Sovereign Federation SDK Surface (v0.1)

**Status:** Local stubs + omega-10 Python package. Not a published PyPI/npm SDK.

## Python (local)

```text
from omega.core.ledger import AppendOnlyLedger, LedgerVerifier
from omega.phoenix.benchmark import PhoenixBenchmark
from omega.htc.chamber import HTCBounded
from omega.redteam.fixtures import run_all_fixtures
from omega.memory.codex import Codex, bootstrap_omega_entries
```

## Federation scripts

- `python scripts/htc_federation.py --cycles N --seed S`
- `python scripts/stress_federation.py --intensity high`

## Boundaries

- No automatic connection to external AI provider APIs.
- No HPC drivers.
- Credentials never embedded.
