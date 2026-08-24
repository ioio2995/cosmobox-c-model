"""Toy Model 0B exact-rational parameters and direct multi-precision
Hamiltonian reassembly (docs/toy-models/toy0b/specification.md Section 4,
docs/toy-models/toy0b/temporal-event-solver.md Section 20).

Scope firewall: this module implements ONLY exact-discrete-component
extraction, the exact rational parameter interface, and direct H^(p)
assembly at the frozen precision levels P0/P1/P2. It performs NO
high-precision diagonalization, NO clustering, NO projector matching, NO
`d_P`, and publishes no precision-stability status. That layer is deferred
to a separate bounded lot (I2-B2).

Backend decision (I2-B-AUDIT, ChatGPT-reviewed): mpmath. `python-flint`/Arb
was rejected because `acb_mat.eig()` cannot return eigenvectors together
with overlapping/multiple eigenvalues, which is architecturally
incompatible with the frozen protocol's cluster-projector requirement.

Frozen reassembly requirement: H^(p) MUST be reassembled directly at
precision p from exact/discrete model data. This module never upcasts an
already-assembled binary64 (P0) Hamiltonian to a higher precision, and
never routes a rational parameter (e.g. g=1/10) through an intermediate
Python `float` -- `Fraction(0.1)` silently yields the binary64
approximation of 0.1, not the exact value 1/10, and is therefore rejected
at the public boundary of this module (`require_exact_rational`).

Exact discrete component contract: the accepted I1-C component matrices
(`H_hop`, `V0`, `N_even`, `V_delta`) are exactly integer-valued for frozen
Model 0B (fermionic signs +-1, occupations 0/1, electric links bounded by
Lambda<=3), hence exactly representable in binary64 with zero rounding
error. This module reuses those accepted builders as-is (no fermionic
sign, hopping, or Gauss logic is reimplemented here) and verifies -- rather
than assumes -- that every entry is exactly finite, real, and
integer-valued before converting to Python `int`. The only genuine
high-precision risk in this model is the rational scalar coefficients
(g, mu, delta), which this module represents exactly via
`fractions.Fraction` and converts to `mpmath.mpf` only inside the target
`mp.workprec` context (never via an intermediate binary64 float).

Concurrency: mpmath's working precision (`mp.workprec`) is global mutable
process state, not thread-local (verified in I2-B-AUDIT: concurrent
threads using different `workprec` values observe each other's precision).

    MPMATH_SHARED_THREAD_PARALLELISM = "NOT_SUPPORTED"

Any future parallel campaign execution using this module must use
process-level isolation (e.g. `multiprocessing`), never shared-memory
threads racing on `mp.workprec`.

Returned-matrix semantics: `assemble_hamiltonian_mp` returns an
`mpmath.matrix` whose entries were computed/rounded inside the requested
`mp.workprec(precision_bits)` context. No claim is made that arithmetic
performed on that matrix *outside* a matching `mp.workprec` context
preserves that working precision automatically -- mpmath numbers are not
tagged with the precision at which they were produced. Callers (e.g. the
future I2-B2 high-precision eigensystem layer) must explicitly re-enter
`mp.workprec(precision_bits)` before performing further arithmetic that
must remain accurate to that precision.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

import mpmath as mp
import numpy as np

from cosmobox_c_model.core.state_space import Basis
from cosmobox_c_model.models.model0b.hamiltonian import (
    build_h_hop,
    build_n_even,
    build_v0,
    build_v_delta,
)

P0_BITS = 53
P1_BITS = 106
P2_BITS = 212

ALLOWED_PRECISION_BITS = (P0_BITS, P1_BITS, P2_BITS)

MPMATH_SHARED_THREAD_PARALLELISM = "NOT_SUPPORTED"

IntMatrix = tuple[tuple[int, ...], ...]


@dataclass(frozen=True)
class ExactDiscreteHamiltonianComponents:
    """Exact integer representation of the accepted Model 0B Hamiltonian
    components, verified (not assumed) integer-valued from the accepted
    I1-C NumPy builders. Entries are plain Python `int`, never float,
    complex, or `mpf`."""

    h_hop: IntMatrix
    v0: IntMatrix
    n_even: IntMatrix
    v_delta: IntMatrix
    dimension: int
    lambda_cutoff: int


def _exact_integer_matrix(matrix: np.ndarray, *, name: str) -> IntMatrix:
    """Verify `matrix` is exactly finite, real, and integer-valued, then
    convert to an immutable tuple-of-tuples of Python `int`. Fails closed
    (no rounding, no tolerance) on any violation."""
    if not np.all(np.isfinite(matrix)):
        raise ValueError(f"{name}: matrix must have only finite entries")
    if not np.array_equal(matrix.imag, np.zeros_like(matrix.imag)):
        raise ValueError(f"{name}: matrix must have exactly zero imaginary part")
    real = matrix.real
    rounded = np.round(real)
    if not np.array_equal(real, rounded):
        raise ValueError(f"{name}: matrix must have exactly integer-valued real entries")
    if np.max(np.abs(rounded)) >= 2**53:
        raise ValueError(f"{name}: entry magnitude exceeds the float64 exact-integer range")
    int_matrix = rounded.astype(np.int64)
    return tuple(tuple(int(value) for value in row) for row in int_matrix)


def build_exact_discrete_components(
    basis: Basis, *, lambda_cutoff: int
) -> ExactDiscreteHamiltonianComponents:
    """Build the exact-integer discrete Model 0B Hamiltonian components by
    reusing the accepted I1-C builders (no physics reimplementation), then
    verifying and converting each to exact Python `int` entries."""
    h_hop = build_h_hop(basis, lambda_cutoff=lambda_cutoff)
    v0 = build_v0(basis)
    n_even = build_n_even(basis)
    v_delta = build_v_delta(basis)

    return ExactDiscreteHamiltonianComponents(
        h_hop=_exact_integer_matrix(h_hop, name="H_hop"),
        v0=_exact_integer_matrix(v0, name="V0"),
        n_even=_exact_integer_matrix(n_even, name="N_even"),
        v_delta=_exact_integer_matrix(v_delta, name="V_delta"),
        dimension=basis.dimension,
        lambda_cutoff=lambda_cutoff,
    )


def require_exact_rational(value: Fraction | int, *, name: str) -> Fraction:
    """Accept only `fractions.Fraction` or `int` and return an exact
    `Fraction`. Rejects float, `np.floating`, `Decimal`, `str`, `bool`, and
    any other object: constructing a `Fraction` from an already-rounded
    binary64 float (e.g. `Fraction(0.1)`) silently yields the wrong exact
    value and must never happen inside this module."""
    if isinstance(value, bool):
        raise TypeError(f"{name} must be a fractions.Fraction or an int, not bool")
    if isinstance(value, Fraction):
        return value
    if isinstance(value, int):
        return Fraction(value)
    raise TypeError(
        f"{name} must be a fractions.Fraction or an int; got {type(value).__name__}"
    )


def _validate_precision_bits(precision_bits: int) -> None:
    if not isinstance(precision_bits, int) or isinstance(precision_bits, bool):
        raise TypeError("precision_bits must be an int")
    if precision_bits not in ALLOWED_PRECISION_BITS:
        raise ValueError(
            f"precision_bits must be one of {ALLOWED_PRECISION_BITS}, got {precision_bits}"
        )


def _fraction_to_mpf(fraction: Fraction) -> "mp.mpf":
    """Exact, correctly-rounded conversion of an exact rational to `mpf` AT
    THE CURRENT WORKING PRECISION. Must be called inside a `mp.workprec`
    context; never routes through an intermediate binary64 float."""
    return mp.mpf(fraction.numerator) / mp.mpf(fraction.denominator)


def assemble_hamiltonian_mp(
    components: ExactDiscreteHamiltonianComponents,
    *,
    g: Fraction | int,
    mu: Fraction | int,
    delta: Fraction | int,
    precision_bits: int,
) -> "mp.matrix":
    """Direct H^(p) reassembly at `precision_bits`
    (specification.md Section 4):

        H = H_hop + g*V0 + 2*mu*N_even + g*delta*V_delta

    from exact integer components and exact rational coefficients, entirely
    inside a single `mp.workprec(precision_bits)` context. Never converts
    from a preassembled (e.g. P0/NumPy) Hamiltonian."""
    _validate_precision_bits(precision_bits)
    g_fraction = require_exact_rational(g, name="g")
    mu_fraction = require_exact_rational(mu, name="mu")
    delta_fraction = require_exact_rational(delta, name="delta")

    dimension = components.dimension
    with mp.workprec(precision_bits):
        g_mp = _fraction_to_mpf(g_fraction)
        mu_mp = _fraction_to_mpf(mu_fraction)
        delta_mp = _fraction_to_mpf(delta_fraction)

        hamiltonian = mp.matrix(dimension, dimension)
        for i in range(dimension):
            h_hop_row = components.h_hop[i]
            v0_row = components.v0[i]
            n_even_row = components.n_even[i]
            v_delta_row = components.v_delta[i]
            for j in range(dimension):
                hamiltonian[i, j] = (
                    mp.mpf(h_hop_row[j])
                    + g_mp * mp.mpf(v0_row[j])
                    + 2 * mu_mp * mp.mpf(n_even_row[j])
                    + g_mp * delta_mp * mp.mpf(v_delta_row[j])
                )

    return hamiltonian
