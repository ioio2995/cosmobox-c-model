"""Toy Model 0B canonical ground-state subspace: consumes an already
qualified `precision_control.SpectralPrecisionControlResult` and, when the
underlying cross-precision spectral qualification allows it, publishes the
ground numerical cluster's index set, cardinality, and projector.

Scope firewall: this module computes NO new spectrum, NO new clustering,
NO new precision control, and applies NO new scientific tolerance. It only
identifies -- within the already-computed cluster partition of the
selected precision level -- the unique existing cluster containing the
index of the minimal eigenvalue, and republishes that cluster's already
-computed projector (`multiprecision.MPEigensystemResult.cluster_projectors`)
unchanged. It performs NO physical interpretation: it publishes no
canonical density matrix (`rho_GS = P_GS/d_GS`), no pure-state choice, no
gap, no spectral weights, and executes no confirmatory campaign.

`GROUND_STATE_RESOLVED` never means a certified physical degeneracy:
`NUMERICAL CLUSTER != PHYSICAL DEGENERACY` (unchanged from every prior
precision layer). It means only that the frozen cross-precision protocol
(`precision_control.py`) reached `PRECISION_STABLE` or
`PRECISION_ESCALATED` and that the numerical ground cluster at the
selected level is well-defined and internally consistent with the accepted
eigensystem result.

`PRECISION_UNRESOLVED` propagates directly to
`GROUND_STATE_UNAVAILABLE_PRECISION`: no `P_GS`, no `d_GS`. This is a
fail-closed propagation of an already-established numerical qualification
outcome, never a physical claim (no observed degeneracy, no zero gap).

Contract violations (a `PRECISION_STABLE`/`PRECISION_ESCALATED` result
missing `selected_level_result`, cluster metadata inconsistent with the
accepted eigensystem, no cluster or multiple clusters claiming the minimal
eigenvalue index) FAIL EXPLICITLY rather than being silently reported as
`GROUND_STATE_UNAVAILABLE_PRECISION`: those are software/protocol
inconsistencies, not numerical qualification outcomes.
"""

from __future__ import annotations

from dataclasses import dataclass

import mpmath as mp

from cosmobox_c_model.models.model0b.precision_control import (
    PRECISION_STATUS_ESCALATED,
    PRECISION_STATUS_STABLE,
    PRECISION_STATUS_UNRESOLVED,
    SpectralPrecisionControlResult,
)

GROUND_STATE_STATUS_RESOLVED = "GROUND_STATE_RESOLVED"
GROUND_STATE_STATUS_UNAVAILABLE_PRECISION = "GROUND_STATE_UNAVAILABLE_PRECISION"

_RESOLVABLE_PRECISION_STATUSES = (PRECISION_STATUS_STABLE, PRECISION_STATUS_ESCALATED)


@dataclass(frozen=True)
class GroundStateBranchResult:
    """Canonical numerical ground-state subspace branch.

    `p_gs` is the already-computed cluster projector from the selected
    precision level's accepted eigensystem result, republished unchanged
    (never recomputed, never normalized, never reduced to a single
    eigenvector). `status = GROUND_STATE_RESOLVED` certifies only that the
    frozen cross-precision protocol reached a resolvable precision status
    and that this cluster is well-defined; it is not a certified physical
    degeneracy statement.
    """

    status: str
    source_precision_status: str
    selected_precision_bits: "int | None"
    ground_cluster_indices: "tuple[int, ...] | None"
    d_gs: "int | None"
    p_gs: "mp.matrix | None"


