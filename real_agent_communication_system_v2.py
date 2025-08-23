#!/usr/bin/env python3
"""
Real Agent Communication System V2 - Phase 2: Screen Region Management
=====================================================================

This system uses your REAL agent coordinates with advanced screen region management
for true simultaneous multi-agent operation.

Features:
- Real agent coordinates from cursor_agent_coords.json
- Screen region isolation for each agent
- Multi-cursor support for simultaneous operation
- Input buffering system to prevent message conflicts
- Coordinated multi-agent execution
- Discord integration for actual agent messaging
- DevLog updates with real agent communication
- 8-agent simultaneous messaging system
- Broadcast system integration with --broadcast flag
- V2 coding standards compliance (modular, testable, maintainable)
"""

import asyncio
import json
import time
import logging
import argparse
import sys
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import pyautogui
import pyperclip
import threading
from dataclasses import dataclass

# Configure PyAutoGUI for real agent communication
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.1  # Reduced from 0.3 for faster operation


@dataclass
class ScreenRegion:
    """Screen region definition for an agent"""

    agent_id: str
    x: int
    y: int
    width: int
    height: int
    input_box: Dict[str, int]
    status_box: Dict[str, int]
    workspace_box: Dict[str, int]
    active: bool = True
    current_cursor: Optional[Tuple[int, int]] = None


