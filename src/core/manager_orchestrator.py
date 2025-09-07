#!/usr/bin/env python3
"""Manager Orchestrator - delegates registry, lifecycle and integration."""

import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional

from .base_manager import BaseManager
from .orchestrator import (
    ManagerRegistry,
    LifecycleManager,
    IntegrationManager,
)

logger = logging.getLogger(__name__)


class ManagerOrchestrator:
    """Coordinate managers via dedicated registry and lifecycle helpers."""

    def __init__(self, config_path: str = "config/manager_orchestrator.json"):
        self.config_path = Path(config_path)
        self.config = self._load_config()

        self.registry = ManagerRegistry()
        self.registry.register_default_managers()
        self.registry.build_dependency_graph()
        self.registry.calculate_startup_order()

        self.lifecycle = LifecycleManager(self.registry, self.config)
        self.integration = IntegrationManager(self.registry, self.lifecycle)

        logger.info("ManagerOrchestrator initialized successfully")

    # ------------------------------------------------------------------
    # Configuration
    # ------------------------------------------------------------------
    def _load_config(self) -> Dict[str, Any]:
        default_config = {
            "health_check_interval": 300,
            "max_startup_time": 60,
            "enable_auto_recovery": True,
            "max_retry_attempts": 3,
            "retry_delay": 5,
            "cleanup_interval": 3600,
            "log_level": "INFO",
            "enable_metrics": True,
            "enable_events": True,
        }
        if not self.config_path.exists():
            return default_config
        try:
            with open(self.config_path, "r") as f:
                config = json.load(f)
                default_config.update(config)
                logger.info("Configuration loaded from %s", self.config_path)
        except Exception as exc:  # pragma: no cover - defensive
            logger.error("Failed to load config: %s", exc)
        return default_config

    # ------------------------------------------------------------------
    # Lifecycle delegation
    # ------------------------------------------------------------------
    def start_all_managers(self) -> bool:
        return self.lifecycle.start_all_managers()

    def stop_all_managers(self) -> None:
        self.lifecycle.stop_all_managers()

    def restart_manager(self, manager_name: str) -> bool:
        return self.lifecycle.restart_manager(manager_name)

    def cleanup(self) -> None:
        self.lifecycle.cleanup(self.config_path, self.config)

    # ------------------------------------------------------------------
    # Integration utilities
    # ------------------------------------------------------------------
    def get_manager(self, manager_name: str) -> Optional[BaseManager]:
        return self.integration.get_manager(manager_name)

    def get_manager_status(self, manager_name: str) -> Optional[Dict[str, Any]]:
        return self.integration.get_manager_status(manager_name)

    def get_all_manager_statuses(self) -> Dict[str, Dict[str, Any]]:
        return self.integration.get_all_manager_statuses()

    def get_orchestrator_metrics(self) -> Dict[str, Any]:
        return self.integration.get_orchestrator_metrics()

    def get_consolidation_summary(self) -> Dict[str, Any]:
        return self.integration.get_consolidation_summary()

    # ------------------------------------------------------------------
    # Context manager & magic methods
    # ------------------------------------------------------------------
    def __enter__(self):
        self.start_all_managers()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop_all_managers()
        self.cleanup()

    def __getitem__(self, manager_name: str) -> BaseManager:
        manager = self.get_manager(manager_name)
        if not manager:
            raise KeyError(f"Manager not found: {manager_name}")
        return manager

    def __contains__(self, manager_name: str) -> bool:
        return manager_name in self.registry.managers

    def __len__(self) -> int:
        return len(self.registry.managers)

    def __iter__(self):
        return iter(self.registry.managers.keys())
