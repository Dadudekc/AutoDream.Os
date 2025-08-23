#!/usr/bin/env python3
"""
Agent Communication System - Agent_Cellphone_V2
==============================================

Main communication system that orchestrates screen regions, input buffering, and broadcasting.
Follows V2 coding standards: ≤200 LOC, single responsibility, clean architecture.

Author: Agent-1 (Foundation & Testing Specialist)
License: MIT
"""

import asyncio
import json
import time
import logging
import argparse
import sys
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
import pyautogui
import pyperclip

# Import our refactored components
from .screen_region_manager import ScreenRegionManager
from .input_buffer_system import InputBufferSystem, BufferedInput
from .broadcast_system import BroadcastSystem, BroadcastMessage


class AgentCommunicationSystem:
    """Main communication system orchestrating all components"""
    
    def __init__(self):
        self.region_manager = ScreenRegionManager()
        self.input_buffer = InputBufferSystem()
        self.broadcast_system = BroadcastSystem()
        self.logger = logging.getLogger(__name__)
        self.is_running = False
        
        # Configure PyAutoGUI
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.1
    
    async def initialize_system(self):
        """Initialize the communication system"""
        try:
            # Start broadcast system
            await self.broadcast_system.start_broadcast_system()
            
            # Load agent coordinates
            await self._load_agent_coordinates()
            
            self.is_running = True
            self.logger.info("🚀 Agent Communication System initialized")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize system: {e}")
            raise
    
    async def _load_agent_coordinates(self):
        """Load agent coordinates from configuration"""
        try:
            coords_file = Path("cursor_agent_coords.json")
            if coords_file.exists():
                with open(coords_file, 'r') as f:
                    coords_data = json.load(f)
                
                for agent_id, coords in coords_data.items():
                    if isinstance(coords, dict) and 'x' in coords and 'y' in coords:
                        self.region_manager.define_agent_region(
                            agent_id, coords['x'], coords['y']
                        )
                        self.logger.info(f"📍 Loaded coordinates for {agent_id}")
                
                self.logger.info(f"✅ Loaded {len(coords_data)} agent coordinates")
            else:
                self.logger.warning("⚠️ No agent coordinates file found")
                
        except Exception as e:
            self.logger.error(f"❌ Error loading coordinates: {e}")
    
    async def send_message_to_agent(self, agent_id: str, message: str, 
                                   target_area: str = "input_box", 
                                   line_breaks: bool = False) -> str:
        """Send a message to a specific agent"""
        # Buffer the input
        buffer_id = await self.input_buffer.buffer_agent_input(
            agent_id, message, target_area, line_breaks=line_breaks
        )
        
        # Execute immediately
        success = await self._execute_agent_input(
            agent_id, message, target_area, line_breaks
        )
        
        if success:
            self.logger.info(f"✅ Message sent to {agent_id}: {message[:30]}...")
        else:
            self.logger.error(f"❌ Failed to send message to {agent_id}")
        
        return buffer_id
    
    async def _execute_agent_input(self, agent_id: str, message: str, 
                                  target_area: str, line_breaks: bool) -> bool:
        """Execute input for a specific agent"""
        region = self.region_manager.get_agent_region(agent_id)
        if not region:
            self.logger.error(f"❌ No region defined for {agent_id}")
            return False
        
        lock = self.region_manager.get_region_lock(agent_id)
        if not lock:
            self.logger.error(f"❌ No lock available for {agent_id}")
            return False
        
        async with lock:
            try:
                return await self._type_in_region(region, target_area, message, line_breaks)
            except Exception as e:
                self.logger.error(f"❌ Error executing input for {agent_id}: {e}")
                return False
    
    async def _type_in_region(self, region, target_area: str, 
                             message: str, line_breaks: bool) -> bool:
        """Type message within agent's region"""
        try:
            # Get target coordinates
            if target_area == "input_box":
                target_x = region.input_box['x']
                target_y = region.input_box['y']
            elif target_area == "workspace_box":
                target_x = region.workspace_box['x']
                target_y = region.workspace_box['y']
            else:
                target_x = region.x + 10
                target_y = region.y + 10
            
            # Move to target
            pyautogui.moveTo(target_x, target_y, duration=0.1)
            pyautogui.click(target_x, target_y)
            time.sleep(0.05)
            
            # Type message
            if line_breaks:
                lines = message.split('\n')
                for i, line in enumerate(lines):
                    if line.strip():
                        pyautogui.typewrite(line, interval=0.03)
                    if i < len(lines) - 1:
                        pyautogui.hotkey('shift', 'enter')
                        time.sleep(0.05)
            else:
                pyautogui.typewrite(message, interval=0.03)
            
            # Send message
            pyautogui.press('enter')
            
            # Update cursor position
            self.region_manager.update_virtual_cursor(region.agent_id, target_x, target_y)
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to type in region: {e}")
            return False
    
    async def broadcast_to_all_agents(self, sender_id: str, message: str, 
                                    message_type: str = "general") -> str:
        """Broadcast message to all registered agents"""
        agent_ids = list(self.region_manager.agent_regions.keys())
        
        broadcast_id = await self.broadcast_system.broadcast_message(
            sender_id, message, message_type, recipients=agent_ids
        )
        
        self.logger.info(f"📢 Broadcast from {sender_id} to {len(agent_ids)} agents")
        return broadcast_id
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        return {
            'system_running': self.is_running,
            'region_stats': self.region_manager.get_region_stats(),
            'buffer_stats': self.input_buffer.get_buffer_stats(),
            'broadcast_stats': self.broadcast_system.get_broadcast_stats(),
            'total_agents': len(self.region_manager.agent_regions),
            'active_regions': self.region_manager.region_stats['active_regions']
        }
    
    def display_system_status(self):
        """Display comprehensive system status"""
        print("\n" + "="*80)
        print("🤖 AGENT COMMUNICATION SYSTEM STATUS")
        print("="*80)
        
        # System status
        print(f"🚀 System Running: {'✅ Yes' if self.is_running else '❌ No'}")
        print(f"📊 Total Agents: {len(self.region_manager.agent_regions)}")
        print()
        
        # Region status
        self.region_manager.display_region_layout()
        
        # Buffer status
        self.input_buffer.display_buffer_status()
        
        # Broadcast status
        self.broadcast_system.display_broadcast_status()
    
    async def shutdown(self):
        """Shutdown the communication system"""
        try:
            self.is_running = False
            
            # Stop broadcast system
            await self.broadcast_system.stop_broadcast_system()
            
            # Cleanup components
            self.region_manager.cleanup()
            self.input_buffer.cleanup()
            self.broadcast_system.cleanup()
            
            self.logger.info("🛑 Agent Communication System shutdown complete")
            
        except Exception as e:
            self.logger.error(f"❌ Error during shutdown: {e}")


