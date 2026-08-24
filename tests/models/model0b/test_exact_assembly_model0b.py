"""Tests for the Toy Model 0B exact-rational parameters and direct
multi-precision Hamiltonian reassembly (docs/toy-models/toy0b/specification.md
Section 4, docs/toy-models/toy0b/temporal-event-solver.md Section 20).

No high-precision eigensystem, clustering, or precision-stability status is
exercised here: this file only covers exact discrete-component extraction and
direct H^(p) assembly."""

from __future__ import annotations

from fractions import Fraction
from importlib.metadata import version as installed_version

import mpmath as mp
import numpy as np
import pytest

from cosmobox_c_model.models.model0b import exact_assembly as ea
from cosmobox_c_model.models.model0b.basis_config import build_physical_basis
from cosmobox_c_model.models.model0b.hamiltonian import (
    build_h_hop,
    build_hamiltonian,
    build_n_even,
    build_v0,
    build_v_delta,
)

LAMBDAS = (1, 2, 3)


def _int_matrix_to_complex128(int_matrix) -> np.ndarray:
    return np.array([[complex(value) for value in row] for row in int_matrix], dtype=complex)


def _mp_matrix_to_complex128(mp_matrix: "mp.matrix") -> np.ndarray:
    d = mp_matrix.rows
    out = np.zeros((d, d), dtype=complex)
    for i in range(d):
        for j in range(d):
            out[i, j] = complex(mp_matrix[i, j])
    return out


# --- Frozen precision constants ------------------------------------------------


def test_precision_bits_constants():
    assert ea.P0_BITS == 53
    assert ea.P1_BITS == 106
    assert ea.P2_BITS == 212
    assert ea.ALLOWED_PRECISION_BITS == (53, 106, 212)


# --- 15. Exact component cross-check --------------------------------------------


@pytest.mark.parametrize("lambda_cutoff", LAMBDAS)
def test_exact_component_crosscheck(lambda_cutoff):
    basis = build_physical_basis(lambda_cutoff)
    components = ea.build_exact_discrete_components(basis, lambda_cutoff=lambda_cutoff)

    assert np.array_equal(
        _int_matrix_to_complex128(components.h_hop),
        build_h_hop(basis, lambda_cutoff=lambda_cutoff),
    )
    assert np.array_equal(_int_matrix_to_complex128(components.v0), build_v0(basis))
    assert np.array_equal(_int_matrix_to_complex128(components.n_even), build_n_even(basis))
    assert np.array_equal(_int_matrix_to_complex128(components.v_delta), build_v_delta(basis))
    assert components.dimension == basis.dimension
    assert components.lambda_cutoff == lambda_cutoff


# --- 16. Reference H cross-check (g=1, mu=0, delta=0) ---------------------------


@pytest.mark.parametrize("lambda_cutoff", LAMBDAS)
@pytest.mark.parametrize("precision_bits", [106, 212])
def test_reference_hamiltonian_crosscheck(lambda_cutoff, precision_bits):
    basis = build_physical_basis(lambda_cutoff)
    components = ea.build_exact_discrete_components(basis, lambda_cutoff=lambda_cutoff)

    H_mp = ea.assemble_hamiltonian_mp(
        components,
        g=Fraction(1, 1),
        mu=Fraction(0, 1),
        delta=Fraction(0, 1),
        precision_bits=precision_bits,
    )
    H_p0 = build_hamiltonian(basis, lambda_cutoff=lambda_cutoff, g=1, mu=0, delta=0)

    assert np.array_equal(_mp_matrix_to_complex128(H_mp), H_p0)


# --- 17. Non-binary rational parameter oracles ----------------------------------


def _independent_fraction_entry(components, g, mu, delta, i, j) -> Fraction:
    return (
        components.h_hop[i][j]
        + g * components.v0[i][j]
        + 2 * mu * components.n_even[i][j]
        + g * delta * components.v_delta[i][j]
    )


NONBINARY_RATIONAL_POINTS = [
    (Fraction(1, 10), Fraction(-3, 4), Fraction(2, 5)),
    (Fraction(1, 2), Fraction(1, 2), Fraction(3, 5)),
]


@pytest.mark.parametrize("g,mu,delta", NONBINARY_RATIONAL_POINTS)
@pytest.mark.parametrize("precision_bits", [106, 212])
def test_nonbinary_rational_parameter_oracle(g, mu, delta, precision_bits):
    basis = build_physical_basis(1)
    components = ea.build_exact_discrete_components(basis, lambda_cutoff=1)

    H_mp = ea.assemble_hamiltonian_mp(
        components, g=g, mu=mu, delta=delta, precision_bits=precision_bits
    )

    # Pure floating-point non-associativity bound: production accumulates four
    # rounded mpf terms per entry, while this oracle rounds a single
    # pre-summed exact Fraction once. Both routes are mathematically
    # identical, but the rounding *path* differs, so bit-identical equality
    # is not guaranteed. The bound below is derived purely from the target
    # precision's own unit roundoff (2**(1-bits)), not from any scientific
    # tolerance: it is ~10^18 times tighter than the frozen 1e-12 backward
    # threshold at bits=106, and stays representation-only in scope.
    bound = mp.mpf(2) ** (8 - precision_bits)

    with mp.workprec(precision_bits):
        for i in range(components.dimension):
            for j in range(components.dimension):
                expected_fraction = _independent_fraction_entry(components, g, mu, delta, i, j)
                expected_mp = mp.mpf(expected_fraction.numerator) / mp.mpf(
                    expected_fraction.denominator
                )
                assert abs(H_mp[i, j] - expected_mp) <= bound


# --- 18. P1 vs P2 assembly consistency -------------------------------------------


