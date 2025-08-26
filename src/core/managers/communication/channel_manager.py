#!/usr/bin/env python3
"""
Channel Manager - V2 Modular Architecture
========================================

Manages communication channels and their lifecycle.
Follows V2 standards: OOP design, SRP, no strict LOC limits.

Author: Agent-4 (Captain)
Task: TASK 4H - Communication Manager Modularization
License: MIT
"""

import logging
import json
import asyncio
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import asdict

from ..base_manager import BaseManager, ManagerStatus, ManagerPriority
from .models import Channel, ChannelType
from .types import CommunicationTypes, CommunicationConfig

logger = logging.getLogger(__name__)


class ChannelManager(BaseManager):
    """
    Channel Manager - Single responsibility: Channel lifecycle management
    
    Manages:
    - Channel creation and initialization
    - Channel status monitoring
    - Channel configuration
    - Channel statistics
    """

    def __init__(self, config_path: str = "config/channel_manager.json"):
        """Initialize channel manager"""
        super().__init__(
            manager_name="ChannelManager",
            config_path=config_path,
            enable_metrics=True,
            enable_events=True,
            enable_persistence=True
        )
        
        self.channels: Dict[str, Channel] = {}
        self.channel_stats: Dict[str, Dict[str, Any]] = {}
        
        # Initialize channel system
        self._load_manager_config()
        self._setup_default_channels()
    
    def _load_manager_config(self):
        """Load manager-specific configuration"""
        try:
            if Path(self.config_path).exists():
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                    self.default_timeout = config.get('default_timeout', CommunicationConfig.DEFAULT_TIMEOUT)
                    self.default_retry_count = config.get('default_retry_count', CommunicationConfig.DEFAULT_RETRY_COUNT)
            else:
                logger.warning(f"Channel config file not found: {self.config_path}")
        except Exception as e:
            logger.error(f"Failed to load channel config: {e}")

    def _setup_default_channels(self):
        """Setup default communication channels"""
        # HTTP channel
        http_channel = Channel(
            id="http_default",
            name="Default HTTP",
            type=ChannelType.HTTP,
            url="http://localhost:8000",
            config={"timeout": self.default_timeout, "retry_count": self.default_retry_count},
            status=CommunicationTypes.ChannelStatus.ACTIVE.value,
            created_at=datetime.now().isoformat(),
            last_used=datetime.now().isoformat(),
            message_count=0,
            error_count=0
        )
        self.channels["http_default"] = http_channel
        
        # Initialize stats
        self.channel_stats["http_default"] = {
            "total_messages": 0,
            "successful_messages": 0,
            "failed_messages": 0,
            "last_activity": datetime.now().isoformat(),
            "uptime_percentage": 100.0,
            "average_response_time": 0.0,
            "error_rate": 0.0
        }
    
    async def create_channel(self, name: str, channel_type: ChannelType, url: str,
                           config: Optional[Dict[str, Any]] = None) -> str:
        """Create a new communication channel"""
        try:
            channel_id = f"{channel_type.value}_{name}_{len(self.channels)}"
            
            channel = Channel(
                id=channel_id,
                name=name,
                type=channel_type,
                url=url,
                config=config or {},
                status=CommunicationTypes.ChannelStatus.ACTIVE.value,
                created_at=datetime.now().isoformat(),
                last_used=datetime.now().isoformat(),
                message_count=0,
                error_count=0
            )
            
            self.channels[channel_id] = channel
            
            # Initialize stats
            self.channel_stats[channel_id] = {
                "total_messages": 0,
                "successful_messages": 0,
                "failed_messages": 0,
                "last_activity": datetime.now().isoformat(),
                "uptime_percentage": 100.0,
                "average_response_time": 0.0,
                "error_rate": 0.0
            }
            
            self._emit_event("channel_created", {
                "channel_id": channel_id,
                "name": name,
                "type": channel_type.value,
                "url": url
            })
            
            logger.info(f"Channel created: {name} (ID: {channel_id})")
            return channel_id
            
        except Exception as e:
            logger.error(f"Failed to create channel: {e}")
            return ""
    
    def get_channel_info(self, channel_id: str) -> Optional[Channel]:
        """Get channel information"""
        try:
            return self.channels.get(channel_id)
        except Exception as e:
            logger.error(f"Failed to get channel info for {channel_id}: {e}")
            return None
    
    def get_active_channels(self) -> List[Channel]:
        """Get list of active channels"""
        try:
            return [
                channel for channel in self.channels.values()
                if channel.status == CommunicationTypes.ChannelStatus.ACTIVE.value
            ]
        except Exception as e:
            logger.error(f"Failed to get active channels: {e}")
            return []
    
    def update_channel_status(self, channel_id: str, status: str) -> bool:
        """Update channel status"""
        try:
            if channel_id in self.channels:
                self.channels[channel_id].status = status
                self.channels[channel_id].last_used = datetime.now().isoformat()
                
                # Update stats
                if channel_id in self.channel_stats:
                    self.channel_stats[channel_id]["last_activity"] = datetime.now().isoformat()
                
                self._emit_event("channel_status_updated", {
                    "channel_id": channel_id,
                    "status": status
                })
                
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to update channel status: {e}")
            return False
    
    def get_channel_statistics(self) -> Dict[str, Any]:
        """Get channel statistics"""
        try:
            total_channels = len(self.channels)
            active_channels = len([c for c in self.channels.values() 
                                 if c.status == CommunicationTypes.ChannelStatus.ACTIVE.value])
            total_messages = sum(c.message_count for c in self.channels.values())
            total_errors = sum(c.error_count for c in self.channels.values())
            
            # Count by type
            type_counts = {}
            for channel in self.channels.values():
                type_name = channel.type.value
                type_counts[type_name] = type_counts.get(type_name, 0) + 1
            
            return {
                "total_channels": total_channels,
                "active_channels": active_channels,
                "total_messages": total_messages,
                "total_errors": total_errors,
                "type_distribution": type_counts,
                "channel_stats": self.channel_stats
            }
            
        except Exception as e:
            logger.error(f"Failed to get channel statistics: {e}")
            return {}
    
    async def close_channel(self, channel_id: str) -> bool:
        """Close a communication channel"""
        try:
            if channel_id not in self.channels:
                logger.warning(f"Channel not found: {channel_id}")
                return False
            
            self.channels[channel_id].status = CommunicationTypes.ChannelStatus.CLOSED.value
            
            self._emit_event("channel_closed", {"channel_id": channel_id})
            logger.info(f"Channel {channel_id} closed")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to close channel {channel_id}: {e}")
            return False

