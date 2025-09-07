# Core Engines Package - Phase-2 Consolidation
from .contracts import (
    Engine,
    EngineContext,
    EngineResult,
    MLEngine,
    AnalysisEngine,
    IntegrationEngine,
    CoordinationEngine,
    UtilityEngine,
)
from .registry import EngineRegistry
from .ml_core_engine import MLCoreEngine
from .analysis_core_engine import AnalysisCoreEngine
from .integration_core_engine import IntegrationCoreEngine
from .coordination_core_engine import CoordinationCoreEngine
from .utility_core_engine import UtilityCoreEngine
from .data_core_engine import DataCoreEngine
from .communication_core_engine import CommunicationCoreEngine
from .validation_core_engine import ValidationCoreEngine
from .configuration_core_engine import ConfigurationCoreEngine
from .monitoring_core_engine import MonitoringCoreEngine
from .security_core_engine import SecurityCoreEngine
from .performance_core_engine import PerformanceCoreEngine
from .storage_core_engine import StorageCoreEngine
from .processing_core_engine import ProcessingCoreEngine
from .orchestration_core_engine import OrchestrationCoreEngine

__all__ = [
    # Contracts
    "Engine",
    "EngineContext",
    "EngineResult",
    "MLEngine",
    "AnalysisEngine",
    "IntegrationEngine",
    "CoordinationEngine",
    "UtilityEngine",
    # Registry
    "EngineRegistry",
    # Core Engines
    "MLCoreEngine",
    "AnalysisCoreEngine",
    "IntegrationCoreEngine",
    "CoordinationCoreEngine",
    "UtilityCoreEngine",
    "DataCoreEngine",
    "CommunicationCoreEngine",
    "ValidationCoreEngine",
    "ConfigurationCoreEngine",
    "MonitoringCoreEngine",
    "SecurityCoreEngine",
    "PerformanceCoreEngine",
    "StorageCoreEngine",
    "ProcessingCoreEngine",
    "OrchestrationCoreEngine",
]
