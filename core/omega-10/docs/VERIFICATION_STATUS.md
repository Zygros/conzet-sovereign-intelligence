# Verification Status

## Current evidence boundary

This repository contains implementation and local test infrastructure. A passing local run is not the same as independent reproduction, production certification, or security certification.

## Required evidence for claims

For every benchmark or capability claim, record:

1. exact commit SHA;
2. environment and dependency versions;
3. command used;
4. fixtures/datasets and parameters;
5. raw or machine-readable output artifact;
6. pass/fail result;
7. independent reproduction or review when claimed as verified.

## Release labels

- **Implemented** — code exists.
- **Tested** — current test execution is recorded.
- **Benchmarked** — reproducible benchmark artifacts exist.
- **Verified** — independent reproduction/review exists.
- **Prototype** — partial or experimental implementation.
- **Designed** — specification without sufficient implementation evidence.
- **Historical** — preserved material, not a current capability claim.

Do not upgrade a claim's status without adding the corresponding evidence artifact.
