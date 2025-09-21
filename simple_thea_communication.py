#!/usr/bin/env python3
"""
Simple Thea Communication V2 - Send & Receive
==============================================

V2 compliant version of Thea communication system.
Modular architecture with clean separation of concerns.

Usage:
# SECURITY: Password placeholder - replace with environment variable
"""

import argparse
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from thea_communication import TheaCommunicationService


def main():
    """Main function for Thea communication."""
    parser = argparse.ArgumentParser(description="Simple Thea Communication V2")
    parser.add_argument("--username", help="OpenAI username/email")
# SECURITY: Password placeholder - replace with environment variable
    parser.add_argument("--selenium", action="store_true", default=True, help="Use Selenium automation")
    parser.add_argument("--manual", action="store_true", help="Use manual automation")
    parser.add_argument("--headless", action="store_true", help="Run in headless mode")
    parser.add_argument("--message", help="Custom message to send")
    
    args = parser.parse_args()
    
    # Determine automation method
    use_selenium = args.selenium and not args.manual
    
    print("🚀 V2_SWARM Thea Communication System V2")
    print("=" * 50)
    
    try:
        # Initialize communication service
        service = TheaCommunicationService(
            username=args.username,
# SECURITY: Password placeholder - replace with environment variable
            use_selenium=use_selenium,
            headless=args.headless
        )
        
        # Initialize driver if using Selenium
        if use_selenium:
            if not service.initialize_driver():
                print("❌ Failed to initialize Selenium driver")
                return 1
        
        # Ensure authentication
        if not service.ensure_authenticated():
            print("❌ Authentication failed")
            return 1
        
        # Run communication cycle
        success = service.run_communication_cycle(args.message)
        
        if success:
            print("✅ Communication cycle completed successfully!")
            return 0
        else:
            print("❌ Communication cycle failed")
            return 1
            
# SECURITY: Key placeholder - replace with environment variable
        print("\n⚠️  Operation cancelled by user")
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return 1
    finally:
        # Cleanup
        try:
            service.cleanup()
        except:
            pass


if __name__ == "__main__":
    sys.exit(main())
