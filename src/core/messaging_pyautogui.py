#!/usr/bin/env python3
"""
PyAutoGUI Messaging Delivery
Sends messages to agent chat input coordinates using PyAutoGUI

RACE CONDITION FIXES (2025-10-15):
- Clipboard locking to prevent concurrent overwrites
- Increased delays (0.5s→1.0s) for slow systems
- 3-attempt retry mechanism for reliability
"""

import logging
import time
import threading

logger = logging.getLogger(__name__)

# RACE CONDITION FIX #1: Global clipboard lock
_clipboard_lock = threading.Lock()

try:
    import pyautogui
    import pyperclip

    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False


def get_message_tag(sender: str, recipient: str) -> str:
    """
    Determine correct message tag based on sender and recipient.
    
    Args:
        sender: Message sender (GENERAL, DISCORD, CAPTAIN, Agent-X, SYSTEM)
        recipient: Message recipient (Agent-X, ALL, CAPTAIN)
    
    Returns:
        Correct message tag ([D2A], [G2A], [C2A], [A2A], [A2C], [S2A])
    """
    sender_upper = sender.upper()
    recipient_upper = recipient.upper() if recipient else ""
    
    # General broadcasts (STRATEGIC - highest priority!)
    if 'GENERAL' in sender_upper:
        return '[G2A]'  # General-to-Agent
    
    # Discord/Commander broadcasts
    if sender_upper in ['DISCORD', 'COMMANDER', 'DISCORD-CONTROLLER']:
        return '[D2A]'  # Discord-to-Agent
    
    # System automated messages
    if sender_upper == 'SYSTEM':
        return '[S2A]'  # System-to-Agent
    
    # Captain to Agent
    if sender_upper in ['CAPTAIN', 'AGENT-4']:
        if 'ALL' in recipient_upper or 'BROADCAST' in recipient_upper:
            return '[C2A-ALL]'  # Captain broadcast
        return '[C2A]'  # Captain-to-Agent
    
    # Agent to Captain
    if recipient_upper in ['CAPTAIN', 'AGENT-4']:
        return '[A2C]'  # Agent-to-Captain
    
    # Agent to Agent
    if sender.startswith('Agent-') and recipient.startswith('Agent-'):
        return '[A2A]'  # Agent-to-Agent
    
    # Fallback to C2A for safety
    return '[C2A]'


def format_c2a_message(recipient: str, content: str, priority: str | None = None, sender: str = "CAPTAIN") -> str:
    """
    Format message with correct tag based on sender (UPDATED - Agent-1 2025-10-15).

    Per STANDARDS.md: Compact messaging with essential fields only.
    NOW SUPPORTS: [D2A], [G2A], [S2A], [C2A], [A2A], [A2C]

    Args:
        recipient: Target agent ID
        content: Message content
        priority: Optional priority level (defaults to 'normal')
        sender: Message sender (determines tag) - NEW!

    Returns:
        Formatted message with correct tag
    """
    priority = priority or "normal"
    
    # Get correct message tag based on sender
    tag = get_message_tag(sender, recipient)

    # Lean format: [Tag] Recipient | Priority (if urgent/high)
    if priority in ("urgent", "high"):
        header = f"{tag} {recipient} | {priority.upper()}"
    else:
        header = f"{tag} {recipient}"

    return f"{header}\n\n{content}"


