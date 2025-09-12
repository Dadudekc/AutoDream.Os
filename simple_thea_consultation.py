#!/usr/bin/env python3
"""
Simple Thea Consultation - Manual Mode (No Selenium Required)
===========================================================

A simple script to consult Thea manually when automated tools aren't available.
Opens Thea in browser and prepares the consultation message for manual sending.

Usage:
    python simple_thea_consultation.py [--message-file FILE] [--open-browser]

Author: Agent-1 - V2_SWARM Manual Thea Consultation
"""

import argparse
import webbrowser
from datetime import datetime
from pathlib import Path

import pyperclip


def read_message(message_file: Path = None) -> str:
    """Read consultation message from file or use default."""
    if message_file and message_file.exists():
        return message_file.read_text(encoding="utf-8")
    return get_default_message()


def get_default_message() -> str:
    """Get default consultation message."""
    return """# 🌟 THEA CONSULTATION - SWARM PHASE 4 ORCHESTRATION GUIDANCE REQUEST

## 🤖 CURRENT SWARM STATUS ANALYSIS

### 🎯 MISSION STATUS: PHASE 4 ORCHESTRATION LAYER DECOMPOSITION
✅ **Consolidation Sprint Progress**: Strong momentum building with Agent-8 achievements
✅ **Agent-8 Success**: JS-08 (75% reduction) & SVC-08 (80% reduction) completed
✅ **Agent-1 Progress**: JS-01 complete, SVC-01 in progress (90% target)
✅ **V2 Compliance**: All work maintaining strict file size standards (≤400 lines)

### 🚨 CRITICAL SYSTEM ISSUES IDENTIFIED:
❌ **Message Routing Failures**: Agent-8 messages consistently misrouted to Agent-7
❌ **Persistent Pattern**: 6 consecutive Agent-8 routing failures detected
❌ **System Impact**: Critical Phase 4 coordination potentially disrupted

## 🎯 STRATEGIC QUESTIONS FOR THEA:

1. 🎯 **PHASE 4 PRIORITIES**: What should be our immediate next priorities given Agent-8's consolidation success and routing issues?
2. 📊 **CONSOLIDATION STRATEGY**: How should we allocate remaining consolidation work (6 chunks across 6 agents) to maximize momentum?
3. ⚡ **ROUTING CRISIS RESPONSE**: What immediate actions should we take to resolve the Agent-8 routing failures?
4. 🔄 **SYSTEM VERIFICATION**: What protocols should we implement for message delivery verification?
5. 🎖️ **PHASE 4 ACCELERATION**: What specific technical approaches should we use for DebateEngine, MessageRouter, InterventionManager, and LifecycleCoordinator decomposition?

🐝 WE ARE SWARM - SEEKING THEA'S STRATEGIC GUIDANCE FOR PHASE 4 SUCCESS!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""


def main():
    """Main entry point for manual Thea consultation."""
    parser = argparse.ArgumentParser(description="Manual Thea Consultation System")
    parser.add_argument("--message-file", type=Path, help="Path to consultation message file")
    parser.add_argument("--open-browser", action="store_true", help="Automatically open Thea in browser")
    parser.add_argument("--no-clipboard", action="store_true", help="Don't copy message to clipboard")

    args = parser.parse_args()

    print("🐝 V2_SWARM MANUAL THEA CONSULTATION")
    print("=" * 50)
    print()

    # Read the consultation message
    message = read_message(args.message_file)

    if not args.no_clipboard:
        try:
            pyperclip.copy(message)
            print("✅ Message copied to clipboard")
            print("💡 Press Ctrl+V (or Cmd+V on Mac) to paste in Thea")
        except Exception as e:
            print(f"⚠️  Could not copy to clipboard: {e}")
            print("📋 Copy the message manually:")
            print("-" * 40)
            print(message[:200] + "..." if len(message) > 200 else message)
            print("-" * 40)

    # Open Thea in browser
    thea_url = "https://chatgpt.com/g/g-67f437d96d7c81918b2dbc12f0423867-thea-manager?model=gpt-5-thinking"

    if args.open_browser:
        try:
            webbrowser.open(thea_url, new=1)
            print(f"🌐 Browser opened to: {thea_url}")
        except Exception as e:
            print(f"⚠️  Could not open browser automatically: {e}")
            print(f"📖 Please manually navigate to: {thea_url}")

    print()
    print("📝 MANUAL STEPS TO COMPLETE CONSULTATION:")
    print("1. Navigate to the Thea URL (opened above)")
    print("2. Ensure you're logged into ChatGPT")
    print("3. Click on the message input field")
    print("4. Press Ctrl+V (or Cmd+V on Mac) to paste the message")
    print("5. Press Enter to send the message to Thea")
    print("6. Wait for Thea's response")
    print("7. Copy Thea's response for analysis")
    print()

    # Save message to file for reference
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    message_file = Path("devlogs") / f"thea_consultation_message_{timestamp}.md"
    message_file.parent.mkdir(exist_ok=True)
    message_file.write_text(message, encoding="utf-8")
    print(f"💾 Consultation message saved to: {message_file}")
    print()

    print("🎯 CONSULTATION READY!")
    print("🐝 WE ARE SWARM - AWAITING THEA'S STRATEGIC GUIDANCE!")
    print()

    # Wait for user confirmation
    input("🎯 Press Enter AFTER you have sent the message to Thea and received a response...")

    print()
    print("📋 NEXT STEPS:")
    print("1. Copy Thea's response from the browser")
    print("2. Save it to a file for analysis")
    print("3. Create an implementation plan based on Thea's guidance")
    print("4. Update the swarm with Thea's strategic recommendations")
    print()
    print("🐝 WE ARE SWARM - READY TO IMPLEMENT THEA'S GUIDANCE!")


if __name__ == "__main__":
    main()
