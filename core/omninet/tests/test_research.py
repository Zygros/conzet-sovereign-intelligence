import unittest

from omninet.research import (
    RoutingObservation,
    benchmark,
    coherence_score,
    confidence_bound,
    logical_population_capacity,
    resilience_index,
    recovery_decay,
)


class ResearchMetricsTests(unittest.TestCase):
    def test_coherence_is_bounded(self):
        observation = RoutingObservation(1, 1, 0, 0, 1)
        self.assertAlmostEqual(coherence_score(observation), 1.0)

    def test_coherence_penalizes_loss_and_latency(self):
        clean = RoutingObservation(1, 1, 0, 0, 1)
        degraded = RoutingObservation(1, 1, 0.8, 0.8, 1)
        self.assertGreater(coherence_score(clean), coherence_score(degraded))

    def test_resilience_index(self):
        self.assertAlmostEqual(resilience_index(1, 0.5, 1), 0.70710678, places=6)
        self.assertEqual(resilience_index(0, 0, 0), 0.0)

    def test_benchmark_reports_relative_gain(self):
        baseline = [RoutingObservation(0.8, 0.8, 0.3, 0.2, 0.7)] * 10
        candidate = [RoutingObservation(0.9, 0.9, 0.2, 0.1, 0.9)] * 10
        result = benchmark(candidate, baseline)
        self.assertGreater(result.relative_gain, 0)
        self.assertEqual(result.observations, 10)

    def test_confidence_bound_is_bounded(self):
        low, high = confidence_bound([0.2, 0.4, 0.6, 0.8])
        self.assertGreaterEqual(low, 0)
        self.assertLessEqual(high, 1)
        self.assertLessEqual(low, high)

    def test_logical_population_does_not_allocate_nodes(self):
        self.assertEqual(logical_population_capacity(6, 10, 4), 60000)

    def test_recovery_decay_is_monotonic(self):
        values = [recovery_decay(i) for i in range(5)]
        self.assertEqual(values, sorted(values, reverse=True))


if __name__ == "__main__":
    unittest.main()
