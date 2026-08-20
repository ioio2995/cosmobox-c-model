"""Model-specific configuration of the Toy Model 0A total basis: a 3-site open
chain (0-1-2) with two truncated U(1) links, 01 and 12
(docs/toy-models/toy0/implementation-design.md Section 6).

State field order, frozen here: (n0, n1, n2, E01, E12). This is the single
place that fixes the deterministic enumeration order required by
software-architecture-governance.md Section 14.2.
"""

from __future__ import annotations

from cosmobox_c_model.core.state_space import Basis, build_composite_basis

# Occupation: 0 < 1. Flux: -1 < 0 < +1 (implementation-design.md Section 6).
OCCUPATION_DOMAIN: tuple[int, ...] = (0, 1)
FLUX_DOMAIN: tuple[int, ...] = (-1, 0, 1)

N_SITES = 3
LINKS: tuple[str, ...] = ("01", "12")

# Field order of the state tuple, matching build_total_basis()'s domain order.
STATE_FIELDS: tuple[str, ...] = ("n0", "n1", "n2", "E01", "E12")


def build_total_basis() -> Basis:
    """Build the deterministic 72-dimensional total basis of Toy Model 0A."""
    domains = (OCCUPATION_DOMAIN,) * N_SITES + (FLUX_DOMAIN,) * len(LINKS)
    return build_composite_basis(domains)
