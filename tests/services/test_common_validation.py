import pytest

from services.middleware.components.common_validation import (
    has_tag,
    metadata_equals,
    metadata_exists,
    source_equals,
    validate_field,
)
from services.middleware.models import DataPacket


def test_validate_field_rules():
    assert validate_field("abc", "required", None)
    assert not validate_field("", "required", None)
    assert validate_field("abc", "min_length", 2)
    assert not validate_field("a", "min_length", 2)
    assert validate_field("abc", "max_length", 5)
    assert not validate_field("abcdef", "max_length", 5)
    assert validate_field(5, "min_value", 3)
    assert not validate_field(2, "min_value", 3)
    assert validate_field(5, "max_value", 10)
    assert not validate_field(15, "max_value", 10)
    assert validate_field("abc", "type", "string")
    assert not validate_field(123, "type", "string")
    assert validate_field(5, "type", "number")
    assert not validate_field("abc", "type", "number")


def test_packet_helpers():
    packet = DataPacket(
        id="1", data="", metadata={"key": "value", "flag": True}, source="src"
    )
    packet.tags.add("tag1")

    assert has_tag(packet, "tag1")
    assert not has_tag(packet, "tag2")

    assert metadata_equals(packet, "key", "value")
    assert not metadata_equals(packet, "key", "other")

    assert metadata_exists(packet, "flag")
    assert not metadata_exists(packet, "missing")

    assert source_equals(packet, "src")
    assert not source_equals(packet, "other")
