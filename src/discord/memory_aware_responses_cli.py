#!/usr/bin/env python3
"""
Memory-Aware Responses CLI - Command Line Interface
==================================================

Command-line interface for memory-aware response generation.

V2 Compliance: ≤400 lines, ≤5 classes, ≤10 functions
Refactored By: Agent-6 (Quality Assurance Specialist)
Original: memory_aware_responses.py (488 lines) - CLI module
"""

import argparse
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.discord.memory_aware_responses_core import (
    MemoryContextManager,
    ResponseGenerator,
    ResponseType,
)


def create_argument_parser():
    """Create argument parser for CLI commands"""
    parser = argparse.ArgumentParser(
        description="Memory-Aware Responses CLI - Context-aware response generation"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Generate response command
    generate_parser = subparsers.add_parser("generate", help="Generate context-aware response")
    generate_parser.add_argument("--user-id", required=True, help="User ID")
    generate_parser.add_argument("--agent-id", required=True, help="Agent ID")
    generate_parser.add_argument("--message", required=True, help="Message to respond to")
    generate_parser.add_argument("--type", required=True, choices=[t.value for t in ResponseType], help="Response type")
    
    # Context management commands
    context_parser = subparsers.add_parser("context", help="Manage conversation contexts")
    context_subparsers = context_parser.add_subparsers(dest="context_action", help="Context actions")
    
    # List contexts
    list_parser = context_subparsers.add_parser("list", help="List active contexts")
    
    # Clear contexts
    clear_parser = context_subparsers.add_parser("clear", help="Clear all contexts")
    
    # Get context
    get_parser = context_subparsers.add_parser("get", help="Get specific context")
    get_parser.add_argument("--user-id", required=True, help="User ID")
    get_parser.add_argument("--agent-id", required=True, help="Agent ID")
    
    # Test command
    test_parser = subparsers.add_parser("test", help="Test response generation")
    test_parser.add_argument("--count", type=int, default=5, help="Number of test responses")
    
    return parser


def handle_generate_command(args):
    """Handle generate response command"""
    context_manager = MemoryContextManager()
    response_generator = ResponseGenerator(context_manager)
    
    response_type = ResponseType(args.type)
    response = response_generator.generate_response(
        args.user_id, args.agent_id, args.message, response_type
    )
    
    print(f"Generated Response: {response}")
    return 0


def handle_context_command(args):
    """Handle context management commands"""
    context_manager = MemoryContextManager()
    
    if args.context_action == "list":
        print(f"Active Contexts: {len(context_manager.active_contexts)}")
        for key, context in context_manager.active_contexts.items():
            print(f"  {key}: {context.conversation_id}")
        return 0
    
    elif args.context_action == "clear":
        context_manager.active_contexts.clear()
        print("All contexts cleared")
        return 0
    
    elif args.context_action == "get":
        context = context_manager.get_or_create_context(args.user_id, args.agent_id)
        print(f"Context: {context.conversation_id}")
        print(f"Messages: {len(context.message_history)}")
        print(f"Last Activity: {context.last_activity}")
        return 0
    
    else:
        print(f"Unknown context action: {args.context_action}")
        return 1


def handle_test_command(args):
    """Handle test command"""
    context_manager = MemoryContextManager()
    response_generator = ResponseGenerator(context_manager)
    
    test_cases = [
        ("user1", "agent-6", "Test status update", ResponseType.STATUS_UPDATE),
        ("user2", "agent-7", "Test coordination", ResponseType.COORDINATION_REQUEST),
        ("user3", "agent-8", "Test completion", ResponseType.TASK_COMPLETION),
        ("user4", "agent-6", "Test alert", ResponseType.SYSTEM_ALERT),
        ("user5", "agent-7", "Test swarm", ResponseType.SWARM_COORDINATION),
    ]
    
    for i, (user_id, agent_id, message, response_type) in enumerate(test_cases[:args.count]):
        response = response_generator.generate_response(user_id, agent_id, message, response_type)
        print(f"Test {i+1}: {response}")
    
    return 0


def handle_command(args):
    """Handle command execution"""
    try:
        if args.command == "generate":
            return handle_generate_command(args)
        elif args.command == "context":
            return handle_context_command(args)
        elif args.command == "test":
            return handle_test_command(args)
        else:
            print(f"Unknown command: {args.command}")
            return 1
    except KeyboardInterrupt:
        print("\n⚠️ Operation cancelled by user")
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return 1


def main():
    """Main CLI entry point"""
    parser = create_argument_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    return handle_command(args)


if __name__ == "__main__":
    sys.exit(main())
