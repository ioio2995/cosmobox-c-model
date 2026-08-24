"""Frozen protocol identity for Toy Model 0B.

This module contains no physics and no numerical protocol values. It
executes no campaign. It only identifies the frozen Model 0B
scientific/protocol source: which model this package implements, that its
specification/validation-plan status is frozen, and the exact commits at
which that freeze occurred.

Mutable governance/workflow state (e.g. implementation branch, current
authorization booleans) does not belong here: this module identifies the
immutable frozen protocol, not mutable governance state.
"""

from __future__ import annotations

MODEL_ID = "model0b"

MODEL_STATUS = "FROZEN"

FREEZE_BASE_COMMIT = (
    "d796c65d2538eaba2be7882647ba91db5cf93a32"
)

FREEZE_RECORD_COMMIT = (
    "1ae0906ef8e657147d50d9eb3f499cc53601efa3"
)

FREEZE_RECORD_REFERENCE = (
    "docs/toy-models/toy0b/freeze-record.md"
)
