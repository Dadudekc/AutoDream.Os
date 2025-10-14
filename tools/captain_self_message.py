"""
Captain's Tool: Self-Message Reminder
======================================

Sends a message to Agent-4 (Captain) as a reminder.
CRITICAL: Captain is an agent too and needs prompts!

Usage: python tools/captain_self_message.py --message "Start your task!" --priority regular

Author: Agent-4 (Captain)
Date: 2025-10-13
"""

import subprocess
import sys


def send_self_message(message: str, priority: str = "regular"):
    """
    Send message to Captain (Agent-4).

    CRITICAL REMINDER: Captain is Agent-4 and needs prompts to run!
    "Prompts are gas - even for Captain!"
    """

    print("\n⛽ CAPTAIN SELF-MESSAGE")
    print("=" * 60)
    print("Reminder: Captain IS Agent-4 - needs prompts too!")
    print(f"Message: {message}")
    print(f"Priority: {priority}")
    print("=" * 60 + "\n")

    cmd = [
        "python",
        "src/services/messaging_cli.py",
        "--agent",
        "Agent-4",
        "--message",
        f"[SELF-REMINDER] {message}",
        "--priority",
        priority,
        "--pyautogui",
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

        if result.returncode == 0:
            print("✅ Self-message sent successfully!")
            print("⛽ Captain activated by own prompt!\n")
            return True
        else:
            print("❌ Failed to send self-message")
            print(f"Error: {result.stderr}")
            return False

    except Exception as e:
        print(f"❌ Error sending self-message: {e}")
        return False


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Send self-message to Captain (Agent-4)",
        epilog="Remember: Captain is Agent-4 and needs prompts too! ⛽",
    )
    parser.add_argument("--message", "-m", required=True, help="Self-reminder message")
    parser.add_argument(
        "--priority", "-p", default="regular", choices=["regular", "urgent"], help="Priority"
    )

    args = parser.parse_args()

    success = send_self_message(args.message, args.priority)

    sys.exit(0 if success else 1)
