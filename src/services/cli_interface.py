#!/usr/bin/env python3
"""
CLI Interface for V2 Message Delivery Service
Handles command-line interface and user interactions
"""

import argparse
import json
import time
import logging

from src.utils.stability_improvements import stability_manager, safe_import
from typing import Dict, Any, List
from messaging import UnifiedMessagingService as V2MessageDeliveryService  # Backward compatibility alias

logger = logging.getLogger(__name__)


class CLIInteface:
    """Command-line interface for V2 Message Delivery Service"""

    def __init__(self):
        self.delivery_service = V2MessageDeliveryService()
        # Registry mapping command names to handler callables
        self.command_registry = {
            "status": lambda a: self._show_status(),
            "agents": lambda a: self._show_agents(),
            "ping": lambda a: self._ping_agent(a.ping[0]),
            "ping_all": lambda a: self._ping_all_agents(),
            "coordinate": lambda a: self._coordinate_agents(a.coordinate[0], a.coordinate[1]),
            "emergency": lambda a: self._send_emergency(a.emergency[0]),
            "send": lambda a: self._send_message(*a.send),
            "send_file": lambda a: self._send_file_message(*a.send_file),
            "send_sync": lambda a: self._send_sync_message(*a.send_sync),
            "broadcast": lambda a: self._broadcast_message(*a.broadcast),
            "broadcast_sync": lambda a: self._broadcast_sync_message(*a.broadcast_sync),
            "broadcast_file": lambda a: self._broadcast_file_message(*a.broadcast_file),
            "broadcast_file_sync": lambda a: self._broadcast_file_sync_message(*a.broadcast_file_sync),
            "update_coords": lambda a: self._update_coordinates(*a.update_coords),
            "test": lambda a: self._test_delivery(),
            "test_sync": lambda a: self._test_sync_delivery(),
        }

    def run(self, args=None):
        """Run the CLI interface"""
        parser = self._create_argument_parser()
        parsed_args = parser.parse_args(args)

        try:
            for cmd, handler in self.command_registry.items():
                if getattr(parsed_args, cmd):
                    handler(parsed_args)
                    break
            else:
                self._show_help()
        except Exception as e:
            print(f"❌ Error: {e}")
            return 1

        return 0

    def _create_argument_parser(self):
        """Create the argument parser"""
        parser = argparse.ArgumentParser(description="V2 Message Delivery Service")
        
        # Status and information commands
        parser.add_argument("--status", action="store_true", help="Show delivery status")
        parser.add_argument("--agents", action="store_true", help="List all available agents")
        
        # Message sending commands
        parser.add_argument(
            "--send",
            nargs=3,
            metavar=("AGENT", "TYPE", "MESSAGE"),
            help="Send message to agent (agent type message)",
        )
        parser.add_argument(
            "--send-file",
            nargs=3,
            metavar=("AGENT", "TYPE", "FILEPATH"),
            help="Send message to agent from file (agent type file)",
        )
        parser.add_argument(
            "--send-sync",
            nargs=3,
            metavar=("AGENT", "TYPE", "MESSAGE"),
            help="Send message to agent synchronously (agent type message)",
        )
        
        # Broadcast commands
        parser.add_argument(
            "--broadcast",
            nargs=2,
            metavar=("TYPE", "MESSAGE"),
            help="Broadcast message to all agents (type message)",
        )
        parser.add_argument(
            "--broadcast-file",
            nargs=2,
            metavar=("TYPE", "FILEPATH"),
            help="Broadcast message to all agents from file (type file)",
        )
        parser.add_argument(
            "--broadcast-sync",
            nargs=2,
            metavar=("TYPE", "MESSAGE"),
            help="Broadcast message synchronously to all agents (type message)",
        )
        parser.add_argument(
            "--broadcast-file-sync",
            nargs=2,
            metavar=("TYPE", "FILEPATH"),
            help="Broadcast message synchronously to all agents from file (type file)",
        )
        
        # Utility commands
        parser.add_argument(
            "--ping", nargs=1, metavar="AGENT", help="Send ping message to specific agent"
        )
        parser.add_argument("--ping-all", action="store_true", help="Send ping to all agents")
        parser.add_argument(
            "--coordinate",
            nargs=2,
            metavar=("AGENTS", "MESSAGE"),
            help="Send coordination message to specific agents (comma-separated list)",
        )
        parser.add_argument(
            "--emergency",
            nargs=1,
            metavar="MESSAGE",
            help="Send emergency broadcast to all agents",
        )
        
        # Configuration and testing
        parser.add_argument(
            "--update-coords",
            nargs=3,
            metavar=("AGENT", "X", "Y"),
            help="Update agent coordinates (agent x y)",
        )
        parser.add_argument("--test", action="store_true", help="Test message delivery")
        parser.add_argument("--test-sync", action="store_true", help="Test synchronous message delivery")
        
        return parser

    def _show_status(self):
        """Show detailed delivery status"""
        status = self.delivery_service.get_delivery_status()
        print("📊 V2 MESSAGE DELIVERY SERVICE STATUS")
        print("=" * 50)

        # Agent status summary
        print(f"\n🤖 AGENT STATUS ({len(status['agent_coordinates'])} agents)")
        print("-" * 40)
        for agent_id, agent_info in status["agent_coordinates"].items():
            status_icon = "🟢" if agent_info["status"] == "active" else "🔴"
            last_delivery = time.strftime(
                "%H:%M:%S", time.localtime(agent_info["last_delivery"])
            )
            print(
                f"{status_icon} {agent_id}: {agent_info['name']} at ({agent_info['input_x']}, {agent_info['input_y']}) - Last: {last_delivery}"
            )

        # Delivery statistics
        print(f"\n📈 DELIVERY STATISTICS")
        print("-" * 40)
        total_deliveries = 0
        total_success = 0
        total_failures = 0

        for agent_status in status["delivery_status"].values():
            total_deliveries += agent_status.get("delivery_count", 0)
            total_success += agent_status.get("successful_deliveries", 0)
            total_failures += agent_status.get("failed_deliveries", 0)

        print(f"Total Messages: {total_deliveries}")
        print(f"Successful: {total_success}")
        print(f"Failed: {total_failures}")
        if total_deliveries > 0:
            print(f"Success Rate: {(total_success/total_deliveries*100):.1f}%")
        else:
            print("Success Rate: N/A")

        # Individual agent delivery status
        if status["delivery_status"]:
            print(f"\n📊 INDIVIDUAL AGENT DELIVERY STATUS")
            print("-" * 40)
            for agent_id, agent_status in status["delivery_status"].items():
                print(
                    f"{agent_id}: {agent_status.get('delivery_count', 0)} messages, "
                    f"{agent_status.get('successful_deliveries', 0)} success, "
                    f"{agent_status.get('failed_deliveries', 0)} failed"
                )

        # System status
        print(f"\n⚙️ SYSTEM STATUS")
        print("-" * 40)
        print(f"PyAutoGUI Available: {'✅ Yes' if status['pyautogui_available'] else '❌ No'}")
        print(f"Queue Size: {status['queue_size']}")
        print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(status['timestamp']))}")

    def _show_agents(self):
        """Show all available agents"""
        print("🤖 AVAILABLE AGENTS")
        print("=" * 50)
        status = self.delivery_service.get_delivery_status()
        for agent_id, agent_info in status["agent_coordinates"].items():
            status_icon = "🟢" if agent_info["status"] == "active" else "🔴"
            print(f"{status_icon} {agent_id}: {agent_info['name']}")
            print(f"   Coordinates: ({agent_info['input_x']}, {agent_info['input_y']})")
            print(f"   Status: {agent_info['status']}")
            print()

    def _ping_agent(self, agent_id: str):
        """Send ping to specific agent"""
        success = self.delivery_service.send_message(
            agent_id, "ping", "Ping message - please acknowledge receipt"
        )
        print(f"{'✅' if success else '❌'} Ping {'sent' if success else 'failed'} to {agent_id}")

    def _ping_all_agents(self):
        """Send ping to all agents"""
        print("📡 Pinging all agents...")
        results = self.delivery_service.broadcast_message(
            "ping", "System ping - all agents please acknowledge"
        )
        success_count = sum(1 for success in results.values() if success)
        print(f"📊 Ping results: {success_count}/{len(results)} agents responded")
        for agent_id, success in results.items():
            status_icon = "✅" if success else "❌"
            print(f"{status_icon} {agent_id}")

    def _coordinate_agents(self, agents_str: str, message: str):
        """Coordinate with specific agents"""
        target_agents = [agent.strip() for agent in agents_str.split(",")]
        print(f"🤝 Coordinating with agents: {', '.join(target_agents)}")
        results = self.delivery_service.broadcast_message(
            "coordination", message, target_agents
        )
        success_count = sum(1 for success in results.values() if success)
        print(f"📊 Coordination results: {success_count}/{len(target_agents)} agents received")

    def _send_emergency(self, message: str):
        """Send emergency broadcast"""
        print("🚨 Sending emergency broadcast...")
        results = self.delivery_service.broadcast_message(
            "emergency", f"EMERGENCY: {message}"
        )
        success_count = sum(1 for success in results.values() if success)
        print(f"🚨 Emergency broadcast sent to {success_count}/8 agents")

    def _send_message(self, agent_id: str, message_type: str, message: str):
        """Send message to specific agent"""
        success = self.delivery_service.send_message(agent_id, message_type, message)
        print(f"{'✅' if success else '❌'} Message {'sent' if success else 'failed'} to {agent_id}")

    def _read_file_content(self, filepath: str) -> str:
        """Read file content with best-effort encoding detection"""
        with open(filepath, "rb") as f:
            raw = f.read()
        for enc in ("utf-8-sig", "cp1252", "latin-1"):
            try:
                return raw.decode(enc)
            except Exception:
                continue
        raise UnicodeDecodeError("unknown", raw, 0, 1, "cannot decode")

    def _send_file_message(self, agent_id: str, message_type: str, filepath: str):
        """Send file content to specific agent"""
        try:
            content = self._read_file_content(filepath)
            success = self.delivery_service.send_message(agent_id, message_type, content)
            print(f"{'✅' if success else '❌'} File message {'sent' if success else 'failed'} to {agent_id}")
        except Exception as e:
            print(f"❌ Error reading file: {e}")

    def _send_sync_message(self, agent_id: str, message_type: str, message: str):
        """Send synchronous message to specific agent"""
        success = self.delivery_service.send_message_sync(agent_id, message_type, message)
        print(f"{'✅' if success else '❌'} Synchronous message {'sent' if success else 'failed'} to {agent_id}")

    def _broadcast_message(self, message_type: str, message: str):
        """Broadcast message to all agents"""
        results = self.delivery_service.broadcast_message(message_type, message)
        success_count = sum(1 for success in results.values() if success)
        print(f"📢 Broadcast sent to {success_count}/8 agents")
        print(f"Results: {results}")

    def _broadcast_sync_message(self, message_type: str, message: str):
        """Broadcast message synchronously to all agents"""
        agents = list(self.delivery_service.agent_coordinates.keys())
        results = {}
        for agent_id in agents:
            ok = self.delivery_service.send_message_sync(agent_id, message_type, message)
            results[agent_id] = ok
            time.sleep(0.2)
        success_count = sum(1 for success in results.values() if success)
        print(f"📢 Broadcast (sync) sent to {success_count}/{len(results)} agents")
        print(f"Results: {results}")

    def _broadcast_file_message(self, message_type: str, filepath: str):
        """Broadcast file content to all agents"""
        try:
            content = self._read_file_content(filepath)
            results = self.delivery_service.broadcast_message(message_type, content)
            success_count = sum(1 for success in results.values() if success)
            print(f"📢 Broadcast sent to {success_count}/8 agents")
            print(f"Results: {results}")
        except Exception as e:
            print(f"❌ Error reading file: {e}")

    def _broadcast_file_sync_message(self, message_type: str, filepath: str):
        """Broadcast file content synchronously to all agents"""
        try:
            content = self._read_file_content(filepath)
            agents = list(self.delivery_service.agent_coordinates.keys())
            results = {}
            for agent_id in agents:
                ok = self.delivery_service.send_message_sync(agent_id, message_type, content)
                results[agent_id] = ok
                time.sleep(0.2)
            success_count = sum(1 for success in results.values() if success)
            print(f"📢 Broadcast (sync) sent to {success_count}/{len(results)} agents")
            print(f"Results: {results}")
        except Exception as e:
            print(f"❌ Error reading file: {e}")

    def _update_coordinates(self, agent_id: str, x: str, y: str):
        """Update agent coordinates"""
        success = self.delivery_service.update_agent_coordinates(agent_id, int(x), int(y))
        print(f"{'✅' if success else '❌'} Coordinates {'updated' if success else 'failed'} for {agent_id}")

    def _test_delivery(self):
        """Test message delivery"""
        print("🧪 Testing message delivery...")

        # Test individual message
        self.delivery_service.send_message("agent_1", "test", "This is a test message")
        time.sleep(1)

        # Test broadcast
        self.delivery_service.broadcast_message("test_broadcast", "This is a test broadcast")
        time.sleep(1)

        # Show status
        status = self.delivery_service.get_delivery_status()
        print(json.dumps(status, indent=2, default=str))

    def _test_sync_delivery(self):
        """Test synchronous message delivery"""
        print("🧪 Testing synchronous message delivery...")
        self.delivery_service.send_message_sync(
            "agent_1", "test_sync", "This is a synchronous test message"
        )
        time.sleep(1)
        status = self.delivery_service.get_delivery_status()
        print(json.dumps(status, indent=2, default=str))

    def _show_help(self):
        """Show help information"""
        print("📤 V2 Message Delivery Service - Enhanced CLI")
        print("=" * 50)
        print("Available commands:")
        print("  --status          Show detailed delivery status")
        print("  --agents          List all available agents")
        print("  --send AGENT TYPE MESSAGE             Send message to specific agent")
        print("  --send-file AGENT TYPE FILE           Send file content to agent")
        print("  --broadcast TYPE MESSAGE              Broadcast to all agents")
        print("  --broadcast-file TYPE FILE            Broadcast file content to all agents")
        print("  --broadcast-sync TYPE MESSAGE         Broadcast synchronously to all agents")
        print("  --broadcast-file-sync TYPE FILE       Broadcast file content synchronously to all agents")
        print("  --ping AGENT      Send ping to specific agent")
        print("  --ping-all        Send ping to all agents")
        print("  --coordinate AGENTS MESSAGE  Coordinate with specific agents")
        print("  --emergency MESSAGE          Emergency broadcast")
        print("  --update-coords AGENT X Y    Update agent coordinates")
        print("  --test           Test message delivery")
        print("  --test-sync      Test synchronous message delivery")
        print("\nExamples:")
        print("  python src/services/cli.py --ping agent_1")
        print("  python src/services/cli.py --coordinate 'agent_1,agent_3' 'Coordinate multimedia integration'")
        print("  python src/services/cli.py --emergency 'System maintenance required'")


def main():
    """Main CLI entry point"""
    cli = CLIInteface()
    return cli.run()


if __name__ == "__main__":
    exit(main())
