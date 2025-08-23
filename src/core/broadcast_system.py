#!/usr/bin/env python3
"""
Broadcast System - Agent_Cellphone_V2
=====================================

Broadcast messaging system for multi-agent communication with clean OOP design.
Follows V2 coding standards: ≤200 LOC, single responsibility, clean architecture.

Author: Agent-1 (Foundation & Testing Specialist)
License: MIT
"""

import asyncio
import json
import time
import logging
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from pathlib import Path


@dataclass
class BroadcastMessage:
    """Represents a broadcast message"""
    message_id: str
    sender_id: str
    content: str
    message_type: str
    priority: int
    timestamp: float
    recipients: List[str]
    metadata: Dict[str, Any]
    status: str = 'pending'


class BroadcastSystem:
    """Broadcast messaging system for multi-agent communication"""
    
    def __init__(self):
        self.broadcast_queue = asyncio.Queue()
        self.message_history: Dict[str, BroadcastMessage] = {}
        self.recipient_handlers: Dict[str, Callable] = {}
        self.broadcast_stats = {
            'total_broadcasts': 0,
            'successful_deliveries': 0,
            'failed_deliveries': 0,
            'active_recipients': 0
        }
        self.logger = logging.getLogger(__name__)
        self.is_running = False
    
    async def broadcast_message(self, sender_id: str, content: str, 
                              message_type: str = "general", priority: int = 1,
                              recipients: Optional[List[str]] = None,
                              metadata: Optional[Dict[str, Any]] = None) -> str:
        """Broadcast a message to multiple agents"""
        message_id = f"broadcast_{sender_id}_{int(time.time() * 1000)}"
        
        message = BroadcastMessage(
            message_id=message_id,
            sender_id=sender_id,
            content=content,
            message_type=message_type,
            priority=priority,
            timestamp=time.time(),
            recipients=recipients or [],
            metadata=metadata or {}
        )
        
        await self.broadcast_queue.put(message)
        self.message_history[message_id] = message
        self.broadcast_stats['total_broadcasts'] += 1
        
        self.logger.info(f"📢 Broadcast from {sender_id}: {content[:50]}...")
        return message_id
    
    async def register_recipient_handler(self, recipient_id: str, handler: Callable):
        """Register a handler for a specific recipient"""
        self.recipient_handlers[recipient_id] = handler
        self.broadcast_stats['active_recipients'] += 1
        self.logger.info(f"📝 Registered handler for {recipient_id}")
    
    async def unregister_recipient_handler(self, recipient_id: str):
        """Unregister a handler for a specific recipient"""
        if recipient_id in self.recipient_handlers:
            del self.recipient_handlers[recipient_id]
            self.broadcast_stats['active_recipients'] -= 1
            self.logger.info(f"🗑️ Unregistered handler for {recipient_id}")
    
    async def process_broadcast_queue(self):
        """Process the broadcast queue and deliver messages"""
        while self.is_running:
            try:
                if not self.broadcast_queue.empty():
                    message = await self.broadcast_queue.get()
                    await self._deliver_broadcast(message)
                else:
                    await asyncio.sleep(0.1)
            except Exception as e:
                self.logger.error(f"❌ Error processing broadcast queue: {e}")
                await asyncio.sleep(1)
    
    async def _deliver_broadcast(self, message: BroadcastMessage):
        """Deliver a broadcast message to all recipients"""
        delivery_results = []
        
        for recipient_id in message.recipients:
            if recipient_id in self.recipient_handlers:
                try:
                    handler = self.recipient_handlers[recipient_id]
                    result = await handler(message)
                    delivery_results.append((recipient_id, True, result))
                    self.broadcast_stats['successful_deliveries'] += 1
                except Exception as e:
                    delivery_results.append((recipient_id, False, str(e)))
                    self.broadcast_stats['failed_deliveries'] += 1
                    self.logger.error(f"❌ Failed to deliver to {recipient_id}: {e}")
            else:
                delivery_results.append((recipient_id, False, "No handler registered"))
                self.broadcast_stats['failed_deliveries'] += 1
        
        # Update message status
        successful_deliveries = sum(1 for _, success, _ in delivery_results if success)
        if successful_deliveries > 0:
            message.status = 'delivered'
        else:
            message.status = 'failed'
        
        # Log delivery results
        self.logger.info(f"📤 Broadcast {message.message_id} delivered to {successful_deliveries}/{len(message.recipients)} recipients")
        
        return delivery_results
    
    async def start_broadcast_system(self):
        """Start the broadcast system"""
        self.is_running = True
        self.logger.info("🚀 Broadcast system started")
        
        # Start processing in background
        asyncio.create_task(self.process_broadcast_queue())
    
    async def stop_broadcast_system(self):
        """Stop the broadcast system"""
        self.is_running = False
        self.logger.info("🛑 Broadcast system stopped")
    
    def get_broadcast_message(self, message_id: str) -> Optional[BroadcastMessage]:
        """Get a specific broadcast message by ID"""
        return self.message_history.get(message_id)
    
    def get_messages_by_sender(self, sender_id: str) -> List[BroadcastMessage]:
        """Get all broadcast messages from a specific sender"""
        return [msg for msg in self.message_history.values() if msg.sender_id == sender_id]
    
    def get_messages_by_type(self, message_type: str) -> List[BroadcastMessage]:
        """Get all broadcast messages of a specific type"""
        return [msg for msg in self.message_history.values() if msg.message_type == message_type]
    
    def get_pending_messages(self) -> List[BroadcastMessage]:
        """Get all pending broadcast messages"""
        return [msg for msg in self.message_history.values() if msg.status == 'pending']
    
    def get_failed_messages(self) -> List[BroadcastMessage]:
        """Get all failed broadcast messages"""
        return [msg for msg in self.message_history.values() if msg.status == 'failed']
    
    def retry_failed_message(self, message_id: str) -> bool:
        """Retry a failed broadcast message"""
        if message_id in self.message_history:
            message = self.message_history[message_id]
            if message.status == 'failed':
                message.status = 'pending'
                asyncio.create_task(self.broadcast_queue.put(message))
                self.logger.info(f"🔄 Retrying failed broadcast: {message_id}")
                return True
        return False
    
    def get_broadcast_stats(self) -> Dict:
        """Get broadcast system statistics"""
        return {
            **self.broadcast_stats,
            'total_messages': len(self.message_history),
            'pending_count': len(self.get_pending_messages()),
            'failed_count': len(self.get_failed_messages()),
            'queue_size': self.broadcast_queue.qsize()
        }
    
    def display_broadcast_status(self):
        """Display current broadcast system status"""
        stats = self.get_broadcast_stats()
        
        print("\n" + "="*60)
        print("📢 BROADCAST SYSTEM STATUS")
        print("="*60)
        print(f"📊 Total Broadcasts: {stats['total_broadcasts']}")
        print(f"✅ Successful Deliveries: {stats['successful_deliveries']}")
        print(f"❌ Failed Deliveries: {stats['failed_deliveries']}")
        print(f"⏳ Pending: {stats['pending_count']}")
        print(f"📝 Active Recipients: {stats['active_recipients']}")
        print(f"🔒 Queue Size: {stats['queue_size']}")
        print()
        
        # Show recent broadcasts
        recent_messages = sorted(
            self.message_history.values(), 
            key=lambda x: x.timestamp, 
            reverse=True
        )[:5]
        
        if recent_messages:
            print("📋 Recent Broadcasts:")
            for message in recent_messages:
                status_emoji = {
                    'pending': '⏳',
                    'delivered': '✅',
                    'failed': '❌'
                }.get(message.status, '❓')
                
                print(f"  {status_emoji} {message.sender_id}: {message.content[:40]}...")
                print(f"     ID: {message.message_id} | Type: {message.message_type}")
                print(f"     Recipients: {len(message.recipients)} | Status: {message.status}")
                print()
    
    def cleanup(self):
        """Cleanup broadcast system resources"""
        self.logger.info("🧹 Broadcast system cleanup complete")


if __name__ == "__main__":
    # Demo usage
    async def demo():
        broadcast_system = BroadcastSystem()
        
        # Start the system
        await broadcast_system.start_broadcast_system()
        
        # Register a recipient handler
        async def demo_handler(message):
            print(f"📨 {message.recipient_id} received: {message.content}")
            return "processed"
        
        await broadcast_system.register_recipient_handler("demo_recipient", demo_handler)
        
        # Send some broadcasts
        await broadcast_system.broadcast_message("Agent-1", "Hello everyone!", recipients=["demo_recipient"])
        await broadcast_system.broadcast_message("Agent-2", "Test broadcast", recipients=["demo_recipient"])
        
        # Wait a bit for processing
        await asyncio.sleep(1)
        
        # Display status
        broadcast_system.display_broadcast_status()
        
        # Stop the system
        await broadcast_system.stop_broadcast_system()
    
    # Run demo
    asyncio.run(demo())
