"""Assembly of the Toy Model 0A operators from generic core primitives
(docs/toy-models/toy0/implementation-design.md Sections 6-14).
"""

from __future__ import annotations

import numpy as np

from cosmobox_c_model.core import fermions, ladder
from cosmobox_c_model.core.operators import action_from_matrix, build_operator_from_action
from cosmobox_c_model.core.state_space import Basis, common_kernel, embed_action
from cosmobox_c_model.models.model0a import constants
from cosmobox_c_model.models.model0a.basis_config import FLUX_DOMAIN

TOTAL_ARITY = 5  # (n0, n1, n2, E01, E12)
OCCUPATION_SLOTS = (0, 1, 2)
LINK_SLOTS = {"01": 3, "12": 4}

# Physical states in the frozen order (L, M, R) (implementation-design.md Section 10).
PHYSICAL_STATES: tuple[tuple[int, ...], ...] = (
    (1, 0, 0, 1, 0),   # L = |100;+1,0>
    (0, 1, 0, 0, 0),   # M = |010;0,0>
    (0, 0, 1, 0, -1),  # R = |001;0,-1>
)


def _fermion_action(kind: str, site: int):
    def action(sub_state):
        if kind == "annihilation":
            return fermions.apply_annihilation(sub_state, site)
        return fermions.apply_creation(sub_state, site)

    return action


def build_annihilation_operator(basis: Basis, site: int) -> np.ndarray:
    action = embed_action(
        _fermion_action("annihilation", site),
        slots=OCCUPATION_SLOTS,
        total_arity=TOTAL_ARITY,
    )
    return build_operator_from_action(basis, action)


def build_creation_operator(basis: Basis, site: int) -> np.ndarray:
    action = embed_action(
        _fermion_action("creation", site),
        slots=OCCUPATION_SLOTS,
        total_arity=TOTAL_ARITY,
    )
    return build_operator_from_action(basis, action)


def _link_matrices() -> tuple[np.ndarray, np.ndarray]:
    e = ladder.build_flux_operator(FLUX_DOMAIN)
    u = ladder.build_truncated_raise_operator(len(FLUX_DOMAIN))
    return e, u


def build_flux_operator(basis: Basis, link: str) -> np.ndarray:
    e, _ = _link_matrices()
    action = embed_action(
        action_from_matrix(e, FLUX_DOMAIN),
        slots=(LINK_SLOTS[link],),
        total_arity=TOTAL_ARITY,
    )
    return build_operator_from_action(basis, action)


def build_link_raise_operator(basis: Basis, link: str) -> np.ndarray:
    _, u = _link_matrices()
    action = embed_action(
        action_from_matrix(u, FLUX_DOMAIN),
        slots=(LINK_SLOTS[link],),
        total_arity=TOTAL_ARITY,
    )
    return build_operator_from_action(basis, action)


def build_gauss_operators(basis: Basis) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Build G_0, G_1, G_2 for the frozen background b = constants.BACKGROUND
    (implementation-design.md Section 9)."""
    n0 = build_creation_operator(basis, 0) @ build_annihilation_operator(basis, 0)
    n1 = build_creation_operator(basis, 1) @ build_annihilation_operator(basis, 1)
    n2 = build_creation_operator(basis, 2) @ build_annihilation_operator(basis, 2)

    e01 = build_flux_operator(basis, "01")
    e12 = build_flux_operator(basis, "12")

    b0, b1, b2 = constants.BACKGROUND
    identity = np.eye(basis.dimension, dtype=complex)
    q0 = n0 - b0 * identity
    q1 = n1 - b1 * identity
    q2 = n2 - b2 * identity

    g0 = e01 - q0
    g1 = e12 - e01 - q1
    g2 = -e12 - q2
    return g0, g1, g2


def discover_physical_states(basis: Basis) -> dict[tuple[int, ...], np.ndarray]:
    """Discover the Gauss-selected physical sector purely from the constraints:
    returns ``{state: kernel_column}`` for every axis-aligned direction found in
    the joint kernel of G_0, G_1, G_2, in whatever order the kernel computation
    returns them.

    This performs no comparison against, and makes no use of, the model's named
    physical states or their expected count: the dimension and content of the
    sector are purely a computed fact. Each column is phase-normalized so its
    dominant entry is exactly 1. Raises `ValueError` if a kernel direction is not
    axis-aligned within `constants.EXACT_MATRIX_ATOL` -- a structural property of
    this (diagonal) Gauss construction, not an assumption about which states are
    physical.
    """
    g0, g1, g2 = build_gauss_operators(basis)
    kernel_vectors = common_kernel([g0, g1, g2], atol=constants.EXACT_MATRIX_ATOL)

    discovered: dict[tuple[int, ...], np.ndarray] = {}
    for column in range(kernel_vectors.shape[1]):
        vector = kernel_vectors[:, column]
        dominant_index = int(np.argmax(np.abs(vector)))
        dominant_magnitude = abs(vector[dominant_index])
        residual = np.sqrt(max(np.linalg.norm(vector) ** 2 - dominant_magnitude**2, 0.0))
        if dominant_magnitude < 1 - constants.EXACT_MATRIX_ATOL or residual > constants.EXACT_MATRIX_ATOL:
            raise ValueError(
                f"Gauss kernel direction {column} is not axis-aligned within "
                f"atol={constants.EXACT_MATRIX_ATOL!r}; the physical sector could "
                "not be discovered unambiguously"
            )
        normalized_vector = vector / vector[dominant_index]
        state = basis.state_at(dominant_index)
        discovered[state] = normalized_vector
    return discovered


def select_physical_inclusion(basis: Basis) -> np.ndarray:
    """Impose the frozen (L, M, R) order (implementation-design.md Section 10) on
    the physical sector discovered from the Gauss constraints. `PHYSICAL_STATES`
    is used here only to label and order the columns already discovered by
    `discover_physical_states`; it is never used to validate or fabricate the
    selection itself -- that validation lives exclusively in the acceptance
    tests (tests/models/model0a/test_basis_and_gauss.py, A03/A04).
    """
    discovered = discover_physical_states(basis)
    inclusion = np.zeros((basis.dimension, len(PHYSICAL_STATES)), dtype=complex)
    for column, state in enumerate(PHYSICAL_STATES):
        inclusion[:, column] = discovered[state]
    return inclusion


def build_relational_operators(basis: Basis) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """O_01 = c0-dagger U01 c1 ; O_12 = c1-dagger U12 c2 ;
    O_02 = c0-dagger U01 U12 c2 (implementation-design.md Section 12), action
    order explicitly right-to-left on kets via matrix multiplication."""
    c0_dagger = build_creation_operator(basis, 0)
    c1 = build_annihilation_operator(basis, 1)
    c1_dagger = build_creation_operator(basis, 1)
    c2 = build_annihilation_operator(basis, 2)
    u01 = build_link_raise_operator(basis, "01")
    u12 = build_link_raise_operator(basis, "12")

    o01 = c0_dagger @ u01 @ c1
    o12 = c1_dagger @ u12 @ c2
    o02 = c0_dagger @ u01 @ u12 @ c2
    return o01, o12, o02
