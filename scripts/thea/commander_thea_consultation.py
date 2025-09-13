#!/usr/bin/env python3
"""
Commander THEA Consultation CLI - Enhanced AI Consultation Tool
=============================================================

Command-line interface for running enhanced Commander THEA consultations
with advanced analysis and strategic guidance.

Author: Agent-4 (Captain) - V2_SWARM
License: MIT
"""

import argparse
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "src"))
sys.path.insert(0, str(project_root))

from src.services.thea import CommanderTheaManager


def main():
    """Main CLI function for Commander THEA consultations."""

    parser = argparse.ArgumentParser(
        description="Commander THEA Enhanced Consultation System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run full consultation with message
  python scripts/thea/commander_thea_consultation.py --message "Your consultation message here"

  # Run quick analysis without browser
  python scripts/thea/commander_thea_consultation.py --quick --message "Quick analysis request"

  # Run consultation from file
  python scripts/thea/commander_thea_consultation.py --file consultation_request.md
        """
    )

    parser.add_argument(
        "--message", "-m",
        type=str,
        help="Consultation message to send to Commander THEA"
    )

    parser.add_argument(
        "--file", "-f",
        type=str,
        help="Read consultation message from file"
    )

    parser.add_argument(
        "--quick", "-q",
        action="store_true",
        help="Run quick analysis without browser interaction"
    )

    parser.add_argument(
        "--context", "-c",
        type=str,
        help="Additional context for the consultation (JSON format)"
    )

    args = parser.parse_args()

    # Validate arguments
    if not args.message and not args.file:
        print("❌ Error: Must provide either --message or --file")
        parser.print_help()
        sys.exit(1)

    if args.message and args.file:
        print("❌ Error: Cannot specify both --message and --file")
        sys.exit(1)

    # Get the message
    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                message = f.read()
        except FileNotFoundError:
            print(f"❌ Error: File not found: {args.file}")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Error reading file: {e}")
            sys.exit(1)
    else:
        message = args.message

    # Parse context if provided
    context = {}
    if args.context:
        try:
            import json
            context = json.loads(args.context)
        except json.JSONDecodeError:
            print("❌ Error: Invalid JSON in --context")
            sys.exit(1)

    # Initialize Commander THEA Manager
    print("🧠 INITIALIZING COMMANDER THEA SYSTEM...")
    commander = CommanderTheaManager()

    if not commander.initialize():
        print("❌ Failed to initialize Commander THEA system")
        sys.exit(1)

    # Run consultation
    try:
        if args.quick:
            print("⚡ RUNNING QUICK ANALYSIS MODE...")
            result = commander.run_quick_analysis(message, context)
            print("\n" + "="*70)
            print(result)
            print("="*70)
        else:
            print("🚀 RUNNING FULL COMMANDER THEA CONSULTATION...")
            success = commander.run_enhanced_consultation(message, context)

            if success:
                print("\n✅ CONSULTATION COMPLETED SUCCESSFULLY!")
                print("📁 Check thea_responses/ directory for detailed analysis files")
            else:
                print("\n❌ CONSULTATION FAILED")
                sys.exit(1)

    except KeyboardInterrupt:
        print("\n⚠️  Consultation interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Consultation failed with error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
