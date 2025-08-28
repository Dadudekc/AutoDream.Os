"""Common validation helpers for middleware components."""

from __future__ import annotations

from typing import Any

from ..models import DataPacket


def has_tag(packet: DataPacket, tag: str) -> bool:
    """Return True if packet has the specified tag."""
    return tag in packet.tags


def metadata_equals(packet: DataPacket, key: str, value: Any) -> bool:
    """Check if packet metadata key equals value."""
    return packet.metadata.get(key) == value


def metadata_exists(packet: DataPacket, key: str) -> bool:
    """Check if packet metadata key exists and is truthy."""
    return bool(packet.metadata.get(key))


def source_equals(packet: DataPacket, source: str) -> bool:
    """Check if packet source equals given source."""
    return packet.source == source


def validate_field(value: Any, rule: str, constraint: Any) -> bool:
    """Validate a field according to the specified rule."""
    if rule == "required":
        return value is not None and value != ""
    if rule == "min_length" and isinstance(value, str):
        return len(value) >= constraint
    if rule == "max_length" and isinstance(value, str):
        return len(value) <= constraint
    if rule == "min_value" and isinstance(value, (int, float)):
        return value >= constraint
    if rule == "max_value" and isinstance(value, (int, float)):
        return value <= constraint
    if rule == "type" and constraint == "string":
        return isinstance(value, str)
    if rule == "type" and constraint == "number":
        return isinstance(value, (int, float))
    return True
