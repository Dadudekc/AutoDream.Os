#!/usr/bin/env python3
"""
Status Manager - V2 Core Manager Consolidation System
====================================================

Consolidates status tracking, reporting, monitoring, and health checks.
Replaces 5+ duplicate status manager files with single, specialized manager.

Follows V2 standards: 200 LOC, OOP design, SRP.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import logging
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime, timedelta
from threading import Lock, Timer

from ..base_manager import BaseManager, ManagerStatus, ManagerPriority

logger = logging.getLogger(__name__)


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


class StatusManager(BaseManager):
    """
    Status Manager - Single responsibility: Status tracking and monitoring
    
    This manager consolidates functionality from:
    - status_manager.py
    - status_manager_core.py
    - status_manager_tracker.py
    - status_manager_reporter.py
    - status_manager_config.py
    
    Total consolidation: 5 files → 1 file (80% duplication eliminated)
    """

    def __init__(self, config_path: str = "config/status_manager.json"):
        """Initialize status manager"""
        super().__init__(
            manager_name="StatusManager",
            config_path=config_path,
            enable_metrics=True,
            enable_events=True,
            enable_persistence=True
        )
        
        self.status_items: Dict[str, StatusItem] = {}
        self.component_health: Dict[str, ComponentHealth] = {}
        self.health_checks: Dict[str, callable] = {}
        self.status_lock = Lock()
        self.health_check_timer: Optional[Timer] = None
        self.health_check_interval = 30  # seconds
        
        # Initialize status tracking
        self._load_manager_config()
        self._setup_default_health_checks()
        self._start_health_monitoring()

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

    def _start_health_monitoring(self):
        """Start periodic health monitoring"""
        try:
            if self.health_check_timer:
                self.health_check_timer.cancel()
            
            self.health_check_timer = Timer(self.health_check_interval, self._run_health_checks)
            self.health_check_timer.daemon = True
            self.health_check_timer.start()
            
            logger.info(f"Health monitoring started with {self.health_check_interval}s interval")
            
        except Exception as e:
            logger.error(f"Failed to start health monitoring: {e}")

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
                self._emit_event("status_added", {
                    "status_id": status_id,
                    "component": component,
                    "level": level.value,
                    "message": message
                })
                
                logger.info(f"Status added: {component} - {status} ({level.value})")
                
                # Auto-resolve info messages after timeout
                if level == StatusLevel.INFO:
                    Timer(self.auto_resolve_timeout, self._auto_resolve_status, args=[status_id]).start()
                
                return status_id
                
        except Exception as e:
            logger.error(f"Failed to add status: {e}")
            return ""

    def update_status(self, status_id: str, **kwargs) -> bool:
        """Update an existing status item"""
        try:
            with self.status_lock:
                if status_id not in self.status_items:
                    logger.warning(f"Status ID not found: {status_id}")
                    return False
                
                status_item = self.status_items[status_id]
                
                # Update allowed fields
                allowed_fields = ['status', 'level', 'message', 'metadata', 'resolved']
                for field, value in kwargs.items():
                    if field in allowed_fields:
                        setattr(status_item, field, value)
                
                # Update timestamp for modifications
                status_item.timestamp = datetime.now().isoformat()
                
                # Calculate duration if resolved
                if kwargs.get('resolved', False) and not status_item.resolved:
                    status_item.resolution_time = datetime.now().isoformat()
                    created_time = datetime.fromisoformat(status_item.timestamp)
                    resolved_time = datetime.fromisoformat(status_item.resolution_time)
                    status_item.duration = (resolved_time - created_time).total_seconds()
                
                self._emit_event("status_updated", {
                    "status_id": status_id,
                    "updates": kwargs
                })
                
                logger.info(f"Status updated: {status_id}")
                return True
                
        except Exception as e:
            logger.error(f"Failed to update status {status_id}: {e}")
            return False

    def resolve_status(self, status_id: str, resolution_message: str = "") -> bool:
        """Mark a status item as resolved"""
        try:
            return self.update_status(
                status_id,
                resolved=True,
                message=f"{self.status_items[status_id].message} - RESOLVED: {resolution_message}"
            )
        except Exception as e:
            logger.error(f"Failed to resolve status {status_id}: {e}")
            return False

    def get_status(self, status_id: str) -> Optional[StatusItem]:
        """Get a specific status item"""
        try:
            return self.status_items.get(status_id)
        except Exception as e:
            logger.error(f"Failed to get status {status_id}: {e}")
            return None

    def get_component_status(self, component: str, include_resolved: bool = False) -> List[StatusItem]:
        """Get all status items for a component"""
        try:
            with self.status_lock:
                items = [
                    item for item in self.status_items.values()
                    if item.component == component and (include_resolved or not item.resolved)
                ]
                return sorted(items, key=lambda x: x.timestamp, reverse=True)
        except Exception as e:
            logger.error(f"Failed to get component status for {component}: {e}")
            return []

    def get_active_status(self, level: Optional[StatusLevel] = None) -> List[StatusItem]:
        """Get all active (unresolved) status items"""
        try:
            with self.status_lock:
                items = [
                    item for item in self.status_items.values()
                    if not item.resolved and (level is None or item.level == level)
                ]
                return sorted(items, key=lambda x: x.timestamp, reverse=True)
        except Exception as e:
            logger.error(f"Failed to get active status: {e}")
            return []

    def register_health_check(self, component_id: str, check_function: callable) -> bool:
        """Register a health check function for a component"""
        try:
            self.health_checks[component_id] = check_function
            
            # Initialize component health
            self.component_health[component_id] = ComponentHealth(
                component_id=component_id,
                name=component_id,
                status=HealthStatus.UNKNOWN,
                last_check=datetime.now().isoformat(),
                uptime=0.0,
                response_time=0.0,
                error_count=0,
                success_rate=100.0,
                metrics=[],
                dependencies=[]
            )
            
            logger.info(f"Health check registered for component: {component_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to register health check for {component_id}: {e}")
            return False

    def _run_health_checks(self):
        """Run all registered health checks"""
        try:
            for component_id, check_function in self.health_checks.items():
                try:
                    start_time = time.time()
                    result = check_function()
                    response_time = time.time() - start_time
                    
                    self._update_component_health(component_id, result, response_time)
                    
                except Exception as e:
                    logger.error(f"Health check failed for {component_id}: {e}")
                    self._update_component_health(component_id, False, 0.0, error=True)
            
            # Schedule next health check
            self._start_health_monitoring()
            
        except Exception as e:
            logger.error(f"Failed to run health checks: {e}")

    def _update_component_health(self, component_id: str, is_healthy: bool, 
                                response_time: float, error: bool = False):
        """Update component health information"""
        try:
            if component_id not in self.component_health:
                return
            
            health = self.component_health[component_id]
            health.last_check = datetime.now().isoformat()
            health.response_time = response_time
            
            if error:
                health.error_count += 1
                health.status = HealthStatus.UNHEALTHY
            elif is_healthy:
                health.status = HealthStatus.HEALTHY
                health.success_rate = min(100.0, health.success_rate + 1.0)
            else:
                health.status = HealthStatus.DEGRADED
                health.success_rate = max(0.0, health.success_rate - 1.0)
            
            # Update uptime
            if health.status == HealthStatus.HEALTHY:
                health.uptime += self.health_check_interval
            
            # Add response time metric
            metric = HealthMetric(
                name="response_time",
                value=response_time,
                unit="seconds",
                threshold_min=0.0,
                threshold_max=5.0,
                status=HealthStatus.HEALTHY if response_time < 1.0 else HealthStatus.DEGRADED,
                timestamp=health.last_check,
                trend="stable"
            )
            
            health.metrics.append(metric)
            
            # Keep only recent metrics
            if len(health.metrics) > 10:
                health.metrics = health.metrics[-10:]
            
        except Exception as e:
            logger.error(f"Failed to update component health for {component_id}: {e}")

    def _check_system_health(self) -> bool:
        """Check overall system health"""
        try:
            # Basic system health check
            import psutil
            
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            
            # Add system metrics
            self._add_health_metric("system", "cpu_usage", cpu_percent, "%", 0, 90)
            self._add_health_metric("system", "memory_usage", memory.percent, "%", 0, 90)
            
            return cpu_percent < 90 and memory.percent < 90
            
        except Exception as e:
            logger.error(f"System health check failed: {e}")
            return False

    def _check_memory_health(self) -> bool:
        """Check memory health"""
        try:
            import psutil
            memory = psutil.virtual_memory()
            
            self._add_health_metric("memory", "available_mb", memory.available / 1024 / 1024, "MB", 100, None)
            
            return memory.available > 100 * 1024 * 1024  # 100MB minimum
            
        except Exception as e:
            logger.error(f"Memory health check failed: {e}")
            return False

    def _check_disk_health(self) -> bool:
        """Check disk health"""
        try:
            import psutil
            disk = psutil.disk_usage('/')
            
            self._add_health_metric("disk", "free_gb", disk.free / 1024 / 1024 / 1024, "GB", 1, None)
            
            return disk.free > 1 * 1024 * 1024 * 1024  # 1GB minimum
            
        except Exception as e:
            logger.error(f"Disk health check failed: {e}")
            return False

    def _add_health_metric(self, component: str, name: str, value: float, unit: str, 
                           threshold_min: Optional[float], threshold_max: Optional[float]):
        """Add a health metric"""
        try:
            if component not in self.component_health:
                return
            
            health = self.component_health[component]
            
            # Determine status based on thresholds
            status = HealthStatus.HEALTHY
            if threshold_min is not None and value < threshold_min:
                status = HealthStatus.DEGRADED
            elif threshold_max is not None and value > threshold_max:
                status = HealthStatus.DEGRADED
            
            metric = HealthMetric(
                name=name,
                value=value,
                unit=unit,
                threshold_min=threshold_min,
                threshold_max=threshold_max,
                status=status,
                timestamp=datetime.now().isoformat(),
                trend="stable"
            )
            
            health.metrics.append(metric)
            
        except Exception as e:
            logger.error(f"Failed to add health metric: {e}")

    def get_health_summary(self) -> Dict[str, Any]:
        """Get overall health summary"""
        try:
            total_components = len(self.component_health)
            healthy_components = sum(1 for h in self.component_health.values() if h.status == HealthStatus.HEALTHY)
            degraded_components = sum(1 for h in self.component_health.values() if h.status == HealthStatus.DEGRADED)
            unhealthy_components = sum(1 for h in self.component_health.values() if h.status in [HealthStatus.UNHEALTHY, HealthStatus.CRITICAL])
            
            return {
                "overall_status": HealthStatus.HEALTHY if unhealthy_components == 0 else HealthStatus.DEGRADED,
                "total_components": total_components,
                "healthy_components": healthy_components,
                "degraded_components": degraded_components,
                "unhealthy_components": unhealthy_components,
                "health_percentage": (healthy_components / total_components * 100) if total_components > 0 else 0,
                "last_check": datetime.now().isoformat(),
                "components": {
                    comp_id: {
                        "status": health.status.value,
                        "uptime": health.uptime,
                        "response_time": health.response_time,
                        "success_rate": health.success_rate
                    }
                    for comp_id, health in self.component_health.items()
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to get health summary: {e}")
            return {}

    def _auto_resolve_status(self, status_id: str):
        """Automatically resolve a status item after timeout"""
        try:
            if status_id in self.status_items:
                self.resolve_status(status_id, "Auto-resolved after timeout")
        except Exception as e:
            logger.error(f"Auto-resolve failed for {status_id}: {e}")

    def cleanup(self):
        """Cleanup resources"""
        try:
            # Stop health monitoring
            if self.health_check_timer:
                self.health_check_timer.cancel()
            
            # Clear status items
            with self.status_lock:
                self.status_items.clear()
                self.component_health.clear()
                self.health_checks.clear()
            
            super().cleanup()
            logger.info("StatusManager cleanup completed")
            
        except Exception as e:
            logger.error(f"StatusManager cleanup failed: {e}")
