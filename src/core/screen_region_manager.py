#!/usr/bin/env python3
"""
Screen Region Manager - Agent_Cellphone_V2
==========================================

Manages isolated screen regions for each agent with proper OOP design.
Follows V2 coding standards: ≤200 LOC, single responsibility, clean architecture.

Author: Agent-1 (Foundation & Testing Specialist)
License: MIT
"""

import asyncio
import logging
from dataclasses import dataclass
from typing import Dict, Optional, Tuple


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
        self.agent_regions: Dict[str, ScreenRegion] = {}
        self.region_locks: Dict[str, asyncio.Lock] = {}
        self.virtual_cursors: Dict[str, Tuple[int, int]] = {}
        self.logger = logging.getLogger(__name__)
        self.region_stats = {
            'total_regions': 0,
            'active_regions': 0,
            'isolated_workspaces': 0
        }
    
    def define_agent_region(self, agent_id: str, x: int, y: int, 
                           width: int = 300, height: int = 200) -> ScreenRegion:
        """Define isolated screen region for agent"""
        # Calculate sub-regions within the agent's workspace
        input_box = {
            'x': x + 10,
            'y': y + height - 30,
            'width': width - 20,
            'height': 25
        }
        
        status_box = {
            'x': x + 10,
            'y': y + 10,
            'width': width - 20,
            'height': 25
        }
        
        workspace_box = {
            'x': x + 10,
            'y': y + 40,
            'width': width - 20,
            'height': height - 80
        }
        
        # Create region
        region = ScreenRegion(
            agent_id=agent_id,
            x=x, y=y,
            width=width, height=height,
            input_box=input_box,
            status_box=status_box,
            workspace_box=workspace_box
        )
        
        self.agent_regions[agent_id] = region
        self.region_locks[agent_id] = asyncio.Lock()
        self.virtual_cursors[agent_id] = (x + 10, y + 10)
        
        self.region_stats['total_regions'] += 1
        self.region_stats['active_regions'] += 1
        self.region_stats['isolated_workspaces'] += 1
        
        self.logger.info(f"📍 Defined region for {agent_id}: ({x}, {y}) {width}x{height}")
        return region
    
    def get_agent_region(self, agent_id: str) -> Optional[ScreenRegion]:
        """Get agent's screen region"""
        return self.agent_regions.get(agent_id)
    
    def is_coordinate_in_region(self, agent_id: str, x: int, y: int) -> bool:
        """Check if coordinates are within agent's region"""
        region = self.get_agent_region(agent_id)
        if not region:
            return False
        
        return (region.x <= x <= region.x + region.width and 
                region.y <= y <= region.y + region.height)
    
    def get_region_lock(self, agent_id: str) -> Optional[asyncio.Lock]:
        """Get region lock for coordination"""
        return self.region_locks.get(agent_id)
    
    def update_virtual_cursor(self, agent_id: str, x: int, y: int):
        """Update virtual cursor position for agent"""
        if agent_id in self.virtual_cursors:
            self.virtual_cursors[agent_id] = (x, y)
    
    def get_virtual_cursor(self, agent_id: str) -> Optional[Tuple[int, int]]:
        """Get virtual cursor position for agent"""
        return self.virtual_cursors.get(agent_id)
    
    def deactivate_region(self, agent_id: str):
        """Deactivate agent region"""
        if agent_id in self.agent_regions:
            self.agent_regions[agent_id].active = False
            self.region_stats['active_regions'] -= 1
            self.logger.info(f"🔴 Deactivated region for {agent_id}")
    
    def activate_region(self, agent_id: str):
        """Activate agent region"""
        if agent_id in self.agent_regions:
            self.agent_regions[agent_id].active = True
            self.region_stats['active_regions'] += 1
            self.logger.info(f"🟢 Activated region for {agent_id}")
    
    def get_region_stats(self) -> Dict:
        """Get region management statistics"""
        return {
            **self.region_stats,
            'defined_regions': len(self.agent_regions),
            'virtual_cursors': len(self.virtual_cursors)
        }
    
    def display_region_layout(self):
        """Display visual representation of region layout"""
        print("\n" + "="*80)
        print("🗺️  SCREEN REGION LAYOUT - AGENT WORKSPACES")
        print("="*80)
        
        for agent_id, region in self.agent_regions.items():
            print(f"📍 {agent_id}:")
            print(f"   🖥️  Main Region: ({region.x}, {region.y}) {region.width}x{region.height}")
            print(f"   📝 Input Box: ({region.input_box['x']}, {region.input_box['y']})")
            print(f"   📊 Status Box: ({region.status_box['x']}, {region.status_box['y']})")
            print(f"   💼 Workspace: ({region.workspace_box['x']}, {region.workspace_box['y']})")
            print(f"   🖱️  Virtual Cursor: {self.virtual_cursors.get(agent_id, 'Not set')}")
            print(f"   🔴 Status: {'🟢 Active' if region.active else '🔴 Inactive'}")
            print()
    
    def cleanup(self):
        """Cleanup resources"""
        # Note: asyncio.Lock objects don't have a close() method
        # They are automatically cleaned up when the object is garbage collected
        self.logger.info("🧹 Screen region manager cleanup complete")


if __name__ == "__main__":
    # Demo usage
    manager = ScreenRegionManager()
    
    # Define some regions
    manager.define_agent_region("Agent-1", 0, 0, 400, 300)
    manager.define_agent_region("Agent-2", 400, 0, 400, 300)
    
    # Display layout
    manager.display_region_layout()
    
    # Show stats
    print("📊 Region Stats:", manager.get_region_stats())
