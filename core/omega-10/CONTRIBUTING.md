# Contributing to OMEGA-10

**Always Add · Never Take · Zero Friction**

## Principles

1. Changes must be small, reviewable, and provenance-preserving.
2. Do not rewrite history or delete evidence artifacts silently.
3. Keep credentials, generated runtime state, and private data out of commits.
4. Every claim that moves from DESIGNED to IMPLEMENTED must link to executable evidence (tests, ledger entries, or run manifests).
5. Describe intent, affected paths, validation performed, and any unresolved uncertainty.

## Development

```bash
make bootstrap
make test
make phoenix
make redteam
make htc
```

## Status discipline

- Codex entries start at DESIGNED unless executable evidence is linked.
- Local evidence does not equal independent reproduction.
- No production claims without a successful health-check artifact.
