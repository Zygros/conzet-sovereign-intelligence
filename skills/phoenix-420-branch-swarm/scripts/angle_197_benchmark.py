#!/usr/bin/env python3
"""Deterministic ablation benchmark for the Phoenix 19.7-degree anchor.

Compares angular alignment against the canonical 19.7° anchor, a zero-anchor
control, and a deliberately perturbed angle. This is a geometry/control
benchmark, not evidence of improved AGI capability by itself.
"""
from __future__ import annotations

from math import pi
from hyperbolic_time_engine import PHOENIX_ANGLE_DEG, PHOENIX_ANGLE_RAD, angular_alignment


def run() -> dict[str, object]:
    controls_deg = (0.0, 10.0, 19.7, 30.0, 45.0)
    rows = []
    for angle_deg in controls_deg:
        angle_rad = angle_deg * pi / 180.0
        rows.append({
            "angle_deg": angle_deg,
            "alignment": angular_alignment(angle_rad),
            "is_anchor": abs(angle_deg - PHOENIX_ANGLE_DEG) < 1e-12,
        })
    anchor = next(r for r in rows if r["is_anchor"])
    return {
        "anchor_deg": PHOENIX_ANGLE_DEG,
        "anchor_rad": PHOENIX_ANGLE_RAD,
        "anchor_alignment": anchor["alignment"],
        "controls": rows,
        "verified": abs(anchor["anchor_alignment"] if "anchor_alignment" in anchor else anchor["alignment"] - 1.0) < 1e-12,
        "note": "Performance claims require a task-level ablation; this benchmark verifies the angular primitive and control structure only.",
    }


if __name__ == "__main__":
    print(run())
