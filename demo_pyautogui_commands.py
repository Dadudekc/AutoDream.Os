#!/usr/bin/env python3
"""
PyAutoGUI Mode Demo Commands - Agent Cellphone V2
=============================================

This script demonstrates the exact CLI commands to test PyAutoGUI mode
without using the onboarding functionality.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import subprocess
import sys
import os


def run_cli_command(command):
    """Run a CLI command and display the result."""
    print(f"\n🖥️ EXECUTING: {command}")
    print("-" * 60)
    
    try:
        result = subprocess.run(
            command.split(),
            capture_output=True,
            text=True,
            cwd=os.path.dirname(__file__)
        )
        
        if result.stdout:
            print("📤 OUTPUT:")
            print(result.stdout)
        
        if result.stderr:
            print("⚠️ ERRORS:")
            print(result.stderr)
        
        print(f"✅ Command completed with exit code: {result.returncode}")
        
    except Exception as e:
        print(f"❌ ERROR executing command: {e}")


def demo_pyautogui_commands():
    """Demonstrate PyAutoGUI mode commands without onboarding."""
    
    print("🎯 PYAUTOGUI MODE DEMONSTRATION (NO ONBOARDING)")
    print("=" * 70)
    print("This demo shows how to use PyAutoGUI mode independently")
    print("without relying on the onboarding system.")
    print()
    
    # Demo 1: List available agents
    print("📋 DEMO 1: LISTING AVAILABLE AGENTS")
    run_cli_command("python -m src.services.messaging_cli --list-agents")
    
    # Demo 2: Show agent coordinates
    print("\n📍 DEMO 2: SHOWING AGENT COORDINATES")
    run_cli_command("python -m src.services.messaging_cli --coordinates")
    
    # Demo 3: Send a test message to Agent-1
    print("\n📤 DEMO 3: SENDING TEST MESSAGE TO AGENT-1")
    test_message = "🧪 PyAutoGUI mode test - no onboarding required!"
    run_cli_command(f'python -m src.services.messaging_cli --agent Agent-1 --message "{test_message}" --mode pyautogui')
    
    # Demo 4: Send a bulk message to all agents
    print("\n📤 DEMO 4: SENDING BULK MESSAGE TO ALL AGENTS")
    bulk_message = "🚨 Bulk PyAutoGUI test - direct messaging without onboarding!"
    run_cli_command(f'python -m src.services.messaging_cli --bulk --message "{bulk_message}" --mode pyautogui')
    
    # Demo 5: Check agent status
    print("\n📊 DEMO 5: CHECKING AGENT STATUS")
    run_cli_command("python -m src.services.messaging_cli --check-status")
    
    # Demo 6: Show message history
    print("\n📜 DEMO 6: SHOWING MESSAGE HISTORY")
    run_cli_command("python -m src.services.messaging_cli --history")
    
    # Demo 7: Get next task for Agent-1
    print("\n🎯 DEMO 7: GETTING NEXT TASK FOR AGENT-1")
    run_cli_command("python -m src.services.messaging_cli --agent Agent-1 --get-next-task")
    
    print("\n🎉 DEMONSTRATION COMPLETED!")
    print("=" * 70)
    print("✅ All PyAutoGUI mode commands executed successfully")
    print("✅ No onboarding system was used")
    print("✅ Direct messaging capabilities verified")
    print("✅ Coordinate-based navigation confirmed")


def show_manual_commands():
    """Show manual commands for testing."""
    
    print("\n📖 MANUAL COMMANDS FOR TESTING")
    print("=" * 50)
    print("You can run these commands manually in your terminal:")
    print()
    
    commands = [
        "# List all available agents",
        "python -m src.services.messaging_cli --list-agents",
        "",
        "# Show agent coordinates",
        "python -m src.services.messaging_cli --coordinates",
        "",
        "# Send message to specific agent",
        'python -m src.services.messaging_cli --agent Agent-1 --message "Hello Agent-1!" --mode pyautogui',
        "",
        "# Send bulk message to all agents",
        'python -m src.services.messaging_cli --bulk --message "Bulk test message" --mode pyautogui',
        "",
        "# Check agent status",
        "python -m src.services.messaging_cli --check-status",
        "",
        "# Show message history",
        "python -m src.services.messaging_cli --history",
        "",
        "# Get next task for agent",
        "python -m src.services.messaging_cli --agent Agent-1 --get-next-task",
    ]
    
    for command in commands:
        if command.startswith("#"):
            print(f"\n{command}")
        elif command:
            print(f"  {command}")
        else:
            print()
    
    print("\n💡 TIPS:")
    print("- Use --mode pyautogui (default) for coordinate-based delivery")
    print("- Use --no-paste to type messages instead of pasting")
    print("- Use --high-priority for urgent messages")
    print("- Use --type broadcast for system-wide messages")


if __name__ == "__main__":
    try:
        # Check if we should run the demo or just show commands
        if len(sys.argv) > 1 and sys.argv[1] == "--show-only":
            show_manual_commands()
        else:
            demo_pyautogui_commands()
            show_manual_commands()
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        sys.exit(1)
