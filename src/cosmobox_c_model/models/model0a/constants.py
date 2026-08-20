"""Frozen protocol constants for the Toy Model 0A benchmark
(docs/toy-models/toy0/implementation-design.md).

All values here are pre-registered scientific/protocol data specific to 0A.
They must never migrate into cosmobox_c_model.core as default values.
"""

from __future__ import annotations

# Background flux configuration (implementation-design.md Section 9).
BACKGROUND = (0, 1, 0)

# Numerical tolerances gelees (implementation-design.md Section 28).
EXACT_MATRIX_ATOL = 1e-12
COMMUTATOR_ATOL = 1e-12
HERMITICITY_ATOL = 1e-12
MEASUREMENT_IMAG_ATOL = 1e-12
SINGULAR_VALUE_ATOL = 1e-12
EXPECTATION_ATOL = 1e-12
RANK_EPSILON = 1e-12
KERNEL_PROJECTOR_FROBENIUS_TOL = 1e-10

# F_delta pre-registered sweep (implementation-design.md Section 27).
F_DELTA_SWEEP = (1e-2, 1e-4, 1e-6, 1e-8, 1e-10, 1e-13, 0.0)
