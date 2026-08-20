"""Model-free unit tests for cosmobox_c_model.core.fermions, exercised on
occupation-number tuples of varying length -- never limited to three modes."""

from __future__ import annotations

from cosmobox_c_model.core.fermions import apply_annihilation, apply_creation, jordan_wigner_sign


def test_annihilation_on_empty_mode_is_none():
    assert apply_annihilation((0, 1, 1), 0) is None


def test_creation_on_occupied_mode_is_none():
    assert apply_creation((1, 0, 1), 0) is None


def test_annihilation_returns_expected_state_and_sign():
    state = (1, 1, 0)
    result = apply_annihilation(state, 1)
    assert result is not None
    new_state, amplitude = result
    assert new_state == (1, 0, 0)
    assert amplitude == jordan_wigner_sign(state, 1)


def test_creation_returns_expected_state_and_sign():
    state = (1, 0, 0)
    result = apply_creation(state, 2)
    assert result is not None
    new_state, amplitude = result
    assert new_state == (1, 0, 1)
    assert amplitude == jordan_wigner_sign(state, 2)


def test_jordan_wigner_sign_is_generic_for_an_arbitrary_number_of_modes():
    # A 5-mode system: the API is not limited to three sites.
    assert jordan_wigner_sign((1, 1, 0, 0, 1), 3) == 1   # sum(1,1,0) = 2 -> even -> +1
    assert jordan_wigner_sign((1, 1, 1, 0, 1), 3) == -1  # sum(1,1,1) = 3 -> odd -> -1
    assert jordan_wigner_sign((0, 0, 0, 0, 0), 4) == 1   # no modes before site 4


def test_number_operator_action_is_sign_free():
    # c_i^dagger c_i on an occupied mode must return amplitude +1: the two
    # Jordan-Wigner signs must cancel exactly.
    state = (1, 1, 1, 1)
    annihilated = apply_annihilation(state, 2)
    assert annihilated is not None
    intermediate_state, amplitude_1 = annihilated
    created = apply_creation(intermediate_state, 2)
    assert created is not None
    final_state, amplitude_2 = created
    assert final_state == state
    assert amplitude_1 * amplitude_2 == 1


def test_creation_then_annihilation_at_a_higher_site_carries_a_nontrivial_sign():
    # Acting at site 3 with one occupied mode before it (site 1) must pick up -1.
    state = (0, 1, 0, 0)
    result = apply_creation(state, 3)
    assert result is not None
    _, amplitude = result
    assert amplitude == -1
