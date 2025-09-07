#!/usr/bin/env python3
"""
Orchestrators Smoke Tests - Agent Cellphone V2
==============================================

Basic smoke tests for orchestration functionality.

Author: Agent-2 (Architecture & Design)
License: MIT
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.core.orchestration.contracts import (
    OrchestrationContext,
    OrchestrationResult,
    Step,
)
from src.core.orchestration.registry import StepRegistry
from src.core.orchestration.core_orchestrator import CoreOrchestrator


class Hello(Step):
    def name(self):
        return "hello"

    def run(self, ctx, payload):
        ctx.logger("hello")
        return {**payload, "hello": True}


def test_core_orchestrator_runs_steps():
    """Test that core orchestrator can run steps."""
    logs = []
    ctx = OrchestrationContext(
        config={}, emit=lambda e, p: None, logger=lambda s: logs.append(s)
    )
    reg = StepRegistry()
    reg.register("hello", lambda: Hello())
    orch = CoreOrchestrator(registry=reg, pipeline=["hello"])
    res: OrchestrationResult = orch.execute(ctx, {})
    assert res.ok is True
    assert res.metrics["steps"] == 1
    assert "hello" in logs


if __name__ == "__main__":
    # Run tests directly
    import sys
    print("Running Orchestrators Smoke Tests...")

    try:
        test_core_orchestrator_runs_steps()
        print("[PASS] Core orchestrator test passed")
        print("[SUCCESS] All orchestrator smoke tests passed!")

    except Exception as e:
        print(f"[FAIL] Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
