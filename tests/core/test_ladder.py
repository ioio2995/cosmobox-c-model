"""Model-free unit tests for cosmobox_c_model.core.ladder, exercised on domain
sizes other than 3 to demonstrate genericity."""

from __future__ import annotations

import numpy as np

from cosmobox_c_model.core.ladder import build_flux_operator, build_truncated_raise_operator


def test_flux_operator_is_diagonal_with_domain_eigenvalues():
    e = build_flux_operator([-2, -1, 0, 1, 2])
    np.testing.assert_allclose(np.diag(e).real, [-2, -1, 0, 1, 2])
    off_diagonal = e - np.diag(np.diag(e))
    np.testing.assert_allclose(off_diagonal, 0)


def test_truncated_raise_operator_shifts_and_truncates_for_arbitrary_dimension():
    u = build_truncated_raise_operator(4)
    for i in range(3):
        expected_column = np.zeros(4)
        expected_column[i + 1] = 1.0
        np.testing.assert_allclose(u[:, i].real, expected_column)
    np.testing.assert_allclose(u[:, 3], np.zeros(4))  # truncated at the top level


def test_ladder_identities_for_a_unit_step_domain():
    domain = [-1, 0, 1]
    e = build_flux_operator(domain)
    u = build_truncated_raise_operator(len(domain))
    u_dagger = u.conj().T

    np.testing.assert_allclose(e @ u - u @ e, u, atol=1e-12)
    np.testing.assert_allclose(e @ u_dagger - u_dagger @ e, -u_dagger, atol=1e-12)
    np.testing.assert_allclose(u_dagger @ u, np.diag([1, 1, 0]), atol=1e-12)
    np.testing.assert_allclose(u @ u_dagger, np.diag([0, 1, 1]), atol=1e-12)


def test_ladder_identities_hold_for_a_larger_unit_step_domain():
    domain = [-2, -1, 0, 1, 2]
    e = build_flux_operator(domain)
    u = build_truncated_raise_operator(len(domain))
    np.testing.assert_allclose(e @ u - u @ e, u, atol=1e-12)


def test_raise_operator_is_never_unitary_at_the_boundary():
    u = build_truncated_raise_operator(3)
    identity = np.eye(3)
    assert not np.allclose(u.conj().T @ u, identity)
    assert not np.allclose(u @ u.conj().T, identity)
