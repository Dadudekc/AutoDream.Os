"""
ChatGPT CLI - V2 Compliant
=========================

Command-line interface for ChatGPT integration.
Provides commands for browser automation and conversation management.

V2 Compliance: ≤400 lines, SOLID principles, comprehensive error handling.

Author: Agent-1 - Browser Automation Specialist
License: MIT
"""

import argparse
import asyncio
import json
import sys

from .extractor import ConversationExtractor
from .navigator import ChatGPTNavigator
from .session import BrowserSessionManager


def create_chatgpt_parser() -> argparse.ArgumentParser:
    """Create argument parser for ChatGPT CLI."""
    parser = argparse.ArgumentParser(
        description="ChatGPT Integration CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Navigate command
    nav_parser = subparsers.add_parser("navigate", help="Navigate to ChatGPT")
    nav_parser.add_argument("--url", help="Conversation URL (optional)")
    nav_parser.add_argument("--headless", action="store_true", help="Run in headless mode")

    # Send message command
    send_parser = subparsers.add_parser("send", help="Send message to ChatGPT")
    send_parser.add_argument("--message", required=True, help="Message to send")
    send_parser.add_argument("--wait", action="store_true", help="Wait for response")

    # Extract command
    extract_parser = subparsers.add_parser("extract", help="Extract conversation")
    extract_parser.add_argument("--url", help="Conversation URL")
    extract_parser.add_argument("--output", help="Output filename")

    # List conversations
    subparsers.add_parser("list", help="List saved conversations")

    # Show conversation
    show_parser = subparsers.add_parser("show", help="Show conversation details")
    show_parser.add_argument("--file", required=True, help="Conversation filename")

    # Session commands
    session_parser = subparsers.add_parser("session", help="Manage browser session")
    session_parser.add_argument(
        "--action", required=True, choices=["save", "load", "clear", "info"], help="Session action"
    )

    # Info command
    subparsers.add_parser("info", help="Show ChatGPT integration capabilities")

    return parser


async def navigate_to_chatgpt(args: argparse.Namespace) -> None:
    """Navigate to ChatGPT."""
    navigator = ChatGPTNavigator()

    try:
        print(f"🌐 Navigating to ChatGPT...")
        page = await navigator.navigate_to_chat(conversation_url=args.url)

        if page:
            print(f"✅ Successfully navigated to ChatGPT")
            print(f"URL: {page.url}")
            print("\nPress Enter to close browser...")
            input()
        else:
            print("❌ Navigation failed")
            sys.exit(1)

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    finally:
        await navigator.close()


async def send_message_to_chatgpt(args: argparse.Namespace) -> None:
    """Send message to ChatGPT."""
    navigator = ChatGPTNavigator()

    try:
        print(f"🌐 Opening ChatGPT...")
        page = await navigator.navigate_to_chat()

        if not page:
            print("❌ Failed to open ChatGPT")
            sys.exit(1)

        print(f"📤 Sending message: {args.message[:50]}...")
        response = await navigator.send_message(args.message, wait_for_response=args.wait)

        if args.wait and response:
            print(f"\n📥 Response:\n{response}")

        print("\n✅ Message sent successfully")

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    finally:
        await navigator.close()


async def extract_conversation(args: argparse.Namespace) -> None:
    """Extract ChatGPT conversation."""
    navigator = ChatGPTNavigator()
    extractor = ConversationExtractor()

    try:
        print(f"🌐 Opening ChatGPT conversation...")
        page = await navigator.navigate_to_chat(conversation_url=args.url)

        if not page:
            print("❌ Failed to open ChatGPT")
            sys.exit(1)

        print(f"📥 Extracting conversation...")
        conversation = await extractor.extract_conversation(page)

        print(f"✅ Extracted {conversation.get('message_count', 0)} messages")

        # Save conversation
        filename = args.output or None
        saved_path = extractor.save_conversation(conversation, filename)

        if saved_path:
            print(f"💾 Conversation saved: {saved_path}")
        else:
            print("❌ Failed to save conversation")

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    finally:
        await navigator.close()


def list_conversations() -> None:
    """List all saved conversations."""
    extractor = ConversationExtractor()
    conversations = extractor.list_conversations()

    if not conversations:
        print("No conversations found")
        return

    print(f"\n📚 Saved Conversations ({len(conversations)}):\n")
    for conv in conversations:
        print(f"File: {conv['filename']}")
        print(f"  ID: {conv.get('conversation_id')}")
        print(f"  Messages: {conv.get('message_count', 0)}")
        print(f"  Size: {conv.get('file_size', 0)} bytes")
        print()


def show_conversation(args: argparse.Namespace) -> None:
    """Show conversation details."""
    extractor = ConversationExtractor()

    try:
        conversation = extractor.load_conversation(args.file)

        if not conversation:
            print(f"❌ Failed to load conversation: {args.file}")
            sys.exit(1)

        print(f"\n💬 Conversation: {conversation.get('conversation_id')}\n")
        print(f"Messages: {conversation.get('message_count', 0)}")
        print(f"URL: {conversation.get('url', 'N/A')}")
        print(f"\nMessages:\n")

        for msg in conversation.get("messages", [])[:10]:  # Show first 10
            role = msg.get("role", "unknown")
            text = msg.get("text", "")
            print(f"[{role.upper()}] {text[:100]}...")
            print()

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


async def manage_session(args: argparse.Namespace) -> None:
    """Manage browser session."""
    session_manager = BrowserSessionManager()

    try:
        if args.action == "info":
            info = session_manager.get_session_info()
            print("\n📊 Session Information:\n")
            print(f"Persistent: {info['persistent']}")
            print(f"Session Valid: {info['session_valid']}")
            print(f"Cookies: {info['cookies_count']}")
            print()

        elif args.action == "clear":
            success = session_manager.clear_session()
            if success:
                print("✅ Session cleared")
            else:
                print("❌ Failed to clear session")

        elif args.action == "load":
            success = await session_manager.load_session()
            if success:
                print("✅ Session loaded")
            else:
                print("❌ Failed to load session")

        else:
            print(f"Unknown session action: {args.action}")

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


def show_info() -> None:
    """Show ChatGPT integration capabilities."""
    navigator = ChatGPTNavigator()
    session_manager = BrowserSessionManager()
    extractor = ConversationExtractor()

    print("\n📊 ChatGPT Integration Capabilities:\n")
    print("Navigation:")
    nav_info = navigator.get_navigation_info()
    print(f"  Playwright: {nav_info['playwright_available']}")
    print(f"  Default URL: {nav_info['default_url']}")

    print("\nSession:")
    session_info = session_manager.get_session_info()
    print(f"  Persistent: {session_info['persistent']}")
    print(f"  Valid: {session_info['session_valid']}")

    print("\nExtraction:")
    extract_info = extractor.get_extraction_info()
    print(f"  Conversations: {extract_info['conversations_count']}")
    print()


def main():
    """Main CLI entry point."""
    parser = create_chatgpt_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        if args.command == "navigate":
            asyncio.run(navigate_to_chatgpt(args))
        elif args.command == "send":
            asyncio.run(send_message_to_chatgpt(args))
        elif args.command == "extract":
            asyncio.run(extract_conversation(args))
        elif args.command == "list":
            list_conversations()
        elif args.command == "show":
            show_conversation(args)
        elif args.command == "session":
            asyncio.run(manage_session(args))
        elif args.command == "info":
            show_info()
        else:
            print(f"Unknown command: {args.command}")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

