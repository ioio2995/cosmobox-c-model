"""E01: F2_prime reproduces F3 exactly -- a pipeline/plumbing check only
(docs/toy-models/toy0/implementation-design.md Section 25)."""

from __future__ import annotations

import numpy as np

from cosmobox_c_model.core.identifiability import analyze_identifiability, build_measurement_matrix
from cosmobox_c_model.models.model0a import constants
from cosmobox_c_model.models.model0a.basis_config import build_total_basis
from cosmobox_c_model.models.model0a.observables import (
    build_families,
    build_f2_prime,
    build_hs_basis,
    build_physical_observables,
    build_physical_occupations,
)


def test_e01_f2_prime_matches_f3():
    basis = build_total_basis()
    observables = build_physical_observables(basis)
    occupations = build_physical_occupations(basis, observables["inclusion"])
    hs_basis = build_hs_basis(observables)
    families = build_families(basis, occupations, observables)
    f2_prime = build_f2_prime(basis, occupations, observables)

    matrix_f3 = build_measurement_matrix(families["F3"], hs_basis, imag_atol=constants.MEASUREMENT_IMAG_ATOL)
    matrix_f2_prime = build_measurement_matrix(f2_prime, hs_basis, imag_atol=constants.MEASUREMENT_IMAG_ATOL)
    np.testing.assert_allclose(matrix_f2_prime, matrix_f3, atol=constants.EXACT_MATRIX_ATOL)

    result_f3 = analyze_identifiability(matrix_f3, rank_tolerance=constants.RANK_EPSILON)
    result_f2_prime = analyze_identifiability(matrix_f2_prime, rank_tolerance=constants.RANK_EPSILON)
    assert result_f2_prime.numerical_rank == result_f3.numerical_rank
    np.testing.assert_allclose(
        result_f2_prime.singular_values_domain,
        result_f3.singular_values_domain,
        atol=constants.SINGULAR_VALUE_ATOL,
    )
