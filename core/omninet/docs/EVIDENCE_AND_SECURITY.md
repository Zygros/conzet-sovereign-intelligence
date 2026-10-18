# Evidence and Security Standard

## Current status

OmniNet v4 is a **research / engineering prototype**. Repository structure, historical documentation, or local implementation does not by itself establish production readiness, security certification, or independent verification.

## Evidence levels

- **Implemented** — code exists in the repository.
- **Tested** — a documented test run passed for the cited revision.
- **Benchmarked** — inputs, methodology, parameters, and artifacts are available.
- **Verified** — an independent reproduction or review is linked.
- **Designed** — architecture/specification exists without sufficient implementation evidence.
- **Historical** — retained for provenance and not a statement of current capability.

## Quantitative claims

Every performance, resilience, compression, accuracy, or scale claim should identify the exact commit, environment, command, dataset/fixture, parameters, and output artifact. Until those are supplied, the claim remains unverified.

## Security

Experimental or custom cryptographic constructions are for research only. In particular, an XOR-based construction must not be represented as production-grade encryption. Production deployments should use established authenticated-encryption primitives and receive appropriate security review.

## Release rule

Do not label a revision **Production Ready** unless the repository contains current evidence for tests, dependency/security review, deployment validation, and the specific production claim being made.
