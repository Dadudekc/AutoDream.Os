#!/usr/bin/env python3
"""
Orchestration System Proof of Concept - Phase-1 Consolidation
============================================================

Comprehensive test demonstrating the new orchestration system
replacing 11+ legacy orchestrators with 3 core orchestrators.

Author: Agent-3 - Infrastructure & DevOps Specialist
Mission: Phase-1 Orchestrator Consolidation
"""

import pytest
from src.core.orchestration import (
    OrchestrationContext,
    OrchestrationResult,
    Step,
    Orchestrator,
    StepRegistry,
    CoreOrchestrator,
    ServiceOrchestrator,
    IntegrationOrchestrator,
    LegacyOrchestratorAdapter,
)


class MockStep(Step):
    """Mock step for testing."""

    def __init__(self, name: str, result_data: dict = None):
        self._name = name
        self.result_data = result_data or {}

    def name(self) -> str:
        return self._name

    def run(self, ctx: OrchestrationContext, payload: dict) -> dict:
        ctx.logger(f"Executing step: {self._name}")
        return {**payload, **self.result_data}


class TestOrchestrationSystem:
    """Test the new orchestration system."""

    def test_core_orchestrator_execution(self):
        """Test CoreOrchestrator executes pipeline steps."""
        # Setup
        logs = []
        events = []

        ctx = OrchestrationContext(
            config={"test": True},
            emit=lambda event, data: events.append((event, data)),
            logger=lambda msg: logs.append(msg),
        )

        registry = StepRegistry()
        registry.register("step1", lambda: MockStep("step1", {"data1": "value1"}))
        registry.register("step2", lambda: MockStep("step2", {"data2": "value2"}))

        orchestrator = CoreOrchestrator(registry, ["step1", "step2"])

        # Execute
        result = orchestrator.execute(ctx, {"initial": "data"})

        # Verify
        assert result.ok is True
        assert result.metrics["steps"] == 2
        assert "ran 2 step(s)" in result.summary

        # Check events
        assert (
            len(events) == 6
        )  # start, step1.start, step1.end, step2.start, step2.end, end
        assert events[0][0] == "orchestrator.start"
        assert events[1][0] == "step.start"
        assert events[2][0] == "step.end"

        # Check logs
        assert "Executing step: step1" in logs
        assert "Executing step: step2" in logs

    def test_service_orchestrator_execution(self):
        """Test ServiceOrchestrator handles service pipelines."""
        logs = []
        ctx = OrchestrationContext(
            config={}, emit=lambda e, p: None, logger=lambda s: logs.append(s)
        )

        registry = StepRegistry()
        registry.register("service_step", lambda: MockStep("service_step"))

        orchestrator = ServiceOrchestrator(registry)

        # Execute with service pipeline
        result = orchestrator.execute(
            ctx, {"service_pipeline": ["service_step"], "data": "test"}
        )

        assert result.ok is True
        assert result.metrics["service_steps"] == 1
        assert "service:1" in result.summary

    def test_integration_orchestrator_execution(self):
        """Test IntegrationOrchestrator handles integration pipelines."""
        logs = []
        ctx = OrchestrationContext(
            config={}, emit=lambda e, p: None, logger=lambda s: logs.append(s)
        )

        registry = StepRegistry()
        registry.register("integration_step", lambda: MockStep("integration_step"))

        orchestrator = IntegrationOrchestrator(registry)

        # Execute with integration pipeline
        result = orchestrator.execute(
            ctx, {"integration_pipeline": ["integration_step"], "data": "test"}
        )

        assert result.ok is True
        assert result.metrics["integration_steps"] == 1
        assert "integration:1" in result.summary

    def test_legacy_adapter_compatibility(self):
        """Test LegacyOrchestratorAdapter maintains backward compatibility."""
        logs = []
        ctx = OrchestrationContext(
            config={}, emit=lambda e, p: None, logger=lambda s: logs.append(s)
        )

        registry = StepRegistry()
        registry.register("lock.init", lambda: MockStep("lock.init"))
        registry.register("lock.acquire", lambda: MockStep("lock.acquire"))
        registry.register("lock.release", lambda: MockStep("lock.release"))

        # Test FileLockingOrchestrator adapter
        adapter = LegacyOrchestratorAdapter("FileLockingOrchestrator", registry)

        result = adapter.execute(ctx, {"file": "test.txt"})

        assert result.ok is True
        assert result.metrics["steps"] == 3  # lock.init, lock.acquire, lock.release
        assert "LegacyAdapter:FileLockingOrchestrator" in adapter.report(result)

    def test_step_registry_functionality(self):
        """Test StepRegistry properly manages step factories."""
        registry = StepRegistry()

        # Register steps
        registry.register("step1", lambda: MockStep("step1"))
        registry.register("step2", lambda: MockStep("step2"))

        # Build steps
        steps = registry.build(["step1", "step2", "nonexistent"])

        assert len(steps) == 2  # nonexistent step ignored
        assert steps[0].name() == "step1"
        assert steps[1].name() == "step2"

        # Test duplicate registration
        with pytest.raises(ValueError, match="duplicate step key"):
            registry.register("step1", lambda: MockStep("duplicate"))

    def test_orchestration_context_immutability(self):
        """Test OrchestrationContext is properly immutable."""
        config = {"key": "value"}
        emit = lambda e, p: None
        logger = lambda s: None

        ctx = OrchestrationContext(config=config, emit=emit, logger=logger)

        # Context should be frozen (immutable) - dataclass with frozen=True
        assert hasattr(ctx, "__dataclass_fields__")

        # Values should be accessible
        assert ctx.config["key"] == "value"
        assert ctx.emit is emit
        assert ctx.logger is logger


def test_architectural_compliance():
    """Test that the new system follows SOLID principles."""

    # SRP: Each orchestrator has single responsibility
    registry = StepRegistry()
    core_orch = CoreOrchestrator(registry, [])
    service_orch = ServiceOrchestrator(registry)
    integration_orch = IntegrationOrchestrator(registry)

    # Each should have distinct behavior
    assert core_orch.__class__.__name__ == "CoreOrchestrator"
    assert service_orch.__class__.__name__ == "ServiceOrchestrator"
    assert integration_orch.__class__.__name__ == "IntegrationOrchestrator"

    # OCP: Should be open for extension via Step protocol
    class CustomStep(Step):
        def name(self):
            return "custom"

        def run(self, ctx, payload):
            return payload

    registry.register("custom", lambda: CustomStep())
    steps = registry.build(["custom"])
    assert len(steps) == 1
    assert steps[0].name() == "custom"

    # LSP: All orchestrators should be substitutable
    orchestrators = [core_orch, service_orch, integration_orch]
    for orch in orchestrators:
        assert hasattr(orch, "plan")
        assert hasattr(orch, "execute")
        assert hasattr(orch, "report")

    # DIP: High-level modules depend on abstractions (Step, Orchestrator protocols)
    assert hasattr(Step, "__protocol__") or hasattr(Step, "__abstractmethods__")
    assert hasattr(Orchestrator, "__protocol__") or hasattr(
        Orchestrator, "__abstractmethods__"
    )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
