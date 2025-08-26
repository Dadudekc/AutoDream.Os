#!/usr/bin/env python3
"""
Unified Coordination CLI - Agent Cellphone V2
============================================

Command-line interface for the unified coordination system.
Provides easy access to all coordination and routing functionality.

Architecture: Single Responsibility Principle - CLI interface for coordination system
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Any

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from .unified_coordination_system import (
    UnifiedCoordinationSystem,
    CoordinationMode,
    MessageType,
    MessagePriority
)


class UnifiedCoordinationCLI:
    """CLI interface for the unified coordination system."""

    def __init__(self):
        """Initialize the CLI interface."""
        self.coordinator = UnifiedCoordinationSystem()
        self.parser = self._setup_argument_parser()

    def _setup_argument_parser(self) -> argparse.ArgumentParser:
        """Setup command line argument parser."""
        parser = argparse.ArgumentParser(
            description="Unified Coordination System CLI",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  # Start coordination system
  python -m src.core.unified_coordination_cli start

  # Send a message
  python -m src.core.unified_coordination_cli send --from Agent-1 --to Agent-2 --type task --content '{"task": "test"}'

  # Broadcast message
  python -m src.core.unified_coordination_cli broadcast --from Agent-1 --type status --content '{"status": "ready"}'

  # Get system health
  python -m src.core.unified_coordination_cli health

  # Create coordination session
  python -m src.core.unified_coordination_cli session --create --id test_session --mode consensus --participants Agent-1,Agent-2

  # Get coordination metrics
  python -m src.core.unified_coordination_cli metrics
            """
        )

        subparsers = parser.add_subparsers(dest='command', help='Available commands')

        # Start command
        start_parser = subparsers.add_parser('start', help='Start coordination system')
        start_parser.add_argument('--workspace', default='agent_workspaces', help='Workspace path')

        # Stop command
        stop_parser = subparsers.add_parser('stop', help='Stop coordination system')

        # Send message command
        send_parser = subparsers.add_parser('send', help='Send a message')
        send_parser.add_argument('--from', dest='sender', required=True, help='Sender agent ID')
        send_parser.add_argument('--to', dest='recipient', required=True, help='Recipient agent ID')
        send_parser.add_argument('--type', required=True, choices=['coordination', 'task', 'status', 'result', 'error'], help='Message type')
        send_parser.add_argument('--content', required=True, help='Message content (JSON string)')
        send_parser.add_argument('--priority', default='normal', choices=['low', 'normal', 'high', 'critical'], help='Message priority')
        send_parser.add_argument('--expires', type=int, help='Message expiration in seconds')

        # Broadcast command
        broadcast_parser = subparsers.add_parser('broadcast', help='Broadcast message to all agents')
        broadcast_parser.add_argument('--from', dest='sender', required=True, help='Sender agent ID')
        broadcast_parser.add_argument('--type', required=True, choices=['coordination', 'task', 'status', 'result', 'error'], help='Message type')
        broadcast_parser.add_argument('--content', required=True, help='Message content (JSON string)')
        broadcast_parser.add_argument('--priority', default='normal', choices=['low', 'normal', 'high', 'critical'], help='Message priority')
        broadcast_parser.add_argument('--targets', help='Comma-separated list of target agents')

        # Health command
        health_parser = subparsers.add_parser('health', help='Get system health')

        # Session command
        session_parser = subparsers.add_parser('session', help='Manage coordination sessions')
        session_parser.add_argument('--create', action='store_true', help='Create new session')
        session_parser.add_argument('--id', help='Session ID')
        session_parser.add_argument('--mode', choices=['consensus', 'majority', 'expert_opinion', 'hierarchical', 'collaborative'], help='Coordination mode')
        session_parser.add_argument('--participants', help='Comma-separated list of participants')
        session_parser.add_argument('--protocol', help='Protocol configuration (JSON string)')
        session_parser.add_argument('--list', action='store_true', help='List all sessions')
        session_parser.add_argument('--get', help='Get session by ID')

        # Metrics command
        metrics_parser = subparsers.add_parser('metrics', help='Get coordination metrics')

        # Status command
        status_parser = subparsers.add_parser('status', help='Get coordination status')

        return parser

    def run(self, args=None):
        """Run the CLI with given arguments."""
        if args is None:
            args = sys.argv[1:]

        if not args:
            self.parser.print_help()
            return

        parsed_args = self.parser.parse_args(args)
        self._execute_command(parsed_args)

    def _execute_command(self, args):
        """Execute the parsed command."""
        try:
            if args.command == 'start':
                self._start_coordination(args)
            elif args.command == 'stop':
                self._stop_coordination(args)
            elif args.command == 'send':
                self._send_message(args)
            elif args.command == 'broadcast':
                self._broadcast_message(args)
            elif args.command == 'health':
                self._get_health(args)
            elif args.command == 'session':
                self._manage_session(args)
            elif args.command == 'metrics':
                self._get_metrics(args)
            elif args.command == 'status':
                self._get_status(args)
            else:
                self.parser.print_help()
        except Exception as e:
            print(f"❌ Error executing command: {e}")
            sys.exit(1)

    def _start_coordination(self, args):
        """Start the coordination system."""
        print("🚀 Starting unified coordination system...")
        self.coordinator.start_coordination_system()
        print("✅ Coordination system started successfully")

    def _stop_coordination(self, args):
        """Stop the coordination system."""
        print("⏹️ Stopping coordination system...")
        self.coordinator.stop_coordination_system()
        print("✅ Coordination system stopped successfully")

    def _send_message(self, args):
        """Send a message."""
        try:
            content = json.loads(args.content)
        except json.JSONDecodeError:
            print("❌ Invalid JSON content")
            return

        message_type = MessageType(args.type)
        priority = MessagePriority(args.priority)

        message_id = self.coordinator.send_message(
            sender_id=args.sender,
            recipient_id=args.recipient,
            message_type=message_type,
            content=content,
            priority=priority,
            expires_in=args.expires
        )

        if message_id:
            print(f"✅ Message sent successfully: {message_id}")
        else:
            print("❌ Failed to send message")

    def _broadcast_message(self, args):
        """Broadcast a message."""
        try:
            content = json.loads(args.content)
        except json.JSONDecodeError:
            print("❌ Invalid JSON content")
            return

        message_type = MessageType(args.type)
        priority = MessagePriority(args.priority)
        target_agents = None
        if args.targets:
            target_agents = [agent.strip() for agent in args.targets.split(',')]

        message_ids = self.coordinator.broadcast_message(
            sender_id=args.sender,
            message_type=message_type,
            content=content,
            priority=priority,
            target_agents=target_agents
        )

        print(f"✅ Broadcast message sent to {len(message_ids)} agents")
        for msg_id in message_ids:
            print(f"  📤 {msg_id}")

    def _get_health(self, args):
        """Get system health."""
        health = self.coordinator.get_system_health()
        print("🏥 SYSTEM HEALTH REPORT")
        print("=" * 50)
        for key, value in health.items():
            print(f"{key.replace('_', ' ').title()}: {value}")

    def _manage_session(self, args):
        """Manage coordination sessions."""
        if args.create:
            if not all([args.id, args.mode, args.participants]):
                print("❌ Session creation requires --id, --mode, and --participants")
                return

            participants = [p.strip() for p in args.participants.split(',')]
            protocol = {}
            if args.protocol:
                try:
                    protocol = json.loads(args.protocol)
                except json.JSONDecodeError:
                    print("❌ Invalid protocol JSON")
                    return

            session = self.coordinator.create_coordination_session(
                session_id=args.id,
                mode=CoordinationMode(args.mode),
                participants=participants,
                protocol=protocol
            )
            print(f"✅ Session created: {session['session_id']}")

        elif args.list:
            sessions = self.coordinator.coordination_sessions
            if not sessions:
                print("📋 No active coordination sessions")
            else:
                print("📋 ACTIVE COORDINATION SESSIONS")
                print("=" * 50)
                for session_id, session in sessions.items():
                    print(f"Session: {session_id}")
                    print(f"  Mode: {session['mode']}")
                    print(f"  Status: {session['status']}")
                    print(f"  Participants: {', '.join(session['participants'])}")
                    print()

        elif args.get:
            session = self.coordinator.get_coordination_session(args.get)
            if session:
                print(f"📋 SESSION DETAILS: {args.get}")
                print("=" * 50)
                for key, value in session.items():
                    print(f"{key.replace('_', ' ').title()}: {value}")
            else:
                print(f"❌ Session not found: {args.get}")

        else:
            print("❌ Session command requires --create, --list, or --get")

    def _get_metrics(self, args):
        """Get coordination metrics."""
        metrics = self.coordinator.get_coordination_metrics()
        print("📊 COORDINATION METRICS")
        print("=" * 50)
        for key, value in metrics.items():
            print(f"{key.replace('_', ' ').title()}: {value}")

    def _get_status(self, args):
        """Get coordination status."""
        health = self.coordinator.get_system_health()
        print("📊 COORDINATION STATUS")
        print("=" * 50)
        print(f"System Active: {'✅ YES' if health['coordination_active'] else '❌ NO'}")
        print(f"Cycles Completed: {health['cycles_completed']}")
        print(f"Active Sessions: {health['active_sessions']}")
        print(f"Message Queue: {health['message_queue_size']} messages")
        print(f"Message History: {health['message_history_size']} messages")
        
        if health['current_cycle']:
            print(f"Current Cycle: {health['current_cycle']}")
        else:
            print("Current Cycle: None")


def main():
    """Main entry point for the CLI."""
    cli = UnifiedCoordinationCLI()
    cli.run()


if __name__ == "__main__":
    main()
