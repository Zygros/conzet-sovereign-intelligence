#!/usr/bin/env python3
"""PHOENIX Hyperbolic Time Engine.

Executable computational layer for the Phoenix Hyperbolic Time Chamber.
Implements Poincare-ball operations, hyperbolic distance and angles, and
curvature sweeps for measurable routing/training experiments.

This is computational time-compression/training infrastructure, not a claim
of physical spacetime time dilation.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import acos, exp, log, sqrt
from typing import Iterable

Vector = tuple[float, ...]

@dataclass(frozen=True)
class HyperbolicConfig:
    curvature: float = -1.0
    epsilon: float = 1e-12

    @property
    def radius(self) -> float:
        if self.curvature >= 0:
            raise ValueError("curvature must be negative")
        return 1.0 / sqrt(-self.curvature)


def _dot(a: Vector, b: Vector) -> float:
    return sum(x * y for x, y in zip(a, b))


def _norm2(a: Vector) -> float:
    return _dot(a, a)


def _clamp_ball(x: Vector, cfg: HyperbolicConfig) -> Vector:
    r = sqrt(_norm2(x))
    limit = cfg.radius * (1.0 - cfg.epsilon)
    if r >= limit:
        scale = limit / r
        return tuple(v * scale for v in x)
    return x


def mobius_add(x: Vector, y: Vector, cfg: HyperbolicConfig = HyperbolicConfig()) -> Vector:
    """Möbius addition for the curvature-scaled Poincare ball."""
    x = _clamp_ball(tuple(x), cfg)
    y = _clamp_ball(tuple(y), cfg)
    c = -cfg.curvature
    xy = _dot(x, y)
    x2 = _norm2(x)
    y2 = _norm2(y)
    den = 1.0 + 2.0 * c * xy + (c * c) * x2 * y2
    sx = 1.0 + 2.0 * c * xy + c * y2
    sy = 1.0 - c * x2
    return _clamp_ball(tuple((sx * a + sy * b) / den for a, b in zip(x, y)), cfg)


def _atanh(x: float) -> float:
    return 0.5 * log((1.0 + x) / (1.0 - x))


def hyperbolic_distance(x: Vector, y: Vector, cfg: HyperbolicConfig = HyperbolicConfig()) -> float:
    """Geodesic distance in a constant-negative-curvature Poincare ball."""
    z = mobius_add(tuple(-v for v in x), tuple(y), cfg)
    rho = sqrt(_norm2(z)) / cfg.radius
    rho = min(max(rho, 0.0), 1.0 - cfg.epsilon)
    return 2.0 / sqrt(-cfg.curvature) * _atanh(rho)


def hyperbolic_angle_at(origin: Vector, a: Vector, b: Vector, cfg: HyperbolicConfig = HyperbolicConfig()) -> float:
    """Angle between geodesic directions at origin in the conformal model."""
    aa = mobius_add(tuple(-v for v in origin), tuple(a), cfg)
    bb = mobius_add(tuple(-v for v in origin), tuple(b), cfg)
    na = sqrt(_norm2(aa))
    nb = sqrt(_norm2(bb))
    if na < cfg.epsilon or nb < cfg.epsilon:
        return 0.0
    value = _dot(aa, bb) / (na * nb)
    return acos(max(-1.0, min(1.0, value)))


def radial_depth(x: Vector, cfg: HyperbolicConfig = HyperbolicConfig()) -> float:
    """Normalized radial depth in [0,1)."""
    return min(sqrt(_norm2(x)) / cfg.radius, 1.0 - cfg.epsilon)


def training_density(curvature: float, branch_factor: float, verification_rate: float) -> float:
    """Dimensionless experimental proxy for useful training density."""
    if curvature >= 0 or branch_factor < 1 or not 0 <= verification_rate <= 1:
        raise ValueError("invalid benchmark parameters")
    return exp(sqrt(-curvature)) * log(1.0 + branch_factor) * verification_rate


def curvature_sweep(curvatures: Iterable[float], branch_factor: float, verification_rate: float) -> list[tuple[float, float]]:
    """Evaluate the benchmark proxy over negative curvature values."""
    return [(k, training_density(k, branch_factor, verification_rate)) for k in curvatures]


def prove() -> dict[str, object]:
    """Deterministic self-check for the computational geometry layer."""
    cfg = HyperbolicConfig(-1.0)
    origin = (0.0, 0.0)
    x = (0.20, 0.10)
    y = (-0.10, 0.25)
    dxy = hyperbolic_distance(x, y, cfg)
    dyx = hyperbolic_distance(y, x, cfg)
    angle = hyperbolic_angle_at(origin, x, y, cfg)
    sweep = curvature_sweep((-0.25, -0.5, -1.0, -2.0), 8.0, 0.9)
    checks = {
        "distance_positive": dxy > 0,
        "distance_symmetric": abs(dxy - dyx) < 1e-10,
        "angle_bounded": 0.0 <= angle <= 3.141592653589793,
        "negative_curvature_sweep": all(k < 0 for k, _ in sweep),
        "finite_scores": all(score > 0 for _, score in sweep),
    }
    return {"verified": all(checks.values()), "checks": checks, "distance": dxy, "angle": angle, "sweep": sweep}

if __name__ == "__main__":
    print(prove())
