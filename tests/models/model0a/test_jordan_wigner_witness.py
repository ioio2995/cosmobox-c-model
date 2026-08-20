"""B07, B08: the Jordan-Wigner witness chi and the full-space non-identity norm
(docs/toy-models/toy0/implementation-design.md Section 14.1)."""

from __future__ import annotations

import numpy as np

from cosmobox_c_model.models.model0a.basis_config import build_total_basis
from cosmobox_c_model.models.model0a.observables import CHI_STATE, CHI_TARGET_STATE
from cosmobox_c_model.models.model0a.operators import build_relational_operators


def test_b07_jordan_wigner_witness_produces_the_expected_signs():
    basis = build_total_basis()
    o01, o12, o02 = build_relational_operators(basis)

    chi_index = basis.index_of_state(CHI_STATE)
    chi_vector = basis.unit_vector(chi_index)

    o01_o12_chi = o01 @ (o12 @ chi_vector)
    np.testing.assert_allclose(o01_o12_chi, 0, atol=1e-12)

    o02_chi = o02 @ chi_vector
    target_index = basis.index_of_state(CHI_TARGET_STATE)
    expected = np.zeros(basis.dimension, dtype=complex)
    expected[target_index] = -1.0
    np.testing.assert_allclose(o02_chi, expected, atol=1e-12)


def test_b08_non_identity_frobenius_norm_on_the_full_space():
    basis = build_total_basis()
    o01, o12, o02 = build_relational_operators(basis)
    difference = o01 @ o12 - o02
    frobenius_norm = np.linalg.norm(difference, ord="fro")
    assert abs(frobenius_norm - 2.0) < 1e-12
