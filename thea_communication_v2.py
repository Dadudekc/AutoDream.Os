#!/usr/bin/env python3
"""
Thea Communication V2 - Clean, Modular Thea Integration
======================================================

V2 compliant Thea communication system with modular architecture.

Usage:
    python thea_communication_v2.py [--username EMAIL] [--password PASS] [--message "Custom message"]

Author: Agent-4 (Captain) - V2_SWARM
License: MIT
"""

import argparse
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from services.thea import TheaCommunicationManager, TheaConfig


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="V2 Compliant Thea Communication System")
    parser.add_argument("--username", help="ChatGPT username/email for automated login")
    parser.add_argument("--password", help="ChatGPT password for automated login")
    parser.add_argument("--no-selenium", action="store_true", help="Disable Selenium automation")
    parser.add_argument("--headless", action="store_true", help="Run browser in headless mode")
    parser.add_argument("--message", help="Custom message to send to Thea")
    parser.add_argument("--quick", action="store_true", help="Send quick message without full cycle")

    args = parser.parse_args()

    try:
        # Create configuration
        config = TheaConfig.from_args(args)

        print("🐝 V2_SWARM THEA COMMUNICATION V2")
        print("=" * 50)
        print(f"📧 Username: {args.username or 'Not provided'}")
        print(f"🔐 Password: {'Provided' if args.password else 'Not provided'}")
        print(f"🤖 Selenium: {'Disabled' if args.no_selenium else 'Enabled'}")
        print(f"👁️  Headless: {'Yes' if args.headless else 'No'}")
        print(f"⚡ Quick Mode: {'Yes' if args.quick else 'No'}")
        print()

        # Create communication manager
        with TheaCommunicationManager(config) as manager:
            if args.quick:
                # Quick message mode
                message = args.message or "Quick test message from V2_SWARM Thea system"
                success = manager.send_quick_message(message)
                if success:
                    print("\n✅ QUICK MESSAGE SENT!")
                else:
                    print("\n❌ QUICK MESSAGE FAILED!")
            else:
                # Full communication cycle
                success = manager.run_communication_cycle(args.message)

                if success:
                    print("\n🎉 SUCCESS!")
                    print("✅ Thea communication completed successfully!")
                    print("🐝 WE ARE SWARM - AUTOMATED COMMUNICATION ESTABLISHED!")
                else:
                    print("\n❌ FAILURE!")
                    print("❌ Thea communication failed")
                    print("💡 Try running with --no-selenium for manual mode")

    except KeyboardInterrupt:
        print("\n⏹️  Operation cancelled by user")
    except Exception as e:
        print(f"\n💥 ERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
