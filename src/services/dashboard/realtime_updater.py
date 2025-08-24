#!/usr/bin/env python3
"""
Real-time Updater - V2 Dashboard System

This module handles real-time updates and WebSocket communication.
Follows V2 coding standards: ≤200 LOC, OOP design, SRP
"""

import json
import logging
import asyncio
from typing import Dict, Any, List, Callable, Optional


class RealTimeUpdater:
    """Real-time updater for dashboard components."""
    
    def __init__(self, websocket_url: str = "ws://localhost:8080/ws"):
        self.websocket_url = websocket_url
        self.websocket = None
        self.update_callbacks: List[Callable] = []
        self.is_connected = False
        self.reconnect_attempts = 0
        self.max_reconnect_attempts = 5
        self.reconnect_delay = 1.0  # seconds
        
        self.logger = logging.getLogger(f"{__name__}.RealTimeUpdater")
        self.logger.info("Real-time updater initialized")
    
    def add_update_callback(self, callback: Callable):
        """Add callback for real-time updates."""
        if callback not in self.update_callbacks:
            self.update_callbacks.append(callback)
            self.logger.info(f"Added update callback: {callback.__name__ if hasattr(callback, '__name__') else 'anonymous'}")
    
    def remove_update_callback(self, callback: Callable):
        """Remove callback for real-time updates."""
        if callback in self.update_callbacks:
            self.update_callbacks.remove(callback)
            self.logger.info(f"Removed update callback: {callback.__name__ if hasattr(callback, '__name__') else 'anonymous'}")
    
    async def connect(self):
        """Establish WebSocket connection."""
        try:
            # In a real implementation, this would use a WebSocket library
            # For now, we'll simulate the connection
            self.logger.info(f"Attempting to connect to {self.websocket_url}")
            
            # Simulate connection delay
            await asyncio.sleep(0.1)
            
            self.is_connected = True
            self.reconnect_attempts = 0
            self.logger.info("WebSocket connection established")
            
            # Start listening for messages
            asyncio.create_task(self._listen_for_messages())
            
        except Exception as e:
            self.logger.error(f"Failed to connect to WebSocket: {e}")
            self.is_connected = False
            await self._handle_reconnection()
    
    async def disconnect(self):
        """Close WebSocket connection."""
        try:
            if self.websocket:
                # In a real implementation, this would close the WebSocket
                pass
            
            self.is_connected = False
            self.logger.info("WebSocket connection closed")
            
        except Exception as e:
            self.logger.error(f"Error disconnecting WebSocket: {e}")
    
    async def send_update(self, data: Dict[str, Any]):
        """Send update through WebSocket."""
        if not self.is_connected:
            self.logger.warning("Cannot send update: WebSocket not connected")
            return False
        
        try:
            # In a real implementation, this would send through WebSocket
            message = json.dumps(data)
            self.logger.debug(f"Sending update: {message}")
            
            # Simulate sending delay
            await asyncio.sleep(0.01)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error sending WebSocket update: {e}")
            return False
    
    def trigger_callbacks(self, data: Dict[str, Any]):
        """Trigger all update callbacks."""
        if not self.update_callbacks:
            return
        
        self.logger.debug(f"Triggering {len(self.update_callbacks)} callbacks with data: {data}")
        
        for callback in self.update_callbacks:
            try:
                callback(data)
            except Exception as e:
                self.logger.error(f"Error in update callback: {e}")
    
    async def broadcast_update(self, update_type: str, payload: Dict[str, Any]):
        """Broadcast update to all connected clients."""
        data = {
            "type": update_type,
            "timestamp": self._get_timestamp(),
            "payload": payload
        }
        
        success = await self.send_update(data)
        if success:
            self.trigger_callbacks(data)
        
        return success
    
    async def _listen_for_messages(self):
        """Listen for incoming WebSocket messages."""
        while self.is_connected:
            try:
                # In a real implementation, this would listen for actual messages
                # For now, we'll simulate receiving messages periodically
                await asyncio.sleep(5.0)  # Check every 5 seconds
                
                # Simulate receiving a heartbeat message
                if self.is_connected:
                    heartbeat_data = {
                        "type": "heartbeat",
                        "timestamp": self._get_timestamp(),
                        "payload": {"status": "alive"}
                    }
                    self.trigger_callbacks(heartbeat_data)
                
            except Exception as e:
                self.logger.error(f"Error listening for messages: {e}")
                break
        
        self.logger.info("Stopped listening for messages")
    
    async def _handle_reconnection(self):
        """Handle WebSocket reconnection logic."""
        if self.reconnect_attempts >= self.max_reconnect_attempts:
            self.logger.error("Max reconnection attempts reached")
            return
        
        self.reconnect_attempts += 1
        delay = self.reconnect_delay * (2 ** (self.reconnect_attempts - 1))  # Exponential backoff
        
        self.logger.info(f"Attempting reconnection in {delay:.1f}s (attempt {self.reconnect_attempts}/{self.max_reconnect_attempts})")
        
        await asyncio.sleep(delay)
        await self.connect()
    
    def _get_timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        import datetime
        return datetime.datetime.now().isoformat()
    
    def get_connection_status(self) -> Dict[str, Any]:
        """Get current connection status."""
        return {
            "connected": self.is_connected,
            "websocket_url": self.websocket_url,
            "reconnect_attempts": self.reconnect_attempts,
            "callback_count": len(self.update_callbacks)
        }
    
    def health_check(self) -> bool:
        """Perform health check on the real-time updater."""
        try:
            # Basic health check
            status = self.get_connection_status()
            self.logger.debug(f"Health check status: {status}")
            return True
        except Exception as e:
            self.logger.error(f"Health check failed: {e}")
            return False


