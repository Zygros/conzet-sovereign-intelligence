"""Regression checks for formulas transcribed from published Conzetian papers.

These tests preserve the printed equations and expose inconsistencies; they do
not silently rewrite the published papers or validate broader architecture claims.
"""
from math import e, isclose, sqrt


PHI = (1 + sqrt(5)) / 2
POWER_TOWER_THRESHOLD = e ** (1 / e)


def c_omega(t: int) -> float:
    """CΩ(t) as printed in the OmniNet v4 whitepaper."""
    if t < 0:
        raise ValueError("t must be a non-negative integer")
    return (PHI ** (2**t) + 1) / 2


def finite_tower(base: float, height: int) -> float:
    """Finite right-associated power tower with a repeated positive base."""
    if height < 1:
        raise ValueError("height must be at least 1")
    value = base
    for _ in range(height - 1):
        value = base**value
    return value


def test_phi_is_above_real_power_tower_convergence_threshold():
    assert PHI > POWER_TOWER_THRESHOLD


def test_phi_is_not_greater_than_e():
    """Guards against the R3 theorem statement typo 'phi > e'."""
    assert PHI < e


def test_c_omega_formula_values_as_printed():
    # The equation CΩ(t) = (φ^(2^t) + 1)/2 gives these values.
    # This test intentionally does not assert the different table values
    # printed in the whitepaper; the discrepancy is documented in the audit.
    assert isclose(c_omega(2), 3.9270509831, rel_tol=2e-3)
    assert isclose(c_omega(3), 23.9897948557, rel_tol=2e-3)
    assert isclose(c_omega(4), 1104.0, rel_tol=2e-3)


def test_finite_tower_base_cases_and_recurrence():
    assert isclose(finite_tower(PHI, 1), PHI, rel_tol=1e-12)
    assert isclose(finite_tower(PHI, 2), 2.178457567, rel_tol=2e-3)
    assert isclose(finite_tower(PHI, 3), 2.843, rel_tol=5e-3)


def test_invalid_tower_height_is_rejected():
    try:
        finite_tower(PHI, 0)
    except ValueError:
        pass
    else:
        raise AssertionError("height=0 must be rejected")
