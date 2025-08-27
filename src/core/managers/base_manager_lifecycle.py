#!/usr/bin/env python3
"""
Base Manager Lifecycle - Agent Cellphone V2
==========================================

Lifecycle management functionality for the base manager system.
Extracted from base_manager.py to follow Single Responsibility Principle.

**Author:** Agent-3 (Integration & Testing)
**Created:** Current Sprint
**Status:** ACTIVE - REFACTORING IN PROGRESS
"""

import logging
import time
from datetime import datetime
from typing import Optional

from .base_manager_types import ManagerStatus


class BaseManagerLifecycle:
    """
    Lifecycle management functionality for base managers.
    
    Handles start, stop, restart, and status transitions.
    """
    
    def __init__(self, manager_id: str, logger: logging.Logger):
        self.manager_id = manager_id
        self.logger = logger
        self.running = False
        self.startup_time: Optional[datetime] = None
        self.shutdown_time: Optional[datetime] = None
        self.status = ManagerStatus.OFFLINE
    
    def start(self, on_start_callback, initialize_resources_callback, start_heartbeat_callback) -> bool:
        """Start the manager - common lifecycle method"""
        try:
            if self.running:
                self.logger.warning(f"Manager {self.manager_id} is already running")
                return True
            
            self.logger.info(f"Starting manager: {self.manager_id}")
            self.status = ManagerStatus.INITIALIZING
            
            # Initialize resources
            if not initialize_resources_callback():
                raise RuntimeError("Failed to initialize resources")
            
            # Start heartbeat monitoring
            start_heartbeat_callback()
            
            # Call subclass-specific startup
            if not on_start_callback():
                raise RuntimeError("Subclass startup failed")
            
            self.running = True
            self.status = ManagerStatus.ONLINE
            self.startup_time = datetime.now()
            
            self.logger.info(f"Manager {self.manager_id} started successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start manager {self.manager_id}: {e}")
            self.status = ManagerStatus.ERROR
            return False
    
    def stop(self, on_stop_callback, stop_heartbeat_callback, cleanup_resources_callback) -> bool:
        """Stop the manager - common lifecycle method"""
        try:
            if not self.running:
                self.logger.warning(f"Manager {self.manager_id} is not running")
                return True
            
            self.logger.info(f"Stopping manager: {self.manager_id}")
            self.status = ManagerStatus.SHUTTING_DOWN
            
            # Stop heartbeat monitoring
            stop_heartbeat_callback()
            
            # Call subclass-specific shutdown
            on_stop_callback()
            
            # Cleanup resources
            cleanup_resources_callback()
            
            self.running = False
            self.status = ManagerStatus.OFFLINE
            self.shutdown_time = datetime.now()
            
            self.logger.info(f"Manager {self.manager_id} stopped successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to stop manager {self.manager_id}: {e}")
            self.status = ManagerStatus.ERROR
            return False
    
    def restart(self, stop_callback, start_callback) -> bool:
        """Restart the manager - common lifecycle method"""
        try:
            self.logger.info(f"Restarting manager: {self.manager_id}")
            
            if not stop_callback():
                return False
            
            # Wait a moment for cleanup
            time.sleep(1)
            
            if not start_callback():
                return False
            
            self.logger.info(f"Manager {self.manager_id} restarted successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to restart manager {self.manager_id}: {e}")
            return False
    
    def get_lifecycle_status(self) -> dict:
        """Get lifecycle-specific status information"""
        return {
            "running": self.running,
            "startup_time": self.startup_time.isoformat() if self.startup_time else None,
            "shutdown_time": self.shutdown_time.isoformat() if self.shutdown_time else None,
            "status": self.status.value
        }
