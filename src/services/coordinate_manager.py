"""
Coordinate Manager - V2 Compliant Main Interface
================================================

Main interface for coordinate management system.
V2 Compliance: ≤400 lines, single responsibility, KISS principle
"""

from dataclasses import dataclass
from typing import Any

from .coordinate_manager_core import (
    CoordinateBatchProcessor,
    CoordinateCalculator,
    CoordinateFilterCore,
)
from .coordinate_manager_models import (
    CoordinateBatch,
    CoordinateFilter,
)


@dataclass
class CoordinateOperationParams:
    """Coordinate operation parameters."""

    operation: str
    coord1: Any
    coord2: Any = None
    coord3: Any = None
    t: float = 0.0


class CoordinateManager:
    """Main coordinate manager interface."""

    def __init__(self):
        """Initialize coordinate manager."""
        self.calculator = CoordinateCalculator()
        self.filter_system = CoordinateFilterCore()
        self.batch_processor = CoordinateBatchProcessor()

    def calculate_coordinate_operations(self, params: CoordinateOperationParams) -> Any:
        """Calculate coordinate operations."""
        if params.operation == "distance" and params.coord2:
            return self.calculator.calculate_distance(params.coord1, params.coord2)
        elif params.operation == "angle" and params.coord2 and params.coord3:
            return self.calculator.calculate_angle(params.coord1, params.coord2, params.coord3)
        elif params.operation == "normalize":
            return self.calculator.normalize_coordinate(params.coord1)
        elif params.operation == "interpolate" and params.coord2:
            return self.calculator.interpolate_coordinates(params.coord1, params.coord2, params.t)
        else:
            return params.coord1

    def add_filter(
        self, name: str, filter_type: CoordinateFilter, parameters: dict[str, Any]
    ) -> bool:
        """Add coordinate filter."""
        return self.filter_system.add_filter(name, filter_type, parameters)

    def apply_filters(self, coordinates: list[Any]) -> list[Any]:
        """Apply all filters to coordinates."""
        return self.filter_system.apply_filters(coordinates)

    def add_batch(self, batch: CoordinateBatch) -> bool:
        """Add batch to processing queue."""
        return self.batch_processor.add_batch(batch)

    def process_batch(self, batch: CoordinateBatch) -> dict[str, Any]:
        """Process coordinate batch."""
        return self.batch_processor.process_batch(batch)

    def get_processing_stats(self) -> dict[str, Any]:
        """Get processing statistics."""
        return self.batch_processor.get_processing_stats()


# Global instance for backward compatibility
coordinate_manager = CoordinateManager()


def main():
    """Main function for testing."""
    manager = CoordinateManager()
    print("Coordinate Manager utilities initialized")
    print(f"Processing stats: {manager.get_processing_stats()}")


if __name__ == "__main__":
    main()
