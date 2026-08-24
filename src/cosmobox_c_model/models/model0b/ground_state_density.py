"""Toy Model 0B canonical ground-state density: consumes an already built
`ground_state_branch.GroundStateBranchResult` and, when resolved, applies
the frozen unified canonical-state rule
(docs/toy-models/toy0b/specification.md Section 4,
docs/toy-models/toy0b/exact-spectral-response.md Section 3):

    rho_GS = P_GS / Tr(P_GS) = P_GS / d_GS

which covers both the unique (`d_GS=1`, `rho_GS=P_GS`, no eigenvector
selection) and degenerate (`d_GS>1`, uniform mixture over the supplied
subspace) cases through a single formula.

Scope firewall: this module performs NO new spectral computation. It does
not accept a `SpectralPrecisionControlResult`, a Hamiltonian, eigenvalues,
or eigenvectors directly, and never re-invokes I2-B2-B or I2-B2-C. `P_GS`
and `d_GS` are consumed exactly as published by
`ground_state_branch.build_ground_state_branch`; `rho_GS` is built by a
single scalar division, never recomputed from eigenvectors, never
choosing a pure state, and never inferring a physical degeneracy from the
numerical cluster cardinality it is given:
`NUMERICAL_CLUSTER != PHYSICAL_DEGENERACY_CERTIFICATION`.

Precision fidelity: `P_GS` entries are already computed at
`selected_precision_bits` (106 or 212 bits). The scalar division
`P_GS / d_GS` is performed strictly inside
`mp.workprec(selected_precision_bits)`, because mpmath rounds arithmetic
results to whatever working precision is active AT THE TIME of the
operation, not to the precision already carried by the operands:
performing this division outside a matching `workprec` context would
silently truncate `rho_GS` to the ambient default precision (typically 53
bits), discarding the actual precision of the already-accepted `P_GS`.

`GROUND_STATE_UNAVAILABLE_PRECISION` propagates directly to
`CANONICAL_GROUND_STATE_UNAVAILABLE_PRECISION`: no `rho_GS`, no `P_GS`, no
`d_GS`. This is a fail-closed propagation of an already-established
numerical qualification outcome, never a physical claim.

Contract violations (`GROUND_STATE_RESOLVED` with a missing/inconsistent
`p_gs`, `d_gs`, or `ground_cluster_indices`, or an unrecognized status)
FAIL EXPLICITLY rather than being silently reported as unavailable: those
are software/protocol inconsistencies, not numerical qualification
outcomes.
"""

from __future__ import annotations

from dataclasses import dataclass

import mpmath as mp

from cosmobox_c_model.models.model0b.ground_state_branch import (
    GROUND_STATE_STATUS_RESOLVED,
    GROUND_STATE_STATUS_UNAVAILABLE_PRECISION,
    GroundStateBranchResult,
)

CANONICAL_GROUND_STATE_STATUS_RESOLVED = "CANONICAL_GROUND_STATE_RESOLVED"
CANONICAL_GROUND_STATE_STATUS_UNAVAILABLE_PRECISION = (
    "CANONICAL_GROUND_STATE_UNAVAILABLE_PRECISION"
)


@dataclass(frozen=True)
class CanonicalGroundStateDensityResult:
    """Canonical ground-state density bundle.

    `rho_gs` is built exactly as `p_gs / d_gs`
    (specification.md Section 4): no pure-state selection, no spectral
    argmin, no new clustering, no new diagonalization, no new p/2p
    matching, no recomputation of `p_gs`. `status =
    CANONICAL_GROUND_STATE_RESOLVED` never certifies a physical
    degeneracy: it certifies only that the already-accepted ground
    numerical cluster was internally consistent and that the frozen
    unified density rule was applied to it.
    """

    status: str
    source_ground_state_status: str
    selected_precision_bits: "int | None"
    ground_cluster_indices: "tuple[int, ...] | None"
    d_gs: "int | None"
    p_gs: "mp.matrix | None"
    rho_gs: "mp.matrix | None"


def build_canonical_ground_state_density(
    branch: GroundStateBranchResult,
) -> CanonicalGroundStateDensityResult:
    """Apply the frozen unified canonical-state rule `rho_GS = P_GS/d_GS`
    (specification.md Section 4, exact-spectral-response.md Section 3) to
    an already built `GroundStateBranchResult`. Performs no new spectral
    computation: consumes `p_gs`/`d_gs`/`ground_cluster_indices` exactly as
    published."""
    status = branch.status

    if status == GROUND_STATE_STATUS_UNAVAILABLE_PRECISION:
        return CanonicalGroundStateDensityResult(
            status=CANONICAL_GROUND_STATE_STATUS_UNAVAILABLE_PRECISION,
            source_ground_state_status=status,
            selected_precision_bits=None,
            ground_cluster_indices=None,
            d_gs=None,
            p_gs=None,
            rho_gs=None,
        )

    if status != GROUND_STATE_STATUS_RESOLVED:
        raise ValueError(
            f"unrecognized GroundStateBranchResult.status {status!r}; expected one of "
            f"{GROUND_STATE_STATUS_RESOLVED!r}, "
            f"{GROUND_STATE_STATUS_UNAVAILABLE_PRECISION!r}"
        )

    p_gs = branch.p_gs
    d_gs = branch.d_gs
    ground_cluster_indices = branch.ground_cluster_indices
    selected_precision_bits = branch.selected_precision_bits

    if p_gs is None:
        raise ValueError(f"{status}: p_gs must not be None")
    if d_gs is None:
        raise ValueError(f"{status}: d_gs must not be None")
    if ground_cluster_indices is None:
        raise ValueError(f"{status}: ground_cluster_indices must not be None")
    if selected_precision_bits is None:
        raise ValueError(f"{status}: selected_precision_bits must not be None")
    if d_gs <= 0:
        raise ValueError(f"{status}: d_gs must be > 0, got {d_gs}")
    if d_gs != len(ground_cluster_indices):
        raise ValueError(
            f"{status}: d_gs={d_gs} does not match "
            f"len(ground_cluster_indices)={len(ground_cluster_indices)}"
        )

    # rho_GS = P_GS / Tr(P_GS) = P_GS / d_GS. Performed strictly inside the
    # precision context that produced p_gs, to avoid silently rounding an
    # already-high-precision projector down to the ambient default
    # precision.
    with mp.workprec(selected_precision_bits):
        rho_gs = p_gs / d_gs

    return CanonicalGroundStateDensityResult(
        status=CANONICAL_GROUND_STATE_STATUS_RESOLVED,
        source_ground_state_status=status,
        selected_precision_bits=selected_precision_bits,
        ground_cluster_indices=ground_cluster_indices,
        d_gs=d_gs,
        p_gs=p_gs,
        rho_gs=rho_gs,
    )
