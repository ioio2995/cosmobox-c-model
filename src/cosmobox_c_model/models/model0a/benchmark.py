"""End-to-end assembly of the Toy Model 0A benchmark
(docs/toy-models/toy0/implementation-design.md Sections 17-31).

This module computes results from the frozen definitions; it never uses an
analytic oracle to fabricate a result -- oracles live exclusively in
tests/models/model0a/.
"""

from __future__ import annotations

from typing import Any

import numpy as np

from cosmobox_c_model.core.identifiability import analyze_identifiability, build_measurement_matrix
from cosmobox_c_model.models.model0a import constants
from cosmobox_c_model.models.model0a.basis_config import build_total_basis
from cosmobox_c_model.models.model0a.observables import (
    build_families,
    build_f2_prime,
    build_f_delta,
    build_hs_basis,
    build_physical_observables,
    build_physical_occupations,
)


def _analyze_family(
    name: str,
    family: tuple[np.ndarray, ...],
    hs_basis: tuple[np.ndarray, ...],
) -> dict[str, Any]:
    matrix = build_measurement_matrix(family, hs_basis, imag_atol=constants.MEASUREMENT_IMAG_ATOL)
    result = analyze_identifiability(matrix, rank_tolerance=constants.RANK_EPSILON)

    raw = result.singular_values_raw
    condition_number_compact = None
    if raw.size >= 2 and float(np.min(raw)) > 0:
        condition_number_compact = float(np.max(raw) / np.min(raw))

    return {
        "name": name,
        "observable_order": [str(i) for i in range(len(family))],
        "measurement_matrix": matrix.tolist(),
        "singular_values_raw": raw.tolist(),
        "singular_values_domain": result.singular_values_domain.tolist(),
        "rank_epsilon": result.rank_tolerance,
        "numerical_rank": result.numerical_rank,
        "kernel_dimension_epsilon": int(result.kernel_basis.shape[0]),
        "kernel_projector": result.kernel_projector.real.tolist(),
        "condition_number_resolved": result.condition_number_resolved,
        "condition_number_compact": condition_number_compact,
    }


def run_benchmark_0a() -> dict[str, Any]:
    """Assemble the full 0A pipeline and return a JSON-serializable report
    following the schema of implementation-design.md Section 31."""
    basis = build_total_basis()
    observables = build_physical_observables(basis)
    occupations = build_physical_occupations(basis, observables["inclusion"])
    hs_basis = build_hs_basis(observables)
    families = build_families(basis, occupations, observables)
    f2_prime = build_f2_prime(basis, occupations, observables)

    family_reports = {
        name: _analyze_family(name, family, hs_basis) for name, family in families.items()
    }
    family_reports["F2_prime"] = _analyze_family("F2_prime", f2_prime, hs_basis)

    conditioning_sweep = []
    for delta in constants.F_DELTA_SWEEP:
        f_delta = build_f_delta(observables, delta)
        entry = _analyze_family(f"F_delta(delta={delta!r})", f_delta, hs_basis)
        entry["delta"] = delta
        conditioning_sweep.append(entry)

    composition_full_frobenius = float(
        np.linalg.norm(
            (observables["O_01_total"] @ observables["O_12_total"]) - observables["O_02_total"],
            ord="fro",
        )
    )

    return {
        "schema_version": "0a-benchmark-v1",
        "model": "toy-model-0a",
        "dimensions": {
            "total": basis.dimension,
            "physical": int(observables["inclusion"].shape[1]),
            "identifiability_domain": len(hs_basis),
        },
        "tolerances": {
            "exact_matrix_atol": constants.EXACT_MATRIX_ATOL,
            "commutator_atol": constants.COMMUTATOR_ATOL,
            "hermiticity_atol": constants.HERMITICITY_ATOL,
            "measurement_imag_atol": constants.MEASUREMENT_IMAG_ATOL,
            "singular_value_atol": constants.SINGULAR_VALUE_ATOL,
            "expectation_atol": constants.EXPECTATION_ATOL,
            "rank_epsilon": constants.RANK_EPSILON,
            "kernel_projector_frobenius_tol": constants.KERNEL_PROJECTOR_FROBENIUS_TOL,
        },
        "defects": {
            "composition_full_frobenius": composition_full_frobenius,
        },
        "families": family_reports,
        "conditioning_sweep": conditioning_sweep,
    }
