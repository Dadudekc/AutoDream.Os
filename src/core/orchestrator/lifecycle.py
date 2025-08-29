import logging
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from ..base_manager import BaseManager, ManagerStatus
from .registry import ManagerRegistry

logger = logging.getLogger(__name__)


class LifecycleManager:
    """Handle starting, stopping and monitoring manager lifecycles."""

    def __init__(self, registry: ManagerRegistry, config: Dict[str, Any]) -> None:
        self.registry = registry
        self.config = config
        self.health_check_interval = config.get("health_check_interval", 300)
        self.last_health_check = datetime.now()
        self.health_thread: Optional[threading.Thread] = None
        self.shutdown_event = threading.Event()

    # ------------------------------------------------------------------
    # Startup and shutdown
    # ------------------------------------------------------------------
    def start_all_managers(self) -> bool:
        logger.info("Starting all managers...")
        startup_results: Dict[str, bool] = {}
        failed: list[str] = []
        for name in self.registry.startup_order:
            info = self.registry.managers[name]
            try:
                manager_instance = info.manager_class(
                    manager_name=name,
                    config_path=info.config_path,
                    enable_metrics=self.config.get("enable_metrics", True),
                    enable_events=self.config.get("enable_events", True),
                )
                if manager_instance.start():
                    info.instance = manager_instance
                    info.status = ManagerStatus.ACTIVE
                    self.registry.manager_instances[name] = manager_instance
                    startup_results[name] = True
                    logger.info("✅ Manager %s started successfully", name)
                else:
                    startup_results[name] = False
                    failed.append(name)
                    logger.error("❌ Manager %s failed to start", name)
            except Exception as exc:  # pragma: no cover - defensive
                startup_results[name] = False
                failed.append(name)
                logger.error("❌ Failed to start manager %s: %s", name, exc)
        if failed:
            logger.error("Failed managers: %s", failed)
            return False
        self._start_health_monitoring()
        return True

    def stop_all_managers(self) -> None:
        logger.info("Stopping all managers...")
        self._stop_health_monitoring()
        for name in reversed(self.registry.startup_order):
            inst = self.registry.manager_instances.get(name)
            if not inst:
                continue
            try:
                inst.stop()
                self.registry.managers[name].status = ManagerStatus.SHUTDOWN
                logger.info("✅ Manager %s stopped", name)
            except Exception as exc:  # pragma: no cover - defensive
                logger.error("❌ Failed to stop manager %s: %s", name, exc)
        logger.info("All managers stopped")

    def restart_manager(self, manager_name: str) -> bool:
        if manager_name not in self.registry.manager_instances:
            logger.error("Manager %s not found", manager_name)
            return False
        inst = self.registry.manager_instances[manager_name]
        try:
            inst.stop()
            if inst.start():
                self.registry.managers[manager_name].status = ManagerStatus.ACTIVE
                logger.info("✅ Manager %s restarted successfully", manager_name)
                return True
            logger.error("❌ Manager %s failed to restart", manager_name)
            return False
        except Exception as exc:  # pragma: no cover - defensive
            logger.error("❌ Failed to restart manager %s: %s", manager_name, exc)
            return False

    # ------------------------------------------------------------------
    # Health monitoring
    # ------------------------------------------------------------------
    def _start_health_monitoring(self) -> None:
        if self.health_thread and self.health_thread.is_alive():
            return
        self.health_thread = threading.Thread(target=self._health_monitoring_loop, daemon=True)
        self.health_thread.start()
        logger.info("Health monitoring started")

    def _stop_health_monitoring(self) -> None:
        self.shutdown_event.set()
        if self.health_thread and self.health_thread.is_alive():
            self.health_thread.join(timeout=5)
        logger.info("Health monitoring stopped")

    def _health_monitoring_loop(self) -> None:
        while not self.shutdown_event.is_set():
            try:
                self._perform_health_checks()
                time.sleep(self.health_check_interval)
            except Exception as exc:  # pragma: no cover - defensive
                logger.error("Health monitoring error: %s", exc)
                time.sleep(60)

    def _perform_health_checks(self) -> None:
        for name, info in self.registry.managers.items():
            inst = self.registry.manager_instances.get(name)
            if not inst:
                continue
            try:
                status = inst.health_check()
                info.last_health_check = datetime.now()
                info.health_status = status
                if not status.get("is_healthy", False):
                    logger.warning("Manager %s is unhealthy: %s", name, status)
                    if self.config.get("enable_auto_recovery", True):
                        self._attempt_auto_recovery(name)
            except Exception as exc:  # pragma: no cover - defensive
                logger.error("Health check failed for %s: %s", name, exc)
                info.health_status = {"error": str(exc)}
        self.last_health_check = datetime.now()

    def _attempt_auto_recovery(self, manager_name: str) -> None:
        max_attempts = self.config.get("max_retry_attempts", 3)
        delay = self.config.get("retry_delay", 5)
        for attempt in range(max_attempts):
            if self.restart_manager(manager_name):
                logger.info("✅ Auto-recovery successful for %s", manager_name)
                return
            logger.warning("Auto-recovery attempt %s failed for %s", attempt + 1, manager_name)
            time.sleep(delay)
        logger.error("❌ Auto-recovery failed for %s after %s attempts", manager_name, max_attempts)

    # ------------------------------------------------------------------
    # Cleanup
    # ------------------------------------------------------------------
    def cleanup(self, config_path: Path, config: Dict[str, Any]) -> None:
        logger.info("Cleaning up orchestrator resources...")
        for name, inst in self.registry.manager_instances.items():
            try:
                inst.cleanup()
            except Exception as exc:  # pragma: no cover - defensive
                logger.error("Cleanup error for %s: %s", name, exc)
        try:
            config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(config_path, "w") as f:
                import json

                json.dump(config, f, indent=2, default=str)
        except Exception as exc:  # pragma: no cover - defensive
            logger.error("Failed to save configuration: %s", exc)
        logger.info("Orchestrator cleanup completed")
