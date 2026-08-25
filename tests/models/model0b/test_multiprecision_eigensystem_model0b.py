"""Tests for the Toy Model 0B single-level high-precision (P1/P2)
eigensystem layer: direct H^(p) reassembly, backward gate, and numerical
clustering (docs/toy-models/toy0b/temporal-event-solver.md Sections 15-17).

NUMERICAL CLUSTER != PHYSICAL DEGENERACY: no cross-precision comparison,
`d_P`, or precision-stability verdict is exercised here."""

from __future__ import annotations

from fractions import Fraction

import mpmath as mp
import pytest

from cosmobox_c_model.models.model0b import multiprecision as mpe
from cosmobox_c_model.models.model0b.basis_config import build_physical_basis
from cosmobox_c_model.models.model0b.exact_assembly import (
    P1_BITS,
    P2_BITS,
    build_exact_discrete_components,
)

PRECISIONS = (P1_BITS, P2_BITS)


def _mp_matrix_from_complex(entries, bits):
    with mp.workprec(bits):
        dimension = len(entries)
        matrix = mp.matrix(dimension, dimension)
        for i in range(dimension):
            for j in range(dimension):
                matrix[i, j] = mp.mpc(entries[i][j])
        return matrix


def _is_exactly_hermitian(matrix) -> bool:
    """Exact (no tolerance, no `almosteq`, no symmetrization) Hermiticity
    check on the matrix representation actually supplied. Test-side helper
    gating only; never used to modify the matrix (PERF-3)."""
    dimension = matrix.rows
    if matrix.cols != dimension:
        return False
    for i in range(dimension):
        for j in range(dimension):
            if matrix[i, j] != matrix[j, i].conjugate():
                return False
    return True


def _spectral_norm(matrix, bits):
    """`||matrix||_2`. Mathematically identical in every case to the
    unconditional `sqrt(lambda_max(A^dagger A))` route, but takes a faster
    Hermitian fast path (`max_i |lambda_i(A)|`, a single `mp.eighe(A)`
    call) when `matrix` is verified EXACTLY Hermitian in its current
    mpmath representation (PERF-3 test-side optimization, mirroring the
    accepted `precision_control._projector_difference_spectral_norm`
    kernel)."""
    with mp.workprec(bits):
        if _is_exactly_hermitian(matrix):
            eigs = mp.eighe(matrix, eigvals_only=True)
            return max(abs(eigs[i]) for i in range(matrix.rows))
        product = matrix.transpose_conj() * matrix
        eigs = mp.eighe(product, eigvals_only=True)
        top = max(eigs[i].real for i in range(matrix.cols))
        return mp.sqrt(max(top, mp.mpf(0)))


def _frac_matmul(a, b):
    n, m, p = len(a), len(b), len(b[0])
    return [[sum(a[i][k] * b[k][j] for k in range(m)) for j in range(p)] for i in range(n)]


def _frac_transpose(a):
    return [list(row) for row in zip(*a)]


def _frac_to_mp_matrix(matrix_of_fractions, bits):
    with mp.workprec(bits):
        dimension = len(matrix_of_fractions)
        out = mp.matrix(dimension, dimension)
        for i in range(dimension):
            for j in range(dimension):
                fraction = matrix_of_fractions[i][j]
                out[i, j] = mp.mpc(mp.mpf(fraction.numerator) / mp.mpf(fraction.denominator))
        return out


# --- Frozen constants -----------------------------------------------------------


def test_mp_allowed_precision_bits():
    assert mpe.MP_ALLOWED_PRECISION_BITS == (106, 212)


def test_backward_tolerances_canonical_exact_fraction():
    # Canonical representation is exact Fraction, never an import-time mpf.
    assert mpe.BACKWARD_RESIDUAL_TOLERANCE == Fraction(1, 10**12)
    assert mpe.BACKWARD_ORTHOGONALITY_TOLERANCE == Fraction(1, 10**12)
    assert isinstance(mpe.BACKWARD_RESIDUAL_TOLERANCE, Fraction)
    assert isinstance(mpe.BACKWARD_ORTHOGONALITY_TOLERANCE, Fraction)


