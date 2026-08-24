"""Tests for the Toy Model 0B elementary physical-sector operators
(docs/toy-models/toy0b/specification.md Sections 3-4): n_i, E_i, the
directed gauge-invariant hop h_i = c_i^dagger U_i c_{i+1}, and
X_i = h_i + h_i^dagger."""

from __future__ import annotations

import numpy as np
import pytest

from cosmobox_c_model.models.model0b import operators as ops
from cosmobox_c_model.models.model0b.basis_config import build_physical_basis
from cosmobox_c_model.models.model0b.constants import BACKGROUND, N_SITES

LAMBDAS = (1, 2, 3)


def _identity(dimension: int) -> np.ndarray:
    return np.eye(dimension, dtype=complex)


# --- A. Shapes ---------------------------------------------------------


@pytest.mark.parametrize("lambda_cutoff", LAMBDAS)
def test_shapes(lambda_cutoff):
    basis = build_physical_basis(lambda_cutoff)
    d = basis.dimension
    for site in range(N_SITES):
        assert ops.build_number_operator(basis, site).shape == (d, d)
        assert ops.build_electric_operator(basis, site).shape == (d, d)
        assert ops.build_directed_hop_operator(basis, site, lambda_cutoff=lambda_cutoff).shape == (d, d)
        assert ops.build_x_operator(basis, site, lambda_cutoff=lambda_cutoff).shape == (d, d)


# --- B. Number diagonal ---------------------------------------------------


@pytest.mark.parametrize("lambda_cutoff", LAMBDAS)
def test_number_diagonal(lambda_cutoff):
    basis = build_physical_basis(lambda_cutoff)
    for site in range(N_SITES):
        n_op = ops.build_number_operator(basis, site)
        for index, state in enumerate(basis.states):
            assert n_op[index, index] == complex(state[site])
        off_diagonal = n_op - np.diag(np.diag(n_op))
        assert np.count_nonzero(off_diagonal) == 0


# --- C. Number projector -------------------------------------------------


@pytest.mark.parametrize("lambda_cutoff", LAMBDAS)
def test_number_projector_and_hermitian(lambda_cutoff):
    basis = build_physical_basis(lambda_cutoff)
    for site in range(N_SITES):
        n_op = ops.build_number_operator(basis, site)
        assert np.array_equal(n_op @ n_op, n_op)
        assert np.array_equal(n_op, n_op.conj().T)


# --- D. Half-filling operator oracle --------------------------------------


@pytest.mark.parametrize("lambda_cutoff", LAMBDAS)
def test_half_filling_operator_oracle(lambda_cutoff):
    basis = build_physical_basis(lambda_cutoff)
    total_n = sum(ops.build_number_operator(basis, site) for site in range(N_SITES))
    assert np.array_equal(total_n, 3 * _identity(basis.dimension))


# --- E. Electric diagonal ---------------------------------------------------


@pytest.mark.parametrize("lambda_cutoff", LAMBDAS)
def test_electric_diagonal(lambda_cutoff):
    basis = build_physical_basis(lambda_cutoff)
    for link in range(N_SITES):
        e_op = ops.build_electric_operator(basis, link)
        for index, state in enumerate(basis.states):
            assert e_op[index, index] == complex(state[N_SITES + link])
        off_diagonal = e_op - np.diag(np.diag(e_op))
        assert np.count_nonzero(off_diagonal) == 0


# --- F. Operator Gauss oracle -----------------------------------------------


@pytest.mark.parametrize("lambda_cutoff", LAMBDAS)
def test_operator_gauss_oracle(lambda_cutoff):
    basis = build_physical_basis(lambda_cutoff)
    identity = _identity(basis.dimension)
    e_ops = [ops.build_electric_operator(basis, link) for link in range(N_SITES)]
    n_ops = [ops.build_number_operator(basis, site) for site in range(N_SITES)]
    for i in range(N_SITES):
        residual = e_ops[i] - e_ops[(i - 1) % N_SITES] - (n_ops[i] - BACKGROUND[i] * identity)
        assert np.array_equal(residual, np.zeros_like(residual))


# --- Test-side independent directed-hop action oracle ------------------------


def _jw_sign(occupations: tuple[int, ...], site: int) -> int:
    return -1 if sum(occupations[:site]) % 2 else 1


def _expected_hop(
    state: tuple[int, ...], link: int, lambda_cutoff: int
) -> tuple[tuple[int, ...], complex] | None:
    """Independent test-side expectation for h_link = c_link^dagger U_link
    c_{(link+1) mod 6}, evaluated directly on the flattened state tuple
    without calling any production private helper."""
    partner = (link + 1) % N_SITES
    matter = list(state[:N_SITES])
    links = list(state[N_SITES:])

    if matter[partner] == 0:
        return None
    sign_annihilation = _jw_sign(tuple(matter), partner)
    matter[partner] = 0

    if links[link] == lambda_cutoff:
        return None

    if matter[link] == 1:
        return None
    sign_creation = _jw_sign(tuple(matter), link)
    matter[link] = 1

    links[link] += 1
    amplitude = complex(sign_annihilation * sign_creation)
    return tuple(matter) + tuple(links), amplitude


