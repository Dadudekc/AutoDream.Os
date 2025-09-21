#!/usr/bin/env python3
"""
Coordinate Mapper - Agent Coordinate Management Tool
==================================================

Interactive tool for mapping and setting agent coordinates for the messaging system.
Supports both onboarding and chat input coordinates for all agents or individually.

Author: Agent-1 (Infrastructure Specialist)
License: MIT
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
import pyautogui
import time

class CoordinateMapper:
    """Interactive coordinate mapping tool for agent messaging system."""
    
    def __init__(self, config_path: str = "config/coordinates.json"):
        self.config_path = config_path
        self.coordinates = self._load_coordinates()
        self.screen_width, self.screen_height = pyautogui.size()
        
    def _load_coordinates(self) -> Dict[str, Any]:
        """Load coordinates from configuration file."""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return self._get_default_structure()
        except Exception as e:
            print(f"Error loading coordinates: {e}")
            return self._get_default_structure()
    
    def _get_default_structure(self) -> Dict[str, Any]:
        """Get default coordinate structure."""
        return {
            "version": "2.0",
            "last_updated": "",
            "agents": {}
        }
    
    def _save_coordinates(self):
        """Save coordinates to configuration file."""
        try:
            # Ensure config directory exists
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.coordinates, f, indent=2, ensure_ascii=False)
            print(f"✅ Coordinates saved to {self.config_path}")
        except Exception as e:
            print(f"❌ Error saving coordinates: {e}")
    
    def _validate_coordinates(self, x: int, y: int) -> bool:
        """Validate coordinates are within screen bounds."""
        return 0 <= x <= self.screen_width and 0 <= y <= self.screen_height
    
    def _get_mouse_position(self, prompt: str) -> tuple:
        """Get mouse position with user interaction."""
        print(f"\n{prompt}")
        print("Move your mouse to the target position and press ENTER...")
        print("(Press Ctrl+C to cancel)")
        
        try:
            input()  # Wait for user input
            x, y = pyautogui.position()
            print(f"📍 Captured coordinates: ({x}, {y})")
            return x, y
        except KeyboardInterrupt:
            print("\n❌ Cancelled by user")
            return None, None
    
    def show_current_coordinates(self):
        """Display current coordinate configuration."""
        print("\n" + "="*60)
        print("📊 CURRENT COORDINATE CONFIGURATION")
        print("="*60)
        print(f"Screen Size: {self.screen_width}x{self.screen_height}")
        print(f"Config File: {self.config_path}")
        print(f"Last Updated: {self.coordinates.get('last_updated', 'Never')}")
        print()
        
        if not self.coordinates.get('agents'):
            print("❌ No agents configured")
            return
        
        for agent_id, agent_data in self.coordinates['agents'].items():
            status = "✅ Active" if agent_data.get('active', True) else "❌ Inactive"
            print(f"🤖 {agent_id} - {status}")
            print(f"   📍 Chat Input: {agent_data.get('chat_input_coordinates', 'Not set')}")
            print(f"   🎯 Onboarding: {agent_data.get('onboarding_coordinates', 'Not set')}")
            print(f"   📝 Description: {agent_data.get('description', 'No description')}")
            print()
    
    def map_all_agents(self):
        """Map coordinates for all agents."""
        print("\n" + "="*60)
        print("🎯 MAPPING ALL AGENTS")
        print("="*60)
        print("This will map both onboarding and chat input coordinates for all agents.")
        print("You'll be prompted to click on each agent's positions.")
        print()
        
        # Get all agent IDs
        agent_ids = list(self.coordinates.get('agents', {}).keys())
        if not agent_ids:
            print("❌ No agents found in configuration")
            return
        
        print(f"Agents to map: {', '.join(agent_ids)}")
        print()
        
        for agent_id in agent_ids:
            print(f"\n🎯 Mapping {agent_id}...")
            
            # Map onboarding coordinates
            print(f"\n1. Onboarding coordinates for {agent_id}:")
            x, y = self._get_mouse_position(f"Click on {agent_id}'s onboarding area")
            if x is not None and y is not None:
                if self._validate_coordinates(x, y):
                    self.coordinates['agents'][agent_id]['onboarding_coordinates'] = [x, y]
                    print(f"✅ Onboarding coordinates set: ({x}, {y})")
                else:
                    print(f"❌ Coordinates ({x}, {y}) are outside screen bounds")
            
            # Map chat input coordinates
            print(f"\n2. Chat input coordinates for {agent_id}:")
            x, y = self._get_mouse_position(f"Click on {agent_id}'s chat input area")
            if x is not None and y is not None:
                if self._validate_coordinates(x, y):
                    self.coordinates['agents'][agent_id]['chat_input_coordinates'] = [x, y]
                    print(f"✅ Chat input coordinates set: ({x}, {y})")
                else:
                    print(f"❌ Coordinates ({x}, {y}) are outside screen bounds")
        
        # Update timestamp
        from datetime import datetime
        self.coordinates['last_updated'] = datetime.now().isoformat()
        
        # Save coordinates
        self._save_coordinates()
        print("\n✅ All agents mapped successfully!")
    
    def map_single_agent(self, agent_id: str):
        """Map coordinates for a single agent."""
        print(f"\n🎯 MAPPING SINGLE AGENT: {agent_id}")
        print("="*60)
        
        # Ensure agent exists
        if agent_id not in self.coordinates.get('agents', {}):
            print(f"❌ Agent {agent_id} not found in configuration")
            return
        
        print(f"Mapping coordinates for {agent_id}...")
        print()
        
        # Map onboarding coordinates
        print("1. Onboarding coordinates:")
        x, y = self._get_mouse_position(f"Click on {agent_id}'s onboarding area")
        if x is not None and y is not None:
            if self._validate_coordinates(x, y):
                self.coordinates['agents'][agent_id]['onboarding_coordinates'] = [x, y]
                print(f"✅ Onboarding coordinates set: ({x}, {y})")
            else:
                print(f"❌ Coordinates ({x}, {y}) are outside screen bounds")
        
        # Map chat input coordinates
        print("\n2. Chat input coordinates:")
        x, y = self._get_mouse_position(f"Click on {agent_id}'s chat input area")
        if x is not None and y is not None:
            if self._validate_coordinates(x, y):
                self.coordinates['agents'][agent_id]['chat_input_coordinates'] = [x, y]
                print(f"✅ Chat input coordinates set: ({x}, {y})")
            else:
                print(f"❌ Coordinates ({x}, {y}) are outside screen bounds")
        
        # Update timestamp
        from datetime import datetime
        self.coordinates['last_updated'] = datetime.now().isoformat()
        
        # Save coordinates
        self._save_coordinates()
        print(f"\n✅ {agent_id} mapped successfully!")
    
    def test_coordinates(self, agent_id: str):
        """Test coordinates for a specific agent."""
        print(f"\n🧪 TESTING COORDINATES FOR {agent_id}")
        print("="*60)
        
        if agent_id not in self.coordinates.get('agents', {}):
            print(f"❌ Agent {agent_id} not found in configuration")
            return
        
        agent_data = self.coordinates['agents'][agent_id]
        
        # Test onboarding coordinates
        onboarding_coords = agent_data.get('onboarding_coordinates')
        if onboarding_coords:
            print(f"🎯 Testing onboarding coordinates: {onboarding_coords}")
            print("Moving mouse to onboarding position...")
            pyautogui.moveTo(onboarding_coords[0], onboarding_coords[1], duration=1)
            print("✅ Mouse moved to onboarding position")
        else:
            print("❌ No onboarding coordinates set")
        
        time.sleep(2)
        
        # Test chat input coordinates
        chat_coords = agent_data.get('chat_input_coordinates')
        if chat_coords:
            print(f"💬 Testing chat input coordinates: {chat_coords}")
            print("Moving mouse to chat input position...")
            pyautogui.moveTo(chat_coords[0], chat_coords[1], duration=1)
            print("✅ Mouse moved to chat input position")
        else:
            print("❌ No chat input coordinates set")
    
    def validate_all_coordinates(self):
        """Validate all coordinates are within screen bounds."""
        print("\n🔍 VALIDATING ALL COORDINATES")
        print("="*60)
        
        issues = []
        for agent_id, agent_data in self.coordinates.get('agents', {}).items():
            # Check onboarding coordinates
            onboarding_coords = agent_data.get('onboarding_coordinates')
            if onboarding_coords:
                x, y = onboarding_coords
                if not self._validate_coordinates(x, y):
                    issues.append(f"{agent_id} onboarding: ({x}, {y}) outside screen bounds")
            
            # Check chat input coordinates
            chat_coords = agent_data.get('chat_input_coordinates')
            if chat_coords:
                x, y = chat_coords
                if not self._validate_coordinates(x, y):
                    issues.append(f"{agent_id} chat input: ({x}, {y}) outside screen bounds")
        
        if issues:
            print("❌ Coordinate validation issues found:")
            for issue in issues:
                print(f"   - {issue}")
        else:
            print("✅ All coordinates are valid!")
    
    def interactive_menu(self):
        """Show interactive menu."""
        while True:
            print("\n" + "="*60)
            print("🎯 COORDINATE MAPPER - AGENT MESSAGING SYSTEM")
            print("="*60)
            print("1. Show current coordinates")
            print("2. Map all agents")
            print("3. Map single agent")
            print("4. Test coordinates")
            print("5. Validate all coordinates")
            print("6. Exit")
            print()
            
            choice = input("Select option (1-6): ").strip()
            
            if choice == "1":
                self.show_current_coordinates()
            elif choice == "2":
                self.map_all_agents()
            elif choice == "3":
                agent_id = input("Enter agent ID (e.g., Agent-1): ").strip()
                if agent_id:
                    self.map_single_agent(agent_id)
            elif choice == "4":
                agent_id = input("Enter agent ID to test (e.g., Agent-1): ").strip()
                if agent_id:
                    self.test_coordinates(agent_id)
            elif choice == "5":
                self.validate_all_coordinates()
            elif choice == "6":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid option. Please select 1-6.")

def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Coordinate Mapper for Agent Messaging System")
    parser.add_argument("--config", default="config/coordinates.json", help="Path to coordinates config file")
    parser.add_argument("--show", action="store_true", help="Show current coordinates")
    parser.add_argument("--map-all", action="store_true", help="Map all agents")
    parser.add_argument("--map-agent", help="Map specific agent (e.g., Agent-1)")
    parser.add_argument("--test", help="Test coordinates for specific agent")
    parser.add_argument("--validate", action="store_true", help="Validate all coordinates")
    parser.add_argument("--interactive", action="store_true", help="Run interactive menu")
    
    args = parser.parse_args()
    
    mapper = CoordinateMapper(args.config)
    
    if args.show:
        mapper.show_current_coordinates()
    elif args.map_all:
        mapper.map_all_agents()
    elif args.map_agent:
        mapper.map_single_agent(args.map_agent)
    elif args.test:
        mapper.test_coordinates(args.test)
    elif args.validate:
        mapper.validate_all_coordinates()
    elif args.interactive:
        mapper.interactive_menu()
    else:
        # Default to interactive menu
        mapper.interactive_menu()

if __name__ == "__main__":
    main()



