"""Tests for the Toy Model 0B frozen cross-precision spectral-projector
control: P0/P1 and P1/P2 numerical-cluster matching, the frozen projector
distance `d_P`, and the deterministic P0/P1/P2 precision-escalation ladder
(docs/toy-models/toy0b/temporal-event-solver.md Sections 15-20).

Arbitration note (I2-B2-B-R1): the frozen protocol itself is unchanged. At
Lambda=2 (g=1, mu=0, delta=0), faithfully executing the frozen protocol
produces PRECISION_UNRESOLVED: both the P0/P1 and P1/P2 comparisons match
their cluster partitions and pass their backward gates, but the frozen
projector distance `d_P` exceeds the frozen 1e-10 threshold at both stages.
This is recorded here as a QUALIFICATION_NONCONFIRMATORY numerical
qualification result, not a physical claim, and not evidence of an
implementation defect (cross-validated by an independent test-side
`mp.svd_c` computation, see
`test_lambda2_full_ladder_and_independent_d_p_oracle`)."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

import mpmath as mp
import pytest

from cosmobox_c_model.models.model0b import precision_control as pc
from cosmobox_c_model.models.model0b.basis_config import build_physical_basis
from cosmobox_c_model.models.model0b.exact_assembly import (
    P0_BITS,
    P1_BITS,
    P2_BITS,
    build_exact_discrete_components,
)
from cosmobox_c_model.models.model0b.multiprecision import (
    PROJECTOR_STABILITY_TOLERANCE,
    _fraction_to_mpf_current,
)

REFERENCE_G = Fraction(1, 1)
REFERENCE_MU = Fraction(0, 1)
REFERENCE_DELTA = Fraction(0, 1)


# --- Frozen constants -----------------------------------------------------------


def test_allowed_precision_pairs():
    assert pc.ALLOWED_PRECISION_PAIRS == ((53, 106), (106, 212))


def test_matching_status_values():
    assert pc.MATCHING_STATUS_MATCHED == "MATCHED"
    assert pc.MATCHING_STATUS_UNRESOLVED == "SPECTRAL_CLUSTER_UNRESOLVED"


def test_failure_reason_values():
    assert pc.FAILURE_REASON_NONE == "NONE"
    assert pc.FAILURE_REASON_BACKWARD_GATE_FAILED == "BACKWARD_GATE_FAILED"
    assert pc.FAILURE_REASON_SPECTRAL_CLUSTER_UNRESOLVED == "SPECTRAL_CLUSTER_UNRESOLVED"
    assert pc.FAILURE_REASON_PROJECTOR_STABILITY_FAILED == "PROJECTOR_STABILITY_FAILED"


def test_precision_status_values():
    assert pc.PRECISION_STATUS_STABLE == "PRECISION_STABLE"
    assert pc.PRECISION_STATUS_ESCALATED == "PRECISION_ESCALATED"
    assert pc.PRECISION_STATUS_UNRESOLVED == "PRECISION_UNRESOLVED"


# --- A-E. Synthetic index-set matching --------------------------------------------


def test_matching_identical_partitions():
    low = ((0,), (1, 2), (3,))
    status, mapping = pc._match_clusters(low, low)
    assert status == pc.MATCHING_STATUS_MATCHED
    assert mapping == ((0,), (1,), (2,))


def test_matching_valid_high_split():
    low = ((0, 1), (2, 3, 4), (5,))
    high = ((0,), (1,), (2,), (3, 4), (5,))
    status, mapping = pc._match_clusters(low, high)
    assert status == pc.MATCHING_STATUS_MATCHED
    assert mapping == ((0, 1), (2, 3), (4,))


def test_matching_high_merge_across_low_boundary():
    low = ((0, 1), (2, 3))
    high = ((0, 1, 2), (3,))
    status, mapping = pc._match_clusters(low, high)
    assert status == pc.MATCHING_STATUS_UNRESOLVED
    assert mapping is None


def test_matching_shifted_boundary():
    low = ((0, 1), (2, 3))
    high = ((0,), (1, 2), (3,))
    status, mapping = pc._match_clusters(low, high)
    assert status == pc.MATCHING_STATUS_UNRESOLVED
    assert mapping is None


@pytest.mark.parametrize(
    "clusters,dimension",
    [
        (((0,), (2,), (1,)), 3),  # not ordered by first index
        (((0, 0), (1,)), 2),  # non-strictly-increasing within cluster
        (((), (0,)), 1),  # empty cluster
        (((0,), (0, 1)), 2),  # overlapping / not pairwise disjoint
        (((0,), (1,)), 3),  # does not flatten to range(dimension)
        (((0,), (2,)), 3),  # missing index 1
    ],
)
def test_validate_partition_rejects_malformed(clusters, dimension):
    with pytest.raises(ValueError):
        pc._validate_partition(clusters, dimension, name="test")


# --- Synthetic projector helpers --------------------------------------------------


@dataclass
class _FakeResult:
    precision_bits: int
    eigenvalues: tuple
    clusters: "tuple[tuple[int, ...], ...]"
    cluster_projectors: "tuple[mp.matrix, ...]"
    backward_gate_pass: bool


def _rank1_projector(dimension: int, index: int, bits: int) -> "mp.matrix":
    with mp.workprec(bits):
        column = mp.matrix(dimension, 1)
        column[index, 0] = mp.mpc(1)
        return column * column.transpose_conj()


def _identity_mp(dimension: int, bits: int) -> "mp.matrix":
    with mp.workprec(bits):
        return mp.eye(dimension)


# --- Synthetic d_P ------------------------------------------------------------------


def test_synthetic_d_p_identical_projectors():
    bits_low, bits_high = 106, 212
    projector = _rank1_projector(2, 0, bits_high)
    low = _FakeResult(bits_low, (0.0, 1.0), ((0,), (1,)), (projector, _rank1_projector(2, 1, bits_high)), True)
    high = _FakeResult(bits_high, (0.0, 1.0), ((0,), (1,)), (projector, _rank1_projector(2, 1, bits_high)), True)

    comparison = pc.compare_precision_levels(low, high)
    assert comparison.matching_status == pc.MATCHING_STATUS_MATCHED
    assert comparison.d_p == mp.mpf(0)
    assert comparison.stability_pass is True
    assert comparison.failure_reason == pc.FAILURE_REASON_NONE


def test_synthetic_d_p_valid_split_projector_sum():
    bits_low, bits_high = 106, 212
    low_projector = _identity_mp(2, bits_high)  # rank-2 projector covering both dims
    high_p0 = _rank1_projector(2, 0, bits_high)
    high_p1 = _rank1_projector(2, 1, bits_high)

    low = _FakeResult(bits_low, (0.0, 1.0), ((0, 1),), (low_projector,), True)
    high = _FakeResult(bits_high, (0.0, 1.0), ((0,), (1,)), (high_p0, high_p1), True)

    comparison = pc.compare_precision_levels(low, high)
    assert comparison.matching_status == pc.MATCHING_STATUS_MATCHED
    assert comparison.cluster_mapping == ((0, 1),)
    assert comparison.d_p == mp.mpf(0)
    assert comparison.stability_pass is True


def test_synthetic_d_p_clearly_different_projectors_fails():
    bits_low, bits_high = 106, 212
    # Same 2-dimensional ambient index-set partition on both sides (trivial
    # 1-1 matching), but the actual projectors are deliberately swapped
    # (orthogonal subspaces): d_P = 1 exactly.
    low_p0 = _rank1_projector(2, 0, bits_high)
    low_p1 = _rank1_projector(2, 1, bits_high)
    high_p0 = _rank1_projector(2, 1, bits_high)
    high_p1 = _rank1_projector(2, 0, bits_high)

    low = _FakeResult(bits_low, (0.0, 1.0), ((0,), (1,)), (low_p0, low_p1), True)
    high = _FakeResult(bits_high, (0.0, 1.0), ((0,), (1,)), (high_p0, high_p1), True)

    comparison = pc.compare_precision_levels(low, high)
    assert comparison.matching_status == pc.MATCHING_STATUS_MATCHED
    assert comparison.d_p == mp.mpf(1)
    assert comparison.stability_pass is False
    assert comparison.failure_reason == pc.FAILURE_REASON_PROJECTOR_STABILITY_FAILED


# --- Backward-gate fail-closed precedence -----------------------------------------


def test_backward_gate_failure_forces_stability_fail():
    bits_low, bits_high = 106, 212
    projector = _rank1_projector(1, 0, bits_high)
    low = _FakeResult(bits_low, (0.0,), ((0,),), (projector,), False)
    high = _FakeResult(bits_high, (0.0,), ((0,),), (projector,), True)

    comparison = pc.compare_precision_levels(low, high)
    assert comparison.stability_pass is False
    assert comparison.failure_reason == pc.FAILURE_REASON_BACKWARD_GATE_FAILED


def test_backward_gate_failure_precedence_over_unresolved_matching():
    bits_low, bits_high = 106, 212
    p = _rank1_projector(3, 0, bits_high)
    low = _FakeResult(bits_low, (0.0, 1.0, 2.0), ((0, 1), (2,)), (p, p), False)
    high = _FakeResult(bits_high, (0.0, 1.0, 2.0), ((0, 1, 2),), (p,), True)

    comparison = pc.compare_precision_levels(low, high)
    assert comparison.matching_status == pc.MATCHING_STATUS_UNRESOLVED
    assert comparison.stability_pass is False
    # Precedence: BACKWARD_GATE_FAILED (1) outranks SPECTRAL_CLUSTER_UNRESOLVED (2).
    assert comparison.failure_reason == pc.FAILURE_REASON_BACKWARD_GATE_FAILED


def test_spectral_cluster_unresolved_when_backward_gates_pass():
    bits_low, bits_high = 106, 212
    p = _rank1_projector(3, 0, bits_high)
    low = _FakeResult(bits_low, (0.0, 1.0, 2.0), ((0, 1), (2,)), (p, p), True)
    high = _FakeResult(bits_high, (0.0, 1.0, 2.0), ((0, 1, 2),), (p,), True)

    comparison = pc.compare_precision_levels(low, high)
    assert comparison.matching_status == pc.MATCHING_STATUS_UNRESOLVED
    assert comparison.d_p is None
    assert comparison.projector_defects == ()
    assert comparison.stability_pass is False
    assert comparison.failure_reason == pc.FAILURE_REASON_SPECTRAL_CLUSTER_UNRESOLVED


# --- Unsupported / malformed input to compare_precision_levels -------------------


def test_compare_precision_levels_rejects_unsupported_pair():
    low = _FakeResult(P0_BITS, (0.0,), ((0,),), (_rank1_projector(1, 0, P2_BITS),), True)
    high = _FakeResult(P2_BITS, (0.0,), ((0,),), (_rank1_projector(1, 0, P2_BITS),), True)
    with pytest.raises(ValueError):
        pc.compare_precision_levels(low, high)


def test_compare_precision_levels_rejects_dimension_mismatch():
    low = _FakeResult(P1_BITS, (0.0,), ((0,),), (_rank1_projector(1, 0, P2_BITS),), True)
    high = _FakeResult(P2_BITS, (0.0, 1.0), ((0,), (1,)), (_rank1_projector(2, 0, P2_BITS), _rank1_projector(2, 1, P2_BITS)), True)
    with pytest.raises(ValueError):
        pc.compare_precision_levels(low, high)


# --- P0 binary64 exact projector conversion --------------------------------------


def test_p0_matrix_to_mp_exact_conversion():
    import numpy as np
    from fractions import Fraction as PyFraction

    matrix = np.array(
        [[1.0 / 3.0, 0.5 + 0.25j], [0.5 - 0.25j, 2.0 / 7.0]],
        dtype=complex,
    )

    with mp.workprec(P1_BITS):
        converted = pc._p0_matrix_to_mp_exact(matrix)

        expected = mp.matrix(2, 2)
        for i in range(2):
            for j in range(2):
                value = matrix[i, j]
                real_fraction = PyFraction.from_float(float(value.real))
                imag_fraction = PyFraction.from_float(float(value.imag))
                expected[i, j] = mp.mpc(
                    mp.mpf(real_fraction.numerator) / mp.mpf(real_fraction.denominator),
                    mp.mpf(imag_fraction.numerator) / mp.mpf(imag_fraction.denominator),
                )

        assert converted == expected


# --- Real model: Lambda=1 P0/P1 (positive regression) -----------------------------


def test_lambda1_real_p0_p1_stable():
    basis = build_physical_basis(1)
    components = build_exact_discrete_components(basis, lambda_cutoff=1)

    p0 = pc._analyze_p0_direct(components, g=REFERENCE_G, mu=REFERENCE_MU, delta=REFERENCE_DELTA)
    p1 = pc._analyze_p1_direct(components, g=REFERENCE_G, mu=REFERENCE_MU, delta=REFERENCE_DELTA)
    comparison = pc.compare_precision_levels(p0, p1)

    assert comparison.matching_status == pc.MATCHING_STATUS_MATCHED
    assert comparison.backward_gates_pass is True
    assert comparison.d_p is not None
    with mp.workprec(P1_BITS):
        threshold = _fraction_to_mpf_current(PROJECTOR_STABILITY_TOLERANCE)
    assert comparison.d_p <= threshold
    assert comparison.stability_pass is True


def test_lambda1_real_p1_p2_stable():
    basis = build_physical_basis(1)
    components = build_exact_discrete_components(basis, lambda_cutoff=1)

    p1 = pc._analyze_p1_direct(components, g=REFERENCE_G, mu=REFERENCE_MU, delta=REFERENCE_DELTA)
    p2 = pc._analyze_p2_direct(components, g=REFERENCE_G, mu=REFERENCE_MU, delta=REFERENCE_DELTA)
    comparison = pc.compare_precision_levels(p1, p2)

    assert comparison.matching_status == pc.MATCHING_STATUS_MATCHED
    assert comparison.backward_gates_pass is True
    with mp.workprec(P2_BITS):
        threshold = _fraction_to_mpf_current(PROJECTOR_STABILITY_TOLERANCE)
    assert comparison.d_p <= threshold
    assert comparison.stability_pass is True


def test_lambda1_end_to_end_precision_stable_lazy_p2():
    basis = build_physical_basis(1)
    components = build_exact_discrete_components(basis, lambda_cutoff=1)

    result = pc.run_spectral_precision_control(
        components, g=REFERENCE_G, mu=REFERENCE_MU, delta=REFERENCE_DELTA
    )

    assert result.precision_status == pc.PRECISION_STATUS_STABLE
    assert result.selected_precision_bits == 106
    assert result.selected_level_result is result.p1_result
    assert result.p0_p1_comparison.stability_pass is True
    assert result.p2_result is None
    assert result.p1_p2_comparison is None


# --- Real model: Lambda=2 (faithful PRECISION_UNRESOLVED qualification) ----------


def test_lambda2_full_ladder_and_independent_d_p_oracle():
    basis = build_physical_basis(2)
    components = build_exact_discrete_components(basis, lambda_cutoff=2)

    result = pc.run_spectral_precision_control(
        components, g=REFERENCE_G, mu=REFERENCE_MU, delta=REFERENCE_DELTA
    )

    p0_p1 = result.p0_p1_comparison
    assert p0_p1.matching_status == pc.MATCHING_STATUS_MATCHED
    assert p0_p1.backward_gates_pass is True
    assert p0_p1.d_p is not None
    with mp.workprec(P1_BITS):
        threshold_p1 = _fraction_to_mpf_current(PROJECTOR_STABILITY_TOLERANCE)
    assert p0_p1.d_p > threshold_p1
    assert p0_p1.stability_pass is False
    assert p0_p1.failure_reason == pc.FAILURE_REASON_PROJECTOR_STABILITY_FAILED

    # P2 must be computed: the P0/P1 pair did not pass.
    assert result.p2_result is not None
    assert result.p1_p2_comparison is not None

    p1_p2 = result.p1_p2_comparison
    assert p1_p2.matching_status == pc.MATCHING_STATUS_MATCHED
    assert p1_p2.backward_gates_pass is True
    assert p1_p2.d_p is not None
    with mp.workprec(P2_BITS):
        threshold_p2 = _fraction_to_mpf_current(PROJECTOR_STABILITY_TOLERANCE)
    assert p1_p2.d_p > threshold_p2
    assert p1_p2.stability_pass is False
    assert p1_p2.failure_reason == pc.FAILURE_REASON_PROJECTOR_STABILITY_FAILED

    assert result.precision_status == pc.PRECISION_STATUS_UNRESOLVED
    assert result.selected_precision_bits is None
    assert result.selected_level_result is None

    # --- Independent test-side d_P oracle for the worst P0/P1 cluster,
    # using mp.svd_c (never the production _spectral_norm_general route). ---
    p0_result = result.p0_result
    worst_index = max(
        range(len(p0_p1.projector_defects)), key=lambda i: p0_p1.projector_defects[i]
    )
    worst_low_cluster = p0_result.clusters[worst_index]
    worst_high_indices = p0_p1.cluster_mapping[worst_index]

    with mp.workprec(P1_BITS):
        # Independent P0->mp exact conversion, written fresh here rather than
        # calling `pc._p0_matrix_to_mp_exact`.
        low_projector_np = p0_result.cluster_projectors[worst_index]
        dimension = low_projector_np.shape[0]
        low_projector_mp = mp.matrix(dimension, dimension)
        for i in range(dimension):
            for j in range(dimension):
                value = low_projector_np[i, j]
                real_fraction = Fraction.from_float(float(value.real))
                imag_fraction = Fraction.from_float(float(value.imag))
                low_projector_mp[i, j] = mp.mpc(
                    mp.mpf(real_fraction.numerator) / mp.mpf(real_fraction.denominator),
                    mp.mpf(imag_fraction.numerator) / mp.mpf(imag_fraction.denominator),
                )

        covering = mp.matrix(dimension, dimension)
        for high_index in worst_high_indices:
            covering = covering + result.p1_result.cluster_projectors[high_index]

        difference = covering - low_projector_mp
        singular_values = mp.svd_c(difference, compute_uv=False)
        independent_norm = singular_values[0]

        production_defect = p0_p1.projector_defects[worst_index]
        # Both routes compute the exact same mathematical spectral norm of
        # the exact same matrix: representation-only agreement, many orders
        # of magnitude tighter than the frozen 1e-10 scale.
        assert abs(independent_norm - production_defect) <= mp.mpf(2) ** (8 - P1_BITS)
        assert independent_norm > threshold_p1

    # Diagnostic-only reporting (not a scientific claim).
    print(f"QUALIFICATION_NONCONFIRMATORY: Lambda=2 worst P0/P1 cluster {worst_low_cluster} "
          f"d_P={float(p0_p1.d_p):.6e}; Lambda=2 P1/P2 d_P={float(p1_p2.d_p):.6e}")


# --- Forced routing (test-side monkeypatching, no production backdoor) -----------


def _make_comparison(low_bits, high_bits, *, stability_pass, matched=True):
    return pc.PrecisionPairComparison(
        low_precision_bits=low_bits,
        high_precision_bits=high_bits,
        matching_status=pc.MATCHING_STATUS_MATCHED if matched else pc.MATCHING_STATUS_UNRESOLVED,
        cluster_mapping=((0,),) if matched else None,
        backward_gates_pass=True,
        projector_defects=(mp.mpf(0),) if matched else (),
        d_p=mp.mpf(0) if matched else None,
        stability_pass=stability_pass,
        failure_reason=(
            pc.FAILURE_REASON_NONE
            if stability_pass
            else (
                pc.FAILURE_REASON_PROJECTOR_STABILITY_FAILED
                if matched
                else pc.FAILURE_REASON_SPECTRAL_CLUSTER_UNRESOLVED
            )
        ),
    )


def test_forced_precision_escalated_route(monkeypatch):
    calls = {"p0": 0, "p1": 0, "p2": 0}

    monkeypatch.setattr(
        pc, "_analyze_p0_direct", lambda *a, **k: calls.__setitem__("p0", calls["p0"] + 1) or "P0"
    )
    monkeypatch.setattr(
        pc, "_analyze_p1_direct", lambda *a, **k: calls.__setitem__("p1", calls["p1"] + 1) or "P1"
    )
    monkeypatch.setattr(
        pc, "_analyze_p2_direct", lambda *a, **k: calls.__setitem__("p2", calls["p2"] + 1) or "P2"
    )

    def fake_compare(low, high):
        if low == "P0" and high == "P1":
            return _make_comparison(53, 106, stability_pass=False)
        if low == "P1" and high == "P2":
            return _make_comparison(106, 212, stability_pass=True)
        raise AssertionError(f"unexpected compare_precision_levels({low!r}, {high!r})")

    monkeypatch.setattr(pc, "compare_precision_levels", fake_compare)

    result = pc.run_spectral_precision_control(
        components=None, g=REFERENCE_G, mu=REFERENCE_MU, delta=REFERENCE_DELTA
    )

    assert result.precision_status == pc.PRECISION_STATUS_ESCALATED
    assert result.selected_precision_bits == 212
    assert result.selected_level_result == "P2"
    assert calls["p2"] == 1  # P2 was actually invoked when the first pair failed.


def test_forced_precision_unresolved_route(monkeypatch):
    calls = {"p2": 0}

    monkeypatch.setattr(pc, "_analyze_p0_direct", lambda *a, **k: "P0")
    monkeypatch.setattr(pc, "_analyze_p1_direct", lambda *a, **k: "P1")
    monkeypatch.setattr(
        pc, "_analyze_p2_direct", lambda *a, **k: calls.__setitem__("p2", calls["p2"] + 1) or "P2"
    )

    def fake_compare(low, high):
        if low == "P0" and high == "P1":
            return _make_comparison(53, 106, stability_pass=False)
        if low == "P1" and high == "P2":
            return _make_comparison(106, 212, stability_pass=False, matched=False)
        raise AssertionError(f"unexpected compare_precision_levels({low!r}, {high!r})")

    monkeypatch.setattr(pc, "compare_precision_levels", fake_compare)

    result = pc.run_spectral_precision_control(
        components=None, g=REFERENCE_G, mu=REFERENCE_MU, delta=REFERENCE_DELTA
    )

    assert result.precision_status == pc.PRECISION_STATUS_UNRESOLVED
    assert result.selected_precision_bits is None
    assert result.selected_level_result is None
    assert calls["p2"] == 1


def test_lazy_p2_not_invoked_when_first_pair_passes(monkeypatch):
    calls = {"p2": 0}

    monkeypatch.setattr(pc, "_analyze_p0_direct", lambda *a, **k: "P0")
    monkeypatch.setattr(pc, "_analyze_p1_direct", lambda *a, **k: "P1")
    monkeypatch.setattr(
        pc, "_analyze_p2_direct", lambda *a, **k: calls.__setitem__("p2", calls["p2"] + 1) or "P2"
    )
    monkeypatch.setattr(
        pc, "compare_precision_levels", lambda low, high: _make_comparison(53, 106, stability_pass=True)
    )

    result = pc.run_spectral_precision_control(
        components=None, g=REFERENCE_G, mu=REFERENCE_MU, delta=REFERENCE_DELTA
    )

    assert calls["p2"] == 0
    assert result.p2_result is None
    assert result.p1_p2_comparison is None
    assert result.precision_status == pc.PRECISION_STATUS_STABLE


# --- Exact nonbinary rational parameter route -------------------------------------


def test_nonbinary_exact_parameter_route_executes_without_float():
    basis = build_physical_basis(1)
    components = build_exact_discrete_components(basis, lambda_cutoff=1)

    result = pc.run_spectral_precision_control(
        components, g=Fraction(1, 10), mu=Fraction(-3, 4), delta=Fraction(2, 5)
    )

    assert isinstance(result, pc.SpectralPrecisionControlResult)
    assert result.precision_status in (
        pc.PRECISION_STATUS_STABLE,
        pc.PRECISION_STATUS_ESCALATED,
        pc.PRECISION_STATUS_UNRESOLVED,
    )


def test_run_spectral_precision_control_rejects_float_g():
    basis = build_physical_basis(1)
    components = build_exact_discrete_components(basis, lambda_cutoff=1)
    with pytest.raises(TypeError):
        pc.run_spectral_precision_control(components, g=0.1, mu=Fraction(0), delta=Fraction(0))
