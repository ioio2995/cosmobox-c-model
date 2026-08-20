"""D01-D04: the F_delta instrumental conditioning sweep
(docs/toy-models/toy0/implementation-design.md Sections 26-27)."""

from __future__ import annotations

import numpy as np
import pytest

from cosmobox_c_model.core.identifiability import analyze_identifiability, build_measurement_matrix
from cosmobox_c_model.models.model0a import constants
from cosmobox_c_model.models.model0a.basis_config import build_total_basis
from cosmobox_c_model.models.model0a.observables import build_f_delta, build_hs_basis, build_physical_observables

EXPECTED_RANK = {
    1e-2: 2, 1e-4: 2, 1e-6: 2, 1e-8: 2, 1e-10: 2,
    1e-13: 1, 0.0: 1,
}


def _sigma_plus(delta: float) -> float:
    return 0.5 * np.sqrt(2 + delta**2 + np.sqrt(4 + delta**4))


def _sigma_minus(delta: float) -> float:
    if delta == 0:
        return 0.0
    return abs(delta) / (2 * _sigma_plus(delta))


def _analyze(delta: float):
    basis = build_total_basis()
    observables = build_physical_observables(basis)
    hs_basis = build_hs_basis(observables)
    family = build_f_delta(observables, delta)
    matrix = build_measurement_matrix(family, hs_basis, imag_atol=constants.MEASUREMENT_IMAG_ATOL)
    return analyze_identifiability(matrix, rank_tolerance=constants.RANK_EPSILON)


@pytest.mark.parametrize("delta", constants.F_DELTA_SWEEP)
def test_d01_raw_singular_values_match_the_analytic_oracle(delta):
    result = _analyze(delta)
    expected = sorted([_sigma_plus(delta), _sigma_minus(delta)], reverse=True)
    raw_sorted = sorted(result.singular_values_raw, reverse=True)
    np.testing.assert_allclose(raw_sorted, expected, atol=constants.SINGULAR_VALUE_ATOL)


@pytest.mark.parametrize("delta", [d for d in constants.F_DELTA_SWEEP if d != 0.0])
def test_d02_compact_condition_number_matches_the_analytic_ratio(delta):
    result = _analyze(delta)
    sigma_plus = float(np.max(result.singular_values_raw))
    sigma_minus = float(np.min(result.singular_values_raw))
    expected_ratio = _sigma_plus(delta) / _sigma_minus(delta)
    assert abs(sigma_plus / sigma_minus - expected_ratio) / expected_ratio < 1e-6


@pytest.mark.parametrize("delta", constants.F_DELTA_SWEEP)
def test_d03_numerical_rank_matches_the_preregistered_sweep_table(delta):
    result = _analyze(delta)
    assert result.numerical_rank == EXPECTED_RANK[delta]


def test_d04_raw_spectrum_is_preserved_below_rank_epsilon_for_delta_1e_13():
    result = _analyze(1e-13)
    smaller = float(np.min(result.singular_values_raw))
    assert 0 < smaller < constants.RANK_EPSILON
    assert result.numerical_rank == 1
    # The raw (pre-threshold) spectrum still carries both singular values: the
    # report can distinguish mathematical_active_rank=2 from rank_epsilon=1.
    assert result.singular_values_raw.shape[0] == 2
