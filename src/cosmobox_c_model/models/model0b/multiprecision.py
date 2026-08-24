"""Toy Model 0B single-level high-precision (P1/P2) eigensystem layer:
direct H^(p) reassembly through the accepted I2-B1 exact-assembly route,
mpmath Hermitian diagonalization, frozen high-precision backward
diagnostics, and the frozen numerical clustering rule
(docs/toy-models/toy0b/temporal-event-solver.md Sections 15-17,
docs/toy-models/toy0b/specification.md Section 4).

Scope firewall: this module analyzes ONE precision level at a time (P1=106
bits or P2=212 bits). It performs NO cross-precision comparison: no P0/P1,
P1/P2, or any other precision matching, no `d_P`, and no
PRECISION_STABLE / PRECISION_ESCALATED / PRECISION_UNRESOLVED routing. That
layer is deferred to a separate bounded lot (I2-B2-B). P0 (53-bit / NumPy)
analysis remains the separately accepted `eigensystem.py` route and is not
reachable through this module (`precision_bits=53` is rejected here).

Critical epistemic rule preserved throughout this module (unchanged from
the accepted P0 layer):

    NUMERICAL CLUSTER != PHYSICAL DEGENERACY

A P1/P2 numerical cluster is a candidate grouping of eigenvalues that
cannot be resolved apart given the current backward-error budget at that
precision. It is never promoted to a certified physical degeneracy
statement by this module. `ground_density_candidate` and
`ground_cluster_dimension_candidate` are P1/P2 numerical-cluster
engineering candidates only; every result is marked
`precision_level_status` accordingly (never a final
PRECISION_STABLE/ESCALATED/UNRESOLVED verdict).

Direct-assembly firewall: the only public scientific entry point,
`analyze_mp_eigensystem`, accepts `ExactDiscreteHamiltonianComponents` plus
exact rational parameters and calls the accepted
`exact_assembly.assemble_hamiltonian_mp` to reassemble H^(p) directly at
the requested precision -- it never accepts a preassembled Hamiltonian
matrix as its public scientific input, and never reconstructs the model
physics itself (no fermionic sign, hopping, or Gauss logic here).

Concurrency: as documented in `exact_assembly.py`
(`MPMATH_SHARED_THREAD_PARALLELISM = "NOT_SUPPORTED"`), mpmath's working
precision is global mutable process state, not thread-local. This module
inherits that constraint unchanged.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

import mpmath as mp

from cosmobox_c_model.models.model0b.exact_assembly import (
    ExactDiscreteHamiltonianComponents,
    P1_BITS,
    P2_BITS,
    assemble_hamiltonian_mp,
)

MP_ALLOWED_PRECISION_BITS = (P1_BITS, P2_BITS)

BACKWARD_RESIDUAL_TOLERANCE = mp.mpf("1e-12")

BACKWARD_ORTHOGONALITY_TOLERANCE = mp.mpf("1e-12")

# Recorded here as frozen protocol provenance for the next (cross-precision)
# stage. NOT used in this module to issue a p/2p stability verdict: d_P and
# cross-precision cluster matching are not implemented here.
PROJECTOR_STABILITY_TOLERANCE = mp.mpf("1e-10")

BACKWARD_GATE_STATUS_PASS = "MP_BACKWARD_PASS"
BACKWARD_GATE_STATUS_FAIL = "MP_BACKWARD_FAIL"

PRECISION_LEVEL_STATUS_P1 = "P1_ANALYZED_NOT_CROSS_PRECISION_CERTIFIED"
PRECISION_LEVEL_STATUS_P2 = "P2_ANALYZED_NOT_CROSS_PRECISION_CERTIFIED"

_PRECISION_LEVEL_STATUS = {
    P1_BITS: PRECISION_LEVEL_STATUS_P1,
    P2_BITS: PRECISION_LEVEL_STATUS_P2,
}


@dataclass(frozen=True)
class MPEigensystemResult:
    """Immutable single-precision-level (P1 or P2) diagnostic bundle.

    `ground_cluster_dimension_candidate` and `ground_density_candidate` are
    engineering candidates only: P1/P2 numerical-cluster artifacts, not a
    cross-precision-certified physical ground-state degeneracy or canonical
    density matrix. `precision_level_status` never claims
    PRECISION_STABLE/ESCALATED/UNRESOLVED.
    """

    precision_bits: int

    eigenvalues: tuple["mp.mpf", ...]
    eigenvectors: "mp.matrix"

    energy_center: "mp.mpf"
    hamiltonian_scale: "mp.mpf"

    residual_ratio: "mp.mpf"
    orthogonality_defect: "mp.mpf"
    backward_gate_pass: bool
    backward_gate_status: str

    epsilon_h: "mp.mpf"

    clusters: tuple[tuple[int, ...], ...]
    cluster_projectors: tuple["mp.matrix", ...]

    ground_cluster_index: int
    ground_cluster_indices: tuple[int, ...]
    ground_cluster_projector: "mp.matrix"
    ground_cluster_dimension_candidate: int
    ground_density_candidate: "mp.matrix"

    ground_to_next_cluster_separation_candidate: "mp.mpf | None"

    precision_level_status: str


def _validate_mp_precision_bits(precision_bits: int) -> None:
    if not isinstance(precision_bits, int) or isinstance(precision_bits, bool):
        raise TypeError("precision_bits must be an int")
    if precision_bits not in MP_ALLOWED_PRECISION_BITS:
        raise ValueError(
            f"precision_bits must be one of {MP_ALLOWED_PRECISION_BITS} "
            f"(P0=53 is the separately accepted NumPy route), got {precision_bits}"
        )


def _validate_hermitian_mp(hamiltonian: "mp.matrix") -> None:
    """Verify `hamiltonian` is exactly Hermitian in its mpmath
    representation. Never symmetrizes."""
    dimension = hamiltonian.rows
    if hamiltonian.cols != dimension:
        raise ValueError("hamiltonian must be square")
    for i in range(dimension):
        for j in range(dimension):
            if hamiltonian[i, j] != hamiltonian[j, i].conjugate():
                raise ValueError("hamiltonian must be exactly Hermitian")


def _spectral_norm_hermitian(eigenvalues) -> "mp.mpf":
    """||A||_2 = max_j |lambda_j(A)| for Hermitian A."""
    return max(abs(e) for e in eigenvalues)


def _spectral_norm_general(matrix: "mp.matrix") -> "mp.mpf":
    """||A||_2 = sqrt(lambda_max(A^dagger A)) for general A, via the
    Hermitian positive-semidefinite A^dagger A."""
    product = matrix.transpose_conj() * matrix
    eigenvalues = mp.eighe(product, eigvals_only=True)
    top = max(eigenvalues[i].real for i in range(matrix.cols))
    return mp.sqrt(max(top, mp.mpf(0)))


def _numerical_clusters_mp(
    eigenvalues: tuple["mp.mpf", ...], epsilon_h: "mp.mpf"
) -> tuple[tuple[int, ...], ...]:
    """Connected overlap components of I_i=[E_i-epsilon_H,E_i+epsilon_H] for
    ascending eigenvalues: a boundary between adjacent indices is resolved
    iff E_{i+1}-E_i > 2*epsilon_H (temporal-event-solver.md Section 16)."""
    dimension = len(eigenvalues)
    clusters: list[list[int]] = [[0]]
    for i in range(1, dimension):
        if eigenvalues[i] - eigenvalues[i - 1] > 2 * epsilon_h:
            clusters.append([i])
        else:
            clusters[-1].append(i)
    return tuple(tuple(cluster) for cluster in clusters)


def _cluster_projector_mp(
    eigenvectors: "mp.matrix", cluster: tuple[int, ...], dimension: int
) -> "mp.matrix":
    """P_C = sum_{i in C} |v_i><v_i|."""
    projector = mp.matrix(dimension, dimension)
    for index in cluster:
        column = eigenvectors[:, index]
        projector = projector + column * column.transpose_conj()
    return projector


def _analyze_mp_hermitian_matrix(
    hamiltonian: "mp.matrix", *, precision_bits: int
) -> MPEigensystemResult:
    """Backend numerical analyzer: Hermitian mpmath diagonalization plus the
    frozen backward gate and numerical-clustering diagnostics, at whatever
    precision is currently active in the caller's `mp.workprec` context.
    Private: the scientific public route is `analyze_mp_eigensystem`, which
    performs the direct H^(p) reassembly before calling this function."""
    dimension = hamiltonian.rows

    eigenvalues_column, eigenvectors = mp.eighe(hamiltonian)
    eigenvalues = tuple(eigenvalues_column[i] for i in range(dimension))

    identity = mp.eye(dimension)
    trace = sum(hamiltonian[i, i] for i in range(dimension))
    energy_center = trace / dimension

    # H_centered = H - E_bar*I is Hermitian (H and E_bar*I both are), and its
    # eigenvalues are exactly (H's eigenvalues - E_bar): reused directly
    # rather than recomputing a second eigendecomposition.
    centered_eigenvalues = tuple(e - energy_center for e in eigenvalues)
    hamiltonian_scale = max(mp.mpf(1), _spectral_norm_hermitian(centered_eigenvalues))

    lambda_diag = mp.diag(list(eigenvalues))
    residual = hamiltonian * eigenvectors - eigenvectors * lambda_diag
    residual_ratio = _spectral_norm_general(residual) / hamiltonian_scale

    # V^dagger V - I is Hermitian by construction.
    orthogonality_matrix = eigenvectors.transpose_conj() * eigenvectors - identity
    orthogonality_eigenvalues = mp.eighe(orthogonality_matrix, eigvals_only=True)
    orthogonality_defect = _spectral_norm_hermitian(
        tuple(orthogonality_eigenvalues[i] for i in range(dimension))
    )

    backward_gate_pass = (
        residual_ratio <= BACKWARD_RESIDUAL_TOLERANCE
        and orthogonality_defect <= BACKWARD_ORTHOGONALITY_TOLERANCE
    )
    backward_gate_status = (
        BACKWARD_GATE_STATUS_PASS if backward_gate_pass else BACKWARD_GATE_STATUS_FAIL
    )

    epsilon_h = hamiltonian_scale * (residual_ratio + orthogonality_defect)

    clusters = _numerical_clusters_mp(eigenvalues, epsilon_h)
    cluster_projectors = tuple(
        _cluster_projector_mp(eigenvectors, cluster, dimension) for cluster in clusters
    )

    ground_cluster_index = 0
    ground_cluster_indices = clusters[ground_cluster_index]
    ground_cluster_projector = cluster_projectors[ground_cluster_index]
    ground_cluster_dimension_candidate = len(ground_cluster_indices)
    ground_density_candidate = ground_cluster_projector / ground_cluster_dimension_candidate

    if len(clusters) > 1:
        next_cluster_indices = clusters[1]
        ground_to_next_cluster_separation_candidate = (
            eigenvalues[next_cluster_indices[0]] - eigenvalues[ground_cluster_indices[-1]]
        )
    else:
        ground_to_next_cluster_separation_candidate = None

    return MPEigensystemResult(
        precision_bits=precision_bits,
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
        precision_level_status=_PRECISION_LEVEL_STATUS[precision_bits],
    )


def analyze_mp_eigensystem(
    components: ExactDiscreteHamiltonianComponents,
    *,
    g: Fraction | int,
    mu: Fraction | int,
    delta: Fraction | int,
    precision_bits: int,
) -> MPEigensystemResult:
    """Direct single-precision-level (P1 or P2) Model 0B eigensystem
    analysis: reassembles H^(p) via the accepted
    `exact_assembly.assemble_hamiltonian_mp`, then performs Hermitian
    diagonalization plus the frozen backward-gate and numerical-clustering
    diagnostics, entirely inside one `mp.workprec(precision_bits)` context
    (temporal-event-solver.md Sections 15-16). Never accepts a preassembled
    Hamiltonian; never claims cross-precision stability."""
    _validate_mp_precision_bits(precision_bits)

    with mp.workprec(precision_bits):
        hamiltonian = assemble_hamiltonian_mp(
            components, g=g, mu=mu, delta=delta, precision_bits=precision_bits
        )
        _validate_hermitian_mp(hamiltonian)
        result = _analyze_mp_hermitian_matrix(hamiltonian, precision_bits=precision_bits)

    return result
