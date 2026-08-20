"""Generic finite composite state spaces: deterministic enumeration, indexing,
sub-action embedding, common-kernel selection, and subspace restriction.

Independent of any particular model: domains, slots and operators are all
supplied by the caller.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Sequence

import numpy as np

SCIENTIFIC_METADATA = {
    "status": "established",
    "origin_model": None,
    "normative_reference": None,
}

State = tuple
ActionResult = "tuple[State, complex] | None"
Action = Callable[[State], ActionResult]


@dataclass(frozen=True)
class Basis:
    """A deterministic enumeration of composite states built from ordered local domains."""

    domains: tuple[tuple[object, ...], ...]
    states: tuple[tuple[object, ...], ...]
    index_of: dict[tuple[object, ...], int]

    @property
    def dimension(self) -> int:
        return len(self.states)

    def state_at(self, index: int) -> tuple[object, ...]:
        return self.states[index]

    def index_of_state(self, state: Sequence[object]) -> int:
        return self.index_of[tuple(state)]

    def unit_vector(self, index: int) -> np.ndarray:
        vector = np.zeros(self.dimension, dtype=complex)
        vector[index] = 1.0
        return vector


def build_composite_basis(domains: Sequence[Sequence[object]]) -> Basis:
    """Enumerate the Cartesian product of `domains` in deterministic lexicographic
    order: the first domain varies slowest, the last domain varies fastest.

    The caller chooses both the order of the domains and the order of values
    within each domain; this function only guarantees a fixed, auditable
    enumeration for a given input.
    """
    domains_t = tuple(tuple(domain) for domain in domains)
    states: list[tuple[object, ...]] = [()]
    for domain in domains_t:
        states = [state + (value,) for state in states for value in domain]
    states_t = tuple(states)
    index_of = {state: i for i, state in enumerate(states_t)}
    return Basis(domains=domains_t, states=states_t, index_of=index_of)


def embed_action(action: Action, *, slots: Sequence[int], total_arity: int) -> Action:
    """Embed an `action` defined on a sub-tuple at positions `slots` into an action
    on full composite states of arity `total_arity`, leaving all other slots
    unchanged. `total_arity` is accepted for interface symmetry with the composite
    state shape it embeds into; it is not otherwise used since positions outside
    `slots` are copied verbatim regardless of the state's total length.
    """

    def embedded(state: State) -> ActionResult:
        sub_state = tuple(state[i] for i in slots)
        result = action(sub_state)
        if result is None:
            return None
        new_sub_state, amplitude = result
        new_state = list(state)
        for slot, value in zip(slots, new_sub_state):
            new_state[slot] = value
        return tuple(new_state), amplitude

    return embedded


def common_kernel(operators: Sequence[np.ndarray], *, atol: float) -> np.ndarray:
    """Return an orthonormal basis (as columns) of the joint zero-eigenspace of a
    family of square operators, i.e. the common kernel of `operators`.

    Computed as the kernel of the vertically stacked operators via a direct SVD
    (never via a Gram matrix), so it works whether the family under-determines or
    over-determines the space. The returned matrix has shape (dim, k), where k is
    the dimension of the joint kernel.
    """
    if not operators:
        raise ValueError("at least one operator is required")
    dim = operators[0].shape[0]
    stacked = np.zeros((0, dim), dtype=complex)
    for operator in operators:
        if operator.shape != (dim, dim):
            raise ValueError("all operators must share the same square shape")
        stacked = np.vstack([stacked, operator])

    _, singular_values, vh = np.linalg.svd(stacked, full_matrices=True)
    n_domain = vh.shape[1]
    padded = np.zeros(n_domain, dtype=float)
    padded[: singular_values.shape[0]] = singular_values
    kernel_mask = padded <= atol
    return vh[kernel_mask].conj().T


def restrict_operator(operator: np.ndarray, inclusion: np.ndarray) -> np.ndarray:
    """Restrict `operator` to the subspace spanned by the columns of `inclusion`:
    computes Q^dagger O Q, where the columns of `inclusion` (Q) are assumed to be
    an orthonormal basis of the target subspace expressed in the ambient basis.
    """
    return inclusion.conj().T @ operator @ inclusion
