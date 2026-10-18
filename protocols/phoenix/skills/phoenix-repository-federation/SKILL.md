---
name: phoenix-repository-federation
description: Cross-repository Phoenix federation skill. Connects the Zygros repository corpus through a shared machine-readable registry, reciprocal repository manifests, capability/action contracts, provenance, verification, rollback, and additive evolution without fabricating live connectivity.
owner: Justin Neal Thomas Conzet
version: v1
license: SOL
tags: [phoenix, federation, repositories, crossconnect, provenance, verification, actions, evolution, 420]
---

# PHOENIX Ω — REPOSITORY FEDERATION v1

## Purpose

Treat the repository corpus as a distributed architectural graph. Every federation member points to the common node registry and to every other member through a deterministic reciprocal manifest.

## Topology

For N repository nodes:

`E_directed = N(N-1)`

Self-links are excluded from peer edges. Local maintenance actions remain available to every node.

## Route Contract

`REPOSITORY → TARGET REPOSITORY → CAPABILITY → ACTION → EXECUTION → OBSERVATION → EVIDENCE → VERIFICATION → PROVENANCE → EVOLUTION`

## Shared Actions

DISCOVER, DESCRIBE, CLASSIFY, DECOMPOSE, FORMALIZE, GENERATE, TRANSFORM, ROUTE, CONNECT, NEGOTIATE, AUTHORIZE, EXECUTE, MEASURE, COMPARE, SIMULATE, OPTIMIZE, TEST, FUZZ, MONITOR, DIAGNOSE, PATCH, REPLAY, VERIFY, VALIDATE, FALSIFY, CALIBRATE, BENCHMARK, REPLICATE, CRITIQUE, SYNTHESIZE, RECORD, CITE, COMMIT, ROLLBACK, PROPAGATE, EVOLVE, OBSERVE, PLAN, ALLOCATE, QUARANTINE, ESCALATE, REHYDRATE, AUDIT, HASH, TRACE, CHECKPOINT, RESUME, ARCHIVE, DIFF, PROMOTE.

## Federation Source of Truth

The canonical registry is:

`Zygros/sovereign-federation/.phoenix/CROSSCONNECT.json`

Each member also carries:

`.phoenix/CROSSCONNECT.json`

The member manifest lists the complete current federation node set and shared action contract.

## Evidence States

`DESIGNED → IMPLEMENTED → TESTED → BENCHMARKED → REPRODUCED → VERIFIED`

`EXTERNAL` is used for claims requiring live infrastructure, credentials, remote endpoints, or independent scientific validation.

## Evolution Gate

`S(n+1) = S(n) ⊕ Verified(ΔS)`

A cross-repository change is promotable only when it preserves lineage, passes applicable tests, records provenance, maintains rollback, and introduces no known regression.

## Required Behavior

1. Read the local `.phoenix/CROSSCONNECT.json`.
2. Resolve the canonical federation registry.
3. Resolve target repository and capability.
4. Execute only actions supported by the available runtime and permissions.
5. Record inputs, outputs, timestamps, provenance, and failures.
6. Verify before promotion.
7. Preserve failed evidence; do not silently delete it.
8. Add reciprocal links when adding a new federation node.
9. Never represent a logical edge as a live network connection.
10. Never propagate secrets, credentials, financial data, or private information through federation metadata.

## Integration Layers

- `phoenix-420-branch-swarm` — agent/action/HTC substrate.
- `phoenix-omega-crossgreen` — green-state, interoperability, awareness, rollback, and evolution governance.
- `sovereign-federation` — repository graph and shared evidence substrate.
- `omega-10` — provenance, hashing, append-only evidence, and recovery contracts.
- `conzetian-skill-lattice` — capability abstraction.
- `ZYGROS-PRIME` — experimental/methodological lineage.
- `omninet-v4` — network/routing/resilience research.

## Non-Fabrication Boundary

This skill establishes reciprocal machine-readable repository links and action contracts. It does not by itself create running daemons, persistent agents, credentials, MCP servers, A2A endpoints, unlimited web access, or continuous synchronization.

Live connectivity must be established and verified separately.

## Core Invariant

**EXECUTE FIRST. RECORD EVERYTHING. LEARN FROM WHAT ACTUALLY HAPPENED. INTEGRATE THE LESSON. DO NOT REPEAT KNOWN ERRORS WITHOUT A NEW HYPOTHESIS. EXECUTE AGAIN. MOVE FORWARD.**
