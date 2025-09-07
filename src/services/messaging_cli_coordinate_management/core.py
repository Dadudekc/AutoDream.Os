"""Facade for coordinate management operations."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from ..messaging_cli_utils import MessagingCLIUtils
from .coordinate_capture import CoordinateCapture
from .coordinate_repository import CoordinateRepository
from .coordinate_setter import CoordinateSetter


class MessagingCLICoordinateManagement:
    """High-level API for managing messaging CLI coordinates."""

    def __init__(self, coords_file: str = "cursor_agent_coords.json") -> None:
        utils = MessagingCLIUtils()
        repository = CoordinateRepository(utils=utils, file_path=coords_file)
        self.repository = repository
        self.setter = CoordinateSetter(repository, utils)
        self.capture = CoordinateCapture(repository)

    # Delegate setters
    def set_onboarding_coordinates(self, coord_string: str) -> Dict[str, Any]:
        return self.setter.set_onboarding_coordinates(coord_string)

    def set_chat_coordinates(self, coord_string: str) -> Dict[str, Any]:
        return self.setter.set_chat_coordinates(coord_string)

    def update_coordinates_from_file(self, file_path: str) -> Dict[str, Any]:
        return self.setter.update_coordinates_from_file(file_path)

    # Delegate capture operations
    def interactive_coordinate_capture(self, agent_id: Optional[str] = None) -> Dict[str, Any]:
        return self.capture.interactive_coordinate_capture(agent_id)

    def capture_onboarding_only(self, agent_id: Optional[str] = None) -> Dict[str, Any]:
        return self.capture.capture_onboarding_only(agent_id)

    def capture_chat_only(self, agent_id: Optional[str] = None) -> Dict[str, Any]:
        return self.capture.capture_chat_only(agent_id)

    # Delegate repository operations
    def update_agent_coordinates(
        self, agent_id: str, onboarding_coords: List[int], chat_coords: List[int]
    ) -> Dict[str, Any]:
        return self.repository.update_agent_coordinates(agent_id, onboarding_coords, chat_coords)

    def update_all_agents_coordinates(
        self, onboarding_coords: List[int], chat_coords: List[int]
    ) -> Dict[str, Any]:
        return self.repository.update_all_agents_coordinates(onboarding_coords, chat_coords)

    def update_onboarding_coordinates(
        self, agent_id: str, onboarding_coords: List[int]
    ) -> Dict[str, Any]:
        return self.repository.update_onboarding_coordinates(agent_id, onboarding_coords)

    def update_chat_coordinates(
        self, agent_id: str, chat_coords: List[int]
    ) -> Dict[str, Any]:
        return self.repository.update_chat_coordinates(agent_id, chat_coords)

    def update_all_onboarding_coordinates(self, onboarding_coords: List[int]) -> Dict[str, Any]:
        return self.repository.update_all_onboarding_coordinates(onboarding_coords)

    def update_all_chat_coordinates(self, chat_coords: List[int]) -> Dict[str, Any]:
        return self.repository.update_all_chat_coordinates(chat_coords)

    def get_chat_input_xy(self, agent_id: str) -> Tuple[int, int]:
        return self.repository.get_chat_input_xy(agent_id)

    def get_onboarding_input_xy(self, agent_id: str) -> Tuple[int, int]:
        return self.repository.get_onboarding_input_xy(agent_id)
