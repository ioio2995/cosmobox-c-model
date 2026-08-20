"""Model-free unit tests for cosmobox_c_model.core.state_space."""

from __future__ import annotations

import numpy as np

from cosmobox_c_model.core.state_space import (
    build_composite_basis,
    common_kernel,
    embed_action,
    restrict_operator,
)


def test_build_composite_basis_enumerates_cartesian_product_in_order():
    basis = build_composite_basis([(0, 1), ("a", "b", "c")])
    assert basis.dimension == 6
    assert basis.states == (
        (0, "a"), (0, "b"), (0, "c"),
        (1, "a"), (1, "b"), (1, "c"),
    )
    assert basis.index_of_state((1, "b")) == 4
    assert basis.state_at(4) == (1, "b")


def test_basis_unit_vector_is_one_hot():
    basis = build_composite_basis([(0, 1, 2)])
    vector = basis.unit_vector(1)
    np.testing.assert_allclose(vector, [0, 1, 0])


def test_common_kernel_of_diagonal_constraint_family():
    # Two diagonal "constraints" on a 4-dim toy space; the joint kernel is the
    # span of the single basis vector where both are exactly zero.
    g0 = np.diag([0.0, 1.0, 0.0, 1.0])
    g1 = np.diag([0.0, 0.0, 1.0, 1.0])
    kernel = common_kernel([g0, g1], atol=1e-9)
    assert kernel.shape == (4, 1)
    projector = kernel @ kernel.conj().T
    expected_projector = np.diag([1.0, 0.0, 0.0, 0.0])
    np.testing.assert_allclose(projector.real, expected_projector, atol=1e-9)


def test_common_kernel_with_fewer_operators_than_dimension():
    # A single zero operator constrains nothing: the joint kernel is the whole space.
    zero_operator = np.zeros((3, 3))
    kernel = common_kernel([zero_operator], atol=1e-9)
    assert kernel.shape == (3, 3)


def test_restrict_operator_extracts_submatrix():
    operator = np.arange(9, dtype=complex).reshape(3, 3)
    inclusion = np.zeros((3, 2), dtype=complex)
    inclusion[0, 0] = 1.0
    inclusion[2, 1] = 1.0
    restricted = restrict_operator(operator, inclusion)
    expected = np.array([[operator[0, 0], operator[0, 2]], [operator[2, 0], operator[2, 2]]])
    np.testing.assert_allclose(restricted, expected)


def test_embed_action_leaves_other_slots_untouched():
    def toy_action(sub_state):
        (value,) = sub_state
        if value == "x":
            return None
        return ("y" if value == "z" else "z",), 2.0

    action = embed_action(toy_action, slots=(1,), total_arity=3)

    result = action(("a", "z", "b"))
    assert result == (("a", "y", "b"), 2.0)

    assert action(("a", "x", "b")) is None


def test_embed_action_with_multi_slot_sub_action():
    def swap_first_two(sub_state):
        a, b = sub_state
        return (b, a), 1.0

    action = embed_action(swap_first_two, slots=(0, 2), total_arity=3)
    result = action(("p", "q", "r"))
    assert result == (("r", "q", "p"), 1.0)
