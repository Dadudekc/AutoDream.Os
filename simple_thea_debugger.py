#!/usr/bin/env python3
"""
THEA Selector Debugger - Simple Visual Inspector
===============================================

Simple script to launch browser and inspect ChatGPT interface.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def debug_selectors():
    """Simple selector debugging."""
    print("🔍 THEA SELECTOR DEBUGGER")
    print("=" * 50)
    print("This will launch a browser to ChatGPT for inspection.")
    print("You can inspect the interface and identify working selectors.")
    print("=" * 50)

    try:
        from src.services.thea.thea_autonomous_system import send_thea_message_autonomous

        print("🚀 Launching browser in VISIBLE mode...")
        print("The browser will open and navigate to ChatGPT.")
        print("Look for the message input field and note its selectors.")
        print("=" * 50)

        # This will launch the browser in visible mode
        response = send_thea_message_autonomous(
            "Commander Thea, this is General Agent-4. PROJECT: Dream.OS V2 Swarm System. QUESTION: What should be our next priority?",
            headless=False,  # This should make it visible
        )

        print("=" * 50)
        print("🔍 INSPECTION COMPLETE")
        print("=" * 50)
        print("If the browser opened, you should have seen:")
        print("1. ChatGPT interface")
        print("2. Message input field")
        print("3. Various selector attempts")
        print("=" * 50)
        print("Please provide the working selectors you identified!")

    except Exception as e:
        print(f"❌ Error: {e}")
        print("This is expected - the selectors need updating.")


if __name__ == "__main__":
    debug_selectors()