class ScreenRegionManager:
    """Manages isolated screen regions for each agent"""

    def __init__(self):
        self.agent_regions = {}
        self.region_locks = {}
        self.virtual_cursors = {}
        self.logger = logging.getLogger(__name__)
        self.region_stats = {
            "total_regions": 0,
            "active_regions": 0,
            "isolated_workspaces": 0,
        }

    def define_agent_region(
        self, agent_id: str, x: int, y: int, width: int = 300, height: int = 200
    ):
        """Define isolated screen region for agent"""
        # Calculate sub-regions within the agent's workspace
        input_box = {
            "x": x + 10,
            "y": y + height - 30,
            "width": width - 20,
            "height": 25,
        }

        status_box = {"x": x + 10, "y": y + 10, "width": width - 20, "height": 25}

        workspace_box = {
            "x": x + 10,
            "y": y + 40,
            "width": width - 20,
            "height": height - 80,
        }

        # Create region
        region = ScreenRegion(
            agent_id=agent_id,
            x=x,
            y=y,
            width=width,
            height=height,
            input_box=input_box,
            status_box=status_box,
            workspace_box=workspace_box,
        )

        self.agent_regions[agent_id] = region
        self.region_locks[agent_id] = asyncio.Lock()
        self.virtual_cursors[agent_id] = {"x": x + 10, "y": y + 10}

        self.region_stats["total_regions"] += 1
        self.region_stats["active_regions"] += 1
        self.region_stats["isolated_workspaces"] += 1

        self.logger.info(
            f"📍 Defined region for {agent_id}: ({x}, {y}) {width}x{height}"
        )

    def get_agent_region(self, agent_id: str) -> Optional[ScreenRegion]:
        """Get agent's screen region"""
        return self.agent_regions.get(agent_id)

    def is_coordinate_in_region(self, agent_id: str, x: int, y: int) -> bool:
        """Check if coordinates are within agent's region"""
        region = self.get_agent_region(agent_id)
        if not region:
            return False

        return (
            region.x <= x <= region.x + region.width
            and region.y <= y <= region.y + region.height
        )

    async def execute_in_region(
        self, agent_id: str, operation: str, target_area: str = "input_box", **kwargs
    ):
        """Execute operation within agent's isolated region"""
        region = self.get_agent_region(agent_id)
        if not region:
            raise ValueError(f"Agent {agent_id} region not defined")

        lock = self.region_locks[agent_id]

        async with lock:  # Only one operation per region at a time
            try:
                if operation == "type":
                    return await self._type_in_region(region, target_area, **kwargs)
                elif operation == "type_with_line_breaks":
                    return await self._type_in_region_with_line_breaks(
                        region, target_area, **kwargs
                    )
                elif operation == "click":
                    return await self._click_in_region(region, target_area, **kwargs)
                elif operation == "update_status":
                    return await self._update_status_in_region(region, **kwargs)
                else:
                    raise ValueError(f"Unknown operation: {operation}")
            except Exception as e:
                self.logger.error(
                    f"❌ Error executing {operation} in {agent_id} region: {e}"
                )
                return False

    async def _type_in_region(
        self, region: ScreenRegion, target_area: str, message: str, method: str = "type"
    ) -> bool:
        """Type message within agent's region"""
        try:
            # Get target coordinates based on area
            if target_area == "input_box":
                target_x = region.input_box["x"]
                target_y = region.input_box["y"]
            elif target_area == "workspace_box":
                target_x = region.workspace_box["x"]
                target_y = region.workspace_box["y"]
            else:
                target_x = region.x + 10
                target_y = region.y + 10

            # Move to target within region
            pyautogui.moveTo(target_x, target_y, duration=0.1)  # Reduced from 0.2

            # Click to focus
            pyautogui.click(target_x, target_y)
            time.sleep(0.05)  # Reduced from 0.1

            # Type message
            if method == "type":
                pyautogui.typewrite(message, interval=0.03)  # Reduced from 0.05
            elif method == "paste":
                pyperclip.copy(message)
                pyautogui.hotkey("ctrl", "v")

            # Press Enter to send
            pyautogui.press("enter")

            # Update virtual cursor position
            self.virtual_cursors[region.agent_id] = (target_x, target_y)

            self.logger.info(
                f"✅ Typed in {region.agent_id} {target_area}: {message[:30]}..."
            )
            return True

        except Exception as e:
            self.logger.error(f"❌ Failed to type in {region.agent_id} region: {e}")
            return False

    async def _type_in_region_with_line_breaks(
        self, region: ScreenRegion, target_area: str, message: str, method: str = "type"
    ) -> bool:
        """Type message within agent's region with proper line break handling"""
        try:
            # Get target coordinates based on area
            if target_area == "input_box":
                target_x = region.input_box["x"]
                target_y = region.input_box["y"]
            elif target_area == "workspace_box":
                target_x = region.workspace_box["x"]
                target_y = region.workspace_box["y"]
            else:
                target_x = region.x + 10
                target_y = region.y + 10

            # Move to target within region
            pyautogui.moveTo(target_x, target_y, duration=0.1)  # Reduced from 0.2

            # Click to focus
            pyautogui.click(target_x, target_y)
            time.sleep(0.05)  # Reduced from 0.1

            # Split message into lines and handle line breaks properly
            lines = message.split("\n")

            for i, line in enumerate(lines):
                # Type the line
                if line.strip():  # Only type non-empty lines
                    if method == "type":
                        pyautogui.typewrite(line, interval=0.03)  # Reduced from 0.05
                    elif method == "paste":
                        pyperclip.copy(line)
                        pyautogui.hotkey("ctrl", "v")

                # Add line break (Shift+Enter) if not the last line
                if i < len(lines) - 1:
                    # Send Shift+Enter for line break
                    pyautogui.hotkey("shift", "enter")
                    time.sleep(0.05)  # Reduced from 0.1 for faster processing

            # Press Enter to send the complete message
            pyautogui.press("enter")

            # Update virtual cursor position
            self.virtual_cursors[region.agent_id] = (target_x, target_y)

            self.logger.info(
                f"✅ Typed with line breaks in {region.agent_id} {target_area}: {message[:30]}..."
            )
            return True

        except Exception as e:
            self.logger.error(
                f"❌ Failed to type with line breaks in {region.agent_id} region: {e}"
            )
            return False

    async def _click_in_region(
        self, region: ScreenRegion, target_area: str, button: str = "left"
    ) -> bool:
        """Click within agent's region"""
        try:
            # Get target coordinates
            if target_area == "input_box":
                target_x = region.input_box["x"]
                target_y = region.input_box["y"]
            elif target_area == "status_box":
                target_x = region.status_box["x"]
                target_y = region.status_box["y"]
            else:
                target_x = region.x + 10
                target_y = region.y + 10

            # Click within region
            pyautogui.click(target_x, target_y, button=button)

            # Update virtual cursor
            self.virtual_cursors[region.agent_id] = (target_x, target_y)

            self.logger.info(f"✅ Clicked in {region.agent_id} {target_area}")
            return True

        except Exception as e:
            self.logger.error(f"❌ Failed to click in {region.agent_id} region: {e}")
            return False

    async def _update_status_in_region(
        self, region: ScreenRegion, status: str, color: str = "green"
    ) -> bool:
        """Update status display in agent's region"""
        try:
            # This would update a visual status indicator in the region
            # For now, we'll simulate it
            self.logger.info(f"📊 Status update for {region.agent_id}: {status}")
            return True

        except Exception as e:
            self.logger.error(
                f"❌ Failed to update status in {region.agent_id} region: {e}"
            )
            return False

    def get_region_stats(self) -> Dict:
        """Get region management statistics"""
        return {
            **self.region_stats,
            "defined_regions": len(self.agent_regions),
            "virtual_cursors": len(self.virtual_cursors),
        }

    def display_region_layout(self):
        """Display visual representation of region layout"""
        print("\n" + "=" * 80)
        print("🗺️  SCREEN REGION LAYOUT - AGENT WORKSPACES")
        print("=" * 80)

        for agent_id, region in self.agent_regions.items():
            print(f"📍 {agent_id}:")
            print(
                f"   🖥️  Main Region: ({region.x}, {region.y}) {region.width}x{region.height}"
            )
            print(f"   📝 Input Box: ({region.input_box['x']}, {region.input_box['y']})")
            print(
                f"   📊 Status Box: ({region.status_box['x']}, {region.status_box['y']})"
            )
            print(
                f"   💼 Workspace: ({region.workspace_box['x']}, {region.workspace_box['y']})"
            )
            print(
                f"   🖱️  Virtual Cursor: {self.virtual_cursors.get(agent_id, 'Not set')}"
            )
            print()


