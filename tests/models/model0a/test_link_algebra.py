"""A02: E, U, U-dagger identities, on the embedded 72-dimensional operators
(docs/toy-models/toy0/implementation-design.md Section 8)."""

from __future__ import annotations

import numpy as np

from cosmobox_c_model.models.model0a import constants
from cosmobox_c_model.models.model0a.basis_config import build_total_basis
from cosmobox_c_model.models.model0a.operators import build_flux_operator, build_link_raise_operator


def _identities_for_link(link: str):
    basis = build_total_basis()
    e = build_flux_operator(basis, link)
    u = build_link_raise_operator(basis, link)
    u_dagger = u.conj().T

    np.testing.assert_allclose(e @ u - u @ e, u, atol=constants.COMMUTATOR_ATOL)
    np.testing.assert_allclose(e @ u_dagger - u_dagger @ e, -u_dagger, atol=constants.COMMUTATOR_ATOL)


def test_a02_link_01_identities():
    _identities_for_link("01")


def test_a02_link_12_identities():
    _identities_for_link("12")


def test_a02_u_dagger_u_and_u_u_dagger_projectors():
    basis = build_total_basis()
    u = build_link_raise_operator(basis, "01")
    u_dagger = u.conj().T

    # These projectors act as diag(1,1,0) / diag(0,1,1) on the 3-level flux
    # sub-domain and as the identity on the rest of the 72-dim space; check the
    # eigenvalue multiplicities rather than a hardcoded full 72x72 matrix.
    udu_eigs = np.sort(np.linalg.eigvalsh(u_dagger @ u).real)
    uud_eigs = np.sort(np.linalg.eigvalsh(u @ u_dagger).real)
    n_boundary = basis.dimension // 3  # one third of states sit at flux level -1 (for U-dagger U)
    np.testing.assert_allclose(udu_eigs[:n_boundary], 0.0, atol=constants.EXACT_MATRIX_ATOL)
    np.testing.assert_allclose(udu_eigs[n_boundary:], 1.0, atol=constants.EXACT_MATRIX_ATOL)
    np.testing.assert_allclose(uud_eigs[:n_boundary], 0.0, atol=constants.EXACT_MATRIX_ATOL)
    np.testing.assert_allclose(uud_eigs[n_boundary:], 1.0, atol=constants.EXACT_MATRIX_ATOL)


def test_a02_u_is_never_unitary():
    basis = build_total_basis()
    u = build_link_raise_operator(basis, "01")
    identity = np.eye(basis.dimension)
    assert not np.allclose(u.conj().T @ u, identity)
    assert not np.allclose(u @ u.conj().T, identity)
