#!/usr/bin/env python3
"""
Thea Autonomous CLI - Command Line Interface for Agent-Friendly Thea
====================================================================

A simple command-line interface for the autonomous Thea system.
Allows agents to interact with Thea without human intervention.

Usage:
    python -m src.services.thea.thea_autonomous_cli send "Hello Thea!"
    python -m src.services.thea.thea_autonomous_cli status
    python -m src.services.thea.thea_autonomous_cli test
"""

import argparse
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.services.thea.thea_autonomous_system import TheaAutonomousSystem, send_thea_message_autonomous


def send_message_command(message: str, headless: bool = True):
    """Send a message to Thea autonomously."""
    print(f"🤖 Sending autonomous message to Thea...")
    print(f"📤 Message: {message}")
    print(f"🫥 Headless mode: {headless}")
    print("-" * 50)
    
    response = send_thea_message_autonomous(message, headless=headless)
    
    if response:
        print(f"✅ SUCCESS: Received response from Thea")
        print(f"📝 Response length: {len(response)} characters")
        print(f"📄 Response preview: {response[:300]}...")
        return True
    else:
        print("❌ FAILED: No response received from Thea")
        return False


def status_command():
    """Get system status."""
    print("📊 Thea Autonomous System Status")
    print("=" * 40)
    
    try:
        thea = TheaAutonomousSystem(headless=True)
        status = thea.get_system_status()
        
        print(f"🔧 Initialized: {status['initialized']}")
        print(f"🫥 Headless mode: {status['headless_mode']}")
        print(f"🍪 Valid cookies: {status['has_valid_cookies']}")
        print(f"🌐 Browser available: {status['browser_available']}")
        print(f"⏰ Last activity: {status['last_activity']}")
        print(f"🔄 Max retries: {status['max_retries']}")
        print(f"⏳ Retry delay: {status['retry_delay']}s")
        
        return True
        
    except Exception as e:
        print(f"❌ Error getting status: {e}")
        return False


def test_command():
    """Run a test message to verify system functionality."""
    test_message = "Hello Thea! This is an autonomous test from Agent-2. Please respond with a brief acknowledgment."
    
    print("🧪 Running Thea Autonomous System Test")
    print("=" * 45)
    
    return send_message_command(test_message, headless=True)


def interactive_command():
    """Run in interactive mode for testing."""
    print("🎮 Thea Autonomous Interactive Mode")
    print("=" * 40)
    print("Type messages to send to Thea (or 'quit' to exit)")
    print("-" * 40)
    
    try:
        with TheaAutonomousSystem(headless=False) as thea:
            while True:
                message = input("\n📤 Enter message: ").strip()
                
                if message.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                if not message:
                    print("⚠️  Please enter a message")
                    continue
                
                print(f"📤 Sending: {message}")
                response = thea.send_message_autonomous(message)
                
                if response:
                    print(f"✅ Response: {response[:500]}...")
                else:
                    print("❌ No response received")
                    
    except KeyboardInterrupt:
        print("\n👋 Interrupted by user")
    except Exception as e:
        print(f"❌ Error in interactive mode: {e}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Thea Autonomous System CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s send "Hello Thea!"
  %(prog)s status
  %(prog)s test
  %(prog)s interactive
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Send command
    send_parser = subparsers.add_parser('send', help='Send a message to Thea')
    send_parser.add_argument('message', help='Message to send to Thea')
    send_parser.add_argument('--visible', action='store_true', 
                           help='Run browser in visible mode (default: headless)')
    
    # Status command
    subparsers.add_parser('status', help='Get system status')
    
    # Test command
    subparsers.add_parser('test', help='Run a test message')
    
    # Interactive command
    subparsers.add_parser('interactive', help='Run in interactive mode')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        if args.command == 'send':
            headless = not args.visible
            success = send_message_command(args.message, headless=headless)
            return 0 if success else 1
            
        elif args.command == 'status':
            success = status_command()
            return 0 if success else 1
            
        elif args.command == 'test':
            success = test_command()
            return 0 if success else 1
            
        elif args.command == 'interactive':
            interactive_command()
            return 0
            
        else:
            print(f"❌ Unknown command: {args.command}")
            return 1
            
    except KeyboardInterrupt:
        print("\n👋 Interrupted by user")
        return 1
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
