"""A01, A03, A04, A05: total basis, physical sector selection and occupations
(docs/toy-models/toy0/implementation-design.md Sections 6-11)."""

from __future__ import annotations

import numpy as np

from cosmobox_c_model.models.model0a import constants
from cosmobox_c_model.models.model0a.basis_config import build_total_basis
from cosmobox_c_model.models.model0a.observables import build_physical_occupations
from cosmobox_c_model.models.model0a.operators import discover_physical_states, select_physical_inclusion


def test_a01_total_dimension_is_72():
    basis = build_total_basis()
    assert basis.dimension == 72


def test_a03_physical_sector_dimension_is_3():
    # Independent discovery from the Gauss constraints: discover_physical_states
    # tests every basis state directly against G_0, G_1, G_2, never through a
    # kernel basis whose orientation (for a degenerate subspace) an SVD is free
    # to choose arbitrarily. This is not the shape of the production inclusion
    # matrix, which is itself sized from exactly this discovery, not the reverse.
    basis = build_total_basis()
    discovered = discover_physical_states(basis)
    assert len(discovered) == 3


def test_a04_physical_states_are_exactly_l_m_r():
    # The oracle here: written directly as literals, since the actual content of
    # the discovered physical sector is precisely what this test verifies.
    basis = build_total_basis()
    discovered = discover_physical_states(basis)
    expected_states = {
        (1, 0, 0, 1, 0),   # L = |100;+1,0>
        (0, 1, 0, 0, 0),   # M = |010;0,0>
        (0, 0, 1, 0, -1),  # R = |001;0,-1>
    }
    assert set(discovered.keys()) == expected_states


def test_a04b_physical_inclusion_is_ordered_l_m_r():
    # select_physical_inclusion() orders the *discovered* states by
    # _physical_order_key (site of the matter occupation), never by filtering
    # against a named L/M/R oracle. Verify directly that this model-specific,
    # oracle-independent rule nonetheless produces the frozen (L, M, R) order,
    # and that each column is exactly the corresponding canonical basis vector
    # (discover_physical_states never rotates or renormalizes it).
    basis = build_total_basis()
    inclusion = select_physical_inclusion(basis)
    expected_order = (
        (1, 0, 0, 1, 0),   # L
        (0, 1, 0, 0, 0),   # M
        (0, 0, 1, 0, -1),  # R
    )
    assert inclusion.shape == (basis.dimension, len(expected_order))
    for column, expected_state in enumerate(expected_order):
        expected_index = basis.index_of_state(expected_state)
        column_vector = inclusion[:, column]
        assert column_vector[expected_index] == 1
        assert np.count_nonzero(column_vector) == 1


def test_a05_occupation_matrices_and_their_sum():
    basis = build_total_basis()
    inclusion = select_physical_inclusion(basis)
    occupations = build_physical_occupations(basis, inclusion)
    n0, n1, n2 = occupations["n_0"], occupations["n_1"], occupations["n_2"]

    np.testing.assert_allclose(n0.real, np.diag([1, 0, 0]), atol=constants.EXACT_MATRIX_ATOL)
    np.testing.assert_allclose(n1.real, np.diag([0, 1, 0]), atol=constants.EXACT_MATRIX_ATOL)
    np.testing.assert_allclose(n2.real, np.diag([0, 0, 1]), atol=constants.EXACT_MATRIX_ATOL)
    np.testing.assert_allclose((n0 + n1 + n2).real, np.eye(3), atol=constants.EXACT_MATRIX_ATOL)