class PyAutoGUIMessagingDelivery:
    """Delivers messages via PyAutoGUI to agent chat coordinates."""

    def __init__(self):
        if not PYAUTOGUI_AVAILABLE:
            raise ImportError("PyAutoGUI not available")
        self.pyautogui = pyautogui

    def validate_coordinates(self, agent_id: str, coords: tuple[int, int]) -> bool:
        """
        Validate coordinates before sending.

        Args:
            agent_id: Agent identifier
            coords: Coordinate tuple (x, y)

        Returns:
            True if coordinates are valid
        """
        if not coords or len(coords) != 2:
            logger.error(f"Invalid coordinates for {agent_id}: {coords}")
            return False

        x, y = coords
        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            logger.error(f"Coordinates must be numeric for {agent_id}: ({x}, {y})")
            return False

        return True

    def send_message(self, message) -> bool:
        """
        Send message to agent chat input coordinates.
        
        RACE CONDITION FIXES:
        - Clipboard locking (prevents concurrent overwrites)
        - Increased delays (1.0s for slow systems)
        - 3-attempt retry mechanism
        """
        # RACE CONDITION FIX #3: Retry mechanism (3 attempts)
        for attempt in range(3):
            try:
                success = self._send_message_attempt(message, attempt + 1)
                if success:
                    return True
                
                # Wait before retry
                if attempt < 2:
                    logger.warning(f"⚠️ Retry {attempt + 1}/3 for {message.recipient}")
                    time.sleep(1.0)
            
            except Exception as e:
                logger.error(f"❌ Attempt {attempt + 1} failed: {e}")
                if attempt < 2:
                    time.sleep(1.0)
        
        logger.error(f"❌ All 3 attempts failed for {message.recipient}")
        return False
    
    def _send_message_attempt(self, message, attempt_num: int) -> bool:
        """Single message delivery attempt with all race condition fixes."""
        try:
            # Get coordinates for agent
            from .coordinate_loader import get_coordinate_loader

            coord_loader = get_coordinate_loader()

            coords = coord_loader.get_chat_coordinates(message.recipient)
            if not coords:
                logger.error(f"No coordinates for {message.recipient}")
                return False

            x, y = coords

            # Get sender from message (check metadata first, then sender attribute)
            sender = "CAPTAIN"  # default
            if hasattr(message, 'sender'):
                sender = message.sender
            if isinstance(message.metadata, dict):
                sender = message.metadata.get('sender', sender)
            
            # Format message content using lean compact formatter with sender
            msg_content = format_c2a_message(
                recipient=message.recipient,
                content=message.content,
                priority=message.priority.value,
                sender=sender  # NEW: Pass sender for correct tagging!
            )

            # Click agent chat input
            self.pyautogui.moveTo(x, y)
            self.pyautogui.click()
            time.sleep(1.0)  # RACE CONDITION FIX #2: Increased from 0.3s

            # RACE CONDITION FIX #1: Clipboard lock (prevents concurrent overwrites!)
            with _clipboard_lock:
                # Paste message (clipboard locked during this entire block!)
                pyperclip.copy(msg_content)
                time.sleep(1.0)  # RACE CONDITION FIX #2: Increased from 0.2s
                
                self.pyautogui.hotkey("ctrl", "v")
                time.sleep(1.0)  # RACE CONDITION FIX #2: Increased from 0.5s (wait for paste)

            # Send message (use Ctrl+Enter for urgent priority)
            if message.priority.value == "urgent":
                self.pyautogui.hotkey("ctrl", "enter")
            else:
                self.pyautogui.press("enter")
            time.sleep(1.0)  # RACE CONDITION FIX #2: Increased from 0.5s

            logger.info(f"✅ Message sent to {message.recipient} at {coords} (attempt {attempt_num})")
            return True

        except Exception as e:
            logger.error(f"❌ PyAutoGUI delivery failed (attempt {attempt_num}): {e}")
            return False


def send_message_pyautogui(agent_id: str, message: str, timeout: int = 30) -> bool:
    """Legacy function for sending messages via PyAutoGUI."""
    try:
        delivery = PyAutoGUIMessagingDelivery()
        from .messaging_core import UnifiedMessage, UnifiedMessagePriority, UnifiedMessageType

        msg = UnifiedMessage(
            content=message,
            sender="CAPTAIN",
            recipient=agent_id,
            message_type=UnifiedMessageType.CAPTAIN_TO_AGENT,
            priority=UnifiedMessagePriority.URGENT,
            tags=[],
            metadata={},
        )
        return delivery.send_message(msg)
    except Exception as e:
        logger.error(f"Failed to send PyAutoGUI message: {e}")
        return False


def send_message_to_onboarding_coords(agent_id: str, message: str, timeout: int = 30) -> bool:
    """Send message to onboarding coordinates."""
    return send_message_pyautogui(agent_id, message, timeout)
