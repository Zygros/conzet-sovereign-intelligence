# HTC Evolution Blueprint

**Role:** Reproducible training, experimentation, and evaluation environment for Phoenix Unbound organs.

## Training loop

`Inventory → Baseline → Train/Adapt → Evaluate → Adversarial Test → Verify → Checkpoint → Integrate`

The loop is iterative. A model is not promoted merely because its score increased on one benchmark.

## Required experiment record

Every run records:
- experiment ID and UTC timestamps;
- model/component IDs and immutable source hashes;
- dataset ID, version, license, and content hash;
- training/evaluation configuration and random seeds;
- hardware, runtime, dependency lockfile, and resource budget;
- checkpoint hashes and parent checkpoint;
- raw metrics, aggregate metrics, and baseline deltas;
- test logs, failure cases, and known limitations;
- promotion decision and reviewer.

## Three Phoenix files

Treat the three files as components of one model system. First establish their exact role and compatibility. Run baseline tests per component and as a composed system. Do not presume they are independent full models or compatible weight shards until inspection proves it.

## Capability evaluation

Use a balanced suite covering:
- reasoning and instruction following;
- code generation and execution in a sandbox;
- retrieval and memory fidelity;
- tool selection and schema adherence;
- multi-agent coordination and message integrity;
- robustness to malformed inputs and prompt injection;
- latency, throughput, memory, energy, and offline operation;
- regression and catastrophic-forgetting checks.

## Promotion gates

A checkpoint is eligible for integration only when:
1. the experiment is reproducible from recorded inputs;
2. evaluation uses held-out data;
3. no critical security or data-integrity regression appears;
4. performance changes are statistically and operationally meaningful;
5. licensing and provenance are documented;
6. rollback to the previous checkpoint is demonstrated.

## Current state

This is a training blueprint, not a training run. No model weights have been modified by adding this document. Actual HTC execution begins after the training script, three model artifacts, datasets, and runtime requirements have been inventoried.