def test_projector_stability_tolerance_canonical_exact_fraction():
    assert mpe.PROJECTOR_STABILITY_TOLERANCE == Fraction(1, 10**10)
    assert isinstance(mpe.PROJECTOR_STABILITY_TOLERANCE, Fraction)


# --- 5. Threshold precision-local materialization regression --------------------


@pytest.mark.parametrize("bits", PRECISIONS)
def test_threshold_materialized_at_active_precision(bits):
    with mp.workprec(bits):
        expected_1e12 = mp.mpf(1) / mp.mpf(10**12)
        expected_1e10 = mp.mpf(1) / mp.mpf(10**10)

        residual_mp = mpe._fraction_to_mpf_current(mpe.BACKWARD_RESIDUAL_TOLERANCE)
        orthogonality_mp = mpe._fraction_to_mpf_current(mpe.BACKWARD_ORTHOGONALITY_TOLERANCE)
        projector_mp = mpe._fraction_to_mpf_current(mpe.PROJECTOR_STABILITY_TOLERANCE)

        assert residual_mp == expected_1e12
        assert orthogonality_mp == expected_1e12
        assert projector_mp == expected_1e10


# --- 6. Boundary-sensitive gate regression ---------------------------------------


def test_boundary_sensitive_threshold_distinguishes_stale_vs_fresh_precision():
    # Reproduce the exact defect identified in review: an mp.mpf constructed
    # at 53-bit (import-time-like) precision differs from the correctly
    # rounded 212-bit value by ~2e-29. Construct a probe value strictly
    # between the two and verify the P2-local frozen threshold gives the
    # mathematically correct (stricter) verdict, while the stale 53-bit
    # approximation would have given the wrong one.
    stale_53bit_threshold = mp.mpf("1e-12")  # constructed at default (53-bit) precision

    with mp.workprec(212):
        fresh_212bit_threshold = mpe._fraction_to_mpf_current(mpe.BACKWARD_RESIDUAL_TOLERANCE)

        assert stale_53bit_threshold != fresh_212bit_threshold

        # A probe strictly between the two thresholds.
        probe = (stale_53bit_threshold + fresh_212bit_threshold) / 2
        assert stale_53bit_threshold != fresh_212bit_threshold
        assert min(stale_53bit_threshold, fresh_212bit_threshold) < probe
        assert probe < max(stale_53bit_threshold, fresh_212bit_threshold)

        # The correct (precision-local, frozen) verdict.
        correct_verdict = probe <= fresh_212bit_threshold
        # The verdict the old import-time-rounded constant would have given.
        stale_verdict = probe <= stale_53bit_threshold

        assert correct_verdict != stale_verdict


# --- PERF-3: test-side spectral norm helper Hermitian fast-path equivalence -----


def test_spectral_norm_helper_hermitian_fast_path_equivalence():
    bits = 106
    hermitian = _mp_matrix_from_complex([[1, 2 + 3j], [2 - 3j, 4]], bits)
    non_hermitian = _mp_matrix_from_complex([[1, 2], [0, 3]], bits)

    with mp.workprec(bits):
        assert _is_exactly_hermitian(hermitian) is True
        assert _is_exactly_hermitian(non_hermitian) is False

        # Fast path vs the unconditional general definition computed inline
        # (never via the helper under test itself).
        fast = _spectral_norm(hermitian, bits)
        product = hermitian.transpose_conj() * hermitian
        eigs = mp.eighe(product, eigvals_only=True)
        general = mp.sqrt(max(eigs[i].real for i in range(hermitian.rows)))
        # Representation-only bound derived from the target precision's own
        # unit roundoff, not a new scientific tolerance and far stricter
        # than any frozen scientific tolerance.
        assert abs(fast - general) <= mp.mpf(2) ** (8 - bits)

        # Non-Hermitian input takes the fallback route exactly: identical
        # call, bit-identical result.
        fast_nh = _spectral_norm(non_hermitian, bits)
        product_nh = non_hermitian.transpose_conj() * non_hermitian
        eigs_nh = mp.eighe(product_nh, eigvals_only=True)
        general_nh = mp.sqrt(max(eigs_nh[i].real for i in range(non_hermitian.rows)))
        assert fast_nh == general_nh


