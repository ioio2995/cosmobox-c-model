"""Generic identifiability engine: measurement matrices, direct-SVD rank, kernel,
kernel projector, and conditioning diagnostics.

No tolerance carries a default value here: every scientific/numerical threshold
is an explicit, keyword-only parameter supplied by the caller's protocol.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np

SCIENTIFIC_METADATA = {
    "status": "established",
    "origin_model": None,
    "normative_reference": None,
}


def build_measurement_matrix(
    observables: Sequence[np.ndarray],
    basis: Sequence[np.ndarray],
    *,
    imag_atol: float,
) -> np.ndarray:
    """Build the measurement matrix (M_F)_{ka} = Tr(B_a O_k) for an ordered family
    of Hermitian observables `observables` and an ordered Hilbert-Schmidt basis
    `basis`.

    Every trace is computed in complex arithmetic; its imaginary part is checked
    against `imag_atol` before the matrix is converted to float64.
    """
    n_observables = len(observables)
    n_basis = len(basis)
    matrix = np.zeros((n_observables, n_basis), dtype=complex)
    for k, observable in enumerate(observables):
        for a, basis_element in enumerate(basis):
            matrix[k, a] = np.trace(basis_element @ observable)

    max_imag = float(np.max(np.abs(matrix.imag))) if matrix.size else 0.0
    if max_imag > imag_atol:
        raise ValueError(
            f"measurement matrix has non-negligible imaginary part "
            f"({max_imag!r} > imag_atol={imag_atol!r})"
        )
    return matrix.real.astype(np.float64)


@dataclass(frozen=True)
class IdentifiabilityResult:
    singular_values_raw: np.ndarray
    singular_values_domain: np.ndarray
    rank_tolerance: float
    numerical_rank: int
    kernel_basis: np.ndarray
    kernel_projector: np.ndarray
    condition_number_resolved: float | None


def analyze_identifiability(matrix: np.ndarray, *, rank_tolerance: float) -> IdentifiabilityResult:
    """Analyze the identifiability structure of a real measurement matrix `matrix`.

    Computes a direct SVD of `matrix` (never `matrix.T @ matrix`), completes the
    singular spectrum with trailing zeros up to the domain dimension, derives the
    numerical rank from the explicit `rank_tolerance` (never the implicit
    tolerance of `numpy.linalg.matrix_rank`), and returns the kernel -- as an
    orthonormal set of domain-coordinate row vectors -- together with its
    orthogonal projector and the condition number on the resolved support.
    """
    n_domain = matrix.shape[1]
    _, singular_values_raw, vh = np.linalg.svd(matrix, full_matrices=True)

    singular_values_domain = np.zeros(n_domain, dtype=float)
    singular_values_domain[: singular_values_raw.shape[0]] = singular_values_raw

    numerical_rank = int(np.count_nonzero(singular_values_domain > rank_tolerance))

    kernel_basis = vh[numerical_rank:].conj()
    kernel_projector = kernel_basis.conj().T @ kernel_basis

    if numerical_rank > 0:
        condition_number_resolved = float(
            singular_values_domain[0] / singular_values_domain[numerical_rank - 1]
        )
    else:
        condition_number_resolved = None

    return IdentifiabilityResult(
        singular_values_raw=singular_values_raw,
        singular_values_domain=singular_values_domain,
        rank_tolerance=rank_tolerance,
        numerical_rank=numerical_rank,
        kernel_basis=kernel_basis,
        kernel_projector=kernel_projector,
        condition_number_resolved=condition_number_resolved,
    )
