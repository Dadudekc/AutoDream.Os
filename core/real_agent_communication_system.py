#!/usr/bin/env python3
"""
Real Agent Communication System - Source of Truth
================================================

This is the primary communication system for the Agent Cellphone project.
It provides:
- Input buffering to prevent message conflicts
- Broadcast messaging to all agents
- Real agent coordinate loading
- PyAutoGUI-based message delivery
- Agent registry management

This system is the SOURCE OF TRUTH for all agent communications.
"""

import os
import sys
import json
import time
import logging
import argparse
import threading
import asyncio
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import pyautogui

# Configure PyAutoGUI
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.1


class InputBufferSystem:
    """Prevents message conflicts by buffering inputs"""

    def __init__(self):
        self.buffer = []
        self.lock = threading.Lock()
        self.logger = logging.getLogger(__name__)

    def add_input(self, agent_id: str, message: str, priority: str = "normal") -> str:
        """Add input to buffer with unique ID"""
        with self.lock:
            input_id = f"{agent_id}_{int(time.time() * 1000)}"
            self.buffer.append(
                {
                    "id": input_id,
                    "agent_id": agent_id,
                    "message": message,
                    "priority": priority,
                    "timestamp": time.time(),
                }
            )
            self.logger.info(
                f"📥 Buffered input from {agent_id} (ID: {input_id}): {message[:50]}..."
            )
            return input_id

    def get_next_input(self) -> Optional[Dict]:
        """Get next input from buffer"""
        with self.lock:
            if self.buffer:
                return self.buffer.pop(0)
            return None

    def get_buffer_status(self) -> Dict:
        """Get current buffer status"""
        with self.lock:
            return {
                "count": len(self.buffer),
                "items": [item["agent_id"] for item in self.buffer],
            }


class AgentRegistry:
    """Manages agent registration and coordinates"""

    def __init__(self):
        self.agents = {}
        self.logger = logging.getLogger(__name__)

        # Initialize unified coordinate manager
        try:
            from src.services.messaging import CoordinateManager

            self.coordinate_manager = CoordinateManager()
            self.logger.info("🗺️ Unified coordinate manager initialized")
        except ImportError:
            self.coordinate_manager = None
            self.logger.warning(
                "⚠️ Unified coordinate manager not available, using fallback"
            )

        self.load_agent_coordinates()

    def load_agent_coordinates(self):
        """Load agent coordinates using unified coordinate manager"""
        try:
            if self.coordinate_manager:
                # Use unified coordinate manager
                self.logger.info(
                    "🗺️ Loading coordinates via unified coordinate manager..."
                )

                # Try 8-agent mode first, then 5-agent as fallback
                for mode in ["8-agent", "5-agent"]:
                    agents = self.coordinate_manager.get_agents_in_mode(mode)
                    if agents:
                        for agent_id in agents:
                            coords = self.coordinate_manager.get_agent_coordinates(
                                agent_id, mode
                            )
                            if coords:
                                self.agents[agent_id] = {
                                    "input_box": coords.input_box,
                                    "starter_location": coords.starter_location,
                                }

                        if self.agents:
                            self.logger.info(
                                f"✅ Loaded {len(self.agents)} real agent coordinates via unified manager ({mode} mode)"
                            )
                            for agent_id, coords in self.agents.items():
                                self.logger.info(f"📍 {agent_id}: {coords['input_box']}")
                            return

                self.logger.warning(
                    "⚠️ No coordinates found via unified manager, using fallback"
                )
                self.load_agent_coordinates_fallback()
            else:
                self.logger.warning(
                    "⚠️ Unified coordinate manager not available, using fallback"
                )
                self.load_agent_coordinates_fallback()

        except Exception as e:
            self.logger.error(f"❌ Failed to load coordinates via unified manager: {e}")
            self.load_agent_coordinates_fallback()

    def load_agent_coordinates_fallback(self):
        """Fallback coordinate loading method for compatibility"""
        config_path = Path("config/agents/coordinates.json")
        if not config_path.exists():
            self.logger.error("❌ cursor_agent_coords.json not found")
            return

        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)

            # Parse the nested cursor_agent_coords.json structure
            for key, value in config.items():
                if isinstance(value, dict):
                    for agent_key, agent_data in value.items():
                        if agent_key.startswith("Agent-"):
                            agent_id = agent_key
                            if (
                                "input_box" in agent_data
                                and "starter_location_box" in agent_data
                            ):
                                # Extract coordinates from the nested structure
                                input_coords = agent_data["input_box"]
                                if (
                                    isinstance(input_coords, dict)
                                    and "x" in input_coords
                                    and "y" in input_coords
                                ):
                                    self.agents[agent_id] = {
                                        "input_box": (
                                            input_coords["x"],
                                            input_coords["y"],
                                        ),
                                        "starter_location": agent_data[
                                            "starter_location_box"
                                        ],
                                    }

            self.logger.info(
                f"✅ Loaded {len(self.agents)} real agent coordinates via fallback"
            )
            for agent_id, coords in self.agents.items():
                self.logger.info(f"📍 {agent_id}: {coords['input_box']}")

        except Exception as e:
            self.logger.error(f"❌ Failed to load agent coordinates via fallback: {e}")

    def get_agent_coordinates(self, agent_id: str) -> Optional[Tuple[int, int]]:
        """Get coordinates for a specific agent"""
        if agent_id in self.agents:
            return self.agents[agent_id]["input_box"]
        return None

    def get_all_agents(self) -> List[str]:
        """Get list of all registered agent IDs"""
        return list(self.agents.keys())