def test_precision_level_status_values():
    assert mpe.PRECISION_LEVEL_STATUS_P1 == "P1_ANALYZED_NOT_CROSS_PRECISION_CERTIFIED"
    assert mpe.PRECISION_LEVEL_STATUS_P2 == "P2_ANALYZED_NOT_CROSS_PRECISION_CERTIFIED"


# --- A. Diagonal distinct (synthetic, backend-private) --------------------------


@pytest.mark.parametrize("bits", PRECISIONS)
def test_synthetic_diagonal_distinct(bits):
    matrix = _mp_matrix_from_complex([[0, 0, 0], [0, 1, 0], [0, 0, 3]], bits)
    with mp.workprec(bits):
        result = mpe._analyze_mp_hermitian_matrix(matrix, precision_bits=bits)

    assert result.clusters == ((0,), (1,), (2,))
    assert result.ground_cluster_dimension_candidate == 1
    assert result.ground_to_next_cluster_separation_candidate == 1
    assert result.backward_gate_pass is True
    assert result.precision_level_status == (
        mpe.PRECISION_LEVEL_STATUS_P1 if bits == P1_BITS else mpe.PRECISION_LEVEL_STATUS_P2
    )


# --- B. Exact degenerate diagonal ------------------------------------------------


@pytest.mark.parametrize("bits", PRECISIONS)
def test_synthetic_exact_degenerate_diagonal(bits):
    matrix = _mp_matrix_from_complex([[0, 0, 0], [0, 0, 0], [0, 0, 2]], bits)
    with mp.workprec(bits):
        result = mpe._analyze_mp_hermitian_matrix(matrix, precision_bits=bits)

        assert result.clusters[0] == (0, 1)
        assert result.ground_cluster_dimension_candidate == 2

        expected_projector = _mp_matrix_from_complex(
            [[1, 0, 0], [0, 1, 0], [0, 0, 0]], bits
        )
        expected_rho = _mp_matrix_from_complex(
            [[0.5, 0, 0], [0, 0.5, 0], [0, 0, 0]], bits
        )
        assert result.ground_cluster_projector == expected_projector
        assert result.ground_density_candidate == expected_rho
        assert result.ground_to_next_cluster_separation_candidate == 2


# --- C. Full zero matrix ----------------------------------------------------------


@pytest.mark.parametrize("bits", PRECISIONS)
@pytest.mark.parametrize("dimension", [2, 3, 5])
def test_synthetic_full_zero_matrix(bits, dimension):
    matrix = mp.matrix(dimension, dimension)
    with mp.workprec(bits):
        result = mpe._analyze_mp_hermitian_matrix(matrix, precision_bits=bits)

        assert len(result.clusters) == 1
        assert result.ground_cluster_dimension_candidate == dimension
        assert result.ground_to_next_cluster_separation_candidate is None

        expected_rho = mp.eye(dimension) / dimension
        assert result.ground_density_candidate == expected_rho


# --- D. Rotated exact degenerate Hermitian matrix ---------------------------------


