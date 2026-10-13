> **Federation index:** [FEDERATION_INDEX.md](https://github.com/Zygros/conzet-sovereign-intelligence/blob/main/FEDERATION_INDEX.md)

# OmniNet v3.0.0-UNITY (CZAOUA Unified)

[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-Sovereign_Open-purple)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Research%20Prototype-blue)](https://github.com/Zygros/omninet-v4)

**The Conzetian Sovereign Internet** — κ-Coherence Routing for Distributed Agent Systems.

> **Evidence boundary:** this repository is a research/engineering prototype. The presence of implementations, tests, benchmarks, or architectural specifications does not by itself establish production readiness, security certification, or independent verification.

## Evidence policy

- **Implemented** — code exists in the repository.
- **Tested** — a documented test run has passed for the cited revision.
- **Benchmarked** — benchmark inputs, methodology, parameters, and output artifacts are available.
- **Verified** — an independent reproduction or review is linked.
- **Designed** — architecture/specification exists without sufficient implementation evidence.
- **Historical** — retained for provenance and not a statement of current capability.

Quantitative claims remain **unverified** until the exact commit, environment, command, fixtures/dataset, parameters, and output artifact are supplied.

## Security boundary

The repository's current security API includes an XOR stream-cipher implementation. Treat that construction as **experimental/demo cryptography**, not production-grade authenticated encryption. Production deployments should use established authenticated-encryption primitives and appropriate security review.

## Overview

OmniNet v4 is a research implementation exploring:

- **κ-Coherence Routing**: alignment-based routing experiments
- **Phoenix Protocol**: self-healing/recovery experiments
- **Transfinite Addressing**: experimental mathematical addressing model
- **Sanov-Conzet Compression**: experimental coordination/compression model

The repository may contain a mixture of executable implementation, benchmarks, and architectural research. Current capability must be established from reproducible evidence rather than README claims alone.

## Ω-9 Research Layer

A new falsifiable research layer is provided in `omninet/research.py`, with deterministic tests in `tests/test_research.py` and the full experimental protocol in `docs/RESEARCH_PROTOCOL_OMEGA9.md`.

It introduces:

- a bounded multiplicative coherence metric;
- resilience scoring under controlled failures;
- descriptive candidate-vs-baseline effect sizes;
- transparent confidence bounds;
- logical-population capacity separated from physical node count;
- a recovery-decay null model.

These are **proposed research instruments**, not established scientific laws. The Ω-9 protocol requires baseline comparisons, fault injection, statistical analysis, raw artifacts, and reproducibility before strong empirical claims are made.

## Installation

```bash
git clone https://github.com/Zygros/omninet-v4.git
cd omninet-v4
pip install -e .
python -c "from omninet import __version__; print(f'OmniNet v{__version__}')"
```

## Quick Start

```python
from omninet.math import kappa_coherence, sanov_conzet_limit

k = kappa_coherence(sigma=0.1, L=0.2)
print(f"κ = {k:.4f}")

result = sanov_conzet_limit()
print(f"Compression: {result.compression_ratio:.2e}:1")
print(f"Coherent: {result.is_coherent}")
```

### Run the daemon

```bash
python -m omninet.daemon --genesis
```

### Run tests

```bash
python -m pytest tests/ -v
```

> The repository contains a historical README assertion of 196 passing tests. That number is **not treated as current verification** until a current run or CI artifact is linked to the relevant commit.

## Architecture

| Module | Description |
|---|---|
| `math` | κ-Coherence mathematics and Conzetian constants |
| `research` | Falsifiable coherence, resilience, scaling, and benchmark metrics |
| `daemon` | Network daemon and recovery experiments |
| `security` | Experimental encryption and secure-storage utilities |
| `knowledge_graph` | Blockchain-inspired memory ledger |
| `echoflux` | Fractal reasoning experiments |
| `sovereign_engine` | AI capability orchestration |
| `spider_driver` | Robotics/hardware abstraction |
| `jolt` | Integrated agent experiment |

## Mathematical foundations

The repository contains experimental mathematical models including the κ-Coherence field equation and Conzetian constant. These are documented as **research definitions**, not independently established scientific results, unless a corresponding reproducible validation artifact is provided.

The Ω-9 research layer adds measurable definitions designed to support falsification and comparison rather than merely restating architectural claims.

## Testing and development

```bash
python -m pytest tests/ -v
python -m pytest tests/ -v --cov=omninet --cov-report=term-missing
black omninet/ tests/
isort omninet/ tests/
mypy omninet/
```

For benchmark or release claims, record the exact commit, environment, command, fixture/data version, parameters, and output artifact.

## Repository structure

```text
omninet-v4/
├── omninet/                 # Core package
├── tests/                   # Test suite
├── docs/                    # Documentation and evidence standards
├── pyproject.toml           # Package configuration
├── setup.py                 # Setup script
├── requirements.txt         # Dependencies
└── LICENSE                  # Repository license
```

## Provenance and release policy

See `SPLUS.md`, `SECURITY.md`, `LICENSE-STATUS.md`, `docs/PROVENANCE.md`, and `docs/EVIDENCE_AND_SECURITY.md` for the repository's evidence and validation boundaries.

A release must not be labeled **Production Ready** unless current evidence demonstrates the required tests, dependency/security review, deployment validation, and the specific production capability being claimed.

## License

See `LICENSE` for applicable terms.

## Author

**Justin Neal Thomas Conzet**

## Citation

```bibtex
@software{omninet_v4_2026,
  title={OmniNet v4: The Conzetian Sovereign Internet},
  author={Conzet, Justin Neal Thomas},
  year={2026},
  url={https://github.com/Zygros/omninet-v4}
}
```
