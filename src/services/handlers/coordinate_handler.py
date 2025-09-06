#!/usr/bin/env python3
"""
Coordinate Handler - V2 Compliance Module
========================================

Handles agent coordinate management and validation.
Extracted from messaging_cli_handlers_orchestrator.py for V2 compliance.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

import time
from typing import Any, Dict, List, Optional
import logging

# Import messaging models and utilities with fallback
try:
    from ..models.messaging_models import RecipientType, SenderType
    from ..unified_messaging_imports import COORDINATE_CONFIG_FILE
    from ...core.unified_data_processing_system import read_json, write_json
except ImportError:
    # Fallback implementations
    COORDINATE_CONFIG_FILE = "config/coordinates.json"

    def read_json(path):
        return {}

    def write_json(path, data):
        pass


class CoordinateHandler:
    """Handler for agent coordinate management and validation."""

    def __init__(self):
        """Initialize coordinate handler."""
        self.logger = logging.getLogger(__name__)
        self.coordinates_cache: Dict[str, List[int]] = {}
        self.last_coordinate_load: Optional[float] = None
        self.cache_ttl_seconds = 300  # 5 minutes

    async def load_coordinates_async(self, service=None) -> Dict[str, Any]:
        """Load agent coordinates asynchronously with caching.

        Args:
            service: Messaging service instance (optional)

        Returns:
            Dict containing coordinate data and success status
        """
        try:
            # Check cache validity
            current_time = time.time()
            if (
                self.last_coordinate_load
                and self.coordinates_cache
                and (current_time - self.last_coordinate_load) < self.cache_ttl_seconds
            ):

                return {
                    "success": True,
                    "coordinates": self.coordinates_cache,
                    "agent_count": len(self.coordinates_cache),
                    "cached": True,
                }

            # Load fresh coordinates
            coords_data = read_json(COORDINATE_CONFIG_FILE)
            coordinates = {}

            if "agents" in coords_data:
                for agent_id, agent_data in coords_data["agents"].items():
                    coordinates[agent_id] = agent_data.get(
                        "chat_input_coordinates", [0, 0]
                    )

            # Update cache
            self.coordinates_cache = coordinates
            self.last_coordinate_load = current_time

            return {
                "success": True,
                "coordinates": coordinates,
                "agent_count": len(coordinates),
                "cached": False,
            }

        except Exception as e:
            self.logger.error(f"Error loading coordinates: {e}")
            return {"success": False, "error": str(e)}

    def print_coordinates_table(self, coordinates: Dict[str, List[int]]) -> None:
        """Print formatted coordinates table."""
        try:
            print("\n📍 Agent Coordinates:")
            print("=" * 40)
            print(f"{'Agent':<12} {'X':<8} {'Y':<8}")
            print("-" * 40)

            for agent_id, coords in sorted(coordinates.items()):
                x, y = coords if len(coords) >= 2 else [0, 0]
                print(f"{agent_id:<12} {x:<8} {y:<8}")

            print("=" * 40)
            print(f"Total agents: {len(coordinates)}")

        except Exception as e:
            self.logger.error(f"Error printing coordinates table: {e}")

    def get_agent_coordinates(self, agent_id: str) -> Optional[List[int]]:
        """Get coordinates for specific agent."""
        return self.coordinates_cache.get(agent_id)

    def validate_coordinates(self, coordinates: List[int]) -> bool:
        """Validate coordinate format."""
        return (
            isinstance(coordinates, list)
            and len(coordinates) >= 2
            and all(isinstance(coord, (int, float)) for coord in coordinates[:2])
        )

    def clear_cache(self) -> None:
        """Clear coordinate cache."""
        self.coordinates_cache.clear()
        self.last_coordinate_load = None
        self.logger.info("Coordinate cache cleared")
