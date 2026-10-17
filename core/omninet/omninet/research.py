"""
OmniNet Research Layer

Reproducible, falsifiable metrics for κ-coherence and resilient routing.

This module deliberately treats the Conzetian quantities as hypotheses and
engineering metrics rather than established scientific laws.  The goal is to
make the architecture experimentally testable against conventional baselines.
"""

from dataclasses import dataclass
from math import exp, isfinite
from typing import Iterable, Sequence


@dataclass(frozen=True)
class RoutingObservation:
    """One normalized routing observation.

    All inputs are normalized to [0, 1], where larger values are better except
    latency and loss.  This makes the metric independent of raw units.
    """

    reliability: float
    throughput: float
    latency: float
    loss: float
    recovery: float


@dataclass(frozen=True)
class ResearchResult:
    """Deterministic output suitable for a benchmark artifact."""

    score: float
    baseline_score: float
    relative_gain: float
    observations: int


def _unit_interval(value: float) -> float:
    if not isfinite(value):
        raise ValueError("metric must be finite")
    return max(0.0, min(1.0, float(value)))


def coherence_score(observation: RoutingObservation) -> float:
    """Compute a bounded routing-coherence score.

    Proposed research metric:

        C = R^0.30 * T^0.20 * (1-L)^0.20 * (1-P)^0.15 * H^0.15

    where R is reliability, T throughput, L normalized latency, P packet
    loss, and H recovery quality.  The geometric form penalizes weak links
    without allowing one excellent metric to hide catastrophic failure in
    another.  The exponents sum to one, making the score dimensionless.

    This is a *proposed metric*, not a claim about a natural constant.
    """
    r = _unit_interval(observation.reliability)
    t = _unit_interval(observation.throughput)
    l = _unit_interval(observation.latency)
    p = _unit_interval(observation.loss)
    h = _unit_interval(observation.recovery)
    return (
        r ** 0.30
        * t ** 0.20
        * (1.0 - l) ** 0.20
        * (1.0 - p) ** 0.15
        * h ** 0.15
    )


def mean_coherence(observations: Iterable[RoutingObservation]) -> float:
    values = [coherence_score(item) for item in observations]
    if not values:
        raise ValueError("at least one observation is required")
    return sum(values) / len(values)


def resilience_index(
    baseline_delivery: float,
    failed_delivery: float,
    recovery_delivery: float,
) -> float:
    """Measure retained service after failure and subsequent recovery.

    The index is the geometric mean of failure retention and recovery
    retention.  It is bounded to [0, 1] and is useful for fault-injection
    experiments where absolute network size changes between trials.
    """
    b = _unit_interval(baseline_delivery)
    f = _unit_interval(failed_delivery)
    r = _unit_interval(recovery_delivery)
    if b == 0.0:
        return 0.0
    failure_retention = f / b
    recovery_retention = r / b
    return max(0.0, min(1.0, (failure_retention * recovery_retention) ** 0.5))


def benchmark(
    candidate: Sequence[RoutingObservation],
    baseline: Sequence[RoutingObservation],
) -> ResearchResult:
    """Compare a candidate routing policy with a baseline.

    No statistical significance is inferred here; this function produces a
    reproducible descriptive effect size that a later statistical layer can
    analyze with confidence intervals and hypothesis tests.
    """
    if not candidate or not baseline:
        raise ValueError("candidate and baseline must both contain observations")
    candidate_score = mean_coherence(candidate)
    baseline_score = mean_coherence(baseline)
    gain = 0.0 if baseline_score == 0 else (candidate_score - baseline_score) / baseline_score
    return ResearchResult(candidate_score, baseline_score, gain, len(candidate))


def confidence_bound(samples: Sequence[float], z: float = 1.96) -> tuple[float, float]:
    """Return a normal-approximation 95% interval for a bounded metric.

    This is intentionally simple and transparent.  For publication-quality
    analysis, bootstrap or distribution-appropriate intervals should be used.
    """
    if not samples:
        raise ValueError("samples cannot be empty")
    n = len(samples)
    mean = sum(samples) / n
    if n == 1:
        return mean, mean
    variance = sum((x - mean) ** 2 for x in samples) / (n - 1)
    margin = z * (variance / n) ** 0.5
    return max(0.0, mean - margin), min(1.0, mean + margin)


def logical_population_capacity(kernel_nodes: int, fanout: int, depth: int) -> int:
    """Calculate logical addressable population without allocating nodes.

    Capacity = kernel_nodes * fanout ** depth.

    This separates *logical population* from physical process count and avoids
    the misleading implication that a large integer means those processes
    are actually running.
    """
    if kernel_nodes < 1 or fanout < 1 or depth < 0:
        raise ValueError("kernel_nodes and fanout must be positive; depth non-negative")
    return kernel_nodes * (fanout ** depth)


def recovery_decay(cycles: int, base: float = 1.0, rate: float = 0.1) -> float:
    """Model expected recovery quality decay over repeated fault cycles."""
    if cycles < 0 or base < 0 or rate < 0:
        raise ValueError("cycles, base, and rate must be non-negative")
    return _unit_interval(base * exp(-rate * cycles))
