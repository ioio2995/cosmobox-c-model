"""C01-C09: Hilbert-Schmidt basis, families F1/F2/F3, kernel projector, and
witness state signatures (docs/toy-models/toy0/implementation-design.md
Sections 15-24)."""

from __future__ import annotations

import numpy as np

from cosmobox_c_model.core.identifiability import analyze_identifiability, build_measurement_matrix
from cosmobox_c_model.models.model0a import constants
from cosmobox_c_model.models.model0a.basis_config import build_total_basis
from cosmobox_c_model.models.model0a.observables import (
    WITNESS_STATES,
    build_families,
    build_hs_basis,
    build_physical_observables,
    build_physical_occupations,
)

SQRT2 = float(np.sqrt(2))


def _setup():
    basis = build_total_basis()
    observables = build_physical_observables(basis)
    occupations = build_physical_occupations(basis, observables["inclusion"])
    hs_basis = build_hs_basis(observables)
    families = build_families(basis, occupations, observables)
    return observables, occupations, hs_basis, families


def _expectation(operator: np.ndarray, state_vector: np.ndarray) -> complex:
    return complex(state_vector.conj() @ operator @ state_vector)


def test_c01_hs_basis_is_hermitian_traceless_and_orthonormal():
    _, _, hs_basis, _ = _setup()
    for element in hs_basis:
        assert abs(np.trace(element)) < constants.EXACT_MATRIX_ATOL
        np.testing.assert_allclose(element, element.conj().T, atol=constants.HERMITICITY_ATOL)
    for i, bi in enumerate(hs_basis):
        for j, bj in enumerate(hs_basis):
            expected = 1.0 if i == j else 0.0
            assert abs(np.trace(bi @ bj).real - expected) < constants.EXACT_MATRIX_ATOL


def test_c02_measurement_matrix_imaginary_part_is_controlled():
    _, _, hs_basis, families = _setup()
    # Must not raise: all families here are built from Hermitian observables.
    build_measurement_matrix(families["F3"], hs_basis, imag_atol=constants.MEASUREMENT_IMAG_ATOL)


def test_c03_family_f1():
    _, _, hs_basis, families = _setup()
    matrix = build_measurement_matrix(families["F1"], hs_basis, imag_atol=constants.MEASUREMENT_IMAG_ATOL)
    result = analyze_identifiability(matrix, rank_tolerance=constants.RANK_EPSILON)
    assert result.numerical_rank == 2
    expected_spectrum = np.array([1, 1, 0, 0, 0, 0, 0, 0], dtype=float)
    np.testing.assert_allclose(
        np.sort(result.singular_values_domain)[::-1], expected_spectrum, atol=constants.SINGULAR_VALUE_ATOL
    )


def test_c04_family_f2():
    _, _, hs_basis, families = _setup()
    matrix = build_measurement_matrix(families["F2"], hs_basis, imag_atol=constants.MEASUREMENT_IMAG_ATOL)
    result = analyze_identifiability(matrix, rank_tolerance=constants.RANK_EPSILON)
    assert result.numerical_rank == 6
    expected_spectrum = np.array([1, 1, 1 / SQRT2, 1 / SQRT2, 1 / SQRT2, 1 / SQRT2, 0, 0])
    np.testing.assert_allclose(
        np.sort(result.singular_values_domain)[::-1], expected_spectrum, atol=constants.SINGULAR_VALUE_ATOL
    )


def test_c05_kernel_projector_f2_matches_the_analytic_reference():
    _, _, hs_basis, families = _setup()
    matrix = build_measurement_matrix(families["F2"], hs_basis, imag_atol=constants.MEASUREMENT_IMAG_ATOL)
    result = analyze_identifiability(matrix, rank_tolerance=constants.RANK_EPSILON)
    reference = np.diag([0, 0, 0, 0, 0, 0, 1, 1]).astype(float)
    frobenius_defect = np.linalg.norm(result.kernel_projector.real - reference, ord="fro")
    assert frobenius_defect < constants.KERNEL_PROJECTOR_FROBENIUS_TOL


def test_c06_family_f3():
    _, _, hs_basis, families = _setup()
    matrix = build_measurement_matrix(families["F3"], hs_basis, imag_atol=constants.MEASUREMENT_IMAG_ATOL)
    result = analyze_identifiability(matrix, rank_tolerance=constants.RANK_EPSILON)
    assert result.numerical_rank == 8
    expected_spectrum = np.array([1, 1] + [1 / SQRT2] * 6)
    np.testing.assert_allclose(
        np.sort(result.singular_values_domain)[::-1], expected_spectrum, atol=constants.SINGULAR_VALUE_ATOL
    )
    assert result.kernel_basis.shape[0] == 0


def test_c07_condition_numbers_of_the_physical_families():
    _, _, hs_basis, families = _setup()
    expected = {"F1": 1.0, "F2": SQRT2, "F3": SQRT2}
    for name, expected_value in expected.items():
        matrix = build_measurement_matrix(families[name], hs_basis, imag_atol=constants.MEASUREMENT_IMAG_ATOL)
        result = analyze_identifiability(matrix, rank_tolerance=constants.RANK_EPSILON)
        assert result.condition_number_resolved is not None
        assert abs(result.condition_number_resolved - expected_value) < 1e-10


def test_c08_witness_states_are_indistinguishable_under_f2():
    observables, occupations, _, _ = _setup()
    operators = (
        occupations["n_0"], occupations["n_1"], occupations["n_2"],
        observables["X_01"], observables["Y_01"],
        observables["X_12"], observables["Y_12"],
    )
    expected = (0.5, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0)
    for psi in WITNESS_STATES.values():
        for operator, expected_value in zip(operators, expected):
            value = _expectation(operator, psi)
            assert abs(value.real - expected_value) < constants.EXPECTATION_ATOL
            assert abs(value.imag) < constants.EXPECTATION_ATOL


def test_c09_witness_states_are_distinguished_under_f3():
    observables, _, _, _ = _setup()
    expected_x02_y02 = {
        "psi_plus": (0.5, 0.0),
        "psi_minus": (-0.5, 0.0),
        "psi_plus_i": (0.0, 0.5),
        "psi_minus_i": (0.0, -0.5),
    }
    for name, psi in WITNESS_STATES.items():
        x02 = _expectation(observables["X_02"], psi)
        y02 = _expectation(observables["Y_02"], psi)
        expected_x, expected_y = expected_x02_y02[name]
        assert abs(x02.real - expected_x) < constants.EXPECTATION_ATOL
        assert abs(y02.real - expected_y) < constants.EXPECTATION_ATOL
