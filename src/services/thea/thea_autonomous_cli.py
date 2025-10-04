#!/usr/bin/env python3
"""
Thea Autonomous CLI
==================
Autonomous communication interface for Thea consultation system.
V2 Compliant: ≤400 lines, focused autonomous communication

Author: Agent-7 (Implementation Specialist)
License: MIT
"""

import argparse
import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

logger = logging.getLogger(__name__)


class TheaAutonomousCommunication:
    """Autonomous communication with Thea consultation system."""

    def __init__(self, project_root: str = "."):
        """Initialize autonomous communication."""
        self.project_root = Path(project_root)
        self.communication_log = self.project_root / "thea_communications.json"
        self.session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        logger.info(f"TheaAutonomousCommunication initialized - Session: {self.session_id}")

    def send_message(self, message: str, context: str = None) -> dict[str, Any]:
        """Send autonomous message to Thea."""
        try:
            logger.info(f"Sending autonomous message: {message[:50]}...")

            # Create communication record
            communication = {
                "session_id": self.session_id,
                "message": message,
                "context": context or "general",
                "timestamp": datetime.now().isoformat(),
                "status": "sent",
                "type": "autonomous_communication",
            }

            # Store communication
            self._store_communication(communication)

            # Process message (in a real implementation, this would communicate with Thea)
            response = self._process_autonomous_message(message, context)

            # Update communication with response
            communication.update(
                {
                    "response": response,
                    "status": "completed",
                    "response_timestamp": datetime.now().isoformat(),
                }
            )

            self._update_communication(communication)

            logger.info("Autonomous message sent successfully")
            return {
                "success": True,
                "session_id": self.session_id,
                "message_id": communication.get("message_id"),
                "response": response,
            }

        except Exception as e:
            logger.error(f"Autonomous message failed: {e}")
            return {"success": False, "error": str(e), "session_id": self.session_id}

    def _process_autonomous_message(self, message: str, context: str = None) -> dict[str, Any]:
        """Process autonomous message (placeholder for actual Thea integration)."""
        # This is a placeholder implementation
        # In a real system, this would integrate with Thea's AI

        response = {
            "type": "autonomous_response",
            "acknowledged": True,
            "message": f"Autonomous message received: '{message}'",
            "context": context or "general",
            "recommendations": [
                "Message has been logged for Thea's review",
                "Response will be provided during next consultation cycle",
                "Consider using strategic consultation for detailed guidance",
            ],
            "next_steps": [
                "Monitor for Thea's response",
                "Use consultation system for immediate needs",
                "Check communication logs for updates",
            ],
        }

        return response

    def _store_communication(self, communication: dict[str, Any]) -> None:
        """Store communication record."""
        try:
            # Load existing communications
            communications = []
            if self.communication_log.exists():
                with open(self.communication_log) as f:
                    communications = json.load(f)

            # Add message ID
            communication[
                "message_id"
            ] = f"msg_{len(communications) + 1}_{datetime.now().strftime('%H%M%S')}"

            # Add new communication
            communications.append(communication)

            # Save updated communications
            with open(self.communication_log, "w") as f:
                json.dump(communications, f, indent=2)

        except Exception as e:
            logger.error(f"Failed to store communication: {e}")

    def _update_communication(self, communication: dict[str, Any]) -> None:
        """Update existing communication record."""
        try:
            # Load existing communications
            communications = []
            if self.communication_log.exists():
                with open(self.communication_log) as f:
                    communications = json.load(f)

            # Update the communication
            for i, comm in enumerate(communications):
                if comm.get("message_id") == communication.get("message_id"):
                    communications[i] = communication
                    break

            # Save updated communications
            with open(self.communication_log, "w") as f:
                json.dump(communications, f, indent=2)

        except Exception as e:
            logger.error(f"Failed to update communication: {e}")

    def get_communication_history(self, limit: int = 10) -> list[dict[str, Any]]:
        """Get communication history."""
        try:
            if not self.communication_log.exists():
                return []

            with open(self.communication_log) as f:
                communications = json.load(f)

            # Return recent communications
            return communications[-limit:] if communications else []

        except Exception as e:
            logger.error(f"Failed to get communication history: {e}")
            return []

    def get_session_status(self) -> dict[str, Any]:
        """Get current session status."""
        try:
            history = self.get_communication_history()
            session_communications = [
                comm for comm in history if comm.get("session_id") == self.session_id
            ]

            return {
                "session_id": self.session_id,
                "total_messages": len(session_communications),
                "pending_responses": len(
                    [comm for comm in session_communications if comm.get("status") == "sent"]
                ),
                "completed_communications": len(
                    [comm for comm in session_communications if comm.get("status") == "completed"]
                ),
                "session_start": session_communications[0]["timestamp"]
                if session_communications
                else None,
                "last_activity": session_communications[-1]["timestamp"]
                if session_communications
                else None,
            }

        except Exception as e:
            logger.error(f"Failed to get session status: {e}")
            return {"session_id": self.session_id, "error": str(e)}


