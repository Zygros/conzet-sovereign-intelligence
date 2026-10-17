from pathlib import Path
from omega.phoenix.benchmark import PhoenixBenchmark

def test_phoenix_recovery(tmp_path: Path):
    bench = PhoenixBenchmark(tmp_path / "phoenix", seed=123, n_components=100, corrupt_fraction=0.90)
    result = bench.run()
    assert result.recovery_rate >= 0.90
    assert result.append_only_history_preserved is True
    assert result.passed is True
