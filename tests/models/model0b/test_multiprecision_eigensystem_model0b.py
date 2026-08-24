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


def _spectral_norm(matrix, bits):
    with mp.workprec(bits):
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


def test_backward_tolerances():
    assert mpe.BACKWARD_RESIDUAL_TOLERANCE == mp.mpf("1e-12")
    assert mpe.BACKWARD_ORTHOGONALITY_TOLERANCE == mp.mpf("1e-12")


def test_projector_stability_tolerance():
    assert mpe.PROJECTOR_STABILITY_TOLERANCE == mp.mpf("1e-10")


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

        assert result.clusters[0] == (0, 1)
        assert result.ground_cluster_dimension_candidate == 2
        assert result.ground_to_next_cluster_separation_candidate == 2

        # Only the basis-invariant projector is checked -- never a specific
        # eigenvector inside the degenerate subspace.
        diff = result.ground_cluster_projector - p_expected_mp
        assert _spectral_norm(diff, bits) <= mpe.PROJECTOR_STABILITY_TOLERANCE


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

        assert result.residual_ratio <= mpe.BACKWARD_RESIDUAL_TOLERANCE
        assert result.orthogonality_defect <= mpe.BACKWARD_ORTHOGONALITY_TOLERANCE
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
        tol = mpe.PROJECTOR_STABILITY_TOLERANCE

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
def test_model0b_reference_analysis(lambda_cutoff, bits):
    basis = build_physical_basis(lambda_cutoff)
    components = build_exact_discrete_components(basis, lambda_cutoff=lambda_cutoff)

    result = mpe.analyze_mp_eigensystem(
        components,
        g=Fraction(1, 1),
        mu=Fraction(0, 1),
        delta=Fraction(0, 1),
        precision_bits=bits,
    )

    assert result.backward_gate_pass is True

    covered = sorted(index for cluster in result.clusters for index in cluster)
    assert covered == list(range(components.dimension))

    with mp.workprec(bits):
        total = mp.matrix(components.dimension, components.dimension)
        for projector in result.cluster_projectors:
            total = total + projector
        completeness_defect = _spectral_norm(total - mp.eye(components.dimension), bits)
    assert completeness_defect <= mpe.PROJECTOR_STABILITY_TOLERANCE

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
    assert completeness_defect <= mpe.PROJECTOR_STABILITY_TOLERANCE

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
