#!/usr/bin/env python3
"""Workflow system integration test suite loader."""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import Dict, Any

import sys
sys.path.append(str(Path(__file__).parent.parent.parent))

from .base_workflow_engine import BaseWorkflowEngine
from .specialized.business_process_workflow import BusinessProcessWorkflow
from .learning_integration import LearningWorkflowIntegration
from .tests import contract_tests, learning_tests, workflow_tests


class WorkflowIntegrationTestPlan:
    """Aggregate and run workflow integration tests."""

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.base_engine = BaseWorkflowEngine()
        self.business_process_workflow = BusinessProcessWorkflow()
        self.learning_integration = LearningWorkflowIntegration()
        self.contract_data: Dict[str, Any] = {}
        self.contract_workflows: Dict[str, str] = {}

    def load_contract_data(self) -> Dict[str, Any]:
        """Load contract data required for integration tests."""
        self.logger.info("📋 Loading contract data for integration testing...")
        data: Dict[str, Any] = {}
        try:
            index_path = "contracts/MASTER_CONTRACT_INDEX.json"
            if os.path.exists(index_path):
                with open(index_path, "r") as f:
                    data["master_index"] = json.load(f)
            template_path = "contracts/CONSOLIDATED_CONTRACT_TEMPLATE.json"
            if os.path.exists(template_path):
                with open(template_path, "r") as f:
                    data["template"] = json.load(f)
        except Exception as e:  # pragma: no cover - logging path
            self.logger.error(f"❌ Failed to load contract data: {e}")
        return data

    def run_comprehensive_integration_test(self) -> Dict[str, Any]:
        """Run all workflow integration test suites."""
        self.contract_data = self.load_contract_data()
        return {
            "contract_integration": contract_tests.run(
                self.base_engine, self.contract_data, self.contract_workflows, self.logger
            ),
            "learning_integration": learning_tests.run(
                self.learning_integration, self.logger
            ),
            "business_process_integration": workflow_tests.run(
                self.business_process_workflow, self.logger
            ),
        }


def main() -> None:
    plan = WorkflowIntegrationTestPlan()
    results = plan.run_comprehensive_integration_test()
    print(results)


if __name__ == "__main__":
    main()
