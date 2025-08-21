#!/usr/bin/env python3
"""
Working PyAutoGUI Agent Message Sender - Agent Cellphone V2
=========================================================

Actually sends messages to agent input coordinates using PyAutoGUI.
"""

import sys
import json
import time
from pathlib import Path

try:
    import pyautogui
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.1
except ImportError:
    print("ERROR: PyAutoGUI not installed. Install with: pip install pyautogui")
    sys.exit(1)

def load_agent_coordinates():
    """Load agent coordinates from the cursor coordinates file."""
    coords_file = Path("../runtime/agent_comms/cursor_agent_coords.json")
    
    if not coords_file.exists():
        print(f"ERROR: Coordinates file not found: {coords_file}")
        return None
    
    try:
        with open(coords_file, 'r') as f:
            coords = json.load(f)
        return coords
    except Exception as e:
        print(f"ERROR: Error loading coordinates: {e}")
        return None

def send_message_to_agent(agent_id, message, high_priority=False):
    """Send a message to a specific agent using PyAutoGUI."""
    
    # Load coordinates
    coords = load_agent_coordinates()
    if not coords:
        return False
    
    # Use 5-agent mode coordinates
    if "5-agent" not in coords:
        print("ERROR: 5-agent mode coordinates not found")
        return False
    
    if agent_id not in coords["5-agent"]:
        print(f"ERROR: Agent {agent_id} not found in 5-agent mode")
        return False
    
    # Get agent input box coordinates
    input_coords = coords["5-agent"][agent_id]["input_box"]
    x, y = input_coords["x"], input_coords["y"]
    
    print(f"Sending message to {agent_id} at coordinates ({x}, {y})")
    print(f"Priority: {'HIGH' if high_priority else 'NORMAL'}")
    print(f"Message: {message[:100]}...")
    
    try:
        # Move to agent input box and click
        print(f"Moving to {agent_id} input box...")
        pyautogui.moveTo(x, y, duration=0.5)
        time.sleep(0.2)
        pyautogui.click(x, y)
        time.sleep(0.3)
        
        # Clear any existing text
        print("Clearing existing text...")
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.2)
        pyautogui.press('delete')
        time.sleep(0.2)
        
        # Type the message with proper line break handling
        print("Typing message with line breaks...")
        lines = message.split('\n')
        for idx, line in enumerate(lines):
            if line:
                # Type the line content
                pyautogui.typewrite(line, interval=0.01)
                time.sleep(0.05)  # Small delay between characters for stability
            
            # For multi-line messages, use proper line breaks that don't send
            if idx < len(lines) - 1:
                # Use Shift+Enter for line breaks (prevents premature sending)
                pyautogui.hotkey('shift', 'enter')
                time.sleep(0.1)  # Delay for UI stability
        
        # Final delay to ensure all input is properly buffered
        time.sleep(0.2)
        
        # Send message based on priority
        if high_priority:
            print("Sending HIGH PRIORITY message (Alt+Enter)...")
            pyautogui.hotkey('alt', 'enter')
        else:
            print("Sending normal message (Enter)...")
            pyautogui.press('enter')
        
        time.sleep(0.5)
        
        print(f"SUCCESS: Message successfully sent to {agent_id}")
        return True
        
    except Exception as e:
        print(f"ERROR: Error sending message to {agent_id}: {e}")
        return False

def main():
    """Main function to send messages."""
    if len(sys.argv) < 3:
        print("Usage: python send_agent_message_pyautogui.py <agent_id> <message> [--high-priority]")
        print("Example: python send_agent_message_pyautogui.py Agent-4 'Hello from Captain-5!' --high-priority")
        print("\nAvailable agents: Agent-1, Agent-2, Agent-3, Agent-4")
        return
    
    agent_id = sys.argv[1]
    message = sys.argv[2]
    high_priority = "--high-priority" in sys.argv
    
    # Validate agent ID
    valid_agents = ["Agent-1", "Agent-2", "Agent-3", "Agent-4"]
    if agent_id not in valid_agents:
        print(f"ERROR: Invalid agent ID: {agent_id}")
        print(f"Valid agents: {', '.join(valid_agents)}")
        return
    
    print("=" * 60)
    print(f"AGENT CELLPHONE MESSAGING SYSTEM - PyAutoGUI")
    print(f"Target: {agent_id}")
    print(f"Priority: {'HIGH' if high_priority else 'NORMAL'}")
    print("=" * 60)
    
    success = send_message_to_agent(agent_id, message, high_priority)
    
    if success:
        print(f"SUCCESS: Message successfully delivered to {agent_id}")
        print(f"INFO: Message sent to agent input coordinates")
    else:
        print(f"ERROR: Failed to send message to {agent_id}")

if __name__ == "__main__":
    main()
