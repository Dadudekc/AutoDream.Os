from src.core.orchestration.contracts import OrchestrationContext, OrchestrationResult, Step
from src.core.orchestration.registry import StepRegistry
from src.core.orchestration.core_orchestrator import CoreOrchestrator

class Hello(Step):
    def name(self): return "hello"
    def run(self, ctx, payload):
        ctx.logger("hello")
        return {**payload, "hello": True}

def test_core_orchestrator_runs_steps(capsys):
    logs = []
    ctx = OrchestrationContext(
        config={}, emit=lambda e,p: None, logger=lambda s: logs.append(s)
    )
    reg = StepRegistry()
    reg.register("hello", lambda: Hello())
    orch = CoreOrchestrator(registry=reg, pipeline=["hello"])
    res: OrchestrationResult = orch.execute(ctx, {})
    assert res.ok is True
    assert res.metrics["steps"] == 1
    assert "hello" in logs