@pytest.mark.parametrize("bits", PRECISIONS)
def test_synthetic_rotated_degenerate_projector_invariance(bits):
    # Exact rational orthogonal rotation composed from two Pythagorean
    # (3,4,5) and (5,12,13) Givens-like rotations, mixing all three
    # coordinates -- not block-preserving, so the raw eigenvectors returned
    # by the solver for the degenerate subspace are not axis-aligned.
    c1, s1 = Fraction(3, 5), Fraction(4, 5)
    r1 = [[c1, -s1, Fraction(0)], [s1, c1, Fraction(0)], [Fraction(0), Fraction(0), Fraction(1)]]
    c2, s2 = Fraction(5, 13), Fraction(12, 13)
    r2 = [[Fraction(1), Fraction(0), Fraction(0)], [Fraction(0), c2, -s2], [Fraction(0), s2, c2]]
    q = _frac_matmul(r2, r1)
    qt = _frac_transpose(q)

    d_matrix = [
        [Fraction(0), Fraction(0), Fraction(0)],
        [Fraction(0), Fraction(0), Fraction(0)],
        [Fraction(0), Fraction(0), Fraction(2)],
    ]
    m_matrix = _frac_matmul(_frac_matmul(q, d_matrix), qt)

    p_axis = [
        [Fraction(1), Fraction(0), Fraction(0)],
        [Fraction(0), Fraction(1), Fraction(0)],
        [Fraction(0), Fraction(0), Fraction(0)],
    ]
    p_expected = _frac_matmul(_frac_matmul(q, p_axis), qt)

    m_mp = _frac_to_mp_matrix(m_matrix, bits)
    p_expected_mp = _frac_to_mp_matrix(p_expected, bits)

    with mp.workprec(bits):
        result = mpe._analyze_mp_hermitian_matrix(m_mp, precision_bits=bits)
        projector_tol = mpe._fraction_to_mpf_current(mpe.PROJECTOR_STABILITY_TOLERANCE)

        assert result.clusters[0] == (0, 1)
        assert result.ground_cluster_dimension_candidate == 2
        assert result.ground_to_next_cluster_separation_candidate == 2

        # Only the basis-invariant projector is checked -- never a specific
        # eigenvector inside the degenerate subspace.
        diff = result.ground_cluster_projector - p_expected_mp
        assert _spectral_norm(diff, bits) <= projector_tol


# --- Backward gate on synthetic matrices ------------------------------------------


@pytest.mark.parametrize("bits", PRECISIONS)
@pytest.mark.parametrize(
    "entries",
    [
        [[0, 0, 0], [0, 1, 0], [0, 0, 3]],
        [[0, 0, 0], [0, 0, 0], [0, 0, 2]],
        [[2, 1], [1, 2]],
        [[0, 1j], [-1j, 0]],
    ],
)
def test_backward_gate_synthetic(entries, bits):
    matrix = _mp_matrix_from_complex(entries, bits)
    with mp.workprec(bits):
        result = mpe._analyze_mp_hermitian_matrix(matrix, precision_bits=bits)
        residual_tol = mpe._fraction_to_mpf_current(mpe.BACKWARD_RESIDUAL_TOLERANCE)
        orthogonality_tol = mpe._fraction_to_mpf_current(mpe.BACKWARD_ORTHOGONALITY_TOLERANCE)

        assert result.residual_ratio <= residual_tol
        assert result.orthogonality_defect <= orthogonality_tol
        assert result.backward_gate_pass is True
        assert result.backward_gate_status == mpe.BACKWARD_GATE_STATUS_PASS

        expected_epsilon = result.hamiltonian_scale * (
            result.residual_ratio + result.orthogonality_defect
        )
        assert result.epsilon_h == expected_epsilon


# --- Projector properties (engineering validation, not d_P) ----------------------


