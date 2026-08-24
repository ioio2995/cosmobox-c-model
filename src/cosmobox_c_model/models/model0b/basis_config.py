"""Direct physical-basis construction for Toy Model 0B: oriented 6-cycle,
fixed background, half filling and periodic Gauss law
(docs/toy-models/toy0b/specification.md Section 3).

State field order, frozen here: (n0,n1,n2,n3,n4,n5, E0,E1,E2,E3,E4,E5). This
is the single place that fixes the deterministic enumeration order required
by software-architecture-governance.md Section 14.2.

The physical Hilbert space is the intersection of the kernels of the
periodic Gauss operators, not the dense Cartesian product of local matter
and link domains. This module therefore builds the constrained subset
directly from the frozen Gauss solution instead of enumerating the ambient
total space and filtering it (specification.md Section 3: "Construction
nominale : construire directement la base physique par Gauss, sans espace
total dense.").
"""

from __future__ import annotations

from itertools import product

from cosmobox_c_model.core.state_space import Basis
from cosmobox_c_model.models.model0b.constants import (
    BACKGROUND,
    MATTER_PARTICLE_NUMBER,
    N_SITES,
)

MATTER_DOMAIN: tuple[int, ...] = (0, 1)

# Field order of the emitted state tuple: six matter occupations followed by
# six electric link values.
STATE_FIELDS: tuple[str, ...] = (
    "n0",
    "n1",
    "n2",
    "n3",
    "n4",
    "n5",
    "E0",
    "E1",
    "E2",
    "E3",
    "E4",
    "E5",
)


def _matter_configurations() -> tuple[tuple[int, ...], ...]:
    """Enumerate the half-filled matter configurations n in {0,1}^N_SITES with
    sum(n) == MATTER_PARTICLE_NUMBER, in deterministic lexicographic order
    (specification.md Section 3)."""
    return tuple(
        n
        for n in product(MATTER_DOMAIN, repeat=N_SITES)
        if sum(n) == MATTER_PARTICLE_NUMBER
    )


def _charges(n: tuple[int, ...]) -> tuple[int, ...]:
    """q_i = n_i - b_i (specification.md Section 3)."""
    return tuple(n[i] - BACKGROUND[i] for i in range(N_SITES))


def _electric_offsets(n: tuple[int, ...]) -> tuple[int, ...]:
    """s_i(n) = sum_{k=0}^{i} q_k for i=0,...,N_SITES-1 (specification.md
    Section 3). Since sum_i q_i = 0 for a half-filled configuration against
    the frozen background, s_{N_SITES-1}(n) == 0."""
    charges = _charges(n)
    offsets = []
    running = 0
    for q in charges:
        running += q
        offsets.append(running)
    return tuple(offsets)


def _admissible_e_bounds(offsets: tuple[int, ...], lambda_cutoff: int) -> tuple[int, int]:
    """Admissible integer interval for the free cycle variable e := E_{N_SITES-1}
    (specification.md Section 3): e_min = -Lambda - min_i s_i,
    e_max = +Lambda - max_i s_i."""
    e_min = -lambda_cutoff - min(offsets)
    e_max = lambda_cutoff - max(offsets)
    return e_min, e_max


def build_physical_basis(lambda_cutoff: int) -> Basis:
    """Build the deterministic physical basis of Toy Model 0B at truncation
    `lambda_cutoff` by direct periodic Gauss construction (specification.md
    Section 3): exact dimension 40*lambda_cutoff-2 for lambda_cutoff>=1.

    States are ordered by ascending matter configuration (lexicographic in
    (n0,...,n5)), and for each matter configuration by ascending free cycle
    variable e := E_{N_SITES-1}.
    """
    if not isinstance(lambda_cutoff, int) or isinstance(lambda_cutoff, bool):
        raise TypeError("lambda_cutoff must be an int")
    if lambda_cutoff < 1:
        raise ValueError("lambda_cutoff must be >= 1")

    electric_domain = tuple(range(-lambda_cutoff, lambda_cutoff + 1))
    domains = (MATTER_DOMAIN,) * N_SITES + (electric_domain,) * N_SITES

    states: list[tuple[int, ...]] = []
    for n in _matter_configurations():
        offsets = _electric_offsets(n)
        e_min, e_max = _admissible_e_bounds(offsets, lambda_cutoff)
        for e in range(e_min, e_max + 1):
            links = tuple(e + s for s in offsets)
            states.append(n + links)

    states_t = tuple(states)
    index_of = {state: i for i, state in enumerate(states_t)}
    return Basis(domains=domains, states=states_t, index_of=index_of)
