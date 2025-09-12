from __future__ import annotations

from typing import Any

from .analysis_core_engine import AnalysisCoreEngine
from .communication_core_engine import CommunicationCoreEngine
from .configuration_core_engine import ConfigurationCoreEngine
from .contracts import Engine, EngineContext
from .coordination_core_engine import CoordinationCoreEngine
from .data_core_engine import DataCoreEngine
from .integration_core_engine import IntegrationCoreEngine
from .ml_core_engine import MLCoreEngine
from .monitoring_core_engine import MonitoringCoreEngine
from .orchestration_core_engine import OrchestrationCoreEngine
from .performance_core_engine import PerformanceCoreEngine
from .processing_core_engine import ProcessingCoreEngine
from .security_core_engine import SecurityCoreEngine
from .storage_core_engine import StorageCoreEngine
from .utility_core_engine import UtilityCoreEngine
from .validation_core_engine import ValidationCoreEngine


class EngineRegistry:
    """Registry for all core engines - SSOT for engine management."""

    def __init__(self):
        self._engines: dict[str, type[Engine]] = {}
        self._instances: dict[str, Engine] = {}
        self._initialize_engines()

    def _initialize_engines(self) -> None:
        """Initialize all core engines."""
        self._engines = {
            "ml": MLCoreEngine,
            "analysis": AnalysisCoreEngine,
            "integration": IntegrationCoreEngine,
            "coordination": CoordinationCoreEngine,
            "utility": UtilityCoreEngine,
            "data": DataCoreEngine,
            "communication": CommunicationCoreEngine,
            "validation": ValidationCoreEngine,
            "configuration": ConfigurationCoreEngine,
            "monitoring": MonitoringCoreEngine,
            "security": SecurityCoreEngine,
            "performance": PerformanceCoreEngine,
            "storage": StorageCoreEngine,
            "processing": ProcessingCoreEngine,
            "orchestration": OrchestrationCoreEngine,
        }

    def get_engine(self, engine_type: str) -> Engine:
        """Get engine instance by type."""
        if engine_type not in self._engines:
            raise ValueError(f"Unknown engine type: {engine_type}")

        if engine_type not in self._instances:
            self._instances[engine_type] = self._engines[engine_type]()

        return self._instances[engine_type]

    def get_engine_types(self) -> list[str]:
        """Get all available engine types."""
        return list(self._engines.keys())

    def initialize_all(self, context: EngineContext) -> dict[str, bool]:
        """Initialize all engines."""
        results = {}
        for engine_type in self._engines:
            try:
                engine = self.get_engine(engine_type)
                results[engine_type] = engine.initialize(context)
            except Exception as e:
                results[engine_type] = False
                context.logger.error(f"Failed to initialize {engine_type} engine: {e}")
        return results

    def cleanup_all(self, context: EngineContext) -> dict[str, bool]:
        """Cleanup all engines."""
        results = {}
        for engine_type, engine in self._instances.items():
            try:
                results[engine_type] = engine.cleanup(context)
            except Exception as e:
                results[engine_type] = False
                context.logger.error(f"Failed to cleanup {engine_type} engine: {e}")
        return results

    def get_all_status(self) -> dict[str, dict[str, Any]]:
        """Get status of all engines."""
        status = {}
        for engine_type, engine in self._instances.items():
            try:
                status[engine_type] = engine.get_status()
            except Exception as e:
                status[engine_type] = {"error": str(e)}
        return status
