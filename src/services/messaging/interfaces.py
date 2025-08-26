#!/usr/bin/env python3
"""
Messaging Interfaces - Agent Cellphone V2
========================================

Clean interfaces defining contracts for different messaging capabilities.
Follows V2 standards: OOP, SRP, clean production-grade code.

Author: V2 SWARM CAPTAIN
License: MIT
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Union, List, Tuple, Protocol
from dataclasses import dataclass
from enum import Enum


@dataclass
class CoordinateData:
    """Data structure for agent coordinates"""

    agent_id: str
    mode: str
    input_box: Tuple[int, int]
    starter_location: Tuple[int, int]


class MessagingMode(Enum):
    """Available messaging modes"""

    PYAUTOGUI = "pyautogui"  # Default: Coordinate-based messaging
    CDP = "cdp"  # Chrome DevTools Protocol (headless)
    HTTP = "http"  # HTTP/HTTPS communication
    WEBSOCKET = "websocket"  # WebSocket communication
    TCP = "tcp"  # TCP communication
    FSM = "fsm"  # FSM-driven coordination
    ONBOARDING = "onboarding"  # Agent onboarding workflows
    CAMPAIGN = "campaign"  # Election/broadcast campaigns
    YOLO = "yolo"  # Automatic mode with FSM activation


class MessageType(Enum):
    """Message types for different modes"""

    # General messaging
    TEXT = "text"
    COMMAND = "command"
    BROADCAST = "broadcast"

    # High priority messaging
    HIGH_PRIORITY = "high_priority"  # Urgent messages with Ctrl+Enter 2x

    # FSM coordination
    TASK_ASSIGNMENT = "task_assignment"
    STATUS_UPDATE = "status_update"
    COORDINATION = "coordination"

    # Onboarding
    ONBOARDING_START = "onboarding_start"
    TRAINING_MODULE = "training_module"
    ROLE_ASSIGNMENT = "role_assignment"

    # Campaign
    ELECTION_BROADCAST = "election_broadcast"
    CAMPAIGN_UPDATE = "campaign_update"
    VOTER_ENGAGEMENT = "voter_engagement"


class IMessageSender(ABC):
    """Interface for message sending capabilities"""

    @abstractmethod
    def send_message(self, recipient: str, message_content: str) -> bool:
        """Send a message to a recipient"""
        raise NotImplementedError("send_message must be implemented")


class ICoordinateManager(ABC):
    """Interface for coordinate management"""

    @abstractmethod
    def get_agent_coordinates(self, agent_id: str, mode: str) -> Optional[Any]:
        """Get coordinates for a specific agent"""
        raise NotImplementedError("get_agent_coordinates must be implemented")

    @abstractmethod
    def validate_coordinates(self) -> Dict[str, Any]:
        """Validate all loaded coordinates"""
        raise NotImplementedError("validate_coordinates must be implemented")

    @abstractmethod
    def get_available_modes(self) -> List[str]:
        """Get available coordinate modes"""
        raise NotImplementedError("get_available_modes must be implemented")

    @abstractmethod
    def get_agents_in_mode(self, mode: str) -> List[str]:
        """Get agents in a specific mode"""
        raise NotImplementedError("get_agents_in_mode must be implemented")

    @abstractmethod
    def map_coordinates(self, mode: str = "8-agent") -> Dict[str, Any]:
        """Map and display coordinate information for debugging"""
        raise NotImplementedError("map_coordinates must be implemented")

    @abstractmethod
    def calibrate_coordinates(
        self,
        agent_id: str,
        input_coords: Tuple[int, int],
        starter_coords: Tuple[int, int],
        mode: str = "8-agent",
    ) -> bool:
        """Calibrate/update coordinates for a specific agent"""
        raise NotImplementedError("calibrate_coordinates must be implemented")

    @abstractmethod
    def consolidate_coordinate_files(self) -> Dict[str, Any]:
        """Consolidate multiple coordinate files"""
        raise NotImplementedError("consolidate_coordinate_files must be implemented")


class IBulkMessaging(ABC):
    """Interface for bulk messaging operations"""

    @abstractmethod
    def send_bulk_messages(
        self, messages: Dict[str, str], mode: str
    ) -> Dict[str, bool]:
        """Send messages to multiple agents"""
        raise NotImplementedError("send_bulk_messages must be implemented")


class ICampaignMessaging(ABC):
    """Interface for campaign messaging operations"""

    @abstractmethod
    def send_campaign_message(
        self, message_content: str, campaign_type: str
    ) -> Dict[str, bool]:
        """Send campaign message to all agents"""
        raise NotImplementedError("send_campaign_message must be implemented")


class IYOLOMessaging(ABC):
    """Interface for YOLO automatic activation messaging"""

    @abstractmethod
    def activate_yolo_mode(self, message_content: str) -> Dict[str, bool]:
        """Activate YOLO mode with automatic agent activation"""
        raise NotImplementedError("activate_yolo_mode must be implemented")


class ICrossSystemMessaging(ABC):
    """Interface for cross-system communication"""

    @abstractmethod
    async def send_cross_system_message(
        self, target_system: str, message_content: str, protocol: str
    ) -> bool:
        """Send message using cross-system communication protocols"""
        raise NotImplementedError("send_cross_system_message must be implemented")


class IFSMMessaging(ABC):
    """Interface for FSM-driven coordination messaging"""

    @abstractmethod
    def send_fsm_message(
        self, agent_id: str, message_type: MessageType, payload: Dict[str, Any]
    ) -> bool:
        """Send FSM-driven coordination message"""
        raise NotImplementedError("send_fsm_message must be implemented")


class IOnboardingMessaging(ABC):
    """Interface for agent onboarding messaging"""

    @abstractmethod
    def send_onboarding_message(
        self, agent_id: str, onboarding_type: MessageType, content: str
    ) -> bool:
        """Send onboarding message"""
        raise NotImplementedError("send_onboarding_message must be implemented")


class CoordinateCaptureInterface(Protocol):
    """Interface for coordinate capture operations"""

    def capture_agent_coordinates(
        self, agent_name: str, mode: str = "8-agent"
    ) -> Optional[CoordinateData]:
        """Capture coordinates for a specific agent"""
        ...
