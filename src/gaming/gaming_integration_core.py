<<<<<<< Updated upstream
"""Backward compatible stub for :mod:`gaming.integration.core`."""

from .integration.core import GamingIntegrationCore, GameType, IntegrationStatus

__all__ = ["GamingIntegrationCore", "GameType", "IntegrationStatus"]
=======
"""
Gaming Integration Core - SOLID Compliant Refactoring
====================================================

SOLID Compliant refactoring following V2 standards.
- SRP: Single Responsibility Principle - Each module has one responsibility
- OCP: Open-Closed Principle - Extension without modification of core classes
- LSP: Liskov Substitution Principle - Subtypes honor base contracts
- ISP: Interface Segregation Principle - Focused interfaces
- DIP: Dependency Inversion Principle - Depend on abstractions

Author: Agent-1 (SOLID Sentinel) - SOLID Enforcement
Original: Agent-8 (SSOT & System Integration Specialist)
License: MIT
"""

import logging
from typing import Dict, Any, Optional, Callable, List, Protocol
from datetime import datetime
from enum import Enum
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


# DIP: Abstract interfaces for dependency injection
class IGameSessionManager(Protocol):
    """Interface for game session management (ISP: Segregated interface)."""
    def create_session(self, game_type: str, player_id: str) -> Optional[Dict[str, Any]]: ...
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]: ...
    def end_session(self, session_id: str) -> bool: ...
    def get_active_sessions(self) -> List[Dict[str, Any]]: ...


class IEntertainmentSystemManager(Protocol):
    """Interface for entertainment system management (ISP: Segregated interface)."""
    def register_system(self, system_id: str, system_type: str) -> bool: ...
    def get_system(self, system_id: str) -> Optional[Dict[str, Any]]: ...
    def get_all_systems(self) -> List[Dict[str, Any]]: ...


class IIntegrationHandler(Protocol):
    """Interface for integration event handlers (ISP: Segregated interface)."""
    def handle_event(self, event: Dict[str, Any]) -> Dict[str, Any]: ...


class IntegrationStatus(Enum):
    """Integration status states."""

    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    ERROR = "error"
    MAINTENANCE = "maintenance"


class GameType(Enum):
    """Game types."""

    STRATEGY = "strategy"
    ACTION = "action"
    PUZZLE = "puzzle"
    SIMULATION = "simulation"
    ROLE_PLAYING = "role_playing"


# SRP: GameSession as simple data class
class GameSession:
    """Simplified game session - Single Responsibility: Data container."""

    def __init__(self, session_id: str, game_type: GameType, player_id: str):
        self.session_id = session_id
        self.game_type = game_type
        self.player_id = player_id
        self.start_time = datetime.now()
        self.status = "active"
        self.score = 0
        self.level = 1

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "session_id": self.session_id,
            "game_type": self.game_type.value,
            "player_id": self.player_id,
            "start_time": self.start_time.isoformat(),
            "status": self.status,
            "score": self.score,
            "level": self.level
        }


# SRP: EntertainmentSystem as simple data class
class EntertainmentSystem:
    """Simplified entertainment system - Single Responsibility: Data container."""

    def __init__(self, system_id: str, system_type: str):
        self.system_id = system_id
        self.system_type = system_type
        self.status = "active"
        self.last_activity = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "system_id": self.system_id,
            "system_type": self.system_type,
            "status": self.status,
            "last_activity": self.last_activity.isoformat()
        }


