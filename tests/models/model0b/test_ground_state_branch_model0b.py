"""Tests for the Toy Model 0B canonical ground-state subspace
(`ground_state_branch.py`): consumes an already qualified
`precision_control.SpectralPrecisionControlResult` and republishes the
existing ground numerical cluster's index set, cardinality, and projector,
with no new clustering, diagonalization, or precision control.

NUMERICAL CLUSTER != PHYSICAL DEGENERACY: `GROUND_STATE_RESOLVED` never
means a certified physical degeneracy; `GROUND_STATE_UNAVAILABLE_PRECISION`
is a fail-closed propagation of an already-established numerical
qualification outcome, never a physical claim."""

from __future__ import annotations

import dataclasses

import mpmath as mp
import pytest

from cosmobox_c_model.models.model0b import ground_state_branch as gsb
from cosmobox_c_model.models.model0b import multiprecision as mpe
from cosmobox_c_model.models.model0b import precision_control as pc


# --- Frozen status constants -----------------------------------------------------


def test_ground_state_status_values():
    assert gsb.GROUND_STATE_STATUS_RESOLVED == "GROUND_STATE_RESOLVED"
    assert gsb.GROUND_STATE_STATUS_UNAVAILABLE_PRECISION == "GROUND_STATE_UNAVAILABLE_PRECISION"


# --- Synthetic helpers -------------------------------------------------------------


def _mp_matrix_from_complex(entries, bits):
    with mp.workprec(bits):
        dimension = len(entries)
        matrix = mp.matrix(dimension, dimension)
        for i in range(dimension):
            for j in range(dimension):
                matrix[i, j] = mp.mpc(entries[i][j])
        return matrix


def _synthetic_selected_result(entries, bits):
    matrix = _mp_matrix_from_complex(entries, bits)
    with mp.workprec(bits):
        return mpe._analyze_mp_hermitian_matrix(matrix, precision_bits=bits)


def _wrap_stable(selected_level_result, bits):
    return pc.SpectralPrecisionControlResult(
        p0_result=None,
        p1_result=selected_level_result,
        p0_p1_comparison=None,
        p2_result=None,
        p1_p2_comparison=None,
        precision_status=pc.PRECISION_STATUS_STABLE,
        selected_precision_bits=bits,
        selected_level_result=selected_level_result,
    )


def _transform_eigenvectors(base_result, new_eigenvectors, bits):
    """Build a new MPEigensystemResult with the SAME eigenvalues/clusters as
    `base_result` but with `new_eigenvectors`, recomputing only
    `cluster_projectors`/`ground_cluster_projector`/`ground_density_candidate`
    consistently via the already-tested private backend helper
    `multiprecision._cluster_projector_mp` -- never a new diagonalization."""
    with mp.workprec(bits):
        dimension = new_eigenvectors.rows
        new_cluster_projectors = tuple(
            mpe._cluster_projector_mp(new_eigenvectors, cluster, dimension)
            for cluster in base_result.clusters
        )
        ground_projector = new_cluster_projectors[base_result.ground_cluster_index]
        ground_density = ground_projector / base_result.ground_cluster_dimension_candidate

    return dataclasses.replace(
        base_result,
        eigenvectors=new_eigenvectors,
        cluster_projectors=new_cluster_projectors,
        ground_cluster_projector=ground_projector,
        ground_density_candidate=ground_density,
    )


# --- A. Non-degenerate ground state -------------------------------------------------


def test_nondegenerate_ground_state():
    bits = 106
    base = _synthetic_selected_result([[0, 0, 0], [0, 1, 0], [0, 0, 3]], bits)
    control_result = _wrap_stable(base, bits)

    branch = gsb.build_ground_state_branch(control_result)

    assert branch.status == gsb.GROUND_STATE_STATUS_RESOLVED
    assert branch.source_precision_status == pc.PRECISION_STATUS_STABLE
    assert branch.selected_precision_bits == bits
    assert branch.ground_cluster_indices == (0,)
    assert branch.d_gs == 1

    with mp.workprec(bits):
        expected = _mp_matrix_from_complex([[1, 0, 0], [0, 0, 0], [0, 0, 0]], bits)
        assert branch.p_gs == expected


