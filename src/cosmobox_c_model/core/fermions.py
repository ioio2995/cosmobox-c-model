"""Generic fermionic primitives for N ordered modes: creation, annihilation, and
the canonical Jordan-Wigner sign convention.

Not limited to any fixed number of modes: `site` and the occupation tuple length
are supplied entirely by the caller.
"""

from __future__ import annotations

SCIENTIFIC_METADATA = {
    "status": "established",
    "origin_model": None,
    "normative_reference": None,
}

Occupations = tuple[int, ...]


def jordan_wigner_sign(occupations: Occupations, site: int) -> int:
    """Return (-1)^(sum_{k<site} n_k), the canonical Jordan-Wigner sign prefactor
    for acting on mode `site` of an occupation-number state."""
    parity = sum(occupations[:site]) % 2
    return -1 if parity else 1


def apply_annihilation(
    occupations: Occupations, site: int
) -> tuple[Occupations, complex] | None:
    """Apply c_site to |n_0...n_site...>. Returns (new_state, amplitude), or None
    if the mode is already empty."""
    if occupations[site] == 0:
        return None
    sign = jordan_wigner_sign(occupations, site)
    new_occupations = list(occupations)
    new_occupations[site] = 0
    return tuple(new_occupations), complex(sign)


def apply_creation(
    occupations: Occupations, site: int
) -> tuple[Occupations, complex] | None:
    """Apply c_site^dagger to |n_0...n_site...>. Returns (new_state, amplitude), or
    None if the mode is already occupied (Pauli exclusion)."""
    if occupations[site] == 1:
        return None
    sign = jordan_wigner_sign(occupations, site)
    new_occupations = list(occupations)
    new_occupations[site] = 1
    return tuple(new_occupations), complex(sign)
