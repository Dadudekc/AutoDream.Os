"""Coordinate management interface."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple


class ICoordinateManager(ABC):
    """Interface for coordinate management."""

    @abstractmethod
    def get_agent_coordinates(self, agent_id: str, mode: str) -> Optional[Any]:
        """Get coordinates for a specific agent."""
        raise NotImplementedError(
            "get_agent_coordinates must be implemented by subclasses"
        )

    @abstractmethod
    def validate_coordinates(self) -> Dict[str, Any]:
        """Validate all loaded coordinates."""
        raise NotImplementedError(
            "validate_coordinates must be implemented by subclasses"
        )

    @abstractmethod
    def get_available_modes(self) -> List[str]:
        """Get available coordinate modes."""
        raise NotImplementedError(
            "get_available_modes must be implemented by subclasses"
        )

    @abstractmethod
    def get_agents_in_mode(self, mode: str) -> List[str]:
        """Get agents in a specific mode."""
        raise NotImplementedError(
            "get_agents_in_mode must be implemented by subclasses"
        )

    @abstractmethod
    def map_coordinates(self, mode: str = "8-agent") -> Dict[str, Any]:
        """Map and display coordinate information for debugging."""
        raise NotImplementedError("map_coordinates must be implemented by subclasses")

    @abstractmethod
    def calibrate_coordinates(
        self,
        agent_id: str,
        input_coords: Tuple[int, int],
        starter_coords: Tuple[int, int],
        mode: str = "8-agent",
    ) -> bool:
        """Calibrate coordinates for a specific agent."""
        raise NotImplementedError(
            "calibrate_coordinates must be implemented by subclasses"
        )

    @abstractmethod
    def consolidate_coordinate_files(self) -> Dict[str, Any]:
        """Consolidate multiple coordinate files."""
        raise NotImplementedError(
            "consolidate_coordinate_files must be implemented by subclasses"
        )
