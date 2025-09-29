#!/usr/bin/env python3
"""
Quality Gates Validator
=======================

Validates quality gates functionality and configuration.
V2 Compliance: ≤150 lines, focused responsibility, KISS principle.
"""

import subprocess
import sys
from pathlib import Path
from typing import Any


class QualityGatesValidator:
    """Validates quality gates functionality."""

    def validate(self) -> dict[str, Any]:
        """Validate quality gates functionality."""
        print("🔍 Validating quality gates functionality...")

        try:
            # Run quality gates script
            result = subprocess.run(
                [sys.executable, "quality_gates.py", "--path", "src"],
                capture_output=True,
                text=True,
                cwd=".",
            )

            quality_gates_working = result.returncode == 0

            # Check configuration files
            config_status = self._check_configuration_files()

            overall_status = (
                quality_gates_working
                and config_status["precommit_exists"]
                and config_status["script_exists"]
            )

            return {
                "category": "quality_gates_functionality",
                "status": "PASSED" if overall_status else "FAILED",
                "results": {
                    "quality_gates_script": config_status["script_exists"],
                    "precommit_config": config_status["precommit_exists"],
                    "quality_gates_execution": quality_gates_working,
                    "output": result.stdout if result.stdout else result.stderr,
                },
                "summary": f"Quality gates: {'Working' if quality_gates_working else 'Failed'}",
            }

        except Exception as e:
            return {
                "category": "quality_gates_functionality",
                "status": "FAILED",
                "results": {"error": str(e)},
                "summary": "Quality gates validation failed",
            }

    def _check_configuration_files(self) -> dict[str, bool]:
        """Check if required configuration files exist."""
        return {
            "precommit_exists": Path(".pre-commit-config.yaml").exists(),
            "script_exists": Path("quality_gates.py").exists(),
        }
