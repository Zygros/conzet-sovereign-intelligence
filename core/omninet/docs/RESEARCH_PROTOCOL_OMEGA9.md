# Ω-9 Research Protocol

## Purpose

This document upgrades OmniNet from a collection of architectural claims into a falsifiable research program. It does **not** declare the proposed metrics, equations, or routing policy scientifically validated. Each item becomes a hypothesis with a reproducible test.

## Hypothesis H1 — Multiplicative Coherence

For routing observations normalized to `[0,1]`, the proposed geometric coherence score in `omninet.research.coherence_score()` should penalize simultaneous degradation more strongly than an arithmetic mean while remaining bounded in `[0,1]`.

### Test
Generate controlled observations with one, two, and three degraded dimensions. Compare geometric score against arithmetic and weighted-arithmetic baselines.

### Success criterion
The proposed metric must preserve rank ordering under all monotonic single-variable perturbations and demonstrate lower score sensitivity to compensation by one unusually strong metric.

## Hypothesis H2 — Resilience Under Fault Injection

A routing policy that explicitly optimizes reliability, recovery, latency, throughput, and loss should maintain higher post-failure service than a policy optimized only for latency on selected fault workloads.

### Experimental matrix

- topology: ring, grid, random geometric, scale-free
- size: 32, 128, 512, 2048 logical nodes
- faults: 1%, 5%, 10%, 25% node/link loss
- traffic: uniform, hotspot, bursty
- policies: shortest-path baseline, latency heuristic, OmniNet candidate
- repetitions: fixed random seeds plus independent seed set

### Metrics

- delivery ratio
- p50/p95 latency
- throughput
- recovery time
- coherence score
- CPU and memory overhead

## Hypothesis H3 — Logical Population Compression

A kernel can represent a large *logical* population without requiring an equivalent number of physical processes. This is a representation/scaling hypothesis, not evidence that the represented agents are actually executing.

The function `logical_population_capacity()` formalizes:

`N_logical = K × F^D`

where `K` is kernel count, `F` fanout, and `D` hierarchy depth.

### Required evidence

Report physical process count, memory consumption, runtime, and logical population separately. Never label logical capacity as deployed node count.

## Hypothesis H4 — Recursive Recovery Degradation

Repeated faults may reduce recovery quality. `recovery_decay()` supplies a transparent null-model curve against which an actual Phoenix/self-healing implementation can be compared.

### Required comparison

Observed recovery quality must be plotted against the null model. A claimed improvement requires a predefined effect size and confidence interval.

## Novelty Standard

OmniNet must not claim novelty merely because terminology is new. Distributed consensus routing and self-healing routing are established research areas, including consistency-first routing and compact self-healing algorithms. The contribution must therefore be stated as a precise mechanism plus a measurable advantage over relevant baselines.

## Evidence Ladder

1. **Defined** — equation/interface exists.
2. **Implemented** — executable implementation exists.
3. **Tested** — deterministic tests pass.
4. **Benchmarked** — controlled comparison exists.
5. **Statistically evaluated** — uncertainty/effect size reported.
6. **Reproduced** — independent environment reproduces result.
7. **Peer reviewed** — external technical scrutiny completed.

Only levels 4–7 support strong empirical claims.

## Ω-9 Acceptance Gate

A subsystem reaches the project's internal 9/10 research target only when it has:

- precise specification;
- reproducible implementation;
- adversarial tests;
- baseline comparison;
- measured resource costs;
- statistical analysis;
- raw result artifacts;
- clear failure cases;
- prior-art comparison;
- reproducible instructions.

This protocol intentionally makes the score harder to earn. The objective is evidence, not inflation.