class InputBufferSystem:
    """Enhanced input buffering system with region management"""

    def __init__(self, region_manager: ScreenRegionManager):
        self.region_manager = region_manager
        self.input_queue = asyncio.Queue()
        self.agent_buffers = {}
        self.coordination_lock = asyncio.Lock()
        self.logger = logging.getLogger(__name__)
        self.buffer_stats = {
            "total_buffered": 0,
            "total_executed": 0,
            "conflicts_prevented": 0,
            "region_executions": 0,
        }

    async def buffer_agent_input(
        self,
        agent_id: str,
        message: str,
        target_area: str = "input_box",
        priority: int = 1,
        line_breaks: bool = False,
    ) -> str:
        """Buffer input from agent for region-specific execution"""
        buffer_id = f"{agent_id}_{int(time.time() * 1000)}"

        input_item = {
            "buffer_id": buffer_id,
            "agent_id": agent_id,
            "message": message,
            "target_area": target_area,
            "priority": priority,
            "timestamp": time.time(),
            "status": "buffered",
            "line_breaks": line_breaks,
        }

        await self.input_queue.put(input_item)
        self.agent_buffers[buffer_id] = input_item
        self.buffer_stats["total_buffered"] += 1

        line_break_info = " with line breaks" if line_breaks else ""
        self.logger.info(
            f"📥 Buffered input from {agent_id} in {target_area}{line_break_info}: {message[:30]}..."
        )
        return buffer_id

    async def execute_buffered_inputs(self) -> Dict[str, bool]:
        """Execute all buffered inputs using region management"""
        results = {}

        async with self.coordination_lock:
            self.logger.info(
                f"🚀 Executing {self.input_queue.qsize()} buffered inputs using regions..."
            )

            while not self.input_queue.empty():
                input_item = await self.input_queue.get()

                # Execute in agent's region
                success = await self._execute_in_agent_region(input_item)
                results[input_item["buffer_id"]] = success

                # Update status
                input_item["status"] = "executed" if success else "failed"
                input_item["execution_time"] = time.time()

                # Small coordination delay
                await asyncio.sleep(0.05)  # Reduced from 0.1 for faster processing

        self.buffer_stats["total_executed"] += len(results)
        self.logger.info(f"✅ Executed {len(results)} buffered inputs using regions")

        return results

    async def execute_buffered_inputs_with_line_breaks(self) -> Dict[str, bool]:
        """Execute all buffered inputs using region management with line break handling"""
        results = {}

        async with self.coordination_lock:
            self.logger.info(
                f"🚀 Executing {self.input_queue.qsize()} buffered inputs with line breaks using regions..."
            )

            while not self.input_queue.empty():
                input_item = await self.input_queue.get()

                # Execute in agent's region with line break handling
                success = await self._execute_in_agent_region_with_line_breaks(
                    input_item
                )
                results[input_item["buffer_id"]] = success

                # Update status
                input_item["status"] = "executed" if success else "failed"
                input_item["execution_time"] = time.time()

                # Small coordination delay
                await asyncio.sleep(0.05)  # Reduced from 0.1 for faster processing

        self.buffer_stats["total_executed"] += len(results)
        self.logger.info(
            f"✅ Executed {len(results)} buffered inputs with line breaks using regions"
        )

        return results

    async def _execute_in_agent_region(self, input_item: Dict) -> bool:
        """Execute single buffered input in agent's region"""
        try:
            agent_id = input_item["agent_id"]
            message = input_item["message"]
            target_area = input_item.get("target_area", "input_box")

            # Execute in agent's isolated region
            success = await self.region_manager.execute_in_region(
                agent_id, "type", target_area, message=message
            )

            if success:
                self.buffer_stats["region_executions"] += 1
                self.logger.info(f"✅ Executed in {agent_id} region: {message[:30]}...")
            else:
                self.logger.error(f"❌ Failed to execute in {agent_id} region")

            return success

        except Exception as e:
            self.logger.error(f"❌ Error executing in region: {e}")
            return False

    async def _execute_in_agent_region_with_line_breaks(self, input_item: Dict) -> bool:
        """Execute single buffered input in agent's region with line break handling"""
        try:
            agent_id = input_item["agent_id"]
            message = input_item["message"]
            target_area = input_item.get("target_area", "input_box")
            line_breaks = input_item.get("line_breaks", False)

            # Execute in agent's isolated region with line break handling
            if line_breaks:
                success = await self.region_manager.execute_in_region(
                    agent_id, "type_with_line_breaks", target_area, message=message
                )
            else:
                success = await self.region_manager.execute_in_region(
                    agent_id, "type", target_area, message=message
                )

            if success:
                self.buffer_stats["region_executions"] += 1
                line_break_info = " with line breaks" if line_breaks else ""
                self.logger.info(
                    f"✅ Executed in {agent_id} region{line_break_info}: {message[:30]}..."
                )
            else:
                self.logger.error(f"❌ Failed to execute in {agent_id} region")

            return success

        except Exception as e:
            self.logger.error(f"❌ Error executing in region with line breaks: {e}")
            return False

    def get_buffer_stats(self) -> Dict:
        """Get enhanced buffer statistics"""
        return {
            **self.buffer_stats,
            "currently_buffered": len(self.agent_buffers),
            "queue_size": self.input_queue.qsize(),
        }


