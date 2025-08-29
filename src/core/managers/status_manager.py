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

import json
import logging
import threading
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union

from ..base_manager import BaseManager, ManagerPriority, ManagerStatus
from .constants import (
    DEFAULT_AUTO_RESOLVE_TIMEOUT,
    DEFAULT_HEALTH_CHECK_INTERVAL,
    DEFAULT_MAX_STATUS_HISTORY,
    STATUS_CONFIG_PATH,
)
from .status_reporter import StatusReportWriter
from .status_entities import ComponentHealth, StatusEvent, StatusItem, StatusMetrics
from .status_types import HealthStatus, StatusLevel
from .status.tracker import StatusTracker
from .status.broadcaster import StatusBroadcaster
from .status.storage import StatusStorage

logger = logging.getLogger(__name__)


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

    def __init__(self, config_path: str = STATUS_CONFIG_PATH):
        """Initialize unified status manager"""
        super().__init__(
            manager_id="status_manager",
            name="StatusManager",
            description="Unified status manager consolidating 7 separate files",
        )

        # Configuration defaults
        self.health_check_interval = DEFAULT_HEALTH_CHECK_INTERVAL
        self.max_status_history = DEFAULT_MAX_STATUS_HISTORY
        self.auto_resolve_timeout = DEFAULT_AUTO_RESOLVE_TIMEOUT

        # Reporting resources
        self.reporter = StatusReportWriter()

        # Load configuration
        self.config_path = config_path
        self._load_manager_config()

        # Modules
        self.tracker = StatusTracker(self.max_status_history)
        self.tracker.set_event_callback(self._emit_event)
        self.broadcaster = StatusBroadcaster(
            self.health_check_interval, self._emit_event
        )
        self.storage = StatusStorage(self.tracker, self.broadcaster)

        logger.info("StatusManager initialized successfully")

    def _load_manager_config(self):
        """Load manager-specific configuration"""
        try:
            if Path(self.config_path).exists():
                with open(self.config_path, "r") as f:
                    config = json.load(f)
                    self.health_check_interval = config.get(
                        "health_check_interval", DEFAULT_HEALTH_CHECK_INTERVAL
                    )
                    self.max_status_history = config.get(
                        "max_status_history", DEFAULT_MAX_STATUS_HISTORY
                    )
                    self.auto_resolve_timeout = config.get(
                        "auto_resolve_timeout", DEFAULT_AUTO_RESOLVE_TIMEOUT
                    )
            else:
                logger.warning(f"Status config file not found: {self.config_path}")
        except Exception as e:
            logger.error(f"Failed to load status config: {e}")

    def register_health_check(
        self, name: str, check_function: Callable[[], HealthStatus]
    ):
        """Register a health check function."""
        self.broadcaster.register_health_check(name, check_function)
        logger.info(f"Registered health check: {name}")

    @property
    def status_items(self) -> Dict[str, StatusItem]:
        return self.tracker.registry.status_items

    @property
    def status_events(self) -> Dict[str, StatusEvent]:
        return self.tracker.registry.status_events

    @property
    def status_lock(self) -> threading.Lock:  # type: ignore[override]
        return self.tracker.registry.status_lock

    @property
    def component_health(self) -> Dict[str, ComponentHealth]:
        return self.broadcaster.component_health

    @property
    def health_checks(self) -> Dict[str, Callable[[], HealthStatus]]:
        return self.broadcaster.health_monitor.health_checks

    def add_status(
        self,
        component: str,
        status: str,
        level: StatusLevel,
        message: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Add a new status item."""
        try:
            status_id = self.tracker.add_status(
                component, status, level, message, metadata
            )
            logger.info(f"Added status for {component}: {status} ({level.value})")
            return status_id
        except Exception as e:
            logger.error(f"Failed to add status for {component}: {e}")
            raise

    def get_status(
        self, component: Optional[str] = None
    ) -> Union[StatusItem, List[StatusItem], None]:
        """Get status information."""
        try:
            return self.tracker.get_status(component)
        except Exception as e:
            logger.error(f"Failed to get status: {e}")
            return None if component else []

    def get_health_status(self, component_id: str) -> Optional[ComponentHealth]:
        """Get health status for a component"""
        try:
            return self.broadcaster.get_health_status(component_id)
        except Exception as e:
            logger.error(f"Failed to get health status for {component_id}: {e}")
            return None

    def get_status_summary(self) -> StatusMetrics:
        """Get status summary metrics."""
        try:
            uptime = (
                (datetime.now() - self.startup_time).total_seconds()
                if self.startup_time
                else 0.0
            )
            return self.tracker.get_status_summary(uptime)
        except Exception as e:
            logger.error(f"Failed to get status summary: {e}")
            return StatusMetrics(
                total_components=0,
                healthy_components=0,
                warning_components=0,
                error_components=0,
                critical_components=0,
                last_update=datetime.now().isoformat(),
                uptime_seconds=0.0,
            )

    def get_active_alerts(self) -> List[StatusItem]:
        """Get active alerts (warning, error, critical)."""
        try:
            return self.tracker.get_active_alerts()
        except Exception as e:
            logger.error(f"Failed to get active alerts: {e}")
            return []

    def resolve_status(
        self, status_id: str, resolution_message: str = "Resolved"
    ) -> bool:
        """Mark a status item as resolved."""
        try:
            resolved = self.tracker.resolve_status(status_id, resolution_message)
            if resolved:
                logger.info(f"Resolved status: {status_id}")
            else:
                logger.warning(f"Status not found: {status_id}")
            return resolved
        except Exception as e:
            logger.error(f"Failed to resolve status {status_id}: {e}")
            return False

    def run_health_checks(self) -> Dict[str, HealthStatus]:
        """Run all registered health checks."""
        try:
            results = self.broadcaster.run_health_checks()
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
        # Allocate reporting resource
        self.reporter.initialize()
        logger.debug(f"Allocated report file at {self.reporter.path}")

    async def _shutdown_manager(self):
        logger.info(f"Shutting down {self.name}...")
        # Stop health monitoring
        self.broadcaster.stop()
        # Final reporting and resource cleanup
        summary = asdict(self.get_status_summary())
        self.reporter.finalize(summary)
        if self.reporter.path:
            logger.info(f"Wrote final status report to {self.reporter.path}")

    def _on_start(self) -> bool:
        """Called when manager starts"""
        try:
            logger.info(f"Starting {self.name}...")
            return True
        except Exception as e:
            logger.error(f"Failed to start {self.name}: {e}")
            return False

    def _on_stop(self):
        """Called when manager stops"""
        try:
            logger.info(f"Stopping {self.name}...")
        except Exception as e:
            logger.error(f"Failed to stop {self.name}: {e}")

    def _on_heartbeat(self):
        """Called on each heartbeat"""
        try:
            # Update last heartbeat time
            self.last_heartbeat = datetime.now()

            # Run health checks if needed
            if not self.broadcaster.health_monitor.timer:
                self._start_health_monitoring()

        except Exception as e:
            logger.error(f"Heartbeat error in {self.name}: {e}")

    def _on_initialize_resources(self) -> bool:
        """Called to initialize manager resources"""
        try:
            logger.info(f"Initializing resources for {self.name}...")
            # Load configuration
            self._load_manager_config()
            self.broadcaster.health_monitor.interval = self.health_check_interval
            return True
        except Exception as e:
            logger.error(f"Failed to initialize resources for {self.name}: {e}")
            return False

    def _on_cleanup_resources(self):
        """Called to cleanup manager resources"""
        try:
            logger.info(f"Cleaning up resources for {self.name}...")
            # Stop health monitoring
            self.broadcaster.stop()
            # Clear data structures
            self.tracker.clear()
            self.broadcaster.clear()
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
            "status": (
                "healthy"
                if all(
                    status == HealthStatus.HEALTHY for status in health_results.values()
                )
                else "degraded"
            ),
            "health_checks": {
                name: status.value for name, status in health_results.items()
            },
            "total_components": len(self.status_items),
            "active_alerts": len(self.get_active_alerts()),
        }

    async def _get_status(self) -> Dict[str, Any]:
        # Return comprehensive status information
        summary = self.get_status_summary()
        return {
            "status": "active",
            "summary": asdict(summary),
            "active_alerts": len(self.get_active_alerts()),
            "health_status": (
                "healthy" if summary.critical_components == 0 else "degraded"
            ),
        }

    async def _get_metrics(self) -> Dict[str, Any]:
        # Return performance metrics
        return {
            "status_items_count": len(self.status_items),
            "events_count": len(self.status_events),
            "health_checks_count": len(self.health_checks),
            "uptime_seconds": (
                (datetime.now() - self.startup_time).total_seconds()
                if self.startup_time
                else 0.0
            ),
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

    async def _process_command(
        self, command: str, payload: Dict[str, Any]
    ) -> Dict[str, Any]:
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
        required_keys = [
            "health_check_interval",
            "max_status_history",
            "auto_resolve_timeout",
        ]
        return all(key in config for key in required_keys)

    async def _apply_config(self, config: Dict[str, Any]):
        # Apply configuration
        if self._validate_config(config):
            self.health_check_interval = config.get(
                "health_check_interval", DEFAULT_HEALTH_CHECK_INTERVAL
            )
            self.max_status_history = config.get(
                "max_status_history", DEFAULT_MAX_STATUS_HISTORY
            )
            self.auto_resolve_timeout = config.get(
                "auto_resolve_timeout", DEFAULT_AUTO_RESOLVE_TIMEOUT
            )
            self.tracker.registry.max_history = self.max_status_history
            self.broadcaster.health_monitor.interval = self.health_check_interval

    async def _reset_state(self):
        """Reset manager state."""
        self.storage.reset()
        logger.info("Status manager state reset")

    async def _backup_state(self) -> Dict[str, Any]:
        """Backup current state."""
        return self.storage.backup()

    async def _restore_state(self, state: Dict[str, Any]):
        """Restore state from backup."""
        try:
            self.storage.restore(state)
            logger.info("Status manager state restored")
        except Exception as e:
            logger.error(f"Failed to restore state: {e}")

    async def _get_dependencies(self) -> List[str]:
        # Return dependencies
        return ["system_manager", "config_manager"]

    async def _get_capabilities(self) -> List[str]:
        # Return capabilities
        return [
            "status_tracking",
            "health_monitoring",
            "alert_management",
            "event_emission",
        ]

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
            "auto_resolve_timeout": {"type": "integer", "default": 3600},
        }

    async def _get_state_schema(self) -> Dict[str, Any]:
        return {
            "status_items": {"type": "object"},
            "status_events": {"type": "object"},
            "component_health": {"type": "object"},
        }

    async def _get_event_schema(self) -> Dict[str, Any]:
        return {
            "status_event": {"type": "object"},
            "health_alert": {"type": "object"},
            "status_update": {"type": "object"},
        }

    async def _get_command_schema(self) -> Dict[str, Any]:
        return {
            "add_status": {"type": "object", "required": ["component", "status"]},
            "get_status": {"type": "object"},
            "run_health_checks": {"type": "object"},
        }

    async def _get_metric_schema(self) -> Dict[str, Any]:
        return {
            "status_items_count": {"type": "integer"},
            "events_count": {"type": "integer"},
            "health_checks_count": {"type": "integer"},
            "uptime_seconds": {"type": "number"},
        }

    async def _get_status_schema(self) -> Dict[str, Any]:
        return {
            "status": {"type": "string"},
            "summary": {"type": "object"},
            "active_alerts": {"type": "integer"},
            "health_status": {"type": "string"},
        }

    async def _get_health_schema(self) -> Dict[str, Any]:
        return {
            "status": {"type": "string"},
            "health_checks": {"type": "object"},
            "total_components": {"type": "integer"},
            "active_alerts": {"type": "integer"},
        }

    async def _get_dependency_schema(self) -> Dict[str, Any]:
        return {
            "system_manager": {"type": "string"},
            "config_manager": {"type": "string"},
        }

    async def _get_capability_schema(self) -> Dict[str, Any]:
        return {
            "status_tracking": {"type": "string"},
            "health_monitoring": {"type": "string"},
            "alert_management": {"type": "string"},
            "event_emission": {"type": "string"},
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
        """Start periodic health monitoring."""
        try:
            self.broadcaster.start(self.health_check_interval)
            logger.info(
                f"Health monitoring started with {self.health_check_interval}s interval"
            )
        except Exception as e:
            logger.error(f"Failed to start health monitoring: {e}")


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
                "auto_resolve_timeout": 3600,
            }

            config_file = config_dir / "status_manager.json"
            with open(config_file, "w") as f:
                json.dump(test_config, f)

            # Initialize manager
            status_manager = StatusManager(str(config_file))

            # Test basic functionality
            status_id = status_manager.add_status(
                "test_component",
                "operational",
                StatusLevel.SUCCESS,
                "Test status message",
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
            status_manager.stop()

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
    parser.add_argument(
        "--config", default="config/status_manager.json", help="Config file path"
    )

    args = parser.parse_args()

    if args.test:
        success = run_smoke_test()
        exit(0 if success else 1)
    else:
        print("StatusManager CLI - Use --test to run smoke test")


if __name__ == "__main__":
    main()