# --- B. Degenerate ground state ----------------------------------------------------


def test_degenerate_ground_state():
    bits = 106
    base = _synthetic_selected_result([[0, 0, 0], [0, 0, 0], [0, 0, 2]], bits)
    control_result = _wrap_stable(base, bits)

    branch = gsb.build_ground_state_branch(control_result)

    assert branch.status == gsb.GROUND_STATE_STATUS_RESOLVED
    assert branch.ground_cluster_indices == (0, 1)
    assert branch.d_gs == 2

    with mp.workprec(bits):
        expected = _mp_matrix_from_complex([[1, 0, 0], [0, 1, 0], [0, 0, 0]], bits)
        assert branch.p_gs == expected


# --- C. Phase invariance -------------------------------------------------------------


def test_ground_state_phase_invariance():
    bits = 106
    base = _synthetic_selected_result([[0, 0, 0], [0, 0, 0], [0, 0, 2]], bits)
    reference_branch = gsb.build_ground_state_branch(_wrap_stable(base, bits))

    with mp.workprec(bits):
        thetas = (0.3, -1.2, 2.7)
        phased = mp.matrix(base.eigenvectors.rows, base.eigenvectors.cols)
        for column in range(base.eigenvectors.cols):
            phase = mp.mpc(mp.cos(thetas[column % len(thetas)]), mp.sin(thetas[column % len(thetas)]))
            for row in range(base.eigenvectors.rows):
                phased[row, column] = base.eigenvectors[row, column] * phase

    phased_result = _transform_eigenvectors(base, phased, bits)
    phased_branch = gsb.build_ground_state_branch(_wrap_stable(phased_result, bits))

    assert phased_branch.ground_cluster_indices == reference_branch.ground_cluster_indices
    assert phased_branch.d_gs == reference_branch.d_gs

    with mp.workprec(bits):
        diff = phased_branch.p_gs - reference_branch.p_gs
        max_defect = max(abs(diff[i, j]) for i in range(diff.rows) for j in range(diff.cols))
    assert max_defect <= mp.mpf(2) ** (8 - bits)


# --- D. Internal unitary rotation invariance ----------------------------------------


def test_ground_state_internal_rotation_invariance():
    bits = 106
    base = _synthetic_selected_result([[0, 0, 0], [0, 0, 0], [0, 0, 2]], bits)
    reference_branch = gsb.build_ground_state_branch(_wrap_stable(base, bits))

    with mp.workprec(bits):
        # Nontrivial unitary rotation mixing the two degenerate ground
        # columns (0, 1); column 2 (excited) is left untouched.
        c, s = mp.cos(0.7), mp.sin(0.7)
        rotated = mp.matrix(base.eigenvectors.rows, base.eigenvectors.cols)
        for row in range(base.eigenvectors.rows):
            v0 = base.eigenvectors[row, 0]
            v1 = base.eigenvectors[row, 1]
            rotated[row, 0] = c * v0 - s * v1
            rotated[row, 1] = s * v0 + c * v1
            rotated[row, 2] = base.eigenvectors[row, 2]

    rotated_result = _transform_eigenvectors(base, rotated, bits)
    rotated_branch = gsb.build_ground_state_branch(_wrap_stable(rotated_result, bits))

    assert rotated_branch.ground_cluster_indices == reference_branch.ground_cluster_indices
    assert rotated_branch.d_gs == reference_branch.d_gs

    with mp.workprec(bits):
        diff = rotated_branch.p_gs - reference_branch.p_gs
        max_defect = max(abs(diff[i, j]) for i in range(diff.rows) for j in range(diff.cols))
    assert max_defect <= mp.mpf(2) ** (8 - bits)


# --- E. Permutation of eigenpairs -----------------------------------------------------


