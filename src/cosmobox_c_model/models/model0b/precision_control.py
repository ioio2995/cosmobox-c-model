"""Toy Model 0B frozen cross-precision spectral-projector control: P0/P1 and
P1/P2 numerical-cluster matching, the frozen projector distance `d_P`, and
the deterministic P0/P1/P2 precision-escalation ladder
(docs/toy-models/toy0b/temporal-event-solver.md Sections 15-20).

Scope firewall: this module certifies NUMERICAL cross-precision projector
stability only. It never publishes a final physical ground-state
degeneracy, `d_GS`, `gap_GS`, spectral weights, or any confirmatory
scientific verdict. `NUMERICAL CLUSTER != PHYSICAL DEGENERACY` is preserved
unchanged from the accepted P0 and P1/P2 layers: a `PRECISION_STABLE` or
`PRECISION_ESCALATED` verdict certifies only that the numerical cluster
partition and its projector are stable under increasing arithmetic
precision, never that it is a certified physical degeneracy.

Matching convention: numerical clusters are already deterministic
partitions of the same ordered spectral index set {0,...,d-1} at every
precision (the model, basis, and index ordering do not change with
precision). A HIGH-precision cluster split of a LOW-precision cluster is
covered by summing the HIGH-precision projectors whose union exactly
equals the LOW cluster's index set (frozen split-cluster rule). Any
HIGH-precision cluster that straddles a LOW-precision resolved boundary
makes the subspace assignment ambiguous and fails closed as
`SPECTRAL_CLUSTER_UNRESOLVED`; no representative-frequency, nearest-value,
centroid, overlap-percentage, Hungarian, or eigenvector-overlap heuristic
matching is used.

Direct-reassembly firewall: P0, P1 and P2 are each reassembled directly
from `ExactDiscreteHamiltonianComponents` + exact rational parameters
through the already-accepted routes (`exact_assembly.assemble_hamiltonian_mp`,
`eigensystem.analyze_p0_eigensystem`, `multiprecision.analyze_mp_eigensystem`).
P0 is never obtained by downcasting a P1/P2 Hamiltonian, and no precision
level is ever upcast from another already-assembled Hamiltonian.

`PRECISION_UNRESOLVED` is terminal: no downstream confirmatory dependency
may consume a result at that status.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

import mpmath as mp
import numpy as np

from cosmobox_c_model.models.model0b.eigensystem import (
    P0EigensystemResult,
    analyze_p0_eigensystem,
)
from cosmobox_c_model.models.model0b.exact_assembly import (
    ExactDiscreteHamiltonianComponents,
    P0_BITS,
    P1_BITS,
    P2_BITS,
    assemble_hamiltonian_mp,
)
from cosmobox_c_model.models.model0b.multiprecision import (
    MPEigensystemResult,
    PROJECTOR_STABILITY_TOLERANCE,
    _fraction_to_mpf_current,
    _spectral_norm_general,
    analyze_mp_eigensystem,
)

ALLOWED_PRECISION_PAIRS = ((P0_BITS, P1_BITS), (P1_BITS, P2_BITS))

MATCHING_STATUS_MATCHED = "MATCHED"
MATCHING_STATUS_UNRESOLVED = "SPECTRAL_CLUSTER_UNRESOLVED"

FAILURE_REASON_NONE = "NONE"
FAILURE_REASON_BACKWARD_GATE_FAILED = "BACKWARD_GATE_FAILED"
FAILURE_REASON_SPECTRAL_CLUSTER_UNRESOLVED = "SPECTRAL_CLUSTER_UNRESOLVED"
FAILURE_REASON_PROJECTOR_STABILITY_FAILED = "PROJECTOR_STABILITY_FAILED"

PRECISION_STATUS_STABLE = "PRECISION_STABLE"
PRECISION_STATUS_ESCALATED = "PRECISION_ESCALATED"
PRECISION_STATUS_UNRESOLVED = "PRECISION_UNRESOLVED"


@dataclass(frozen=True)
class PrecisionPairComparison:
    """Frozen cross-precision comparison of one (LOW, HIGH) precision pair:
    53->106 or 106->212. Never a final physical-degeneracy or ground-state
    claim."""

    low_precision_bits: int
    high_precision_bits: int

    matching_status: str
    cluster_mapping: "tuple[tuple[int, ...], ...] | None"

    backward_gates_pass: bool

    projector_defects: "tuple[mp.mpf, ...]"
    d_p: "mp.mpf | None"

    stability_pass: bool
    failure_reason: str


@dataclass(frozen=True)
class SpectralPrecisionControlResult:
    """Frozen P0/P1/P2 precision-escalation ladder outcome.

    `selected_level_result` is a NUMERICAL precision-selected eigensystem
    only: it does not by itself define physical degeneracy, final `d_GS`,
    or final `gap_GS`. `PRECISION_UNRESOLVED` is terminal for any
    downstream confirmatory dependency.
    """

    p0_result: P0EigensystemResult
    p1_result: MPEigensystemResult
    p0_p1_comparison: PrecisionPairComparison

    p2_result: "MPEigensystemResult | None"
    p1_p2_comparison: "PrecisionPairComparison | None"

    precision_status: str
    selected_precision_bits: "int | None"
    selected_level_result: "MPEigensystemResult | None"


def _validate_partition(
    clusters: "tuple[tuple[int, ...], ...]", dimension: int, *, name: str
) -> None:
    """Fail closed (no repair, no sorting) unless `clusters` is a
    well-formed partition of `range(dimension)`: nonempty integer-index
    tuples with strictly increasing indices, clusters ordered by their
    first index, pairwise disjoint, flattening exactly to
    `tuple(range(dimension))`."""
    if not isinstance(clusters, tuple) or not all(isinstance(c, tuple) for c in clusters):
        raise ValueError(f"{name}: clusters must be a tuple of tuples")

    flattened: list[int] = []
    previous_first: "int | None" = None
    for cluster in clusters:
        if len(cluster) == 0:
            raise ValueError(f"{name}: clusters must be nonempty")
        if not all(isinstance(index, int) and not isinstance(index, bool) for index in cluster):
            raise ValueError(f"{name}: cluster indices must be int")
        for previous_index, current_index in zip(cluster, cluster[1:]):
            if current_index <= previous_index:
                raise ValueError(f"{name}: cluster indices must be strictly increasing")
        if previous_first is not None and cluster[0] <= previous_first:
            raise ValueError(f"{name}: clusters must be ordered by first index")
        previous_first = cluster[0]
        flattened.extend(cluster)

    if len(set(flattened)) != len(flattened):
        raise ValueError(f"{name}: clusters must be pairwise disjoint")

    if tuple(flattened) != tuple(range(dimension)):
        raise ValueError(f"{name}: clusters must flatten exactly to range(dimension)")


def _match_clusters(
    low_clusters: "tuple[tuple[int, ...], ...]",
    high_clusters: "tuple[tuple[int, ...], ...]",
) -> "tuple[str, tuple[tuple[int, ...], ...] | None]":
    """Deterministic index-set subspace matching (frozen split-cluster
    rule): for each LOW cluster, collect every HIGH cluster whose index set
    is fully contained in it, and require their union to equal the LOW
    cluster exactly. Any HIGH cluster overlapping a LOW cluster without
    being fully contained in it fails closed as
    `SPECTRAL_CLUSTER_UNRESOLVED`. Returns HIGH-cluster ordinal indices per
    LOW cluster (deterministic LOW-cluster order), never a representative
    frequency."""
    mapping: list[tuple[int, ...]] = []
    for low_cluster in low_clusters:
        low_set = set(low_cluster)
        covering_high_indices: list[int] = []
        covered: set[int] = set()
        for high_index, high_cluster in enumerate(high_clusters):
            high_set = set(high_cluster)
            if not (high_set & low_set):
                continue
            if not high_set <= low_set:
                return MATCHING_STATUS_UNRESOLVED, None
            covering_high_indices.append(high_index)
            covered |= high_set
        if covered != low_set:
            return MATCHING_STATUS_UNRESOLVED, None
        mapping.append(tuple(covering_high_indices))
    return MATCHING_STATUS_MATCHED, tuple(mapping)


def _p0_matrix_to_mp_exact(matrix: np.ndarray) -> "mp.matrix":
    """Convert a P0 (NumPy complex128) matrix to an mpmath matrix,
    preserving EXACTLY the binary64 value actually stored in each entry via
    `Fraction.from_float` (never a decimal-string roundtrip). Must be
    called only while the target HIGH `mp.workprec(...)` context is
    active."""
    dimension = matrix.shape[0]
    out = mp.matrix(dimension, dimension)
    for i in range(dimension):
        for j in range(dimension):
            value = matrix[i, j]
            real_fraction = Fraction.from_float(float(value.real))
            imag_fraction = Fraction.from_float(float(value.imag))
            out[i, j] = mp.mpc(
                _fraction_to_mpf_current(real_fraction),
                _fraction_to_mpf_current(imag_fraction),
            )
    return out


def compare_precision_levels(low_result, high_result) -> PrecisionPairComparison:
    """Compare an accepted LOW-precision result against an accepted
    HIGH-precision result for one of the two frozen adjacent pairs
    (53->106 or 106->212): index-set cluster matching, then the frozen
    projector distance `d_P = max_C ||P_C^(HIGH)-P_C^(LOW)||_2` with the
    LOW cluster's projector covered by the SUM of the matching
    HIGH-precision projectors. Deterministic pair failure precedence:
    BACKWARD_GATE_FAILED > SPECTRAL_CLUSTER_UNRESOLVED >
    PROJECTOR_STABILITY_FAILED > NONE."""
    low_bits = low_result.precision_bits
    high_bits = high_result.precision_bits
    if (low_bits, high_bits) not in ALLOWED_PRECISION_PAIRS:
        raise ValueError(
            f"unsupported precision pair ({low_bits} -> {high_bits}); "
            f"allowed pairs are {ALLOWED_PRECISION_PAIRS}"
        )

    dimension = len(low_result.eigenvalues)
    if len(high_result.eigenvalues) != dimension:
        raise ValueError("low_result and high_result must refer to the same matrix dimension")

    _validate_partition(low_result.clusters, dimension, name="low_result.clusters")
    _validate_partition(high_result.clusters, dimension, name="high_result.clusters")

    backward_gates_pass = bool(low_result.backward_gate_pass) and bool(
        high_result.backward_gate_pass
    )

    matching_status, mapping = _match_clusters(low_result.clusters, high_result.clusters)

    if matching_status == MATCHING_STATUS_UNRESOLVED:
        failure_reason = (
            FAILURE_REASON_BACKWARD_GATE_FAILED
            if not backward_gates_pass
            else FAILURE_REASON_SPECTRAL_CLUSTER_UNRESOLVED
        )
        return PrecisionPairComparison(
            low_precision_bits=low_bits,
            high_precision_bits=high_bits,
            matching_status=matching_status,
            cluster_mapping=None,
            backward_gates_pass=backward_gates_pass,
            projector_defects=(),
            d_p=None,
            stability_pass=False,
            failure_reason=failure_reason,
        )

    with mp.workprec(high_bits):
        if low_bits == P0_BITS:
            low_projectors_mp = tuple(
                _p0_matrix_to_mp_exact(projector) for projector in low_result.cluster_projectors
            )
        else:
            # P1 projectors are already mpmath values holding the P1-rounded
            # numbers: reused as-is, never recomputed at HIGH precision.
            low_projectors_mp = low_result.cluster_projectors

        projector_defects_list = []
        for low_index, high_indices in enumerate(mapping):
            covering = mp.matrix(dimension, dimension)
            for high_index in high_indices:
                covering = covering + high_result.cluster_projectors[high_index]
            difference = covering - low_projectors_mp[low_index]
            projector_defects_list.append(_spectral_norm_general(difference))
        projector_defects = tuple(projector_defects_list)
        d_p = max(projector_defects)

        projector_tolerance_mp = _fraction_to_mpf_current(PROJECTOR_STABILITY_TOLERANCE)
        projector_stability_pass = d_p <= projector_tolerance_mp

    if not backward_gates_pass:
        failure_reason = FAILURE_REASON_BACKWARD_GATE_FAILED
        stability_pass = False
    elif not projector_stability_pass:
        failure_reason = FAILURE_REASON_PROJECTOR_STABILITY_FAILED
        stability_pass = False
    else:
        failure_reason = FAILURE_REASON_NONE
        stability_pass = True

    return PrecisionPairComparison(
        low_precision_bits=low_bits,
        high_precision_bits=high_bits,
        matching_status=matching_status,
        cluster_mapping=mapping,
        backward_gates_pass=backward_gates_pass,
        projector_defects=projector_defects,
        d_p=d_p,
        stability_pass=stability_pass,
        failure_reason=failure_reason,
    )


def _analyze_p0_direct(
    components: ExactDiscreteHamiltonianComponents,
    *,
    g: "Fraction | int",
    mu: "Fraction | int",
    delta: "Fraction | int",
) -> P0EigensystemResult:
    """Direct P0 (53-bit) reassembly from exact discrete components + exact
    rational parameters through the accepted
    `exact_assembly.assemble_hamiltonian_mp` route, converted entrywise to
    NumPy complex128 (an exact, lossless conversion at 53-bit precision),
    then analyzed through the accepted, unmodified
    `eigensystem.analyze_p0_eigensystem` -- which itself fails closed on
    any non-exact Hermiticity before diagonalizing. Never downcasts an
    already-assembled P1/P2 Hamiltonian."""
    with mp.workprec(P0_BITS):
        hamiltonian_mp = assemble_hamiltonian_mp(
            components, g=g, mu=mu, delta=delta, precision_bits=P0_BITS
        )
        dimension = hamiltonian_mp.rows
        hamiltonian_np = np.zeros((dimension, dimension), dtype=complex)
        for i in range(dimension):
            for j in range(dimension):
                value = hamiltonian_mp[i, j]
                hamiltonian_np[i, j] = complex(float(value.real), float(value.imag))
    return analyze_p0_eigensystem(hamiltonian_np)


def _analyze_p1_direct(
    components: ExactDiscreteHamiltonianComponents,
    *,
    g: "Fraction | int",
    mu: "Fraction | int",
    delta: "Fraction | int",
) -> MPEigensystemResult:
    return analyze_mp_eigensystem(components, g=g, mu=mu, delta=delta, precision_bits=P1_BITS)


def _analyze_p2_direct(
    components: ExactDiscreteHamiltonianComponents,
    *,
    g: "Fraction | int",
    mu: "Fraction | int",
    delta: "Fraction | int",
) -> MPEigensystemResult:
    return analyze_mp_eigensystem(components, g=g, mu=mu, delta=delta, precision_bits=P2_BITS)


def run_spectral_precision_control(
    components: ExactDiscreteHamiltonianComponents,
    *,
    g: "Fraction | int",
    mu: "Fraction | int",
    delta: "Fraction | int",
) -> SpectralPrecisionControlResult:
    """Frozen P0/P1/P2 escalation ladder (temporal-event-solver.md Section
    20): P0/P1 stable -> PRECISION_STABLE; otherwise P2 is computed and
    P1/P2 stable -> PRECISION_ESCALATED; otherwise PRECISION_UNRESOLVED. P2
    is never computed on the P0/P1-stable branch (lazy escalation). No
    majority vote, no averaging, no fallback to a lower precision after a
    higher comparison fails."""
    p0_result = _analyze_p0_direct(components, g=g, mu=mu, delta=delta)
    p1_result = _analyze_p1_direct(components, g=g, mu=mu, delta=delta)
    p0_p1_comparison = compare_precision_levels(p0_result, p1_result)

    if p0_p1_comparison.stability_pass:
        return SpectralPrecisionControlResult(
            p0_result=p0_result,
            p1_result=p1_result,
            p0_p1_comparison=p0_p1_comparison,
            p2_result=None,
            p1_p2_comparison=None,
            precision_status=PRECISION_STATUS_STABLE,
            selected_precision_bits=P1_BITS,
            selected_level_result=p1_result,
        )

    p2_result = _analyze_p2_direct(components, g=g, mu=mu, delta=delta)
    p1_p2_comparison = compare_precision_levels(p1_result, p2_result)

    if p1_p2_comparison.stability_pass:
        precision_status = PRECISION_STATUS_ESCALATED
        selected_precision_bits = P2_BITS
        selected_level_result = p2_result
    else:
        precision_status = PRECISION_STATUS_UNRESOLVED
        selected_precision_bits = None
        selected_level_result = None

    return SpectralPrecisionControlResult(
        p0_result=p0_result,
        p1_result=p1_result,
        p0_p1_comparison=p0_p1_comparison,
        p2_result=p2_result,
        p1_p2_comparison=p1_p2_comparison,
        precision_status=precision_status,
        selected_precision_bits=selected_precision_bits,
        selected_level_result=selected_level_result,
    )
