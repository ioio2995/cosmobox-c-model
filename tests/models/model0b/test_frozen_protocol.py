"""Tests for the Toy Model 0B frozen protocol identity module
(implementation-only skeleton, no physics)."""

from __future__ import annotations

from cosmobox_c_model.models.model0b import frozen_protocol


def test_model0b_package_importable():
    import cosmobox_c_model.models.model0b as model0b

    assert model0b is not None


def test_model_id():
    assert frozen_protocol.MODEL_ID == "model0b"


def test_model_status_is_frozen():
    assert frozen_protocol.MODEL_STATUS == "FROZEN"


def test_freeze_base_commit():
    assert (
        frozen_protocol.FREEZE_BASE_COMMIT
        == "d796c65d2538eaba2be7882647ba91db5cf93a32"
    )


def test_freeze_record_commit():
    assert (
        frozen_protocol.FREEZE_RECORD_COMMIT
        == "1ae0906ef8e657147d50d9eb3f499cc53601efa3"
    )


def test_freeze_record_reference():
    assert (
        frozen_protocol.FREEZE_RECORD_REFERENCE
        == "docs/toy-models/toy0b/freeze-record.md"
    )
