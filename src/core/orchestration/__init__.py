# Orchestration package - Phase-1 Consolidation
from .contracts import OrchestrationContext, OrchestrationResult, Step, Orchestrator
from .registry import StepRegistry
from .core_orchestrator import CoreOrchestrator
from .service_orchestrator import ServiceOrchestrator
from .integration_orchestrator import IntegrationOrchestrator
from .adapters.legacy_adapter import LegacyOrchestratorAdapter

__all__ = [
    "OrchestrationContext",
    "OrchestrationResult",
    "Step",
    "Orchestrator",
    "StepRegistry",
    "CoreOrchestrator",
    "ServiceOrchestrator",
    "IntegrationOrchestrator",
    "LegacyOrchestratorAdapter",
]
