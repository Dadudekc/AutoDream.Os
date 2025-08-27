#!/usr/bin/env python3
"""Performance and scalability helpers for integration tests."""

import logging
import time

from ..integration_test_plan_structures import PerformanceTestResult
from ...base_workflow_engine import BaseWorkflowEngine


def test_performance_and_scalability(
    base_engine: BaseWorkflowEngine, logger: logging.Logger
) -> PerformanceTestResult:
    """Test workflow system performance and scalability."""
    logger.info("\u26a1 Testing performance and scalability...")
    result = PerformanceTestResult()
    try:
        start_time = time.time()
        test_workflows = []
        for i in range(10):
            workflow_def = {
                "name": f"Performance Test Workflow {i}",
                "description": f"Test workflow for performance testing {i}",
                "steps": [{"step_id": f"test_step_{i}", "name": f"Test Step {i}", "step_type": "test"}],
            }
            workflow_id = base_engine.create_workflow("sequential", workflow_def)
            if workflow_id:
                test_workflows.append(workflow_id)
        result.workflow_creation_time = time.time() - start_time
        result.concurrent_workflows = len(test_workflows)
        if test_workflows:
            start_time = time.time()
            for workflow_id in test_workflows[:5]:
                try:
                    base_engine.execute_workflow(workflow_id)
                except Exception as exc:  # pragma: no cover - logging
                    logger.warning(f"\u26a0\ufe0f Failed to execute workflow {workflow_id}: {exc}")
            result.execution_time = time.time() - start_time
            system_health = base_engine.get_system_health()
            result.details.append(
                {
                    "test_type": "system_health",
                    "result": system_health,
                    "status": "success",
                }
            )
        if result.workflow_creation_time > 0:
            creation_score = max(0, 100 - (result.workflow_creation_time * 100))
            execution_score = max(0, 100 - (result.execution_time * 100))
            result.performance_score = (creation_score + execution_score) / 2
        logger.info(
            f"\u2705 Performance testing complete: Score {result.performance_score:.1f}/100"
        )
        return result
    except Exception as e:  # pragma: no cover - logging
        logger.error(f"\u274c Performance testing failed: {e}")
        return result
