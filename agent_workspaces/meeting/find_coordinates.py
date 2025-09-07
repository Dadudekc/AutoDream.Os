#!/usr/bin/env python3
"""
🧭 COORDINATE FINDER UTILITY 🧭

Purpose: Help find the correct input coordinates for each agent's messaging interface
Usage: Run this script and move your mouse to the input fields to get coordinates
"""

import pyautogui
import json
import time
from pathlib import Path

def find_coordinates():
    """Interactive coordinate finder for agent input fields"""
    print("🧭 COORDINATE FINDER UTILITY")
    print("=" * 50)
    print("Instructions:")
    print("1. Move your mouse to each agent's input field")
    print("2. Press Ctrl+C to capture coordinates")
    print("3. Repeat for all agents")
    print("4. Coordinates will be saved to input_coordinates_config.json")
    print("=" * 50)
    
    # Agent list
    agents = [
        "Agent-1", "Agent-2", "Agent-3", "Agent-4",
        "Agent-5", "Agent-6", "Agent-7", "Agent-8"
    ]
    
    coordinates = {}
    
    for agent in agents:
        print(f"\n🎯 Move mouse to {agent}'s input field...")
        print("Press Ctrl+C when ready...")
        
        try:
            # Wait for user to position mouse
            input(f"Position mouse at {agent}'s input field and press Enter...")
            
            # Get current mouse position
            x, y = pyautogui.position()
            coordinates[agent] = {
                "x": x,
                "y": y,
                "description": f"{agent} input field coordinates"
            }
            
            print(f"✅ {agent}: ({x}, {y})")
            
        except KeyboardInterrupt:
            print(f"⏹️ Skipping {agent}")
            continue
    
    # Save coordinates to config file
    config = {
        "agent_input_coordinates": coordinates,
        "messaging_settings": {
            "click_delay": 0.5,
            "typing_delay": 0.5,
            "send_delay": 0.5,
            "send_key": "enter",
            "clear_input_before_typing": True
        },
        "notes": "Coordinates captured using coordinate finder utility"
    }
    
    config_file = Path("input_coordinates_config.json")
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Coordinates saved to {config_file}")
    print("You can now run the auto-resume system with these coordinates!")

def show_current_coordinates():
    """Show currently configured coordinates"""
    config_file = Path("input_coordinates_config.json")
    if config_file.exists():
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        print("📍 CURRENT COORDINATES:")
        print("=" * 50)
        for agent, coords in config.get("agent_input_coordinates", {}).items():
            print(f"{agent}: ({coords['x']}, {coords['y']}) - {coords['description']}")
    else:
        print("❌ No coordinate configuration found")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--show":
            show_current_coordinates()
        elif sys.argv[1] == "--help":
            print("""
🧭 COORDINATE FINDER UTILITY 🧭

Usage:
  python find_coordinates.py              # Interactive coordinate finder
  python find_coordinates.py --show      # Show current coordinates
  python find_coordinates.py --help      # Show this help

The coordinate finder will help you set up the correct input coordinates
for each agent's messaging interface in the auto-resume system.
            """)
        else:
            print(f"❌ Unknown option: {sys.argv[1]}")
            print("Use --help for usage information")
    else:
        find_coordinates()
