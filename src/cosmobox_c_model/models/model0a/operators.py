"""Assembly of the Toy Model 0A operators from generic core primitives
(docs/toy-models/toy0/implementation-design.md Sections 6-14).
"""

from __future__ import annotations

import numpy as np

from cosmobox_c_model.core import fermions, ladder
from cosmobox_c_model.core.operators import action_from_matrix, build_operator_from_action
from cosmobox_c_model.core.state_space import Basis, embed_action
from cosmobox_c_model.models.model0a import constants
from cosmobox_c_model.models.model0a.basis_config import FLUX_DOMAIN

TOTAL_ARITY = 5  # (n0, n1, n2, E01, E12)
OCCUPATION_SLOTS = (0, 1, 2)
LINK_SLOTS = {"01": 3, "12": 4}
N_SITES = len(OCCUPATION_SLOTS)


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
    """Discover the Gauss-selected physical sector by testing every basis state
    individually against the three constraints (implementation-design.md
    Section 9), never via the orientation of a kernel basis returned by an SVD.

    A degenerate zero-eigenspace has no unique orthonormal basis: any unitary
    rotation within it is an equally valid set of singular vectors, so a kernel
    computed via `core.state_space.common_kernel` cannot in general be assumed
    to align with the ambient basis. This function sidesteps that entirely by
    never computing a joint kernel: a basis state |s> is physical iff
    G_k|s> = 0 (within `constants.EXACT_MATRIX_ATOL`) for k=0,1,2, tested
    directly on each of the basis's own canonical unit vectors.

    Returns ``{state: unit_vector}`` for every state found physical, in the
    basis's own deterministic enumeration order. Makes no use of, and performs
    no comparison against, the model's named physical states or their expected
    count: the content and dimension of the sector are a purely computed fact.
    """
    g0, g1, g2 = build_gauss_operators(basis)
    discovered: dict[tuple[int, ...], np.ndarray] = {}
    for index, state in enumerate(basis.states):
        unit_vector = basis.unit_vector(index)
        if all(
            np.linalg.norm(g @ unit_vector) <= constants.EXACT_MATRIX_ATOL
            for g in (g0, g1, g2)
        ):
            discovered[state] = unit_vector
    return discovered


def _physical_order_key(state: tuple[int, ...]) -> tuple[int, tuple[int, ...]]:
    """Deterministic, model-specific ordering key for a discovered physical
    state: primarily by the site index carrying the matter occupation (the
    position of the single `1` among n0, n1, n2), with the full state tuple as
    a tie-break for absolute determinism when that is not unique.

    Uses only the occupation structure of the state itself -- never a named
    physical state or PHYSICAL_STATES -- yet coincides with the frozen (L, M, R)
    order for 0A's expected sector, since L/M/R are exactly the states with the
    matter excitation at site 0/1/2 respectively.
    """
    occupation = state[:N_SITES]
    matter_site = occupation.index(1) if 1 in occupation else N_SITES
    return (matter_site, state)


def select_physical_inclusion(basis: Basis) -> np.ndarray:
    """Build Q from every state actually discovered by `discover_physical_states`
    -- never filtered, counted, or sized against any named physical state -- in
    the deterministic model-specific order of `_physical_order_key`.
    """
    discovered = discover_physical_states(basis)
    ordered_states = sorted(discovered.keys(), key=_physical_order_key)
    inclusion = np.zeros((basis.dimension, len(ordered_states)), dtype=complex)
    for column, state in enumerate(ordered_states):
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
