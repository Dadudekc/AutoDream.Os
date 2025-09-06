from __future__ import annotations
from typing import Dict, Any, Iterable
from .contracts import Orchestrator, Step, OrchestrationContext, OrchestrationResult
from .registry import StepRegistry

class ServiceOrchestrator(Orchestrator):
    """Service-scope orchestration: IO, messaging, analytics service flows."""
    def __init__(self, registry: StepRegistry) -> None:
        self.registry = registry

    def plan(self, ctx: OrchestrationContext, payload: Dict[str, Any]) -> Iterable[Step]:
        keys = payload.get("service_pipeline", [])
        return self.registry.build(keys)

    def execute(self, ctx: OrchestrationContext, payload: Dict[str, Any]) -> OrchestrationResult:
        steps = list(self.plan(ctx, payload))
        data = dict(payload)
        for s in steps:
            data = s.run(ctx, data)
        return OrchestrationResult(ok=True, summary=f"service:{len(steps)}", metrics={"service_steps": len(steps)})

    def report(self, result: OrchestrationResult) -> str:
        return f"[ServiceOrchestrator] {result.summary}"
