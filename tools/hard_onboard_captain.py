#!/usr/bin/env python3
"""
Hard onboard Captain (Agent-4) with complete session context.
Quick tool for Captain self-reset.
"""

import sys
from pathlib import Path

# Ensure src is in path
repo_root = Path(__file__).parent.parent
sys.path.insert(0, str(repo_root))

from src.services.hard_onboarding_service import hard_onboard_agent


def main():
    """Execute Captain hard onboarding."""

    # Load onboarding message
    onboarding_file = repo_root / "agent_workspaces" / "Agent-4" / "HARD_ONBOARDING_MESSAGE.md"

    if not onboarding_file.exists():
        print(f"❌ Onboarding file not found: {onboarding_file}")
        return 1

    onboarding_message = onboarding_file.read_text(encoding="utf-8")
    print(f"📄 Loaded onboarding message ({len(onboarding_message)} chars)")

    # Execute hard onboarding
    print("🚨 Starting HARD ONBOARDING for Agent-4 (Captain)...")
    print("  Protocol: Clear chat → Execute → New window → Navigate → Send message")

    success = hard_onboard_agent(
        agent_id="Agent-4",
        onboarding_message=onboarding_message,
        role="Captain & Strategic Oversight",
    )

    if success:
        print("✅ Captain hard onboarding COMPLETE!")
        return 0
    else:
        print("❌ Captain hard onboarding FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