@pytest.mark.parametrize("bits", PRECISIONS)
@pytest.mark.parametrize(
    "entries",
    [
        [[0, 0, 0], [0, 1, 0], [0, 0, 3]],
        [[0, 0, 0], [0, 0, 0], [0, 0, 2]],
        [[2, 1], [1, 2]],
    ],
)
def test_projector_properties_synthetic(entries, bits):
    matrix = _mp_matrix_from_complex(entries, bits)
    with mp.workprec(bits):
        result = mpe._analyze_mp_hermitian_matrix(matrix, precision_bits=bits)
        dimension = matrix.rows
        tol = mpe._fraction_to_mpf_current(mpe.PROJECTOR_STABILITY_TOLERANCE)

        total = mp.matrix(dimension, dimension)
        for cluster, projector in zip(result.clusters, result.cluster_projectors):
            hermitian_defect = _spectral_norm(projector - projector.transpose_conj(), bits)
            assert hermitian_defect <= tol

            idempotent_defect = _spectral_norm(projector * projector - projector, bits)
            assert idempotent_defect <= tol

            trace = sum(projector[i, i] for i in range(dimension))
            assert abs(trace.real - len(cluster)) <= tol
            total = total + projector

        for i, projector_i in enumerate(result.cluster_projectors):
            for j, projector_j in enumerate(result.cluster_projectors):
                if i != j:
                    cross = projector_i * projector_j
                    assert _spectral_norm(cross, bits) <= tol

        completeness_defect = _spectral_norm(total - mp.eye(dimension), bits)
        assert completeness_defect <= tol


# --- Model 0B reference tests -----------------------------------------------------


@pytest.mark.parametrize("lambda_cutoff,bits", [(1, P1_BITS), (1, P2_BITS), (2, P1_BITS), (2, P2_BITS)])
def test_model0b_reference_analysis(
    lambda_cutoff,
    bits,
    lambda1_precision_result,
    lambda1_p2_result,
    lambda2_precision_result,
):
    # PERF-3: reuse the already-computed real P1/P2 results from the PERF-1
    # session fixtures (conftest.py) instead of rebuilding
    # components/rerunning analyze_mp_eigensystem here. Same scientific
    # route, same real MPEigensystemResult objects, no mock, no serialized
    # result, no frozen eigenvalue.
    if lambda_cutoff == 1:
        result = lambda1_precision_result.p1_result if bits == P1_BITS else lambda1_p2_result
    else:
        result = (
            lambda2_precision_result.p1_result
            if bits == P1_BITS
            else lambda2_precision_result.p2_result
        )

    assert result.precision_bits == bits
    assert result.backward_gate_pass is True

    dimension = len(result.eigenvalues)
    covered = sorted(index for cluster in result.clusters for index in cluster)
    assert covered == list(range(dimension))

    with mp.workprec(bits):
        total = mp.matrix(dimension, dimension)
        for projector in result.cluster_projectors:
            total = total + projector
        completeness_defect = _spectral_norm(total - mp.eye(dimension), bits)
        projector_tol = mpe._fraction_to_mpf_current(mpe.PROJECTOR_STABILITY_TOLERANCE)
    assert completeness_defect <= projector_tol

    assert len(result.ground_cluster_indices) >= 1

    expected_status = (
        mpe.PRECISION_LEVEL_STATUS_P1 if bits == P1_BITS else mpe.PRECISION_LEVEL_STATUS_P2
    )
    assert result.precision_level_status == expected_status

    if lambda_cutoff == 2:
        assert result.ground_cluster_dimension_candidate == 1


# --- Lambda=3 scalability regression -----------------------------------------------


def test_model0b_lambda3_p2_scalability():
    basis = build_physical_basis(3)
    components = build_exact_discrete_components(basis, lambda_cutoff=3)

    result = mpe.analyze_mp_eigensystem(
        components,
        g=Fraction(1, 1),
        mu=Fraction(0, 1),
        delta=Fraction(0, 1),
        precision_bits=P2_BITS,
    )

    assert result.backward_gate_pass is True

    with mp.workprec(P2_BITS):
        total = mp.matrix(components.dimension, components.dimension)
        for projector in result.cluster_projectors:
            total = total + projector
        completeness_defect = _spectral_norm(total - mp.eye(components.dimension), P2_BITS)
        projector_tol = mpe._fraction_to_mpf_current(mpe.PROJECTOR_STABILITY_TOLERANCE)
    assert completeness_defect <= projector_tol

    assert result.precision_level_status == mpe.PRECISION_LEVEL_STATUS_P2


# --- Direct assembly provenance -----------------------------------------------------


