#!/usr/bin/env python3
"""
Screen Region Manager - Agent_Cellphone_V2
==========================================

Manages isolated screen regions for each agent with proper OOP design.
Follows V2 coding standards: ≤200 LOC, single responsibility, clean architecture.
Now inherits from BaseManager for unified functionality.

Author: Agent-1 (Foundation & Testing Specialist)
License: MIT
"""

import asyncio
import logging
import time

from src.utils.stability_improvements import stability_manager, safe_import
from dataclasses import dataclass
from typing import Dict, Optional, Tuple, List, Any

from .base_manager import BaseManager


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


class ScreenRegionManager(BaseManager):
    """Manages isolated screen regions for each agent
    
    Now inherits from BaseManager for unified functionality
    """
    
    def __init__(self):
        super().__init__(
            manager_id="screen_region_manager",
            name="Screen Region Manager",
            description="Manages isolated screen regions for each agent"
        )
        
        self.agent_regions: Dict[str, ScreenRegion] = {}
        self.region_locks: Dict[str, asyncio.Lock] = {}
        self.virtual_cursors: Dict[str, Tuple[int, int]] = {}
        self.region_stats = {
            'total_regions': 0,
            'active_regions': 0,
            'isolated_workspaces': 0
        }
        
        # Screen region management tracking
        self.region_operations: List[Dict[str, Any]] = []
        self.regions_created = 0
        self.regions_activated = 0
        self.regions_deactivated = 0
        self.failed_operations: List[Dict[str, Any]] = []
        
        self.logger.info("Screen Region Manager initialized")
    
    def define_agent_region(self, agent_id: str, x: int, y: int, 
                           width: int = 300, height: int = 200) -> ScreenRegion:
        """Define isolated screen region for agent"""
        start_time = time.time()
        try:
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
            
            # Record successful operation
            self.regions_created += 1
            self.record_operation("define_agent_region", True, time.time() - start_time)
            
            self.logger.info(f"📍 Defined region for {agent_id}: ({x}, {y}) {width}x{height}")
            return region
            
        except Exception as e:
            self.logger.error(f"Failed to define region for {agent_id}: {e}")
            self.record_operation("define_agent_region", False, time.time() - start_time)
            self.failed_operations.append({
                "operation": "define_agent_region",
                "agent_id": agent_id,
                "error": str(e),
                "timestamp": time.time()
            })
            raise
    
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
        start_time = time.time()
        try:
            if agent_id in self.agent_regions:
                self.agent_regions[agent_id].active = False
                self.region_stats['active_regions'] -= 1
                
                # Record successful operation
                self.regions_deactivated += 1
                self.record_operation("deactivate_region", True, time.time() - start_time)
                
                self.logger.info(f"🔴 Deactivated region for {agent_id}")
            else:
                self.record_operation("deactivate_region", False, time.time() - start_time)
                
        except Exception as e:
            self.logger.error(f"Failed to deactivate region for {agent_id}: {e}")
            self.record_operation("deactivate_region", False, time.time() - start_time)
            self.failed_operations.append({
                "operation": "deactivate_region",
                "agent_id": agent_id,
                "error": str(e),
                "timestamp": time.time()
            })
    
    def activate_region(self, agent_id: str):
        """Activate agent region"""
        start_time = time.time()
        try:
            if agent_id in self.agent_regions:
                self.agent_regions[agent_id].active = True
                self.region_stats['active_regions'] += 1
                
                # Record successful operation
                self.regions_activated += 1
                self.record_operation("activate_region", True, time.time() - start_time)
                
                self.logger.info(f"🟢 Activated region for {agent_id}")
            else:
                self.record_operation("activate_region", False, time.time() - start_time)
                
        except Exception as e:
            self.logger.error(f"Failed to activate region for {agent_id}: {e}")
            self.record_operation("activate_region", False, time.time() - start_time)
            self.failed_operations.append({
                "operation": "activate_region",
                "agent_id": agent_id,
                "error": str(e),
                "timestamp": time.time()
            })
    
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

    # ============================================================================
    # BaseManager Abstract Method Implementations
    # ============================================================================
    
    def _on_start(self) -> bool:
        """Initialize screen region management system"""
        try:
            self.logger.info("Starting Screen Region Manager...")
            
            # Clear tracking data
            self.region_operations.clear()
            self.regions_created = 0
            self.regions_activated = 0
            self.regions_deactivated = 0
            self.failed_operations.clear()
            
            self.logger.info("Screen Region Manager started successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start Screen Region Manager: {e}")
            return False
    
    def _on_stop(self) -> bool:
        """Cleanup screen region management system"""
        try:
            self.logger.info("Stopping Screen Region Manager...")
            
            # Save screen region management data
            self._save_screen_region_data()
            
            self.logger.info("Screen Region Manager stopped successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to stop Screen Region Manager: {e}")
            return False
    
    def _on_heartbeat(self) -> bool:
        """Screen region management health check"""
        try:
            # Check screen region management health
            health_status = self._check_screen_region_health()
            
            # Update metrics
            self.metrics.update(
                operations_count=len(self.region_operations),
                success_rate=self._calculate_success_rate(),
                average_response_time=self._calculate_average_response_time(),
                health_status=health_status
            )
            
            return health_status == "healthy"
            
        except Exception as e:
            self.logger.error(f"Screen Region Manager heartbeat failed: {e}")
            return False
    
    def _on_initialize_resources(self) -> bool:
        """Initialize screen region management resources"""
        try:
            # Initialize region tracking
            self.region_operations = []
            self.regions_created = 0
            self.regions_activated = 0
            self.regions_deactivated = 0
            self.failed_operations = []
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Screen Region Manager resources: {e}")
            return False
    
    def _on_cleanup_resources(self) -> bool:
        """Cleanup screen region management resources"""
        try:
            # Save screen region management data
            self._save_screen_region_data()
            
            # Clear tracking data
            self.region_operations.clear()
            self.regions_created = 0
            self.regions_activated = 0
            self.regions_deactivated = 0
            self.failed_operations.clear()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to cleanup Screen Region Manager resources: {e}")
            return False
    
    def _on_recovery_attempt(self) -> bool:
        """Attempt to recover from errors"""
        try:
            self.logger.info("Attempting Screen Region Manager recovery...")
            
            # Reinitialize region tracking
            self.region_operations = []
            self.regions_created = 0
            self.regions_activated = 0
            self.regions_deactivated = 0
            self.failed_operations = []
            
            self.logger.info("Screen Region Manager recovery successful")
            return True
                
        except Exception as e:
            self.logger.error(f"Screen Region Manager recovery attempt failed: {e}")
            return False
    
    # ============================================================================
    # Private Helper Methods
    # ============================================================================
    
    def _save_screen_region_data(self):
        """Save screen region management data for persistence"""
        try:
            data = {
                "regions_created": self.regions_created,
                "regions_activated": self.regions_activated,
                "regions_deactivated": self.regions_deactivated,
                "failed_operations": self.failed_operations,
                "timestamp": time.time()
            }
            
            # Save to file or database as needed
            # For now, just log the data
            self.logger.info(f"Screen region management data: {data}")
            
        except Exception as e:
            self.logger.error(f"Failed to save screen region management data: {e}")
    
    def _check_screen_region_health(self) -> str:
        """Check screen region management system health"""
        try:
            # Check if we have regions defined
            if len(self.agent_regions) > 0:
                # Check if we have recent operations
                if len(self.region_operations) > 0:
                    return "healthy"
                else:
                    return "idle"
            else:
                return "no_regions"
                
        except Exception as e:
            self.logger.error(f"Screen region management health check failed: {e}")
            return "unhealthy"
    
    def _calculate_success_rate(self) -> float:
        """Calculate operation success rate"""
        try:
            if len(self.region_operations) == 0:
                return 1.0
            
            successful_ops = sum(1 for op in self.region_operations if op.get("success", False))
            return successful_ops / len(self.region_operations)
            
        except Exception as e:
            self.logger.error(f"Failed to calculate success rate: {e}")
            return 0.0
    
    def _calculate_average_response_time(self) -> float:
        """Calculate average operation response time"""
        try:
            if len(self.region_operations) == 0:
                return 0.0
            
            total_time = sum(op.get("duration", 0.0) for op in self.region_operations)
            return total_time / len(self.region_operations)
            
        except Exception as e:
            self.logger.error(f"Failed to calculate average response time: {e}")
            return 0.0


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
