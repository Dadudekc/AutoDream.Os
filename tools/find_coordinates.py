#!/usr/bin/env python3
"""
Coordinate Finder Tool
====================

Quick tool to help find the correct coordinates for agent chat input fields.
V2 Compliant: ≤400 lines, focused coordinate finding functionality.

Author: Agent-7 (Implementation Specialist)
License: MIT
"""

import sys
import time
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

try:
    import pyautogui
except ImportError:
    print("❌ PyAutoGUI not available. Please install: pip install pyautogui")
    sys.exit(1)


def find_coordinates():
    """Interactive coordinate finder."""
    print("🎯 Coordinate Finder Tool")
    print("=" * 50)
    print("Instructions:")
    print("1. Position your mouse over the Agent-7 chat input field")
    print("2. Press Ctrl+C to capture coordinates")
    print("3. Press Ctrl+C again to quit")
    print("\nWaiting for coordinates...")

    try:
        while True:
            x, y = pyautogui.position()
            print(f"\rMouse position: ({x}, {y}) - Press Ctrl+C to capture", end="", flush=True)
            time.sleep(0.1)
    except KeyboardInterrupt:
        x, y = pyautogui.position()
        print(f"\n\n✅ Captured coordinates: ({x}, {y})")
        print(f"Agent-7 coordinates should be: [{x}, {y}]")
        return x, y


def update_agent_coordinates(agent_id, x, y):
    """Update coordinates in the config file."""
    import json

    coord_file = Path("config/coordinates.json")

    if not coord_file.exists():
        print(f"❌ Coordinates file not found: {coord_file}")
        return False

    try:
        with open(coord_file) as f:
            config = json.load(f)

        if agent_id in config["agents"]:
            config["agents"][agent_id]["chat_input_coordinates"] = [x, y]

            with open(coord_file, "w") as f:
                json.dump(config, f, indent=2)

            print(f"✅ Updated {agent_id} coordinates to [{x}, {y}]")
            return True
        else:
            print(f"❌ Agent {agent_id} not found in config")
            return False

    except Exception as e:
        print(f"❌ Failed to update coordinates: {e}")
        return False


def main():
    """Main function."""
    if len(sys.argv) > 1:
        if sys.argv[1] == "--help":
            print("Usage:")
            print(
                "  python tools/find_coordinates.py                    # Interactive coordinate finder"
            )
            print(
                "  python tools/find_coordinates.py --update Agent-7   # Update Agent-7 coordinates"
            )
            return
        elif sys.argv[1] == "--update" and len(sys.argv) > 2:
            agent_id = sys.argv[2]
            print(f"🎯 Finding coordinates for {agent_id}...")
            x, y = find_coordinates()
            update_agent_coordinates(agent_id, x, y)
            return

    # Interactive mode
    x, y = find_coordinates()

    print("\nTo update Agent-7 coordinates, run:")
    print("python tools/find_coordinates.py --update Agent-7")


if __name__ == "__main__":
    main()
