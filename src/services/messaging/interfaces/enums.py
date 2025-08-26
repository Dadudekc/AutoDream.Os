"""Enumerations for messaging modes and types."""

from enum import Enum


class MessagingMode(Enum):
    """Available messaging modes."""

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
    """Message types for different modes."""

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
