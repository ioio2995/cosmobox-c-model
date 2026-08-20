"""Model-specific observables, Hilbert-Schmidt basis, measurement families and
witness states for Toy Model 0A
(docs/toy-models/toy0/implementation-design.md Sections 12-27).
"""

from __future__ import annotations

import numpy as np

from cosmobox_c_model.core.operators import hermitian_parts
from cosmobox_c_model.core.state_space import Basis, restrict_operator
from cosmobox_c_model.models.model0a.operators import (
    build_annihilation_operator,
    build_creation_operator,
    build_relational_operators,
    select_physical_inclusion,
)

SQRT2 = float(np.sqrt(2))
SQRT6 = float(np.sqrt(6))

# Jordan-Wigner witness (implementation-design.md Section 14.1).
CHI_STATE: tuple[int, ...] = (0, 1, 1, 0, -1)  # |011;0,-1>
CHI_TARGET_STATE: tuple[int, ...] = (1, 1, 0, 1, 0)  # |110;+1,0>

# Physical witness states, in the (L, M, R) coordinate basis
# (implementation-design.md Section 24).
WITNESS_STATES: dict[str, np.ndarray] = {
    "psi_plus": np.array([1, 0, 1], dtype=complex) / SQRT2,
    "psi_minus": np.array([1, 0, -1], dtype=complex) / SQRT2,
    "psi_plus_i": np.array([1, 0, 1j], dtype=complex) / SQRT2,
    "psi_minus_i": np.array([1, 0, -1j], dtype=complex) / SQRT2,
}


def build_physical_observables(basis: Basis) -> dict[str, np.ndarray]:
    """Restrict O_01, O_12, O_02 to the physical (L, M, R) sector and derive their
    hermitian parts X_ij, Y_ij."""
    inclusion = select_physical_inclusion(basis)
    o01_total, o12_total, o02_total = build_relational_operators(basis)

    o01 = restrict_operator(o01_total, inclusion)
    o12 = restrict_operator(o12_total, inclusion)
    o02 = restrict_operator(o02_total, inclusion)

    x01, y01 = hermitian_parts(o01)
    x12, y12 = hermitian_parts(o12)
    x02, y02 = hermitian_parts(o02)

    return {
        "inclusion": inclusion,
        "O_01": o01,
        "O_12": o12,
        "O_02": o02,
        "O_01_total": o01_total,
        "O_12_total": o12_total,
        "O_02_total": o02_total,
        "X_01": x01,
        "Y_01": y01,
        "X_12": x12,
        "Y_12": y12,
        "X_02": x02,
        "Y_02": y02,
    }


def build_physical_occupations(basis: Basis, inclusion: np.ndarray) -> dict[str, np.ndarray]:
    """Restrict n_0, n_1, n_2 to the physical (L, M, R) sector
    (implementation-design.md Section 11)."""
    occupations = {}
    for site in (0, 1, 2):
        n_total = build_creation_operator(basis, site) @ build_annihilation_operator(basis, site)
        occupations[f"n_{site}"] = restrict_operator(n_total, inclusion)
    return occupations


def build_hs_basis(observables: dict[str, np.ndarray]) -> tuple[np.ndarray, ...]:
    """Frozen orthonormal Hilbert-Schmidt traceless basis B1...B8
    (implementation-design.md Section 15)."""
    l = np.array([[1, 0, 0], [0, 0, 0], [0, 0, 0]], dtype=complex)
    m = np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]], dtype=complex)
    r = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 1]], dtype=complex)

    b1 = (l - m) / SQRT2
    b2 = (l + m - 2 * r) / SQRT6
    b3 = SQRT2 * observables["X_01"]
    b4 = SQRT2 * observables["Y_01"]
    b5 = SQRT2 * observables["X_12"]
    b6 = SQRT2 * observables["Y_12"]
    b7 = SQRT2 * observables["X_02"]
    b8 = SQRT2 * observables["Y_02"]
    return (b1, b2, b3, b4, b5, b6, b7, b8)


def build_families(
    basis: Basis,
    occupations: dict[str, np.ndarray],
    observables: dict[str, np.ndarray],
) -> dict[str, tuple[np.ndarray, ...]]:
    """Frozen ordered families F1, F2, F3 (implementation-design.md Section 17)."""
    n0, n1, n2 = occupations["n_0"], occupations["n_1"], occupations["n_2"]
    x01, y01 = observables["X_01"], observables["Y_01"]
    x12, y12 = observables["X_12"], observables["Y_12"]
    x02, y02 = observables["X_02"], observables["Y_02"]

    f1 = (n0, n1, n2)
    f2 = (n0, n1, n2, x01, y01, x12, y12)
    f3 = (n0, n1, n2, x01, y01, x12, y12, x02, y02)
    return {"F1": f1, "F2": f2, "F3": f3}


def build_f2_prime(
    basis: Basis,
    occupations: dict[str, np.ndarray],
    observables: dict[str, np.ndarray],
) -> tuple[np.ndarray, ...]:
    """Pipeline-control family F2_prime (implementation-design.md Section 25):
    a plumbing test only, never a scientific result on its own."""
    inclusion = observables["inclusion"]
    o_comp_total = observables["O_01_total"] @ observables["O_12_total"]
    o_comp = restrict_operator(o_comp_total, inclusion)
    x_comp, y_comp = hermitian_parts(o_comp)

    n0, n1, n2 = occupations["n_0"], occupations["n_1"], occupations["n_2"]
    x01, y01 = observables["X_01"], observables["Y_01"]
    x12, y12 = observables["X_12"], observables["Y_12"]
    return (n0, n1, n2, x01, y01, x12, y12, x_comp, y_comp)


def build_f_delta(observables: dict[str, np.ndarray], delta: float) -> tuple[np.ndarray, np.ndarray]:
    """Purely instrumental conditioning control F_delta
    (implementation-design.md Section 26): no physical interpretation of its own."""
    x01, y01 = observables["X_01"], observables["Y_01"]
    return (x01, x01 + delta * y01)
