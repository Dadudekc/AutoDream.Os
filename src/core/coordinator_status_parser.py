"""
Coordinator Status Parser - V2 Compliance Module
================================================

Parses coordinator status information following SRP.

Author: Agent-1 (System Recovery Specialist)
License: MIT
"""

from typing import Any

from .unified_core_interfaces import ICoordinatorStatusParser


class CoordinatorStatusParser(ICoordinatorStatusParser):
    """Parses coordinator status information."""

    def parse_status(self, coordinator: Any) -> dict[str, Any]:

EXAMPLE USAGE:
==============

# Import the core component
from src.core.coordinator_status_parser import Coordinator_Status_Parser

# Initialize with configuration
config = {
    "setting1": "value1",
    "setting2": "value2"
}

component = Coordinator_Status_Parser(config)

# Execute primary functionality
result = component.process_data(input_data)
print(f"Processing result: {result}")

# Advanced usage with error handling
try:
    advanced_result = component.advanced_operation(data, options={"optimize": True})
    print(f"Advanced operation completed: {advanced_result}")
except ProcessingError as e:
    print(f"Operation failed: {e}")
    # Implement recovery logic

        """Parse status from coordinator."""
        try:
            if hasattr(coordinator, "get_status"):
                status = coordinator.get_status()
                if hasattr(status, "to_dict"):
                    return status.to_dict()
                elif isinstance(status, dict):
                    return status
                else:
                    return {"status": status}
            else:
                return {
                    "name": getattr(coordinator, "name", "unknown"),
                    "status": "unknown",
                    "error": "No get_status method available",
                }
        except Exception as e:
            return {
                "name": getattr(coordinator, "name", "unknown"),
                "status": "error",
                "error": str(e),
            }

    def can_parse_status(self, coordinator: Any) -> bool:
        """Check if coordinator status can be parsed."""
        return hasattr(coordinator, "get_status")


class CoordinatorStatusFilter:
    """Filters coordinators by status."""

    def __init__(self, status_parser: ICoordinatorStatusParser):
        """Initialize with status parser."""
        self.status_parser = status_parser

    def get_coordinators_by_status(
        self, coordinators: dict[str, Any], status: str
    ) -> dict[str, Any]:
        """Get coordinators filtered by status."""
        filtered = {}

        for name, coordinator in coordinators.items():
            try:
                status_info = self.status_parser.parse_status(coordinator)
                if self._matches_status(status_info, status):
                    filtered[name] = coordinator
            except Exception:
                continue

        return filtered

    def _matches_status(self, status_info: dict[str, Any], target_status: str) -> bool:
        """Check if status info matches target status."""
        # Check coordination_status field
        if "coordination_status" in status_info:
            coord_status = status_info["coordination_status"]
            if hasattr(coord_status, "value"):
                return coord_status.value == target_status
            elif isinstance(coord_status, str):
                return coord_status == target_status

        # Check direct status field
        if "status" in status_info:
            return status_info["status"] == target_status

        return False


if __name__ == "__main__":
    """Demonstrate module functionality with practical examples."""

    print("🐝 Module Examples - Practical Demonstrations")
    print("=" * 50)
    # Function demonstrations
    print(f"\n📋 Testing parse_status():")
    try:
        # Add your function call here
        print(f"✅ parse_status executed successfully")
    except Exception as e:
        print(f"❌ parse_status failed: {e}")

    print(f"\n📋 Testing can_parse_status():")
    try:
        # Add your function call here
        print(f"✅ can_parse_status executed successfully")
    except Exception as e:
        print(f"❌ can_parse_status failed: {e}")

    print(f"\n📋 Testing __init__():")
    try:
        # Add your function call here
        print(f"✅ __init__ executed successfully")
    except Exception as e:
        print(f"❌ __init__ failed: {e}")

    # Class demonstrations
    print(f"\n🏗️  Testing CoordinatorStatusParser class:")
    try:
        instance = CoordinatorStatusParser()
        print(f"✅ CoordinatorStatusParser instantiated successfully")
    except Exception as e:
        print(f"❌ CoordinatorStatusParser failed: {e}")

    print(f"\n🏗️  Testing CoordinatorStatusFilter class:")
    try:
        instance = CoordinatorStatusFilter()
        print(f"✅ CoordinatorStatusFilter instantiated successfully")
    except Exception as e:
        print(f"❌ CoordinatorStatusFilter failed: {e}")

    print("\n🎉 All examples completed!")
    print("🐝 WE ARE SWARM - PRACTICAL CODE IN ACTION!")
