"""Elementary Toy Model 0B operators on the physical basis: local matter
number n_i, local electric field E_i, and the directed gauge-invariant
hopping h_i = c_i^dagger U_i c_{i+1} together with its hermitian combination
X_i = h_i + h_i^dagger (docs/toy-models/toy0b/specification.md Sections 3-4).

The physical basis built by `basis_config.build_physical_basis` already IS
H_phys (the periodic-Gauss-selected sector), not a dense ambient Cartesian
product. The individual actions c_i, c_i^dagger and U_i do not generally
preserve H_phys on their own, so this module never builds standalone
creation/annihilation/link-raise matrices on the physical basis. Instead
h_i is implemented as a single atomic action combining the matter
annihilation at site (i+1) mod 6, the truncated link raise on E_i, and the
matter creation at site i, evaluated directly on the flattened physical
state tuple.

No Hamiltonian assembly is performed here.
"""

from __future__ import annotations

import numpy as np

from cosmobox_c_model.core.fermions import apply_annihilation, apply_creation
from cosmobox_c_model.core.operators import build_operator_from_action
from cosmobox_c_model.core.state_space import Basis
from cosmobox_c_model.models.model0b.constants import N_SITES

State = tuple[int, ...]
ActionResult = "tuple[State, complex] | None"


def _validate_index(index: int, *, name: str) -> None:
    if not isinstance(index, int) or isinstance(index, bool):
        raise TypeError(f"{name} must be an int, got {type(index).__name__}")
    if not (0 <= index < N_SITES):
        raise ValueError(f"{name} must be in 0..{N_SITES - 1}, got {index}")


def _validate_lambda_cutoff(lambda_cutoff: int) -> None:
    if not isinstance(lambda_cutoff, int) or isinstance(lambda_cutoff, bool):
        raise TypeError("lambda_cutoff must be an int")
    if lambda_cutoff < 1:
        raise ValueError("lambda_cutoff must be >= 1")


def _validate_basis_cutoff_consistency(basis: Basis, lambda_cutoff: int) -> None:
    """The supplied `basis` must have been built at exactly `lambda_cutoff`: its
    six electric coordinate domains must each equal
    (-lambda_cutoff,...,+lambda_cutoff). Truncation is scientific model state
    and must never be inferred or silently mismatched."""
    expected_electric_domain = tuple(range(-lambda_cutoff, lambda_cutoff + 1))
    electric_domains = basis.domains[N_SITES:]
    if any(domain != expected_electric_domain for domain in electric_domains):
        raise ValueError(
            "basis electric coordinate domains are not consistent with the "
            "supplied lambda_cutoff"
        )


def build_number_operator(basis: Basis, site: int) -> np.ndarray:
    """n_site |state> = n_site(state) |state> (specification.md Section 3)."""
    _validate_index(site, name="site")

    def action(state: State) -> ActionResult:
        return state, complex(state[site])

    return build_operator_from_action(basis, action)


def build_electric_operator(basis: Basis, link: int) -> np.ndarray:
    """E_link |state> = E_link(state) |state> (specification.md Section 3)."""
    _validate_index(link, name="link")
    slot = N_SITES + link

    def action(state: State) -> ActionResult:
        return state, complex(state[slot])

    return build_operator_from_action(basis, action)


def _directed_hop_action(link: int, lambda_cutoff: int):
    partner = (link + 1) % N_SITES

    def action(state: State) -> ActionResult:
        matter = state[:N_SITES]
        links = state[N_SITES:]

        annihilation = apply_annihilation(matter, partner)
        if annihilation is None:
            return None
        matter_after_annihilation, annihilation_amplitude = annihilation

        current_e = links[link]
        if current_e == lambda_cutoff:
            return None

        creation = apply_creation(matter_after_annihilation, link)
        if creation is None:
            return None
        new_matter, creation_amplitude = creation

        new_links = list(links)
        new_links[link] = current_e + 1

        new_state = new_matter + tuple(new_links)
        amplitude = annihilation_amplitude * creation_amplitude
        return new_state, amplitude

    return action


def build_directed_hop_operator(basis: Basis, link: int, *, lambda_cutoff: int) -> np.ndarray:
    """h_link = c_link^dagger U_link c_{(link+1) mod 6} (specification.md
    Sections 3-4): a single atomic gauge-invariant action on the physical
    basis, forward-truncated (E_link=+lambda_cutoff annihilates)."""
    _validate_index(link, name="link")
    _validate_lambda_cutoff(lambda_cutoff)
    _validate_basis_cutoff_consistency(basis, lambda_cutoff)
    action = _directed_hop_action(link, lambda_cutoff)
    return build_operator_from_action(basis, action)


def build_x_operator(basis: Basis, link: int, *, lambda_cutoff: int) -> np.ndarray:
    """X_link = h_link + h_link^dagger (specification.md Section 4)."""
    hop = build_directed_hop_operator(basis, link, lambda_cutoff=lambda_cutoff)
    return hop + hop.conj().T
