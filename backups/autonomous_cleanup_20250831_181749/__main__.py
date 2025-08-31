#!/usr/bin/env python3
"""
Services Package Main Entry Point - Agent Cellphone V2
====================================================

Main entry point for the services package.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import sys
import os

# Add the parent directory to the path to enable imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from .unified_messaging_service import main as messaging_main
except ImportError:
    # Fallback if unified_messaging_service is not available
    def messaging_main():
        print("❌ ERROR: Unified messaging service not available")
        sys.exit(1)

def main():
    """Main entry point for services package."""
    if len(sys.argv) > 1:
        # Handle messaging mode
        messaging_main()
    else:
        print("🚨 SERVICES PACKAGE - Agent Cellphone V2")
        print("=" * 50)
        print("Available commands:")
        print("• python -m src.services --mode pyautogui --bulk --message 'Your message'")
        print("• python -m src.services --mode pyautogui --agent Agent-4 --message 'Your message'")
        print("• python -m src.services --onboarding --onboarding-style friendly")
        print("• python -m src.services --onboard --onboarding-style strict")
        print("• python -m src.services --list-agents")
        print("• python -m src.services --coordinates")
        print("• python -m src.services --history")
        print()

if __name__ == "__main__":
    main()
