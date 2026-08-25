"""PERF-1: session-scoped test fixtures for the Toy Model 0B real-model
reference computations (Lambda=1, Lambda=2 at g=1, mu=0, delta=0), shared
across the I2-B2-B / I2-B2-C / I2-B2-D integration tests within a single
pytest session.

Scope firewall: this file is test infrastructure ONLY. It introduces no
new algorithm, threshold, or precision level; every fixture calls the
already-accepted production routes exactly as the tests previously called
them directly (`build_physical_basis`, `build_exact_discrete_components`,
`precision_control.run_spectral_precision_control`,
`precision_control._analyze_p2_direct`). The only change is that, within a
single pytest session, each of these real-model computations is performed
at most once and then reused by every test that needs the same reference
point, instead of being recomputed independently by every test module.

In particular, the full frozen P0/P1/P2 ladder for the Lambda=2 reference
point (`lambda2_precision_result`) -- by far the most expensive
computation in the suite -- is executed exactly once per session here.

Fixture results are never mutated by tests: `mp.matrix`/`np.ndarray`
fields on the shared dataclasses are read-only by test convention. A test
that needs an intentionally altered copy must use `dataclasses.replace`
(or build a fresh local object), never modify a shared fixture result in
place.
"""

from __future__ import annotations

from fractions import Fraction

import pytest

from cosmobox_c_model.models.model0b import precision_control as pc
from cosmobox_c_model.models.model0b.basis_config import build_physical_basis
from cosmobox_c_model.models.model0b.exact_assembly import build_exact_discrete_components

REFERENCE_G = Fraction(1, 1)
REFERENCE_MU = Fraction(0, 1)
REFERENCE_DELTA = Fraction(0, 1)


@pytest.fixture(scope="session")
def lambda1_components():
    """Exact discrete Hamiltonian components at Lambda=1 (session-shared,
    read-only)."""
    basis = build_physical_basis(1)
    return build_exact_discrete_components(basis, lambda_cutoff=1)


@pytest.fixture(scope="session")
def lambda2_components():
    """Exact discrete Hamiltonian components at Lambda=2 (session-shared,
    read-only)."""
    basis = build_physical_basis(2)
    return build_exact_discrete_components(basis, lambda_cutoff=2)


@pytest.fixture(scope="session")
def lambda1_precision_result(lambda1_components):
    """Real `run_spectral_precision_control` at the frozen reference point
    (g=1, mu=0, delta=0), Lambda=1: `PRECISION_STABLE`, P2 not computed
    (lazy escalation). Computed at most once per session."""
    return pc.run_spectral_precision_control(
        lambda1_components, g=REFERENCE_G, mu=REFERENCE_MU, delta=REFERENCE_DELTA
    )


@pytest.fixture(scope="session")
def lambda2_precision_result(lambda2_components):
    """Real `run_spectral_precision_control` at the frozen reference point
    (g=1, mu=0, delta=0), Lambda=2: the full P0/P1/P2 ladder is executed
    (faithfully reaching `PRECISION_UNRESOLVED`, cf. I2-B2-B-R1
    arbitration). This is the single authoritative execution of that
    ladder for this reference point in the session."""
    return pc.run_spectral_precision_control(
        lambda2_components, g=REFERENCE_G, mu=REFERENCE_MU, delta=REFERENCE_DELTA
    )


@pytest.fixture(scope="session")
def lambda1_p2_result(lambda1_components):
    """Explicit, session-unique P2 (212-bit) analysis for the Lambda=1
    reference point. Needed only to independently qualify the P1/P2
    comparison route: the normal `PRECISION_STABLE` ladder for Lambda=1
    never computes P2 (lazy escalation, preserved and verified separately
    via `lambda1_precision_result`)."""
    return pc._analyze_p2_direct(
        lambda1_components, g=REFERENCE_G, mu=REFERENCE_MU, delta=REFERENCE_DELTA
    )
