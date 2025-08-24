"""
Message Storage - Extracted from v2_comprehensive_messaging_system.py

This module handles message storage including:
- Message persistence and retrieval
- Message indexing and search
- Storage backends (memory, database, file)
- Message lifecycle management

Original file: src/core/v2_comprehensive_messaging_system.py
Extraction date: 2024-12-19
"""

import logging
import threading
import time
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Set, Callable
from dataclasses import dataclass, field
from collections import defaultdict, deque
from abc import ABC, abstractmethod

# Configure logging
logger = logging.getLogger(__name__)

# Import enums and data structures from main file
from ..v2_comprehensive_messaging_system import (
    V2MessageType, V2MessagePriority, V2MessageStatus,
    V2Message, V2AgentInfo, IMessageStorage
)


class V2MessageStorage(IMessageStorage):
    """Message storage implementation - SRP: Store and retrieve messages"""
    
    def __init__(self):
        self.messages: Dict[str, V2Message] = {}
        self.agent_messages: Dict[str, List[str]] = defaultdict(list)
        self.type_messages: Dict[V2MessageType, List[str]] = defaultdict(list)
        self.status_messages: Dict[V2MessageStatus, List[str]] = defaultdict(list)
        self.timestamp_index: List[tuple] = []  # (timestamp, message_id) pairs
        self.lock = threading.RLock()
        self.storage_stats = {
            "total_messages": 0,
            "messages_by_type": defaultdict(int),
            "messages_by_status": defaultdict(int),
            "messages_by_agent": defaultdict(int)
        }
        
    def store_message(self, message: V2Message) -> bool:
        """Store a message with indexing"""
        try:
            with self.lock:
                # Store the message
                self.messages[message.message_id] = message
                
                # Update indexes
                self._update_indexes(message, "add")
                
                # Update statistics
                self.storage_stats["total_messages"] += 1
                self.storage_stats["messages_by_type"][message.message_type] += 1
                self.storage_stats["messages_by_status"][message.status] += 1
                
                if message.recipient_id and message.recipient_id != "broadcast":
                    self.storage_stats["messages_by_agent"][message.recipient_id] += 1
                
                logger.debug(f"Stored message {message.message_id}")
                return True
                
        except Exception as e:
            logger.error(f"Failed to store message: {e}")
            return False
    
    def get_message(self, message_id: str) -> Optional[V2Message]:
        """Retrieve a message by ID"""
        try:
            with self.lock:
                return self.messages.get(message_id)
        except Exception as e:
            logger.error(f"Failed to get message {message_id}: {e}")
            return None
    
    def get_messages_for_agent(self, agent_id: str, 
                              message_type: Optional[V2MessageType] = None,
                              status: Optional[V2MessageStatus] = None,
                              limit: Optional[int] = None) -> List[V2Message]:
        """Get messages for an agent with optional filtering"""
        try:
            messages = []
            with self.lock:
                # Get message IDs for this agent
                agent_message_ids = self.agent_messages.get(agent_id, [])
                
                for message_id in agent_message_ids:
                    if message_id in self.messages:
                        message = self.messages[message_id]
                        
                        # Apply filters
                        if message_type and message.message_type != message_type:
                            continue
                        if status and message.status != status:
                            continue
                        
                        messages.append(message)
                        
                        # Apply limit if specified
                        if limit and len(messages) >= limit:
                            break
            
            # Sort by priority (highest first) then by timestamp (oldest first)
            messages.sort(key=lambda m: (m.priority.value, m.timestamp), reverse=True)
            return messages
            
        except Exception as e:
            logger.error(f"Failed to get messages for agent {agent_id}: {e}")
            return []
    
    def get_messages_by_type(self, message_type: V2MessageType, 
                            limit: Optional[int] = None) -> List[V2Message]:
        """Get messages by type"""
        try:
            messages = []
            with self.lock:
                type_message_ids = self.type_messages.get(message_type, [])
                
                for message_id in type_message_ids:
                    if message_id in self.messages:
                        messages.append(self.messages[message_id])
                        
                        if limit and len(messages) >= limit:
                            break
            
            # Sort by timestamp (newest first)
            messages.sort(key=lambda m: m.timestamp, reverse=True)
            return messages
            
        except Exception as e:
            logger.error(f"Failed to get messages by type {message_type}: {e}")
            return []
    
    def get_messages_by_status(self, status: V2MessageStatus, 
                              limit: Optional[int] = None) -> List[V2Message]:
        """Get messages by status"""
        try:
            messages = []
            with self.lock:
                status_message_ids = self.status_messages.get(status, [])
                
                for message_id in status_message_ids:
                    if message_id in self.messages:
                        messages.append(self.messages[message_id])
                        
                        if limit and len(messages) >= limit:
                            break
            
            # Sort by timestamp (newest first)
            messages.sort(key=lambda m: m.timestamp, reverse=True)
            return messages
            
        except Exception as e:
            logger.error(f"Failed to get messages by status {status}: {e}")
            return []
    
    def update_message_status(self, message_id: str, status: V2MessageStatus) -> bool:
        """Update message status"""
        try:
            with self.lock:
                if message_id in self.messages:
                    old_status = self.messages[message_id].status
                    self.messages[message_id].status = status
                    
                    # Update status index
                    if old_status != status:
                        # Remove from old status index
                        if message_id in self.status_messages[old_status]:
                            self.status_messages[old_status].remove(message_id)
                        
                        # Add to new status index
                        self.status_messages[status].append(message_id)
                        
                        # Update statistics
                        self.storage_stats["messages_by_status"][old_status] -= 1
                        self.storage_stats["messages_by_status"][status] += 1
                    
                    logger.debug(f"Updated message {message_id} status to {status}")
                    return True
                return False
                
        except Exception as e:
            logger.error(f"Failed to update message status: {e}")
            return False
    
    def delete_message(self, message_id: str) -> bool:
        """Delete a message"""
        try:
            with self.lock:
                if message_id in self.messages:
                    message = self.messages[message_id]
                    
                    # Remove from indexes
                    self._update_indexes(message, "remove")
                    
                    # Update statistics
                    self.storage_stats["total_messages"] -= 1
                    self.storage_stats["messages_by_type"][message.message_type] -= 1
                    self.storage_stats["messages_by_status"][message.status] -= 1
                    
                    if message.recipient_id and message.recipient_id != "broadcast":
                        self.storage_stats["messages_by_agent"][message.recipient_id] -= 1
                    
                    # Remove from main storage
                    del self.messages[message_id]
                    
                    logger.debug(f"Deleted message {message_id}")
                    return True
                return False
                
        except Exception as e:
            logger.error(f"Failed to delete message: {e}")
            return False
    
    def _update_indexes(self, message: V2Message, operation: str):
        """Update all indexes for a message"""
        try:
            if operation == "add":
                # Add to agent index
                if message.recipient_id and message.recipient_id != "broadcast":
                    self.agent_messages[message.recipient_id].append(message.message_id)
                
                # Add to type index
                self.type_messages[message.message_type].append(message.message_id)
                
                # Add to status index
                self.status_messages[message.status].append(message.message_id)
                
                # Add to timestamp index
                self.timestamp_index.append((message.timestamp, message.message_id))
                self.timestamp_index.sort(key=lambda x: x[0])  # Sort by timestamp
                
            elif operation == "remove":
                # Remove from agent index
                if message.recipient_id and message.recipient_id != "broadcast":
                    if message.message_id in self.agent_messages[message.recipient_id]:
                        self.agent_messages[message.recipient_id].remove(message.message_id)
                
                # Remove from type index
                if message.message_id in self.type_messages[message.message_type]:
                    self.type_messages[message.message_type].remove(message.message_id)
                
                # Remove from status index
                if message.message_id in self.status_messages[message.status]:
                    self.status_messages[message.status].remove(message.message_id)
                
                # Remove from timestamp index
                self.timestamp_index = [(t, mid) for t, mid in self.timestamp_index if mid != message.message_id]
                
        except Exception as e:
            logger.error(f"Failed to update indexes: {e}")
    
    def cleanup_expired_messages(self, max_age_hours: int = 24) -> int:
        """Clean up expired messages"""
        try:
            cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
            expired_messages = []
            
            with self.lock:
                for message_id, message in list(self.messages.items()):
                    if message.timestamp < cutoff_time:
                        expired_messages.append(message_id)
                
                # Delete expired messages
                for message_id in expired_messages:
                    self.delete_message(message_id)
            
            logger.info(f"Cleaned up {len(expired_messages)} expired messages")
            return len(expired_messages)
            
        except Exception as e:
            logger.error(f"Failed to cleanup expired messages: {e}")
            return 0
    
    def get_storage_stats(self) -> Dict[str, Any]:
        """Get storage statistics"""
        with self.lock:
            return self.storage_stats.copy()
    
    def get_storage_health(self) -> Dict[str, Any]:
        """Get storage health metrics"""
        with self.lock:
            return {
                "total_messages": len(self.messages),
                "index_sizes": {
                    "agent_messages": sum(len(ids) for ids in self.agent_messages.values()),
                    "type_messages": sum(len(ids) for ids in self.type_messages.values()),
                    "status_messages": sum(len(ids) for ids in self.status_messages.values()),
                    "timestamp_index": len(self.timestamp_index)
                },
                "memory_usage_estimate": len(self.messages) * 1024,  # Rough estimate in bytes
                "index_consistency": self._check_index_consistency()
            }
    
    def _check_index_consistency(self) -> bool:
        """Check if indexes are consistent with main storage"""
        try:
            # Check if all indexed message IDs exist in main storage
            all_indexed_ids = set()
            all_indexed_ids.update(self.agent_messages.keys())
            all_indexed_ids.update(self.type_messages.keys())
            all_indexed_ids.update(self.status_messages.keys())
            
            for message_id in all_indexed_ids:
                if message_id not in self.messages:
                    return False
            
            return True
        except Exception:
            return False
