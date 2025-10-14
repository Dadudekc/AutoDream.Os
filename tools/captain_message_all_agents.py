"""
Captain's Tool: Message All Agents
===================================

Sends messages to all 8 agents (including self!) with one command.
Prevents forgetting to message Captain (Agent-4).

Usage: python tools/captain_message_all_agents.py --message "Check INBOX!" --priority regular

Author: Agent-4 (Captain)
Date: 2025-10-13
"""

import subprocess
import sys

SWARM_AGENTS = [
    "Agent-1",
    "Agent-2",
    "Agent-3",
    "Agent-4",
    "Agent-5",
    "Agent-6",
    "Agent-7",
    "Agent-8",
]


def message_all_agents(message: str, priority: str = "regular", include_captain: bool = True):
    """Send message to all agents including Captain."""

    agents_to_message = (
        SWARM_AGENTS if include_captain else [a for a in SWARM_AGENTS if a != "Agent-4"]
    )

    print(f"\n🚀 Messaging {len(agents_to_message)} agents...")
    print(f"Priority: {priority}")
    print(f"Message: {message[:80]}...\n")

    results = {}
    for agent in agents_to_message:
        cmd = [
            "python",
            "src/services/messaging_cli.py",
            "--agent",
            agent,
            "--message",
            message,
            "--priority",
            priority,
            "--pyautogui",
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            success = result.returncode == 0
            results[agent] = success

            status = "✅" if success else "❌"
            print(f"{status} {agent}: {'Sent' if success else 'Failed'}")

        except Exception as e:
            results[agent] = False
            print(f"❌ {agent}: Error - {e}")

    successful = sum(1 for v in results.values() if v)
    print(f"\n✅ Messages sent: {successful}/{len(agents_to_message)}")

    return results


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Message all swarm agents")
    parser.add_argument("--message", "-m", required=True, help="Message content")
    parser.add_argument(
        "--priority",
        "-p",
        default="regular",
        choices=["regular", "urgent"],
        help="Message priority",
    )
    parser.add_argument(
        "--skip-captain", action="store_true", help="Skip messaging Agent-4 (Captain)"
    )

    args = parser.parse_args()

    results = message_all_agents(args.message, args.priority, not args.skip_captain)

    sys.exit(0 if all(results.values()) else 1)
