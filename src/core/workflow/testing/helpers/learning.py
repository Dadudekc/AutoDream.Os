#!/usr/bin/env python3
"""Learning workflow helpers for integration tests."""

import logging

from ..integration_test_plan_structures import LearningIntegrationResult
from ...learning_integration import LearningWorkflowIntegration


def test_learning_workflow_integration(
    learning_integration: LearningWorkflowIntegration, logger: logging.Logger
) -> LearningIntegrationResult:
    """Test learning workflow integration."""
    logger.info("\ud83e\uddd0 Testing learning workflow integration...")
    result = LearningIntegrationResult()
    try:
        learning_workflow_id = learning_integration.create_learning_workflow(
            "Integration Testing - Learning Workflow", "test_agent_001"
        )
        if learning_workflow_id:
            result.learning_workflows_created += 1
            result.integration_success += 1
            result.details.append(
                {
                    "test_type": "learning_workflow",
                    "workflow_id": learning_workflow_id,
                    "status": "success",
                    "message": "Learning workflow created successfully",
                }
            )
            logger.info(f"\u2705 Created learning workflow: {learning_workflow_id}")
        else:
            result.integration_failures += 1
            result.details.append(
                {
                    "test_type": "learning_workflow",
                    "status": "failed",
                    "message": "Failed to create learning workflow",
                }
            )
        decision_workflow_id = learning_integration.create_decision_workflow(
            "integration_test", "high", {"test_mode": True, "integration_required": True}
        )
        if decision_workflow_id:
            result.decision_workflows_created += 1
            result.integration_success += 1
            result.details.append(
                {
                    "test_type": "decision_workflow",
                    "workflow_id": decision_workflow_id,
                    "status": "success",
                    "message": "Decision workflow created successfully",
                }
            )
            logger.info(f"\u2705 Created decision workflow: {decision_workflow_id}")
        else:
            result.integration_failures += 1
            result.details.append(
                {
                    "test_type": "decision_workflow",
                    "status": "failed",
                    "message": "Failed to create decision workflow",
                }
            )
        integration_status = learning_integration.get_integration_status()
        status = "success" if "error" not in integration_status else "failed"
        result.details.append(
            {
                "test_type": "integration_status",
                "status": status,
                "message": "Integration status retrieved successfully"
                if status == "success"
                else "Failed to get integration status",
            }
        )
        logger.info(
            f"\u2705 Learning workflow integration testing complete: {result.integration_success} successes"
        )
        return result
    except Exception as e:  # pragma: no cover - logging
        logger.error(f"\u274c Learning workflow integration testing failed: {e}")
        return result