# --- G, I, K. Independent action oracle / physical closure / occupancy ------


@pytest.mark.parametrize("lambda_cutoff", LAMBDAS)
@pytest.mark.parametrize("link", range(N_SITES))
def test_directed_hop_independent_action_oracle(lambda_cutoff, link):
    basis = build_physical_basis(lambda_cutoff)
    hop = ops.build_directed_hop_operator(basis, link, lambda_cutoff=lambda_cutoff)

    for column, state in enumerate(basis.states):
        expected = _expected_hop(state, link, lambda_cutoff)
        matrix_column = hop[:, column]
        nonzero_rows = np.flatnonzero(matrix_column)

        if expected is None:
            assert nonzero_rows.size == 0
            continue

        expected_state, expected_amplitude = expected
        assert expected_state in basis.index_of
        expected_row = basis.index_of_state(expected_state)

        assert nonzero_rows.size == 1
        assert nonzero_rows[0] == expected_row
        assert matrix_column[expected_row] == pytest.approx(expected_amplitude)


# --- H. Periodic bond 5 -> 0 explicitly ---------------------------------------


@pytest.mark.parametrize("lambda_cutoff", LAMBDAS)
def test_periodic_bond_5_to_0(lambda_cutoff):
    basis = build_physical_basis(lambda_cutoff)
    hop = ops.build_directed_hop_operator(basis, 5, lambda_cutoff=lambda_cutoff)

    found_nonzero_column = False
    for column, state in enumerate(basis.states):
        expected = _expected_hop(state, 5, lambda_cutoff)
        matrix_column = hop[:, column]
        if expected is None:
            assert np.count_nonzero(matrix_column) == 0
            continue
        found_nonzero_column = True
        expected_state, expected_amplitude = expected
        expected_row = basis.index_of_state(expected_state)
        assert matrix_column[expected_row] == pytest.approx(expected_amplitude)

    assert found_nonzero_column, "link 5 (periodic bond 5->0) must have at least one nonzero hop column"


# --- J. Truncated top boundary ------------------------------------------------


@pytest.mark.parametrize("lambda_cutoff", LAMBDAS)
@pytest.mark.parametrize("link", range(N_SITES))
def test_truncated_top_boundary(lambda_cutoff, link):
    basis = build_physical_basis(lambda_cutoff)
    hop = ops.build_directed_hop_operator(basis, link, lambda_cutoff=lambda_cutoff)

    saw_boundary_state = False
    for column, state in enumerate(basis.states):
        if state[N_SITES + link] == lambda_cutoff:
            saw_boundary_state = True
            assert np.count_nonzero(hop[:, column]) == 0

    # Boundary states must exist for at least one (link, lambda_cutoff) pair to
    # make the assertion above non-vacuous; this is checked structurally at
    # link=0 (a matter configuration with spread 0 always admits e=lambda_cutoff).
    if link == 0:
        assert saw_boundary_state


# --- L. Single target -----------------------------------------------------


@pytest.mark.parametrize("lambda_cutoff", LAMBDAS)
@pytest.mark.parametrize("link", range(N_SITES))
def test_single_target_and_unit_modulus(lambda_cutoff, link):
    basis = build_physical_basis(lambda_cutoff)
    hop = ops.build_directed_hop_operator(basis, link, lambda_cutoff=lambda_cutoff)
    for column in range(basis.dimension):
        nonzero = np.flatnonzero(hop[:, column])
        assert nonzero.size <= 1
        for row in nonzero:
            assert abs(hop[row, column]) == pytest.approx(1.0)


# --- M. Derived sign fingerprint -----------------------------------------


@pytest.mark.parametrize("lambda_cutoff", LAMBDAS)
def test_fermionic_sign_fingerprint_all_plus_one(lambda_cutoff):
    basis = build_physical_basis(lambda_cutoff)
    for link in range(N_SITES):
        hop = ops.build_directed_hop_operator(basis, link, lambda_cutoff=lambda_cutoff)
        nonzero_entries = hop[np.nonzero(hop)]
        for amplitude in nonzero_entries:
            assert amplitude == pytest.approx(1.0 + 0.0j)


# --- N. X definition --------------------------------------------------------


