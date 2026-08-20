"""B01-B06: construction, gauge invariance, projected matrices, and the
projected (not global) composition identity
(docs/toy-models/toy0/implementation-design.md Sections 12-14)."""

from __future__ import annotations

import numpy as np

from cosmobox_c_model.core.state_space import restrict_operator
from cosmobox_c_model.models.model0a.basis_config import build_total_basis
from cosmobox_c_model.models.model0a.operators import (
    build_gauss_operators,
    build_relational_operators,
    select_physical_inclusion,
)


def test_b01_b03_operators_are_deterministic_from_the_action_construction():
    # Regression guard: two independent constructions from the same primitives
    # must agree, since no target matrix is injected.
    basis = build_total_basis()
    o01_a, o12_a, o02_a = build_relational_operators(basis)
    o01_b, o12_b, o02_b = build_relational_operators(basis)
    np.testing.assert_allclose(o01_a, o01_b)
    np.testing.assert_allclose(o12_a, o12_b)
    np.testing.assert_allclose(o02_a, o02_b)


def test_b04_gauge_invariance_on_the_full_72_dim_space():
    basis = build_total_basis()
    g0, g1, g2 = build_gauss_operators(basis)
    o01, o12, o02 = build_relational_operators(basis)

    for gauss_operator in (g0, g1, g2):
        for observable in (o01, o12, o02):
            commutator = gauss_operator @ observable - observable @ gauss_operator
            assert np.max(np.abs(commutator)) < 1e-12


def test_b05_projected_matrices_match_the_oracle():
    basis = build_total_basis()
    inclusion = select_physical_inclusion(basis)
    o01, o12, o02 = build_relational_operators(basis)

    o01_phys = restrict_operator(o01, inclusion)
    o12_phys = restrict_operator(o12, inclusion)
    o02_phys = restrict_operator(o02, inclusion)

    expected_o01 = np.array([[0, 1, 0], [0, 0, 0], [0, 0, 0]], dtype=complex)  # |L><M|
    expected_o12 = np.array([[0, 0, 0], [0, 0, 1], [0, 0, 0]], dtype=complex)  # |M><R|
    expected_o02 = np.array([[0, 0, 1], [0, 0, 0], [0, 0, 0]], dtype=complex)  # |L><R|

    np.testing.assert_allclose(o01_phys, expected_o01, atol=1e-12)
    np.testing.assert_allclose(o12_phys, expected_o12, atol=1e-12)
    np.testing.assert_allclose(o02_phys, expected_o02, atol=1e-12)


def test_b06_composition_identity_is_only_projected_never_global():
    basis = build_total_basis()
    inclusion = select_physical_inclusion(basis)
    o01, o12, o02 = build_relational_operators(basis)

    composition_total = o01 @ o12
    assert not np.allclose(composition_total, o02, atol=1e-9)

    composition_phys = restrict_operator(composition_total, inclusion)
    o02_phys = restrict_operator(o02, inclusion)
    np.testing.assert_allclose(composition_phys, o02_phys, atol=1e-12)
