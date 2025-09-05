#!/usr/bin/env python3
"""
Unified Messaging Core - Agent Cellphone V2
===========================================

Core messaging functionality for the unified messaging service.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

from .unified_messaging_imports import (
    logging, COORDINATE_CONFIG_FILE, get_logger, get_unified_utility, 
    load_coordinates_from_json, json
)
from ..core.simple_validation_system import get_simple_validator
import time
from datetime import datetime
from typing import Any, Dict, List, Optional
from pathlib import Path

from .models.messaging_models import (
    UnifiedMessage,
    UnifiedMessageType,
    UnifiedMessagePriority,
    UnifiedMessageTag,
    UnifiedSenderType,
    UnifiedRecipientType
)
from .message_identity_clarification import format_message_with_identity_clarification


class UnifiedMessagingCore:
    """
    Core messaging functionality for the unified messaging service.

    V2 COMPLIANCE: Single responsibility, dependency injection, proper error handling.
    Handles message creation, validation, and delivery coordination.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the unified messaging core with V2 compliance."""
        self.config = config or {}
        self.message_history: List[UnifiedMessage] = []
        self.logger = get_logger(__name__)
        self.validator = get_simple_validator()
        self.utility = get_unified_utility()

        # Validate configuration on initialization
        self._validate_config()

    def _validate_config(self) -> None:
        """Validate configuration with V2 compliance."""
        required_fields = ["message_history_limit", "delivery_timeout"]
        defaults = {
            "message_history_limit": 1000,
            "delivery_timeout": 30,
            "max_message_length": 10000,
            "enable_message_validation": True
        }

        for field, default in defaults.items():
            if field not in self.config:
                self.config[field] = default

        missing = self.validator.validate_required_fields(self.config, required_fields)
        if missing:
            self.logger.warning(f"Missing config fields, using defaults: {missing}")

    def create_message(
        self,
        content: str,
        sender: str,
        recipient: str,
        message_type: UnifiedMessageType = UnifiedMessageType.TEXT,
        priority: UnifiedMessagePriority = UnifiedMessagePriority.REGULAR,
        tags: Optional[List[UnifiedMessageTag]] = None,
        sender_type: UnifiedSenderType = UnifiedSenderType.SYSTEM,
        recipient_type: UnifiedRecipientType = UnifiedRecipientType.AGENT
    ) -> Optional[UnifiedMessage]:
        """
        Create a new unified message with V2 compliance validation.

        Args:
            content: Message content
            sender: Sender identifier
            recipient: Recipient identifier
            message_type: Type of message
            priority: Message priority
            tags: Optional message tags
            sender_type: Type of sender
            recipient_type: Type of recipient

        Returns:
            UnifiedMessage if valid, None if validation fails
        """
        try:
            # Validate input parameters
            if not self.validator.validate_required([content, sender, recipient]):
                self.logger.error("Missing required message parameters")
                return None

            # Validate content length
            if not self.validator.validate_string_length(content, max_length=self.config["max_message_length"]):
                self.logger.error(f"Message content exceeds maximum length: {self.config['max_message_length']}")
                return None

            # Create message with validation
            message = UnifiedMessage(
                content=content,
                sender=sender,
                recipient=recipient,
                message_type=message_type,
                priority=priority,
                tags=tags or [],
                sender_type=sender_type,
                recipient_type=recipient_type,
                timestamp=datetime.now()
            )

            self.logger.info(f"✅ Created message: {message.message_id}")
            return message

        except Exception as e:
            self.logger.error(f"❌ Error creating message: {e}")
            return None
    
    def send_message(
        self,
        message: UnifiedMessage,
        mode: str = "pyautogui",
        use_onboarding_coords: bool = False
    ) -> bool:
        """
        Send a message using the specified delivery method with V2 compliance.

        Args:
            message: Message to send
            mode: Delivery mode ("pyautogui" or "inbox")
            use_onboarding_coords: Whether to use onboarding coordinates

        Returns:
            True if successful, False otherwise
        """
        try:
            # Validate message before sending
            if not self.validator.validate_required([message.content, message.sender, message.recipient]):
                self.logger.error("Cannot send invalid message")
                return False

            # Manage message history with size limits
            self.message_history.append(message)
            if len(self.message_history) > self.config["message_history_limit"]:
                self.message_history.pop(0)  # Remove oldest message

            # Route to appropriate delivery method
            if mode == "inbox":
                return self._send_to_inbox(message)
            elif mode == "pyautogui":
                return self._send_via_pyautogui(message, use_onboarding_coords)
            else:
                self.logger.error(f"❌ Unknown delivery mode: {mode}")
                return False

        except Exception as e:
            self.logger.error(f"❌ Failed to send message {message.message_id}: {e}")
            return False
    
    def _send_to_inbox(self, message: UnifiedMessage) -> bool:
        """
        Send message to agent inbox with V2 compliance.

        Args:
            message: Message to send

        Returns:
            True if successful, False otherwise
        """
        try:
            # Use pathlib for path handling
            from pathlib import Path
            inbox_dir = Path(f"agent_workspaces/{message.recipient}/inbox")
            inbox_dir.mkdir(parents=True, exist_ok=True)

            # Create unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = inbox_dir / f"message_{timestamp}_{message.message_id[:8]}.md"

            # Format message with identity clarification
            formatted_message = format_message_with_identity_clarification(
                message, message.recipient
            )

            # Write message using standard file operations
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(formatted_message)
            success = True
            if success:
                self.logger.info(f"✅ Message sent to inbox: {filename}")
                return True
            else:
                self.logger.error(f"❌ Failed to write message to inbox: {filename}")
                return False

        except Exception as e:
            self.logger.error(f"❌ Failed to send to inbox: {e}")
            return False
    
    def _send_via_pyautogui(self, message: UnifiedMessage, use_onboarding_coords: bool = False) -> bool:
        """
        Send message via PyAutoGUI to agent coordinates with V2 compliance.

        Args:
            message: Message to send
            use_onboarding_coords: Whether to use onboarding coordinates

        Returns:
            True if successful, False otherwise
        """
        try:
            # Load coordinates using unified function
            agents = load_coordinates_from_json()
            if message.recipient not in agents:
                self.logger.error(f"❌ No coordinates found for {message.recipient}")
                return False

            agent_coords = agents[message.recipient].get("coords")
            if not agent_coords or len(agent_coords) != 2:
                self.logger.error(f"❌ Invalid coordinates for {message.recipient}: {agent_coords}")
                return False

            # Ensure coordinates are integers
            try:
                x, y = int(agent_coords[0]), int(agent_coords[1])
            except (ValueError, TypeError) as e:
                self.logger.error(f"❌ Coordinate type error for {message.recipient}: {agent_coords} - {e}")
                return False

            self.logger.info(f"📤 Sending PyAutoGUI message to {message.recipient} at ({x}, {y})")

            # Import PyAutoGUI libraries (lazy loading for better performance)
            try:
                import pyautogui
                import pyperclip
            except ImportError as e:
                self.logger.error(f"❌ PyAutoGUI not available: {e}")
                return False

            # Move to coordinates with validation
            if not self._validate_coordinates(x, y):
                self.logger.error(f"❌ Invalid coordinates for {message.recipient}: ({x}, {y})")
                return False

            pyautogui.moveTo(x, y, duration=0.1)
            pyautogui.click()
            time.sleep(0.1)

            # Clear existing content
            pyautogui.hotkey("ctrl", "a")
            pyautogui.press("delete")
            time.sleep(0.05)

            # Format and send message
            formatted_message = format_message_with_identity_clarification(
                message, message.recipient
            )

            pyperclip.copy(formatted_message)
            pyautogui.hotkey("ctrl", "v")
            time.sleep(0.05)
            pyautogui.press("enter")

            self.logger.info(f"✅ PyAutoGUI message sent to {message.recipient}")
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
            # Allow negative coordinates for multi-monitor setups (left monitor)
            # Allow some margin for multi-monitor setups
            return (-screen_width <= x <= screen_width * 2) and (0 <= y <= screen_height * 2)
        except ImportError:
            # If PyAutoGUI is not available, assume coordinates are valid
            return True
    
    def get_message_history(self) -> List[UnifiedMessage]:
        """Get the message history."""
        return self.message_history.copy()
    
    def clear_message_history(self) -> None:
        """Clear the message history."""
        self.message_history.clear()
    
    def get_config(self) -> Dict[str, Any]:
        """Get the current configuration."""
        return self.config.copy()
    
    def update_config(self, new_config: Dict[str, Any]) -> None:
        """Update the configuration."""
        self.config.update(new_config)