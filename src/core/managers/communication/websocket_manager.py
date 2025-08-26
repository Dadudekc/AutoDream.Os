#!/usr/bin/env python3
"""
WebSocket Manager - V2 Modular Architecture
=========================================

Manages WebSocket connections, listeners, and message handling.
Follows V2 standards: OOP design, SRP, no strict LOC limits.

Author: Agent-4 (Captain)
Task: TASK 4H - Communication Manager Modularization
License: MIT
"""

import logging
import asyncio
import websockets
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
from dataclasses import asdict
from pathlib import Path
import json

from ..base_manager import BaseManager, ManagerStatus, ManagerPriority
from .models import Channel
from .types import CommunicationTypes, CommunicationConfig

logger = logging.getLogger(__name__)


class WebSocketManager(BaseManager):
    """
    WebSocket Manager - Single responsibility: WebSocket connection management
    
    Manages:
    - WebSocket connection lifecycle
    - Message listeners and handlers
    - Connection health monitoring
    - WebSocket-specific operations
    """

    def __init__(self, config_path: str = "config/websocket_manager.json"):
        """Initialize WebSocket manager"""
        super().__init__(
            manager_name="WebSocketManager",
            config_path=config_path,
            enable_metrics=True,
            enable_events=True,
            enable_persistence=True
        )
        
        self.websocket_connections: Dict[str, Any] = {}
        self.connection_metrics: Dict[str, Dict[str, Any]] = {}
        self.message_listeners: Dict[str, asyncio.Task] = {}
        
        # WebSocket settings
        self.default_ping_interval = CommunicationConfig.DEFAULT_PING_INTERVAL
        self.default_ping_timeout = CommunicationConfig.DEFAULT_PING_TIMEOUT
        self.max_connections = CommunicationConfig.MAX_WEBSOCKET_CONNECTIONS
        
        # Initialize WebSocket system
        self._load_manager_config()
    
    def _load_manager_config(self):
        """Load manager-specific configuration"""
        try:
            if Path(self.config_path).exists():
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                    self.default_ping_interval = config.get('ping_interval', 
                                                          CommunicationConfig.DEFAULT_PING_INTERVAL)
                    self.default_ping_timeout = config.get('ping_timeout', 
                                                         CommunicationConfig.DEFAULT_PING_TIMEOUT)
                    self.max_connections = config.get('max_connections', 
                                                    CommunicationConfig.MAX_WEBSOCKET_CONNECTIONS)
            else:
                logger.warning(f"WebSocket config file not found: {self.config_path}")
        except Exception as e:
            logger.error(f"Failed to load WebSocket config: {e}")
    
    async def initialize_websocket_channel(self, channel_id: str, channel: Channel, 
                                         message_handler: Callable) -> bool:
        """Initialize WebSocket channel"""
        try:
            if len(self.websocket_connections) >= self.max_connections:
                logger.error(f"Maximum WebSocket connections reached: {self.max_connections}")
                return False
            
            # Create WebSocket connection
            websocket = await websockets.connect(
                channel.url,
                extra_headers=channel.config.get('headers', {}),
                ping_interval=channel.config.get('ping_interval', self.default_ping_interval),
                ping_timeout=channel.config.get('ping_timeout', self.default_ping_timeout)
            )
            
            self.websocket_connections[channel_id] = websocket
            
            # Initialize connection metrics
            self.connection_metrics[channel_id] = {
                "connected_at": datetime.now().isoformat(),
                "last_ping": datetime.now().isoformat(),
                "last_pong": datetime.now().isoformat(),
                "messages_sent": 0,
                "messages_received": 0,
                "connection_errors": 0,
                "is_healthy": True
            }
            
            # Start message listener
            listener_task = asyncio.create_task(
                self._websocket_message_listener(channel_id, websocket, message_handler)
            )
            self.message_listeners[channel_id] = listener_task
            
            self._emit_event("websocket_connected", {
                "channel_id": channel_id,
                "url": channel.url
            })
            
            logger.info(f"WebSocket channel {channel_id} initialized")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize WebSocket channel {channel_id}: {e}")
            if channel_id in self.connection_metrics:
                self.connection_metrics[channel_id]["connection_errors"] += 1
                self.connection_metrics[channel_id]["is_healthy"] = False
            return False
    
    async def _websocket_message_listener(self, channel_id: str, websocket, 
                                        message_handler: Callable):
        """Listen for WebSocket messages"""
        try:
            async for message in websocket:
                # Update metrics
                if channel_id in self.connection_metrics:
                    self.connection_metrics[channel_id]["messages_received"] += 1
                    self.connection_metrics[channel_id]["last_pong"] = datetime.now().isoformat()
                
                # Process message through handler
                try:
                    await message_handler(channel_id, message)
                except Exception as e:
                    logger.error(f"Message handler error for WebSocket channel {channel_id}: {e}")
                    if channel_id in self.connection_metrics:
                        self.connection_metrics[channel_id]["connection_errors"] += 1
                
        except websockets.exceptions.ConnectionClosed:
            logger.info(f"WebSocket connection closed for channel {channel_id}")
            if channel_id in self.connection_metrics:
                self.connection_metrics[channel_id]["is_healthy"] = False
        except Exception as e:
            logger.error(f"WebSocket message listener error for channel {channel_id}: {e}")
            if channel_id in self.connection_metrics:
                self.connection_metrics[channel_id]["connection_errors"] += 1
                self.connection_metrics[channel_id]["is_healthy"] = False
    
    async def send_websocket_message(self, channel_id: str, message_data: Any) -> bool:
        """Send message through WebSocket channel"""
        try:
            if channel_id not in self.websocket_connections:
                logger.warning(f"WebSocket connection not found for channel {channel_id}")
                return False
            
            websocket = self.websocket_connections[channel_id]
            
            # Serialize message content
            if isinstance(message_data, (dict, list)):
                message_data = json.dumps(message_data)
            else:
                message_data = str(message_data)
            
            # Send message
            await websocket.send(message_data)
            
            # Update metrics
            if channel_id in self.connection_metrics:
                self.connection_metrics[channel_id]["messages_sent"] += 1
                self.connection_metrics[channel_id]["last_ping"] = datetime.now().isoformat()
            
            return True
            
        except Exception as e:
            logger.error(f"WebSocket message send failed: {e}")
            if channel_id in self.connection_metrics:
                self.connection_metrics[channel_id]["connection_errors"] += 1
            return False
    
    def get_websocket_connection_info(self, channel_id: str) -> Optional[Dict[str, Any]]:
        """Get WebSocket connection information"""
        try:
            if channel_id in self.websocket_connections:
                websocket = self.websocket_connections[channel_id]
                return {
                    "channel_id": channel_id,
                    "connected": not websocket.closed,
                    "metrics": self.connection_metrics.get(channel_id, {}),
                    "listener_active": channel_id in self.message_listeners
                }
            return None
        except Exception as e:
            logger.error(f"Failed to get WebSocket connection info for {channel_id}: {e}")
            return None
    
    def get_websocket_statistics(self) -> Dict[str, Any]:
        """Get WebSocket connection statistics"""
        try:
            total_connections = len(self.websocket_connections)
            active_connections = len([
                ch_id for ch_id, metrics in self.connection_metrics.items()
                if metrics.get("is_healthy", False)
            ])
            
            total_messages_sent = sum(
                metrics.get("messages_sent", 0) 
                for metrics in self.connection_metrics.values()
            )
            total_messages_received = sum(
                metrics.get("messages_received", 0) 
                for metrics in self.connection_metrics.values()
            )
            total_errors = sum(
                metrics.get("connection_errors", 0) 
                for metrics in self.connection_metrics.values()
            )
            
            return {
                "total_connections": total_connections,
                "active_connections": active_connections,
                "total_messages_sent": total_messages_sent,
                "total_messages_received": total_messages_received,
                "total_errors": total_errors,
                "connection_metrics": self.connection_metrics
            }
            
        except Exception as e:
            logger.error(f"Failed to get WebSocket statistics: {e}")
            return {}
    
    async def close_websocket_connection(self, channel_id: str) -> bool:
        """Close WebSocket connection"""
        try:
            if channel_id not in self.websocket_connections:
                logger.warning(f"WebSocket connection not found for channel {channel_id}")
                return False
            
            websocket = self.websocket_connections[channel_id]
            
            # Cancel message listener
            if channel_id in self.message_listeners:
                self.message_listeners[channel_id].cancel()
                del self.message_listeners[channel_id]
            
            # Close WebSocket connection
            if not websocket.closed:
                await websocket.close()
            
            # Clean up
            del self.websocket_connections[channel_id]
            if channel_id in self.connection_metrics:
                del self.connection_metrics[channel_id]
            
            self._emit_event("websocket_disconnected", {"channel_id": channel_id})
            logger.info(f"WebSocket connection {channel_id} closed")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to close WebSocket connection {channel_id}: {e}")
            return False
    
    async def health_check_websockets(self) -> Dict[str, bool]:
        """Perform health check on all WebSocket connections"""
        try:
            health_results = {}
            
            for channel_id, websocket in self.websocket_connections.items():
                try:
                    # Check if connection is still open
                    is_healthy = not websocket.closed
                    
                    # Update metrics
                    if channel_id in self.connection_metrics:
                        self.connection_metrics[channel_id]["is_healthy"] = is_healthy
                    
                    health_results[channel_id] = is_healthy
                    
                    if not is_healthy:
                        logger.warning(f"WebSocket connection {channel_id} is unhealthy")
                        
                except Exception as e:
                    logger.error(f"Health check failed for WebSocket {channel_id}: {e}")
                    health_results[channel_id] = False
                    
                    if channel_id in self.connection_metrics:
                        self.connection_metrics[channel_id]["is_healthy"] = False
            
            return health_results
            
        except Exception as e:
            logger.error(f"WebSocket health check failed: {e}")
            return {}

