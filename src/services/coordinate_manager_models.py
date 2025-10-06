"""
Coordinate Manager Models - V2 Compliant
========================================

Data models for coordinate management system.
V2 Compliance: ≤400 lines, ≤5 classes, KISS principle
"""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any


class CoordinateOperation(Enum):
    """Coordinate operation enumeration."""

    ADD = "add"
    SUBTRACT = "subtract"
    MULTIPLY = "multiply"
    DIVIDE = "divide"
    DISTANCE = "distance"
    NORMALIZE = "normalize"


class CoordinateFilter(Enum):
    """Coordinate filter enumeration."""

    BY_TYPE = "by_type"
    BY_SYSTEM = "by_system"
    BY_RANGE = "by_range"
    BY_TIMESTAMP = "by_timestamp"


@dataclass
class CoordinateRange:
    """Coordinate range data structure."""

    min_x: float
    max_x: float
    min_y: float
    max_y: float
    min_z: float = 0.0
    max_z: float = 0.0
    name: str = "default"


@dataclass
class CoordinateBatch:
    """Coordinate batch data structure."""

    coordinates: list[tuple[str, Any]]  # (coord_id, coordinate)
    operation: CoordinateOperation
    parameters: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))

