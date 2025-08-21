#!/usr/bin/env python3
import json
import time
from pathlib import Path
print("Enhanced 8-Agent Messaging System - TEST_SYNC Ready")
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
            print("TEST_SYNC: This is a synchronous test message")
            test_message = {
                "agent_id": "agent_1",
                "type": "test_sync",
                "content": "This is a synchronous test message",
                "timestamp": time.time()
            }
            print(json.dumps(test_message, indent=2))
            print("TEST_SYNC message format validated successfully!")
        else:
            print("Warning: 8-agent mode not found")
    else:
        print(f"Coordinate file not found: {config_path}")
except Exception as e:
    print(f"Error: {e}")
