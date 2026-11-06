> **Federation index:** [FEDERATION_INDEX.md](https://github.com/Zygros/conzet-sovereign-intelligence/blob/main/FEDERATION_INDEX.md)

# OMEGA-10 v0.1: Evidence Substrate

**Status banner:** OMEGA-10 v0.1: implementation and local test evidence; not independently reproduced.

Canonical serialization, SHA-256 hashing, append-only JSONL ledger with hash chaining, Ed25519 signing, run manifests, Master Codex, Phoenix deterministic recovery benchmark, red-team fault fixtures (≥20), and local-only Hyperbolic Time Chamber (HTC) bounded mode.

## Quick start

```bash
make bootstrap
make test
make phoenix
make redteam
make htc
make demo
```

## Evidence discipline

- Every ledger mutation that breaks the chain fails verification.
- Codex entries start at DESIGNED unless executable evidence is linked.
- HTC never enables network or deployment by default.
- No production or independent-reproduction claims without artifacts.

## Related (Federation)

- **Map of all repos:** https://github.com/Zygros/sovereign-federation
- Outsider audit & plain catalog: https://github.com/Zygros/sovereign-federation/tree/main/docs
- Phoenix meta-archive: https://github.com/Zygros/PHOENIX-PROTOCOL-ULTIMATE
- Multi-AI bridge: https://github.com/Zygros/multi-ai-convergence-protocol

## License

MIT
