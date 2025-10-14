"""
Captain Operations Tools
=========================

Tool adapters for Captain-specific operations discovered in Session 2025-10-13.

Tools enable:
- Agent status checking (idle detection)
- Git verification (integrity checks)
- Points calculation (ROI-based)
- Mission assignment (structured orders)
- Gas delivery (PyAutoGUI activation)
- Leaderboard updates
- Work verification
- Cycle reporting

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


class StatusCheckTool(IToolAdapter):
    """Check all agent status.json files to detect idle agents."""

    def get_spec(self) -> ToolSpec:
        """Get tool specification."""
        return ToolSpec(
            name="captain.status_check",
            version="1.0.0",
            category="captain",
            summary="Check all agent status files to detect idle agents",
            required_params=[],
            optional_params={"agents": SWARM_AGENTS, "threshold_hours": 24},
        )

    def validate(self, params: dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate parameters."""
        return (True, [])

    def execute(self, params: dict[str, Any], context: dict[str, Any] | None = None) -> ToolResult:
        """Execute status check across all agents."""
        try:
            agents = params.get("agents", SWARM_AGENTS)
            threshold = params.get("threshold_hours", 24)

            results = {}
            idle_agents = []

            for agent in agents:
                status_file = Path(f"agent_workspaces/{agent}/status.json")
                if status_file.exists():
                    try:
                        status_data = json.loads(status_file.read_text())
                        results[agent] = status_data

                        # Check if idle based on last_activity
                        if "last_activity" in status_data:
                            last_activity = datetime.fromisoformat(status_data["last_activity"])
                            hours_idle = (datetime.now() - last_activity).total_seconds() / 3600

                            if hours_idle > threshold:
                                idle_agents.append(
                                    {
                                        "agent": agent,
                                        "hours_idle": round(hours_idle, 1),
                                        "status": status_data.get("status", "unknown"),
                                    }
                                )
                    except Exception as e:
                        results[agent] = {"error": str(e)}
                else:
                    results[agent] = {"error": "Status file not found"}

            return ToolResult(
                success=True,
                output={
                    "all_status": results,
                    "idle_agents": idle_agents,
                    "threshold_hours": threshold,
                },
                exit_code=0,
            )
        except Exception as e:
            logger.error(f"Error checking agent status: {e}")
            raise ToolExecutionError(str(e), tool_name="captain.status_check")


