"""Tests for the Toy Model 0B canonical ground-state density
(`ground_state_density.py`): applies the frozen canonical-state
prescription to an already built
`ground_state_branch.GroundStateBranchResult`, with no new spectral
computation.

NUMERICAL_CLUSTER != PHYSICAL_DEGENERACY_CERTIFICATION:
`CANONICAL_GROUND_STATE_RESOLVED` is only reachable for `d_gs == 1`
(where `rho = |Omega><Omega| = P_GS` exactly) and never certifies a
physical degeneracy. For `d_gs > 1`, this module holds no
structural/exact degeneracy certificate and fails closed as
`CANONICAL_GROUND_STATE_UNAVAILABLE_DEGENERACY_CERTIFICATION` rather than
constructing `rho_gs = p_gs/d_gs` from an uncertified numerical
multiplicity. `CANONICAL_GROUND_STATE_UNAVAILABLE_PRECISION` is a
fail-closed propagation of an already-established numerical qualification
outcome (I2-B2-D-R1)."""

from __future__ import annotations

import dataclasses

import mpmath as mp
import pytest

from cosmobox_c_model.models.model0b import ground_state_branch as gsb
from cosmobox_c_model.models.model0b import ground_state_density as gsd
from cosmobox_c_model.models.model0b import multiprecision as mpe
from cosmobox_c_model.models.model0b import precision_control as pc
from cosmobox_c_model.models.model0b.multiprecision import (
    PROJECTOR_STABILITY_TOLERANCE,
    _fraction_to_mpf_current,
)


# --- Frozen status constants -----------------------------------------------------


def test_canonical_ground_state_status_values():
    assert gsd.CANONICAL_GROUND_STATE_STATUS_RESOLVED == "CANONICAL_GROUND_STATE_RESOLVED"
    assert (
        gsd.CANONICAL_GROUND_STATE_STATUS_UNAVAILABLE_PRECISION
        == "CANONICAL_GROUND_STATE_UNAVAILABLE_PRECISION"
    )
    assert (
        gsd.CANONICAL_GROUND_STATE_STATUS_UNAVAILABLE_DEGENERACY_CERTIFICATION
        == "CANONICAL_GROUND_STATE_UNAVAILABLE_DEGENERACY_CERTIFICATION"
    )


# --- Synthetic helpers -------------------------------------------------------------


def _mp_matrix_from_complex(entries, bits):
    with mp.workprec(bits):
        dimension = len(entries)
        matrix = mp.matrix(dimension, dimension)
        for i in range(dimension):
            for j in range(dimension):
                matrix[i, j] = mp.mpc(entries[i][j])
        return matrix


def _synthetic_eigensystem_result(entries, bits):
    matrix = _mp_matrix_from_complex(entries, bits)
    with mp.workprec(bits):
        return mpe._analyze_mp_hermitian_matrix(matrix, precision_bits=bits)


def _resolved_branch(entries, bits):
    """Build a resolved GroundStateBranchResult directly from a synthetic
    eigensystem (reusing the already-accepted ground_state_branch route via
    a synthetic SpectralPrecisionControlResult wrapper)."""
    eigensystem_result = _synthetic_eigensystem_result(entries, bits)
    control_result = pc.SpectralPrecisionControlResult(
        p0_result=None,
        p1_result=eigensystem_result,
        p0_p1_comparison=None,
        p2_result=None,
        p1_p2_comparison=None,
        precision_status=pc.PRECISION_STATUS_STABLE,
        selected_precision_bits=bits,
        selected_level_result=eigensystem_result,
    )
    return gsb.build_ground_state_branch(control_result)


# --- A. d_GS = 1 ---------------------------------------------------------------------