def send_command_handler(args: argparse.Namespace) -> int:
    """Handle send command."""
    print("🤖 Thea Autonomous Communication")
    print("=" * 50)

    try:
        thea = TheaAutonomousCommunication()

        result = thea.send_message(message=args.message, context=args.context)

        if result["success"]:
            print("✅ Message sent successfully!")
            print(f"📋 Session ID: {result['session_id']}")
            print(f"📨 Message ID: {result['message_id']}")

            # Display response
            response = result["response"]
            print("\n📊 Thea Response:")
            print(f"Type: {response['type']}")
            print(f"Message: {response['message']}")

            if "recommendations" in response:
                print("\n💡 Recommendations:")
                for i, rec in enumerate(response["recommendations"], 1):
                    print(f"   {i}. {rec}")

            if "next_steps" in response:
                print("\n🎯 Next Steps:")
                for i, step in enumerate(response["next_steps"], 1):
                    print(f"   {i}. {step}")

            return 0
        else:
            print(f"❌ Message failed: {result.get('error', 'Unknown error')}")
            return 1

    except Exception as e:
        print(f"❌ Send command error: {e}")
        return 1


def status_command_handler(args: argparse.Namespace) -> int:
    """Handle status command."""
    print("📊 Thea Autonomous Communication Status")
    print("=" * 50)

    try:
        thea = TheaAutonomousCommunication()

        # Get session status
        status = thea.get_session_status()
        print("📋 Session Status:")
        print(f"   Session ID: {status['session_id']}")
        print(f"   Total Messages: {status.get('total_messages', 0)}")
        print(f"   Pending Responses: {status.get('pending_responses', 0)}")
        print(f"   Completed: {status.get('completed_communications', 0)}")

        if status.get("session_start"):
            print(f"   Session Start: {status['session_start']}")
        if status.get("last_activity"):
            print(f"   Last Activity: {status['last_activity']}")

        # Get communication history
        history = thea.get_communication_history(limit=5)
        print(f"\n📋 Recent Communications: {len(history)}")

        if history:
            for comm in history:
                status_icon = (
                    "✅"
                    if comm.get("status") == "completed"
                    else "⏳"
                    if comm.get("status") == "sent"
                    else "❌"
                )
                print(
                    f"   {status_icon} {comm.get('message_id', 'N/A')}: {comm.get('message', '')[:50]}{'...' if len(comm.get('message', '')) > 50 else ''}"
                )

        return 0

    except Exception as e:
        print(f"❌ Status command error: {e}")
        return 1


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="Thea Autonomous Communication System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Send command
    send_parser = subparsers.add_parser("send", help="Send autonomous message to Thea")
    send_parser.add_argument("message", help="Message to send to Thea")
    send_parser.add_argument("--context", help="Additional context for the message")

    # Status command
    status_parser = subparsers.add_parser("status", help="Show communication status and history")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Route to appropriate handler
    if args.command == "send":
        return send_command_handler(args)
    elif args.command == "status":
        return status_command_handler(args)
    else:
        print(f"❌ Unknown command: {args.command}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