def main():
    """CLI interface for the communication system"""
    parser = argparse.ArgumentParser(
        description="Agent Communication System V2",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument("--status", action="store_true", 
                       help="Show system status")
    parser.add_argument("--send", nargs=2, metavar=("AGENT", "MESSAGE"),
                       help="Send message to specific agent")
    parser.add_argument("--broadcast", nargs=2, metavar=("SENDER", "MESSAGE"),
                       help="Broadcast message to all agents")
    parser.add_argument("--demo", action="store_true",
                       help="Run demo scenario")
    
    args = parser.parse_args()
    
    async def run_cli():
        system = AgentCommunicationSystem()
        
        try:
            await system.initialize_system()
            
            if args.status:
                system.display_system_status()
            
            elif args.send:
                agent_id, message = args.send
                buffer_id = await system.send_message_to_agent(agent_id, message)
                print(f"✅ Message buffered with ID: {buffer_id}")
            
            elif args.broadcast:
                sender_id, message = args.broadcast
                broadcast_id = await system.broadcast_to_all_agents(sender_id, message)
                print(f"📢 Broadcast sent with ID: {broadcast_id}")
            
            elif args.demo:
                print("🚀 Running demo scenario...")
                
                # Send messages to different agents
                await system.send_message_to_agent("Agent-1", "Hello from demo!")
                await system.broadcast_to_all_agents("Demo", "Testing broadcast system")
                
                # Wait for processing
                await asyncio.sleep(2)
                
                # Show status
                system.display_system_status()
            
            else:
                parser.print_help()
            
        except KeyboardInterrupt:
            print("\n🛑 Shutting down...")
        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            await system.shutdown()
    
    # Run CLI
    asyncio.run(run_cli())


if __name__ == "__main__":
    main()
