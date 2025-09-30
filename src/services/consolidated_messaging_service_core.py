#!/usr/bin/env python3
"""
Consolidated Messaging Service - Core
====================================

Core classes and data structures for consolidated messaging system.

Author: Agent-4 (Captain & Operations Coordinator)
License: MIT
"""

import json
import logging
from pathlib import Path
import time

# Lazy import to prevent hard dep at import time
try:
    import pyautogui  # noqa: F401
    import pyperclip  # noqa: F401
except Exception as e:
    pyautogui = None  # type: ignore
    pyperclip = None  # type: ignore
    logging.warning(f"PyAutoGUI import failed: {e}")

# Import enhanced validation components
try:
    from src.services.messaging.enhanced_message_validator import EnhancedMessageValidator
    from src.services.messaging.enhanced_pyautogui_handler import EnhancedPyAutoGUIHandler

    ENHANCED_VALIDATION_AVAILABLE = True
except Exception as e:
    EnhancedMessageValidator = None
    EnhancedPyAutoGUIHandler = None
    ENHANCED_VALIDATION_AVAILABLE = False
    logging.warning(f"Enhanced validation import failed: {e}")

# Import memory management components
try:
    from src.services.messaging.memory_leak_fixes import (
        initialize_memory_management,
        cleanup_memory_resources,
        get_memory_status,
        memory_fixer
    )
    MEMORY_MANAGEMENT_AVAILABLE = True
except Exception as e:
    MEMORY_MANAGEMENT_AVAILABLE = False
    logging.warning(f"Memory management import failed: {e}")

logger = logging.getLogger(__name__)


class CoordinationRequest:
    """Data structure for coordination requests."""

    def __init__(self, from_agent: str, to_agent: str, message: str):
        """Initialize coordination request."""
        self.request_id = f"{from_agent}_{to_agent}_{int(time.time())}"
        self.from_agent = from_agent
        self.to_agent = to_agent
        self.message = message
        self.timestamp = time.time()
        self.acknowledged = False
        self.responded = False
        self.completed = False

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "from_agent": self.from_agent,
            "to_agent": self.to_agent,
            "message": self.message,
            "timestamp": self.timestamp,
            "acknowledged": self.acknowledged,
            "responded": self.responded,
            "completed": self.completed,
        }


class MessageProtocolChecker:
    """Check message protocol compliance."""

    def __init__(self, coordination_requests: dict):
        """Initialize protocol checker."""
        self.coordination_requests = coordination_requests

    def check_violations(self) -> dict[str, list[str]]:
        """Check for protocol violations."""
        violations = {"overdue": [], "unacknowledged": [], "incomplete": []}
        current_time = time.time()

        for request_id, request in self.coordination_requests.items():
            time_elapsed = current_time - request["timestamp"]

            if not request["acknowledged"] and time_elapsed > 300:  # 5 minutes
                violations["unacknowledged"].append(request_id)
            elif not request["responded"] and time_elapsed > 600:  # 10 minutes
                violations["overdue"].append(request_id)
            elif not request["completed"] and time_elapsed > 1800:  # 30 minutes
                violations["incomplete"].append(request_id)

        return violations


class AgentCoordinatesLoader:
    """Load agent coordinates from configuration."""

    def __init__(self, coord_path: str = "config/coordinates.json"):
        """Initialize coordinates loader."""
        self.coord_path = coord_path

    def load(self) -> dict:
        """Load agent coordinates from JSON file."""
        try:
            with open(self.coord_path) as f:
                data = json.load(f)
            return data.get("agents", {})
        except Exception as e:
            logger.error(f"Error loading coordinates: {e}")
            return {}


class AgentStatusChecker:
    """Check agent status."""

    def __init__(self, agent_data: dict):
        """Initialize status checker."""
        self.agent_data = agent_data

    def is_active(self, agent_id: str) -> bool:
        """Check if agent is active."""
        agent = self.agent_data.get(agent_id, {})
        return agent.get("active", False)


class ConsolidatedMessagingServiceCore:
    """Core messaging service with essential messaging functionality."""

    def __init__(self, coord_path: str = "config/coordinates.json") -> None:
        """Initialize consolidated messaging service core."""
        self.coord_path = coord_path
        loader = AgentCoordinatesLoader(coord_path)
        self.agent_data = loader.load()

        # Enhanced functionality
        self.auto_devlog_enabled = True
        self.response_protocol_enabled = True
        self.coordination_requests = {}

        # Status checker
        self.status_checker = AgentStatusChecker(self.agent_data)

        # Initialize enhanced validation if available
        if ENHANCED_VALIDATION_AVAILABLE:
            self.enhanced_validator = EnhancedMessageValidator()
            self.enhanced_handler = EnhancedPyAutoGUIHandler()
            logger.info("Enhanced messaging validation system initialized")
        else:
            self.enhanced_validator = None
            self.enhanced_handler = None
            logger.warning("Enhanced validation not available - using basic messaging")

        # Initialize memory management if available
        if MEMORY_MANAGEMENT_AVAILABLE:
            initialize_memory_management()
            logger.info("Memory management system initialized")
        else:
            logger.warning("Memory management not available - potential memory leaks possible")

    def track_coordination_request(self, from_agent: str, to_agent: str, message: str) -> None:
        """Track coordination requests for protocol compliance."""
        request = CoordinationRequest(from_agent, to_agent, message)
        self.coordination_requests[request.request_id] = request.to_dict()
        logger.info(f"Coordination request tracked: {request.request_id}")

    def check_response_protocol(self) -> dict[str, list[str]]:
        """Check for protocol violations."""
        checker = MessageProtocolChecker(self.coordination_requests)
        return checker.check_violations()

    def is_agent_active(self, agent_id: str) -> bool:
        """Check if agent is active."""
        return self.status_checker.is_active(agent_id)

    def get_agent_coordinates(self, agent_id: str) -> tuple[int, int] | None:
        """Get agent coordinates."""
        agent = self.agent_data.get(agent_id)
        if agent and "coordinates" in agent:
            return tuple(agent["coordinates"])
        return None
    
    def get_service_status(self) -> dict:
        """Get messaging service status."""
        status = {
            "service": "ConsolidatedMessagingServiceCore",
            "status": "active",
            "agents_loaded": len(self.agent_data),
            "coordination_requests": len(self.coordination_requests),
            "enhanced_validation": ENHANCED_VALIDATION_AVAILABLE,
            "memory_management": MEMORY_MANAGEMENT_AVAILABLE,
            "auto_devlog": self.auto_devlog_enabled,
            "response_protocol": self.response_protocol_enabled,
        }
        
        # Add memory status if available
        if MEMORY_MANAGEMENT_AVAILABLE:
            status["memory_status"] = get_memory_status()
        
        return status
    
    def cleanup_memory(self) -> dict:
        """Cleanup memory resources."""
        if MEMORY_MANAGEMENT_AVAILABLE:
            return cleanup_memory_resources()
        else:
            return {"error": "Memory management not available"}
    
    def get_memory_status(self) -> dict:
        """Get memory status."""
        if MEMORY_MANAGEMENT_AVAILABLE:
            return get_memory_status()
        else:
            return {"error": "Memory management not available"}
