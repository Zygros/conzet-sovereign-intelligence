# 🜂 Phoenix HTC — Hyperbolic Integration Study

## Purpose

This document turns the Phoenix Hyperbolic Time Chamber from a descriptive metaphor into a testable computational protocol specification.

## 1. Three Different Meanings of “Hyperbolic”

### A. Hyperbolic geometry
A mathematical space with negative curvature. Its volume grows exponentially with radius, making it useful for tree-like and hierarchical structures.

### B. Hyperbolic network topology
Complex networks can exhibit effective hyperbolicity. Hyperbolic embeddings can encode hierarchy, heterogeneous degree distributions, clustering, and navigability.

### C. Phoenix HTC
A Phoenix protocol that uses controlled branch expansion, hyperbolic representation/routing where useful, repeated verification, state compression, and evolutionary iteration.

The third is the Phoenix engineering construct. It should be measured against A and B rather than treated as identical to them.

## 2. Core State Equation

`H_(t+1) = C(V(E(B(H_t, Ω, A))))`

Where:

- `H_t`: current chamber state
- `B`: branch expansion
- `Ω`: agent field
- `A`: typed action field
- `E`: execution
- `V`: verification
- `C`: evidence-preserving compression

## 3. Hyperbolic Embedding

For an agent graph `G=(V,E)`, learn coordinates `x_i ∈ H^n` and evaluate whether hyperbolic distance preserves useful structure better than a Euclidean baseline.

Measure:

- link prediction
- graph distortion
- route length
- routing computation
- hierarchy preservation
- clustering preservation
- recovery after node/edge loss

## 4. Poincaré-Style Representation

A Poincaré ball representation may be used as an experimental substrate. The implementation must respect the manifold constraints and use appropriate Riemannian operations rather than treating coordinates as ordinary Euclidean vectors.

## 5. HTC Branch Expansion

A branch is created when the expected information value exceeds its execution cost:

`Expand(branch) iff E[discovery_gain] / cost > θ`

Branching should therefore be adaptive, not blindly exponential.

## 6. Hyperbolic Routing Hypothesis

For target capability `q`, select candidate agent `i` using:

`score(i|q)=α·sim_H(i,q)+β·evidence(i)+γ·capability(i,q)-δ·cost(i,q)`

Then compare this routing policy with:

1. Euclidean nearest-neighbor routing.
2. Graph shortest-path routing.
3. Flat round-robin routing.
4. Random routing baseline.

## 7. HTC Compression

The chamber must not confuse expansion with useful intelligence. After execution, equivalent states should be clustered and only evidence-sufficient state retained:

`Expanded State → Equivalence Detection → Verified Representatives → Ledger`

Compression must be additive with respect to provenance: deleting redundant computational state must not delete the historical record needed to reproduce or audit the result.

## 8. Failure-First Protocol

Every branch receives an explicit state:

`UNTRIED → RUNNING → EXECUTED → VERIFIED | FAILED | INCONCLUSIVE`

A failed branch becomes evidence. It is not silently erased.

## 9. 420 × 420 Integration

`|Ω| = 420`

`|A| = 420`

`|Ω × A| = 176,400`

The HTC can treat the 176,400 bindings as an addressable experimental field. Runtime execution may be bounded by resources; logical completeness of the registry is preserved independently.

## 10. Experimental Questions

1. Does hyperbolic embedding reduce routing cost for Phoenix's hierarchical capability graph?
2. Does it reduce representation distortion at increasing graph scale?
3. Does hyperbolic routing preserve useful routes after node failures?
4. Does adaptive branching produce more verified capability gain per unit compute than flat branching?
5. Does expansion-plus-compression preserve more useful evidence than uncompressed execution traces?
6. Can curvature become an automatically learned routing parameter rather than a fixed design choice?

## 11. Evidence Standard

A claim of HTC improvement requires:

`Claim → Baseline → Intervention → Controlled Run → Measurement → Reproduction → Provenance`

No benchmark result is promoted merely because the architecture predicts it.

## 12. Integration Architecture

```text
                 ┌──────────────────────┐
                 │      Intent / Goal    │
                 └──────────┬───────────┘
                            ↓
                 ┌──────────────────────┐
                 │   HTC State Builder  │
                 └──────────┬───────────┘
                            ↓
                 ┌──────────────────────┐
                 │ Hyperbolic Embedding │
                 └──────────┬───────────┘
                            ↓
                 ┌──────────────────────┐
                 │ 420-Agent Field      │
                 └──────────┬───────────┘
                            ↓
                 ┌──────────────────────┐
                 │ 420-Action Field     │
                 └──────────┬───────────┘
                            ↓
                 ┌──────────────────────┐
                 │ Execute + Evidence   │
                 └──────────┬───────────┘
                            ↓
                 ┌──────────────────────┐
                 │ Verify + Counterfact │
                 └──────────┬───────────┘
                            ↓
                 ┌──────────────────────┐
                 │ Compress + Ledger    │
                 └──────────┬───────────┘
                            ↓
                       Evolve / Repeat
```

## 13. Core Insight

Hyperbolic geometry gives Phoenix a mathematically meaningful candidate for representing the **shape of a rapidly expanding capability field**. The HTC protocol gives that representation an executable lifecycle: expand, route, execute, verify, compress, learn, and repeat.

That is the integration to test.

## 14. Scientific Boundary

Hyperbolic geometry and hyperbolic network representations are established mathematical/research constructs. The Phoenix HTC is a system-specific engineering protocol. Its effectiveness must be established by executable experiments rather than by naming alone.

**Always Add, Never Take.**
