"""Data models for gaming integration."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List


class IntegrationStatus(Enum):
    """Status of gaming system integration."""

    DISCONNECTED = "disconnected"
    CONNECTED = "connected"
    ERROR = "error"


class GameType(Enum):
    """Types of games supported by the system."""

    ACTION = "action"
    ADVENTURE = "adventure"
    PUZZLE = "puzzle"
    STRATEGY = "strategy"


@dataclass
class GameSession:
    """Represents an active gaming session."""

    session_id: str
    game_type: GameType
    player_id: str
    start_time: datetime
    status: str
    metadata: Dict[str, Any]
    performance_metrics: Dict[str, Any]


@dataclass
class EntertainmentSystem:
    """Represents an entertainment system component."""

    system_id: str
    system_type: str
    status: IntegrationStatus
    capabilities: List[str]
    configuration: Dict[str, Any]
    last_updated: datetime
