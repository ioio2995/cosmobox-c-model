"""Frozen physical constants for Toy Model 0B
(docs/toy-models/toy0b/specification.md Section 3).

All values here are pre-registered scientific/protocol data specific to 0B.
They must never migrate into cosmobox_c_model.core as default values.
"""

from __future__ import annotations

# Oriented 6-cycle: 0 -> 1 -> 2 -> 3 -> 4 -> 5 -> 0 (specification.md Section 3).
N_SITES = 6

# Fixed background flux configuration (specification.md Section 3).
BACKGROUND = (0, 1, 0, 1, 0, 1)

# Half-filling constraint: sum(n_i) == 3 (specification.md Section 3).
MATTER_PARTICLE_NUMBER = 3