def test_nondegenerate_canonical_density():
    bits = 106
    branch = _resolved_branch([[0, 0, 0], [0, 1, 0], [0, 0, 3]], bits)

    density = gsd.build_canonical_ground_state_density(branch)

    assert density.status == gsd.CANONICAL_GROUND_STATE_STATUS_RESOLVED
    assert density.source_ground_state_status == gsb.GROUND_STATE_STATUS_RESOLVED
    assert density.selected_precision_bits == bits
    assert density.d_gs == 1
    # rho = |Omega><Omega| = P_GS / 1 = P_GS: republished directly, no
    # arithmetic operation.
    assert density.rho_gs is density.p_gs


# --- B. d_GS = 2 (synthetic): fail-closed, no degeneracy certificate ------------------


def test_degenerate_cluster_fails_closed_on_uncertified_multiplicity():
    bits = 106
    branch = _resolved_branch([[0, 0, 0], [0, 0, 0], [0, 0, 2]], bits)

    density = gsd.build_canonical_ground_state_density(branch)

    assert (
        density.status
        == gsd.CANONICAL_GROUND_STATE_STATUS_UNAVAILABLE_DEGENERACY_CERTIFICATION
    )
    assert density.rho_gs is None
    # Numerical sub-space diagnostics remain available, but are never a
    # degeneracy certification.
    assert density.d_gs == 2
    assert density.ground_cluster_indices == branch.ground_cluster_indices
    assert density.p_gs is branch.p_gs
    assert density.selected_precision_bits == bits


# --- C. Basis invariance (d_gs > 1) -----------------------------------------------------


def test_canonical_density_basis_invariance_degenerate():
    bits = 106
    base = _synthetic_eigensystem_result([[0, 0, 0], [0, 0, 0], [0, 0, 2]], bits)

    with mp.workprec(bits):
        # Unitary rotation mixing the two degenerate ground columns (0, 1);
        # column 2 (excited) is left untouched.
        c, s = mp.cos(0.9), mp.sin(0.9)
        rotated = mp.matrix(base.eigenvectors.rows, base.eigenvectors.cols)
        for row in range(base.eigenvectors.rows):
            v0 = base.eigenvectors[row, 0]
            v1 = base.eigenvectors[row, 1]
            rotated[row, 0] = c * v0 - s * v1
            rotated[row, 1] = s * v0 + c * v1
            rotated[row, 2] = base.eigenvectors[row, 2]

        dimension = rotated.rows
        rotated_cluster_projectors = tuple(
            mpe._cluster_projector_mp(rotated, cluster, dimension) for cluster in base.clusters
        )
        ground_projector = rotated_cluster_projectors[base.ground_cluster_index]
        ground_density = ground_projector / base.ground_cluster_dimension_candidate

    rotated_eigensystem = dataclasses.replace(
        base,
        eigenvectors=rotated,
        cluster_projectors=rotated_cluster_projectors,
        ground_cluster_projector=ground_projector,
        ground_density_candidate=ground_density,
    )

    def _wrap(result):
        control_result = pc.SpectralPrecisionControlResult(
            p0_result=None,
            p1_result=result,
            p0_p1_comparison=None,
            p2_result=None,
            p1_p2_comparison=None,
            precision_status=pc.PRECISION_STATUS_STABLE,
            selected_precision_bits=bits,
            selected_level_result=result,
        )
        return gsb.build_ground_state_branch(control_result)

    reference_density = gsd.build_canonical_ground_state_density(_wrap(base))
    rotated_density = gsd.build_canonical_ground_state_density(_wrap(rotated_eigensystem))

    # Both rotations must fail closed identically: no rho_gs is fabricated
    # for an uncertified d_gs > 1 multiplicity, regardless of the internal
    # eigenvector basis chosen for the numerical cluster.
    assert (
        reference_density.status
        == rotated_density.status
        == gsd.CANONICAL_GROUND_STATE_STATUS_UNAVAILABLE_DEGENERACY_CERTIFICATION
    )
    assert reference_density.rho_gs is None
    assert rotated_density.rho_gs is None
    assert rotated_density.d_gs == reference_density.d_gs

    # The diagnostic projector p_gs itself remains invariant under the
    # internal unitary rotation (already established by
    # ground_state_branch.py's own invariance guarantee).
    with mp.workprec(bits):
        diff = rotated_density.p_gs - reference_density.p_gs
        max_defect = max(abs(diff[i, j]) for i in range(diff.rows) for j in range(diff.cols))
    # Representation-only engineering bound derived from the target
    # precision's own unit roundoff, not a new scientific tolerance.
    assert max_defect <= mp.mpf(2) ** (8 - bits)


