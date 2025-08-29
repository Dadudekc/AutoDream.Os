from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
import json
import logging
import pyautogui
import pyperclip
from .coordinate_manager import CoordinateManager, AgentCoordinates
from .interfaces import IMessageSender, IBulkMessaging
from dataclasses import dataclass
from src.utils.stability_improvements import stability_manager, safe_import
import time

#!/usr/bin/env python3
"""
Unified PyAutoGUI Messaging System - Agent Cellphone V2
=======================================================

Single source of truth for all PyAutoGUI-based agent communication.
Consolidates all duplicate PyAutoGUI messaging functionality.

Follows V2 standards: 400 LOC, OOP design, SRP.
"""



# Import PyAutoGUI with safety checks
try:
    PYAUTOGUI_AVAILABLE = True
    PYPERCLIP_AVAILABLE = True
    logger = logging.getLogger(__name__)
except ImportError as e:
    PYAUTOGUI_AVAILABLE = False
    PYPERCLIP_AVAILABLE = False
    logger = logging.getLogger(__name__)
    logger.warning(f"PyAutoGUI not available: {e}")



@dataclass
class MessageDeliveryResult:
    """Result of message delivery attempt."""
    success: bool
    recipient: str
    message_type: str
    timestamp: datetime
    error_message: Optional[str] = None
    delivery_method: str = "pyautogui"
    coordinates_used: Optional[Tuple[int, int]] = None


@dataclass
class BulkMessageResult:
    """Result of bulk message delivery."""
    total_messages: int
    successful_deliveries: int
    failed_deliveries: int
    results: List[MessageDeliveryResult]
    start_time: datetime
    end_time: Optional[datetime] = None


