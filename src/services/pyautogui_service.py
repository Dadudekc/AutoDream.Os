#!/usr/bin/env python3
"""
PyAutoGUI Service - Agent Cellphone V2
======================================

PyAutoGUI operations for agent activation and messaging.
Follows V2 standards: ≤ 200 LOC, SRP, OOP design, CLI interface.
"""

import json
import time
import logging
import pyautogui
import pyperclip
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass
import argparse

@dataclass
class AgentCoordinates:
    """Agent coordinate data structure."""
    agent_id: str
    starter_location: Tuple[int, int]
    input_box: Tuple[int, int]
    mode: str

class PyAutoGUIService:
    """
    PyAutoGUI Service - Single responsibility: PyAutoGUI operations for agent coordination.
    
    This service manages:
    - Agent activation through PyAutoGUI
    - Message sending to agents
    - Coordinate management and validation
    - PyAutoGUI safety and configuration
    """
    
    def __init__(self, coordinates_file: str = "runtime/agent_comms/cursor_agent_coords.json"):
        """Initialize PyAutoGUI Service."""
        self.coordinates_file = Path(coordinates_file)
        self.logger = self._setup_logging()
        self.coordinates = self._load_coordinates()
        
        # Initialize PyAutoGUI settings
        self._setup_pyautogui()
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for the service."""
        logger = logging.getLogger("PyAutoGUIService")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def _setup_pyautogui(self):
        """Setup PyAutoGUI safety and configuration."""
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.5
        self.logger.info("PyAutoGUI configured with safety settings")
    
    def _load_coordinates(self) -> Dict[str, Any]:
        """Load agent coordinates from configuration file."""
        try:
            if self.coordinates_file.exists():
                with open(self.coordinates_file, 'r') as f:
                    coords = json.load(f)
                    self.logger.info(f"Coordinates loaded: {len(coords)} agent configurations")
                    return coords
            else:
                self.logger.error(f"Coordinate file not found: {self.coordinates_file}")
                return {}
        except Exception as e:
            self.logger.error(f"Error loading coordinates: {e}")
            return {}
    
    def get_agent_coordinates(self, agent_id: str, mode: str = "5-agent") -> Optional[AgentCoordinates]:
        """Get coordinates for a specific agent."""
        try:
            if mode in self.coordinates and agent_id in self.coordinates[mode]:
                agent_coords = self.coordinates[mode][agent_id]
                
                starter_x = agent_coords["starter_location_box"]["x"]
                starter_y = agent_coords["starter_location_box"]["y"]
                input_x = agent_coords["input_box"]["x"]
                input_y = agent_coords["input_box"]["y"]
                
                return AgentCoordinates(
                    agent_id=agent_id,
                    starter_location=(starter_x, starter_y),
                    input_box=(input_x, input_y),
                    mode=mode
                )
            else:
                self.logger.warning(f"Coordinates not found for {agent_id} in {mode} mode")
                return None
        except Exception as e:
            self.logger.error(f"Error getting coordinates for {agent_id}: {e}")
            return None
    
    def activate_agent(self, agent_id: str, mode: str = "5-agent") -> bool:
        """Activate an agent by clicking their starter location."""
        try:
            coords = self.get_agent_coordinates(agent_id, mode)
            if not coords:
                self.logger.error(f"No coordinates for {agent_id}")
                return False
            
            x, y = coords.starter_location
            
            self.logger.info(f"Activating {agent_id} at coordinates ({x}, {y})")
            
            # Move to and click starter location
            pyautogui.moveTo(x, y, duration=0.5)
            pyautogui.click()
            
            # Wait for activation
            time.sleep(1.0)
            
            self.logger.info(f"✅ {agent_id} activated successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error activating {agent_id}: {e}")
            return False
    
    def send_message_to_agent(self, agent_id: str, message: str, mode: str = "5-agent", 
                             use_shift_enter: bool = True) -> bool:
        """Send a message to an agent by typing in their input box."""
        try:
            coords = self.get_agent_coordinates(agent_id, mode)
            if not coords:
                self.logger.error(f"No coordinates for {agent_id}")
                return False
            
            x, y = coords.input_box
            
            self.logger.info(f"Sending message to {agent_id} at coordinates ({x}, {y})")
            
            # Click input box
            pyautogui.moveTo(x, y, duration=0.5)
            pyautogui.click()
            
            # Clear existing text and type message
            pyautogui.hotkey('ctrl', 'a')  # Select all
            pyautogui.press('delete')       # Clear
            
            if use_shift_enter and '\n' in message:
                # Handle multi-line messages with Shift+Enter
                lines = message.split('\n')
                for i, line in enumerate(lines):
                    if i > 0:  # Add line break for all lines except the first
                        pyautogui.hotkey('shift', 'enter')  # Shift+Enter for line break
                    pyautogui.typewrite(line, interval=0.05)
            else:
                # Single line message
                pyautogui.typewrite(message, interval=0.05)
            
            # Send message (Enter key)
            pyautogui.press('enter')
            
            self.logger.info(f"✅ Message sent to {agent_id}: {message[:50]}...")
            return True
            
        except Exception as e:
            self.logger.error(f"Error sending message to {agent_id}: {e}")
            return False
    
    def send_fast_message(self, agent_id: str, message_template: str, mode: str = "5-agent") -> bool:
        """Fast message sending using clipboard and template."""
        try:
            coords = self.get_agent_coordinates(agent_id, mode)
            if not coords:
                self.logger.error(f"No coordinates for {agent_id}")
                return False
            
            x, y = coords.input_box
            
            self.logger.info(f"Fast message to {agent_id} at coordinates ({x}, {y})")
            
            # Copy template to clipboard first
            pyperclip.copy(message_template)
            
            # Click input box
            pyautogui.moveTo(x, y, duration=0.5)
            pyautogui.click()
            
            # Clear existing text
            pyautogui.hotkey('ctrl', 'a')  # Select all
            pyautogui.press('delete')       # Clear
            
            # Type agent name
            pyautogui.typewrite(agent_id, interval=0.05)
            
            # Shift+Enter twice for spacing
            pyautogui.hotkey('shift', 'enter')  # First line break
            pyautogui.hotkey('shift', 'enter')  # Second line break
            
            # Paste the message template
            pyautogui.hotkey('ctrl', 'v')  # Paste
            
            # Send message (Enter key)
            pyautogui.press('enter')
            
            self.logger.info(f"✅ Fast message sent to {agent_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error sending fast message to {agent_id}: {e}")
            return False
    
    def validate_coordinates(self) -> Dict[str, Any]:
        """Validate all loaded coordinates."""
        validation_results = {
            "total_modes": len(self.coordinates),
            "total_agents": 0,
            "valid_coordinates": 0,
            "missing_coordinates": 0,
            "errors": []
        }
        
        for mode, agents in self.coordinates.items():
            for agent_id, coords in agents.items():
                validation_results["total_agents"] += 1
                
                try:
                    # Check required coordinate fields
                    required_fields = ["starter_location_box", "input_box"]
                    if all(field in coords for field in required_fields):
                        validation_results["valid_coordinates"] += 1
                    else:
                        validation_results["missing_coordinates"] += 1
                        validation_results["errors"].append(f"Missing fields for {agent_id} in {mode}")
                except Exception as e:
                    validation_results["errors"].append(f"Error validating {agent_id} in {mode}: {e}")
        
        return validation_results

def main():
    """CLI interface for PyAutoGUI Service."""
    parser = argparse.ArgumentParser(description="PyAutoGUI Service CLI")
    parser.add_argument("--activate", type=str, help="Activate specific agent")
    parser.add_argument("--send", type=str, help="Send message to specific agent")
    parser.add_argument("--message", type=str, help="Message content to send")
    parser.add_argument("--fast", type=str, help="Send fast message to specific agent")
    parser.add_argument("--template", type=str, help="Message template for fast sending")
    parser.add_argument("--validate", action="store_true", help="Validate coordinates")
    parser.add_argument("--mode", type=str, default="5-agent", help="Agent mode (default: 5-agent)")
    
    args = parser.parse_args()
    
    # Initialize service
    pyautogui_service = PyAutoGUIService()
    
    if args.activate:
        success = pyautogui_service.activate_agent(args.activate, args.mode)
        print(f"Agent activation: {'✅ Success' if success else '❌ Failed'}")
    
    elif args.send and args.message:
        success = pyautogui_service.send_message_to_agent(args.send, args.message, args.mode)
        print(f"Message sending: {'✅ Success' if success else '❌ Failed'}")
    
    elif args.fast and args.template:
        success = pyautogui_service.send_fast_message(args.fast, args.template, args.mode)
        print(f"Fast message sending: {'✅ Success' if success else '❌ Failed'}")
    
    elif args.validate:
        results = pyautogui_service.validate_coordinates()
        print("📊 Coordinate Validation Results:")
        for key, value in results.items():
            print(f"  {key}: {value}")
    
    else:
        print("🤖 PyAutoGUI Service - Use --help for available commands")

if __name__ == "__main__":
    main()
