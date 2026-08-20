"""Structural invariant: core (and tests/core) never import models
(software-architecture-governance.md Sections 6, 6.1, 19.1)."""

from __future__ import annotations

import ast
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CORE_SRC = REPO_ROOT / "src" / "cosmobox_c_model" / "core"
CORE_TESTS = REPO_ROOT / "tests" / "core"

FORBIDDEN_PREFIX = "cosmobox_c_model.models"


def _imports_models(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    offenders: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.startswith(FORBIDDEN_PREFIX):
                    offenders.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            if module.startswith(FORBIDDEN_PREFIX):
                offenders.append(module)
    return offenders


def _check_directory(directory: Path) -> dict[str, list[str]]:
    violations: dict[str, list[str]] = {}
    for path in directory.rglob("*.py"):
        offenders = _imports_models(path)
        if offenders:
            violations[str(path.relative_to(REPO_ROOT))] = offenders
    return violations


def test_core_does_not_import_models():
    violations = _check_directory(CORE_SRC)
    assert not violations, f"core modules importing models: {violations}"


def test_core_tests_do_not_import_models():
    violations = _check_directory(CORE_TESTS)
    assert not violations, f"tests/core importing models: {violations}"
