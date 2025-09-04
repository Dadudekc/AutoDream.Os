"""
Messaging Delivery Manager - V2 Compliance Delivery Management
===============================================================

Handles delivery method selection, execution, and fallback strategies with V2 compliance.

V2 COMPLIANCE: Dependency injection, async patterns, proper error handling.
DESIGN PATTERN: Strategy pattern for delivery methods, Factory pattern for delivery creation.

Author: Agent-2 (Architecture & Design Specialist)
Mission: V2 Compliance Architecture & Design Optimization
Status: V2 COMPLIANT - Delivery Manager Optimized
"""

import asyncio
from .unified_messaging_imports import (
    logging, get_logger, get_unified_validator, get_unified_utility,
    load_coordinates_from_json, json
)
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, TYPE_CHECKING

from .models.messaging_models import (
    UnifiedMessage as Message,
    DeliveryMethod
)

if TYPE_CHECKING:
    from .messaging_coordinate_delivery import CoordinateMessagingDelivery

class MessagingDeliveryManager:
    """
    Manages message delivery with multiple methods and fallback strategies.

    V2 COMPLIANCE: Dependency injection, proper error handling, async patterns.
    Handles delivery method selection, execution monitoring, and fallback strategies.
    """

    def __init__(self, logger=None, config: Optional[Dict[str, Any]] = None):
        """
        Initialize delivery manager with V2 compliance.

        Args:
            logger: Optional logger instance
            config: Optional configuration dictionary
        """
        self.logger = logger or get_logger(__name__)
        self.validator = get_unified_validator()
        self.utility = get_unified_utility()
        self.config = config or {}

        # Delivery method priorities (configurable)
        self.delivery_priorities = self.config.get(
            'delivery_priorities',
            [DeliveryMethod.PYAUTOGUI, DeliveryMethod.INBOX]
        )

        # Delivery statistics with V2 compliance
        self.delivery_stats: Dict[str, Any] = {
            'total_sent': 0,
            'total_failed': 0,
            'method_stats': {},
            'last_delivery_time': None,
            'avg_delivery_time': 0.0
        }

        # Configuration defaults
        self._set_config_defaults()

    def _set_config_defaults(self) -> None:
        """Set default configuration values."""
        defaults = {
            'max_delivery_attempts': 3,
            'delivery_timeout': 30,
            'enable_delivery_stats': True,
            'fallback_to_inbox': True
        }

        for key, default in defaults.items():
            if key not in self.config:
                self.config[key] = default

    async def deliver_message(self, message: Message,
                            preferred_method: DeliveryMethod = None) -> bool:
        """
        Deliver a message using the best available method with V2 compliance.

        Args:
            message: Message to deliver
            preferred_method: Preferred delivery method

        Returns:
            True if delivered successfully, False otherwise
        """
        import time

        try:
            # Validate message before delivery
            if not self.validator.validate_required(message):
                self.logger.error("Cannot deliver invalid message")
                return False

            start_time = time.time()
            self.logger.info(f"🚀 Delivering message {message.message_id} to {message.recipient}")

            # Determine delivery methods to try
            methods_to_try = self._get_delivery_methods(preferred_method)

            # Try each method in priority order
            for method in methods_to_try:
                try:
                    self.logger.debug(f"Attempting delivery via {method.value}")
                    success = await self._deliver_with_method(message, method)

                    if success:
                        delivery_time = time.time() - start_time
                        self._update_delivery_stats(method, True, delivery_time)
                        self.logger.info(f"✅ Message {message.message_id} delivered via {method.value} in {delivery_time:.2f}s")
                        return True
                    else:
                        self.logger.warning(f"⚠️ Method {method.value} failed for message {message.message_id}")

                except Exception as e:
                    self.logger.error(f"❌ Error with method {method.value}: {e}")

            # All methods failed
            delivery_time = time.time() - start_time
            self._update_delivery_stats(None, False, delivery_time)
            self.logger.error(f"❌ All delivery methods failed for message {message.message_id} to {message.recipient}")
            return False

        except Exception as e:
            self.logger.error(f"❌ Critical error delivering message {message.message_id}: {e}")
            return False

    async def _deliver_with_method(self, message: Message, method: DeliveryMethod) -> bool:
        """
        Deliver message using a specific method with V2 compliance.

        Args:
            message: Message to deliver
            method: Delivery method to use

        Returns:
            True if successful, False otherwise
        """
        try:
            if method == DeliveryMethod.PYAUTOGUI:
                return await self._deliver_pyautogui(message)
            elif method == DeliveryMethod.INBOX:
                return await self._deliver_inbox(message)
            elif method == DeliveryMethod.API:
                return await self._deliver_api(message)
            else:
                self.logger.warning(f"⚠️ Unknown delivery method: {method}")
                return False

        except Exception as e:
            self.logger.error(f"❌ Error with {method.value}: {e}")
            return False

    async def _deliver_pyautogui(self, message: Message) -> bool:
        """
        Deliver message using PyAutoGUI coordinates with V2 compliance.

        Args:
            message: Message to deliver

        Returns:
            True if successful, False otherwise
        """
        try:
            # Get agent coordinates using unified function
            coordinates = await self._get_agent_coordinates(message.recipient)
            if not self.validator.validate_required(coordinates):
                self.logger.warning(f"⚠️ No coordinates found for {message.recipient}")
                return False

            # Import and use PyAutoGUI directly (lazy loading for better performance)
            try:
                import pyautogui
                import pyperclip
            except ImportError as e:
                self.logger.error(f"❌ PyAutoGUI not available: {e}")
                return False

            x, y = coordinates

            # Validate coordinates
            if not self._validate_coordinates(x, y):
                self.logger.error(f"❌ Invalid coordinates for {message.recipient}: ({x}, {y})")
                return False

            self.logger.debug(f"📤 Moving to coordinates ({x}, {y}) for {message.recipient}")

            # Move to coordinates and interact
            pyautogui.moveTo(x, y, duration=0.1)
            pyautogui.click()
            await asyncio.sleep(0.1)  # Use asyncio.sleep for async compatibility

            # Clear existing content
            pyautogui.hotkey("ctrl", "a")
            pyautogui.press("delete")
            await asyncio.sleep(0.05)

            # Format message (simplified for delivery manager)
            formatted_message = f"Message from {message.sender}: {message.content}"

            # Send message
            pyperclip.copy(formatted_message)
            pyautogui.hotkey("ctrl", "v")
            await asyncio.sleep(0.05)
            pyautogui.press("enter")

            self.logger.info(f"✅ PyAutoGUI delivery successful for {message.recipient}")
            return True

        except Exception as e:
            self.logger.error(f"❌ PyAutoGUI delivery failed: {e}")
            return False

    def _validate_coordinates(self, x: int, y: int) -> bool:
        """
        Validate that coordinates are within reasonable screen bounds.

        Args:
            x: X coordinate
            y: Y coordinate

        Returns:
            True if coordinates are valid, False otherwise
        """
        try:
            import pyautogui
            screen_width, screen_height = pyautogui.size()
            # Allow some margin for multi-monitor setups
            return (0 <= x <= screen_width * 2) and (0 <= y <= screen_height * 2)
        except ImportError:
            # If PyAutoGUI is not available, assume coordinates are valid
            return True

    async def _deliver_inbox(self, message: Message) -> bool:
        """
        Deliver message by writing to inbox file with V2 compliance.

        Args:
            message: Message to deliver

        Returns:
            True if successful, False otherwise
        """
        try:
            # Create inbox path using unified utility
            inbox_dir = self.utility.resolve_path(f"agent_workspaces/{message.recipient}/inbox")
            self.utility.ensure_directory(inbox_dir)

            # Create unique message file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{timestamp}_{message.message_id[:8]}_message.md"
            file_path = inbox_dir / filename

            # Format message content with proper metadata handling
            created_at = getattr(message, 'created_at', getattr(message, 'timestamp', datetime.now()))

            content = f"""# Message from {message.sender}

**Message ID:** {message.message_id}
**Type:** {message.message_type.value}
**Priority:** {message.priority.value}
**Timestamp:** {created_at.isoformat() if hasattr(created_at, 'isoformat') else str(created_at)}
**Sender Type:** {message.sender_type.value if message.sender_type else 'unknown'}
**Recipient Type:** {message.recipient_type.value if message.recipient_type else 'unknown'}

## Content

{message.content}

## Metadata

```json
{json.dumps(message.metadata or {}, indent=2, default=str)}
```

## Tags

{message.tags if message.tags else 'No tags'}
"""

            # Write message using unified utility
            success = self.utility.write_file(file_path, content)
            if success:
                self.logger.info(f"📝 Message {message.message_id} written to inbox: {file_path}")
                return True
            else:
                self.logger.error(f"❌ Failed to write message {message.message_id} to inbox")
                return False

        except Exception as e:
            self.logger.error(f"❌ Inbox delivery failed for message {message.message_id}: {e}")
            return False

    async def _deliver_api(self, message: Message) -> bool:
        """
        Deliver message via API call.

        Args:
            message: Message to deliver

        Returns:
            True if successful, False otherwise
        """
        try:
            # Placeholder for API delivery
            # This would implement actual API calls to external services
            self.get_logger(__name__).info("🔌 API delivery not yet implemented")
            return False

        except Exception as e:
            self.get_logger(__name__).error(f"❌ API delivery failed: {e}")
            return False

    async def _get_agent_coordinates(self, agent_id: str) -> Optional[Tuple[int, int]]:
        """
        Get coordinates for an agent from the configuration file with V2 compliance.

        Args:
            agent_id: Agent identifier

        Returns:
            Agent coordinates as (x, y) tuple or None
        """
        try:
            # Use unified coordinate loading function
            agents = load_coordinates_from_json()

            if agent_id not in agents:
                self.logger.error(f"❌ Agent {agent_id} not found in coordinate configuration")
                return None

            # Get coordinates for this agent
            coords = agents[agent_id].get("coords")
            if not coords or len(coords) != 2:
                self.logger.error(f"❌ Invalid coordinates for agent {agent_id}: {coords}")
                return None

            # Ensure coordinates are integers
            try:
                x, y = int(coords[0]), int(coords[1])
                self.logger.debug(f"✅ Loaded coordinates for {agent_id}: ({x}, {y})")
                return (x, y)
            except (ValueError, TypeError) as e:
                self.logger.error(f"❌ Coordinate type error for {agent_id}: {coords} - {e}")
                return None

        except Exception as e:
            self.logger.error(f"❌ Error getting coordinates for {agent_id}: {e}")
            return None

    def _get_delivery_methods(self, preferred_method: DeliveryMethod = None) -> List[DeliveryMethod]:
        """
        Get ordered list of delivery methods to try.

        Args:
            preferred_method: Preferred method to try first

        Returns:
            Ordered list of delivery methods
        """
        if preferred_method:
            methods = [preferred_method]
            methods.extend([m for m in self.delivery_priorities if m != preferred_method])
            return methods

        return self.delivery_priorities.copy()

    def _update_delivery_stats(self, method: Optional[DeliveryMethod], success: bool, delivery_time: Optional[float] = None) -> None:
        """
        Update delivery statistics with V2 compliance.

        Args:
            method: Delivery method used (None if all methods failed)
            success: Whether delivery was successful
            delivery_time: Time taken for delivery in seconds
        """
        if not self.config.get('enable_delivery_stats', True):
            return

        # Update basic counters
        if success:
            self.delivery_stats['total_sent'] += 1
        else:
            self.delivery_stats['total_failed'] += 1

        # Update method-specific stats
        if method:
            method_key = method.value
            if method_key not in self.delivery_stats['method_stats']:
                self.delivery_stats['method_stats'][method_key] = {
                    'sent': 0, 'failed': 0, 'total_time': 0.0, 'avg_time': 0.0
                }

            stats = self.delivery_stats['method_stats'][method_key]
            if success:
                stats['sent'] += 1
            else:
                stats['failed'] += 1

            # Update timing statistics
            if delivery_time is not None:
                stats['total_time'] += delivery_time
                total_attempts = stats['sent'] + stats['failed']
                if total_attempts > 0:
                    stats['avg_time'] = stats['total_time'] / total_attempts

        # Update overall timing
        if delivery_time is not None:
            if self.delivery_stats['last_delivery_time'] is not None:
                # Calculate running average
                total_deliveries = self.delivery_stats['total_sent'] + self.delivery_stats['total_failed']
                if total_deliveries > 0:
                    self.delivery_stats['avg_delivery_time'] = (
                        (self.delivery_stats['avg_delivery_time'] * (total_deliveries - 1)) + delivery_time
                    ) / total_deliveries
            else:
                self.delivery_stats['avg_delivery_time'] = delivery_time

            self.delivery_stats['last_delivery_time'] = delivery_time

    def get_delivery_stats(self) -> Dict[str, Any]:
        """
        Get delivery statistics.

        Returns:
            Dictionary with delivery statistics
        """
        return self.delivery_stats.copy()

    def reset_delivery_stats(self) -> None:
        """
        Reset delivery statistics.
        """
        self.delivery_stats = {
            'total_sent': 0,
            'total_failed': 0,
            'method_stats': {}
        }
        self.get_logger(__name__).info("🔄 Delivery statistics reset")