def test_public_route_requires_exact_components_not_a_matrix():
    basis = build_physical_basis(1)
    components = build_exact_discrete_components(basis, lambda_cutoff=1)

    # The public function only accepts ExactDiscreteHamiltonianComponents; a
    # bare mpmath matrix (even a validly assembled one) is not an accepted
    # substitute for the components + exact-parameter route.
    with pytest.raises(AttributeError):
        mpe.analyze_mp_eigensystem(
            mp.eye(components.dimension),
            g=Fraction(1),
            mu=Fraction(0),
            delta=Fraction(0),
            precision_bits=P1_BITS,
        )


def test_no_public_matrix_only_entry_point_exists():
    assert not hasattr(mpe, "analyze_mp_matrix")


# --- Input validation ------------------------------------------------------------


def test_rejects_p0_precision():
    basis = build_physical_basis(1)
    components = build_exact_discrete_components(basis, lambda_cutoff=1)
    with pytest.raises(ValueError):
        mpe.analyze_mp_eigensystem(
            components, g=Fraction(1), mu=Fraction(0), delta=Fraction(0), precision_bits=53
        )


@pytest.mark.parametrize("bad_precision", [0, 107, 211, 213])
def test_rejects_other_unauthorized_precisions(bad_precision):
    basis = build_physical_basis(1)
    components = build_exact_discrete_components(basis, lambda_cutoff=1)
    with pytest.raises(ValueError):
        mpe.analyze_mp_eigensystem(
            components,
            g=Fraction(1),
            mu=Fraction(0),
            delta=Fraction(0),
            precision_bits=bad_precision,
        )


def test_rejects_bool_precision():
    basis = build_physical_basis(1)
    components = build_exact_discrete_components(basis, lambda_cutoff=1)
    with pytest.raises(TypeError):
        mpe.analyze_mp_eigensystem(
            components, g=Fraction(1), mu=Fraction(0), delta=Fraction(0), precision_bits=True
        )


def test_rejects_float_g():
    basis = build_physical_basis(1)
    components = build_exact_discrete_components(basis, lambda_cutoff=1)
    with pytest.raises(TypeError):
        mpe.analyze_mp_eigensystem(
            components, g=0.1, mu=Fraction(0), delta=Fraction(0), precision_bits=P1_BITS
        )


# --- Precision context restoration -------------------------------------------------


def test_precision_context_restored_after_p1_analysis():
    basis = build_physical_basis(1)
    components = build_exact_discrete_components(basis, lambda_cutoff=1)
    before = mp.mp.prec
    mpe.analyze_mp_eigensystem(
        components, g=Fraction(1), mu=Fraction(0), delta=Fraction(0), precision_bits=P1_BITS
    )
    assert mp.mp.prec == before


def test_precision_context_restored_after_p2_analysis():
    basis = build_physical_basis(1)
    components = build_exact_discrete_components(basis, lambda_cutoff=1)
    before = mp.mp.prec
    mpe.analyze_mp_eigensystem(
        components, g=Fraction(1), mu=Fraction(0), delta=Fraction(0), precision_bits=P2_BITS
    )
    assert mp.mp.prec == before


def test_precision_context_unaffected_by_rejected_call():
    basis = build_physical_basis(1)
    components = build_exact_discrete_components(basis, lambda_cutoff=1)
    before = mp.mp.prec
    with pytest.raises(ValueError):
        mpe.analyze_mp_eigensystem(
            components, g=Fraction(1), mu=Fraction(0), delta=Fraction(0), precision_bits=53
        )
    assert mp.mp.prec == before


def test_precision_context_restored_when_called_from_nested_workprec():
    basis = build_physical_basis(1)
    components = build_exact_discrete_components(basis, lambda_cutoff=1)
    with mp.workprec(53):
        inner_before = mp.mp.prec
        mpe.analyze_mp_eigensystem(
            components, g=Fraction(1), mu=Fraction(0), delta=Fraction(0), precision_bits=P2_BITS
        )
        assert mp.mp.prec == inner_before
