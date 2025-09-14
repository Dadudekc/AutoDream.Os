#!/usr/bin/env python3
"""
Swarm Agent Onboarding Script
============================

Direct entry point for the swarm agent onboarding system.
This script provides a clean interface to the --start flag functionality.

Usage:
    python swarm_onboarding.py [--dry-run] [--agent AGENT_ID]

Examples:
    python swarm_onboarding.py --dry-run
    python swarm_onboarding.py --agent Agent-1
    python swarm_onboarding.py
"""

import sys
import argparse
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.services.messaging.consolidated_messaging_service import ConsolidatedMessagingService


def main():
    """Main entry point for swarm onboarding."""
    parser = argparse.ArgumentParser(
        description="Swarm Agent Onboarding System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python swarm_onboarding.py --dry-run          # Test mode - no actual clicking
  python swarm_onboarding.py --agent Agent-1    # Onboard specific agent
  python swarm_onboarding.py                    # Onboard all agents (live mode)
        """
    )

    parser.add_argument("--dry-run", action="store_true",
                       help="Run in dry-run mode (no actual clicking/pasting)")
    parser.add_argument("--agent", "-a", help="Specific agent to onboard (default: all agents)")

    args = parser.parse_args()

    print("🐝 **SWARM ONBOARDING SYSTEM** 🐝")
    print("=" * 50)

    try:
        # Initialize messaging service
        service = ConsolidatedMessagingService(dry_run=args.dry_run)

        # Run onboarding sequence
        result = service.start_agent_onboarding(
            dry_run=args.dry_run,
            specific_agent=args.agent
        )

        if result == 0:
            print("\n🎉 **ONBOARDING SUCCESSFUL!** 🎉")
            print("All agents have been activated and are ready for coordination!")
            print("🐝 **WE ARE SWARM** 🚀🔥")
        else:
            print("\n❌ **ONBOARDING FAILED** ❌")
            print("Some agents could not be onboarded. Check the output above for details.")
            sys.exit(1)

    except Exception as e:
        print(f"\n❌ **CRITICAL ERROR** ❌")
        print(f"Onboarding system failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
