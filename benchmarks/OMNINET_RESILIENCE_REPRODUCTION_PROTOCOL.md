# OmniNet v4 Resilience and Privacy Reproduction Protocol
**Date:** 2026-10-12  
**Status:** Experiment design; no new simulation result is claimed by this document.  
**Purpose:** Turn the whitepaper's headline network claims into a reproducible, falsifiable benchmark.

## 1. Claims to reproduce separately
Do not combine all outcomes into a single “survival” score. The whitepaper reports:
- 10,000-node simulation;
- 847 attack vectors;
- 99.7% survival;
- 90.3% connectivity under 30% random node failure;
- 3.2-second recovery;
- 95% Sybil resistance.

These are source-reported claims until the exact implementation, configuration, logs, and seeds are recovered and reproduced.

## 2. Required artifact bundle
Each run must archive:
1. source commit and dependency lockfile;
2. topology generator and exact parameters;
3. node and edge counts before and after each fault;
4. random seeds and trial count;
5. attack catalogue with attack preconditions and success criteria;
6. baseline implementations and identical resource limits;
7. per-trial raw results, not only aggregate percentages;
8. machine/runtime details and timing method;
9. metrics definitions and aggregation script;
10. SHA-256 hashes of every input, raw output, and report.

## 3. Operational definitions
- **Survival:** Define the unit of survival (node, service, message delivery, or end-to-end task) and the observation window.
- **Connectivity:** Report at least (a) fraction of surviving nodes in the largest connected component, (b) reachable ordered-pair fraction, and (c) successful end-to-end delivery rate. Do not use the word “connectivity” without identifying which measure is intended.
- **Recovery time:** Define start/end events and whether recovery means routing restoration, service restoration, or task completion. Report median, p95, and worst-case.
- **Sybil resistance:** Define attacker identity budget, trust/key assumptions, infiltration success, false rejection of honest nodes, and the number of trials.
- **Attack vectors:** Give each vector a stable ID, implementation, expected effect, detection criterion, and pass/fail oracle.

## 4. Experimental matrix
For each baseline and each attack family, run:
- no-failure control;
- 10%, 20%, 30%, and 40% random node failures;
- targeted high-degree-node removal;
- bridge/cut-node removal;
- Sybil infiltration at multiple attacker budgets;
- route poisoning / dishonest relay;
- message replay and stale-state injection;
- partition and reconnect;
- high-latency, packet-loss, and node-churn conditions;
- key compromise and malicious insider cases where applicable.

Use fixed seeds for regression tests and a separate predeclared seed set for held-out evaluation. Repeat stochastic experiments enough times to report uncertainty intervals.

## 5. Baselines and fairness
Compare against at least:
- a simple shortest-path or standard routing baseline appropriate to the implemented network;
- a relevant established mesh/overlay protocol;
- an ablation of OmniNet with κ-coherence routing disabled;
- an ablation with any trust/reputation mechanism disabled.

Keep topology, traffic demand, adversary budget, hardware, and time budget matched. Report overhead as well as resilience: throughput, median/p95 latency, bytes per delivered message, CPU/memory, and control-plane traffic.

## 6. Reporting template
For every metric, publish:
- metric definition and unit;
- numerator/denominator;
- sample size and missing runs;
- mean/median and uncertainty interval as appropriate;
- baseline and relative change;
- failures and unexpected behavior;
- raw artifact links and hashes;
- independent reproduction status.

A paper figure should be generated from archived raw data by a checked-in script.

## 7. Stop conditions
Do not claim successful reproduction if:
- source/configuration is unavailable;
- seeds or raw outputs cannot be recovered;
- the metric definition differs materially from the publication;
- the baseline is not resource-matched;
- failed trials were silently excluded;
- only a synthetic demonstration was run.

## 8. Next actions
1. Locate the original simulator or authoring notebook.
2. If it cannot be recovered, label the original metrics “not reproducible from currently available artifacts” and build a new, separately labelled implementation.
3. Run controls first, then randomized failure, then adversarial cases.
4. publish the new implementation and raw data as an additive companion artifact, never as if it were the original experiment.
