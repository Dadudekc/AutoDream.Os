"""
Captain Advanced Tools - Critical Additions from 2025-10-13 Session
====================================================================

Advanced tools discovered during Cycle coordination:
- File existence validation (prevents phantom tasks)
- Project scan automation
- Phantom task detection
- Multi-agent fuel delivery
- Swarm status dashboard
- Agent readiness checks
- Task pool validation
- Markov ROI integration
- Completion tracking

Discovered Needs:
- Agent-5: ml_optimizer_models.py phantom task
- Agent-7: verification_plan.py phantom task
- Agent-6: Self-prompting protocol validation
- Team Beta: Drive Mode coordination

V2 Compliance: <400 lines
Author: Agent-4 (Captain) - Session 2025-10-13
"""

import json
import logging
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any

from ..adapters.base_adapter import IToolAdapter, ToolResult, ToolSpec
from ..adapters.error_types import ToolExecutionError

logger = logging.getLogger(__name__)

# Swarm agents list
SWARM_AGENTS = [f"Agent-{i}" for i in range(1, 9)]


class FileExistenceValidator(IToolAdapter):
    """Validate file existence before task assignment (prevents phantom tasks)."""

    def get_spec(self) -> ToolSpec:
        """Get tool specification."""
        return ToolSpec(
            name="captain.validate_file_exists",
            version="1.0.0",
            category="captain",
            summary="Verify file exists before assigning as task (prevents phantom tasks)",
            required_params=["file_path"],
            optional_params={"check_size": True},
        )

    def validate(self, params: dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate parameters."""
        spec = self.get_spec()
        return spec.validate_params(params)

    def execute(self, params: dict[str, Any], context: dict[str, Any] | None = None) -> ToolResult:
        """Execute file existence validation."""
        try:
            file_path = params["file_path"]
            check_size = params.get("check_size", True)

            file = Path(file_path)
            exists = file.exists()

            validation = {
                "file_path": file_path,
                "exists": exists,
                "is_phantom": not exists,
                "verdict": "VALID" if exists else "PHANTOM_TASK",
            }

            if exists and check_size:
                validation["size"] = file.stat().st_size
                validation["lines"] = len(
                    file.read_text(encoding="utf-8", errors="ignore").splitlines()
                )

            return ToolResult(success=True, output=validation, exit_code=0 if exists else 1)
        except Exception as e:
            logger.error(f"Error validating file existence: {e}")
            raise ToolExecutionError(str(e), tool_name="captain.validate_file_exists")


class ProjectScanRunner(IToolAdapter):
    """Run fresh project scan to update violation data."""

    def get_spec(self) -> ToolSpec:
        """Get tool specification."""
        return ToolSpec(
            name="captain.run_project_scan",
            version="1.0.0",
            category="captain",
            summary="Run fresh project scan to update violations and eliminate phantom files",
            required_params=[],
            optional_params={"generate_reports": True},
        )

    def validate(self, params: dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate parameters."""
        return (True, [])

    def execute(self, params: dict[str, Any], context: dict[str, Any] | None = None) -> ToolResult:
        """Execute project scan."""
        try:
            # Run project scanner
            result = subprocess.run(
                ["python", "tools/run_project_scan.py"],
                capture_output=True,
                text=True,
                cwd=Path.cwd(),
            )

            scan_output = {
                "scan_completed": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
            }

            # Check if project_analysis.json was updated
            analysis_file = Path("project_analysis.json")
            if analysis_file.exists():
                scan_output["analysis_updated"] = True
                scan_output["analysis_file"] = str(analysis_file)

                # Count violations
                with open(analysis_file) as f:
                    data = json.load(f)
                    scan_output["total_files"] = len(data)

            return ToolResult(
                success=result.returncode == 0, output=scan_output, exit_code=result.returncode
            )
        except Exception as e:
            logger.error(f"Error running project scan: {e}")
            raise ToolExecutionError(str(e), tool_name="captain.run_project_scan")


class PhantomTaskDetector(IToolAdapter):
    """Detect phantom tasks (files in task pool that don't exist)."""

    def get_spec(self) -> ToolSpec:
        """Get tool specification."""
        return ToolSpec(
            name="captain.detect_phantoms",
            version="1.0.0",
            category="captain",
            summary="Detect phantom tasks in project_analysis.json",
            required_params=[],
            optional_params={"analysis_file": "project_analysis.json"},
        )

    def validate(self, params: dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate parameters."""
        return (True, [])

    def execute(self, params: dict[str, Any], context: dict[str, Any] | None = None) -> ToolResult:
        """Execute phantom detection."""
        try:
            analysis_file = Path(params.get("analysis_file", "project_analysis.json"))

            if not analysis_file.exists():
                return ToolResult(
                    success=False,
                    output={"error": "project_analysis.json not found"},
                    exit_code=1,
                    error_message="Analysis file does not exist",
                )

            with open(analysis_file) as f:
                data = json.load(f)

            phantom_tasks = []
            valid_tasks = []

            for file_path in data.keys():
                file = Path(file_path)
                if file.exists():
                    valid_tasks.append(file_path)
                else:
                    phantom_tasks.append(file_path)

            return ToolResult(
                success=True,
                output={
                    "total_files_in_analysis": len(data),
                    "valid_files": len(valid_tasks),
                    "phantom_files": len(phantom_tasks),
                    "phantom_list": phantom_tasks[:10],  # First 10 only
                    "phantom_percentage": (
                        round((len(phantom_tasks) / len(data)) * 100, 2) if data else 0
                    ),
                    "recommendation": (
                        "Run fresh project scan" if phantom_tasks else "Task pool is clean"
                    ),
                },
                exit_code=0,
            )
        except Exception as e:
            logger.error(f"Error detecting phantoms: {e}")
            raise ToolExecutionError(str(e), tool_name="captain.detect_phantoms")


class MultiFuelDelivery(IToolAdapter):
    """Send fuel (gas) to multiple agents at once."""

    def get_spec(self) -> ToolSpec:
        """Get tool specification."""
        return ToolSpec(
            name="captain.multi_fuel",
            version="1.0.0",
            category="captain",
            summary="Send activation messages to multiple agents at once",
            required_params=["agent_ids", "message"],
            optional_params={"priority": "regular", "use_pyautogui": True},
        )

    def validate(self, params: dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate parameters."""
        spec = self.get_spec()
        return spec.validate_params(params)

    def execute(self, params: dict[str, Any], context: dict[str, Any] | None = None) -> ToolResult:
        """Execute multi-agent fuel delivery."""
        try:
            agent_ids = params["agent_ids"]
            message = params["message"]
            priority = params.get("priority", "regular")
            use_pyautogui = params.get("use_pyautogui", True)

            delivery_results = {}
            success_count = 0

            for agent_id in agent_ids:
                cmd = [
                    "python",
                    "-m",
                    "src.services.messaging_cli",
                    "--agent",
                    agent_id,
                    "--message",
                    message,
                    "--priority",
                    priority,
                ]

                if use_pyautogui:
                    cmd.append("--pyautogui")

                result = subprocess.run(cmd, capture_output=True, text=True, cwd=Path.cwd())

                delivery_results[agent_id] = {"success": result.returncode == 0}
                if result.returncode == 0:
                    success_count += 1

            return ToolResult(
                success=success_count > 0,
                output={
                    "agents_targeted": len(agent_ids),
                    "deliveries_successful": success_count,
                    "success_rate": (
                        round((success_count / len(agent_ids)) * 100, 2) if agent_ids else 0
                    ),
                    "delivery_results": delivery_results,
                },
                exit_code=0 if success_count == len(agent_ids) else 1,
            )
        except Exception as e:
            logger.error(f"Error delivering multi-agent fuel: {e}")
            raise ToolExecutionError(str(e), tool_name="captain.multi_fuel")


class MarkovROIRunner(IToolAdapter):
    """Run Markov ROI optimizer and return optimal assignments."""

    def get_spec(self) -> ToolSpec:
        """Get tool specification."""
        return ToolSpec(
            name="captain.markov_roi",
            version="1.0.0",
            category="captain",
            summary="Execute Markov ROI optimizer for optimal task assignments",
            required_params=[],
            optional_params={"agent_count": 8},
        )

    def validate(self, params: dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate parameters."""
        return (True, [])

    def execute(self, params: dict[str, Any], context: dict[str, Any] | None = None) -> ToolResult:
        """Execute Markov ROI optimization."""
        try:
            result = subprocess.run(
                ["python", "tools/markov_8agent_roi_optimizer.py"],
                capture_output=True,
                text=True,
                cwd=Path.cwd(),
            )

            markov_output = {"optimization_completed": result.returncode == 0}

            # Load results
            results_file = Path("agent_workspaces/Agent-4/8agent_roi_assignments.json")
            if results_file.exists():
                with open(results_file) as f:
                    assignments = json.load(f)
                    markov_output.update(
                        {
                            "total_agents": assignments.get("total_agents", 0),
                            "total_points": assignments.get("total_points", 0),
                            "avg_roi": assignments.get("avg_roi", 0),
                            "top_3_tasks": assignments.get("assignments", [])[:3],
                        }
                    )

            return ToolResult(
                success=result.returncode == 0, output=markov_output, exit_code=result.returncode
            )
        except Exception as e:
            logger.error(f"Error running Markov ROI: {e}")
            raise ToolExecutionError(str(e), tool_name="captain.markov_roi")


class SwarmStatusDashboard(IToolAdapter):
    """Generate comprehensive swarm status dashboard."""

    def get_spec(self) -> ToolSpec:
        return ToolSpec(
            name="captain.swarm_status",
            version="1.0.0",
            category="captain",
            summary="Generate swarm status overview",
            required_params=[],
            optional_params={},
        )

    def validate(self, params: dict[str, Any]) -> tuple[bool, list[str]]:
        return (True, [])

    def execute(self, params: dict[str, Any], context: dict[str, Any] | None = None) -> ToolResult:
        """Execute swarm dashboard generation."""
        try:
            dashboard = {"timestamp": datetime.now().isoformat(), "agents": {}, "active_count": 0}

            for agent_id in SWARM_AGENTS:
                workspace = Path(f"agent_workspaces/{agent_id}")
                if workspace.exists():
                    status_file = workspace / "status.json"
                    if status_file.exists():
                        status = json.loads(status_file.read_text())
                        dashboard["agents"][agent_id] = {
                            "status": status.get("status", "UNKNOWN"),
                            "mission": status.get("current_mission"),
                        }
                        if status.get("status") in ["ACTIVE", "EXECUTING"]:
                            dashboard["active_count"] += 1

            dashboard["swarm_health"] = "EXCELLENT" if dashboard["active_count"] >= 5 else "GOOD"
            return ToolResult(success=True, output=dashboard, exit_code=0)
        except Exception as e:
            raise ToolExecutionError(str(e), tool_name="captain.swarm_status")