# SRP: GameSessionManager handles only session-related operations
class GameSessionManager:
    """Game session manager - Single Responsibility: Session management."""

    def __init__(self):
        self.sessions: Dict[str, GameSession] = {}

    def create_session(self, game_type: str, player_id: str) -> Optional[Dict[str, Any]]:
        """Create a new game session."""
        try:
            session_id = f"session_{int(datetime.now().timestamp())}"
            game_type_enum = GameType(game_type)
            session = GameSession(session_id, game_type_enum, player_id)
            self.sessions[session_id] = session

            logger.info(f"Created game session: {session_id}")
            return session.to_dict()
        except Exception as e:
            logger.error(f"Error creating game session: {e}")
            return None

    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get game session."""
        session = self.sessions.get(session_id)
        return session.to_dict() if session else None

    def end_session(self, session_id: str) -> bool:
        """End game session."""
        try:
            if session_id in self.sessions:
                session = self.sessions[session_id]
                session.status = "ended"
                logger.info(f"Ended game session: {session_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error ending game session: {e}")
            return False

    def get_active_sessions(self) -> List[Dict[str, Any]]:
        """Get active game sessions."""
        return [
            session.to_dict()
            for session in self.sessions.values()
            if session.status == "active"
        ]


# SRP: EntertainmentSystemManager handles only system-related operations
class EntertainmentSystemManager:
    """Entertainment system manager - Single Responsibility: System management."""

    def __init__(self):
        self.systems: Dict[str, EntertainmentSystem] = {}

    def register_system(self, system_id: str, system_type: str) -> bool:
        """Register entertainment system."""
        try:
            system = EntertainmentSystem(system_id, system_type)
            self.systems[system_id] = system
            logger.info(f"Registered entertainment system: {system_id}")
            return True
        except Exception as e:
            logger.error(f"Error registering entertainment system: {e}")
            return False

    def get_system(self, system_id: str) -> Optional[Dict[str, Any]]:
        """Get entertainment system."""
        system = self.systems.get(system_id)
        return system.to_dict() if system else None

    def get_all_systems(self) -> List[Dict[str, Any]]:
        """Get all entertainment systems."""
        return [system.to_dict() for system in self.systems.values()]


# SRP: IntegrationEventHandler handles only event processing
class IntegrationEventHandler:
    """Integration event handler - Single Responsibility: Event processing."""

    def __init__(self, session_manager: IGameSessionManager):
        self.session_manager = session_manager

    def handle_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Handle integration events."""
        try:
            event_type = event.get("type", "unknown")

            if event_type == "create_session":
                return self._handle_create_session(event)
            elif event_type == "end_session":
                return self._handle_end_session(event)
            elif event_type == "get_session":
                return self._handle_get_session(event)

            return {"success": False, "error": "Unknown event type"}
        except Exception as e:
            logger.error(f"Error handling event: {e}")
            return {"success": False, "error": str(e)}

    def _handle_create_session(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Handle session creation event."""
        game_type = event.get("game_type", "strategy")
        player_id = event.get("player_id", "unknown")
        session = self.session_manager.create_session(game_type, player_id)
        return {
            "success": session is not None,
            "session_id": session.get("session_id") if session else None,
        }

    def _handle_end_session(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Handle session end event."""
        session_id = event.get("session_id")
        return {"success": self.session_manager.end_session(session_id)}

    def _handle_get_session(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Handle session retrieval event."""
        session_id = event.get("session_id")
        session = self.session_manager.get_session(session_id)
        return {
            "success": session is not None,
            "session": session,
        }


# DIP & OCP: GamingIntegrationCore uses composition and dependency injection
class GamingIntegrationCore:
    """Gaming integration core - SOLID Compliant: Uses composition and interfaces."""

    def __init__(self,
                 config: Optional[Dict[str, Any]] = None,
                 session_manager: Optional[IGameSessionManager] = None,
                 system_manager: Optional[IEntertainmentSystemManager] = None):
        """Initialize with dependency injection."""
        self.config = config or {}
        self.status = IntegrationStatus.DISCONNECTED

        # DIP: Inject dependencies or use defaults
        self.session_manager = session_manager or GameSessionManager()
        self.system_manager = system_manager or EntertainmentSystemManager()

        # OCP: Event handlers can be extended without modifying core
        self.event_handlers: Dict[str, IIntegrationHandler] = {}
        self.is_initialized = False

        self._initialize_integration()

    def _initialize_integration(self):
        """Initialize the integration system."""
        try:
            logger.info("Initializing Gaming Integration Core")
            self._setup_default_handlers()
            self._connect_to_systems()
            self.is_initialized = True
            self.status = IntegrationStatus.CONNECTED
        except Exception as e:
            logger.error(f"Error initializing gaming integration: {e}")
            self.status = IntegrationStatus.ERROR

    def _setup_default_handlers(self):
        """Setup default event handlers."""
        self.event_handlers["session_management"] = IntegrationEventHandler(self.session_manager)

    def _connect_to_systems(self):
        """Connect to gaming systems."""
        try:
            logger.info("Connecting to gaming systems")
            self.status = IntegrationStatus.CONNECTED
        except Exception as e:
            logger.error(f"Error connecting to systems: {e}")
            self.status = IntegrationStatus.ERROR

    # SRP: Delegate session operations to session manager
    def create_game_session(self, game_type: GameType, player_id: str) -> Optional[Dict[str, Any]]:
        """Create a new game session - delegates to session manager."""
        if not self.is_initialized:
            logger.warning("Gaming integration not initialized")
            return None
        # Handle both enum and string inputs
        game_type_str = game_type.value if hasattr(game_type, 'value') else str(game_type)
        return self.session_manager.create_session(game_type_str, player_id)

    def get_game_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get game session - delegates to session manager."""
        return self.session_manager.get_session(session_id)

    def end_game_session(self, session_id: str) -> bool:
        """End game session - delegates to session manager."""
        return self.session_manager.end_session(session_id)

    def get_active_sessions(self) -> List[Dict[str, Any]]:
        """Get active game sessions - delegates to session manager."""
        return self.session_manager.get_active_sessions()

    # SRP: Delegate system operations to system manager
    def register_entertainment_system(self, system_id: str, system_type: str) -> bool:
        """Register entertainment system - delegates to system manager."""
        return self.system_manager.register_system(system_id, system_type)

    def get_entertainment_system(self, system_id: str) -> Optional[Dict[str, Any]]:
        """Get entertainment system - delegates to system manager."""
        return self.system_manager.get_system(system_id)

    def get_all_entertainment_systems(self) -> List[Dict[str, Any]]:
        """Get all entertainment systems - delegates to system manager."""
        return self.system_manager.get_all_systems()

    # OCP: Add event handler registration without modifying core
    def register_event_handler(self, name: str, handler: IIntegrationHandler) -> None:
        """Register event handler - Open-Closed Principle."""
        self.event_handlers[name] = handler

    def handle_event(self, handler_name: str, event: Dict[str, Any]) -> Dict[str, Any]:
        """Handle event using registered handler."""
        handler = self.event_handlers.get(handler_name)
        if handler:
            return handler.handle_event(event)
        return {"success": False, "error": f"Handler '{handler_name}' not found"}

    # LSP: Maintain backward compatibility while honoring new interface contracts
    def get_status(self) -> str:
        """Get integration status."""
        return self.status.value

    def is_connected(self) -> bool:
        """Check if integration is connected."""
        return self.status == IntegrationStatus.CONNECTED

    def get_core_health(self) -> Dict[str, Any]:
        """Get core health status."""
        return {
            "status": self.get_status(),
            "initialized": self.is_initialized,
            "session_count": len(self.session_manager.get_active_sessions()),
            "system_count": len(self.system_manager.get_all_systems()),
            "handler_count": len(self.event_handlers)
        }

# Factory function for backward compatibility
def create_gaming_integration_core(config: Optional[Dict[str, Any]] = None) -> GamingIntegrationCore:
    """Factory function for creating GamingIntegrationCore instances."""
    return GamingIntegrationCore(config)


# Backward compatibility alias
GamingCore = GamingIntegrationCore
>>>>>>> Stashed changes