def build_ground_state_branch(
    result: SpectralPrecisionControlResult,
) -> GroundStateBranchResult:
    """Build the canonical ground-state subspace branch from an already
    qualified `precision_control.SpectralPrecisionControlResult`.

    Uses EXCLUSIVELY the numerical cluster partition already present in
    `result.selected_level_result` (`temporal-event-solver.md` Section 16):
    no new clustering, no new epsilon, no ad hoc `abs(E_i-E_0)<tolerance`
    test, no new spectral matching. The minimal-eigenvalue index is
    identified directly from `selected_level_result.eigenvalues`, the
    unique existing cluster containing it is located within
    `selected_level_result.clusters`, and the corresponding
    already-computed projector is republished unchanged from
    `selected_level_result.cluster_projectors`. The independently
    identified cluster/projector/cardinality are cross-checked against the
    convenience `ground_cluster_*` fields already present on the accepted
    eigensystem result; any mismatch is a cluster-metadata inconsistency
    and fails explicitly rather than being reported as a numerical
    unavailability.
    """
    precision_status = result.precision_status

    if precision_status == PRECISION_STATUS_UNRESOLVED:
        return GroundStateBranchResult(
            status=GROUND_STATE_STATUS_UNAVAILABLE_PRECISION,
            source_precision_status=precision_status,
            selected_precision_bits=None,
            ground_cluster_indices=None,
            d_gs=None,
            p_gs=None,
        )

    if precision_status not in _RESOLVABLE_PRECISION_STATUSES:
        raise ValueError(
            f"unrecognized precision_status {precision_status!r}; expected one of "
            f"{PRECISION_STATUS_STABLE!r}, {PRECISION_STATUS_ESCALATED!r}, "
            f"{PRECISION_STATUS_UNRESOLVED!r}"
        )

    selected = result.selected_level_result
    if selected is None:
        raise ValueError(
            f"{precision_status}: selected_level_result must be present; a resolvable "
            "precision status without a selected level result is a protocol "
            "contract violation, not a numerical qualification outcome"
        )

    eigenvalues = selected.eigenvalues
    clusters = selected.clusters
    if not eigenvalues:
        raise ValueError("selected_level_result.eigenvalues must be nonempty")

    min_index = min(range(len(eigenvalues)), key=lambda index: eigenvalues[index])

    matching_positions = [
        position for position, cluster in enumerate(clusters) if min_index in cluster
    ]
    if len(matching_positions) == 0:
        raise ValueError(
            "no cluster in selected_level_result.clusters contains the minimal "
            f"eigenvalue index {min_index}"
        )
    if len(matching_positions) > 1:
        raise ValueError(
            f"multiple clusters {matching_positions} claim to contain the minimal "
            f"eigenvalue index {min_index}; malformed cluster partition"
        )

    cluster_position = matching_positions[0]
    ground_cluster_indices = clusters[cluster_position]

    if cluster_position >= len(selected.cluster_projectors):
        raise ValueError(
            "selected_level_result.cluster_projectors is inconsistent with "
            "selected_level_result.clusters: missing projector for the matched cluster"
        )
    p_gs = selected.cluster_projectors[cluster_position]

    # Cross-check against the already-computed ground-cluster convenience
    # fields on the accepted eigensystem result: any mismatch is a genuine
    # cluster-metadata inconsistency, never a numerical qualification
    # outcome.
    if ground_cluster_indices != selected.ground_cluster_indices:
        raise ValueError(
            "cluster metadata inconsistent with the accepted eigensystem: "
            f"independently identified ground cluster {ground_cluster_indices} does "
            f"not match selected_level_result.ground_cluster_indices "
            f"{selected.ground_cluster_indices}"
        )
    if p_gs != selected.ground_cluster_projector:
        raise ValueError(
            "cluster metadata inconsistent with the accepted eigensystem: "
            "independently identified ground projector does not match "
            "selected_level_result.ground_cluster_projector"
        )

    d_gs = len(ground_cluster_indices)
    if d_gs != selected.ground_cluster_dimension_candidate:
        raise ValueError(
            "cluster metadata inconsistent with the accepted eigensystem: "
            f"d_gs={d_gs} does not match "
            "selected_level_result.ground_cluster_dimension_candidate="
            f"{selected.ground_cluster_dimension_candidate}"
        )

    return GroundStateBranchResult(
        status=GROUND_STATE_STATUS_RESOLVED,
        source_precision_status=precision_status,
        selected_precision_bits=result.selected_precision_bits,
        ground_cluster_indices=ground_cluster_indices,
        d_gs=d_gs,
        p_gs=p_gs,
    )
