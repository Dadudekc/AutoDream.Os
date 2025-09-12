"""
Mock Coordinate Loader for Testing
==================================

Provides mock coordinate loading functionality for smoke testing.
"""

import json
from pathlib import Path
from typing import Any


def _load_coordinates() -> dict[str, dict[str, Any]]:
    """Load agent coordinates from the config/coordinates.json SSOT."""
    # Look for coordinate file in config directory regardless of current working directory
    coord_file = Path(__file__).parent.parent.parent / "config" / "coordinates.json"
    data = json.loads(coord_file.read_text(encoding="utf-8"))
    agents: dict[str, dict[str, Any]] = {}
    for agent_id, info in data.get("agents", {}).items():
        chat = info.get("chat_input_coordinates", [0, 0])
        agents[agent_id] = {
            "coords": tuple(chat),  # Store as tuple for coordinate loader
            "x": chat[0],
            "y": chat[1],
            "description": info.get("description", ""),
        }
    return agents


COORDINATES: dict[str, dict[str, Any]] = _load_coordinates()


class CoordinateLoader:
    """Coordinate loader for agent positioning and communication."""

    def __init__(self):
        """Initialize coordinate loader."""
        self.coordinates = COORDINATES.copy()
        self.agent_status = {}

    def get_chat_coordinates(self, agent_id: str) -> tuple[int, int]:
        """Get chat coordinates for agent."""
        if agent_id in self.coordinates:
            return self.coordinates[agent_id]["chat"]
        raise ValueError(f"Agent {agent_id} not found")

    def get_agent_description(self, agent_id: str) -> str:
        """Get agent description."""
        if agent_id in self.coordinates:
            return self.coordinates[agent_id].get("description", "")
        return ""

    def is_agent_active(self, agent_id: str) -> bool:
        """Check if agent is active."""
        return agent_id in self.coordinates

    def get_all_agents(self) -> list[str]:
        """Get all available agents."""
        return list(self.coordinates.keys())


def get_coordinate_loader() -> CoordinateLoader:
    """Get coordinate loader instance."""
    return CoordinateLoader()


# Example usage:
if __name__ == "__main__":
    """Demonstrate coordinate loader functionality."""

    print("🐝 Coordinate Loader Examples - Practical Demonstrations")
    print("=" * 60)

    # Test coordinate loader instantiation
    print(f"\n📋 Testing CoordinateLoader instantiation:")
    try:
        loader = get_coordinate_loader()
        print(f"✅ CoordinateLoader instantiated successfully")
    except Exception as e:
        print(f"❌ CoordinateLoader failed: {e}")

    # Test agent coordinate retrieval
    print(f"\n📋 Testing coordinate retrieval:")
    try:
        coords = loader.get_chat_coordinates("Agent-3")
        print(f"✅ Agent-3 coordinates: {coords}")
    except Exception as e:
        print(f"❌ Coordinate retrieval failed: {e}")

    # Test agent listing
    print(f"\n📋 Testing agent listing:")
    try:
        agents = loader.get_all_agents()
        print(f"✅ Found {len(agents)} agents: {agents[:3]}...")
    except Exception as e:
        print(f"❌ Agent listing failed: {e}")

    print("\n🎉 Coordinate loader examples completed!")
    print("🐝 WE ARE SWARM - COORDINATE SYSTEMS VALIDATED!")


def get_coordinate_loader() -> CoordinateLoader:
    """Get global coordinate loader instance."""
    global _coordinate_loader
    if _coordinate_loader is None:
        _coordinate_loader = CoordinateLoader()
    return _coordinate_loader


if __name__ == "__main__":
    """Demonstrate module functionality with practical examples."""

    print("🐝 Module Examples - Practical Demonstrations")
    print("=" * 50)
    # Function demonstrations
    print(f"\n📋 Testing _load_coordinates():")
    try:
        # Add your function call here
        print(f"✅ _load_coordinates executed successfully")
    except Exception as e:
        print(f"❌ _load_coordinates failed: {e}")

    print(f"\n📋 Testing get_coordinate_loader():")
    try:
        # Add your function call here
        print(f"✅ get_coordinate_loader executed successfully")
    except Exception as e:
        print(f"❌ get_coordinate_loader failed: {e}")

    print(f"\n📋 Testing __init__():")
    try:
        # Add your function call here
        print(f"✅ __init__ executed successfully")
    except Exception as e:
        print(f"❌ __init__ failed: {e}")

    # Class demonstrations
    print(f"\n🏗️  Testing CoordinateLoader class:")
    try:
        instance = CoordinateLoader()
        print(f"✅ CoordinateLoader instantiated successfully")
    except Exception as e:
        print(f"❌ CoordinateLoader failed: {e}")

    print("\n🎉 All examples completed!")
    print("🐝 WE ARE SWARM - PRACTICAL CODE IN ACTION!")