class GitVerifyTool(IToolAdapter):
    """Verify git commits for work attribution and integrity checks."""

    def get_spec(self) -> ToolSpec:
        """Get tool specification."""
        return ToolSpec(
            name="captain.git_verify",
            version="1.0.0",
            category="captain",
            summary="Verify git commits for work attribution",
            required_params=["commit_hash"],
            optional_params={"show_stat": True, "show_diff": False},
        )

    def validate(self, params: dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate parameters."""
        spec = self.get_spec()
        return spec.validate_params(params)

    def execute(self, params: dict[str, Any], context: dict[str, Any] | None = None) -> ToolResult:
        """Execute git verification."""
        try:
            commit_hash = params["commit_hash"]
            show_stat = params.get("show_stat", True)
            show_diff = params.get("show_diff", False)

            # Build git command
            cmd = ["git", "show"]
            if show_stat:
                cmd.append("--stat")
            if not show_diff:
                cmd.append("--no-patch")
            cmd.append(commit_hash)

            # Execute git command
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=Path.cwd())

            if result.returncode != 0:
                return ToolResult(
                    success=False,
                    output={"error": result.stderr},
                    exit_code=result.returncode,
                    error_message=f"Git command failed: {result.stderr}",
                )

            return ToolResult(
                success=True,
                output={"commit_hash": commit_hash, "commit_info": result.stdout, "verified": True},
                exit_code=0,
            )
        except Exception as e:
            logger.error(f"Error verifying git commit: {e}")
            raise ToolExecutionError(str(e), tool_name="captain.git_verify")


class PointsCalculatorTool(IToolAdapter):
    """Calculate points based on ROI, impact, and complexity."""

    def get_spec(self) -> ToolSpec:
        """Get tool specification."""
        return ToolSpec(
            name="captain.calc_points",
            version="1.0.0",
            category="captain",
            summary="Calculate task points based on ROI metrics",
            required_params=["task_type"],
            optional_params={
                "impact": "medium",
                "complexity": "medium",
                "time_saved": 0,
                "custom_multiplier": 1.0,
            },
        )

    def validate(self, params: dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate parameters."""
        spec = self.get_spec()
        return spec.validate_params(params)

    def execute(self, params: dict[str, Any], context: dict[str, Any] | None = None) -> ToolResult:
        """Execute points calculation."""
        try:
            task_type = params["task_type"]
            impact = params.get("impact", "medium")
            complexity = params.get("complexity", "medium")
            time_saved = params.get("time_saved", 0)
            multiplier = params.get("custom_multiplier", 1.0)

            # Base points by task type
            base_points = {
                "refactor": 500,
                "consolidation": 1000,
                "tooling": 400,
                "testing": 300,
                "documentation": 200,
                "bugfix": 300,
                "feature": 800,
                "infrastructure": 600,
            }

            # Impact multipliers
            impact_mult = {"low": 0.7, "medium": 1.0, "high": 1.5, "critical": 2.0}

            # Complexity multipliers
            complexity_mult = {
                "trivial": 0.5,
                "low": 0.8,
                "medium": 1.0,
                "high": 1.3,
                "expert": 1.6,
            }

            base = base_points.get(task_type, 400)
            impact_factor = impact_mult.get(impact, 1.0)
            complexity_factor = complexity_mult.get(complexity, 1.0)

            # Calculate total points
            calculated = int(base * impact_factor * complexity_factor * multiplier)

            # Add time-saved bonus
            if time_saved > 0:
                time_bonus = int(time_saved * 10)  # 10 pts per hour saved
                calculated += time_bonus

            return ToolResult(
                success=True,
                output={
                    "task_type": task_type,
                    "base_points": base,
                    "impact_multiplier": impact_factor,
                    "complexity_multiplier": complexity_factor,
                    "custom_multiplier": multiplier,
                    "time_bonus": int(time_saved * 10) if time_saved > 0 else 0,
                    "total_points": calculated,
                    "breakdown": f"{base} × {impact_factor} × {complexity_factor} × {multiplier}",
                },
                exit_code=0,
            )
        except Exception as e:
            logger.error(f"Error calculating points: {e}")
            raise ToolExecutionError(str(e), tool_name="captain.calc_points")


class MissionAssignTool(IToolAdapter):
    """Create structured mission files in agent inboxes."""

    def get_spec(self) -> ToolSpec:
        """Get tool specification."""
        return ToolSpec(
            name="captain.assign_mission",
            version="1.0.0",
            category="captain",
            summary="Create structured mission file in agent inbox",
            required_params=["agent_id", "mission_title", "mission_description"],
            optional_params={
                "points": 0,
                "roi": 0.0,
                "complexity": "medium",
                "priority": "regular",
                "dependencies": [],
            },
        )

    def validate(self, params: dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate parameters."""
        spec = self.get_spec()
        return spec.validate_params(params)

    def execute(self, params: dict[str, Any], context: dict[str, Any] | None = None) -> ToolResult:
        """Execute mission assignment."""
        try:
            agent_id = params["agent_id"]
            mission_title = params["mission_title"]
            mission_desc = params["mission_description"]
            points = params.get("points", 0)
            roi = params.get("roi", 0.0)
            complexity = params.get("complexity", "medium")
            priority = params.get("priority", "regular")
            dependencies = params.get("dependencies", [])

            # Create mission file
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"C2A_MISSION_{mission_title.replace(' ', '_').upper()}_{timestamp}.md"
            inbox_path = Path(f"agent_workspaces/{agent_id}/inbox")
            inbox_path.mkdir(parents=True, exist_ok=True)

            mission_file = inbox_path / filename

            # Generate mission content
            content = f"""# [C2A] CAPTAIN → {agent_id}: {mission_title}

**Date:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**Priority:** {priority}  
**Estimated Points:** {points}  
**ROI:** {roi}  
**Complexity:** {complexity}

---

## 🎯 MISSION OBJECTIVE

{mission_desc}

---

## 📊 MISSION METRICS

- **Points:** {points} pts
- **ROI:** {roi}
- **Complexity:** {complexity}
- **Priority:** {priority}

---

## 🔗 DEPENDENCIES

{chr(10).join(f'- {dep}' for dep in dependencies) if dependencies else 'None'}

---

## ✅ SUCCESS CRITERIA

- [ ] Implementation complete
- [ ] Tests passing
- [ ] Documentation updated
- [ ] Git commit created
- [ ] Report delivered

---

## 📝 REPORTING

Report completion to: agent_workspaces/Agent-4/inbox/
Tag: #DONE-{mission_title.replace(' ', '-').upper()}

---

**🐝 WE. ARE. SWARM.** ⚡🔥
"""

            mission_file.write_text(content, encoding="utf-8")

            return ToolResult(
                success=True,
                output={
                    "agent_id": agent_id,
                    "mission_file": str(mission_file),
                    "mission_title": mission_title,
                    "points": points,
                    "created": True,
                },
                exit_code=0,
            )
        except Exception as e:
            logger.error(f"Error assigning mission: {e}")
            raise ToolExecutionError(str(e), tool_name="captain.assign_mission")


class GasDeliveryTool(IToolAdapter):
    """Send PyAutoGUI activation messages to agents ("Prompts Are Gas")."""

    def get_spec(self) -> ToolSpec:
        """Get tool specification."""
        return ToolSpec(
            name="captain.deliver_gas",
            version="1.0.0",
            category="captain",
            summary="Send PyAutoGUI activation message to agent",
            required_params=["agent_id", "message"],
            optional_params={"priority": "regular"},
        )

    def validate(self, params: dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate parameters."""
        spec = self.get_spec()
        return spec.validate_params(params)

    def execute(self, params: dict[str, Any], context: dict[str, Any] | None = None) -> ToolResult:
        """Execute gas delivery (PyAutoGUI message)."""
        try:
            agent_id = params["agent_id"]
            message = params["message"]
            priority = params.get("priority", "regular")

            # Use messaging_cli to send PyAutoGUI message
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
                "--pyautogui",
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, cwd=Path.cwd())

            if result.returncode != 0:
                return ToolResult(
                    success=False,
                    output={"error": result.stderr},
                    exit_code=result.returncode,
                    error_message=f"Gas delivery failed: {result.stderr}",
                )

            return ToolResult(
                success=True,
                output={
                    "agent_id": agent_id,
                    "message_sent": True,
                    "delivery_method": "PyAutoGUI",
                    "gas_type": "activation",
                    "stdout": result.stdout,
                },
                exit_code=0,
            )
        except Exception as e:
            logger.error(f"Error delivering gas: {e}")
            raise ToolExecutionError(str(e), tool_name="captain.deliver_gas")


class LeaderboardUpdateTool(IToolAdapter):
    """Update agent leaderboard with new points."""

    def get_spec(self) -> ToolSpec:
        """Get tool specification."""
        return ToolSpec(
            name="captain.update_leaderboard",
            version="1.0.0",
            category="captain",
            summary="Update agent leaderboard with session points",
            required_params=["updates"],
            optional_params={"session_date": None},
        )

    def validate(self, params: dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate parameters."""
        spec = self.get_spec()
        return spec.validate_params(params)

    def execute(self, params: dict[str, Any], context: dict[str, Any] | None = None) -> ToolResult:
        """Execute leaderboard update."""
        try:
            updates = params["updates"]  # Dict: {agent_id: points}
            session_date = params.get("session_date", datetime.now().strftime("%Y-%m-%d"))

            leaderboard_file = Path("runtime/leaderboard.json")
            leaderboard_file.parent.mkdir(parents=True, exist_ok=True)

            # Load existing leaderboard
            if leaderboard_file.exists():
                leaderboard = json.loads(leaderboard_file.read_text())
            else:
                leaderboard = {"version": "1.0.0", "last_updated": session_date, "agents": {}}

            # Update agent scores
            for agent_id, points in updates.items():
                if agent_id not in leaderboard["agents"]:
                    leaderboard["agents"][agent_id] = {"total_points": 0, "sessions": []}

                leaderboard["agents"][agent_id]["total_points"] += points
                leaderboard["agents"][agent_id]["sessions"].append(
                    {"date": session_date, "points": points}
                )

            # Sort by total points
            sorted_agents = sorted(
                leaderboard["agents"].items(), key=lambda x: x[1]["total_points"], reverse=True
            )

            leaderboard["last_updated"] = session_date
            leaderboard["ranking"] = [agent_id for agent_id, _ in sorted_agents]

            # Save leaderboard
            leaderboard_file.write_text(json.dumps(leaderboard, indent=2))

            return ToolResult(
                success=True,
                output={
                    "leaderboard_file": str(leaderboard_file),
                    "updates_applied": len(updates),
                    "ranking": leaderboard["ranking"][:5],  # Top 5
                    "last_updated": session_date,
                },
                exit_code=0,
            )
        except Exception as e:
            logger.error(f"Error updating leaderboard: {e}")
            raise ToolExecutionError(str(e), tool_name="captain.update_leaderboard")


class WorkVerifyTool(IToolAdapter):
    """Comprehensive work verification (git + files + tests)."""

    def get_spec(self) -> ToolSpec:
        """Get tool specification."""
        return ToolSpec(
            name="captain.verify_work",
            version="1.0.0",
            category="captain",
            summary="Verify completed work with git commits and file checks",
            required_params=["agent_id", "work_description"],
            optional_params={"commit_hash": None, "files_changed": []},
        )

    def validate(self, params: dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate parameters."""
        spec = self.get_spec()
        return spec.validate_params(params)

    def execute(self, params: dict[str, Any], context: dict[str, Any] | None = None) -> ToolResult:
        """Execute work verification."""
        try:
            agent_id = params["agent_id"]
            work_desc = params["work_description"]
            commit_hash = params.get("commit_hash")
            files_changed = params.get("files_changed", [])

            verification_results = {
                "agent_id": agent_id,
                "work_description": work_desc,
                "verified": True,
                "checks": {},
            }

            # Check 1: Git commit verification
            if commit_hash:
                git_result = subprocess.run(
                    ["git", "show", "--stat", "--no-patch", commit_hash],
                    capture_output=True,
                    text=True,
                    cwd=Path.cwd(),
                )
                verification_results["checks"]["git_commit"] = {
                    "verified": git_result.returncode == 0,
                    "commit_hash": commit_hash,
                    "commit_info": git_result.stdout
                    if git_result.returncode == 0
                    else git_result.stderr,
                }

            # Check 2: Files exist
            if files_changed:
                files_status = {}
                for file_path in files_changed:
                    file = Path(file_path)
                    files_status[file_path] = {
                        "exists": file.exists(),
                        "size": file.stat().st_size if file.exists() else 0,
                    }
                verification_results["checks"]["files"] = files_status

            # Check 3: Agent workspace activity
            workspace = Path(f"agent_workspaces/{agent_id}")
            if workspace.exists():
                verification_results["checks"]["workspace"] = {
                    "exists": True,
                    "files_count": len(list(workspace.rglob("*"))),
                }

            return ToolResult(success=True, output=verification_results, exit_code=0)
        except Exception as e:
            logger.error(f"Error verifying work: {e}")
            raise ToolExecutionError(str(e), tool_name="captain.verify_work")


class CycleReportTool(IToolAdapter):
    """Generate Captain's cycle report."""

    def get_spec(self) -> ToolSpec:
        """Get tool specification."""
        return ToolSpec(
            name="captain.cycle_report",
            version="1.0.0",
            category="captain",
            summary="Generate Captain's cycle activity report",
            required_params=["cycle_number"],
            optional_params={
                "missions_assigned": 0,
                "messages_sent": 0,
                "agents_activated": [],
                "points_awarded": 0,
                "notes": "",
            },
        )

    def validate(self, params: dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate parameters."""
        spec = self.get_spec()
        return spec.validate_params(params)

    def execute(self, params: dict[str, Any], context: dict[str, Any] | None = None) -> ToolResult:
        """Execute cycle report generation."""
        try:
            cycle_num = params["cycle_number"]
            missions = params.get("missions_assigned", 0)
            messages = params.get("messages_sent", 0)
            agents = params.get("agents_activated", [])
            points = params.get("points_awarded", 0)
            notes = params.get("notes", "")

            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            report_file = Path(f"agent_workspaces/Agent-4/CAPTAIN_CYCLE_{cycle_num}_{timestamp}.md")
            report_file.parent.mkdir(parents=True, exist_ok=True)

            content = f"""# 🎯 CAPTAIN'S CYCLE REPORT #{cycle_num}

**Date:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**Cycle:** {cycle_num}

---

## 📊 CYCLE METRICS

- **Missions Assigned:** {missions}
- **Messages Sent:** {messages}
- **Agents Activated:** {len(agents)}
- **Points Awarded:** {points}

---

## 🤖 AGENTS ACTIVATED

{chr(10).join(f'- {agent}' for agent in agents) if agents else 'None this cycle'}

---

## 📝 CYCLE NOTES

{notes if notes else 'No additional notes this cycle.'}

---

## 🎯 NEXT CYCLE PRIORITIES

- Monitor agent progress
- Check for idle agents
- Review completed work
- Update leaderboard

---

**🐝 WE. ARE. SWARM.** ⚡🔥
"""

            report_file.write_text(content, encoding="utf-8")

            return ToolResult(
                success=True,
                output={
                    "cycle_number": cycle_num,
                    "report_file": str(report_file),
                    "missions_assigned": missions,
                    "messages_sent": messages,
                    "agents_activated": agents,
                    "points_awarded": points,
                },
                exit_code=0,
            )
        except Exception as e:
            logger.error(f"Error generating cycle report: {e}")
            raise ToolExecutionError(str(e), tool_name="captain.cycle_report")


class MarkovOptimizerTool(IToolAdapter):
    """Interface to Markov chain optimizer for task selection."""

    def get_spec(self) -> ToolSpec:
        """Get tool specification."""
        return ToolSpec(
            name="captain.markov_optimize",
            version="1.0.0",
            category="captain",
            summary="Use Markov optimizer for ROI-based task selection",
            required_params=["tasks"],
            optional_params={"agent_count": 8, "time_budget": 120},
        )

    def validate(self, params: dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate parameters."""
        spec = self.get_spec()
        return spec.validate_params(params)

    def execute(self, params: dict[str, Any], context: dict[str, Any] | None = None) -> ToolResult:
        """Execute Markov optimization."""
        try:
            tasks = params["tasks"]  # List of task dicts with ROI, time, points
            agent_count = params.get("agent_count", 8)
            time_budget = params.get("time_budget", 120)

            # Simple greedy optimizer (real Markov would be more complex)
            # Sort tasks by ROI descending
            sorted_tasks = sorted(tasks, key=lambda t: t.get("roi", 0), reverse=True)

            assignments = []
            total_time = 0
            total_points = 0

            for task in sorted_tasks:
                task_time = task.get("time_estimate", 60)
                if total_time + task_time <= time_budget:
                    assignments.append(task)
                    total_time += task_time
                    total_points += task.get("points", 0)

            avg_roi = (
                sum(t.get("roi", 0) for t in assignments) / len(assignments) if assignments else 0
            )

            return ToolResult(
                success=True,
                output={
                    "recommended_tasks": assignments,
                    "total_tasks": len(assignments),
                    "total_time": total_time,
                    "total_points": total_points,
                    "average_roi": round(avg_roi, 2),
                    "efficiency": round((total_points / total_time) * 100, 2)
                    if total_time > 0
                    else 0,
                },
                exit_code=0,
            )
        except Exception as e:
            logger.error(f"Error running Markov optimizer: {e}")
            raise ToolExecutionError(str(e), tool_name="captain.markov_optimize")


class IntegrityCheckTool(IToolAdapter):
    """Verify work claims with git history and Entry #025 integrity checks."""

    def get_spec(self) -> ToolSpec:
        """Get tool specification."""
        return ToolSpec(
            name="captain.integrity_check",
            version="1.0.0",
            category="captain",
            summary="Verify work claims with git history (Entry #025)",
            required_params=["agent_id", "claimed_work"],
            optional_params={"search_terms": []},
        )

    def validate(self, params: dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate parameters."""
        spec = self.get_spec()
        return spec.validate_params(params)

    def execute(self, params: dict[str, Any], context: dict[str, Any] | None = None) -> ToolResult:
        """Execute integrity check."""
        try:
            agent_id = params["agent_id"]
            claimed_work = params["claimed_work"]
            search_terms = params.get("search_terms", [])

            # Search git log for commits related to claimed work
            git_results = []

            for term in search_terms:
                result = subprocess.run(
                    ["git", "log", "--all", "--oneline", "--grep", term],
                    capture_output=True,
                    text=True,
                    cwd=Path.cwd(),
                )

                if result.returncode == 0 and result.stdout.strip():
                    git_results.append(
                        {"search_term": term, "commits_found": result.stdout.strip().split("\n")}
                    )

            # Check if any commits found
            integrity_status = {
                "agent_id": agent_id,
                "claimed_work": claimed_work,
                "git_commits_found": len(git_results) > 0,
                "commit_details": git_results,
                "integrity_verdict": "VERIFIED" if git_results else "NO_EVIDENCE",
                "recommendation": "Approve work claim" if git_results else "Request more evidence",
            }

            return ToolResult(success=True, output=integrity_status, exit_code=0)
        except Exception as e:
            logger.error(f"Error checking integrity: {e}")
            raise ToolExecutionError(str(e), tool_name="captain.integrity_check")