@pytest.mark.parametrize("g,mu,delta", NONBINARY_RATIONAL_POINTS)
def test_p1_p2_assembly_consistency(g, mu, delta):
    basis = build_physical_basis(1)
    components = ea.build_exact_discrete_components(basis, lambda_cutoff=1)

    H_p1 = ea.assemble_hamiltonian_mp(components, g=g, mu=mu, delta=delta, precision_bits=106)
    H_p2 = ea.assemble_hamiltonian_mp(components, g=g, mu=mu, delta=delta, precision_bits=212)

    # Same non-scientific, precision-derived engineering bound as above,
    # evaluated at the coarser (P1) precision.
    bound = mp.mpf(2) ** (8 - 106)

    with mp.workprec(212):
        for i in range(components.dimension):
            for j in range(components.dimension):
                assert abs(mp.mpc(H_p1[i, j]) - H_p2[i, j]) <= bound


# --- 19. Input validation --------------------------------------------------------


def test_require_exact_rational_accepts_fraction_and_int():
    assert ea.require_exact_rational(Fraction(1, 2), name="x") == Fraction(1, 2)
    assert ea.require_exact_rational(3, name="x") == Fraction(3, 1)


@pytest.mark.parametrize(
    "bad_value",
    [0.1, np.float64(0.5), True, False, "1/2", None],
)
def test_require_exact_rational_rejects_non_exact_types(bad_value):
    with pytest.raises(TypeError):
        ea.require_exact_rational(bad_value, name="x")


def test_assemble_hamiltonian_rejects_float_g():
    basis = build_physical_basis(1)
    components = ea.build_exact_discrete_components(basis, lambda_cutoff=1)
    with pytest.raises(TypeError):
        ea.assemble_hamiltonian_mp(
            components, g=0.1, mu=Fraction(0), delta=Fraction(0), precision_bits=106
        )


def test_assemble_hamiltonian_rejects_numpy_float_mu():
    basis = build_physical_basis(1)
    components = ea.build_exact_discrete_components(basis, lambda_cutoff=1)
    with pytest.raises(TypeError):
        ea.assemble_hamiltonian_mp(
            components,
            g=Fraction(1),
            mu=np.float64(0.5),
            delta=Fraction(0),
            precision_bits=106,
        )


def test_assemble_hamiltonian_rejects_bool_delta():
    basis = build_physical_basis(1)
    components = ea.build_exact_discrete_components(basis, lambda_cutoff=1)
    with pytest.raises(TypeError):
        ea.assemble_hamiltonian_mp(
            components, g=Fraction(1), mu=Fraction(0), delta=True, precision_bits=106
        )


@pytest.mark.parametrize("bad_precision", [52, 107, 213])
def test_assemble_hamiltonian_rejects_unauthorized_precision(bad_precision):
    basis = build_physical_basis(1)
    components = ea.build_exact_discrete_components(basis, lambda_cutoff=1)
    with pytest.raises(ValueError):
        ea.assemble_hamiltonian_mp(
            components,
            g=Fraction(1),
            mu=Fraction(0),
            delta=Fraction(0),
            precision_bits=bad_precision,
        )


def test_assemble_hamiltonian_rejects_bool_precision():
    basis = build_physical_basis(1)
    components = ea.build_exact_discrete_components(basis, lambda_cutoff=1)
    with pytest.raises(TypeError):
        ea.assemble_hamiltonian_mp(
            components, g=Fraction(1), mu=Fraction(0), delta=Fraction(0), precision_bits=True
        )


# --- Precision context restoration ------------------------------------------------


def test_precision_context_restored_after_successful_call():
    basis = build_physical_basis(1)
    components = ea.build_exact_discrete_components(basis, lambda_cutoff=1)
    before = mp.mp.prec
    ea.assemble_hamiltonian_mp(
        components, g=Fraction(1), mu=Fraction(0), delta=Fraction(0), precision_bits=212
    )
    assert mp.mp.prec == before


def test_precision_context_unaffected_by_rejected_call():
    basis = build_physical_basis(1)
    components = ea.build_exact_discrete_components(basis, lambda_cutoff=1)
    before = mp.mp.prec
    with pytest.raises(ValueError):
        ea.assemble_hamiltonian_mp(
            components, g=Fraction(1), mu=Fraction(0), delta=Fraction(0), precision_bits=999
        )
    assert mp.mp.prec == before


def test_precision_context_restored_when_called_from_nested_workprec():
    basis = build_physical_basis(1)
    components = ea.build_exact_discrete_components(basis, lambda_cutoff=1)
    with mp.workprec(53):
        inner_before = mp.mp.prec
        ea.assemble_hamiltonian_mp(
            components, g=Fraction(1), mu=Fraction(0), delta=Fraction(0), precision_bits=212
        )
        assert mp.mp.prec == inner_before


# --- Fraction(float) firewall (documentation-level regression) -------------------


def test_fraction_from_float_pitfall_is_not_used_internally():
    # Fraction(0.1) silently yields the binary64 approximation of 0.1, not
    # the exact value 1/10: this module's public boundary must never
    # construct a Fraction this way internally (require_exact_rational
    # rejects float outright, see test_require_exact_rational_rejects_*).
    assert Fraction(0.1) != Fraction(1, 10)
    assert Fraction("0.1") == Fraction(1, 10)


# --- 20. Dependency version ---------------------------------------------------


def _parse_simple_version(version_string: str) -> tuple[int, ...]:
    parts = []
    for component in version_string.split("."):
        digits = ""
        for character in component:
            if character.isdigit():
                digits += character
            else:
                break
        parts.append(int(digits) if digits else 0)
    return tuple(parts)


def test_mpmath_version_within_authorized_range():
    installed = _parse_simple_version(installed_version("mpmath"))
    assert installed >= (1, 4, 1)
    assert installed < (1, 5)