# --- D. Fail-closed propagation --------------------------------------------------------


def test_unavailable_precision_propagates():
    branch = gsb.GroundStateBranchResult(
        status=gsb.GROUND_STATE_STATUS_UNAVAILABLE_PRECISION,
        source_precision_status=pc.PRECISION_STATUS_UNRESOLVED,
        selected_precision_bits=None,
        ground_cluster_indices=None,
        d_gs=None,
        p_gs=None,
    )

    density = gsd.build_canonical_ground_state_density(branch)

    assert density.status == gsd.CANONICAL_GROUND_STATE_STATUS_UNAVAILABLE_PRECISION
    assert density.source_ground_state_status == gsb.GROUND_STATE_STATUS_UNAVAILABLE_PRECISION
    assert density.selected_precision_bits is None
    assert density.ground_cluster_indices is None
    assert density.d_gs is None
    assert density.p_gs is None
    assert density.rho_gs is None


# --- E. PRECISION_UNAVAILABLE with an inconsistent field: FAIL EXPLICITLY --------------


def _unavailable_branch_template():
    return gsb.GroundStateBranchResult(
        status=gsb.GROUND_STATE_STATUS_UNAVAILABLE_PRECISION,
        source_precision_status=pc.PRECISION_STATUS_UNRESOLVED,
        selected_precision_bits=None,
        ground_cluster_indices=None,
        d_gs=None,
        p_gs=None,
    )


def test_unavailable_precision_with_stray_selected_precision_bits_fails():
    branch = dataclasses.replace(_unavailable_branch_template(), selected_precision_bits=106)
    with pytest.raises(ValueError):
        gsd.build_canonical_ground_state_density(branch)


def test_unavailable_precision_with_stray_ground_cluster_indices_fails():
    branch = dataclasses.replace(_unavailable_branch_template(), ground_cluster_indices=(0,))
    with pytest.raises(ValueError):
        gsd.build_canonical_ground_state_density(branch)


def test_unavailable_precision_with_stray_d_gs_fails():
    branch = dataclasses.replace(_unavailable_branch_template(), d_gs=1)
    with pytest.raises(ValueError):
        gsd.build_canonical_ground_state_density(branch)


def test_unavailable_precision_with_stray_p_gs_fails():
    stray_p_gs = _mp_matrix_from_complex([[1]], 106)
    branch = dataclasses.replace(_unavailable_branch_template(), p_gs=stray_p_gs)
    with pytest.raises(ValueError):
        gsd.build_canonical_ground_state_density(branch)


# --- F. GROUND_STATE_RESOLVED contract violations: FAIL EXPLICITLY --------------------


def _resolved_branch_template(bits=106):
    reference = _resolved_branch([[0, 0, 0], [0, 1, 0], [0, 0, 3]], bits)
    return reference


def test_resolved_with_none_p_gs_fails():
    branch = dataclasses.replace(_resolved_branch_template(), p_gs=None)
    with pytest.raises(ValueError):
        gsd.build_canonical_ground_state_density(branch)


def test_resolved_with_none_d_gs_fails():
    branch = dataclasses.replace(_resolved_branch_template(), d_gs=None)
    with pytest.raises(ValueError):
        gsd.build_canonical_ground_state_density(branch)


def test_resolved_with_none_indices_fails():
    branch = dataclasses.replace(_resolved_branch_template(), ground_cluster_indices=None)
    with pytest.raises(ValueError):
        gsd.build_canonical_ground_state_density(branch)


