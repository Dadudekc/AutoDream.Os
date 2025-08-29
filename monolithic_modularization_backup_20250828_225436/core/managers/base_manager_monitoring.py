#!/usr/bin/env python3
"""
Base Manager Monitoring - Agent Cellphone V2
===========================================

Monitoring and status functionality for the base manager system.
Extracted from base_manager.py to follow Single Responsibility Principle.

**Author:** Agent-3 (Integration & Testing)
**Created:** Current Sprint
**Status:** ACTIVE - REFACTORING IN PROGRESS
"""

import logging
from datetime import datetime
from typing import Dict, Any, Optional

from .base_manager_types import ManagerStatus


class BaseManagerMonitoring:
    """
    Monitoring and status functionality for base managers.
    
    Handles health checks, status reporting, and performance metrics.
    """
    
    def __init__(self, manager_id: str, name: str, logger: logging.Logger):
        self.manager_id = manager_id
        self.name = name
        self.logger = logger
        self.last_heartbeat = datetime.now()
        self.heartbeat_interval = 30
        self.error_count = 0
        self.last_error: Optional[str] = None
        self.recovery_attempts = 0
        self.max_retries = 3
    
    def get_status(self, lifecycle_status: dict, metrics: dict) -> Dict[str, Any]:
        """Get comprehensive manager status - common monitoring method"""
        return {
            "manager_id": self.manager_id,
            "name": self.name,
            **lifecycle_status,
            "uptime_seconds": metrics.get("uptime_seconds", 0.0),
            "operations_processed": metrics.get("operations_processed", 0),
            "errors_count": metrics.get("errors_count", 0),
            "last_operation": metrics.get("last_operation"),
            "performance_score": metrics.get("performance_score", 0.0),
            "last_heartbeat": self.last_heartbeat.isoformat(),
            "recovery_attempts": self.recovery_attempts,
            "last_error": self.last_error
        }
    
    def is_healthy(self, running: bool) -> bool:
        """Check if manager is healthy - common health check method"""
        if not running:
            return False
        
        # Check heartbeat
        if (datetime.now() - self.last_heartbeat).total_seconds() > self.heartbeat_interval * 2:
            return False
        
        # Check error threshold
        if self.error_count > self.max_retries:
            return False
        
        return True
    
    def update_heartbeat(self):
        """Update heartbeat timestamp"""
        self.last_heartbeat = datetime.now()
    
    def record_error(self, error: str):
        """Record an error occurrence"""
        self.last_error = error
        self.error_count += 1
    
    def reset_error_count(self):
        """Reset error count after successful recovery"""
        self.error_count = 0
        self.last_error = None
    
    def increment_recovery_attempts(self):
        """Increment recovery attempt counter"""
        self.recovery_attempts += 1
    
    def get_monitoring_status(self) -> dict:
        """Get monitoring-specific status information"""
        return {
            "last_heartbeat": self.last_heartbeat.isoformat(),
            "error_count": self.error_count,
            "last_error": self.last_error,
            "recovery_attempts": self.recovery_attempts,
            "max_retries": self.max_retries
        }