@pytest.mark.parametrize("lambda_cutoff", LAMBDAS)
@pytest.mark.parametrize("link", range(N_SITES))
def test_x_definition(lambda_cutoff, link):
    basis = build_physical_basis(lambda_cutoff)
    hop = ops.build_directed_hop_operator(basis, link, lambda_cutoff=lambda_cutoff)
    x_op = ops.build_x_operator(basis, link, lambda_cutoff=lambda_cutoff)
    assert np.array_equal(x_op, hop + hop.conj().T)


# --- O. X hermiticity -------------------------------------------------------


@pytest.mark.parametrize("lambda_cutoff", LAMBDAS)
@pytest.mark.parametrize("link", range(N_SITES))
def test_x_hermiticity(lambda_cutoff, link):
    basis = build_physical_basis(lambda_cutoff)
    x_op = ops.build_x_operator(basis, link, lambda_cutoff=lambda_cutoff)
    assert np.array_equal(x_op, x_op.conj().T)


# --- P. No extra normalization -----------------------------------------------


@pytest.mark.parametrize("lambda_cutoff", LAMBDAS)
def test_x_no_extra_normalization(lambda_cutoff):
    basis = build_physical_basis(lambda_cutoff)
    for link in range(N_SITES):
        hop = ops.build_directed_hop_operator(basis, link, lambda_cutoff=lambda_cutoff)
        x_op = ops.build_x_operator(basis, link, lambda_cutoff=lambda_cutoff)
        nonzero_rows, nonzero_cols = np.nonzero(hop)
        for row, col in zip(nonzero_rows, nonzero_cols):
            assert x_op[row, col] == pytest.approx(hop[row, col])
            assert x_op[col, row] == pytest.approx(hop[row, col].conjugate())


# --- Index validation ---------------------------------------------------------


@pytest.mark.parametrize("bad_site", [-1, 6, 100])
def test_number_operator_rejects_out_of_range_site(bad_site):
    basis = build_physical_basis(1)
    with pytest.raises(ValueError):
        ops.build_number_operator(basis, bad_site)


@pytest.mark.parametrize("bad_site", [True, False, 1.0, "0", None])
def test_number_operator_rejects_non_integer_site(bad_site):
    basis = build_physical_basis(1)
    with pytest.raises(TypeError):
        ops.build_number_operator(basis, bad_site)


@pytest.mark.parametrize("bad_link", [-1, 6, 100])
def test_electric_operator_rejects_out_of_range_link(bad_link):
    basis = build_physical_basis(1)
    with pytest.raises(ValueError):
        ops.build_electric_operator(basis, bad_link)


@pytest.mark.parametrize("bad_link", [True, False, 1.0, "0", None])
def test_electric_operator_rejects_non_integer_link(bad_link):
    basis = build_physical_basis(1)
    with pytest.raises(TypeError):
        ops.build_electric_operator(basis, bad_link)


@pytest.mark.parametrize("bad_link", [-1, 6, 100])
def test_hop_operator_rejects_out_of_range_link(bad_link):
    basis = build_physical_basis(1)
    with pytest.raises(ValueError):
        ops.build_directed_hop_operator(basis, bad_link, lambda_cutoff=1)


@pytest.mark.parametrize("bad_link", [True, False, 1.0, "0", None])
def test_hop_operator_rejects_non_integer_link(bad_link):
    basis = build_physical_basis(1)
    with pytest.raises(TypeError):
        ops.build_directed_hop_operator(basis, bad_link, lambda_cutoff=1)


# --- Lambda cutoff validation --------------------------------------------------


def test_hop_operator_rejects_zero_lambda_cutoff():
    basis = build_physical_basis(1)
    with pytest.raises(ValueError):
        ops.build_directed_hop_operator(basis, 0, lambda_cutoff=0)


def test_hop_operator_rejects_negative_lambda_cutoff():
    basis = build_physical_basis(1)
    with pytest.raises(ValueError):
        ops.build_directed_hop_operator(basis, 0, lambda_cutoff=-1)


@pytest.mark.parametrize("bad_lambda", [True, 1.0, "1", None])
def test_hop_operator_rejects_non_integer_lambda_cutoff(bad_lambda):
    basis = build_physical_basis(1)
    with pytest.raises(TypeError):
        ops.build_directed_hop_operator(basis, 0, lambda_cutoff=bad_lambda)


# --- Basis / cutoff consistency ------------------------------------------------


def test_hop_operator_rejects_basis_cutoff_mismatch():
    basis = build_physical_basis(1)
    with pytest.raises(ValueError):
        ops.build_directed_hop_operator(basis, 0, lambda_cutoff=2)


def test_x_operator_rejects_basis_cutoff_mismatch():
    basis = build_physical_basis(2)
    with pytest.raises(ValueError):
        ops.build_x_operator(basis, 0, lambda_cutoff=1)
