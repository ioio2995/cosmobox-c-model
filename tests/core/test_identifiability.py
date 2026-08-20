"""Model-free unit tests for cosmobox_c_model.core.identifiability, using
synthetic measurement matrices independent of any model's F1/F2/F3."""

from __future__ import annotations

import numpy as np
import pytest

from cosmobox_c_model.core.identifiability import analyze_identifiability, build_measurement_matrix


def test_build_measurement_matrix_computes_hs_traces():
    basis = (np.eye(2, dtype=complex), np.array([[0, 1], [1, 0]], dtype=complex))
    observables = (np.array([[1, 0], [0, -1]], dtype=complex),)
    matrix = build_measurement_matrix(observables, basis, imag_atol=1e-9)
    np.testing.assert_allclose(matrix, [[0, 0]])


def test_build_measurement_matrix_rejects_large_imaginary_residual():
    basis = (np.eye(2, dtype=complex),)
    non_hermitian_observable = (np.array([[1j, 0], [0, 0]], dtype=complex),)
    with pytest.raises(ValueError):
        build_measurement_matrix(non_hermitian_observable, basis, imag_atol=1e-9)


def test_analyze_identifiability_full_rank_synthetic_matrix():
    matrix = np.eye(3, 5)
    result = analyze_identifiability(matrix, rank_tolerance=1e-9)
    assert result.singular_values_domain.shape == (5,)
    assert result.numerical_rank == 3
    assert result.kernel_basis.shape == (2, 5)
    np.testing.assert_allclose(result.kernel_projector, result.kernel_projector.conj().T)


def test_analyze_identifiability_completes_the_spectrum_with_trailing_zeros():
    matrix = np.array([[1.0, 0.0, 0.0]])
    result = analyze_identifiability(matrix, rank_tolerance=1e-9)
    np.testing.assert_allclose(result.singular_values_domain, [1.0, 0.0, 0.0])


def test_analyze_identifiability_uses_direct_svd_not_a_gram_matrix():
    # A matrix whose small singular value would be destroyed by forming
    # matrix.T @ matrix in float64 (a Gram matrix squares the condition number).
    tiny = 1e-9
    matrix = np.array([[1.0, 0.0], [1.0, tiny]]) / np.sqrt(2)
    result = analyze_identifiability(matrix, rank_tolerance=1e-12)
    assert result.numerical_rank == 2
    assert result.singular_values_domain[-1] > 1e-12
    # squaring would push this below float64 resolution relative to sigma_max
    assert (tiny**2) < np.finfo(float).eps


def test_analyze_identifiability_kernel_projector_matches_explicit_nullspace():
    matrix = np.array([[1.0, 0.0, 0.0]])
    result = analyze_identifiability(matrix, rank_tolerance=1e-9)
    expected_projector = np.diag([0.0, 1.0, 1.0])
    np.testing.assert_allclose(result.kernel_projector.real, expected_projector, atol=1e-12)


def test_analyze_identifiability_rank_tolerance_is_keyword_only():
    with pytest.raises(TypeError):
        analyze_identifiability(np.eye(2), 1e-9)  # positional tolerance must fail


def test_build_measurement_matrix_imag_atol_is_keyword_only():
    with pytest.raises(TypeError):
        build_measurement_matrix((np.eye(2, dtype=complex),), (np.eye(2, dtype=complex),), 1e-9)
