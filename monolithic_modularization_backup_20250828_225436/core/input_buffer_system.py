#!/usr/bin/env python3
"""
Input Buffer System - Agent_Cellphone_V2
========================================

Enhanced input buffering system with region management for clean OOP design.
Follows V2 coding standards: ≤200 LOC, single responsibility, clean architecture.

Author: Agent-1 (Foundation & Testing Specialist)
License: MIT
"""

import asyncio
import time
import logging

from src.utils.stability_improvements import stability_manager, safe_import
from typing import Dict, List, Any, Optional
from dataclasses import dataclass


@dataclass
class BufferedInput:
    """Represents a buffered input item"""
    buffer_id: str
    agent_id: str
    message: str
    target_area: str
    priority: int
    timestamp: float
    status: str
    line_breaks: bool
    execution_time: Optional[float] = None


class InputBufferSystem:
    """Enhanced input buffering system with region management"""
    
    def __init__(self):
        self.input_queue = asyncio.Queue()
        self.agent_buffers: Dict[str, BufferedInput] = {}
        self.coordination_lock = asyncio.Lock()
        self.logger = logging.getLogger(__name__)
        self.buffer_stats = {
            'total_buffered': 0,
            'total_executed': 0,
            'conflicts_prevented': 0,
            'region_executions': 0
        }
    
    async def buffer_agent_input(self, agent_id: str, message: str, 
                                target_area: str = "input_box", priority: int = 1, 
                                line_breaks: bool = False) -> str:
        """Buffer input from agent for region-specific execution"""
        buffer_id = f"{agent_id}_{int(time.time() * 1000)}"
        
        input_item = BufferedInput(
            buffer_id=buffer_id,
            agent_id=agent_id,
            message=message,
            target_area=target_area,
            priority=priority,
            timestamp=time.time(),
            status='buffered',
            line_breaks=line_breaks
        )
        
        await self.input_queue.put(input_item)
        self.agent_buffers[buffer_id] = input_item
        self.buffer_stats['total_buffered'] += 1
        
        line_break_info = " with line breaks" if line_breaks else ""
        self.logger.info(f"📥 Buffered input from {agent_id} in {target_area}{line_break_info}: {message[:30]}...")
        return buffer_id
    
    async def execute_buffered_inputs(self, execution_handler) -> Dict[str, bool]:
        """Execute all buffered inputs using provided execution handler"""
        results = {}
        
        async with self.coordination_lock:
            self.logger.info(f"🚀 Executing {self.input_queue.qsize()} buffered inputs...")
            
            while not self.input_queue.empty():
                input_item = await self.input_queue.get()
                
                # Execute using provided handler
                success = await execution_handler(input_item)
                results[input_item.buffer_id] = success
                
                # Update status
                input_item.status = 'executed' if success else 'failed'
                input_item.execution_time = time.time()
                
                # Small coordination delay
                await asyncio.sleep(0.05)
        
        self.buffer_stats['total_executed'] += len(results)
        self.logger.info(f"✅ Executed {len(results)} buffered inputs")
        
        return results
    
    def get_buffered_input(self, buffer_id: str) -> Optional[BufferedInput]:
        """Get a specific buffered input by ID"""
        return self.agent_buffers.get(buffer_id)
    
    def get_agent_buffers(self, agent_id: str) -> List[BufferedInput]:
        """Get all buffered inputs for a specific agent"""
        return [item for item in self.agent_buffers.values() if item.agent_id == agent_id]
    
    def get_pending_buffers(self) -> List[BufferedInput]:
        """Get all pending buffered inputs"""
        return [item for item in self.agent_buffers.values() if item.status == 'buffered']
    
    def get_failed_buffers(self) -> List[BufferedInput]:
        """Get all failed buffered inputs"""
        return [item for item in self.agent_buffers.values() if item.status == 'failed']
    
    def retry_failed_input(self, buffer_id: str) -> bool:
        """Retry a failed input by resetting its status"""
        if buffer_id in self.agent_buffers:
            input_item = self.agent_buffers[buffer_id]
            if input_item.status == 'failed':
                input_item.status = 'buffered'
                input_item.retry_count = getattr(input_item, 'retry_count', 0) + 1
                self.logger.info(f"🔄 Retrying failed input: {buffer_id}")
                return True
        return False
    
    def clear_completed_buffers(self, max_age_hours: int = 24):
        """Clear old completed buffers to free memory"""
        cutoff_time = time.time() - (max_age_hours * 3600)
        cleared_count = 0
        
        buffer_ids = list(self.agent_buffers.keys())
        for buffer_id in buffer_ids:
            input_item = self.agent_buffers[buffer_id]
            if (input_item.status in ['executed', 'failed'] and 
                input_item.timestamp < cutoff_time):
                del self.agent_buffers[buffer_id]
                cleared_count += 1
        
        if cleared_count > 0:
            self.logger.info(f"🧹 Cleared {cleared_count} old completed buffers")
    
    def get_buffer_stats(self) -> Dict:
        """Get buffer system statistics"""
        return {
            **self.buffer_stats,
            'current_buffers': len(self.agent_buffers),
            'pending_count': len(self.get_pending_buffers()),
            'failed_count': len(self.get_failed_buffers()),
            'queue_size': self.input_queue.qsize()
        }
    
    def display_buffer_status(self):
        """Display current buffer system status"""
        stats = self.get_buffer_stats()
        
        print("\n" + "="*60)
        print("📥 INPUT BUFFER SYSTEM STATUS")
        print("="*60)
        print(f"📊 Total Buffered: {stats['total_buffered']}")
        print(f"✅ Total Executed: {stats['total_executed']}")
        print(f"⏳ Pending: {stats['pending_count']}")
        print(f"❌ Failed: {stats['failed_count']}")
        print(f"🔒 Queue Size: {stats['queue_size']}")
        print(f"🔄 Conflicts Prevented: {stats['conflicts_prevented']}")
        print()
        
        # Show recent buffers
        recent_buffers = sorted(
            self.agent_buffers.values(), 
            key=lambda x: x.timestamp, 
            reverse=True
        )[:5]
        
        if recent_buffers:
            print("📋 Recent Buffers:")
            for buffer_item in recent_buffers:
                status_emoji = {
                    'buffered': '⏳',
                    'executed': '✅',
                    'failed': '❌'
                }.get(buffer_item.status, '❓')
                
                print(f"  {status_emoji} {buffer_item.agent_id}: {buffer_item.message[:40]}...")
                print(f"     ID: {buffer_item.buffer_id} | Area: {buffer_item.target_area}")
                print()
    
    def cleanup(self):
        """Cleanup buffer system resources"""
        self.clear_completed_buffers()
        self.logger.info("🧹 Input buffer system cleanup complete")


if __name__ == "__main__":
    # Demo usage
    async def demo():
        buffer_system = InputBufferSystem()
        
        # Buffer some inputs
        await buffer_system.buffer_agent_input("Agent-1", "Hello world", "input_box")
        await buffer_system.buffer_agent_input("Agent-2", "Test message", "workspace_box", priority=2)
        
        # Display status
        buffer_system.display_buffer_status()
        
        # Show stats
        print("📊 Buffer Stats:", buffer_system.get_buffer_stats())
    
    # Run demo
    asyncio.run(demo())

