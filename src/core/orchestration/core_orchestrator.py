from __future__ import annotations
from typing import Dict, Any, Iterable, List
from .contracts import Orchestrator, Step, OrchestrationContext, OrchestrationResult
from .registry import StepRegistry


class CoreOrchestrator(Orchestrator):
    """Single SRP: execute a pipeline of Steps with events + metrics."""

    def __init__(self, registry: StepRegistry, pipeline: Iterable[str]) -> None:
        self.registry = registry
        self.pipeline_keys = list(pipeline)

    def plan(
        self, ctx: OrchestrationContext, payload: Dict[str, Any]
    ) -> Iterable[Step]:
        return self.registry.build(self.pipeline_keys)

    def execute(
        self, ctx: OrchestrationContext, payload: Dict[str, Any]
    ) -> OrchestrationResult:
        ctx.emit("orchestrator.start", {"pipeline": self.pipeline_keys})
        data: Dict[str, Any] = dict(payload)
        steps = list(self.plan(ctx, payload))
        for s in steps:
            ctx.emit("step.start", {"name": s.name()})
            data = s.run(ctx, data)
            ctx.emit("step.end", {"name": s.name()})
        summary = f"ran {len(steps)} step(s)"
        ctx.emit("orchestrator.end", {"summary": summary})
        return OrchestrationResult(
            ok=True, summary=summary, metrics={"steps": len(steps)}
        )

    def report(self, result: OrchestrationResult) -> str:
        return f"[CoreOrchestrator] {result.summary} :: metrics={result.metrics}"
