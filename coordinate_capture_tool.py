#!/usr/bin/env python3
"""
Interactive Coordinate Capture Tool
====================================

Captures agent coordinates interactively using PyAutoGUI.
User moves cursor to desired location and presses Enter to capture coordinates.

Author: Agent-5 (Business Intelligence Specialist & Co-Captain)
Mission: Implement missing coordinate setter functionality
"""

import json
import time
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Any
import logging

logger = logging.getLogger(__name__)

# Try to import PyAutoGUI
try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False
    print("❌ PyAutoGUI not available. Install with: pip install pyautogui")
    sys.exit(1)

# Configuration
COORD_FILE = Path("cursor_agent_coords.json")
AGENTS = ["Agent-1", "Agent-2", "Agent-3", "Agent-4",
          "Agent-5", "Agent-6", "Agent-7", "Agent-8"]

# Agent descriptions for user guidance
AGENT_DESCRIPTIONS = {
    "Agent-1": "Integration & Core Systems Specialist",
    "Agent-2": "Architecture & Design Specialist",
    "Agent-3": "Infrastructure & DevOps Specialist",
    "Agent-4": "Quality Assurance Specialist (CAPTAIN)",
    "Agent-5": "Business Intelligence Specialist",
    "Agent-6": "Coordination & Communication Specialist",
    "Agent-7": "Web Development Specialist",
    "Agent-8": "Operations & Support Specialist"
}