class MessageDelivery:
    """Handles actual message delivery to agents"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def send_message(
        self, agent_id: str, coordinates: Tuple[int, int], message: str
    ) -> bool:
        """Send message to agent at specific coordinates"""
        try:
            self.logger.info(
                f"📤 Sending message to {agent_id} at {coordinates}: {message[:50]}..."
            )

            # Move to coordinates
            pyautogui.moveTo(coordinates[0], coordinates[1], duration=0.5)
            time.sleep(0.2)

            # Click to focus
            pyautogui.click()
            time.sleep(0.2)

            # Type message
            pyautogui.write(message)
            time.sleep(0.2)

            # Press Enter
            pyautogui.press("enter")
            time.sleep(0.5)

            self.logger.info(f"✅ Message sent successfully to {agent_id}")
            return True

        except Exception as e:
            self.logger.error(f"❌ Failed to send message to {agent_id}: {e}")
            return False


class BroadcastSystem:
    """Handles broadcasting messages to all agents"""

    def __init__(
        self, agent_registry: AgentRegistry, message_delivery: MessageDelivery
    ):
        self.agent_registry = agent_registry
        self.message_delivery = message_delivery
        self.input_buffer = InputBufferSystem()
        self.logger = logging.getLogger(__name__)
        self.broadcast_history = []

    def broadcast_message(self, message: str, priority: str = "normal") -> Dict:
        """Broadcast message to all agents using input buffering"""
        self.logger.info(f"🚀 BUFFERED BROADCASTING: {message}")
        self.logger.info(f"🔄 Priority: {priority.upper()}")
        self.logger.info(f"🔄 Method: Input Buffering (Conflict Prevention)")
        self.logger.info("=" * 60)

        # Buffer inputs for all agents
        agent_ids = self.agent_registry.get_all_agents()
        self.logger.info(
            f"📤 BUFFERED BROADCAST TO ALL {len(agent_ids)} AGENTS - Priority: {priority.upper()}"
        )

        for agent_id in agent_ids:
            self.input_buffer.add_input(agent_id, message, priority)

        buffer_status = self.input_buffer.get_buffer_status()
        self.logger.info(f"📥 Buffered {buffer_status['count']} inputs for broadcast")

        # Execute buffered inputs
        self.logger.info(f"🚀 Executing {buffer_status['count']} buffered inputs...")

        successful_sends = 0
        failed_sends = 0

        while True:
            input_item = self.input_buffer.get_next_input()
            if not input_item:
                break

            agent_id = input_item["agent_id"]
            coordinates = self.agent_registry.get_agent_coordinates(agent_id)

            if coordinates:
                if self.message_delivery.send_message(
                    agent_id, coordinates, input_item["message"]
                ):
                    successful_sends += 1
                    self.logger.info(
                        f"✅ Executed buffered input from {agent_id}: {input_item['message'][:50]}..."
                    )
                else:
                    failed_sends += 1
                    self.logger.error(
                        f"❌ Failed to execute buffered input from {agent_id}"
                    )
            else:
                failed_sends += 1
                self.logger.error(f"❌ No coordinates found for {agent_id}")

        self.logger.info(f"✅ Executed {buffer_status['count']} buffered inputs")

        # Summary
        success_rate = (
            (successful_sends / (successful_sends + failed_sends)) * 100
            if (successful_sends + failed_sends) > 0
            else 0
        )

        summary = {
            "successful_sends": successful_sends,
            "failed_sends": failed_sends,
            "success_rate": success_rate,
            "total_agents": len(agent_ids),
            "method": "Input Buffering (Conflict Prevention)",
        }

        self.logger.info("=" * 60)
        self.logger.info("🔄 **BUFFERED BROADCAST SUMMARY**")
        self.logger.info("=" * 60)
        self.logger.info(f"✅ Successful sends: {successful_sends}")
        self.logger.info(f"❌ Failed sends: {failed_sends}")
        self.logger.info(f"🔄 Success rate: {success_rate:.1f}%")
        self.logger.info(f"🎯 Total agents: {len(agent_ids)}")
        self.logger.info(f"🔄 Method: {summary['method']}")
        self.logger.info("=" * 60)

        if successful_sends > 0:
            self.logger.info(
                "🚀 **SUCCESSFUL BROADCAST! Some agents received the message!**"
            )
        else:
            self.logger.info("❌ **BROADCAST FAILED! No agents received the message.**")

        self.logger.info("=" * 60)

        # Record in history
        self.broadcast_history.append(
            {
                "timestamp": datetime.now().isoformat(),
                "message": message,
                "priority": priority,
                "summary": summary,
            }
        )

        return summary


class DevLog:
    """Development logging system"""

    def __init__(self):
        self.log_file = "agent_communication_devlog.json"
        self.logger = logging.getLogger(__name__)

    def save_log(self, data: Dict):
        """Save log data to file"""
        try:
            with open(self.log_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            self.logger.info(f"✅ DevLog saved to {self.log_file}")
        except Exception as e:
            self.logger.error(f"❌ Failed to save DevLog: {e}")


class RealAgentCommunicationSystem:
    """Main communication system class"""

    def __init__(self):
        self.setup_logging()
        self.logger = logging.getLogger(__name__)
        self.logger.info("🚀 Starting Enhanced Real Agent Communication System.")
        self.logger.info(
            "Make sure Discord/your applications are open at the target coordinates!"
        )
        self.logger.info("🔄 NEW: Input buffering system prevents message conflicts!")
        self.logger.info("Use --help for command-line options.")

        self.agent_registry = AgentRegistry()
        self.message_delivery = MessageDelivery()
        self.broadcast_system = BroadcastSystem(
            self.agent_registry, self.message_delivery
        )
        self.dev_log = DevLog()

    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler("agent_communication.log", encoding="utf-8"),
            ],
        )

    def show_status(self):
        """Show system status"""
        self.logger.info("📊 **SYSTEM STATUS**")
        self.logger.info("=" * 40)

        # Agent status
        agents = self.agent_registry.get_all_agents()
        self.logger.info(f"🎯 Registered Agents: {len(agents)}")
        for agent_id in agents:
            coords = self.agent_registry.get_agent_coordinates(agent_id)
            self.logger.info(f"  📍 {agent_id}: {coords}")

        # Buffer status
        buffer_status = self.broadcast_system.input_buffer.get_buffer_status()
        self.logger.info(f"🔄 Input Buffer: {buffer_status['count']} items")

        # Broadcast history
        if self.broadcast_system.broadcast_history:
            self.logger.info(
                f"📡 Recent Broadcasts: {len(self.broadcast_system.broadcast_history)}"
            )
            for broadcast in self.broadcast_system.broadcast_history[-3:]:
                self.logger.info(
                    f"  📅 {broadcast['timestamp']}: {broadcast['message'][:50]}..."
                )

    def test_buffering(self):
        """Test the input buffering system"""
        self.logger.info("🧪 **TESTING INPUT BUFFERING SYSTEM**")
        self.logger.info("=" * 50)

        test_messages = [
            "Test message 1 from buffering system",
            "Test message 2 from buffering system",
            "Test message 3 from buffering system",
            "Test message 4 from buffering system",
        ]

        # Buffer test messages
        for i, message in enumerate(test_messages):
            agent_id = f"Agent-{i+1}"
            self.broadcast_system.input_buffer.add_input(agent_id, message, "normal")

        # Execute buffered messages
        buffer_status = self.broadcast_system.input_buffer.get_buffer_status()
        self.logger.info(f"📥 Buffered {len(test_messages)} test messages")

        successful_sends = 0
        failed_sends = 0

        while True:
            input_item = self.broadcast_system.input_buffer.get_next_input()
            if not input_item:
                break

            agent_id = input_item["agent_id"]
            coordinates = self.agent_registry.get_agent_coordinates(agent_id)

            if coordinates:
                if self.message_delivery.send_message(
                    agent_id, coordinates, input_item["message"]
                ):
                    successful_sends += 1
                    self.logger.info(
                        f"✅ Executed buffered input from {agent_id}: {input_item['message'][:50]}..."
                    )
                else:
                    failed_sends += 1
            else:
                failed_sends += 1

        self.logger.info(f"✅ Executed {successful_sends} buffered inputs")

        # Save test results
        test_data = {
            "test_type": "input_buffering",
            "timestamp": datetime.now().isoformat(),
            "messages_sent": successful_sends,
            "messages_failed": failed_sends,
            "total_messages": len(test_messages),
        }
        self.dev_log.save_log(test_data)

    async def send_message_to_agent_with_line_breaks(
        self, agent_id: str, message: str, target_area: str = "input_box"
    ) -> bool:
        """Send message to a specific agent while preserving line breaks."""
        coordinates = self.agent_registry.get_agent_coordinates(agent_id)
        if not coordinates:
            self.logger.error(f"❌ Agent {agent_id} not found")
            return False

        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None, lambda: self.message_delivery.send_message(agent_id, coordinates, message)
        )
        return bool(result)

    async def send_message_to_all_agents(self, message: str, target_area: str = "input_box") -> bool:
        """Broadcast a message to all agents."""
        self.broadcast_system.broadcast_message(message)
        return True

    async def send_message_to_all_agents_with_line_breaks(
        self, message: str, target_area: str = "input_box"
    ) -> bool:
        """Broadcast a multiline message to all agents."""
        self.broadcast_system.broadcast_message(message)
        return True

    def get_agent_status(self) -> Dict[str, Dict[str, Any]]:
        """Get basic status information for all agents."""
        status: Dict[str, Dict[str, Any]] = {}
        for agent_id in self.agent_registry.get_all_agents():
            coords = self.agent_registry.get_agent_coordinates(agent_id)
            status[agent_id] = {
                "coordinates": {"x": coords[0], "y": coords[1]} if coords else None,
                "status": "active",
                "processing": False,
                "last_message": None,
            }
        return status

    def run(self):
        """Main run method"""
        parser = argparse.ArgumentParser(
            description="Real Agent Communication System - Source of Truth",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  # Show system status
  python real_agent_communication_system.py --status

  # Test input buffering system
  python real_agent_communication_system.py --test-buffering

  # Broadcast message to all agents
  python real_agent_communication_system.py --broadcast "Hello all agents!" --priority high

  # Send message to specific agent
  python real_agent_communication_system.py --agent Agent-1 --message "Hello Agent-1!"
            """,
        )

        parser.add_argument(
            "--broadcast", type=str, help="Broadcast message to all agents"
        )
        parser.add_argument("--agent", type=str, help="Target agent ID")
        parser.add_argument("--message", type=str, help="Message to send")
        parser.add_argument(
            "--priority",
            choices=["normal", "high"],
            default="normal",
            help="Message priority",
        )
        parser.add_argument("--status", action="store_true", help="Show system status")
        parser.add_argument(
            "--test-buffering", action="store_true", help="Test input buffering system"
        )

        args = parser.parse_args()

        if args.status:
            self.show_status()
        elif args.test_buffering:
            self.test_buffering()
        elif args.broadcast:
            result = self.broadcast_system.broadcast_message(
                args.broadcast, args.priority
            )
            self.dev_log.save_log(result)
        elif args.agent and args.message:
            coordinates = self.agent_registry.get_agent_coordinates(args.agent)
            if coordinates:
                success = self.message_delivery.send_message(
                    args.agent, coordinates, args.message
                )
                if success:
                    self.logger.info(f"✅ Message sent to {args.agent}")
                else:
                    self.logger.error(f"❌ Failed to send message to {args.agent}")
            else:
                self.logger.error(f"❌ Agent {args.agent} not found")
        else:
            parser.print_help()


def main():
    """Main entry point"""
    try:
        system = RealAgentCommunicationSystem()
        system.run()
    except KeyboardInterrupt:
        print("\n🛑 System interrupted by user")
    except Exception as e:
        print(f"❌ System error: {e}")
        logging.error(f"System error: {e}", exc_info=True)


if __name__ == "__main__":
    main()
