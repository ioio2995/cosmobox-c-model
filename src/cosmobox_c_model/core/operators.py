"""Generic operator construction and decomposition utilities: turning an action
rule into a matrix (and back), and splitting an operator into hermitian parts.
"""

from __future__ import annotations

from typing import Callable, Sequence

import numpy as np

from cosmobox_c_model.core.state_space import Basis

SCIENTIFIC_METADATA = {
    "status": "established",
    "origin_model": None,
    "normative_reference": None,
}

State = tuple
ActionResult = "tuple[State, complex] | None"
Action = Callable[[State], ActionResult]


def build_operator_from_action(basis: Basis, action: Action) -> np.ndarray:
    """Build the matrix representation of an operator on `basis` from an action
    rule. `action(state)` must return `(new_state, amplitude)` for the image of a
    given basis state, or `None` if the operator annihilates it.
    """
    dimension = basis.dimension
    matrix = np.zeros((dimension, dimension), dtype=complex)
    for column, state in enumerate(basis.states):
        result = action(state)
        if result is None:
            continue
        new_state, amplitude = result
        row = basis.index_of_state(new_state)
        matrix[row, column] = amplitude
    return matrix


def action_from_matrix(matrix: np.ndarray, domain: Sequence[object]) -> Action:
    """Turn a dense matrix with at most one nonzero entry per column, acting on a
    1-tuple state drawn from `domain`, into an action function compatible with
    `build_operator_from_action` / `embed_action`. This is the practical inverse
    of `build_operator_from_action` for single-value domains and diagonal or
    shift-like operators; it does not support genuinely superposed actions
    (more than one nonzero entry per column).
    """
    domain_t = tuple(domain)

    def action(state: State) -> ActionResult:
        (value,) = state
        column_index = domain_t.index(value)
        column = matrix[:, column_index]
        nonzero_rows = np.flatnonzero(column)
        if nonzero_rows.size == 0:
            return None
        row = int(nonzero_rows[0])
        return (domain_t[row],), complex(column[row])

    return action


def hermitian_parts(operator: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Return (X, Y) such that O = X + iY, with X = (O+O-dagger)/2 and
    Y = (O-O-dagger)/(2i)."""
    x = (operator + operator.conj().T) / 2
    y = (operator - operator.conj().T) / (2j)
    return x, y
