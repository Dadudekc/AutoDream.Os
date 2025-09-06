from __future__ import annotations
from typing import Dict, Any, Iterable
from .contracts import Orchestrator, Step, OrchestrationContext, OrchestrationResult
from .registry import StepRegistry

class IntegrationOrchestrator(Orchestrator):
    """Integration-scope: external APIs, adapters, retries (kept simple = KISS)."""
    def __init__(self, registry: StepRegistry) -> None:
        self.registry = registry

    def plan(self, ctx: OrchestrationContext, payload: Dict[str, Any]) -> Iterable[Step]:
        keys = payload.get("integration_pipeline", [])
        return self.registry.build(keys)

    def execute(self, ctx: OrchestrationContext, payload: Dict[str, Any]) -> OrchestrationResult:
        data = dict(payload)
        steps = list(self.plan(ctx, payload))
        for s in steps:
            data = s.run(ctx, data)
        return OrchestrationResult(ok=True, summary=f"integration:{len(steps)}", metrics={"integration_steps": len(steps)})

    def report(self, result: OrchestrationResult) -> str:
        return f"[IntegrationOrchestrator] {result.summary}"
