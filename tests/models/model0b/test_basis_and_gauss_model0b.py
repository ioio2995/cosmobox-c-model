"""Tests for the Toy Model 0B physical basis and periodic Gauss law
(docs/toy-models/toy0b/specification.md Section 3): six-site oriented cycle,
fixed background, half filling, exact dimensions 38/78/118 for
Lambda=1,2,3."""

from __future__ import annotations

from itertools import product

import pytest

from cosmobox_c_model.models.model0b import constants
from cosmobox_c_model.models.model0b.basis_config import build_physical_basis

LITERAL_BACKGROUND = (0, 1, 0, 1, 0, 1)

EXACT_DIMENSIONS = {1: 38, 2: 78, 3: 118}


# --- A. Model constants -----------------------------------------------


def test_n_sites():
    assert constants.N_SITES == 6


def test_background():
    assert constants.BACKGROUND == LITERAL_BACKGROUND


def test_matter_particle_number():
    assert constants.MATTER_PARTICLE_NUMBER == 3


# --- B. Exact matter configuration count -------------------------------


@pytest.mark.parametrize("lambda_cutoff", [1, 2, 3])
def test_exact_matter_configuration_count(lambda_cutoff):
    basis = build_physical_basis(lambda_cutoff)
    matter_parts = {state[:6] for state in basis.states}
    assert len(matter_parts) == 20
    for n in matter_parts:
        assert sum(n) == 3


# --- C. Exact dimensions ------------------------------------------------


@pytest.mark.parametrize("lambda_cutoff,expected_dimension", sorted(EXACT_DIMENSIONS.items()))
def test_exact_dimension(lambda_cutoff, expected_dimension):
    basis = build_physical_basis(lambda_cutoff)
    assert basis.dimension == expected_dimension


# --- D. Half filling ------------------------------------------------------


@pytest.mark.parametrize("lambda_cutoff", [1, 2, 3])
def test_every_state_satisfies_half_filling(lambda_cutoff):
    basis = build_physical_basis(lambda_cutoff)
    for state in basis.states:
        n = state[:6]
        assert sum(n) == 3


# --- E. Periodic Gauss law -------------------------------------------------


@pytest.mark.parametrize("lambda_cutoff", [1, 2, 3])
def test_every_state_satisfies_periodic_gauss(lambda_cutoff):
    basis = build_physical_basis(lambda_cutoff)
    for state in basis.states:
        n = state[:6]
        e_links = state[6:]
        for i in range(6):
            assert e_links[i] - e_links[(i - 1) % 6] == n[i] - LITERAL_BACKGROUND[i]


# --- F. Electric link cutoff -----------------------------------------------


@pytest.mark.parametrize("lambda_cutoff", [1, 2, 3])
def test_electric_links_inside_cutoff(lambda_cutoff):
    basis = build_physical_basis(lambda_cutoff)
    for state in basis.states:
        for e in state[6:]:
            assert -lambda_cutoff <= e <= lambda_cutoff


# --- G. No duplicate physical states ---------------------------------------


@pytest.mark.parametrize("lambda_cutoff", [1, 2, 3])
def test_no_duplicate_states(lambda_cutoff):
    basis = build_physical_basis(lambda_cutoff)
    assert len(set(basis.states)) == len(basis.states)


# --- H. Deterministic order -------------------------------------------------


@pytest.mark.parametrize("lambda_cutoff", [1, 2, 3])
def test_deterministic_order_across_independent_calls(lambda_cutoff):
    basis_a = build_physical_basis(lambda_cutoff)
    basis_b = build_physical_basis(lambda_cutoff)
    assert basis_a.states == basis_b.states
    assert basis_a.index_of == basis_b.index_of


def test_ordering_contract_matter_lexicographic_then_e_ascending():
    basis = build_physical_basis(1)
    matter_sequence = [state[:6] for state in basis.states]
    distinct_matter_in_order = list(dict.fromkeys(matter_sequence))
    assert distinct_matter_in_order == sorted(distinct_matter_in_order)

    for matter in distinct_matter_in_order:
        e5_values = [state[11] for state in basis.states if state[:6] == matter]
        assert e5_values == sorted(e5_values)


# --- I. Basis index roundtrip ------------------------------------------------


@pytest.mark.parametrize("lambda_cutoff", [1, 2, 3])
def test_basis_index_roundtrip(lambda_cutoff):
    basis = build_physical_basis(lambda_cutoff)
    for index, state in enumerate(basis.states):
        assert basis.state_at(index) == state
        assert basis.index_of_state(state) == index


# --- J. Exact spread distribution oracle (test-side, independent) -----------


def _test_side_matter_configurations():
    return [
        n for n in product((0, 1), repeat=6) if sum(n) == 3
    ]


def _test_side_spread(n):
    charges = [n[i] - LITERAL_BACKGROUND[i] for i in range(6)]
    offsets = []
    running = 0
    for q in charges:
        running += q
        offsets.append(running)
    return max(offsets) - min(offsets)


def test_exact_spread_distribution_oracle():
    matter_configurations = _test_side_matter_configurations()
    assert len(matter_configurations) == 20

    spread_counts = {0: 0, 1: 0, 2: 0}
    for n in matter_configurations:
        spread = _test_side_spread(n)
        spread_counts[spread] = spread_counts.get(spread, 0) + 1

    assert spread_counts == {0: 1, 1: 16, 2: 3}


# --- K. Independent brute-force oracle at Lambda=1 ---------------------------


def test_lambda1_independent_brute_force_oracle():
    background = (0, 1, 0, 1, 0, 1)
    matter_configurations = [
        n for n in product((0, 1), repeat=6) if sum(n) == 3
    ]
    assert len(matter_configurations) == 20

    oracle_states = set()
    for n in matter_configurations:
        for links in product((-1, 0, 1), repeat=6):
            if all(
                links[i] - links[(i - 1) % 6] == n[i] - background[i]
                for i in range(6)
            ):
                oracle_states.add(n + links)

    assert len(oracle_states) == 38
    assert oracle_states == set(build_physical_basis(1).states)


# --- L. Invalid Lambda --------------------------------------------------------


def test_lambda_zero_rejected():
    with pytest.raises(ValueError):
        build_physical_basis(0)


def test_negative_lambda_rejected():
    with pytest.raises(ValueError):
        build_physical_basis(-1)


def test_non_integral_float_lambda_rejected():
    with pytest.raises(TypeError):
        build_physical_basis(1.5)


def test_integral_float_lambda_rejected():
    with pytest.raises(TypeError):
        build_physical_basis(2.0)
