"""A01, A03, A04, A05: total basis, physical sector selection and occupations
(docs/toy-models/toy0/implementation-design.md Sections 6-11)."""

from __future__ import annotations

import numpy as np

from cosmobox_c_model.models.model0a.basis_config import build_total_basis
from cosmobox_c_model.models.model0a.observables import build_physical_occupations
from cosmobox_c_model.models.model0a.operators import PHYSICAL_STATES, select_physical_inclusion


def test_a01_total_dimension_is_72():
    basis = build_total_basis()
    assert basis.dimension == 72


def test_a03_physical_sector_dimension_is_3():
    basis = build_total_basis()
    inclusion = select_physical_inclusion(basis)
    assert inclusion.shape == (72, 3)


def test_a04_physical_states_are_exactly_l_m_r():
    assert PHYSICAL_STATES == (
        (1, 0, 0, 1, 0),
        (0, 1, 0, 0, 0),
        (0, 0, 1, 0, -1),
    )


def test_a05_occupation_matrices_and_their_sum():
    basis = build_total_basis()
    inclusion = select_physical_inclusion(basis)
    occupations = build_physical_occupations(basis, inclusion)
    n0, n1, n2 = occupations["n_0"], occupations["n_1"], occupations["n_2"]

    np.testing.assert_allclose(n0.real, np.diag([1, 0, 0]), atol=1e-12)
    np.testing.assert_allclose(n1.real, np.diag([0, 1, 0]), atol=1e-12)
    np.testing.assert_allclose(n2.real, np.diag([0, 0, 1]), atol=1e-12)
    np.testing.assert_allclose((n0 + n1 + n2).real, np.eye(3), atol=1e-12)
