#!/usr/bin/env python3
"""Data model compatibility helpers for integration tests."""

import logging

from ..integration_test_plan_structures import DataModelCompatibilityResult
from ...base_workflow_engine import BaseWorkflowEngine
from ...specialized.business_process_workflow import BusinessProcessWorkflow


def test_data_model_compatibility(
    base_engine: BaseWorkflowEngine,
    business_process_workflow: BusinessProcessWorkflow,
    logger: logging.Logger,
) -> DataModelCompatibilityResult:
    """Test data model compatibility between workflow system and contracts."""
    logger.info("\ud83d\udd0d Testing data model compatibility...")
    result = DataModelCompatibilityResult()
    try:
        test_definition = {
            "name": "Contract Integration Test",
            "description": "Test workflow for contract integration",
            "steps": [
                {"step_id": "contract_load", "name": "Load Contract", "step_type": "data_loading"},
                {"step_id": "workflow_generate", "name": "Generate Workflow", "step_type": "workflow_generation"},
                {"step_id": "validate", "name": "Validate Integration", "step_type": "validation"},
            ],
            "metadata": {
                "contract_integration": True,
                "test_mode": True,
                "validation_required": True,
            },
        }
        try:
            workflow_id = base_engine.create_workflow("sequential", test_definition)
            result.models_tested += 1
            if workflow_id:
                result.compatibility_success += 1
                result.details.append(
                    {
                        "test_type": "workflow_creation",
                        "status": "success",
                        "message": "Workflow definition compatible with system",
                    }
                )
            else:
                result.compatibility_failures += 1
                result.details.append(
                    {
                        "test_type": "workflow_creation",
                        "status": "failed",
                        "message": "Workflow creation failed",
                    }
                )
        except Exception as e:  # pragma: no cover - logging
            result.compatibility_failures += 1
            result.validation_errors.append(str(e))
            result.details.append(
                {
                    "test_type": "workflow_creation",
                    "status": "error",
                    "message": f"Workflow creation error: {str(e)}",
                }
            )
        try:
            business_data = {
                "business_unit": "Integration Testing",
                "priority": "high",
                "compliance_required": True,
                "expected_duration": 24,
                "business_rules": {"test_mode": True, "validation_required": True},
            }
            business_workflow_id = business_process_workflow.create_business_process(
                "compliance", business_data
            )
            result.models_tested += 1
            if business_workflow_id:
                result.compatibility_success += 1
                result.details.append(
                    {
                        "test_type": "business_process",
                        "status": "success",
                        "message": "Business process data model compatible",
                    }
                )
            else:
                result.compatibility_failures += 1
                result.details.append(
                    {
                        "test_type": "business_process",
                        "status": "failed",
                        "message": "Business process creation failed",
                    }
                )
        except Exception as e:  # pragma: no cover - logging
            result.compatibility_failures += 1
            result.validation_errors.append(str(e))
            result.details.append(
                {
                    "test_type": "business_process",
                    "status": "error",
                    "message": f"Business process error: {str(e)}",
                }
            )
        logger.info(
            f"\u2705 Data model compatibility testing complete: {result.compatibility_success} successes, {result.compatibility_failures} failures"
        )
        return result
    except Exception as e:  # pragma: no cover - logging
        logger.error(f"\u274c Data model compatibility testing failed: {e}")
        return result
