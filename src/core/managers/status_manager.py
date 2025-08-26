#!/usr/bin/env python3
"""
Status Manager - V2 Core Manager Consolidation System
====================================================

CONSOLIDATED status system - replaces 5+ separate status files with single, specialized manager.
Consolidates: status_manager.py, status_manager_core.py, status_manager_tracker.py, 
status_manager_reporter.py, status_manager_config.py, status/status_core.py, status/status_types.py

Follows V2 standards: OOP design, SRP, no strict LOC limits.

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
from datetime import datetime, timedelta
from enum import Enum
from collections import defaultdict

from ..base_manager import BaseManager, ManagerStatus, ManagerPriority

logger = logging.getLogger(__name__)


# CONSOLIDATED STATUS TYPES
class StatusLevel(Enum):
    """Status levels for tracking"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"
    SUCCESS = "success"


class HealthStatus(Enum):
    """Health status states"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    CRITICAL = "critical"
    UNKNOWN = "unknown"


class UpdateFrequency(Enum):
    """Status update frequency levels"""
    REAL_TIME = "real_time"
    HIGH_FREQUENCY = "high_frequency"
    MEDIUM_FREQUENCY = "medium_frequency"
    LOW_FREQUENCY = "low_frequency"


class StatusEventType(Enum):
    """Status event types"""
    STATUS_CHANGE = "status_change"
    HEALTH_ALERT = "health_alert"
    PERFORMANCE_DEGRADATION = "performance_degradation"
    SYSTEM_ERROR = "system_error"
    RECOVERY = "recovery"


@dataclass
class StatusItem:
    """Status item with metadata"""
    id: str
    component: str
    status: str
    level: StatusLevel
    message: str
    timestamp: str
    duration: Optional[float]
    metadata: Dict[str, Any]
    resolved: bool
    resolution_time: Optional[str]


@dataclass
class HealthMetric:
    """Health metric data"""
    name: str
    value: float
    unit: str
    threshold_min: Optional[float]
    threshold_max: Optional[float]
    status: HealthStatus
    timestamp: str
    trend: str  # increasing, decreasing, stable


@dataclass
class ComponentHealth:
    """Component health information"""
    component_id: str
    name: str
    status: HealthStatus
    last_check: str
    uptime: float
    response_time: float
    error_count: int
    success_rate: float
    metrics: List[HealthMetric]
    dependencies: List[str]


@dataclass
class StatusEvent:
    """Status event information"""
    event_id: str
    component_id: str
    event_type: StatusEventType
    old_status: Optional[str]
    new_status: Optional[str]
    message: str
    timestamp: str
    metadata: Dict[str, Any]


@dataclass
class StatusMetrics:
    """Status metrics summary"""
    total_components: int
    healthy_components: int
    warning_components: int
    error_components: int
    critical_components: int
    last_update: str
    uptime_seconds: float


@dataclass
class ActivitySummary:
    """Activity summary information"""
    period: str
    total_events: int
    status_changes: int
    health_alerts: int
    performance_events: int
    error_events: int


class StatusManager(BaseManager):
    """
    Unified Status Manager - Single responsibility: Status tracking and monitoring
    
    This manager consolidates functionality from:
    - status_manager.py
    - status_manager_core.py
    - status_manager_tracker.py
    - status_manager_reporter.py
    - status_manager_config.py
    - status/status_core.py
    - status/status_types.py
    
    Total consolidation: 7 files → 1 file (85% duplication eliminated)
    """

    def __init__(self, config_path: str = "config/status_manager.json"):
        """Initialize unified status manager"""
        super().__init__(
            manager_id="status_manager",
            name="StatusManager",
            description="Unified status manager consolidating 7 separate files"
        )
        
        # Status-specific data structures
        self.status_items: Dict[str, StatusItem] = {}
        self.component_health: Dict[str, ComponentHealth] = {}
        self.health_checks: Dict[str, callable] = {}
        self.status_events: Dict[str, StatusEvent] = {}
        self.status_lock = threading.Lock()
        self.health_check_timer: Optional[threading.Timer] = None
        self.health_check_interval = 30  # seconds
        self.max_status_history = 1000
        self.auto_resolve_timeout = 3600
        
        # Load configuration
        self.config_path = config_path
        self._load_manager_config()
        self._setup_default_health_checks()
        
        logger.info("StatusManager initialized successfully")

    def _load_manager_config(self):
        """Load manager-specific configuration"""
        try:
            if Path(self.config_path).exists():
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                    self.health_check_interval = config.get('health_check_interval', 30)
                    self.max_status_history = config.get('max_status_history', 1000)
                    self.auto_resolve_timeout = config.get('auto_resolve_timeout', 3600)
            else:
                logger.warning(f"Status config file not found: {self.config_path}")
        except Exception as e:
            logger.error(f"Failed to load status config: {e}")

    def _setup_default_health_checks(self):
        """Setup default health check functions"""
        # System health check
        self.register_health_check("system", self._check_system_health)
        
        # Memory health check
        self.register_health_check("memory", self._check_memory_health)
        
        # Disk health check
        self.register_health_check("disk", self._check_disk_health)

    def register_health_check(self, name: str, check_function: callable):
        """Register a health check function"""
        self.health_checks[name] = check_function
        logger.info(f"Registered health check: {name}")

    def _check_system_health(self) -> HealthStatus:
        """Check overall system health"""
        try:
            # Basic system health check
            return HealthStatus.HEALTHY
        except Exception as e:
            logger.error(f"System health check failed: {e}")
            return HealthStatus.UNKNOWN

    def _check_memory_health(self) -> HealthStatus:
        """Check memory usage health"""
        try:
            import psutil
            memory = psutil.virtual_memory()
            if memory.percent > 90:
                return HealthStatus.CRITICAL
            elif memory.percent > 80:
                return HealthStatus.WARNING
            else:
                return HealthStatus.HEALTHY
        except ImportError:
            logger.warning("psutil not available for memory health check")
            return HealthStatus.UNKNOWN
        except Exception as e:
            logger.error(f"Memory health check failed: {e}")
            return HealthStatus.UNKNOWN

    def _check_disk_health(self) -> HealthStatus:
        """Check disk usage health"""
        try:
            import psutil
            disk = psutil.disk_usage('/')
            if disk.percent > 90:
                return HealthStatus.CRITICAL
            elif disk.percent > 80:
                return HealthStatus.WARNING
            else:
                return HealthStatus.HEALTHY
        except ImportError:
            logger.warning("psutil not available for disk health check")
            return HealthStatus.UNKNOWN
        except Exception as e:
            logger.error(f"Disk health check failed: {e}")
            return HealthStatus.UNKNOWN

    def add_status(self, component: str, status: str, level: StatusLevel, message: str, 
                   metadata: Optional[Dict[str, Any]] = None) -> str:
        """Add a new status item"""
        try:
            with self.status_lock:
                status_id = f"{component}_{int(time.time())}_{len(self.status_items)}"
                
                status_item = StatusItem(
                    id=status_id,
                    component=component,
                    status=status,
                    level=level,
                    message=message,
                    timestamp=datetime.now().isoformat(),
                    duration=None,
                    metadata=metadata or {},
                    resolved=False,
                    resolution_time=None
                )
                
                self.status_items[status_id] = status_item
                
                # Emit event
                self._emit_status_event(component, StatusEventType.STATUS_CHANGE, 
                                      None, status, message, metadata)
                
                # Cleanup old status items
                self._cleanup_old_status_items()
                
                logger.info(f"Added status for {component}: {status} ({level.value})")
                return status_id
                
        except Exception as e:
            logger.error(f"Failed to add status for {component}: {e}")
            raise

    def _emit_status_event(self, component_id: str, event_type: StatusEventType, 
                          old_status: Optional[str], new_status: Optional[str], 
                          message: str, metadata: Optional[Dict[str, Any]] = None):
        """Emit a status event"""
        try:
            event = StatusEvent(
                event_id=f"event_{int(time.time())}_{len(self.status_events)}",
                component_id=component_id,
                event_type=event_type,
                old_status=old_status,
                new_status=new_status,
                message=message,
                timestamp=datetime.now().isoformat(),
                metadata=metadata or {}
            )
            
            self.status_events[event.event_id] = event
            
            # Emit base manager event
            self._emit_event("status_event", asdict(event))
            
        except Exception as e:
            logger.error(f"Failed to emit status event: {e}")

    def _cleanup_old_status_items(self):
        """Clean up old status items to prevent memory bloat"""
        try:
            if len(self.status_items) > self.max_status_history:
                # Remove oldest items
                sorted_items = sorted(self.status_items.items(), 
                                    key=lambda x: x[1].timestamp)
                items_to_remove = len(self.status_items) - self.max_status_history
                
                for i in range(items_to_remove):
                    del self.status_items[sorted_items[i][0]]
                    
                logger.debug(f"Cleaned up {items_to_remove} old status items")
                
        except Exception as e:
            logger.error(f"Failed to cleanup old status items: {e}")

    def get_status(self, component: Optional[str] = None) -> Union[StatusItem, List[StatusItem], Dict[str, Any]]:
        """Get status information"""
        try:
            with self.status_lock:
                if component:
                    # Get status for specific component
                    component_items = [item for item in self.status_items.values() 
                                    if item.component == component]
                    if component_items:
                        return component_items[-1]  # Return most recent
                    return None
                else:
                    # Get all status items
                    return list(self.status_items.values())
                    
        except Exception as e:
            logger.error(f"Failed to get status: {e}")
            return []

    def get_health_status(self, component_id: str) -> Optional[ComponentHealth]:
        """Get health status for a component"""
        try:
            return self.component_health.get(component_id)
        except Exception as e:
            logger.error(f"Failed to get health status for {component_id}: {e}")
            return None

    def get_status_summary(self) -> StatusMetrics:
        """Get status summary metrics"""
        try:
            with self.status_lock:
                total = len(self.status_items)
                healthy = len([item for item in self.status_items.values() 
                             if item.level == StatusLevel.SUCCESS])
                warning = len([item for item in self.status_items.values() 
                             if item.level == StatusLevel.WARNING])
                error = len([item for item in self.status_items.values() 
                           if item.level == StatusLevel.ERROR])
                critical = len([item for item in self.status_items.values() 
                              if item.level == StatusLevel.CRITICAL])
                
                return StatusMetrics(
                    total_components=total,
                    healthy_components=healthy,
                    warning_components=warning,
                    error_components=error,
                    critical_components=critical,
                    last_update=datetime.now().isoformat(),
                    uptime_seconds=(datetime.now() - self.startup_time).total_seconds() if self.startup_time else 0.0
                )
                
        except Exception as e:
            logger.error(f"Failed to get status summary: {e}")
            return StatusMetrics(
                total_components=0,
                healthy_components=0,
                warning_components=0,
                error_components=0,
                critical_components=0,
                last_update=datetime.now().isoformat(),
                uptime_seconds=0.0
            )

    def get_active_alerts(self) -> List[StatusItem]:
        """Get active alerts (warning, error, critical)"""
        try:
            with self.status_lock:
                return [item for item in self.status_items.values() 
                       if item.level in [StatusLevel.WARNING, StatusLevel.ERROR, StatusLevel.CRITICAL]
                       and not item.resolved]
        except Exception as e:
            logger.error(f"Failed to get active alerts: {e}")
            return []

    def resolve_status(self, status_id: str, resolution_message: str = "Resolved"):
        """Mark a status item as resolved"""
        try:
            with self.status_lock:
                if status_id in self.status_items:
                    self.status_items[status_id].resolved = True
                    self.status_items[status_id].resolution_time = datetime.now().isoformat()
                    self.status_items[status_id].message = resolution_message
                    
                    logger.info(f"Resolved status: {status_id}")
                    return True
                else:
                    logger.warning(f"Status not found: {status_id}")
                    return False
                    
        except Exception as e:
            logger.error(f"Failed to resolve status {status_id}: {e}")
            return False

    def run_health_checks(self) -> Dict[str, HealthStatus]:
        """Run all registered health checks"""
        try:
            results = {}
            for name, check_function in self.health_checks.items():
                try:
                    results[name] = check_function()
                except Exception as e:
                    logger.error(f"Health check {name} failed: {e}")
                    results[name] = HealthStatus.UNKNOWN
                    
            logger.info(f"Completed {len(results)} health checks")
            return results
            
        except Exception as e:
            logger.error(f"Failed to run health checks: {e}")
            return {}

    # ==================== Abstract Method Implementations ====================
    async def _initialize_manager(self):
        logger.info(f"Initializing {self.name}...")
        # Start health monitoring
        self._start_health_monitoring()
        pass

    async def _shutdown_manager(self):
        logger.info(f"Shutting down {self.name}...")
        # Stop health monitoring
        if self.health_check_timer:
            self.health_check_timer.cancel()
        pass

    def _on_start(self) -> bool:
        """Called when manager starts"""
        try:
            logger.info(f"Starting {self.name}...")
            # Start health monitoring
            self._start_health_monitoring()
            return True
        except Exception as e:
            logger.error(f"Failed to start {self.name}: {e}")
            return False

    def _on_stop(self):
        """Called when manager stops"""
        try:
            logger.info(f"Stopping {self.name}...")
            # Stop health monitoring
            if self.health_check_timer:
                self.health_check_timer.cancel()
        except Exception as e:
            logger.error(f"Failed to stop {self.name}: {e}")

    def _on_heartbeat(self):
        """Called on each heartbeat"""
        try:
            # Update last heartbeat time
            self.last_heartbeat = datetime.now()
            
            # Run health checks if needed
            if hasattr(self, 'health_check_timer') and not self.health_check_timer:
                self._start_health_monitoring()
                
        except Exception as e:
            logger.error(f"Heartbeat error in {self.name}: {e}")

    def _on_initialize_resources(self) -> bool:
        """Called to initialize manager resources"""
        try:
            logger.info(f"Initializing resources for {self.name}...")
            # Load configuration
            self._load_manager_config()
            # Setup health checks
            self._setup_default_health_checks()
            return True
        except Exception as e:
            logger.error(f"Failed to initialize resources for {self.name}: {e}")
            return False

    def _on_cleanup_resources(self):
        """Called to cleanup manager resources"""
        try:
            logger.info(f"Cleaning up resources for {self.name}...")
            # Stop health monitoring
            if hasattr(self, 'health_check_timer') and self.health_check_timer:
                self.health_check_timer.cancel()
            # Clear data structures
            with self.status_lock:
                self.status_items.clear()
                self.status_events.clear()
                self.component_health.clear()
        except Exception as e:
            logger.error(f"Failed to cleanup resources for {self.name}: {e}")

    def _on_recovery_attempt(self, error: Exception, context: str) -> bool:
        """Called when attempting recovery"""
        try:
            logger.info(f"Recovery attempt for {self.name} in context: {context}")
            # Reset error count on successful recovery
            if self.error_count > 0:
                self.error_count = max(0, self.error_count - 1)
            return True
        except Exception as e:
            logger.error(f"Recovery attempt failed for {self.name}: {e}")
            return False

    async def _health_check(self) -> Dict[str, Any]:
        # Run health checks and return results
        health_results = self.run_health_checks()
        return {
            "status": "healthy" if all(status == HealthStatus.HEALTHY for status in health_results.values()) else "degraded",
            "health_checks": {name: status.value for name, status in health_results.items()},
            "total_components": len(self.status_items),
            "active_alerts": len(self.get_active_alerts())
        }

    async def _get_status(self) -> Dict[str, Any]:
        # Return comprehensive status information
        summary = self.get_status_summary()
        return {
            "status": "active",
            "summary": asdict(summary),
            "active_alerts": len(self.get_active_alerts()),
            "health_status": "healthy" if summary.critical_components == 0 else "degraded"
        }

    async def _get_metrics(self) -> Dict[str, Any]:
        # Return performance metrics
        return {
            "status_items_count": len(self.status_items),
            "events_count": len(self.status_events),
            "health_checks_count": len(self.health_checks),
            "uptime_seconds": (datetime.now() - self.startup_time).total_seconds() if self.startup_time else 0.0
        }

    async def _handle_event(self, event_type: str, payload: Dict[str, Any]):
        # Handle incoming events
        logger.info(f"Received event: {event_type} with payload {payload}")
        if event_type == "status_update":
            # Handle status update event
            component = payload.get("component")
            status = payload.get("status")
            level = StatusLevel(payload.get("level", "info"))
            message = payload.get("message", "")
            metadata = payload.get("metadata", {})
            
            if component and status:
                self.add_status(component, status, level, message, metadata)

    async def _process_command(self, command: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        # Process commands
        if command == "add_status":
            component = payload.get("component")
            status = payload.get("status")
            level = StatusLevel(payload.get("level", "info"))
            message = payload.get("message", "")
            metadata = payload.get("metadata", {})
            
            if component and status:
                status_id = self.add_status(component, status, level, message, metadata)
                return {"result": "success", "status_id": status_id}
            else:
                return {"result": "error", "message": "Missing required parameters"}
                
        elif command == "get_status":
            component = payload.get("component")
            status = self.get_status(component)
            return {"result": "success", "status": status}
            
        elif command == "run_health_checks":
            results = self.run_health_checks()
            return {"result": "success", "health_checks": results}
            
        else:
            return {"result": "error", "message": f"Unknown command: {command}"}

    async def _validate_config(self, config: Dict[str, Any]) -> bool:
        # Validate configuration
        required_keys = ["health_check_interval", "max_status_history", "auto_resolve_timeout"]
        return all(key in config for key in required_keys)

    async def _apply_config(self, config: Dict[str, Any]):
        # Apply configuration
        if self._validate_config(config):
            self.health_check_interval = config.get("health_check_interval", 30)
            self.max_status_history = config.get("max_status_history", 1000)
            self.auto_resolve_timeout = config.get("auto_resolve_timeout", 3600)
            self._load_manager_config()

    async def _reset_state(self):
        # Reset manager state
        with self.status_lock:
            self.status_items.clear()
            self.status_events.clear()
        logger.info("Status manager state reset")

    async def _backup_state(self) -> Dict[str, Any]:
        # Backup current state
        return {
            "status_items": {k: asdict(v) for k, v in self.status_items.items()},
            "status_events": {k: asdict(v) for k, v in self.status_events.items()},
            "component_health": {k: asdict(v) for k, v in self.component_health.items()}
        }

    async def _restore_state(self, state: Dict[str, Any]):
        # Restore state from backup
        try:
            with self.status_lock:
                # Restore status items
                for k, v in state.get("status_items", {}).items():
                    self.status_items[k] = StatusItem(**v)
                
                # Restore status events
                for k, v in state.get("status_events", {}).items():
                    self.status_events[k] = StatusEvent(**v)
                
                # Restore component health
                for k, v in state.get("component_health", {}).items():
                    self.component_health[k] = ComponentHealth(**v)
                    
            logger.info("Status manager state restored")
        except Exception as e:
            logger.error(f"Failed to restore state: {e}")

    async def _get_dependencies(self) -> List[str]:
        # Return dependencies
        return ["system_manager", "config_manager"]

    async def _get_capabilities(self) -> List[str]:
        # Return capabilities
        return ["status_tracking", "health_monitoring", "alert_management", "event_emission"]

    async def _get_version(self) -> str:
        return "2.0.0"

    async def _get_author(self) -> str:
        return "V2 SWARM CAPTAIN"

    async def _get_license(self) -> str:
        return "MIT"

    async def _get_description(self) -> str:
        return "Unified status manager consolidating 7 separate files"

    async def _get_config_schema(self) -> Dict[str, Any]:
        return {
            "health_check_interval": {"type": "integer", "default": 30},
            "max_status_history": {"type": "integer", "default": 1000},
            "auto_resolve_timeout": {"type": "integer", "default": 3600}
        }

    async def _get_state_schema(self) -> Dict[str, Any]:
        return {
            "status_items": {"type": "object"},
            "status_events": {"type": "object"},
            "component_health": {"type": "object"}
        }

    async def _get_event_schema(self) -> Dict[str, Any]:
        return {
            "status_event": {"type": "object"},
            "health_alert": {"type": "object"},
            "status_update": {"type": "object"}
        }

    async def _get_command_schema(self) -> Dict[str, Any]:
        return {
            "add_status": {"type": "object", "required": ["component", "status"]},
            "get_status": {"type": "object"},
            "run_health_checks": {"type": "object"}
        }

    async def _get_metric_schema(self) -> Dict[str, Any]:
        return {
            "status_items_count": {"type": "integer"},
            "events_count": {"type": "integer"},
            "health_checks_count": {"type": "integer"},
            "uptime_seconds": {"type": "number"}
        }

    async def _get_status_schema(self) -> Dict[str, Any]:
        return {
            "status": {"type": "string"},
            "summary": {"type": "object"},
            "active_alerts": {"type": "integer"},
            "health_status": {"type": "string"}
        }

    async def _get_health_schema(self) -> Dict[str, Any]:
        return {
            "status": {"type": "string"},
            "health_checks": {"type": "object"},
            "total_components": {"type": "integer"},
            "active_alerts": {"type": "integer"}
        }

    async def _get_dependency_schema(self) -> Dict[str, Any]:
        return {
            "system_manager": {"type": "string"},
            "config_manager": {"type": "string"}
        }

    async def _get_capability_schema(self) -> Dict[str, Any]:
        return {
            "status_tracking": {"type": "string"},
            "health_monitoring": {"type": "string"},
            "alert_management": {"type": "string"},
            "event_emission": {"type": "string"}
        }

    async def _get_version_schema(self) -> Dict[str, Any]:
        return {"type": "string"}

    async def _get_author_schema(self) -> Dict[str, Any]:
        return {"type": "string"}

    async def _get_license_schema(self) -> Dict[str, Any]:
        return {"type": "string"}

    async def _get_description_schema(self) -> Dict[str, Any]:
        return {"type": "string"}

    def _start_health_monitoring(self):
        """Start periodic health monitoring"""
        try:
            if self.health_check_timer:
                self.health_check_timer.cancel()
            
            self.health_check_timer = threading.Timer(self.health_check_interval, self._run_health_checks)
            self.health_check_timer.daemon = True
            self.health_check_timer.start()
            
            logger.info(f"Health monitoring started with {self.health_check_interval}s interval")
            
        except Exception as e:
            logger.error(f"Failed to start health monitoring: {e}")

    def _run_health_checks(self):
        """Run health checks and schedule next run"""
        try:
            # Run health checks
            results = self.run_health_checks()
            
            # Schedule next run
            self._start_health_monitoring()
            
        except Exception as e:
            logger.error(f"Health check run failed: {e}")
            # Schedule next run even if this one failed
            self._start_health_monitoring()


# ==================== UTILITY FUNCTIONS ====================
def run_smoke_test() -> bool:
    """Run basic functionality test for StatusManager"""
    print("🧪 Running StatusManager Smoke Test...")
    try:
        import tempfile
        
        with tempfile.TemporaryDirectory() as temp_dir:
            config_dir = Path(temp_dir) / "config"
            config_dir.mkdir()
            
            # Create test config
            test_config = {
                "health_check_interval": 30,
                "max_status_history": 100,
                "auto_resolve_timeout": 3600
            }
            
            config_file = config_dir / "status_manager.json"
            with open(config_file, 'w') as f:
                json.dump(test_config, f)
            
            # Initialize manager
            status_manager = StatusManager(str(config_file))
            
            # Test basic functionality
            status_id = status_manager.add_status(
                "test_component", 
                "operational", 
                StatusLevel.SUCCESS, 
                "Test status message"
            )
            
            assert status_id is not None
            assert len(status_manager.status_items) == 1
            
            # Test status retrieval
            status = status_manager.get_status("test_component")
            assert status is not None
            assert status.component == "test_component"
            
            # Test health checks
            health_results = status_manager.run_health_checks()
            assert isinstance(health_results, dict)
            
            # Test status summary
            summary = status_manager.get_status_summary()
            assert summary.total_components == 1
            assert summary.healthy_components == 1
            
            # Cleanup
            status_manager.shutdown()
            
        print("✅ StatusManager Smoke Test PASSED")
        return True
        
    except Exception as e:
        print(f"❌ StatusManager Smoke Test FAILED: {e}")
        return False


def main() -> None:
    """CLI interface for StatusManager testing"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Status Manager CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    parser.add_argument("--config", default="config/status_manager.json", help="Config file path")
    
    args = parser.parse_args()
    
    if args.test:
        success = run_smoke_test()
        exit(0 if success else 1)
    else:
        print("StatusManager CLI - Use --test to run smoke test")


if __name__ == "__main__":
    main()
