"""Tests for the Toy Model 0B static aggregates and Hamiltonian assembly
(docs/toy-models/toy0b/specification.md Section 4): N_even, V0, V_delta,
H_hop and H(g,mu,delta)."""

from __future__ import annotations

import numpy as np
import pytest

from cosmobox_c_model.models.model0b import hamiltonian as ham
from cosmobox_c_model.models.model0b import operators as ops
from cosmobox_c_model.models.model0b.basis_config import build_physical_basis
from cosmobox_c_model.models.model0b.constants import N_SITES

LAMBDAS = (1, 2, 3)


# --- A-D. N_even -----------------------------------------------------------


@pytest.mark.parametrize("lambda_cutoff", LAMBDAS)
def test_n_even_shape(lambda_cutoff):
    basis = build_physical_basis(lambda_cutoff)
    n_even = ham.build_n_even(basis)
    assert n_even.shape == (basis.dimension, basis.dimension)


@pytest.mark.parametrize("lambda_cutoff", LAMBDAS)
def test_n_even_statewise_diagonal_oracle(lambda_cutoff):
    basis = build_physical_basis(lambda_cutoff)
    n_even = ham.build_n_even(basis)
    for index, state in enumerate(basis.states):
        assert n_even[index, index] == complex(state[0] + state[2] + state[4])
    off_diagonal = n_even - np.diag(np.diag(n_even))
    assert np.count_nonzero(off_diagonal) == 0


@pytest.mark.parametrize("lambda_cutoff", LAMBDAS)
def test_n_even_composition_oracle(lambda_cutoff):
    basis = build_physical_basis(lambda_cutoff)
    n_even = ham.build_n_even(basis)
    expected = (
        ops.build_number_operator(basis, 0)
        + ops.build_number_operator(basis, 2)
        + ops.build_number_operator(basis, 4)
    )
    assert np.array_equal(n_even, expected)


@pytest.mark.parametrize("lambda_cutoff", LAMBDAS)
def test_n_even_hermitian(lambda_cutoff):
    basis = build_physical_basis(lambda_cutoff)
    n_even = ham.build_n_even(basis)
    assert np.array_equal(n_even, n_even.conj().T)


# --- E-G. V0 -----------------------------------------------------------------


@pytest.mark.parametrize("lambda_cutoff", LAMBDAS)
def test_v0_statewise_diagonal_oracle(lambda_cutoff):
    basis = build_physical_basis(lambda_cutoff)
    v0 = ham.build_v0(basis)
    for index, state in enumerate(basis.states):
        expected = sum(state[N_SITES + i] ** 2 for i in range(N_SITES))
        assert v0[index, index] == complex(expected)
    off_diagonal = v0 - np.diag(np.diag(v0))
    assert np.count_nonzero(off_diagonal) == 0


@pytest.mark.parametrize("lambda_cutoff", LAMBDAS)
def test_v0_composition_oracle(lambda_cutoff):
    basis = build_physical_basis(lambda_cutoff)
    v0 = ham.build_v0(basis)
    expected = sum(
        ops.build_electric_operator(basis, link) @ ops.build_electric_operator(basis, link)
        for link in range(N_SITES)
    )
    assert np.array_equal(v0, expected)


@pytest.mark.parametrize("lambda_cutoff", LAMBDAS)
def test_v0_hermitian_and_nonnegative(lambda_cutoff):
    basis = build_physical_basis(lambda_cutoff)
    v0 = ham.build_v0(basis)
    assert np.array_equal(v0, v0.conj().T)
    assert np.all(np.diag(v0).real >= 0)
    assert np.all(np.diag(v0).imag == 0)


# --- H-J. V_delta --------------------------------------------------------------


@pytest.mark.parametrize("lambda_cutoff", LAMBDAS)
def test_v_delta_statewise_diagonal_oracle(lambda_cutoff):
    basis = build_physical_basis(lambda_cutoff)
    v_delta = ham.build_v_delta(basis)
    for index, state in enumerate(basis.states):
        expected = sum((-1) ** i * state[N_SITES + i] ** 2 for i in range(N_SITES))
        assert v_delta[index, index] == complex(expected)
    off_diagonal = v_delta - np.diag(np.diag(v_delta))
    assert np.count_nonzero(off_diagonal) == 0


@pytest.mark.parametrize("lambda_cutoff", LAMBDAS)
def test_v_delta_composition_oracle(lambda_cutoff):
    basis = build_physical_basis(lambda_cutoff)
    v_delta = ham.build_v_delta(basis)
    expected = sum(
        (-1) ** link
        * (ops.build_electric_operator(basis, link) @ ops.build_electric_operator(basis, link))
        for link in range(N_SITES)
    )
    assert np.array_equal(v_delta, expected)


def test_v_delta_naming_firewall():
    assert not hasattr(ham, "build_v_stag")
    assert not hasattr(ham, "V_stag")
    assert hasattr(ham, "build_v_delta")
    # Negative assertion only: this string must not otherwise appear as a
    # production identifier in this module.
    forbidden = "V_stag"
    assert forbidden not in dir(ham)


# --- K-M. H_hop ----------------------------------------------------------------


