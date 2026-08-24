"""Tests for the Toy Model 0B P0 eigensystem layer: backward gate, numerical
clustering, cluster projectors, and the numerical ground-cluster candidate
(docs/toy-models/toy0b/temporal-event-solver.md Sections 15-17).

NUMERICAL CLUSTER != PHYSICAL DEGENERACY: this file never asserts a
precision-certified physical quantity for the Model 0B reference
Hamiltonian; only P0-only engineering diagnostics."""

from __future__ import annotations

import numpy as np
import pytest

from cosmobox_c_model.models.model0b import eigensystem as eig
from cosmobox_c_model.models.model0b.basis_config import build_physical_basis
from cosmobox_c_model.models.model0b.hamiltonian import build_hamiltonian


# --- Frozen constants --------------------------------------------------------


def test_p0_bits():
    assert eig.P0_BITS == 53


def test_backward_residual_tolerance():
    assert eig.BACKWARD_RESIDUAL_TOLERANCE == 1e-12


def test_backward_orthogonality_tolerance():
    assert eig.BACKWARD_ORTHOGONALITY_TOLERANCE == 1e-12


def test_projector_stability_tolerance():
    assert eig.PROJECTOR_STABILITY_TOLERANCE == 1e-10


# --- Simple exact matrices ----------------------------------------------------


def test_diagonal_matrix_no_degeneracy():
    matrix = np.diag([0.0, 1.0, 3.0]).astype(complex)
    result = eig.analyze_p0_eigensystem(matrix)

    assert np.array_equal(result.eigenvalues, np.array([0.0, 1.0, 3.0]))
    assert result.clusters == ((0,), (1,), (2,))
    assert result.ground_cluster_dimension_candidate == 1

    expected_ground_projector = np.diag([1.0, 0.0, 0.0]).astype(complex)
    assert np.allclose(result.ground_cluster_projector, expected_ground_projector, atol=1e-10)
    assert np.allclose(result.ground_density_candidate, result.ground_cluster_projector, atol=1e-10)
    assert result.ground_to_next_cluster_separation_candidate == pytest.approx(1.0)


def test_exact_degenerate_diagonal_matrix():
    matrix = np.diag([0.0, 0.0, 2.0]).astype(complex)
    result = eig.analyze_p0_eigensystem(matrix)

    assert result.clusters[0] == (0, 1)
    assert result.ground_cluster_dimension_candidate == 2

    expected_ground_projector = np.diag([1.0, 1.0, 0.0]).astype(complex)
    assert np.allclose(result.ground_cluster_projector, expected_ground_projector, atol=1e-10)

    expected_rho = np.diag([0.5, 0.5, 0.0]).astype(complex)
    assert np.allclose(result.ground_density_candidate, expected_rho, atol=1e-10)

    assert result.ground_to_next_cluster_separation_candidate == pytest.approx(2.0)


@pytest.mark.parametrize("dimension", [2, 3, 5])
def test_fully_degenerate_zero_matrix(dimension):
    matrix = np.zeros((dimension, dimension), dtype=complex)
    result = eig.analyze_p0_eigensystem(matrix)

    assert len(result.clusters) == 1
    assert result.ground_cluster_dimension_candidate == dimension
    assert result.ground_to_next_cluster_separation_candidate is None

    expected_rho = np.eye(dimension, dtype=complex) / dimension
    assert np.allclose(result.ground_density_candidate, expected_rho, atol=1e-10)


# --- Backward diagnostics ------------------------------------------------------


@pytest.mark.parametrize(
    "matrix",
    [
        np.diag([0.0, 1.0, 3.0]).astype(complex),
        np.diag([0.0, 0.0, 2.0]).astype(complex),
        np.zeros((4, 4), dtype=complex),
        np.array([[2.0, 1.0], [1.0, 2.0]], dtype=complex),
        np.array([[0.0, 1.0j], [-1.0j, 0.0]], dtype=complex),
    ],
)
def test_backward_diagnostics_pass_and_epsilon_derived(matrix):
    result = eig.analyze_p0_eigensystem(matrix)

    assert result.residual_ratio <= eig.BACKWARD_RESIDUAL_TOLERANCE
    assert result.orthogonality_defect <= eig.BACKWARD_ORTHOGONALITY_TOLERANCE
    assert result.backward_gate_pass is True
    assert result.backward_gate_status == eig.BACKWARD_GATE_STATUS_PASS

    expected_epsilon = result.hamiltonian_scale * (
        result.residual_ratio + result.orthogonality_defect
    )
    assert result.epsilon_h == pytest.approx(expected_epsilon)