def test_resolved_with_none_selected_precision_bits_fails():
    branch = dataclasses.replace(_resolved_branch_template(), selected_precision_bits=None)
    with pytest.raises(ValueError):
        gsd.build_canonical_ground_state_density(branch)


@pytest.mark.parametrize("bad_d_gs", [0, -1, -5])
def test_resolved_with_non_positive_d_gs_fails(bad_d_gs):
    branch = dataclasses.replace(_resolved_branch_template(), d_gs=bad_d_gs)
    with pytest.raises(ValueError):
        gsd.build_canonical_ground_state_density(branch)


def test_resolved_with_d_gs_mismatched_to_indices_fails():
    branch = dataclasses.replace(_resolved_branch_template(), d_gs=2)
    with pytest.raises(ValueError):
        gsd.build_canonical_ground_state_density(branch)


def test_unrecognized_status_fails():
    branch = dataclasses.replace(_resolved_branch_template(), status="NOT_A_REAL_STATUS")
    with pytest.raises(ValueError):
        gsd.build_canonical_ground_state_density(branch)


# --- G. No new spectral computation -----------------------------------------------------


def test_no_spectral_recalculation(monkeypatch):
    branch = _resolved_branch_template()

    def _forbidden_eighe(*args, **kwargs):
        raise AssertionError("ground_state_density must never call mp.eighe")

    def _forbidden_run_spectral_precision_control(*args, **kwargs):
        raise AssertionError("ground_state_density must never call run_spectral_precision_control")

    def _forbidden_build_ground_state_branch(*args, **kwargs):
        raise AssertionError("ground_state_density must never call build_ground_state_branch")

    monkeypatch.setattr(mp, "eighe", _forbidden_eighe)
    monkeypatch.setattr(
        pc, "run_spectral_precision_control", _forbidden_run_spectral_precision_control
    )
    monkeypatch.setattr(gsb, "build_ground_state_branch", _forbidden_build_ground_state_branch)

    density = gsd.build_canonical_ground_state_density(branch)
    assert density.status == gsd.CANONICAL_GROUND_STATE_STATUS_RESOLVED


# --- H-I. Real model integration: I2-B2-B -> I2-B2-C -> I2-B2-D --------------------------


def test_lambda1_real_canonical_ground_state_resolved(lambda1_precision_result):
    # Shared PRECISION_STABLE ladder result (PERF-1, conftest.py): never
    # relaunches the ladder here.
    branch = gsb.build_ground_state_branch(lambda1_precision_result)
    density = gsd.build_canonical_ground_state_density(branch)

    assert density.status == gsd.CANONICAL_GROUND_STATE_STATUS_RESOLVED
    assert density.d_gs == 1
    assert density.rho_gs is density.p_gs
    with mp.workprec(density.selected_precision_bits):
        trace = sum(density.rho_gs[i, i] for i in range(density.rho_gs.rows))
        # The real (non-synthetic) eigensystem carries its own already
        # -accepted backward-error residual (I2-B2-A/I2-B2-B); trace(rho_gs)
        # is therefore exact only up to that already-established
        # PROJECTOR_STABILITY_TOLERANCE scale, not bit-exact.
        tolerance = _fraction_to_mpf_current(PROJECTOR_STABILITY_TOLERANCE)
        assert abs(trace - mp.mpf(1)) <= tolerance


def test_lambda2_real_canonical_ground_state_unavailable(lambda2_precision_result):
    # Single authoritative Lambda=2 full P0/P1/P2 ladder execution for the
    # session, shared via conftest.py (PERF-1): never recomputed here.
    branch = gsb.build_ground_state_branch(lambda2_precision_result)
    density = gsd.build_canonical_ground_state_density(branch)

    assert density.status == gsd.CANONICAL_GROUND_STATE_STATUS_UNAVAILABLE_PRECISION
    assert density.rho_gs is None
    assert density.p_gs is None
    assert density.d_gs is None
    assert density.selected_precision_bits is None
