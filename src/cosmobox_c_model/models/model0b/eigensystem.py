"""Toy Model 0B P0 (53-bit / NumPy binary64) eigensystem layer: Hermitian
diagonalization, frozen backward-error diagnostics, and the frozen numerical
clustering rule (docs/toy-models/toy0b/temporal-event-solver.md Sections
15-17, docs/toy-models/toy0b/specification.md Section 4).

Scope firewall: this module implements ONLY the P0 = 53-bit route. The
frozen multi-precision protocol (P1 >= 106 bits, P2 >= 212 bits, p/2p
projector stability `d_P`) is NOT implemented here and is deferred to a
separate bounded lot.

Critical epistemic rule preserved throughout this module:

    NUMERICAL CLUSTER != PHYSICAL DEGENERACY

A P0 numerical cluster is a candidate grouping of eigenvalues that cannot be
resolved apart given the current backward-error budget. It is never promoted
to a certified physical degeneracy statement by this module. Downstream
confirmatory use of `ground_density_candidate` /
`ground_cluster_dimension_candidate` requires the (not yet implemented)
precision-stability route; this module marks every result
`precision_status = "P0_ONLY_NOT_PRECISION_CERTIFIED"` accordingly.

This module receives an already assembled Hamiltonian matrix: it never
reconstructs H from (g, mu, delta), never knows the campaign grid, never
mutates H, and never silently symmetrizes an input that fails the exact
Hermiticity check.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

P0_BITS = 53

BACKWARD_RESIDUAL_TOLERANCE = 1e-12

BACKWARD_ORTHOGONALITY_TOLERANCE = 1e-12

# Recorded here as frozen protocol provenance for the next (P1/P2) stage.
# Not used in this module to claim p/2p projector stability: P1 and P2 are
# not implemented here.
PROJECTOR_STABILITY_TOLERANCE = 1e-10

BACKWARD_GATE_STATUS_PASS = "P0_BACKWARD_PASS"
BACKWARD_GATE_STATUS_FAIL = "P0_BACKWARD_FAIL"

PRECISION_STATUS_P0_ONLY = "P0_ONLY_NOT_PRECISION_CERTIFIED"


@dataclass(frozen=True)
class P0EigensystemResult:
    """Immutable P0 diagnostic bundle for a single assembled Hamiltonian.

    `ground_cluster_dimension_candidate` and `ground_density_candidate` are
    engineering candidates only: they are P0 numerical-cluster artifacts, not
    a precision-certified physical ground-state degeneracy or canonical
    density matrix.
    """

    eigenvalues: np.ndarray
    eigenvectors: np.ndarray

    energy_center: complex
    hamiltonian_scale: float

    residual_ratio: float
    orthogonality_defect: float
    backward_gate_pass: bool
    backward_gate_status: str

    epsilon_h: float

    clusters: tuple[tuple[int, ...], ...]
    cluster_projectors: tuple[np.ndarray, ...]

    ground_cluster_index: int
    ground_cluster_indices: tuple[int, ...]
    ground_cluster_projector: np.ndarray
    ground_cluster_dimension_candidate: int
    ground_density_candidate: np.ndarray

    ground_to_next_cluster_separation_candidate: float | None

    precision_bits: int
    precision_status: str


def _validate_hamiltonian(hamiltonian: np.ndarray) -> None:
    if not isinstance(hamiltonian, np.ndarray) or hamiltonian.ndim != 2:
        raise ValueError("hamiltonian must be a 2D array")
    rows, cols = hamiltonian.shape
    if rows != cols:
        raise ValueError("hamiltonian must be square")
    if not np.all(np.isfinite(hamiltonian)):
        raise ValueError("hamiltonian must have only finite entries")
    if not np.array_equal(hamiltonian, hamiltonian.conj().T):
        raise ValueError("hamiltonian must be exactly Hermitian")


def _numerical_clusters(
    eigenvalues: np.ndarray, epsilon_h: float
) -> tuple[tuple[int, ...], ...]:
    """Connected overlap components of I_i=[E_i-epsilon_H,E_i+epsilon_H] for
    ascending eigenvalues: a boundary between adjacent indices is resolved
    iff E_{i+1}-E_i > 2*epsilon_H (temporal-event-solver.md Section 16)."""
    dimension = eigenvalues.shape[0]
    clusters: list[list[int]] = [[0]]
    for i in range(1, dimension):
        if eigenvalues[i] - eigenvalues[i - 1] > 2 * epsilon_h:
            clusters.append([i])
        else:
            clusters[-1].append(i)
    return tuple(tuple(cluster) for cluster in clusters)


def analyze_p0_eigensystem(hamiltonian: np.ndarray) -> P0EigensystemResult:
    """Hermitian P0 (NumPy binary64) diagonalization plus the frozen
    backward gate and numerical-clustering diagnostics
    (temporal-event-solver.md Sections 15-16). Never claims P1/P2 precision
    stability."""
    _validate_hamiltonian(hamiltonian)
    dimension = hamiltonian.shape[0]

    eigenvalues, eigenvectors = np.linalg.eigh(hamiltonian)

    identity = np.eye(dimension, dtype=complex)
    energy_center = complex(np.trace(hamiltonian) / dimension)
    centered = hamiltonian - energy_center * identity
    hamiltonian_scale = max(1.0, float(np.linalg.norm(centered, ord=2)))

    lambda_diag = np.diag(eigenvalues).astype(complex)
    residual = hamiltonian @ eigenvectors - eigenvectors @ lambda_diag
    residual_ratio = float(np.linalg.norm(residual, ord=2) / hamiltonian_scale)

    orthogonality_defect = float(
        np.linalg.norm(eigenvectors.conj().T @ eigenvectors - identity, ord=2)
    )

    backward_gate_pass = (
        residual_ratio <= BACKWARD_RESIDUAL_TOLERANCE
        and orthogonality_defect <= BACKWARD_ORTHOGONALITY_TOLERANCE
    )
    backward_gate_status = (
        BACKWARD_GATE_STATUS_PASS if backward_gate_pass else BACKWARD_GATE_STATUS_FAIL
    )

    epsilon_h = hamiltonian_scale * (residual_ratio + orthogonality_defect)

    clusters = _numerical_clusters(eigenvalues, epsilon_h)
    cluster_projectors = tuple(
        eigenvectors[:, list(cluster)] @ eigenvectors[:, list(cluster)].conj().T
        for cluster in clusters
    )

    ground_cluster_index = 0
    ground_cluster_indices = clusters[ground_cluster_index]
    ground_cluster_projector = cluster_projectors[ground_cluster_index]
    ground_cluster_dimension_candidate = len(ground_cluster_indices)
    ground_density_candidate = ground_cluster_projector / ground_cluster_dimension_candidate

    if len(clusters) > 1:
        next_cluster_indices = clusters[1]
        ground_to_next_cluster_separation_candidate = float(
            eigenvalues[next_cluster_indices[0]] - eigenvalues[ground_cluster_indices[-1]]
        )
    else:
        ground_to_next_cluster_separation_candidate = None

    return P0EigensystemResult(
        eigenvalues=eigenvalues,
        eigenvectors=eigenvectors,
        energy_center=energy_center,
        hamiltonian_scale=hamiltonian_scale,
        residual_ratio=residual_ratio,
        orthogonality_defect=orthogonality_defect,
        backward_gate_pass=backward_gate_pass,
        backward_gate_status=backward_gate_status,
        epsilon_h=epsilon_h,
        clusters=clusters,
        cluster_projectors=cluster_projectors,
        ground_cluster_index=ground_cluster_index,
        ground_cluster_indices=ground_cluster_indices,
        ground_cluster_projector=ground_cluster_projector,
        ground_cluster_dimension_candidate=ground_cluster_dimension_candidate,
        ground_density_candidate=ground_density_candidate,
        ground_to_next_cluster_separation_candidate=ground_to_next_cluster_separation_candidate,
        precision_bits=P0_BITS,
        precision_status=PRECISION_STATUS_P0_ONLY,
    )
