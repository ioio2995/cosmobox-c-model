"""B07, B08: the Jordan-Wigner witness chi and the full-space non-identity norm
(docs/toy-models/toy0/implementation-design.md Section 14.1)."""

from __future__ import annotations

import numpy as np

from cosmobox_c_model.models.model0a import constants
from cosmobox_c_model.models.model0a.basis_config import build_total_basis
from cosmobox_c_model.models.model0a.observables import CHI_STATE, CHI_TARGET_STATE
from cosmobox_c_model.models.model0a.operators import build_relational_operators


def test_b07_jordan_wigner_witness_produces_the_expected_signs():
    # Coefficients here are exclusively 0 and -1: compare exactly, not with a
    # tolerance-based allclose.
    basis = build_total_basis()
    o01, o12, o02 = build_relational_operators(basis)

    chi_index = basis.index_of_state(CHI_STATE)
    chi_vector = basis.unit_vector(chi_index)

    o01_o12_chi = o01 @ (o12 @ chi_vector)
    assert np.array_equal(o01_o12_chi, np.zeros(basis.dimension, dtype=complex))

    o02_chi = o02 @ chi_vector
    target_index = basis.index_of_state(CHI_TARGET_STATE)
    expected = np.zeros(basis.dimension, dtype=complex)
    expected[target_index] = -1.0
    assert np.array_equal(o02_chi, expected)


def test_b08_non_identity_frobenius_norm_on_the_full_space():
    basis = build_total_basis()
    o01, o12, o02 = build_relational_operators(basis)
    difference = o01 @ o12 - o02
    frobenius_norm = np.linalg.norm(difference, ord="fro")
    assert abs(frobenius_norm - 2.0) < constants.EXACT_MATRIX_ATOL