# --- Projectors ---------------------------------------------------------------


@pytest.mark.parametrize(
    "matrix",
    [
        np.diag([0.0, 1.0, 3.0]).astype(complex),
        np.diag([0.0, 0.0, 2.0]).astype(complex),
        np.zeros((3, 3), dtype=complex),
        np.array([[2.0, 1.0], [1.0, 2.0]], dtype=complex),
    ],
)
def test_projector_properties(matrix):
    result = eig.analyze_p0_eigensystem(matrix)
    dimension = matrix.shape[0]
    tol = eig.PROJECTOR_STABILITY_TOLERANCE

    total = np.zeros((dimension, dimension), dtype=complex)
    for cluster, projector in zip(result.clusters, result.cluster_projectors):
        assert np.allclose(projector, projector.conj().T, atol=tol)
        assert np.allclose(projector @ projector, projector, atol=tol)
        assert np.trace(projector).real == pytest.approx(len(cluster), abs=tol)
        total = total + projector

    for i, (_, projector_i) in enumerate(zip(result.clusters, result.cluster_projectors)):
        for j, (_, projector_j) in enumerate(zip(result.clusters, result.cluster_projectors)):
            if i != j:
                assert np.allclose(
                    projector_i @ projector_j,
                    np.zeros((dimension, dimension)),
                    atol=tol,
                )

    assert np.allclose(total, np.eye(dimension, dtype=complex), atol=tol)


# --- Model 0B reference qualification ------------------------------------------


def test_model0b_reference_qualification_lambda2():
    basis = build_physical_basis(2)
    hamiltonian = build_hamiltonian(basis, lambda_cutoff=2, g=1, mu=0, delta=0)
    result = eig.analyze_p0_eigensystem(hamiltonian)

    assert hamiltonian.shape == (78, 78)
    assert result.backward_gate_pass is True
    assert len(result.clusters[result.ground_cluster_index]) == 1
    assert result.ground_cluster_dimension_candidate == 1

    ground_trace = np.trace(result.ground_density_candidate)
    assert ground_trace.real == pytest.approx(1.0, abs=1e-10)
    assert ground_trace.imag == pytest.approx(0.0, abs=1e-10)

    assert result.ground_to_next_cluster_separation_candidate is not None
    assert result.ground_to_next_cluster_separation_candidate > 0.0

    assert result.precision_status == "P0_ONLY_NOT_PRECISION_CERTIFIED"
    assert result.precision_bits == 53


@pytest.mark.parametrize("lambda_cutoff", [1, 3])
def test_model0b_reference_lambda_sanity(lambda_cutoff):
    basis = build_physical_basis(lambda_cutoff)
    hamiltonian = build_hamiltonian(basis, lambda_cutoff=lambda_cutoff, g=1, mu=0, delta=0)
    result = eig.analyze_p0_eigensystem(hamiltonian)

    assert result.backward_gate_pass is True

    dimension = hamiltonian.shape[0]
    total = sum(result.cluster_projectors)
    assert np.allclose(total, np.eye(dimension, dtype=complex), atol=eig.PROJECTOR_STABILITY_TOLERANCE)

    assert result.precision_status == "P0_ONLY_NOT_PRECISION_CERTIFIED"


# --- Invalid input --------------------------------------------------------------


def test_rejects_non_2d_input():
    with pytest.raises(ValueError):
        eig.analyze_p0_eigensystem(np.zeros(3))


def test_rejects_non_square_input():
    with pytest.raises(ValueError):
        eig.analyze_p0_eigensystem(np.zeros((2, 3)))


def test_rejects_nan_input():
    matrix = np.eye(2, dtype=complex)
    matrix[0, 0] = np.nan
    with pytest.raises(ValueError):
        eig.analyze_p0_eigensystem(matrix)


def test_rejects_inf_input():
    matrix = np.eye(2, dtype=complex)
    matrix[0, 0] = np.inf
    with pytest.raises(ValueError):
        eig.analyze_p0_eigensystem(matrix)


def test_rejects_non_hermitian_input():
    matrix = np.array([[1.0, 1.0], [0.0, 1.0]], dtype=complex)
    with pytest.raises(ValueError):
        eig.analyze_p0_eigensystem(matrix)


def test_does_not_silently_symmetrize_non_hermitian_input():
    matrix = np.array([[1.0, 2.0], [0.0, 1.0]], dtype=complex)
    with pytest.raises(ValueError):
        eig.analyze_p0_eigensystem(matrix)
    # The input itself must remain untouched by the rejected call.
    assert matrix[0, 1] == 2.0
    assert matrix[1, 0] == 0.0