def test_ground_state_eigenpair_permutation_invariance():
    bits = 106
    base = _synthetic_selected_result([[0, 0, 0], [0, 1, 0], [0, 0, 3]], bits)
    reference_branch = gsb.build_ground_state_branch(_wrap_stable(base, bits))

    # Consistently permute eigenvalues, eigenvectors, and cluster indices:
    # swap positions 0 and 2 (move the minimal eigenvalue from slot 0 to
    # slot 2).
    permutation = (2, 1, 0)
    with mp.workprec(bits):
        permuted_eigenvalues = tuple(base.eigenvalues[permutation[i]] for i in range(3))
        permuted_eigenvectors = mp.matrix(3, 3)
        for new_col, old_col in enumerate(permutation):
            for row in range(3):
                permuted_eigenvectors[row, new_col] = base.eigenvectors[row, old_col]

    inverse = tuple(permutation.index(i) for i in range(3))
    permuted_clusters = tuple(
        tuple(sorted(inverse[i] for i in cluster)) for cluster in base.clusters
    )

    with mp.workprec(bits):
        permuted_cluster_projectors = tuple(
            mpe._cluster_projector_mp(permuted_eigenvectors, cluster, 3)
            for cluster in permuted_clusters
        )
        ground_projector = permuted_cluster_projectors[base.ground_cluster_index]
        ground_density = ground_projector / base.ground_cluster_dimension_candidate

    permuted_result = dataclasses.replace(
        base,
        eigenvalues=permuted_eigenvalues,
        eigenvectors=permuted_eigenvectors,
        clusters=permuted_clusters,
        cluster_projectors=permuted_cluster_projectors,
        ground_cluster_indices=permuted_clusters[base.ground_cluster_index],
        ground_cluster_projector=ground_projector,
        ground_density_candidate=ground_density,
    )

    permuted_branch = gsb.build_ground_state_branch(_wrap_stable(permuted_result, bits))

    assert permuted_branch.d_gs == reference_branch.d_gs == 1
    assert permuted_branch.ground_cluster_indices == (2,)

    with mp.workprec(bits):
        assert permuted_branch.p_gs == reference_branch.p_gs


# --- F. PRECISION_UNRESOLVED propagation -----------------------------------------


def test_precision_unresolved_propagates_to_unavailable():
    control_result = pc.SpectralPrecisionControlResult(
        p0_result=None,
        p1_result=None,
        p0_p1_comparison=None,
        p2_result=None,
        p1_p2_comparison=None,
        precision_status=pc.PRECISION_STATUS_UNRESOLVED,
        selected_precision_bits=None,
        selected_level_result=None,
    )

    branch = gsb.build_ground_state_branch(control_result)

    assert branch.status == gsb.GROUND_STATE_STATUS_UNAVAILABLE_PRECISION
    assert branch.source_precision_status == pc.PRECISION_STATUS_UNRESOLVED
    assert branch.selected_precision_bits is None
    assert branch.ground_cluster_indices is None
    assert branch.d_gs is None
    assert branch.p_gs is None


# --- G. Contract violations: FAIL EXPLICITLY, never silently unavailable ---------


@pytest.mark.parametrize(
    "precision_status", [pc.PRECISION_STATUS_STABLE, pc.PRECISION_STATUS_ESCALATED]
)
def test_resolvable_status_without_selected_result_fails_explicitly(precision_status):
    control_result = pc.SpectralPrecisionControlResult(
        p0_result=None,
        p1_result=None,
        p0_p1_comparison=None,
        p2_result=None,
        p1_p2_comparison=None,
        precision_status=precision_status,
        selected_precision_bits=106,
        selected_level_result=None,
    )
    with pytest.raises(ValueError):
        gsb.build_ground_state_branch(control_result)


