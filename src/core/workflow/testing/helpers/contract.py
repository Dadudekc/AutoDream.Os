#!/usr/bin/env python3
"""Contract testing helpers for integration tests."""

import json
import logging
import os
from typing import Any, Dict, Optional

from ..integration_test_plan_structures import ContractIntegrationResult
from ...base_workflow_engine import BaseWorkflowEngine


def load_contract_data(logger: logging.Logger) -> Dict[str, Any]:
    """Load contract data for integration testing."""
    logger.info("\ud83d\udccb Loading contract data for integration testing...")
    contract_data: Dict[str, Any] = {}
    try:
        contract_index_path = "contracts/MASTER_CONTRACT_INDEX.json"
        if os.path.exists(contract_index_path):
            with open(contract_index_path, "r") as f:
                contract_data["master_index"] = json.load(f)
            logger.info("\u2705 Master contract index loaded")

        template_path = "contracts/CONSOLIDATED_CONTRACT_TEMPLATE.json"
        if os.path.exists(template_path):
            with open(template_path, "r") as f:
                contract_data["template"] = json.load(f)
            logger.info("\u2705 Contract template loaded")

        phase_contracts = [
            "contracts/phase3a_core_system_contracts.json",
            "contracts/phase3b_moderate_contracts.json",
            "contracts/phase3c_standard_moderate_contracts.json",
        ]
        for contract_file in phase_contracts:
            if os.path.exists(contract_file):
                with open(contract_file, "r") as f:
                    phase_name = os.path.basename(contract_file).replace(".json", "")
                    contract_data[phase_name] = json.load(f)
                    logger.info(f"\u2705 {phase_name} contracts loaded")
        return contract_data
    except Exception as e:  # pragma: no cover - logging
        logger.error(f"\u274c Failed to load contract data: {e}")
        return {}


def test_contract_workflow_integration(
    base_engine: BaseWorkflowEngine,
    contract_data: Dict[str, Any],
    logger: logging.Logger,
    contract_workflows: Optional[Dict[str, str]] = None,
) -> ContractIntegrationResult:
    """Test workflow system integration with contracts."""
    logger.info("\ud83d\udd04 Testing contract workflow integration...")
    result = ContractIntegrationResult()
    if contract_workflows is None:
        contract_workflows = {}
    try:
        if "master_index" in contract_data:
            master_contract = contract_data["master_index"]
            workflow_definition = {
                "name": "Contract Management Workflow",
                "description": "Automated contract management and tracking",
                "steps": [
                    {"step_id": "contract_analysis", "name": "Contract Analysis", "step_type": "analysis"},
                    {"step_id": "workflow_generation", "name": "Workflow Generation", "step_type": "generation"},
                    {"step_id": "execution_tracking", "step_type": "tracking"},
                ],
                "metadata": {
                    "contract_type": "master_index",
                    "total_phases": master_contract.get("total_phases", 0),
                    "total_contracts": master_contract.get("total_contracts", 0),
                },
            }
            workflow_id = base_engine.create_workflow("sequential", workflow_definition)
            if workflow_id:
                result.workflows_created += 1
                result.integration_success += 1
                contract_workflows["master_index"] = workflow_id
                result.details.append(
                    {
                        "contract_type": "master_index",
                        "workflow_id": workflow_id,
                        "status": "success",
                        "message": "Master contract workflow created successfully",
                    }
                )
                logger.info(f"\u2705 Created workflow for master contract: {workflow_id}")
            else:
                result.integration_failures += 1
                result.details.append(
                    {
                        "contract_type": "master_index",
                        "status": "failed",
                        "message": "Failed to create workflow",
                    }
                )
        for phase_name, phase_data in contract_data.items():
            if phase_name in ["master_index", "template"]:
                continue
            result.contracts_processed += 1
            try:
                phase_workflow_definition = {
                    "name": f"{phase_name.replace('_', ' ').title()} Workflow",
                    "description": f"Automated workflow for {phase_name} contracts",
                    "steps": [
                        {"step_id": "phase_analysis", "name": "Phase Analysis", "step_type": "analysis"},
                        {"step_id": "contract_processing", "name": "Contract Processing", "step_type": "processing"},
                        {"step_id": "validation", "name": "Validation", "step_type": "validation"},
                    ],
                    "metadata": {
                        "contract_type": phase_name,
                        "contract_count": len(phase_data.get("contracts", [])),
                        "priority": phase_data.get("priority", "unknown"),
                    },
                }
                phase_workflow_id = base_engine.create_workflow("sequential", phase_workflow_definition)
                if phase_workflow_id:
                    result.workflows_created += 1
                    result.integration_success += 1
                    contract_workflows[phase_name] = phase_workflow_id
                    result.details.append(
                        {
                            "contract_type": phase_name,
                            "workflow_id": phase_workflow_id,
                            "status": "success",
                            "message": f"{phase_name} workflow created successfully",
                        }
                    )
                    logger.info(f"\u2705 Created workflow for {phase_name}: {phase_workflow_id}")
                else:
                    result.integration_failures += 1
                    result.details.append(
                        {
                            "contract_type": phase_name,
                            "status": "failed",
                            "message": f"Failed to create {phase_name} workflow",
                        }
                    )
            except Exception as e:  # pragma: no cover - logging
                result.integration_failures += 1
                result.details.append(
                    {
                        "contract_type": phase_name,
                        "status": "error",
                        "message": f"Error processing {phase_name}: {str(e)}",
                    }
                )
                logger.error(f"\u274c Error processing {phase_name}: {e}")
        logger.info(
            f"\u2705 Contract integration testing complete: {result.integration_success} successes, {result.integration_failures} failures"
        )
        result.workflows = contract_workflows
        return result
    except Exception as e:  # pragma: no cover - logging
        logger.error(f"\u274c Contract integration testing failed: {e}")
        return result
