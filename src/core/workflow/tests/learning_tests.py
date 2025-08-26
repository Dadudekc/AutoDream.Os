"""Learning workflow integration tests."""

from __future__ import annotations

import logging
from typing import Dict, Any

from ..learning_integration import LearningWorkflowIntegration


def run(
    learning_integration: LearningWorkflowIntegration,
    logger: logging.Logger | None = None,
) -> Dict[str, Any]:
    """Test learning workflow integration using existing unified systems."""
    logger = logger or logging.getLogger(__name__)
    logger.info("🧠 Testing learning workflow integration...")

    test_results: Dict[str, Any] = {
        "learning_workflows_created": 0,
        "decision_workflows_created": 0,
        "integration_success": 0,
        "integration_failures": 0,
        "details": [],
    }

    try:
        # Test learning workflow creation
        test_goal = "Integration Testing - Learning Workflow"
        test_agent = "test_agent_001"

        learning_workflow_id = learning_integration.create_learning_workflow(
            test_goal,
            test_agent,
        )

        if learning_workflow_id:
            test_results["learning_workflows_created"] += 1
            test_results["integration_success"] += 1

            test_results["details"].append(
                {
                    "test_type": "learning_workflow",
                    "workflow_id": learning_workflow_id,
                    "status": "success",
                    "message": "Learning workflow created successfully",
                }
            )

            logger.info(f"✅ Created learning workflow: {learning_workflow_id}")
        else:
            test_results["integration_failures"] += 1
            test_results["details"].append(
                {
                    "test_type": "learning_workflow",
                    "status": "failed",
                    "message": "Failed to create learning workflow",
                }
            )

        # Test decision workflow creation
        decision_workflow_id = learning_integration.create_decision_workflow(
            "integration_test",
            "high",
            {"test_mode": True, "integration_required": True},
        )

        if decision_workflow_id:
            test_results["decision_workflows_created"] += 1
            test_results["integration_success"] += 1

            test_results["details"].append(
                {
                    "test_type": "decision_workflow",
                    "workflow_id": decision_workflow_id,
                    "status": "success",
                    "message": "Decision workflow created successfully",
                }
            )

            logger.info(f"✅ Created decision workflow: {decision_workflow_id}")
        else:
            test_results["integration_failures"] += 1
            test_results["details"].append(
                {
                    "test_type": "decision_workflow",
                    "status": "failed",
                    "message": "Failed to create decision workflow",
                }
            )

        # Test integration status
        integration_status = learning_integration.get_integration_status()

        if "error" not in integration_status:
            test_results["details"].append(
                {
                    "test_type": "integration_status",
                    "status": "success",
                    "message": "Integration status retrieved successfully",
                }
            )
        else:
            test_results["details"].append(
                {
                    "test_type": "integration_status",
                    "status": "failed",
                    "message": "Failed to get integration status",
                }
            )

        logger.info(
            "✅ Learning workflow integration testing complete: %s successes",
            test_results["integration_success"],
        )
        return test_results

    except Exception as e:  # pragma: no cover - logging path
        logger.error(f"❌ Learning workflow integration testing failed: {e}")
        return {"error": str(e)}
