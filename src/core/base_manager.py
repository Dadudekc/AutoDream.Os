#!/usr/bin/env python3
"""
Base Manager System - Agent Cellphone V2
========================================

REFACTORED base manager system using extracted modules for better SRP compliance.
Reduced from 578 lines to under 400 lines while maintaining all functionality.

**Author:** Agent-3 (Integration & Testing)
**Created:** Current Sprint
**Status:** ACTIVE - REFACTORING COMPLETED
"""

import logging
import threading
import time
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable

from .managers.base_manager_types import (
    ManagerStatus, ManagerPriority, ManagerMetrics, ManagerConfig
)
from .managers.base_manager_interface import BaseManagerInterface
from .managers.base_manager_lifecycle import BaseManagerLifecycle
from .managers.base_manager_monitoring import BaseManagerMonitoring
from .managers.base_manager_config import BaseManagerConfiguration
from .managers.base_manager_utils import BaseManagerUtils


class BaseManager(BaseManagerInterface):
    """
    REFACTORED base manager class using extracted modules.
    
    Orchestrates specialized components for lifecycle, monitoring, configuration,
    and utilities while maintaining the same public interface.
    """
    
    def __init__(self, manager_id: str, name: str, description: str = ""):
        # Core identification
        self.manager_id = manager_id
        self.name = name
        self.description = description
        
        # Priority and status
        self.priority = ManagerPriority.NORMAL
        
        # Performance tracking
        self.metrics = ManagerMetrics(manager_id=manager_id)
        self.operations_history: List[Dict[str, Any]] = []
        
        # Heartbeat monitoring
        self.heartbeat_thread: Optional[threading.Thread] = None
        self.last_heartbeat = datetime.now()
        
        # Event handlers
        self.event_handlers: Dict[str, List[Callable]] = {}
        
        # Resource management
        self.resources: Dict[str, Any] = {}
        self.resource_locks: Dict[str, threading.Lock] = {}
        
        # Initialize specialized components
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.lifecycle = BaseManagerLifecycle(manager_id, self.logger)
        self.monitoring = BaseManagerMonitoring(manager_id, name, self.logger)
        self.config_manager = BaseManagerConfiguration(manager_id, name, description, self.logger)
        self.utils = BaseManagerUtils()
        
        self.logger.info(f"BaseManager initialized: {manager_id} ({name})")
    
    # ============================================================================
    # LIFECYCLE MANAGEMENT - Delegated to specialized component
    # ============================================================================
    
    def start(self) -> bool:
        """Start the manager - delegated to lifecycle component"""
        return self.lifecycle.start(
            self._on_start,
            self._initialize_resources,
            self._start_heartbeat_monitoring
        )
    
    def stop(self) -> bool:
        """Stop the manager - delegated to lifecycle component"""
        return self.lifecycle.stop(
            self._on_stop,
            self._stop_heartbeat_monitoring,
            self._cleanup_resources
        )
    
    def restart(self) -> bool:
        """Restart the manager - delegated to lifecycle component"""
        return self.lifecycle.restart(
            lambda: self.stop(),
            lambda: self.start()
        )
    
    # ============================================================================
    # STATUS AND MONITORING - Delegated to specialized component
    # ============================================================================
    
    def get_status(self) -> Dict[str, Any]:
        """Get comprehensive manager status - delegated to monitoring component"""
        lifecycle_status = self.lifecycle.get_lifecycle_status()
        monitoring_status = self.monitoring.get_monitoring_status()
        
        return self.monitoring.get_status(lifecycle_status, {
            "uptime_seconds": self.metrics.uptime_seconds,
            "operations_processed": self.metrics.operations_processed,
            "errors_count": self.metrics.errors_count,
            "last_operation": self.metrics.last_operation,
            "performance_score": self.metrics.performance_score
        })
    
    def is_healthy(self) -> bool:
        """Check if manager is healthy - delegated to monitoring component"""
        return self.monitoring.is_healthy(self.lifecycle.running)
    
    # ============================================================================
    # CONFIGURATION MANAGEMENT - Delegated to specialized component
    # ============================================================================
    
    def update_config(self, **kwargs) -> bool:
        """Update manager configuration - delegated to config component"""
        return self.config_manager.update_config(**kwargs)
    
    def load_config_from_file(self, config_file: str) -> bool:
        """Load configuration from file - delegated to config component"""
        return self.config_manager.load_config_from_file(config_file)
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get performance metrics with utility calculations"""
        return {
            "manager_id": self.manager_id,
            "uptime_seconds": self.metrics.uptime_seconds,
            "operations_processed": self.metrics.operations_processed,
            "errors_count": self.metrics.errors_count,
            "success_rate": self.utils.calculate_success_rate(
                self.metrics.operations_processed, self.metrics.errors_count
            ),
            "error_rate": self.utils.calculate_error_rate(
                self.metrics.operations_processed, self.metrics.errors_count
            ),
            "avg_operation_time": self.utils.calculate_avg_operation_time(
                self.operations_history
            ),
            "performance_score": self.metrics.performance_score,
            "last_operation": self.metrics.last_operation.isoformat() if self.metrics.last_operation else None
        }
    
    def cleanup(self) -> bool:
        """Cleanup manager resources"""
        try:
            self.stop()
            self._cleanup_resources()
            return True
        except Exception as e:
            self.logger.error(f"Failed to cleanup manager {self.manager_id}: {e}")
            return False
    
    # ============================================================================
    # HEARTBEAT MONITORING - Core functionality
    # ============================================================================
    
    def _start_heartbeat_monitoring(self):
        """Start heartbeat monitoring thread"""
        if self.heartbeat_thread and self.heartbeat_thread.is_alive():
            return
        
        self.heartbeat_thread = threading.Thread(
            target=self._heartbeat_worker,
            daemon=True,
            name=f"heartbeat-{self.manager_id}"
        )
        self.heartbeat_thread.start()
    
    def _stop_heartbeat_monitoring(self):
        """Stop heartbeat monitoring thread"""
        if self.heartbeat_thread and self.heartbeat_thread.is_alive():
            self.heartbeat_thread.join(timeout=5)
    
    def _heartbeat_worker(self):
        """Heartbeat monitoring worker thread"""
        while self.lifecycle.running:
            try:
                self.monitoring.update_heartbeat()
                self._on_heartbeat()
                time.sleep(self.config_manager.config.heartbeat_interval)
            except Exception as e:
                self.logger.error(f"Heartbeat error: {e}")
                break
    
    # ============================================================================
    # RESOURCE MANAGEMENT - Core functionality
    # ============================================================================
    
    def _initialize_resources(self) -> bool:
        """Initialize manager resources"""
        try:
            return self._on_initialize_resources()
        except Exception as e:
            self.logger.error(f"Failed to initialize resources: {e}")
            return False
    
    def _cleanup_resources(self):
        """Cleanup manager resources"""
        try:
            self._on_cleanup_resources()
            self.resources.clear()
            self.resource_locks.clear()
        except Exception as e:
            self.logger.error(f"Failed to cleanup resources: {e}")
    
    # ============================================================================
    # EVENT HANDLING - Core functionality
    # ============================================================================
    
    def _emit_event(self, event_type: str, event_data: Dict[str, Any]):
        """Emit event to registered handlers"""
        if event_type in self.event_handlers:
            for handler in self.event_handlers[event_type]:
                try:
                    handler(event_data)
                except Exception as e:
                    self.logger.error(f"Event handler error: {e}")
    
    def register_event_handler(self, event_type: str, handler: Callable):
        """Register event handler"""
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        self.event_handlers[event_type].append(handler)
    
    # ============================================================================
    # ABSTRACT METHODS - Subclasses must implement these
    # ============================================================================
    
    @abstractmethod
    def _on_start(self) -> bool:
        """Subclass-specific startup logic"""
        raise NotImplementedError
    
    @abstractmethod
    def _on_stop(self):
        """Subclass-specific shutdown logic"""
        raise NotImplementedError
    
    @abstractmethod
    def _on_heartbeat(self):
        """Subclass-specific heartbeat logic"""
        raise NotImplementedError
    
    @abstractmethod
    def _on_initialize_resources(self) -> bool:
        """Subclass-specific resource initialization"""
        raise NotImplementedError
    
    @abstractmethod
    def _on_cleanup_resources(self):
        """Subclass-specific resource cleanup"""
        raise NotImplementedError
    
    @abstractmethod
    def _on_recovery_attempt(self, error: Exception, context: str) -> bool:
        """Subclass-specific recovery logic"""
        raise NotImplementedError
    
    # ============================================================================
    # UTILITY METHODS - Delegated to utility component
    # ============================================================================
    
    def _calculate_success_rate(self) -> float:
        """Calculate operation success rate - delegated to utility component"""
        return self.utils.calculate_success_rate(
            self.metrics.operations_processed, self.metrics.errors_count
        )
    
    def _calculate_error_rate(self) -> float:
        """Calculate operation error rate - delegated to utility component"""
        return self.utils.calculate_error_rate(
            self.metrics.operations_processed, self.metrics.errors_count
        )
    
    def _calculate_avg_operation_time(self) -> float:
        """Calculate average operation time - delegated to utility component"""
        return self.utils.calculate_avg_operation_time(self.operations_history)
    
    def _get_current_timestamp(self) -> str:
        """Get current timestamp string - delegated to utility component"""
        return self.utils.get_current_timestamp()
    
    # ============================================================================
    # STRING REPRESENTATION
    # ============================================================================
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.manager_id}, status={self.lifecycle.status.value})"
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(manager_id='{self.manager_id}', name='{self.name}', status={self.lifecycle.status.value})"