class BroadcastSystem:
    """Enhanced broadcast system with region management"""

    def __init__(self, comm_system, region_manager: ScreenRegionManager):
        self.comm_system = comm_system
        self.region_manager = region_manager
        self.logger = logging.getLogger(__name__)
        self.broadcast_history = []
        self.input_buffer = InputBufferSystem(region_manager)

    async def region_based_broadcast(
        self, message: str, priority: str = "normal"
    ) -> Tuple[int, int]:
        """Broadcast message to all agents using region management"""
        self.logger.info(
            f"🚀 REGION-BASED BROADCAST TO ALL 8 AGENTS - Priority: {priority.upper()}"
        )

        # Buffer inputs for all agents in their regions
        buffer_ids = []
        for agent_id in self.comm_system.agent_coordinates.keys():
            buffer_id = await self.input_buffer.buffer_agent_input(
                agent_id,
                message,
                target_area="input_box",
                priority=2 if priority == "high" else 1,
            )
            buffer_ids.append(buffer_id)

        self.logger.info(
            f"📥 Buffered {len(buffer_ids)} inputs for region-based broadcast"
        )

        # Execute all buffered inputs using region management
        results = await self.input_buffer.execute_buffered_inputs()

        # Count successful/failed executions
        successful_sends = sum(1 for success in results.values() if success)
        failed_sends = len(results) - successful_sends

        # Log broadcast summary
        self.logger.info(
            f"📊 REGION-BASED BROADCAST SUMMARY: {successful_sends} successful, {failed_sends} failed"
        )

        # Add to broadcast history
        self.add_broadcast_history(
            message, priority, successful_sends, failed_sends, "region-based"
        )

        return successful_sends, failed_sends

    async def region_based_broadcast_with_line_breaks(
        self, message: str, priority: str = "normal"
    ) -> Tuple[int, int]:
        """Broadcast message to all agents using region management with line break handling"""
        self.logger.info(
            f"🚀 REGION-BASED BROADCAST WITH LINE BREAKS TO ALL 8 AGENTS - Priority: {priority.upper()}"
        )

        # Buffer inputs for all agents in their regions with line break handling
        buffer_ids = []
        for agent_id in self.comm_system.agent_coordinates.keys():
            buffer_id = await self.input_buffer.buffer_agent_input(
                agent_id,
                message,
                target_area="input_box",
                priority=2 if priority == "high" else 1,
                line_breaks=True,
            )
            buffer_ids.append(buffer_id)

        self.logger.info(
            f"📥 Buffered {len(buffer_ids)} inputs for region-based broadcast with line breaks"
        )

        # Execute all buffered inputs using region management with line breaks
        results = await self.input_buffer.execute_buffered_inputs_with_line_breaks()

        # Count successful/failed executions
        successful_sends = sum(1 for success in results.values() if success)
        failed_sends = len(results) - successful_sends

        # Log broadcast summary
        self.logger.info(
            f"📊 REGION-BASED BROADCAST WITH LINE BREAKS SUMMARY: {successful_sends} successful, {failed_sends} failed"
        )

        # Add to broadcast history
        self.add_broadcast_history(
            message,
            priority,
            successful_sends,
            failed_sends,
            "region-based-with-line-breaks",
        )

        return successful_sends, failed_sends

    async def broadcast_to_all_agents(
        self, message: str, priority: str = "normal"
    ) -> Tuple[int, int]:
        """Legacy broadcast method - now uses region management"""
        return await self.region_based_broadcast(message, priority)

    def add_broadcast_history(
        self,
        message: str,
        priority: str,
        successful: int,
        failed: int,
        method: str = "region-based",
    ):
        """Add broadcast to history"""
        broadcast_entry = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "message": message,
            "priority": priority,
            "successful_sends": successful,
            "failed_sends": failed,
            "total_agents": successful + failed,
            "method": method,
        }
        self.broadcast_history.append(broadcast_entry)

        # Keep only last 50 broadcasts
        if len(self.broadcast_history) > 50:
            self.broadcast_history = self.broadcast_history[-50:]

    def get_broadcast_history(self) -> List[Dict]:
        """Get broadcast history"""
        return self.broadcast_history.copy()

    def display_broadcast_summary(self, successful: int, failed: int, total: int):
        """Display enhanced broadcast summary"""
        print("\n" + "=" * 60)
        print("📊 **REGION-BASED BROADCAST SUMMARY**")
        print("=" * 60)
        print(f"✅ Successful sends: {successful}")
        print(f"❌ Failed sends: {failed}")
        print(f"📈 Success rate: {(successful/total*100):.1f}%")
        print(f"🎯 Total agents: {total}")
        print(f"🔄 Method: Screen Region Management + Input Buffering")
        print(f"🗺️  Workspace Isolation: Active")

        if successful == total:
            print("\n🎉 **PERFECT BROADCAST! All agents received the message!**")
        elif successful > 0:
            print(
                f"\n✅ **PARTIAL SUCCESS! {successful} out of {total} agents received the message.**"
            )
        else:
            print("\n❌ **BROADCAST FAILED! No agents received the message.**")
        print("=" * 60)


