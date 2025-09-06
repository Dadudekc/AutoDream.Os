from __future__ import annotations
from typing import Dict, Any, Iterable, Type
from ..contracts import Orchestrator, Step, OrchestrationContext, OrchestrationResult
from ..core_orchestrator import CoreOrchestrator
from ..registry import StepRegistry

LEGACY_MAP = {
    "FileLockingOrchestrator": ["lock.init", "lock.acquire", "lock.release"],
    "VectorDatabaseMLOptimizer": ["ml.load", "ml.optimize", "ml.persist"],
    "DeploymentOrchestratorEngine": ["deploy.init", "deploy.execute", "deploy.verify"],
    "EnhancedIntegrationOrchestrator": [
        "integration.init",
        "integration.coordinate",
        "integration.optimize",
    ],
    "SwarmCoordinationEnhancer": ["swarm.init", "swarm.coordinate", "swarm.monitor"],
    "EmergencyInterventionOrchestrator": [
        "emergency.init",
        "emergency.assess",
        "emergency.intervene",
    ],
    "MessagingOptimizationOrchestrator": [
        "messaging.init",
        "messaging.optimize",
        "messaging.deliver",
    ],
}


class LegacyOrchestratorAdapter(Orchestrator):
    """Wrap a legacy Orchestrator interface to the new CoreOrchestrator without breaking
    callers."""

    def __init__(self, legacy_name: str, registry: StepRegistry) -> None:
        self.legacy_name = legacy_name
        pipeline = LEGACY_MAP.get(legacy_name, [])
        self.core = CoreOrchestrator(registry, pipeline)

    def plan(
        self, ctx: OrchestrationContext, payload: Dict[str, Any]
    ) -> Iterable[Step]:
        return self.core.plan(ctx, payload)

    def execute(
        self, ctx: OrchestrationContext, payload: Dict[str, Any]
    ) -> OrchestrationResult:
        return self.core.execute(ctx, payload)

    def report(self, result: OrchestrationResult) -> str:
        return f"[LegacyAdapter:{self.legacy_name}] {self.core.report(result)}"
