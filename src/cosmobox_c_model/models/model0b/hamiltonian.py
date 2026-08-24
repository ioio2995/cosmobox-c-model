"""Frozen Toy Model 0B static aggregates and Hamiltonian assembly
(docs/toy-models/toy0b/specification.md Section 4):

    N_even  = n_0 + n_2 + n_4
    V0      = sum_i E_i^2
    V_delta = sum_i (-1)^i E_i^2
    H_hop   = -sum_i X_i
    H(g,mu,delta) = H_hop + g*V0 + 2*mu*N_even + g*delta*V_delta

with the energy unit J == 1 frozen for Toy Model 0B (no J parameter is
exposed).

This module is assembly only: it composes the elementary operators accepted
in I1-B (`models.model0b.operators`) with the frozen coefficients above. It
performs no diagonalization, no eigenvalue/ground-state computation, no
reflection covariance, and no campaign execution.
"""

from __future__ import annotations

import numpy as np

from cosmobox_c_model.core.state_space import Basis
from cosmobox_c_model.models.model0b.constants import N_SITES
from cosmobox_c_model.models.model0b.operators import (
    build_electric_operator,
    build_number_operator,
    build_x_operator,
)

N_EVEN_SITES = (0, 2, 4)


def build_n_even(basis: Basis) -> np.ndarray:
    """N_even = n_0 + n_2 + n_4 (specification.md Section 4)."""
    return sum(build_number_operator(basis, site) for site in N_EVEN_SITES)


def build_v0(basis: Basis) -> np.ndarray:
    """V0 = sum_i E_i^2 (specification.md Section 4)."""
    total = np.zeros((basis.dimension, basis.dimension), dtype=complex)
    for link in range(N_SITES):
        e_link = build_electric_operator(basis, link)
        total = total + e_link @ e_link
    return total


def build_v_delta(basis: Basis) -> np.ndarray:
    """V_delta = sum_i (-1)^i E_i^2 (specification.md Section 4)."""
    total = np.zeros((basis.dimension, basis.dimension), dtype=complex)
    for link in range(N_SITES):
        e_link = build_electric_operator(basis, link)
        sign = 1 if link % 2 == 0 else -1
        total = total + sign * (e_link @ e_link)
    return total


def build_h_hop(basis: Basis, *, lambda_cutoff: int) -> np.ndarray:
    """H_hop = -sum_i X_i (specification.md Section 4), J == 1 frozen."""
    total = np.zeros((basis.dimension, basis.dimension), dtype=complex)
    for link in range(N_SITES):
        total = total + build_x_operator(basis, link, lambda_cutoff=lambda_cutoff)
    return -total


def build_hamiltonian(
    basis: Basis,
    *,
    lambda_cutoff: int,
    g: float,
    mu: float,
    delta: float,
) -> np.ndarray:
    """H(g,mu,delta) = H_hop + g*V0 + 2*mu*N_even + g*delta*V_delta
    (specification.md Section 4). Coefficient firewall: the electric
    isotropic term carries coefficient g, the even-matter term carries
    coefficient 2*mu, and the alternating electric term carries coefficient
    g*delta -- each applied explicitly, not folded into a single rescaled
    electric aggregate."""
    h_hop = build_h_hop(basis, lambda_cutoff=lambda_cutoff)
    v0 = build_v0(basis)
    n_even = build_n_even(basis)
    v_delta = build_v_delta(basis)
    return h_hop + g * v0 + 2 * mu * n_even + g * delta * v_delta
