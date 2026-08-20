"""Structural invariant: every public core module exposes a valid
SCIENTIFIC_METADATA, and normative_reference (when present) points to a real
file, with a matching heading when an anchor is given
(software-architecture-governance.md Sections 5.1, 5.2, 19.2)."""

from __future__ import annotations

import importlib
import pkgutil
import re
from pathlib import Path

import pytest

from cosmobox_c_model import core as core_package

ALLOWED_STATUSES = {"established", "project-defined"}

REPO_ROOT = Path(__file__).resolve().parents[2]


def _iter_core_modules():
    for module_info in pkgutil.iter_modules(core_package.__path__, core_package.__name__ + "."):
        leaf_name = module_info.name.rsplit(".", 1)[-1]
        if leaf_name.startswith("_"):
            continue
        yield importlib.import_module(module_info.name)


def _parse_reference(reference: str) -> tuple[str, str | None]:
    if "#" in reference:
        path_part, anchor = reference.split("#", 1)
        return path_part, anchor
    return reference, None


def _heading_slugs(document_path: Path) -> set[str]:
    slugs = set()
    for line in document_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("#"):
            title = line.lstrip("#").strip()
            slug = re.sub(r"[^a-z0-9\- ]", "", title.lower()).strip().replace(" ", "-")
            slugs.add(slug)
    return slugs


CORE_MODULES = list(_iter_core_modules())


@pytest.mark.parametrize("module", CORE_MODULES, ids=lambda m: m.__name__)
def test_core_module_has_valid_scientific_metadata(module):
    assert hasattr(module, "SCIENTIFIC_METADATA"), f"{module.__name__} is missing SCIENTIFIC_METADATA"
    metadata = module.SCIENTIFIC_METADATA

    status = metadata.get("status")
    assert status in ALLOWED_STATUSES, f"{module.__name__}: invalid status {status!r}"

    if status == "project-defined":
        assert metadata.get("origin_model") is not None, (
            f"{module.__name__}: origin_model required for project-defined"
        )
        assert metadata.get("normative_reference") is not None, (
            f"{module.__name__}: normative_reference required for project-defined"
        )

    # Any normative_reference actually present must be valid, regardless of
    # status: a stale or broken reference must fail even on a module whose
    # status does not strictly require one.
    normative_reference = metadata.get("normative_reference")
    if normative_reference is not None:
        reference_path, anchor = _parse_reference(normative_reference)
        target = REPO_ROOT / reference_path
        assert target.is_file(), f"{module.__name__}: normative_reference file not found: {reference_path}"

        if anchor:
            slugs = _heading_slugs(target)
            assert anchor in slugs, f"{module.__name__}: anchor #{anchor} not found in {reference_path}"


def test_at_least_one_core_module_was_discovered():
    # Guards against the discovery mechanism silently finding nothing.
    assert CORE_MODULES
