"""Coordinate data structures and capture interface."""

from dataclasses import dataclass
from typing import Optional, Tuple, Protocol


@dataclass
class CoordinateData:
    """Data structure for agent coordinates."""

    agent_id: str
    mode: str
    input_box: Tuple[int, int]
    starter_location: Tuple[int, int]


class CoordinateCaptureInterface(Protocol):
    """Interface for coordinate capture operations."""

    def capture_agent_coordinates(
        self, agent_name: str, mode: str = "8-agent"
    ) -> Optional[CoordinateData]:
        """Capture coordinates for a specific agent."""
        ...
