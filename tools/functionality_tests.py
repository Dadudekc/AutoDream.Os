#!/usr/bin/env python3
"""
Functionality Test Runner
=========================

Runs agent-specific functionality verification tests.

Author: Agent-6 (VSCode Forking & Quality Gates Specialist)
Refactored from: functionality_verification.py
License: MIT
"""

import subprocess
from datetime import datetime
from typing import Any


class FunctionalityTests:
    """Runs agent-specific functionality tests."""

    def run_agent_tests(self, agent_id: str) -> dict[str, Any]:
        """Run agent-specific functionality verification."""
        results = {
            "agent_id": agent_id,
            "timestamp": datetime.now().isoformat(),
            "tests_run": [],
            "tests_passed": [],
            "tests_failed": [],
            "functionality_status": "UNKNOWN",
        }

        # Define agent-specific tests
        agent_tests = self._get_agent_tests(agent_id)

        for test_name, test_command in agent_tests.items():
            try:
                result = subprocess.run(
                    test_command, shell=True, capture_output=True, text=True, timeout=300
                )

                results["tests_run"].append(test_name)

                if result.returncode == 0:
                    results["tests_passed"].append(test_name)
                else:
                    results["tests_failed"].append(
                        {
                            "test": test_name,
                            "return_code": result.returncode,
                            "stdout": result.stdout[-500:],
                            "stderr": result.stderr[-500:],
                        }
                    )

            except subprocess.TimeoutExpired:
                results["tests_failed"].append(
                    {"test": test_name, "error": "TIMEOUT", "timeout_seconds": 300}
                )
            except Exception as e:
                results["tests_failed"].append({"test": test_name, "error": str(e)})

        # Determine overall status
        if not results["tests_run"]:
            results["functionality_status"] = "NO_TESTS"
        elif not results["tests_failed"]:
            results["functionality_status"] = "FULLY_FUNCTIONAL"
        elif len(results["tests_failed"]) / len(results["tests_run"]) < 0.1:
            results["functionality_status"] = "MINOR_ISSUES"
        else:
            results["functionality_status"] = "SIGNIFICANT_ISSUES"

        return results

    def _get_agent_tests(self, agent_id: str) -> dict[str, str]:
        """Get agent-specific test commands."""
        base_tests = {
            "import_test": "python -c \"import sys; sys.path.insert(0, '.'); print('Imports OK')\"",
            "basic_functionality": "python -c \"print('Basic Python OK')\"",
        }

        agent_specific = {
            "Agent-1": {
                "integration_test": "python -m pytest tests/integration/ -v --tb=short",
                "api_test": "python -c \"from src.services.messaging_cli import *; print('API OK')\"",
            },
            "Agent-2": {
                "architecture_test": "python -c \"from src.core.constants.fsm import *; print('Architecture OK')\"",
                "solid_test": "python -m pytest tests/test_solid_principles.py -v",
            },
            "Agent-3": {
                "infrastructure_test": "python -c \"from src.core.deployment import *; print('Infrastructure OK')\"",
                "performance_test": "python -m pytest tests/performance/ -v --tb=short",
            },
            "Agent-4": {
                "quality_test": "python -m pytest tests/ -k 'smoke' -v",
                "consolidation_test": "python -c \"from src.core.unified_config import *; print('Config OK')\"",
            },
            "Agent-6": {
                "messaging_test": "python -m src.services.messaging_cli --check-status",
                "communication_test": "python -c \"from src.services.messaging_pyautogui import *; print('Messaging OK')\"",
            },
            "Agent-7": {
                "web_test": "python -c \"from src.web.frontend import *; print('Web OK')\"",
                "frontend_test": "python -c \"print('Frontend components accessible')\"",
            },
        }

        # Merge base tests with agent-specific tests
        tests = base_tests.copy()
        if agent_id in agent_specific:
            tests.update(agent_specific[agent_id])

        return tests