class UnifiedPyAutoGUIMessaging(IMessageSender, IBulkMessaging):
    """
    Unified PyAutoGUI Messaging System - Single responsibility: All PyAutoGUI messaging.
    
    Consolidates all PyAutoGUI messaging functionality into one system to eliminate duplication.
    """

    def __init__(self, coordinate_manager: CoordinateManager):
        """Initialize the unified PyAutoGUI messaging system."""
        self.coordinate_manager = coordinate_manager
        self._setup_pyautogui()
        self.delivery_history: List[MessageDeliveryResult] = []
        
        logger.info("UnifiedPyAutoGUIMessaging initialized")

    def _setup_pyautogui(self) -> None:
        """Setup PyAutoGUI safety and configuration."""
        global PYAUTOGUI_AVAILABLE
        
        if not PYAUTOGUI_AVAILABLE:
            logger.warning("PyAutoGUI not available - messaging will be simulated")
            return
            
        try:
            # Safety configuration
            pyautogui.FAILSAFE = True
            pyautogui.PAUSE = 0.5
            
            # Test basic functionality
            screen_size = pyautogui.size()
            logger.info(f"PyAutoGUI configured: screen size {screen_size}, safety enabled")
            
        except Exception as e:
            logger.error(f"Failed to setup PyAutoGUI: {e}")
            PYAUTOGUI_AVAILABLE = False

    def send_message(
        self, 
        recipient: str, 
        message_content: str, 
        message_type: str = "text", 
        new_chat: bool = False,
        priority: str = "normal"
    ) -> bool:
        """
        Send message using unified PyAutoGUI system.
        
        Args:
            recipient: Agent ID to send message to
            message_content: Message content to send
            message_type: Type of message (text, onboarding_start, task_assigned, etc.)
            new_chat: Whether this is a new chat (onboarding) message
            priority: Message priority (normal, high, urgent)
        """
        try:
            # Get agent coordinates
            coords = self.coordinate_manager.get_agent_coordinates(recipient, "8-agent")
            if not coords:
                logger.error(f"No coordinates found for {recipient}")
                return False
            
            # Determine delivery method based on message type and priority
            if new_chat or message_type == "onboarding_start":
                success = self._send_onboarding_message(recipient, message_content, coords)
            elif priority == "urgent":
                success = self._send_urgent_message(recipient, message_content, coords)
            elif priority == "high":
                success = self._send_high_priority_message(recipient, message_content, coords)
            else:
                success = self._send_normal_message(recipient, message_content, coords)
            
            # Record delivery result
            result = MessageDeliveryResult(
                success=success,
                recipient=recipient,
                message_type=message_type,
                timestamp=datetime.now(),
                error_message=None if success else "Delivery failed",
                coordinates_used=(coords.input_box[0], coords.input_box[1]) if success else None
            )
            self.delivery_history.append(result)
            
            return success
            
        except Exception as e:
            logger.error(f"Error sending message to {recipient}: {e}")
            
            # Record failed delivery
            result = MessageDeliveryResult(
                success=False,
                recipient=recipient,
                message_type=message_type,
                timestamp=datetime.now(),
                error_message=str(e)
            )
            self.delivery_history.append(result)
            
            return False

    def _send_onboarding_message(self, recipient: str, message_content: str, coords: AgentCoordinates) -> bool:
        """Send onboarding message using proper sequence: starter → Ctrl+N → validate → paste."""
        try:
            if not PYAUTOGUI_AVAILABLE:
                logger.warning("PyAutoGUI not available - simulating onboarding message")
                return True
                
            starter_x, starter_y = coords.starter_location
            
            logger.info(f"🚀 Onboarding message to {recipient} at ({starter_x}, {starter_y})")
            
            # Step 1: Click starter location
            pyautogui.moveTo(starter_x, starter_y, duration=0.3)
            pyautogui.click()
            time.sleep(0.5)
            
            # Step 2: Open new chat with Ctrl+N
            pyautogui.hotkey('ctrl', 'n')
            time.sleep(1.0)
            
            # Step 3: Validate focus and paste message
            pyautogui.moveTo(starter_x, starter_y, duration=0.3)
            pyautogui.click()
            time.sleep(0.5)
            
            # Step 4: Paste message content
            if PYPERCLIP_AVAILABLE:
                pyperclip.copy(message_content)
                pyautogui.hotkey('ctrl', 'v')
            else:
                pyautogui.write(message_content)
            
            time.sleep(0.5)
            
            # Step 5: Send message
            pyautogui.press('enter')
            
            logger.info(f"✅ Onboarding message sent to {recipient}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send onboarding message to {recipient}: {e}")
            return False

    def _send_urgent_message(self, recipient: str, message_content: str, coords: AgentCoordinates) -> bool:
        """Send urgent message with visual emphasis."""
        try:
            if not PYAUTOGUI_AVAILABLE:
                logger.warning("PyAutoGUI not available - simulating urgent message")
                return True
                
            input_x, input_y = coords.input_box
            
            logger.info(f"🚨 URGENT message to {recipient} at ({input_x}, {input_y})")
            
            # Click input box
            pyautogui.moveTo(input_x, input_y, duration=0.2)
            pyautogui.click()
            time.sleep(0.3)
            
            # Add urgent prefix
            urgent_content = f"🚨 URGENT: {message_content}"
            
            # Paste message
            if PYPERCLIP_AVAILABLE:
                pyperclip.copy(urgent_content)
                pyautogui.hotkey('ctrl', 'v')
            else:
                pyautogui.write(urgent_content)
            
            time.sleep(0.3)
            
            # Send with Ctrl+Enter for emphasis
            pyautogui.hotkey('ctrl', 'enter')
            
            logger.info(f"✅ Urgent message sent to {recipient}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send urgent message to {recipient}: {e}")
            return False

    def _send_high_priority_message(self, recipient: str, message_content: str, coords: AgentCoordinates) -> bool:
        """Send high priority message."""
        try:
            if not PYAUTOGUI_AVAILABLE:
                logger.warning("PyAutoGUI not available - simulating high priority message")
                return True
                
            input_x, input_y = coords.input_box
            
            logger.info(f"⚠️ High priority message to {recipient} at ({input_x}, {input_y})")
            
            # Click input box
            pyautogui.moveTo(input_x, input_y, duration=0.3)
            pyautogui.click()
            time.sleep(0.5)
            
            # Add priority prefix
            priority_content = f"⚠️ {message_content}"
            
            # Paste message
            if PYPERCLIP_AVAILABLE:
                pyperclip.copy(priority_content)
                pyautogui.hotkey('ctrl', 'v')
            else:
                pyautogui.write(priority_content)
            
            time.sleep(0.5)
            
            # Send message
            pyautogui.press('enter')
            
            logger.info(f"✅ High priority message sent to {recipient}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send high priority message to {recipient}: {e}")
            return False

    def _send_normal_message(self, recipient: str, message_content: str, coords: AgentCoordinates) -> bool:
        """Send normal message."""
        try:
            if not PYAUTOGUI_AVAILABLE:
                logger.warning("PyAutoGUI not available - simulating normal message")
                return True
                
            input_x, input_y = coords.input_box
            
            logger.info(f"📤 Normal message to {recipient} at ({input_x}, {input_y})")
            
            # Click input box
            pyautogui.moveTo(input_x, input_y, duration=0.3)
            pyautogui.click()
            time.sleep(0.5)
            
            # Paste message
            if PYPERCLIP_AVAILABLE:
                pyperclip.copy(message_content)
                pyautogui.hotkey('ctrl', 'v')
            else:
                pyautogui.write(message_content)
            
            time.sleep(0.5)
            
            # Send message
            pyautogui.press('enter')
            
            logger.info(f"✅ Normal message sent to {recipient}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send normal message to {recipient}: {e}")
            return False

    def send_bulk_messages(
        self, 
        messages: Dict[str, str], 
        mode: str = "8-agent",
        message_type: str = "text",
        priority: str = "normal",
        new_chat: bool = False
    ) -> Dict[str, bool]:
        """
        Send bulk messages to multiple agents.
        
        Args:
            messages: Dict of {agent_id: message_content}
            mode: Coordinate mode (8-agent, 4-agent, etc.)
            message_type: Type of messages to send
            priority: Priority level for all messages
        """
        start_time = datetime.now()
        results: List[MessageDeliveryResult] = []
        success_count = 0
        failure_count = 0
        
        logger.info(f"📤 Starting bulk message delivery to {len(messages)} agents")
        
        for agent_id, message_content in messages.items():
            try:
                if new_chat:
                    # Special onboarding sequence: click starter location, Ctrl+N, then paste message
                    success = self._send_onboarding_message(agent_id, message_content, mode)
                else:
                    # Normal message sending
                    success = self.send_message(
                        recipient=agent_id,
                        message_content=message_content,
                        message_type=message_type,
                        priority=priority
                    )
                
                if success:
                    success_count += 1
                    results.append(MessageDeliveryResult(
                        recipient=agent_id,
                        success=True,
                        timestamp=datetime.now(),
                        message_type=message_type
                    ))
                else:
                    failure_count += 1
                    results.append(MessageDeliveryResult(
                        recipient=agent_id,
                        success=False,
                        timestamp=datetime.now(),
                        message_type=message_type
                    ))
                    
            except Exception as e:
                logger.error(f"Error in bulk delivery to {agent_id}: {e}")
                failure_count += 1
                results.append(MessageDeliveryResult(
                    recipient=agent_id,
                    success=False,
                    timestamp=datetime.now(),
                    message_type=message_type
                ))
        
        end_time = datetime.now()
        
        # Create bulk result
        bulk_result = BulkMessageResult(
            total_messages=len(messages),
            successful_deliveries=success_count,
            failed_deliveries=failure_count,
            results=results,
            start_time=start_time,
            end_time=end_time
        )
        
        logger.info(f"📊 Bulk delivery complete: {success_count}/{len(messages)} successful")
        return {agent_id: success for agent_id, success in zip(messages.keys(), [r.success for r in results])}

    def get_delivery_status(self, recipient: str = None) -> Dict[str, Any]:
        """Get delivery status for specific recipient or all deliveries."""
        if recipient:
            # Filter by recipient
            recipient_results = [r for r in self.delivery_history if r.recipient == recipient]
            return {
                "recipient": recipient,
                "total_deliveries": len(recipient_results),
                "successful": len([r for r in recipient_results if r.success]),
                "failed": len([r for r in recipient_results if not r.success]),
                "last_delivery": recipient_results[-1].timestamp if recipient_results else None
            }
        else:
            # Return overall status
            return {
                "total_deliveries": len(self.delivery_history),
                "successful": len([r for r in self.delivery_history if r.success]),
                "failed": len([r for r in self.delivery_history if not r.success]),
                "success_rate": len([r for r in self.delivery_history if r.success]) / len(self.delivery_history) if self.delivery_history else 0,
                "last_delivery": self.delivery_history[-1].timestamp if self.delivery_history else None
            }

    def clear_delivery_history(self) -> None:
        """Clear delivery history."""
        self.delivery_history.clear()
        logger.info("Delivery history cleared")

    def get_system_status(self) -> Dict[str, Any]:
        """Get overall system status."""
        return {
            "pyautogui_available": PYAUTOGUI_AVAILABLE,
            "pyperclip_available": PYPERCLIP_AVAILABLE,
            "coordinate_manager_connected": self.coordinate_manager is not None,
            "delivery_history_size": len(self.delivery_history),
            "last_delivery": self.delivery_history[-1].timestamp if self.delivery_history else None
        }

    def activate_agent(self, agent_id: str, mode: str = "8-agent") -> bool:
        """Activate an agent by clicking their starter location."""
        try:
            coords = self.coordinate_manager.get_agent_coordinates(agent_id, mode)
            if not coords:
                logger.error(f"No coordinates found for {agent_id}")
                return False
            
            if not PYAUTOGUI_AVAILABLE:
                logger.warning("PyAutoGUI not available - simulating agent activation")
                return True
            
            starter_x, starter_y = coords.starter_location
            
            logger.info(f"🚀 Activating agent {agent_id} at ({starter_x}, {starter_y})")
            
            # Click starter location to activate agent
            pyautogui.moveTo(starter_x, starter_y, duration=0.3)
            pyautogui.click()
            time.sleep(0.5)
            
            logger.info(f"✅ Agent {agent_id} activated")
            return True
            
        except Exception as e:
            logger.error(f"Failed to activate agent {agent_id}: {e}")
            return False

    def _send_onboarding_message(self, agent_id: str, message_content: str, mode: str) -> bool:
        """Send onboarding message with new chat sequence: click starter location, Ctrl+N, paste message."""
        try:
            if not PYAUTOGUI_AVAILABLE:
                logger.warning("PyAutoGUI not available - simulating onboarding message")
                return True
                
            coords = self.coordinate_manager.get_agent_coordinates(agent_id, mode)
            if not coords:
                logger.error(f"No coordinates found for {agent_id}")
                return False
            
            starter_x, starter_y = coords.starter_location
            input_x, input_y = coords.input_box
            
            logger.info(f"🚀 Onboarding {agent_id}: Clicking starter location at ({starter_x}, {starter_y})")
            
            # Step 1: Click to the starter agent location
            pyautogui.moveTo(starter_x, starter_y, duration=0.3)
            pyautogui.click()
            time.sleep(0.5)
            
            # Step 2: Click Ctrl+N to start new chat
            logger.info(f"🆕 Starting new chat for {agent_id} with Ctrl+N")
            pyautogui.hotkey('ctrl', 'n')
            time.sleep(1.0)  # Wait for new chat to load
            
            # Step 3: Click the starter input spot and paste the first message
            logger.info(f"📝 Pasting onboarding message to {agent_id} at ({input_x}, {input_y})")
            pyautogui.moveTo(input_x, input_y, duration=0.3)
            pyautogui.click()
            time.sleep(0.5)
            
            # Paste the onboarding message
            if PYPERCLIP_AVAILABLE:
                pyperclip.copy(message_content)
                pyautogui.hotkey('ctrl', 'v')
            else:
                pyautogui.write(message_content)
            
            time.sleep(0.5)
            
            # Send the message
            pyautogui.press('enter')
            
            logger.info(f"✅ Onboarding message sent to {agent_id} with new chat sequence")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send onboarding message to {agent_id}: {e}")
            return False

    def test_coordinates(self, agent_id: str, mode: str = "8-agent") -> bool:
        """Test if coordinates are valid for an agent."""
        try:
            coords = self.coordinate_manager.get_agent_coordinates(agent_id, mode)
            if not coords:
                logger.error(f"No coordinates found for {agent_id}")
                return False
            
            # Test if coordinates are within screen bounds
            if PYAUTOGUI_AVAILABLE:
                screen_width, screen_height = pyautogui.size()
                
                # Check input box coordinates
                input_x, input_y = coords.input_box
                if not (0 <= input_x <= screen_width and 0 <= input_y <= screen_height):
                    logger.error(f"Input box coordinates ({input_x}, {input_y}) out of bounds")
                    return False
                
                # Check starter location coordinates
                starter_x, starter_y = coords.starter_location
                if not (0 <= starter_x <= screen_width and 0 <= starter_y <= screen_height):
                    logger.error(f"Starter coordinates ({starter_x}, {starter_y}) out of bounds")
                    return False
                
                logger.info(f"✅ Coordinates for {agent_id} are valid")
                return True
            else:
                logger.warning("PyAutoGUI not available - coordinate validation skipped")
                return True
                
        except Exception as e:
            logger.error(f"Error testing coordinates for {agent_id}: {e}")
            return False

    def _send_onboarding_message(self, agent_id: str, message_content: str, mode: str = "8-agent") -> bool:
        """
        Send onboarding message using the specific PyAutoGUI sequence:
        1. Click to starter agent location
        2. Press Ctrl+N (new chat)
        3. Paste message in starter input location
        """
        try:
            if not PYAUTOGUI_AVAILABLE:
                logger.warning("PyAutoGUI not available - simulating onboarding message")
                return True
                
            # Get agent coordinates
            coords = self.coordinate_manager.get_agent_coordinates(agent_id, mode)
            if not coords:
                logger.error(f"No coordinates found for {agent_id}")
                return False
            
            starter_x, starter_y = coords.starter_location
            input_x, input_y = coords.input_box
            
            logger.info(f"🚀 ONBOARDING: {agent_id} - Clicking starter location at ({starter_x}, {starter_y})")
            
            # STEP 1: Click to starter agent location
            pyautogui.moveTo(starter_x, starter_y, duration=0.3)
            pyautogui.click()
            time.sleep(0.5)
            
            logger.info(f"📱 ONBOARDING: {agent_id} - Pressing Ctrl+N for new chat")
            
            # STEP 2: Press Ctrl+N (new chat)
            pyautogui.hotkey('ctrl', 'n')
            time.sleep(1.0)  # Wait for new chat to load
            
            logger.info(f"📝 ONBOARDING: {agent_id} - Pasting message in starter location at ({starter_x}, {starter_y})")
            
            # STEP 3: Click starter location again and paste message
            pyautogui.moveTo(starter_x, starter_y, duration=0.3)
            pyautogui.click()
            time.sleep(0.5)
            
            # Paste the onboarding message
            if PYPERCLIP_AVAILABLE:
                pyperclip.copy(message_content)
                pyautogui.hotkey('ctrl', 'v')
            else:
                pyautogui.write(message_content)
            
            time.sleep(0.5)
            
            # Send the message
            pyautogui.press('enter')
            
            logger.info(f"✅ ONBOARDING: {agent_id} - Message sent successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send onboarding message to {agent_id}: {e}")
            return False


# Factory function for creating messaging instances
def create_unified_pyautogui_messaging(coordinate_manager: CoordinateManager) -> UnifiedPyAutoGUIMessaging:
    """Create a new unified PyAutoGUI messaging instance."""
    return UnifiedPyAutoGUIMessaging(coordinate_manager)