class CoordinateCaptureTool:
    """Interactive coordinate capture tool using PyAutoGUI."""

    def __init__(self):
        """Initialize the coordinate capture tool."""
        self.captured_coords = {}
        self.load_existing_coordinates()

    def load_existing_coordinates(self):
        """Load existing coordinates from JSON file."""
        try:
            if COORD_FILE.exists():
                with open(COORD_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.captured_coords = data
                print("✅ Loaded existing coordinates from cursor_agent_coords.json")
            else:
                print("⚠️  No existing coordinate file found. Creating new one.")
                self.captured_coords = {
                    "description": "Agent coordinate configuration - Single Source of Truth for all agent coordinates",
                    "version": "2.1.0",
                    "last_updated": "",
                    "coordinate_system": {
                        "origin": "top-left",
                        "unit": "pixels",
                        "multi_monitor_support": True
                    },
                    "agents": {}
                }
        except Exception as e:
            print(f"❌ Error loading coordinates: {e}")
            sys.exit(1)

    def capture_coordinate(self, agent_id: str, coord_type: str) -> Tuple[int, int]:
        """Capture a single coordinate interactively."""
        description = AGENT_DESCRIPTIONS.get(agent_id, agent_id)

        print(f"\n🎯 {coord_type.upper()} COORDINATES - {agent_id}")
        print(f"   Description: {description}")
        print(f"   Move your cursor to the {coord_type.lower()} input field for {agent_id}")
        print("   Press ENTER when cursor is in position..."
        print("   (Or type 'skip' to skip this coordinate)"
        print("   (Or type 'quit' to exit)")

        while True:
            user_input = input("\nReady? (press Enter to capture, 'skip' to skip, 'quit' to exit): ").strip().lower()

            if user_input == 'quit':
                print("Exiting coordinate capture...")
                sys.exit(0)
            elif user_input == 'skip':
                print(f"⏭️  Skipped {coord_type} coordinates for {agent_id}")
                return None

            try:
                # Get current mouse position
                x, y = pyautogui.position()
                print(f"📍 Captured coordinates: ({x}, {y})")

                # Confirm with user
                confirm = input(f"Confirm coordinates ({x}, {y})? (y/n): ").strip().lower()
                if confirm in ['y', 'yes']:
                    return (x, y)
                else:
                    print("❌ Coordinate rejected. Try again.")

            except Exception as e:
                print(f"❌ Error capturing coordinates: {e}")
                return None

    def capture_all_onboarding_coords(self):
        """Capture onboarding coordinates for all agents."""
        print("\n" + "="*80)
        print("🎯 PHASE 1: CAPTURING ONBOARDING INPUT COORDINATES")
        print("="*80)
        print("Onboarding coordinates are used when agents first join the swarm.")
        print("Position cursor in the onboarding input field for each agent.\n")

        for agent_id in AGENTS:
            print(f"\n🔄 Processing {agent_id}...")

            # Check if agent already exists in coordinates
            if agent_id not in self.captured_coords.get("agents", {}):
                self.captured_coords.setdefault("agents", {})[agent_id] = {}

            coords = self.capture_coordinate(agent_id, "onboarding")

            if coords:
                self.captured_coords["agents"][agent_id]["onboarding_input_coords"] = list(coords)
                self.captured_coords["agents"][agent_id]["description"] = AGENT_DESCRIPTIONS.get(agent_id, "")
                self.captured_coords["agents"][agent_id]["active"] = True
                print(f"✅ Saved onboarding coordinates for {agent_id}: {coords}")

    def capture_all_chat_coords(self):
        """Capture chat coordinates for all agents."""
        print("\n" + "="*80)
        print("🎯 PHASE 2: CAPTURING CHAT INPUT COORDINATES")
        print("="*80)
        print("Chat coordinates are used for regular messaging between agents.")
        print("Position cursor in the chat input field for each agent.\n")

        for agent_id in AGENTS:
            print(f"\n🔄 Processing {agent_id}...")

            coords = self.capture_coordinate(agent_id, "chat")

            if coords:
                self.captured_coords["agents"][agent_id]["chat_input_coordinates"] = list(coords)
                print(f"✅ Saved chat coordinates for {agent_id}: {coords}")

    def save_coordinates(self):
        """Save captured coordinates to JSON file."""
        try:
            # Update timestamp
            from datetime import datetime
            self.captured_coords["last_updated"] = datetime.now().isoformat()

            # Save to file
            with open(COORD_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.captured_coords, f, indent=2)

            print("
✅ Coordinates saved successfully!"            print(f"📁 File: {COORD_FILE}")
            print(f"📅 Updated: {self.captured_coords['last_updated']}")

            # Show summary
            agents_count = len(self.captured_coords.get("agents", {}))
            print(f"🤖 Total agents configured: {agents_count}")

        except Exception as e:
            print(f"❌ Error saving coordinates: {e}")
            return False

        return True

    def show_current_coordinates(self):
        """Display current coordinates for all agents."""
        print("\n" + "="*80)
        print("📊 CURRENT COORDINATES SUMMARY")
        print("="*80)

        agents = self.captured_coords.get("agents", {})

        if not agents:
            print("❌ No coordinates configured yet.")
            return

        print("<8")
        print("-" * 82)

        for agent_id in AGENTS:
            if agent_id in agents:
                agent_data = agents[agent_id]
                onboarding = agent_data.get("onboarding_input_coords", ["-", "-"])
                chat = agent_data.get("chat_input_coordinates", ["-", "-"])
                description = agent_data.get("description", "")

                print("<8")
            else:
                print("<8")

        print("="*80)

    def run_full_capture(self):
        """Run the complete coordinate capture process."""
        print("🚀 COORDINATE CAPTURE TOOL")
        print("="*50)
        print("This tool will help you capture coordinates for all agents.")
        print("Make sure all agent windows are open and positioned correctly.\n")

        # Show current state
        self.show_current_coordinates()

        # Confirm start
        start = input("\nReady to start coordinate capture? (y/n): ").strip().lower()
        if start not in ['y', 'yes']:
            print("Coordinate capture cancelled.")
            return

        # Phase 1: Onboarding coordinates
        self.capture_all_onboarding_coords()

        # Phase 2: Chat coordinates
        self.capture_all_chat_coords()

        # Save and show final results
        if self.save_coordinates():
            self.show_current_coordinates()
            print("\n🎉 Coordinate capture complete!")
            print("✅ All coordinates saved to cursor_agent_coords.json")
            print("✅ Ready for PyAutoGUI messaging system")

    def run_single_agent_capture(self, agent_id: str):
        """Capture coordinates for a single agent."""
        print(f"🎯 Single Agent Coordinate Capture: {agent_id}")
        print("="*50)

        if agent_id not in AGENTS:
            print(f"❌ Invalid agent ID: {agent_id}")
            print(f"Valid agents: {', '.join(AGENTS)}")
            return

        # Check if agent exists
        if agent_id not in self.captured_coords.get("agents", {}):
            self.captured_coords.setdefault("agents", {})[agent_id] = {}

        # Capture onboarding coordinates
        print(f"\n🔄 Capturing onboarding coordinates for {agent_id}...")
        onboarding_coords = self.capture_coordinate(agent_id, "onboarding")
        if onboarding_coords:
            self.captured_coords["agents"][agent_id]["onboarding_input_coords"] = list(onboarding_coords)
            self.captured_coords["agents"][agent_id]["description"] = AGENT_DESCRIPTIONS.get(agent_id, "")
            self.captured_coords["agents"][agent_id]["active"] = True

        # Capture chat coordinates
        print(f"\n🔄 Capturing chat coordinates for {agent_id}...")
        chat_coords = self.capture_coordinate(agent_id, "chat")
        if chat_coords:
            self.captured_coords["agents"][agent_id]["chat_input_coordinates"] = list(chat_coords)

        # Save
        if self.save_coordinates():
            print(f"\n✅ Coordinates updated for {agent_id}")


def main():
    """Main entry point for coordinate capture tool."""
    if len(sys.argv) > 1:
        agent_id = sys.argv[1]
        tool = CoordinateCaptureTool()
        tool.run_single_agent_capture(agent_id)
    else:
        tool = CoordinateCaptureTool()
        tool.run_full_capture()


if __name__ == "__main__":
    main()
