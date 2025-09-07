#!/usr/bin/env python3
"""
Messaging CLI Handlers (Refactored) - Agent Cellphone V2
======================================================

Refactored messaging CLI handlers module with V2 compliance.
Clean, tested, class-based, reusable, scalable code.

Author: Agent-3 (Infrastructure & DevOps)
License: MIT
"""

import logging
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime

from .messaging_cli_utils import MessagingCLIUtils
from .messaging_cli_command_handlers import MessagingCLICommandHandlers
from .messaging_cli_coordinate_management import MessagingCLICoordinateManagement

logger = logging.getLogger(__name__)


# Legacy interface functions for backward compatibility
def read_json(file_path: str) -> Dict[str, Any]:
    """Read JSON file safely (legacy interface)."""
    return MessagingCLIUtils.read_json(file_path)


def write_json(file_path: str, data: Dict[str, Any]) -> bool:
    """Write JSON file safely (legacy interface)."""
    return MessagingCLIUtils.write_json(file_path, data)


def handle_utility_commands(args) -> bool:
    """Handle utility commands like status checking and history (legacy interface)."""
    handler = MessagingCLICommandHandlers()
    return handler.handle_utility_commands(args)


def handle_contract_commands(args) -> bool:
    """Handle contract-related commands (legacy interface)."""
    handler = MessagingCLICommandHandlers()
    return handler.handle_contract_commands(args)


def handle_onboarding_commands(args) -> bool:
    """Handle onboarding-related commands (legacy interface)."""
    handler = MessagingCLICommandHandlers()
    return handler.handle_onboarding_commands(args)


def handle_message_commands(args) -> bool:
    """Handle message-related commands (legacy interface)."""
    handler = MessagingCLICommandHandlers()
    return handler.handle_message_commands(args)


def handle_overnight_commands(args) -> bool:
    """Handle overnight commands (legacy interface)."""
    handler = MessagingCLICommandHandlers()
    return handler.handle_overnight_commands(args)


# Legacy coordinate management functions
def set_onboarding_coordinates(coord_string: str) -> Dict[str, Any]:
    """Set onboarding coordinates for an agent (legacy interface)."""
    coord_manager = MessagingCLICoordinateManagement()
    return coord_manager.set_onboarding_coordinates(coord_string)


def set_chat_coordinates(coord_string: str) -> Dict[str, Any]:
    """Set chat coordinates for an agent (legacy interface)."""
    coord_manager = MessagingCLICoordinateManagement()
    return coord_manager.set_chat_coordinates(coord_string)


def update_coordinates_from_file(file_path: str) -> Dict[str, Any]:
    """Update coordinates from a file (legacy interface)."""
    coord_manager = MessagingCLICoordinateManagement()
    return coord_manager.update_coordinates_from_file(file_path)


def interactive_coordinate_capture(agent_id: Optional[str] = None) -> Dict[str, Any]:
    """Interactive coordinate capture mode (legacy interface)."""
    coord_manager = MessagingCLICoordinateManagement()
    return coord_manager.interactive_coordinate_capture(agent_id)


def update_agent_coordinates(agent_id: str, onboarding_coords: List[int], chat_coords: List[int]) -> Dict[str, Any]:
    """Update coordinates for a specific agent (legacy interface)."""
    coord_manager = MessagingCLICoordinateManagement()
    return coord_manager.update_agent_coordinates(agent_id, onboarding_coords, chat_coords)


def update_all_agents_coordinates(onboarding_coords: List[int], chat_coords: List[int]) -> Dict[str, Any]:
    """Update coordinates for all agents (legacy interface)."""
    coord_manager = MessagingCLICoordinateManagement()
    return coord_manager.update_all_agents_coordinates(onboarding_coords, chat_coords)


def capture_onboarding_only(agent_id: Optional[str] = None) -> Dict[str, Any]:
    """Capture only onboarding coordinates (legacy interface)."""
    coord_manager = MessagingCLICoordinateManagement()
    return coord_manager.capture_onboarding_only(agent_id)


def capture_chat_only(agent_id: Optional[str] = None) -> Dict[str, Any]:
    """Capture only chat coordinates (legacy interface)."""
    coord_manager = MessagingCLICoordinateManagement()
    return coord_manager.capture_chat_only(agent_id)


def update_onboarding_coordinates(agent_id: str, onboarding_coords: List[int]) -> Dict[str, Any]:
    """Update only onboarding coordinates for a specific agent (legacy interface)."""
    coord_manager = MessagingCLICoordinateManagement()
    return coord_manager.update_onboarding_coordinates(agent_id, onboarding_coords)


def update_chat_coordinates(agent_id: str, chat_coords: List[int]) -> Dict[str, Any]:
    """Update only chat coordinates for a specific agent (legacy interface)."""
    coord_manager = MessagingCLICoordinateManagement()
    return coord_manager.update_chat_coordinates(agent_id, chat_coords)


def update_all_onboarding_coordinates(onboarding_coords: List[int]) -> Dict[str, Any]:
    """Update onboarding coordinates for all agents (legacy interface)."""
    coord_manager = MessagingCLICoordinateManagement()
    return coord_manager.update_all_onboarding_coordinates(onboarding_coords)


def update_all_chat_coordinates(chat_coords: List[int]) -> Dict[str, Any]:
    """Update chat coordinates for all agents (legacy interface)."""
    coord_manager = MessagingCLICoordinateManagement()
    return coord_manager.update_all_chat_coordinates(chat_coords)


def get_chat_input_xy(agent_id: str) -> Tuple[int, int]:
    """Get chat input coordinates for an agent (legacy interface)."""
    coord_manager = MessagingCLICoordinateManagement()
    return coord_manager.get_chat_input_xy(agent_id)


def get_onboarding_input_xy(agent_id: str) -> Tuple[int, int]:
    """Get onboarding input coordinates for an agent (legacy interface)."""
    coord_manager = MessagingCLICoordinateManagement()
    return coord_manager.get_onboarding_input_xy(agent_id)
