#!/usr/bin/env python3
"""
V3 Directives Validator
=======================

Validates V3 directives deployment across all agents.
V2 Compliance: ≤150 lines, focused responsibility, KISS principle.
"""

import json
from pathlib import Path
from typing import Any


class V3DirectivesValidator:
    """Validates V3 directives deployment across all agents."""

    def __init__(self, agent_workspaces: Path):
        self.agent_workspaces = agent_workspaces
        self.team_alpha = ["Agent-1", "Agent-2", "Agent-3", "Agent-4"]

    def validate(self) -> dict[str, Any]:
        """Validate V3 directives deployment across all agents."""
        print("🔍 Validating V3 directives deployment...")

        validation_results = {}

        for agent_id in self.team_alpha:
            agent_dir = self.agent_workspaces / agent_id

            # Check required files
            files_status = self._check_required_files(agent_dir)

            # Validate V3 contracts
            contracts_valid = self._validate_v3_contracts(agent_id)

            validation_results[agent_id] = {
                "files_present": files_status,
                "v3_contracts_valid": contracts_valid,
                "overall_status": all(files_status.values()) and contracts_valid,
            }

        overall_valid = all(result["overall_status"] for result in validation_results.values())

        return {
            "category": "v3_directives_deployment",
            "status": "PASSED" if overall_valid else "FAILED",
            "results": validation_results,
            "summary": f"{sum(result['overall_status'] for result in validation_results.values())}/{len(self.team_alpha)} agents validated",
        }

    def _check_required_files(self, agent_dir: Path) -> dict[str, bool]:
        """Check if required files are present."""
        required_files = [
            "v3_directives.json",
            "quality_guidelines.json",
            "v3_onboarding_status.json",
            "future_tasks.json",
            "working_tasks.json",
        ]

        files_status = {}
        for file in required_files:
            file_path = agent_dir / file
            files_status[file] = file_path.exists()

        return files_status

    def _validate_v3_contracts(self, agent_id: str) -> bool:
        """Validate V3 contracts for specific agent."""
        try:
            contracts_file = self.agent_workspaces / agent_id / "future_tasks.json"
            if not contracts_file.exists():
                return False

            with open(contracts_file) as f:
                contracts_data = json.load(f)

            # Check if contracts have V3 format
            if "future_tasks" not in contracts_data:
                return False

            # Validate contract structure
            for task in contracts_data["future_tasks"]:
                if not self._validate_contract_structure(task):
                    return False

            return True

        except Exception:
            return False

    def _validate_contract_structure(self, task: dict[str, Any]) -> bool:
        """Validate individual contract structure."""
        required_fields = ["task_id", "title", "priority", "estimated_duration", "description"]

        # Check required fields
        if not all(field in task for field in required_fields):
            return False

        # Check if task_id starts with V3-
        if not task["task_id"].startswith("V3-"):
            return False

        return True
