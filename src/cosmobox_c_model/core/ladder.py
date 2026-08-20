"""Generic truncated ladder operators: a diagonal operator over a finite ordered
domain, and a truncated raising operator on that same domain.

The raising operator is a clipped shift -- never cyclic, never unitary at the
boundary -- parameterized only by the domain size. No gauge-group or graph
semantics are introduced here.
"""

from __future__ import annotations

from typing import Sequence

import numpy as np

SCIENTIFIC_METADATA = {
    "status": "established",
    "origin_model": None,
    "normative_reference": None,
}


def build_flux_operator(domain: Sequence[float]) -> np.ndarray:
    """Diagonal operator whose eigenvalues are exactly `domain`, in the given order."""
    return np.diag(np.array(domain, dtype=complex))


def build_truncated_raise_operator(dimension: int) -> np.ndarray:
    """Truncated raising operator on a domain of `dimension` ordered levels: maps
    level i to level i+1 for i < dimension-1, and annihilates the top level."""
    matrix = np.zeros((dimension, dimension), dtype=complex)
    for i in range(dimension - 1):
        matrix[i + 1, i] = 1.0
    return matrix
