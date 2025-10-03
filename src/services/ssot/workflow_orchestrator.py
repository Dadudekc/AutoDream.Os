#!/usr/bin/env python3
"""
SSOT Workflow Orchestrator
==========================

V2 Compliant: ≤400 lines, implements SSOT workflow orchestration
for autonomous development system.

This module orchestrates all SSOT workflows to ensure consistent
data across the autonomous development system.

🐝 WE ARE SWARM - SSOT Workflow Optimization
"""

import json
import logging
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SSOTWorkflowOrchestrator:
    """Orchestrates SSOT workflows for autonomous development."""

    def __init__(self, project_root: str = "."):
        """Initialize SSOT workflow orchestrator."""
        self.project_root = Path(project_root)
        self.services_dir = self.project_root / "src" / "services"

        # SSOT workflow components
        self.workflow_components = {
            "config_sync": "ssot/config_sync.py",
            "role_consistency": "ssot/role_consistency.py",
            "ssot_validator": "ssot/ssot_validator.py",
            "anti_slop": "anti_slop/anti_slop_protocol.py",
        }

        # Workflow execution log
        self.execution_log = []

    def execute_full_ssot_workflow(self) -> dict[str, Any]:
        """Execute complete SSOT workflow."""
        logger.info("Starting full SSOT workflow execution")

        workflow_results = {
            "workflow_id": f"SSOT_WORKFLOW_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "start_time": datetime.now().isoformat(),
            "components_executed": [],
            "results": {},
            "total_time": 0,
            "success": True,
        }

        start_time = time.time()

        try:
            # Step 1: Configuration Synchronization
            config_result = self._execute_config_sync()
            workflow_results["components_executed"].append("config_sync")
            workflow_results["results"]["config_sync"] = config_result

            # Step 2: Role Consistency Enforcement
            role_result = self._execute_role_consistency()
            workflow_results["components_executed"].append("role_consistency")
            workflow_results["results"]["role_consistency"] = role_result

            # Step 3: SSOT Validation
            validation_result = self._execute_ssot_validation()
            workflow_results["components_executed"].append("ssot_validation")
            workflow_results["results"]["ssot_validation"] = validation_result

            # Step 4: Content Quality Control
            quality_result = self._execute_content_quality()
            workflow_results["components_executed"].append("content_quality")
            workflow_results["results"]["content_quality"] = quality_result

            # Step 5: Generate Workflow Report
            report_result = self._generate_workflow_report(workflow_results)
            workflow_results["results"]["workflow_report"] = report_result

        except Exception as e:
            logger.error(f"SSOT workflow execution failed: {e}")
            workflow_results["success"] = False
            workflow_results["error"] = str(e)

        workflow_results["total_time"] = time.time() - start_time
        workflow_results["end_time"] = datetime.now().isoformat()

        # Log execution
        self.execution_log.append(workflow_results)
        self._save_execution_log()

        logger.info(
            f"SSOT workflow execution complete. Time: {workflow_results['total_time']:.2f}s"
        )
        return workflow_results

    def _execute_config_sync(self) -> dict[str, Any]:
        """Execute configuration synchronization."""
        logger.info("Executing configuration synchronization")

        try:
            config_sync_path = self.services_dir / self.workflow_components["config_sync"]
            result = subprocess.run(
                [sys.executable, str(config_sync_path)], capture_output=True, text=True, timeout=60
            )

            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "execution_time": 0.5,  # Estimated
            }
        except Exception as e:
            logger.error(f"Config sync execution failed: {e}")
            return {"success": False, "error": str(e), "execution_time": 0}

    def _execute_role_consistency(self) -> dict[str, Any]:
        """Execute role consistency enforcement."""
        logger.info("Executing role consistency enforcement")

        try:
            role_consistency_path = self.services_dir / self.workflow_components["role_consistency"]
            result = subprocess.run(
                [sys.executable, str(role_consistency_path)],
                capture_output=True,
                text=True,
                timeout=60,
            )

            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "execution_time": 0.3,  # Estimated
            }
        except Exception as e:
            logger.error(f"Role consistency execution failed: {e}")
            return {"success": False, "error": str(e), "execution_time": 0}

    def _execute_ssot_validation(self) -> dict[str, Any]:
        """Execute SSOT validation."""
        logger.info("Executing SSOT validation")

        try:
            ssot_validator_path = self.services_dir / self.workflow_components["ssot_validator"]
            result = subprocess.run(
                [sys.executable, str(ssot_validator_path)],
                capture_output=True,
                text=True,
                timeout=60,
            )

            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "execution_time": 0.4,  # Estimated
            }
        except Exception as e:
            logger.error(f"SSOT validation execution failed: {e}")
            return {"success": False, "error": str(e), "execution_time": 0}

    def _execute_content_quality(self) -> dict[str, Any]:
        """Execute content quality control."""
        logger.info("Executing content quality control")

        try:
            anti_slop_path = self.services_dir / self.workflow_components["anti_slop"]
            result = subprocess.run(
                [sys.executable, str(anti_slop_path)], capture_output=True, text=True, timeout=60
            )

            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "execution_time": 0.2,  # Estimated
            }
        except Exception as e:
            logger.error(f"Content quality execution failed: {e}")
            return {"success": False, "error": str(e), "execution_time": 0}

    def _generate_workflow_report(self, workflow_results: dict[str, Any]) -> dict[str, Any]:
        """Generate comprehensive workflow report."""
        logger.info("Generating SSOT workflow report")

        report = {
            "workflow_summary": {
                "workflow_id": workflow_results["workflow_id"],
                "total_time": workflow_results["total_time"],
                "components_executed": len(workflow_results["components_executed"]),
                "success": workflow_results["success"],
            },
            "component_results": {},
            "efficiency_metrics": {
                "total_execution_time": workflow_results["total_time"],
                "average_component_time": 0,
                "success_rate": 0,
            },
            "recommendations": [],
        }

        # Analyze component results
        successful_components = 0
        total_component_time = 0

        for component, result in workflow_results["results"].items():
            if component != "workflow_report":
                report["component_results"][component] = {
                    "success": result.get("success", False),
                    "execution_time": result.get("execution_time", 0),
                }

                if result.get("success", False):
                    successful_components += 1

                total_component_time += result.get("execution_time", 0)

        # Calculate efficiency metrics
        report["efficiency_metrics"]["average_component_time"] = (
            total_component_time / len(workflow_results["components_executed"])
            if workflow_results["components_executed"]
            else 0
        )
        report["efficiency_metrics"]["success_rate"] = (
            successful_components / len(workflow_results["components_executed"])
            if workflow_results["components_executed"]
            else 0
        )

        # Generate recommendations
        if report["efficiency_metrics"]["success_rate"] < 1.0:
            report["recommendations"].append("Some components failed - review error logs")

        if report["efficiency_metrics"]["total_execution_time"] > 5.0:
            report["recommendations"].append(
                "Workflow execution time exceeds 5 seconds - optimize components"
            )

        return report

    def _save_execution_log(self):
        """Save execution log to file."""
        log_file = self.project_root / "ssot_workflow_log.json"
        try:
            with open(log_file, "w", encoding="utf-8") as f:
                json.dump(self.execution_log, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving execution log: {e}")

    def get_workflow_status(self) -> dict[str, Any]:
        """Get current workflow status."""
        return {
            "orchestrator_status": "ACTIVE",
            "components_available": len(self.workflow_components),
            "last_execution": self.execution_log[-1] if self.execution_log else None,
            "total_executions": len(self.execution_log),
        }


def main():
    """Main execution function."""
    orchestrator = SSOTWorkflowOrchestrator()

    # Execute full SSOT workflow
    results = orchestrator.execute_full_ssot_workflow()

    print("SSOT Workflow Execution Results:")
    print(f"  Workflow ID: {results['workflow_id']}")
    print(f"  Success: {results['success']}")
    print(f"  Total Time: {results['total_time']:.2f}s")
    print(f"  Components Executed: {len(results['components_executed'])}")

    # Get workflow status
    status = orchestrator.get_workflow_status()
    print(f"  Orchestrator Status: {status['orchestrator_status']}")


if __name__ == "__main__":
    main()
