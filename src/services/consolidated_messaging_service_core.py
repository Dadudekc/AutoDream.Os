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
import time
from dataclasses import dataclass

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
        cleanup_memory_resources,
        get_memory_status,
        initialize_memory_management,
    )

    MEMORY_MANAGEMENT_AVAILABLE = True
except Exception as e:
    MEMORY_MANAGEMENT_AVAILABLE = False
    logging.warning(f"Memory management import failed: {e}")

logger = logging.getLogger(__name__)


@dataclass
class ScreenshotTrigger:
    """Screenshot trigger configuration for messaging system."""

    trigger_type: str  # COORDINATION, MILESTONE, CRITICAL, USER_REQUEST
    cycle_interval: int  # Every N cycles
    last_triggered: str = ""
    enabled: bool = True

    def __post_init__(self):
        if not self.last_triggered:
            self.last_triggered = time.strftime("%Y-%m-%dT%H:%M:%S")


class ScreenshotManager:
    """Integrated screenshot management for messaging system."""

    def __init__(self):
        """Initialize screenshot manager."""
        self.current_cycle = 0
        self.triggers = {
            "COORDINATION": ScreenshotTrigger("COORDINATION", 3),  # Every 3 cycles
            "MILESTONE": ScreenshotTrigger("MILESTONE", 10),  # Every 10 cycles
            "CRITICAL": ScreenshotTrigger("CRITICAL", 1),  # Always enabled
            "USER_REQUEST": ScreenshotTrigger("USER_REQUEST", 1),  # Always enabled
        }
        logger.info("Screenshot Manager initialized")

    def should_take_screenshot(self, cycle_type: str, event_type: str = "NORMAL") -> bool:
        """Determine if screenshot should be taken based on triggers."""
        try:
            # User request always triggers
            if event_type == "USER_REQUEST":
                logger.info("Screenshot triggered: User request")
                return True

            # Critical events always trigger
            if event_type in ["MAJOR_COMPLETION", "SYSTEM_FAILURE", "AGENT_ERROR"]:
                logger.info(f"Screenshot triggered: Critical event - {event_type}")
                return True

            # Check cycle-based triggers
            if cycle_type == "COORDINATION":
                coordination_trigger = self.triggers.get("COORDINATION")
                if coordination_trigger and coordination_trigger.enabled:
                    if (
                        self.current_cycle % coordination_trigger.cycle_interval == 0
                        and self.current_cycle > 0
                    ):
                        logger.info(
                            f"Screenshot triggered: Coordination cycle {self.current_cycle}"
                        )
                        return True

            # Check milestone triggers
            milestone_trigger = self.triggers.get("MILESTONE")
            if milestone_trigger and milestone_trigger.enabled:
                if (
                    self.current_cycle % milestone_trigger.cycle_interval == 0
                    and self.current_cycle > 0
                ):
                    logger.info(f"Screenshot triggered: Milestone cycle {self.current_cycle}")
                    return True

            return False

        except Exception as e:
            logger.error(f"Error checking screenshot trigger: {e}")
            return False

    def increment_cycle(self):
        """Increment cycle counter."""
        self.current_cycle += 1
        logger.debug(f"Cycle incremented to {self.current_cycle}")

    def get_screenshot_context(self, trigger_reason: str) -> dict:
        """Generate screenshot context metadata."""
        return {
            "cycle_number": self.current_cycle,
            "trigger_reason": trigger_reason,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "focus_agents": ["Agent-4", "Agent-5", "Agent-6", "Agent-7", "Agent-8"],
            "expected_content": self._get_expected_content(trigger_reason),
            "screenshot_type": self._get_screenshot_type(trigger_reason),
        }

    def _get_expected_content(self, trigger_reason: str) -> str:
        """Get expected screenshot content based on trigger."""
        content_map = {
            "COORDINATION": "Multi-agent coordination and A2A messages",
            "MILESTONE": "System-wide progress and agent status",
            "CRITICAL": "Error context and system state",
            "USER_REQUEST": "Specific user-requested context",
        }
        return content_map.get(trigger_reason, "General system status")

    def _get_screenshot_type(self, trigger_reason: str) -> str:
        """Get screenshot type based on trigger."""
        type_map = {
            "COORDINATION": "multi_agent_view",
            "MILESTONE": "system_overview",
            "CRITICAL": "error_context",
            "USER_REQUEST": "custom_context",
        }
        return type_map.get(trigger_reason, "general")


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
            # Handle both formats: direct agents or nested under "agents" key
            if "agents" in data:
                return data["agents"]
            else:
                # Convert direct format to expected format
                converted = {}
                for agent_id, agent_data in data.items():
                    if isinstance(agent_data, dict) and "x" in agent_data and "y" in agent_data:
                        converted[agent_id] = {
                            "chat_input_coordinates": [agent_data["x"], agent_data["y"]],
                            "monitor": agent_data.get("monitor", 1),
                            "status": agent_data.get("status", "INACTIVE"),
                            "active": agent_data.get("status", "INACTIVE") == "ACTIVE",
                        }
                return converted
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
        if agent and "chat_input_coordinates" in agent:
            return tuple(agent["chat_input_coordinates"])
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