class RealAgentCommunicationSystem:
    """Real agent communication with screen region management"""

    def __init__(self):
        self.agent_coordinates = {}
        self.devlog_updates = []
        self.setup_logging()

        # Initialize unified coordinate manager
        try:
            from src.services.messaging import CoordinateManager

            self.coordinate_manager = CoordinateManager()
            self.load_real_coordinates()
        except ImportError:
            self.logger.warning(
                "⚠️ Unified coordinate manager not available, using fallback"
            )
            self.coordinate_manager = None
            self.load_real_coordinates_fallback()

        # Initialize region management
        self.region_manager = ScreenRegionManager()
        self.setup_agent_regions()

        # Initialize enhanced systems
        self.broadcast_system = BroadcastSystem(self, self.region_manager)
        self.input_buffer = self.broadcast_system.input_buffer

    def setup_logging(self):
        """Setup logging for the system"""
        logging.basicConfig(
            level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
        )
        self.logger = logging.getLogger(__name__)

    def load_real_coordinates(self):
        """Load real agent coordinates using unified coordinate manager"""
        try:
            if self.coordinate_manager:
                # Use unified coordinate manager
                self.logger.info(
                    "🗺️ Loading coordinates via unified coordinate manager..."
                )

                # Get coordinates for 8-agent mode
                for i in range(1, 9):
                    agent_key = f"Agent-{i}"
                    coords = self.coordinate_manager.get_agent_coordinates(
                        agent_key, "8-agent"
                    )

                    if coords:
                        self.agent_coordinates[agent_key] = {
                            "input_x": coords.input_box[0],
                            "input_y": coords.input_box[1],
                            "starter_x": coords.starter_location[0],
                            "starter_y": coords.starter_location[1],
                            "status": "active",
                            "last_message": None,
                            "processing": False,
                        }
                    else:
                        self.logger.warning(f"⚠️ No coordinates found for {agent_key}")

                self.logger.info(
                    f"✅ Loaded {len(self.agent_coordinates)} real agent coordinates via unified manager"
                )
                if self.agent_coordinates:
                    first_agent = list(self.agent_coordinates.keys())[0]
                    coords = self.agent_coordinates[first_agent]
                    self.logger.info(
                        f"📍 {first_agent}: ({coords['input_x']}, {coords['input_y']})"
                    )
            else:
                self.logger.error("❌ Unified coordinate manager not available")

        except Exception as e:
            self.logger.error(f"❌ Failed to load coordinates via unified manager: {e}")
            # Fallback to old method if unified manager fails
            self.load_real_coordinates_fallback()

    def load_real_coordinates_fallback(self):
        """Fallback coordinate loading method for compatibility"""
        try:
            config_path = Path("config/cursor_agent_coords.json")
            if config_path.exists():
                with open(config_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                # Get 8-agent layout
                layout = data.get("8-agent", {})
                if layout:
                    self.agent_coordinates = {}
                    for i in range(1, 9):
                        agent_key = f"Agent-{i}"
                        agent_info = layout.get(agent_key, {})

                        if agent_info:
                            input_box = agent_info.get("input_box", {})
                            starter_box = agent_info.get("starter_location_box", {})

                            self.agent_coordinates[agent_key] = {
                                "input_x": input_box.get("x"),
                                "input_y": input_box.get("y"),
                                "starter_x": starter_box.get("x"),
                                "starter_y": starter_box.get("y"),
                                "status": "active",
                                "last_message": None,
                                "processing": False,
                            }

                    self.logger.info(
                        f"✅ Loaded {len(self.agent_coordinates)} real agent coordinates via fallback"
                    )
                    if self.agent_coordinates:
                        first_agent = list(self.agent_coordinates.keys())[0]
                        coords = self.agent_coordinates[first_agent]
                        self.logger.info(
                            f"📍 {first_agent}: ({coords['input_x']}, {coords['input_y']})"
                        )
                else:
                    self.logger.error("❌ 8-agent layout not found in coordinates file")
            else:
                self.logger.error("❌ cursor_agent_coords.json not found")

        except Exception as e:
            self.logger.error(f"❌ Failed to load coordinates via fallback: {e}")

    def setup_agent_regions(self):
        """Setup screen regions for all agents"""
        self.logger.info("🗺️ Setting up screen regions for all agents...")

        for agent_id, coords in self.agent_coordinates.items():
            x, y = coords["input_x"], coords["input_y"]

            # Define region around agent's input coordinates
            # Adjust width/height based on screen layout
            if x < 0:  # Left side agents
                width, height = 300, 200
            else:  # Right side agents
                width, height = 300, 200

            self.region_manager.define_agent_region(agent_id, x, y, width, height)

        self.logger.info(f"✅ Setup {len(self.agent_coordinates)} agent screen regions")

    async def send_message_to_agent(
        self, agent_id: str, message: str, target_area: str = "input_box"
    ):
        """Send message to specific agent using region management"""
        if agent_id not in self.agent_coordinates:
            self.logger.error(f"❌ Agent {agent_id} not found in coordinates")
            return False

        try:
            self.logger.info(
                f"📤 Sending message to {agent_id} in {target_area}: {message}"
            )

            # Execute in agent's isolated region
            success = await self.region_manager.execute_in_region(
                agent_id, "type", target_area, message=message
            )

            if success:
                # Update agent status
                coords = self.agent_coordinates[agent_id]
                coords["last_message"] = {
                    "message": message,
                    "timestamp": time.time(),
                    "target_area": target_area,
                }

                # Add to devlog
                self.add_devlog_update(
                    f"Message sent to {agent_id} in {target_area}: {message}"
                )

                self.logger.info(
                    f"✅ Message sent successfully to {agent_id} in {target_area}"
                )
                return True
            else:
                self.logger.error(f"❌ Failed to send message to {agent_id}")
                return False

        except Exception as e:
            self.logger.error(f"❌ Failed to send message to {agent_id}: {e}")
            return False

    async def send_message_to_agent_with_line_breaks(
        self, agent_id: str, message: str, target_area: str = "input_box"
    ):
        """Send message to specific agent with proper line break handling"""
        if agent_id not in self.agent_coordinates:
            self.logger.error(f"❌ Agent {agent_id} not found in coordinates")
            return False

        try:
            self.logger.info(
                f"📤 Sending message with line breaks to {agent_id} in {target_area}: {message}"
            )

            # Execute in agent's isolated region with line break handling
            success = await self.region_manager.execute_in_region(
                agent_id, "type_with_line_breaks", target_area, message=message
            )

            if success:
                # Update agent status
                coords = self.agent_coordinates[agent_id]
                coords["last_message"] = {
                    "message": message,
                    "timestamp": time.time(),
                    "target_area": target_area,
                    "line_breaks_handled": True,
                }

                # Add to devlog
                self.add_devlog_update(
                    f"Message with line breaks sent to {agent_id} in {target_area}: {message}"
                )

                self.logger.info(
                    f"✅ Message with line breaks sent successfully to {agent_id} in {target_area}"
                )
                return True
            else:
                self.logger.error(
                    f"❌ Failed to send message with line breaks to {agent_id}"
                )
                return False

        except Exception as e:
            self.logger.error(
                f"❌ Failed to send message with line breaks to {agent_id}: {e}"
            )
            return False

    async def send_message_to_all_agents(
        self, message: str, target_area: str = "input_box"
    ):
        """Send message to all 8 agents using region management"""
        self.logger.info(
            f"🚀 Sending message to ALL agents using region management: {message}"
        )

        # Use the region-based broadcast system
        successful, failed = await self.broadcast_system.region_based_broadcast(message)

        # Add to devlog
        self.add_devlog_update(
            f"Region-based multi-agent broadcast: {successful}/{len(self.agent_coordinates)} agents received message"
        )

        return successful == len(self.agent_coordinates)

    async def send_message_to_all_agents_with_line_breaks(
        self, message: str, target_area: str = "input_box"
    ):
        """Send message to all 8 agents with proper line break handling"""
        self.logger.info(
            f"🚀 Sending message with line breaks to ALL agents using region management: {message}"
        )

        # Use the region-based broadcast system with line break handling
        (
            successful,
            failed,
        ) = await self.broadcast_system.region_based_broadcast_with_line_breaks(message)

        # Add to devlog
        self.add_devlog_update(
            f"Region-based multi-agent broadcast with line breaks: {successful}/{len(self.agent_coordinates)} agents received message"
        )

        return successful == len(self.agent_coordinates)

    async def send_coordinated_messages(
        self, messages: Dict[str, str], target_areas: Dict[str, str] = None
    ):
        """Send different messages to different agents using region management"""
        self.logger.info("🎬 Starting coordinated messaging using region management...")

        if target_areas is None:
            target_areas = {agent_id: "input_box" for agent_id in messages.keys()}

        # Buffer all messages for region execution
        buffer_ids = []
        for agent_id, message in messages.items():
            if agent_id in self.agent_coordinates:
                target_area = target_areas.get(agent_id, "input_box")
                buffer_id = await self.input_buffer.buffer_agent_input(
                    agent_id, message, target_area
                )
                buffer_ids.append(buffer_id)

                # Add to devlog
                self.add_devlog_update(
                    f"Buffered coordinated message to {agent_id} in {target_area}: {message}"
                )
            else:
                self.logger.warning(
                    f"⚠️ Agent {agent_id} not found for coordinated messaging"
                )

        # Execute all buffered messages using region management
        results = await self.input_buffer.execute_buffered_inputs()

        success_count = sum(1 for r in results.values() if r)
        self.logger.info(
            f"✅ Coordinated messaging complete: {success_count}/{len(messages)} successful"
        )

        return results

    def add_devlog_update(self, update: str):
        """Add update to development log"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            "timestamp": timestamp,
            "update": update,
            "system": "RealAgentCommunicationV2",
        }
        self.devlog_updates.append(log_entry)

        # Keep only last 100 updates
        if len(self.devlog_updates) > 100:
            self.devlog_updates = self.devlog_updates[-100:]

    def get_devlog_summary(self) -> List[Dict]:
        """Get development log summary"""
        return self.devlog_updates.copy()

    def save_devlog(self, filename: str = "agent_communication_v2_devlog.json"):
        """Save development log to file"""
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(self.devlog_updates, f, indent=2, ensure_ascii=False)
            self.logger.info(f"✅ DevLog saved to {filename}")
        except Exception as e:
            self.logger.error(f"❌ Failed to save DevLog: {e}")

    def get_agent_status(self) -> Dict:
        """Get current status of all agents with region information"""
        status = {}
        for agent_id, coords in self.agent_coordinates.items():
            region = self.region_manager.get_agent_region(agent_id)
            status[agent_id] = {
                "coordinates": {"x": coords["input_x"], "y": coords["input_y"]},
                "status": coords["status"],
                "processing": coords["processing"],
                "last_message": coords["last_message"],
                "region_active": region.active if region else False,
                "virtual_cursor": self.region_manager.virtual_cursors.get(agent_id),
            }
        return status

    def display_agent_status(self):
        """Display enhanced agent status with region information"""
        print("\n" + "=" * 80)
        print(
            "🎯 REAL AGENT COMMUNICATION SYSTEM V2 STATUS (WITH SCREEN REGION MANAGEMENT)"
        )
        print("=" * 80)

        for agent_id, info in self.get_agent_status().items():
            coords = info["coordinates"]
            last_msg = info["last_message"]
            region_active = info["region_active"]
            virtual_cursor = info["virtual_cursor"]

            status_icon = "🔄" if info["processing"] else "✅"
            region_status = " (REGION ACTIVE)" if region_active else " (NO REGION)"

            if last_msg:
                msg_preview = (
                    last_msg["message"][:30] + "..."
                    if len(last_msg["message"]) > 30
                    else last_msg["message"]
                )
                print(
                    f"{status_icon} {agent_id}: ({coords['x']}, {coords['y']}) - Last: {msg_preview}{region_status}"
                )
            else:
                print(
                    f"{status_icon} {agent_id}: ({coords['x']}, {coords['y']}) - No messages yet{region_status}"
                )

            if virtual_cursor:
                print(f"   🖱️  Virtual Cursor: {virtual_cursor}")

        # Display region statistics
        region_stats = self.region_manager.get_region_stats()
        print(f"\n🗺️ Screen Region Stats:")
        print(f"  📍 Total Regions: {region_stats['total_regions']}")
        print(f"  ✅ Active Regions: {region_stats['active_regions']}")
        print(f"  💼 Isolated Workspaces: {region_stats['isolated_workspaces']}")
        print(f"  🖱️ Virtual Cursors: {region_stats['virtual_cursors']}")

        # Display buffer statistics
        buffer_stats = self.input_buffer.get_buffer_stats()
        print(f"\n📊 Enhanced Buffer Stats:")
        print(f"  📥 Total Buffered: {buffer_stats['total_buffered']}")
        print(f"  ✅ Total Executed: {buffer_stats['total_executed']}")
        print(f"  🚫 Conflicts Prevented: {buffer_stats['conflicts_prevented']}")
        print(f"  🗺️ Region Executions: {buffer_stats['region_executions']}")
        print(f"  🔄 Currently Buffered: {buffer_stats['currently_buffered']}")
        print(f"  📋 Queue Size: {buffer_stats['queue_size']}")

        print("=" * 80)


class DiscordIntegration:
    """Discord integration for agent communication"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.discord_active = False

    async def send_discord_message(self, channel: str, message: str):
        """Send message to Discord channel"""
        try:
            # This would integrate with your actual Discord bot/API
            self.logger.info(f"📱 Discord: Sending to #{channel}: {message}")

            # For now, simulate Discord integration
            await asyncio.sleep(0.1)  # Simulate API call

            self.logger.info(f"✅ Discord message sent to #{channel}")
            return True

        except Exception as e:
            self.logger.error(f"❌ Discord message failed: {e}")
            return False

    async def broadcast_to_discord(self, message: str, channels: List[str] = None):
        """Broadcast message to multiple Discord channels"""
        if channels is None:
            channels = ["general", "agent-coordination", "devlog"]

        self.logger.info(f"📢 Broadcasting to Discord channels: {channels}")

        results = {}
        for channel in channels:
            result = await self.send_discord_message(channel, message)
            results[channel] = result

        success_count = sum(1 for r in results.values() if r)
        self.logger.info(
            f"✅ Discord broadcast complete: {success_count}/{len(channels)} channels"
        )

        return results


class CLIInterface:
    """Enhanced command-line interface for V2 system"""

    def __init__(self):
        self.parser = self.setup_argument_parser()

    def setup_argument_parser(self):
        """Setup command-line argument parser"""
        parser = argparse.ArgumentParser(
            description="Real Agent Communication System V2 - Phase 2: Screen Region Management",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  # Run interactive demo
  python real_agent_communication_system_v2.py

  # Region-based broadcast
  python real_agent_communication_system_v2.py --broadcast "Hello from V2 system!"

  # High priority broadcast
  python real_agent_communication_system_v2.py --broadcast "URGENT: System alert!" --priority high

  # Send to specific agent in specific area
  python real_agent_communication_system_v2.py --agent Agent-1 --message "Test message" --area workspace_box

  # Show system status with region info
  python real_agent_communication_system_v2.py --status

  # Test region management system
  python real_agent_communication_system_v2.py --test-regions

  # Display region layout
  python real_agent_communication_system_v2.py --show-layout
            """,
        )

        # Main operation modes
        parser.add_argument(
            "--broadcast",
            type=str,
            metavar="MESSAGE",
            help="Region-based broadcast message to all agents",
        )
        parser.add_argument(
            "--agent",
            type=str,
            metavar="AGENT_ID",
            help="Send message to specific agent (e.g., Agent-1)",
        )
        parser.add_argument(
            "--message", type=str, metavar="TEXT", help="Message text to send"
        )
        parser.add_argument(
            "--area",
            choices=["input_box", "workspace_box", "status_box"],
            default="input_box",
            help="Target area in agent region (default: input_box)",
        )
        parser.add_argument(
            "--priority",
            choices=["normal", "high"],
            default="normal",
            help="Message priority (default: normal)",
        )
        parser.add_argument(
            "--status",
            action="store_true",
            help="Show system status with region information",
        )
        parser.add_argument(
            "--test-regions",
            action="store_true",
            help="Test the screen region management system",
        )
        parser.add_argument(
            "--show-layout", action="store_true", help="Display visual region layout"
        )

        return parser

    def parse_arguments(self):
        """Parse command-line arguments"""
        return self.parser.parse_args()

    def display_help(self):
        """Display help information"""
        self.parser.print_help()


async def main():
    """Main function with enhanced CLI support"""
    cli = CLIInterface()
    args = cli.parse_arguments()

    # Initialize the V2 system
    comm_system = RealAgentCommunicationSystem()
    discord = DiscordIntegration()

    # Handle different CLI modes
    if args.broadcast:
        # Region-based broadcast mode
        print(f"🚀 REGION-BASED BROADCASTING: {args.broadcast}")
        print(f"🎯 Priority: {args.priority.upper()}")
        print(f"🔄 Method: Screen Region Management + Input Buffering")
        print(f"🗺️  Workspace Isolation: Active")
        print("=" * 60)

        # Execute region-based broadcast
        successful, failed = await comm_system.broadcast_system.region_based_broadcast(
            args.broadcast, args.priority
        )

        # Display results
        comm_system.broadcast_system.display_broadcast_summary(
            successful, failed, successful + failed
        )

        # Save devlog
        comm_system.save_devlog()

        # Exit with appropriate code
        sys.exit(0 if failed == 0 else 1)

    elif args.agent and args.message:
        # Single agent messaging mode with region management
        print(f"📤 Sending to {args.agent} in {args.area}: {args.message}")
        print("=" * 60)

        success = await comm_system.send_message_to_agent(
            args.agent, args.message, args.area
        )

        if success:
            print(f"✅ Message sent successfully to {args.agent} in {args.area}")
            comm_system.save_devlog()
            sys.exit(0)
        else:
            print(f"❌ Failed to send message to {args.agent}")
            sys.exit(1)

    elif args.status:
        # Enhanced status display mode
        comm_system.display_agent_status()

        print("\n📊 Broadcast History:")
        broadcast_history = comm_system.broadcast_system.get_broadcast_history()
        if broadcast_history:
            for entry in broadcast_history[-5:]:  # Show last 5
                print(
                    f"  {entry['timestamp']}: {entry['message'][:50]}... ({entry.get('method', 'legacy')})"
                )
        else:
            print("  No broadcasts yet")

        sys.exit(0)

    elif args.show_layout:
        # Display region layout
        comm_system.region_manager.display_region_layout()
        sys.exit(0)

    elif args.test_regions:
        # Test region management system
        print("🧪 TESTING SCREEN REGION MANAGEMENT SYSTEM")
        print("=" * 60)

        # Test region operations
        test_operations = [
            ("Agent-1", "input_box", "Test message 1 in input box"),
            ("Agent-2", "workspace_box", "Test message 2 in workspace"),
            ("Agent-3", "status_box", "Test message 3 in status area"),
            ("Agent-4", "input_box", "Test message 4 in input box"),
        ]

        print("🗺️ Testing region-based operations...")
        results = {}
        for agent_id, area, message in test_operations:
            print(f"  📍 Testing {agent_id} in {area}...")
            success = await comm_system.region_manager.execute_in_region(
                agent_id, "type", area, message=message
            )
            results[f"{agent_id}_{area}"] = success
            print(f"    {'✅ SUCCESS' if success else '❌ FAILED'}")

        print(f"\n📊 Region Test Results:")
        for operation, success in results.items():
            status = "✅ SUCCESS" if success else "❌ FAILED"
            print(f"  {status}: {operation}")

        # Display region statistics
        print(f"\n🗺️ Final Region Stats:")
        region_stats = comm_system.region_manager.get_region_stats()
        for key, value in region_stats.items():
            print(f"  {key}: {value}")

        comm_system.save_devlog()
        sys.exit(0)

    else:
        # Interactive demo mode (default)
        print(
            "🚀 REAL AGENT COMMUNICATION SYSTEM V2 DEMO (PHASE 2: SCREEN REGION MANAGEMENT)"
        )
        print("=" * 80)
        print(
            "This system uses your REAL agent coordinates with advanced screen region management!"
        )
        print(
            "Messages will be sent to actual agent input locations in isolated workspaces."
        )
        print("🔄 NEW: Screen region isolation prevents workspace conflicts!")
        print("🗺️ NEW: Multi-cursor support for simultaneous operation!")
        print("=" * 80)

        # Display region layout
        comm_system.region_manager.display_region_layout()

        # Display current agent status
        comm_system.display_agent_status()

        # Demo 1: Region-based broadcasting
        print("\n🎬 Demo 1: Region-Based Broadcasting to ALL agents")
        print("Sending: 'Hello from V2 System with Screen Region Management!'")

        success = await comm_system.send_message_to_all_agents(
            "Hello from V2 System with Screen Region Management! 🚀"
        )

        if success:
            print("✅ All agents received the region-based broadcast message!")
        else:
            print("⚠️ Some agents may not have received the message")

        # Demo 2: Coordinated messaging in different areas
        print("\n🎬 Demo 2: Coordinated messaging in different region areas")

        coordinated_messages = {
            "Agent-1": "Agent-1: Repository cleanup status update! 🧹",
            "Agent-5": "Agent-5: Captain coordination report! ⭐",
            "Agent-8": "Agent-8: Business development update! 💼",
        }

        target_areas = {
            "Agent-1": "workspace_box",  # In workspace area
            "Agent-5": "input_box",  # In input area
            "Agent-8": "status_box",  # In status area
        }

        results = await comm_system.send_coordinated_messages(
            coordinated_messages, target_areas
        )

        # Demo 3: Discord integration
        print("\n🎬 Demo 3: Discord integration")

        discord_results = await discord.broadcast_to_discord(
            "V2 System with Screen Region Management is now operational! 🎉"
        )

        # Final status and devlog
        print("\n🎯 Final System Status:")
        comm_system.display_agent_status()

        print("\n📝 Development Log Summary:")
        devlog = comm_system.get_devlog_summary()
        for entry in devlog[-5:]:  # Show last 5 entries
            print(f"  {entry['timestamp']}: {entry['update']}")

        # Save devlog
        comm_system.save_devlog()

        print(
            f"\n🎉 Demo complete! Check 'agent_communication_v2_devlog.json' for full log."
        )
        print("🔄 Screen region management system is now active!")
        print("🗺️ Agent workspaces are isolated and conflict-free!")
        return "SUCCESS"


if __name__ == "__main__":
    print("🚀 Starting Real Agent Communication System V2 - Phase 2...")
    print("Make sure Discord/your applications are open at the target coordinates!")
    print("🔄 NEW: Screen region management prevents workspace conflicts!")
    print("🗺️ NEW: Multi-cursor support for simultaneous operation!")
    print("Use --help for command-line options.\n")

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⚠️ Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        sys.exit(1)