def test_no_cluster_contains_minimal_index_fails_explicitly():
    bits = 106
    base = _synthetic_selected_result([[0, 0, 0], [0, 1, 0], [0, 0, 3]], bits)
    # Malformed: drop the cluster containing index 0 entirely.
    malformed = dataclasses.replace(
        base,
        clusters=tuple(c for c in base.clusters if 0 not in c),
        cluster_projectors=tuple(
            p for c, p in zip(base.clusters, base.cluster_projectors) if 0 not in c
        ),
    )
    with pytest.raises(ValueError):
        gsb.build_ground_state_branch(_wrap_stable(malformed, bits))


def test_multiple_clusters_claim_minimal_index_fails_explicitly():
    bits = 106
    base = _synthetic_selected_result([[0, 0, 0], [0, 1, 0], [0, 0, 3]], bits)
    # Malformed: duplicate a cluster claiming to also contain index 0.
    malformed = dataclasses.replace(
        base,
        clusters=base.clusters + ((0,),),
        cluster_projectors=base.cluster_projectors + (base.cluster_projectors[0],),
    )
    with pytest.raises(ValueError):
        gsb.build_ground_state_branch(_wrap_stable(malformed, bits))


def test_cluster_metadata_inconsistent_with_eigensystem_fails_explicitly():
    bits = 106
    base = _synthetic_selected_result([[0, 0, 0], [0, 1, 0], [0, 0, 3]], bits)
    # Malformed: ground_cluster_indices field disagrees with the actual
    # clusters tuple (independent identification will disagree with it).
    malformed = dataclasses.replace(base, ground_cluster_indices=(1,))
    with pytest.raises(ValueError):
        gsb.build_ground_state_branch(_wrap_stable(malformed, bits))


def test_unrecognized_precision_status_fails_explicitly():
    control_result = pc.SpectralPrecisionControlResult(
        p0_result=None,
        p1_result=None,
        p0_p1_comparison=None,
        p2_result=None,
        p1_p2_comparison=None,
        precision_status="NOT_A_REAL_STATUS",
        selected_precision_bits=None,
        selected_level_result=None,
    )
    with pytest.raises(ValueError):
        gsb.build_ground_state_branch(control_result)


# --- H. No spectral recalculation -------------------------------------------------


def test_no_spectral_recalculation(monkeypatch):
    bits = 106
    base = _synthetic_selected_result([[0, 0, 0], [0, 1, 0], [0, 0, 3]], bits)
    control_result = _wrap_stable(base, bits)

    def _forbidden(*args, **kwargs):
        raise AssertionError("ground_state_branch must never call mp.eighe")

    monkeypatch.setattr(mp, "eighe", _forbidden)

    branch = gsb.build_ground_state_branch(control_result)
    assert branch.status == gsb.GROUND_STATE_STATUS_RESOLVED


# --- I. Real model integration: Lambda=1 (resolved) and Lambda=2 (unresolved) ----


def test_lambda1_real_ground_state_resolved(lambda1_precision_result):
    # Shared PRECISION_STABLE ladder result (PERF-1, conftest.py): never
    # relaunches run_spectral_precision_control here.
    branch = gsb.build_ground_state_branch(lambda1_precision_result)

    assert branch.status == gsb.GROUND_STATE_STATUS_RESOLVED
    assert branch.source_precision_status == pc.PRECISION_STATUS_STABLE
    assert branch.selected_precision_bits == 106
    assert branch.d_gs == 1
    assert branch.ground_cluster_indices == (0,)


def test_lambda2_real_ground_state_unavailable_precision(lambda2_precision_result):
    # Single authoritative Lambda=2 full P0/P1/P2 ladder execution for the
    # session, shared via conftest.py (PERF-1): never recomputed here.
    branch = gsb.build_ground_state_branch(lambda2_precision_result)

    assert branch.status == gsb.GROUND_STATE_STATUS_UNAVAILABLE_PRECISION
    assert branch.source_precision_status == pc.PRECISION_STATUS_UNRESOLVED
    assert branch.selected_precision_bits is None
    assert branch.ground_cluster_indices is None
    assert branch.d_gs is None
    assert branch.p_gs is None
