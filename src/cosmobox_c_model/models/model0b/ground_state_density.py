"""Toy Model 0B canonical ground-state density: consumes an already built
`ground_state_branch.GroundStateBranchResult` and applies the frozen
canonical-state prescription
(docs/toy-models/toy0b/specification.md Section 4,
docs/toy-models/toy0b/exact-spectral-response.md Section 3):

    unique ground state:     rho = |Omega><Omega|
    degenerate ground state: rho = P_GS / Tr(P_GS)

Fail-closed multiplicity qualification (I2-B2-D-R1): the frozen protocol
distinguishes an EXACT/physical ground-state degeneracy from a numerical
spectral cluster (`NUMERICAL_CLUSTER != PHYSICAL_DEGENERACY`; a generic
zero tolerance never creates ground-state degeneracy by itself). The
`d_gs`/`p_gs` published by `ground_state_branch.py` are the cardinality
and projector of a numerically qualified spectral cluster, not a
certificate that the ground state is exactly/physically degenerate.
Therefore:

- `d_gs == 1`: the numerical ground cluster is unidimensional, so the two
  branches of the frozen prescription coincide exactly
  (`rho = |Omega><Omega| = P_GS / 1 = P_GS`): this module republishes
  `p_gs` directly as `rho_gs`, with no eigenvector selection and no
  arithmetic operation.
- `d_gs > 1`: this module holds no structural/exact certificate that the
  cluster's multiplicity is a physical degeneracy (that certificate is
  explicitly out of scope for this lot and is deferred to a future
  dedicated layer). It therefore does NOT construct or publish
  `rho_gs = p_gs/d_gs` as a resolved canonical state: it returns a
  distinct fail-closed status,
  `CANONICAL_GROUND_STATE_UNAVAILABLE_DEGENERACY_CERTIFICATION`, with
  `rho_gs = None`, while still republishing `p_gs`/`d_gs`/
  `ground_cluster_indices`/`selected_precision_bits` as numerical
  sub-space diagnostics/provenance -- never as a degeneracy certification.

Scope firewall: this module performs NO new spectral computation. It does
not accept a `SpectralPrecisionControlResult`, a Hamiltonian, eigenvalues,
or eigenvectors directly, and never re-invokes I2-B2-B or I2-B2-C. `P_GS`
and `d_GS` are consumed exactly as published by
`ground_state_branch.build_ground_state_branch`; this module never infers
a physical degeneracy from the numerical cluster cardinality it is given,
never treats a numerically-zero-compatible gap as an exact degeneracy, and
never uses a generic tolerance to authorize a uniform mixture.

Precision fidelity: `P_GS` entries are already computed at
`selected_precision_bits` (106 or 212 bits). Any future arithmetic
operation on a high-precision mpmath projector must be performed strictly
inside `mp.workprec(selected_precision_bits)`, because mpmath rounds
arithmetic results to whatever working precision is active AT THE TIME of
the operation, not to the precision already carried by the operands:
performing such an operation outside a matching `workprec` context would
silently truncate the result to the ambient default precision (typically
53 bits), discarding the actual precision of the already-accepted `P_GS`.
This is not a new scientific tolerance; it is a representation-fidelity
requirement. In the currently authorized `d_gs == 1` route, `p_gs` is
republished directly with no arithmetic operation at all.

`GROUND_STATE_UNAVAILABLE_PRECISION` propagates directly to
`CANONICAL_GROUND_STATE_UNAVAILABLE_PRECISION`: no `rho_GS`, no `P_GS`, no
`d_GS`. This is a fail-closed propagation of an already-established
numerical qualification outcome, never a physical claim. An incoming
`GROUND_STATE_UNAVAILABLE_PRECISION` branch whose other fields are not
also `None` is itself a contract violation and fails explicitly rather
than being silently normalized.

Contract violations (`GROUND_STATE_RESOLVED` with a missing/inconsistent
`p_gs`, `d_gs`, `ground_cluster_indices`, or `selected_precision_bits`, or
an unrecognized status) FAIL EXPLICITLY rather than being silently
reported as unavailable: those are software/protocol inconsistencies, not
numerical qualification outcomes.
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
CANONICAL_GROUND_STATE_STATUS_UNAVAILABLE_DEGENERACY_CERTIFICATION = (
    "CANONICAL_GROUND_STATE_UNAVAILABLE_DEGENERACY_CERTIFICATION"
)


@dataclass(frozen=True)
class CanonicalGroundStateDensityResult:
    """Canonical ground-state density bundle.

    For `status = CANONICAL_GROUND_STATE_RESOLVED` (only reachable when
    `d_gs == 1`), `rho_gs` is `p_gs` republished directly: no pure-state
    selection beyond what the unidimensional numerical cluster already
    fixes, no spectral argmin, no new clustering, no new diagonalization,
    no new p/2p matching, no recomputation of `p_gs`.

    For `status = CANONICAL_GROUND_STATE_UNAVAILABLE_DEGENERACY_CERTIFICATION`
    (`d_gs > 1`), `rho_gs` is `None`: `p_gs`/`d_gs`/`ground_cluster_indices`
    remain available as numerical sub-space diagnostics only, never as a
    physical degeneracy certification.

    `status = CANONICAL_GROUND_STATE_RESOLVED` never certifies a physical
    degeneracy: it certifies only that the already-accepted, unidimensional
    ground numerical cluster was internally consistent and that the frozen
    canonical-state prescription was applied to it.
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
    """Apply the frozen canonical-state prescription
    (specification.md Section 4, exact-spectral-response.md Section 3) to
    an already built `GroundStateBranchResult`. Performs no new spectral
    computation: consumes `p_gs`/`d_gs`/`ground_cluster_indices` exactly as
    published.

    `d_gs == 1` republishes `p_gs` as `rho_gs` directly (the unique- and
    degenerate-branch prescriptions coincide exactly for a unidimensional
    numerical cluster). `d_gs > 1` fails closed as
    `CANONICAL_GROUND_STATE_UNAVAILABLE_DEGENERACY_CERTIFICATION`: a
    numerical cluster of cardinality > 1 is not, by itself, a
    structural/exact certificate of physical ground-state degeneracy
    (`NUMERICAL_CLUSTER != PHYSICAL_DEGENERACY`)."""
    status = branch.status

    if status == GROUND_STATE_STATUS_UNAVAILABLE_PRECISION:
        if (
            branch.selected_precision_bits is not None
            or branch.ground_cluster_indices is not None
            or branch.d_gs is not None
            or branch.p_gs is not None
        ):
            raise ValueError(
                f"{status}: selected_precision_bits, ground_cluster_indices, d_gs, "
                "and p_gs must all be None for this status; a resolvable-looking "
                "field alongside GROUND_STATE_UNAVAILABLE_PRECISION is a protocol "
                "contract violation, not a numerical qualification outcome"
            )
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

    if d_gs > 1:
        # No structural/exact certificate of physical degeneracy is
        # available at this layer: fail closed rather than construct a
        # uniform mixture from an uncertified numerical multiplicity.
        return CanonicalGroundStateDensityResult(
            status=CANONICAL_GROUND_STATE_STATUS_UNAVAILABLE_DEGENERACY_CERTIFICATION,
            source_ground_state_status=status,
            selected_precision_bits=selected_precision_bits,
            ground_cluster_indices=ground_cluster_indices,
            d_gs=d_gs,
            p_gs=p_gs,
            rho_gs=None,
        )

    # d_gs == 1: rho = |Omega><Omega| = P_GS / 1 = P_GS. Republished
    # directly, with no arithmetic operation.
    rho_gs = p_gs

    return CanonicalGroundStateDensityResult(
        status=CANONICAL_GROUND_STATE_STATUS_RESOLVED,
        source_ground_state_status=status,
        selected_precision_bits=selected_precision_bits,
        ground_cluster_indices=ground_cluster_indices,
        d_gs=d_gs,
        p_gs=p_gs,
        rho_gs=rho_gs,
    )
