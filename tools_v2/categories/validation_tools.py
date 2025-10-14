#!/usr/bin/env python3
"""
System Validation Tools
=======================

Tools for smoke tests, validation, and system checks.

Author: Agent-7 - Repository Cloning Specialist
Created: 2025-10-13
"""

import logging
import subprocess
import sys
from typing import Any

from ..adapters.base_adapter import IToolAdapter

logger = logging.getLogger(__name__)


class SmokeTestTool(IToolAdapter):
    """Run smoke tests."""

    def execute(self, params: dict[str, Any]) -> dict[str, Any]:
        """Execute smoke tests."""
        try:
            system = params.get("system", "all")

            if system == "all":
                test_files = [
                    "tests/test_msg_task_smoke.py",
                    "tests/test_oss_cli_smoke.py",
                    "tests/test_messaging_smoke.py",
                    "tests/test_error_handling_smoke.py",
                ]
            else:
                test_map = {
                    "msg_task": "tests/test_msg_task_smoke.py",
                    "oss": "tests/test_oss_cli_smoke.py",
                    "messaging": "tests/test_messaging_smoke.py",
                    "errors": "tests/test_error_handling_smoke.py",
                }
                test_files = [test_map.get(system, "")]

            results = []
            for test_file in test_files:
                if test_file:
                    result = subprocess.run(
                        [sys.executable, "-m", "pytest", test_file, "-v", "-m", "smoke"],
                        capture_output=True,
                        text=True,
                    )
                    results.append(
                        {
                            "file": test_file,
                            "passed": result.returncode == 0,
                            "output": result.stdout[-500:] if result.stdout else "",
                        }
                    )

            passing = sum(1 for r in results if r["passed"])
            total = len(results)

            return {
                "success": True,
                "results": results,
                "passed": passing,
                "total": total,
                "all_passed": passing == total,
            }

        except Exception as e:
            return {"success": False, "error": str(e)}


class FeatureFlagTool(IToolAdapter):
    """Check or set feature flags."""

    def execute(self, params: dict[str, Any]) -> dict[str, Any]:
        """Execute feature flag operations."""
        try:
            from src.features.flags import FF_MSG_TASK, FF_OSS_CLI, is_enabled

            action = params.get("action", "check")
            feature = params.get("feature")

            if action == "check":
                if feature:
                    return {"success": True, "feature": feature, "enabled": is_enabled(feature)}
                else:
                    return {
                        "success": True,
                        "flags": {
                            "msg_task": FF_MSG_TASK,
                            "oss_cli": FF_OSS_CLI,
                        },
                    }

            return {"success": False, "error": "Only 'check' action supported via tool"}

        except Exception as e:
            return {"success": False, "error": str(e)}


class RollbackTool(IToolAdapter):
    """Emergency rollback features."""

    def execute(self, params: dict[str, Any]) -> dict[str, Any]:
        """Execute rollback."""
        try:
            from src.features.flags import disable_feature

            feature = params.get("feature")
            if not feature:
                # Disable all
                for feat in ["msg_task", "oss_cli"]:
                    disable_feature(feat)
                return {"success": True, "message": "All features disabled"}
            else:
                disable_feature(feature)
                return {"success": True, "message": f"Feature disabled: {feature}"}

        except Exception as e:
            return {"success": False, "error": str(e)}


class ValidationReportTool(IToolAdapter):
    """Generate validation report for all systems."""

    def execute(self, params: dict[str, Any]) -> dict[str, Any]:
        """Execute validation report."""
        try:
            from src.obs.metrics import snapshot

            metrics = snapshot()

            # Calculate success rates
            ingest_ok = metrics.get("msg_task.ingest.ok", 0)
            ingest_fail = metrics.get("msg_task.ingest.fail", 0)
            ingest_total = ingest_ok + ingest_fail

            report = {
                "timestamp": str(__import__("datetime").datetime.now()),
                "systems": {
                    "msg_task": {
                        "operational": True,
                        "success_rate": (
                            (ingest_ok / ingest_total * 100) if ingest_total > 0 else 100
                        ),
                        "slo_target": 99.0,
                    },
                    "oss": {
                        "operational": True,
                        "clones_ok": metrics.get("oss.clone.ok", 0),
                        "clones_fail": metrics.get("oss.clone.fail", 0),
                    },
                    "messaging": {
                        "operational": True,
                        "sent": metrics.get("messaging.sent", 0),
                        "failed": metrics.get("messaging.failed", 0),
                    },
                },
                "metrics": metrics,
            }

            return {"success": True, "report": report}

        except Exception as e:
            return {"success": False, "error": str(e)}
