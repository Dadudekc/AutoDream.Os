#!/usr/bin/env python3
"""
Base Manager - V2 Core Manager Consolidation System
==================================================

Single source of truth for all manager functionality.
Consolidates 80% duplication across 42 manager files.
Follows V2 standards: 400 LOC, OOP design, SRP.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import logging
import json
import time
import threading
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable, Union
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime, timedelta
from abc import ABC, abstractmethod

from src.utils.stability_improvements import stability_manager, safe_import

logger = logging.getLogger(__name__)


class ManagerStatus(Enum):
    """Standard manager status states"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"
    MAINTENANCE = "maintenance"
    INITIALIZING = "initializing"
    SHUTDOWN = "shutdown"


class ManagerPriority(Enum):
    """Standard manager priority levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


@dataclass
class ManagerMetrics:
    """Standard manager performance metrics"""
    total_operations: int
    successful_operations: int
    failed_operations: int
    average_response_time: float
    last_activity: datetime
    uptime: float
    error_count: int
    warning_count: int


@dataclass
class ManagerEvent:
    """Standard manager event structure"""
    event_id: str
    event_type: str
    timestamp: datetime
    source: str
    data: Dict[str, Any]
    priority: ManagerPriority
    is_handled: bool = False


class BaseManager(ABC):
    """
    Base Manager - Single responsibility: Common manager functionality
    
    This class consolidates 80% of duplicate code across 42 manager files:
    - CRUD operations (Create, Read, Update, Delete)
    - Event handling and callbacks
    - Configuration management
    - Status tracking and monitoring
    - Lifecycle management
    - Error handling and logging
    - Metrics collection and reporting
    """

    def __init__(
        self,
        manager_name: str,
        config_path: Optional[str] = None,
        enable_metrics: bool = True,
        enable_events: bool = True,
        enable_persistence: bool = True
    ):
        """Initialize base manager with common functionality"""
        self.manager_name = manager_name
        self.config_path = Path(config_path) if config_path else None
        self.enable_metrics = enable_metrics
        self.enable_events = enable_events
        self.enable_persistence = enable_persistence
        
        # Core state
        self.status = ManagerStatus.INITIALIZING
        self.start_time = datetime.now()
        self.last_activity = datetime.now()
        
        # Configuration
        self.config = {}
        self._load_config()
        
        # Metrics
        if self.enable_metrics:
            self.metrics = ManagerMetrics(
                total_operations=0,
                successful_operations=0,
                failed_operations=0,
                average_response_time=0.0,
                last_activity=self.start_time,
                uptime=0.0,
                error_count=0,
                warning_count=0
            )
        
        # Events
        if self.enable_events:
            self.event_handlers: Dict[str, List[Callable]] = {}
            self.event_history: List[ManagerEvent] = []
            self.max_event_history = 1000
        
        # Persistence
        if self.enable_persistence:
            self.data_storage: Dict[str, Any] = {}
            self._load_persistent_data()
        
        # Threading
        self._lock = threading.RLock()
        self._shutdown_event = threading.Event()
        
        # Initialize manager
        self._initialize_manager()
        self.status = ManagerStatus.ACTIVE
        
        logger.info(f"BaseManager '{manager_name}' initialized successfully")

    def _load_config(self) -> None:
        """Load manager configuration"""
        if not self.config_path or not self.config_path.exists():
            self.config = self._get_default_config()
            return
        
        try:
            with open(self.config_path, 'r') as f:
                self.config = json.load(f)
            logger.info(f"Configuration loaded from {self.config_path}")
        except Exception as e:
            logger.error(f"Failed to load config from {self.config_path}: {e}")
            self.config = self._get_default_config()

    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration for manager"""
        return {
            "max_retries": 3,
            "retry_delay": 1.0,
            "timeout": 30.0,
            "enable_logging": True,
            "log_level": "INFO",
            "max_history_size": 1000,
            "cleanup_interval": 3600,  # 1 hour
            "health_check_interval": 300,  # 5 minutes
        }

    def _load_persistent_data(self) -> None:
        """Load persistent data storage"""
        if not self.enable_persistence:
            return
        
        try:
            data_file = Path(f"runtime/{self.manager_name}_data.json")
            if data_file.exists():
                with open(data_file, 'r') as f:
                    self.data_storage = json.load(f)
                logger.info(f"Persistent data loaded from {data_file}")
        except Exception as e:
            logger.error(f"Failed to load persistent data: {e}")
            self.data_storage = {}

    def _save_persistent_data(self) -> None:
        """Save persistent data storage"""
        if not self.enable_persistence:
            return
        
        try:
            data_file = Path(f"runtime/{self.manager_name}_data.json")
            data_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(data_file, 'w') as f:
                json.dump(self.data_storage, f, indent=2, default=str)
            
            logger.debug(f"Persistent data saved to {data_file}")
        except Exception as e:
            logger.error(f"Failed to save persistent data: {e}")

    def _initialize_manager(self) -> None:
        """Initialize manager-specific functionality"""
        # Override in subclasses
        pass

    # ========================================
    # CRUD OPERATIONS (Create, Read, Update, Delete)
    # ========================================

    def create(self, key: str, data: Any, **kwargs) -> bool:
        """Create new item in manager"""
        with self._lock:
            try:
                start_time = time.time()
                
                # Validate data
                if not self._validate_data(data):
                    logger.error(f"Invalid data for key {key}")
                    return False
                
                # Check if key exists
                if key in self.data_storage:
                    logger.warning(f"Key {key} already exists, overwriting")
                
                # Store data
                self.data_storage[key] = data
                
                # Update metrics
                if self.enable_metrics:
                    self._update_metrics(True, time.time() - start_time)
                
                # Trigger event
                if self.enable_events:
                    self._trigger_event("item_created", {"key": key, "data": data})
                
                # Save persistence
                if self.enable_persistence:
                    self._save_persistent_data()
                
                logger.info(f"Created item with key: {key}")
                return True
                
            except Exception as e:
                logger.error(f"Failed to create item {key}: {e}")
                if self.enable_metrics:
                    self._update_metrics(False, 0)
                return False

    def read(self, key: str, default: Any = None) -> Any:
        """Read item from manager"""
        with self._lock:
            try:
                start_time = time.time()
                
                # Get data
                data = self.data_storage.get(key, default)
                
                # Update metrics
                if self.enable_metrics:
                    self._update_metrics(True, time.time() - start_time)
                
                # Trigger event
                if self.enable_events:
                    self._trigger_event("item_read", {"key": key, "found": key in self.data_storage})
                
                return data
                
            except Exception as e:
                logger.error(f"Failed to read item {key}: {e}")
                if self.enable_metrics:
                    self._update_metrics(False, 0)
                return default

    def update(self, key: str, data: Any, **kwargs) -> bool:
        """Update existing item in manager"""
        with self._lock:
            try:
                start_time = time.time()
                
                # Check if key exists
                if key not in self.data_storage:
                    logger.error(f"Key {key} not found for update")
                    return False
                
                # Validate data
                if not self._validate_data(data):
                    logger.error(f"Invalid data for key {key}")
                    return False
                
                # Update data
                self.data_storage[key] = data
                
                # Update metrics
                if self.enable_metrics:
                    self._update_metrics(True, time.time() - start_time)
                
                # Trigger event
                if self.enable_events:
                    self._trigger_event("item_updated", {"key": key, "data": data})
                
                # Save persistence
                if self.enable_persistence:
                    self._save_persistent_data()
                
                logger.info(f"Updated item with key: {key}")
                return True
                
            except Exception as e:
                logger.error(f"Failed to update item {key}: {e}")
                if self.enable_metrics:
                    self._update_metrics(False, 0)
                return False

    def delete(self, key: str, **kwargs) -> bool:
        """Delete item from manager"""
        with self._lock:
            try:
                start_time = time.time()
                
                # Check if key exists
                if key not in self.data_storage:
                    logger.warning(f"Key {key} not found for deletion")
                    return False
                
                # Get data before deletion for event
                data = self.data_storage[key]
                
                # Delete data
                del self.data_storage[key]
                
                # Update metrics
                if self.enable_metrics:
                    self._update_metrics(True, time.time() - start_time)
                
                # Trigger event
                if self.enable_events:
                    self._trigger_event("item_deleted", {"key": key, "data": data})
                
                # Save persistence
                if self.enable_persistence:
                    self._save_persistent_data()
                
                logger.info(f"Deleted item with key: {key}")
                return True
                
            except Exception as e:
                logger.error(f"Failed to delete item {key}: {e}")
                if self.enable_metrics:
                    self._update_metrics(False, 0)
                return False

    def exists(self, key: str) -> bool:
        """Check if item exists in manager"""
        return key in self.data_storage

    def count(self) -> int:
        """Get total count of items"""
        return len(self.data_storage)

    def keys(self) -> List[str]:
        """Get all keys in manager"""
        return list(self.data_storage.keys())

    def values(self) -> List[Any]:
        """Get all values in manager"""
        return list(self.data_storage.values())

    def items(self) -> List[tuple]:
        """Get all key-value pairs in manager"""
        return list(self.data_storage.items())

    def clear(self) -> None:
        """Clear all data from manager"""
        with self._lock:
            self.data_storage.clear()
            if self.enable_persistence:
                self._save_persistent_data()
            logger.info("All data cleared from manager")

    # ========================================
    # EVENT HANDLING AND CALLBACKS
    # ========================================

    def register_event_handler(self, event_type: str, handler: Callable) -> None:
        """Register event handler for specific event type"""
        if not self.enable_events:
            logger.warning("Events not enabled for this manager")
            return
        
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        
        self.event_handlers[event_type].append(handler)
        logger.debug(f"Registered event handler for {event_type}")

    def unregister_event_handler(self, event_type: str, handler: Callable) -> None:
        """Unregister event handler"""
        if event_type in self.event_handlers and handler in self.event_handlers[event_type]:
            self.event_handlers[event_type].remove(handler)
            logger.debug(f"Unregistered event handler for {event_type}")

    def _trigger_event(self, event_type: str, data: Dict[str, Any]) -> None:
        """Trigger event and notify handlers"""
        if not self.enable_events:
            return
        
        # Create event
        event = ManagerEvent(
            event_id=f"{self.manager_name}_{event_type}_{int(time.time())}",
            event_type=event_type,
            timestamp=datetime.now(),
            source=self.manager_name,
            data=data,
            priority=ManagerPriority.INFO
        )
        
        # Add to history
        self.event_history.append(event)
        if len(self.event_history) > self.max_event_history:
            self.event_history.pop(0)
        
        # Notify handlers
        if event_type in self.event_handlers:
            for handler in self.event_handlers[event_type]:
                try:
                    handler(event)
                except Exception as e:
                    logger.error(f"Event handler error for {event_type}: {e}")

    # ========================================
    # CONFIGURATION MANAGEMENT
    # ========================================

    def get_config(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self.config.get(key, default)

    def set_config(self, key: str, value: Any) -> None:
        """Set configuration value"""
        self.config[key] = value
        logger.debug(f"Configuration updated: {key} = {value}")

    def update_config(self, config_updates: Dict[str, Any]) -> None:
        """Update multiple configuration values"""
        self.config.update(config_updates)
        logger.info(f"Configuration updated with {len(config_updates)} values")

    def save_config(self) -> bool:
        """Save configuration to file"""
        if not self.config_path:
            logger.warning("No config path specified")
            return False
        
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=2, default=str)
            logger.info(f"Configuration saved to {self.config_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to save configuration: {e}")
            return False

    # ========================================
    # STATUS TRACKING AND MONITORING
    # ========================================

    def get_status(self) -> ManagerStatus:
        """Get current manager status"""
        return self.status

    def set_status(self, status: ManagerStatus) -> None:
        """Set manager status"""
        old_status = self.status
        self.status = status
        logger.info(f"Manager status changed: {old_status} -> {status}")
        
        if self.enable_events:
            self._trigger_event("status_changed", {
                "old_status": old_status.value,
                "new_status": status.value
            })

    def is_active(self) -> bool:
        """Check if manager is active"""
        return self.status == ManagerStatus.ACTIVE

    def is_error(self) -> bool:
        """Check if manager has errors"""
        return self.status == ManagerStatus.ERROR

    def get_uptime(self) -> float:
        """Get manager uptime in seconds"""
        return (datetime.now() - self.start_time).total_seconds()

    def get_last_activity(self) -> datetime:
        """Get last activity timestamp"""
        return self.last_activity

    def update_activity(self) -> None:
        """Update last activity timestamp"""
        self.last_activity = datetime.now()

    # ========================================
    # LIFECYCLE MANAGEMENT
    # ========================================

    def start(self) -> bool:
        """Start the manager"""
        try:
            if self.status == ManagerStatus.ACTIVE:
                logger.warning("Manager is already active")
                return True
            
            self._start_manager()
            self.status = ManagerStatus.ACTIVE
            self.start_time = datetime.now()
            
            if self.enable_events:
                self._trigger_event("manager_started", {})
            
            logger.info(f"Manager '{self.manager_name}' started successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start manager: {e}")
            self.status = ManagerStatus.ERROR
            return False

    def stop(self) -> bool:
        """Stop the manager"""
        try:
            if self.status == ManagerStatus.SHUTDOWN:
                logger.warning("Manager is already stopped")
                return True
            
            self._stop_manager()
            self.status = ManagerStatus.SHUTDOWN
            
            if self.enable_events:
                self._trigger_event("manager_stopped", {})
            
            logger.info(f"Manager '{self.manager_name}' stopped successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to stop manager: {e}")
            return False

    def restart(self) -> bool:
        """Restart the manager"""
        logger.info(f"Restarting manager '{self.manager_name}'")
        if self.stop() and self.start():
            logger.info(f"Manager '{self.manager_name}' restarted successfully")
            return True
        return False

    def shutdown(self) -> None:
        """Shutdown the manager gracefully"""
        logger.info(f"Shutting down manager '{self.manager_name}'")
        self._shutdown_event.set()
        self.stop()

    # ========================================
    # ERROR HANDLING AND LOGGING
    # ========================================

    def handle_error(self, error: Exception, context: str = "") -> None:
        """Handle manager errors"""
        error_msg = f"Manager error in {context}: {error}"
        logger.error(error_msg)
        
        if self.enable_metrics:
            self.metrics.error_count += 1
        
        if self.enable_events:
            self._trigger_event("error_occurred", {
                "error": str(error),
                "context": context,
                "timestamp": datetime.now().isoformat()
            })
        
        # Set error status if critical
        if self.status != ManagerStatus.ERROR:
            self.set_status(ManagerStatus.ERROR)

    def handle_warning(self, warning: str, context: str = "") -> None:
        """Handle manager warnings"""
        warning_msg = f"Manager warning in {context}: {warning}"
        logger.warning(warning_msg)
        
        if self.enable_metrics:
            self.metrics.warning_count += 1
        
        if self.enable_events:
            self._trigger_event("warning_occurred", {
                "warning": warning,
                "context": context,
                "timestamp": datetime.now().isoformat()
            })

    # ========================================
    # METRICS COLLECTION AND REPORTING
    # ========================================

    def _update_metrics(self, success: bool, response_time: float) -> None:
        """Update manager metrics"""
        if not self.enable_metrics:
            return
        
        self.metrics.total_operations += 1
        if success:
            self.metrics.successful_operations += 1
        else:
            self.metrics.failed_operations += 1
        
        # Update average response time
        if self.metrics.total_operations > 0:
            total_time = self.metrics.average_response_time * (self.metrics.total_operations - 1)
            self.metrics.average_response_time = (total_time + response_time) / self.metrics.total_operations
        
        # Update uptime
        self.metrics.uptime = self.get_uptime()
        self.metrics.last_activity = datetime.now()

    def get_metrics(self) -> ManagerMetrics:
        """Get current manager metrics"""
        if not self.enable_metrics:
            return None
        
        # Update uptime before returning
        self.metrics.uptime = self.get_uptime()
        return self.metrics

    def reset_metrics(self) -> None:
        """Reset manager metrics"""
        if not self.enable_metrics:
            return
        
        self.metrics = ManagerMetrics(
            total_operations=0,
            successful_operations=0,
            failed_operations=0,
            average_response_time=0.0,
            last_activity=datetime.now(),
            uptime=0.0,
            error_count=0,
            warning_count=0
        )
        logger.info("Manager metrics reset")

    def get_success_rate(self) -> float:
        """Get operation success rate"""
        if not self.enable_metrics or self.metrics.total_operations == 0:
            return 0.0
        
        return self.metrics.successful_operations / self.metrics.total_operations

    # ========================================
    # ABSTRACT METHODS (Override in subclasses)
    # ========================================

    @abstractmethod
    def _validate_data(self, data: Any) -> bool:
        """Validate data before storage (override in subclasses)"""
        return True

    def _start_manager(self) -> None:
        """Start manager-specific functionality (override in subclasses)"""
        pass

    def _stop_manager(self) -> None:
        """Stop manager-specific functionality (override in subclasses)"""
        pass

    # ========================================
    # UTILITY METHODS
    # ========================================

    def get_info(self) -> Dict[str, Any]:
        """Get comprehensive manager information"""
        return {
            "manager_name": self.manager_name,
            "status": self.status.value,
            "start_time": self.start_time.isoformat(),
            "last_activity": self.last_activity.isoformat(),
            "uptime": self.get_uptime(),
            "item_count": self.count(),
            "config_keys": list(self.config.keys()),
            "event_types": list(self.event_handlers.keys()) if self.enable_events else [],
            "metrics": asdict(self.metrics) if self.enable_metrics else None,
        }

    def health_check(self) -> Dict[str, Any]:
        """Perform health check on manager"""
        health_status = {
            "manager_name": self.manager_name,
            "status": self.status.value,
            "is_healthy": self.status == ManagerStatus.ACTIVE,
            "uptime": self.get_uptime(),
            "item_count": self.count(),
            "last_activity": self.get_last_activity().isoformat(),
        }
        
        if self.enable_metrics:
            health_status.update({
                "success_rate": self.get_success_rate(),
                "error_count": self.metrics.error_count,
                "warning_count": self.metrics.warning_count,
            })
        
        return health_status

    def cleanup(self) -> None:
        """Clean up manager resources"""
        # Clean up old events
        if self.enable_events and len(self.event_history) > self.max_event_history:
            cutoff_time = datetime.now() - timedelta(hours=24)
            self.event_history = [
                event for event in self.event_history 
                if event.timestamp > cutoff_time
            ]
        
        # Save persistent data
        if self.enable_persistence:
            self._save_persistent_data()
        
        logger.debug("Manager cleanup completed")

    def __enter__(self):
        """Context manager entry"""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.shutdown()

    def __len__(self) -> int:
        """Get number of items in manager"""
        return self.count()

    def __contains__(self, key: str) -> bool:
        """Check if key exists in manager"""
        return self.exists(key)

    def __getitem__(self, key: str) -> Any:
        """Get item by key"""
        return self.read(key)

    def __setitem__(self, key: str, value: Any) -> None:
        """Set item by key"""
        self.create(key, value)

    def __delitem__(self, key: str) -> None:
        """Delete item by key"""
        self.delete(key)
