from __future__ import annotations

"""High-level PyAutoGUI messaging interface coordinating GUI helpers and transports."""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
import logging

from .coordinate_manager import CoordinateManager, AgentCoordinates
from .interfaces import IMessageSender, IBulkMessaging
from .pyautogui_helpers import (
    setup_pyautogui,
    PYAUTOGUI_AVAILABLE,
    PYPERCLIP_AVAILABLE,
)
from . import transports

logger = logging.getLogger(__name__)


@dataclass
class MessageDeliveryResult:
    """Result of a single message delivery attempt."""

    success: bool
    recipient: str
    message_type: str
    timestamp: datetime
    error_message: Optional[str] = None
    delivery_method: str = "pyautogui"
    coordinates_used: Optional[Tuple[int, int]] = None


@dataclass
class BulkMessageResult:
    """Aggregate results for a bulk delivery operation."""

    total_messages: int
    successful_deliveries: int
    failed_deliveries: int
    results: List[MessageDeliveryResult]
    start_time: datetime
    end_time: Optional[datetime] = None


class UnifiedPyAutoGUIMessaging(IMessageSender, IBulkMessaging):
    """Coordinate PyAutoGUI helper utilities with transport implementations."""

    def __init__(self, coordinate_manager: CoordinateManager):
        self.coordinate_manager = coordinate_manager
        setup_pyautogui()
        self.delivery_history: List[MessageDeliveryResult] = []
        logger.info("UnifiedPyAutoGUIMessaging initialized")

    # ------------------------------------------------------------------
    # Message sending helpers
    # ------------------------------------------------------------------
    def _get_coords(
        self, agent_id: str, mode: str = "8-agent"
    ) -> Optional[AgentCoordinates]:
        coords = self.coordinate_manager.get_agent_coordinates(agent_id, mode)
        if not coords:
            logger.error(f"No coordinates found for {agent_id}")
        return coords

    def send_message(
        self,
        recipient: str,
        message_content: str,
        message_type: str = "text",
        new_chat: bool = False,
        priority: str = "normal",
    ) -> bool:
        """Send a message using the appropriate transport."""
        coords = self._get_coords(recipient)
        if not coords:
            return False

        try:
            if new_chat or message_type == "onboarding_start":
                success = transports.send_onboarding_message(coords, message_content)
            elif priority == "urgent":
                success = transports.send_urgent_message(coords, message_content)
            elif priority == "high":
                success = transports.send_high_priority_message(coords, message_content)
            else:
                success = transports.send_normal_message(coords, message_content)

            result = MessageDeliveryResult(
                success=success,
                recipient=recipient,
                message_type=message_type,
                timestamp=datetime.now(),
                error_message=None if success else "Delivery failed",
                coordinates_used=coords.input_box if success else None,
            )
            self.delivery_history.append(result)
            return success
        except Exception as e:  # pragma: no cover - defensive logging
            logger.error(f"Error sending message to {recipient}: {e}")
            self.delivery_history.append(
                MessageDeliveryResult(
                    success=False,
                    recipient=recipient,
                    message_type=message_type,
                    timestamp=datetime.now(),
                    error_message=str(e),
                )
            )
            return False

    def send_bulk_messages(
        self,
        messages: Dict[str, str],
        mode: str = "8-agent",
        message_type: str = "text",
        priority: str = "normal",
        new_chat: bool = False,
    ) -> Dict[str, bool]:
        start_time = datetime.now()
        results: Dict[str, bool] = {}
        success_count = 0
        failure_count = 0

        for agent_id, message in messages.items():
            success = self.send_message(
                agent_id, message, message_type, new_chat=new_chat, priority=priority
            )
            results[agent_id] = success
            if success:
                success_count += 1
            else:
                failure_count += 1

        self.delivery_history.append(
            MessageDeliveryResult(
                success=failure_count == 0,
                recipient="bulk",
                message_type=message_type,
                timestamp=datetime.now(),
            )
        )
        logger.info(
            f"Bulk delivery complete: {success_count}/{len(messages)} successful"
        )
        return results

    # ------------------------------------------------------------------
    # Specialized helpers used by UnifiedMessagingService
    # ------------------------------------------------------------------
    def send_onboarding_message(
        self, agent_id: str, message: str, mode: str = "8-agent"
    ) -> bool:
        coords = self._get_coords(agent_id, mode)
        if not coords:
            return False
        return transports.send_onboarding_message(coords, message)

    def send_bulk_onboarding(
        self, onboarding_messages: Dict[str, str], mode: str = "8-agent"
    ) -> Dict[str, bool]:
        return {
            agent: self.send_onboarding_message(agent, msg, mode)
            for agent, msg in onboarding_messages.items()
        }

    def send_high_priority_message(
        self, agent_id: str, message: str, mode: str = "8-agent"
    ) -> bool:
        coords = self._get_coords(agent_id, mode)
        if not coords:
            return False
        return transports.send_high_priority_message(coords, message)

    def send_bulk_high_priority(
        self, urgent_messages: Dict[str, str], mode: str = "8-agent"
    ) -> Dict[str, bool]:
        return {
            agent: self.send_high_priority_message(agent, msg, mode)
            for agent, msg in urgent_messages.items()
        }

    def activate_agent(self, agent_id: str, mode: str = "8-agent") -> bool:
        coords = self._get_coords(agent_id, mode)
        if not coords:
            return False
        return transports.activate_agent(coords)

    # ------------------------------------------------------------------
    # Status and history utilities
    # ------------------------------------------------------------------
    def clear_delivery_history(self) -> None:
        self.delivery_history.clear()

    def get_system_status(self) -> Dict[str, Any]:
        return {
            "pyautogui_available": PYAUTOGUI_AVAILABLE,
            "pyperclip_available": PYPERCLIP_AVAILABLE,
            "coordinate_manager_connected": self.coordinate_manager is not None,
            "delivery_history_size": len(self.delivery_history),
            "last_delivery": self.delivery_history[-1].timestamp
            if self.delivery_history
            else None,
        }


# Factory


def create_unified_pyautogui_messaging(
    coordinate_manager: CoordinateManager,
) -> UnifiedPyAutoGUIMessaging:
    """Factory helper for compatibility."""
    return UnifiedPyAutoGUIMessaging(coordinate_manager)
