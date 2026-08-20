"""Model-free unit tests for cosmobox_c_model.core.operators, using synthetic
toy bases and action rules independent of any model."""

from __future__ import annotations

import numpy as np
import pytest

from cosmobox_c_model.core.operators import action_from_matrix, build_operator_from_action, hermitian_parts
from cosmobox_c_model.core.state_space import build_composite_basis


def test_build_operator_from_action_matches_an_explicit_matrix():
    basis = build_composite_basis([(0, 1, 2)])

    def shift_up(state):
        (value,) = state
        if value == 2:
            return None
        return (value + 1,), 1.0

    matrix = build_operator_from_action(basis, shift_up)
    expected = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0]], dtype=complex)
    np.testing.assert_allclose(matrix, expected)


def test_action_from_matrix_round_trips_build_operator_from_action():
    basis = build_composite_basis([(0, 1, 2)])
    original = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0]], dtype=complex)
    action = action_from_matrix(original, (0, 1, 2))
    rebuilt = build_operator_from_action(basis, action)
    np.testing.assert_allclose(rebuilt, original)


def test_action_from_matrix_returns_none_for_a_zero_column():
    matrix = np.array([[0, 0], [0, 0]], dtype=complex)
    action = action_from_matrix(matrix, (0, 1))
    assert action((0,)) is None


def test_action_from_matrix_rejects_a_shape_incompatible_with_the_domain():
    matrix = np.zeros((3, 3), dtype=complex)
    with pytest.raises(ValueError):
        action_from_matrix(matrix, (0, 1))  # domain has size 2, matrix is 3x3


def test_action_from_matrix_rejects_a_non_square_matrix():
    matrix = np.zeros((2, 3), dtype=complex)
    with pytest.raises(ValueError):
        action_from_matrix(matrix, (0, 1, 2))


def test_action_from_matrix_rejects_a_column_with_more_than_one_nonzero_entry():
    matrix = np.array([[1, 0], [1, 0]], dtype=complex)  # column 0 has two entries
    with pytest.raises(ValueError):
        action_from_matrix(matrix, (0, 1))


def test_hermitian_parts_reconstruct_the_operator():
    operator = np.array([[1, 2 + 1j], [0, 3]], dtype=complex)
    x, y = hermitian_parts(operator)
    np.testing.assert_allclose(x, x.conj().T)
    np.testing.assert_allclose(y, y.conj().T)
    np.testing.assert_allclose(x + 1j * y, operator)


def test_hermitian_parts_of_a_hermitian_operator_has_zero_y():
    operator = np.array([[1, 2 - 1j], [2 + 1j, 3]], dtype=complex)
    x, y = hermitian_parts(operator)
    np.testing.assert_allclose(x, operator)
    np.testing.assert_allclose(y, np.zeros_like(y), atol=1e-12)