@pytest.mark.parametrize("lambda_cutoff", LAMBDAS)
def test_h_hop_definition(lambda_cutoff):
    basis = build_physical_basis(lambda_cutoff)
    h_hop = ham.build_h_hop(basis, lambda_cutoff=lambda_cutoff)
    expected = -sum(
        ops.build_x_operator(basis, link, lambda_cutoff=lambda_cutoff) for link in range(N_SITES)
    )
    assert np.array_equal(h_hop, expected)


@pytest.mark.parametrize("lambda_cutoff", LAMBDAS)
def test_h_hop_hermitian(lambda_cutoff):
    basis = build_physical_basis(lambda_cutoff)
    h_hop = ham.build_h_hop(basis, lambda_cutoff=lambda_cutoff)
    assert np.array_equal(h_hop, h_hop.conj().T)


@pytest.mark.parametrize("lambda_cutoff", LAMBDAS)
def test_h_hop_diagonal_matches_minus_sum_x(lambda_cutoff):
    basis = build_physical_basis(lambda_cutoff)
    h_hop = ham.build_h_hop(basis, lambda_cutoff=lambda_cutoff)
    minus_sum_x = -sum(
        ops.build_x_operator(basis, link, lambda_cutoff=lambda_cutoff) for link in range(N_SITES)
    )
    assert np.array_equal(np.diag(h_hop), np.diag(minus_sum_x))


# --- N-S. Full Hamiltonian -------------------------------------------------------


@pytest.mark.parametrize("lambda_cutoff", LAMBDAS)
def test_reference_decomposition_g1_mu0_delta0(lambda_cutoff):
    basis = build_physical_basis(lambda_cutoff)
    h_hop = ham.build_h_hop(basis, lambda_cutoff=lambda_cutoff)
    v0 = ham.build_v0(basis)
    h_full = ham.build_hamiltonian(basis, lambda_cutoff=lambda_cutoff, g=1, mu=0, delta=0)
    assert np.array_equal(h_full, h_hop + v0)


@pytest.mark.parametrize("lambda_cutoff", LAMBDAS)
@pytest.mark.parametrize("delta_value", [0.0, 0.5])
def test_pure_hopping_assembly_identity_g0_mu0(lambda_cutoff, delta_value):
    basis = build_physical_basis(lambda_cutoff)
    h_hop = ham.build_h_hop(basis, lambda_cutoff=lambda_cutoff)
    h_full = ham.build_hamiltonian(
        basis, lambda_cutoff=lambda_cutoff, g=0, mu=0, delta=delta_value
    )
    assert np.array_equal(h_full, h_hop)


@pytest.mark.parametrize("lambda_cutoff", LAMBDAS)
def test_mu_coefficient_identity(lambda_cutoff):
    basis = build_physical_basis(lambda_cutoff)
    h_hop = ham.build_h_hop(basis, lambda_cutoff=lambda_cutoff)
    n_even = ham.build_n_even(basis)
    h_full = ham.build_hamiltonian(basis, lambda_cutoff=lambda_cutoff, g=0, mu=0.5, delta=0)
    assert np.array_equal(h_full, h_hop + n_even)


@pytest.mark.parametrize("lambda_cutoff", LAMBDAS)
def test_delta_coefficient_identity(lambda_cutoff):
    basis = build_physical_basis(lambda_cutoff)
    h_hop = ham.build_h_hop(basis, lambda_cutoff=lambda_cutoff)
    v0 = ham.build_v0(basis)
    v_delta = ham.build_v_delta(basis)
    h_full = ham.build_hamiltonian(basis, lambda_cutoff=lambda_cutoff, g=0.5, mu=0, delta=0.5)
    expected = h_hop + 0.5 * v0 + 0.25 * v_delta
    assert np.array_equal(h_full, expected)


@pytest.mark.parametrize("lambda_cutoff", LAMBDAS)
def test_general_binary_exact_composition(lambda_cutoff):
    basis = build_physical_basis(lambda_cutoff)
    g, mu, delta = 2, -0.5, 0.25

    h_hop = ham.build_h_hop(basis, lambda_cutoff=lambda_cutoff)
    v0 = ham.build_v0(basis)
    n_even = ham.build_n_even(basis)
    v_delta = ham.build_v_delta(basis)

    expected = h_hop + g * v0 + 2 * mu * n_even + g * delta * v_delta
    h_full = ham.build_hamiltonian(basis, lambda_cutoff=lambda_cutoff, g=g, mu=mu, delta=delta)
    assert np.array_equal(h_full, expected)


@pytest.mark.parametrize("lambda_cutoff", LAMBDAS)
@pytest.mark.parametrize(
    "g,mu,delta",
    [
        (1, 0, 0),
        (0, 0, 0.5),
        (0, 0.5, 0),
        (0.5, 0, 0.5),
        (2, -0.5, 0.25),
    ],
)
def test_full_hamiltonian_hermitian(lambda_cutoff, g, mu, delta):
    basis = build_physical_basis(lambda_cutoff)
    h_full = ham.build_hamiltonian(basis, lambda_cutoff=lambda_cutoff, g=g, mu=mu, delta=delta)
    assert np.array_equal(h_full, h_full.conj().T)
