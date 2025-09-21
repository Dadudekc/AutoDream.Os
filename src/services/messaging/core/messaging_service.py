#!/usr/bin/env python3
"""
Core Messaging Service
======================

Core messaging functionality for agent-to-agent communication.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List

from src.core.coordinate_loader import CoordinateLoader

# Lazy import to prevent hard dep at import time
try:
    import pyautogui  # noqa: F401
    import pyperclip  # noqa: F401
except Exception as e:
    pyautogui = None  # type: ignore
    pyperclip = None  # type: ignore
    logging.warning(f"PyAutoGUI import failed: {e}")

logger = logging.getLogger(__name__)


class MessagingService:
    """Core messaging service for agent communication."""
    
    def __init__(self, coord_path: str = "config/coordinates.json") -> None:
        """Initialize messaging service with coordinate validation."""
        self.coords_file = coord_path
        self.loader = CoordinateLoader(coord_path)
        self.loader.load()
        self.validation_report = self.loader.validate_all()
        
        if not self.validation_report.is_all_ok():
            logger.warning("Coordinate validation issues detected")
            for issue in self.validation_report.issues:
                logger.warning(f"  - {issue}")
    
    def send_message(self, agent_id: str, message: str, from_agent: str = "Agent-2", priority: str = "NORMAL") -> bool:
        """Send message to specific agent via PyAutoGUI automation."""
        if not self._is_agent_active(agent_id):
            logger.warning(f"Agent {agent_id} is inactive, message not sent")
            return False
            
        try:
            # Get agent coordinates
            try:
                coords = self.loader.get_agent_coordinates(agent_id)
            except ValueError as e:
                logger.error(f"Agent {agent_id} not found in coordinates: {e}")
                return False
            
            # Format A2A message
            formatted_message = self._format_a2a_message(from_agent, agent_id, message, priority)
            
            # Send via PyAutoGUI
            success = self._paste_to_coords(coords, formatted_message)
            
            if success:
                logger.info(f"Message sent to {agent_id} from {from_agent}")
            else:
                logger.error(f"Failed to send message to {agent_id}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error sending message to {agent_id}: {e}")
            return False
    
    def broadcast_message(self, message: str, from_agent: str = "Agent-2", priority: str = "NORMAL") -> Dict[str, bool]:
        """Send message to all active agents."""
        results = {}
        
        for agent_id in self.loader.get_agent_ids():
            if self._is_agent_active(agent_id):
                results[agent_id] = self.send_message(agent_id, message, from_agent, priority)
            else:
                results[agent_id] = False
                logger.info(f"Skipping inactive agent {agent_id}")
        
        return results
    
    def _get_quality_guidelines(self) -> str:
        """Get quality guidelines reminder for all agent communications."""
        return """🎯 QUALITY GUIDELINES REMINDER
============================================================
📋 V2 Compliance Requirements:
• File Size: ≤400 lines (hard limit)
• Enums: ≤3 per file
• Classes: ≤5 per file
• Functions: ≤10 per file
• Complexity: ≤10 cyclomatic complexity per function
• Parameters: ≤5 per function
• Inheritance: ≤2 levels deep

🚫 Forbidden Patterns (Red Flags):
• Abstract Base Classes (without 2+ implementations)
• Excessive async operations (without concurrency need)
• Complex inheritance chains (>2 levels)
• Event sourcing for simple operations
• Dependency injection for simple objects
• Threading for synchronous operations
• 20+ fields per entity
• 5+ enums per file

✅ Required Patterns (Green Flags):
• Simple data classes with basic fields
• Direct method calls instead of complex event systems
• Synchronous operations for simple tasks
• Basic validation for essential data
• Simple configuration with defaults
• Basic error handling with clear messages

🎯 KISS Principle: Start with the simplest solution that works!
📊 QUALITY GATES: Run `python quality_gates.py` before submitting code!
============================================================"""
    
    def _format_a2a_message(self, from_agent: str, to_agent: str, message: str, priority: str = "NORMAL") -> str:
        """Format agent-to-agent message with standard template and quality guidelines."""
        quality_guidelines = self._get_quality_guidelines()
        return f"""============================================================
[A2A] MESSAGE
============================================================
📤 FROM: {from_agent}
📥 TO: {to_agent}
Priority: {priority}
Tags: GENERAL
------------------------------------------------------------
{message}
📝 DISCORD DEVLOG REMINDER: Create a Discord devlog for this action in devlogs/ directory
------------------------------------------------------------
{quality_guidelines}
------------------------------------------------------------
"""
    
    def _paste_to_coords(self, coords, message: str) -> bool:
        """Paste message to coordinates using PyAutoGUI with fallback to inbox."""
        if not pyautogui or not pyperclip:
            logger.warning("PyAutoGUI or Pyperclip not available, falling back to inbox delivery")
            return self._fallback_to_inbox(coords, message)
        
        try:
            # Copy message to clipboard
            pyperclip.copy(message)
            
            # Click coordinates
            pyautogui.click(coords[0], coords[1])
            pyautogui.sleep(0.5)
            
            # Paste message
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.sleep(0.5)
            
            # Send message
            pyautogui.press('enter')
            
            return True
            
        except Exception as e:
            logger.warning(f"PyAutoGUI failed, falling back to inbox delivery: {e}")
            return self._fallback_to_inbox(coords, message)
    
    def _fallback_to_inbox(self, coords, message: str) -> bool:
        """Fallback to inbox delivery when PyAutoGUI is not available."""
        try:
            # Import inbox delivery
            from src.services.messaging.delivery.inbox_delivery import send_message_inbox
            from src.services.messaging.models import UnifiedMessage
            from datetime import datetime
            
            # Extract agent ID from coordinates (this is a simplified approach)
            # In a real implementation, you'd need to map coordinates back to agent IDs
            agent_id = self._get_agent_id_from_coords(coords)
            if not agent_id:
                logger.error("Could not determine agent ID from coordinates")
                return False
            
            # Create unified message
            unified_message = UnifiedMessage(
                content=message,
                sender="Discord-Commander",
                recipient=agent_id,
                priority="NORMAL",
                message_type="text",
                timestamp=datetime.now()
            )
            
            # Send via inbox
            return send_message_inbox(unified_message)
            
        except Exception as e:
            logger.error(f"Inbox fallback failed: {e}")
            return False
    
    def _get_agent_id_from_coords(self, coords) -> str:
        """Get agent ID from coordinates (simplified mapping)."""
        try:
            # This is a simplified approach - in practice you'd need a reverse lookup
            # For now, we'll use a basic mapping based on the coordinates
            x, y = coords[0], coords[1]
            
            # Map coordinates to agent IDs (this matches the coordinates.json)
            coord_to_agent = {
                (-1269, 481): "Agent-1",
                (-308, 480): "Agent-2", 
                (-1269, 1001): "Agent-3",
                (-308, 1000): "Agent-4",
                (652, 421): "Agent-5",
                (1612, 419): "Agent-6",
                (920, 851): "Agent-7",
                (1611, 941): "Agent-8"
            }
            
            return coord_to_agent.get((x, y), "Agent-1")  # Default to Agent-1
            
        except Exception as e:
            logger.error(f"Error mapping coordinates to agent ID: {e}")
            return "Agent-1"  # Default fallback
    
    def _is_agent_active(self, agent_id: str) -> bool:
        """Check if agent is active."""
        try:
            agents = self.loader.coordinates.get("agents", {})
            agent_data = agents.get(agent_id, {})
            return agent_data.get("active", True)
        except Exception:
            return True  # Default to active if check fails
