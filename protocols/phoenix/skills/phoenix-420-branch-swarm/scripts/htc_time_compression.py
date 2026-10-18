#!/usr/bin/env python3
"""Phoenix HTC-365 benchmark kernel.

Measures computational time compression, not physical time dilation.
The benchmark freezes a baseline workload, executes an HTC workload,
and reports verified work per wall-clock second.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
import hashlib
import json
import time


@dataclass(frozen=True)
class RunResult:
    label: str
    work_units: int
    wall_seconds: float
    verified_units: int
    digest: str

    @property
    def verified_throughput(self) -> float:
        return self.verified_units / self.wall_seconds if self.wall_seconds else 0.0


def deterministic_work(units: int) -> str:
    state = b"PHOENIX-HTC-365"
    for i in range(units):
        state = hashlib.sha256(state + i.to_bytes(8, "big")).digest()
    return state.hex()


def run(label: str, units: int) -> RunResult:
    start = time.perf_counter()
    digest = deterministic_work(units)
    elapsed = time.perf_counter() - start
    return RunResult(label, units, elapsed, units, digest)


def compare(baseline: RunResult, htc: RunResult) -> dict:
    speedup = htc.verified_throughput / baseline.verified_throughput
    return {
        "baseline": asdict(baseline),
        "htc": asdict(htc),
        "measured_speedup": speedup,
        "target_speedup": 365.0,
        "target_met": speedup >= 365.0,
        "verification": baseline.digest == htc.digest if baseline.work_units == htc.work_units else False,
        "interpretation": "computational throughput ratio; not physical time dilation",
    }


def main() -> None:
    # Small reproducible smoke benchmark. Scale units for a real HTC-365 run.
    baseline = run("baseline", 10000)
    htc = run("htc", 10000)
    report = compare(baseline, htc)
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
