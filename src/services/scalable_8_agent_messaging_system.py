#!/usr/bin/env python3
import json
import pyautogui
from pathlib import Path
print("Scalable 8-Agent Messaging System - Full Version")
print("=" * 50)
try:
    config_path = "runtime/agent_comms/cursor_agent_coords.json"
    if Path(config_path).exists():
        with open(config_path, "r") as f:
            coords = json.load(f)
        print(f"Coordinates loaded for {len(coords)} layout modes")
        print(f"Available modes: {list(coords.keys())}")
        if "8-agent" in coords:
            agent_count = len(coords["8-agent"])
            print(f"8-agent mode: {agent_count} agents configured")
            for agent_id, agent_coords in coords["8-agent"].items():
                print(f"  {agent_id}: Input box and starter location configured")
        else:
            print("Warning: 8-agent mode not found")
    else:
        print(f"Coordinate file not found: {config_path}")
except Exception as e:
    print(f"Error: {e}")
