#!/usr/bin/env python3
"""
Swarm Mission Control - The Masterpiece Tool
============================================

The ONE tool agents can't live without.

Like the messaging system revolutionized coordination, Swarm Mission Control
revolutionizes task selection and execution by providing:

- WHAT should I work on? (Optimal next task)
- WHY this task? (ROI, impact, urgency)
- WITH WHAT CONTEXT? (Full context package)
- WHO else is working? (Avoid conflicts)
- WHAT'S been done? (Don't duplicate)
- WHAT dependencies? (Coordination needs)

This tool answers the fundamental question every agent asks:
"What should I do next and how do I do it effectively?"

Author: Agent-3 (Infrastructure & DevOps) - Masterpiece Tool
License: MIT
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

from ..adapters.base_adapter import IToolAdapter

logger = logging.getLogger(__name__)


class SwarmMissionControl(IToolAdapter):
    """
    Swarm Mission Control - The masterpiece tool for intelligent task selection.

    Provides each agent with:
    1. Optimal next task recommendation
    2. Full context package for execution
    3. Swarm state awareness (who's doing what)
    4. Conflict detection (avoid duplicate work)
    5. Dependency mapping (coordination needs)
    6. Success patterns (learn from past work)
    """

    def get_name(self) -> str:
        return "mission_control"

    def get_description(self) -> str:
        return "Get optimal next mission with full context (agents can't live without this)"

    def get_spec(self) -> dict[str, Any]:
        """Get tool specification."""
        return {
            "name": self.get_name(),
            "description": self.get_description(),
            "parameters": {
                "agent": {"type": "string", "required": True, "description": "Agent ID"}
            },
        }

    def validate(self, **kwargs) -> tuple[bool, str | None]:
        """Validate parameters."""
        if not kwargs.get("agent"):
            return False, "Agent ID required"
        return True, None

    def execute(self, **kwargs) -> dict[str, Any]:
        """Execute mission control analysis."""
        try:
            agent_id = kwargs.get("agent", "Agent-1")

            # PHASE 1: READ ENTIRE SWARM STATE
            swarm_state = self._read_swarm_state()

            # PHASE 2: READ AGENT'S CONTEXT
            agent_context = self._read_agent_context(agent_id, swarm_state)

            # PHASE 3: ANALYZE AVAILABLE WORK
            available_work = self._analyze_available_work(swarm_state)

            # PHASE 4: CALCULATE OPTIMAL TASK
            optimal_task = self._calculate_optimal_task(
                agent_id, agent_context, available_work, swarm_state
            )

            # PHASE 5: BUILD CONTEXT PACKAGE
            context_package = self._build_context_package(optimal_task, agent_context, swarm_state)

            # PHASE 6: RETURN MISSION BRIEF
            return {
                "success": True,
                "agent": agent_id,
                "timestamp": datetime.now().isoformat(),
                # THE ANSWER TO "WHAT SHOULD I DO?"
                "recommended_task": optimal_task,
                # THE ANSWER TO "WITH WHAT CONTEXT?"
                "context_package": context_package,
                # THE ANSWER TO "WHO'S DOING WHAT?"
                "swarm_state": swarm_state["summary"],
                # THE ANSWER TO "WHAT'S MY STATUS?"
                "agent_context": agent_context,
                # EXECUTION READY
                "ready_to_execute": optimal_task is not None,
                "mission_brief": self._format_mission_brief(optimal_task, context_package),
            }

        except Exception as e:
            logger.error(f"Mission control failed: {e}")
            return {"success": False, "error": str(e)}

    def _read_swarm_state(self) -> dict[str, Any]:
        """Read complete swarm state from all agents."""
        swarm_state = {
            "agents": {},
            "active_missions": [],
            "completed_today": [],
            "total_points": 0,
            "summary": {},
        }

        try:
            # Read all agent status files
            workspace = Path("agent_workspaces")
            for i in range(1, 9):
                agent_id = f"Agent-{i}"
                status_file = workspace / agent_id / "status.json"

                if status_file.exists():
                    try:
                        with open(status_file) as f:
                            status = json.load(f)
                            swarm_state["agents"][agent_id] = status

                            # Track active missions
                            mission = status.get("current_mission", "")
                            if mission and "COMPLETE" not in mission.upper():
                                swarm_state["active_missions"].append(
                                    {"agent": agent_id, "mission": mission}
                                )

                            # Sum points
                            points = status.get("points_earned", 0)
                            if isinstance(points, (int, float)):
                                swarm_state["total_points"] += points

                    except:
                        pass

            swarm_state["summary"] = {
                "total_agents": len(swarm_state["agents"]),
                "active_count": len(swarm_state["active_missions"]),
                "total_points": swarm_state["total_points"],
            }

        except Exception as e:
            logger.error(f"Error reading swarm state: {e}")

        return swarm_state

    def _read_agent_context(self, agent_id: str, swarm_state: dict) -> dict[str, Any]:
        """Read agent's specific context."""
        context = {
            "agent_id": agent_id,
            "status": {},
            "inbox_count": 0,
            "inbox_messages": [],
            "recent_completions": [],
            "specialty": self._get_agent_specialty(agent_id),
        }

        try:
            # Read agent status
            if agent_id in swarm_state["agents"]:
                context["status"] = swarm_state["agents"][agent_id]

            # Read inbox
            inbox_path = Path(f"agent_workspaces/{agent_id}/inbox")
            if inbox_path.exists():
                inbox_files = list(inbox_path.glob("*.md"))
                context["inbox_count"] = len(inbox_files)

                # Read priority messages
                priority_messages = []
                for msg_file in sorted(inbox_files, key=lambda x: x.stat().st_mtime, reverse=True)[
                    :5
                ]:
                    try:
                        content = open(msg_file).read()
                        priority_messages.append(
                            {
                                "file": msg_file.name,
                                "preview": content[:200],
                                "modified": datetime.fromtimestamp(
                                    msg_file.stat().st_mtime
                                ).isoformat(),
                            }
                        )
                    except:
                        pass

                context["inbox_messages"] = priority_messages

        except Exception as e:
            logger.error(f"Error reading agent context: {e}")

        return context

    def _analyze_available_work(self, swarm_state: dict) -> list[dict]:
        """Analyze what work is available."""
        available = []

        try:
            # Check project analysis for violations
            if Path("project_analysis.json").exists():
                with open("project_analysis.json") as f:
                    analysis = json.load(f)
                    # Look for files that need work (this is simplified)
                    # Real implementation would parse violations
                    available.append(
                        {"type": "v2_compliance", "source": "project_analysis", "count": "multiple"}
                    )

            # Check captain's tracking for unassigned work
            captain_docs = Path("agent_workspaces/Agent-4")
            if captain_docs.exists():
                # Look for execution orders or task lists
                for doc in captain_docs.glob("*EXECUTION*.md"):
                    available.append(
                        {"type": "captain_order", "source": str(doc), "priority": "HIGH"}
                    )

        except Exception as e:
            logger.error(f"Error analyzing available work: {e}")

        return available

    def _calculate_optimal_task(
        self, agent_id: str, agent_context: dict, available_work: list, swarm_state: dict
    ) -> dict | None:
        """Calculate optimal next task for agent."""

        # Check inbox first (highest priority)
        if agent_context["inbox_count"] > 0:
            inbox_messages = agent_context["inbox_messages"]
            if inbox_messages:
                latest = inbox_messages[0]
                return {
                    "type": "inbox_order",
                    "priority": "URGENT",
                    "source": latest["file"],
                    "description": "Check inbox - Captain's orders waiting",
                    "roi": 999,  # Highest priority
                    "reasoning": f"{agent_context['inbox_count']} messages in inbox",
                }

        # Check for specialty-aligned work
        specialty = agent_context.get("specialty", "")
        if "Infrastructure" in specialty and available_work:
            for work in available_work:
                if "orchestrat" in str(work.get("source", "")).lower():
                    return {
                        "type": "specialty_match",
                        "priority": "HIGH",
                        "description": "Infrastructure work matches your specialty",
                        "source": work.get("source"),
                        "roi": 800,
                        "reasoning": "Aligns with Infrastructure & DevOps expertise",
                    }

        # No specific task found
        return {
            "type": "scan_for_opportunities",
            "priority": "MEDIUM",
            "description": "Scan project for proactive opportunities",
            "roi": 500,
            "reasoning": "No urgent tasks - proactive mode",
        }

    def _build_context_package(
        self, task: dict | None, agent_context: dict, swarm_state: dict
    ) -> dict[str, Any]:
        """Build complete context package for task execution."""
        if not task:
            return {}

        package = {
            "task_summary": task.get("description", "No task"),
            "priority": task.get("priority", "MEDIUM"),
            "estimated_roi": task.get("roi", 0),
            # Swarm coordination context
            "other_agents_working": [
                {"agent": m["agent"], "mission": m["mission"]}
                for m in swarm_state["active_missions"]
            ],
            # Agent status
            "your_status": agent_context.get("status", {}),
            # Related files
            "check_these_files": [],
            # Coordination needs
            "coordinate_with": [],
            # Success patterns
            "similar_past_work": [],
        }

        # Add task-specific context
        if task.get("source"):
            package["reference_file"] = task["source"]
            package["check_these_files"].append(task["source"])

        return package

    def _format_mission_brief(self, task: dict | None, context: dict) -> str:
        """Format human-readable mission brief."""
        if not task:
            return "No mission identified - Agent appears to be resting"

        brief = f"""
🎯 MISSION BRIEF FOR EXECUTION
================================

RECOMMENDED TASK: {task.get('description', 'Unknown')}
PRIORITY: {task.get('priority', 'MEDIUM')}
ROI: {task.get('roi', 0)}
TYPE: {task.get('type', 'Unknown')}

REASONING: {task.get('reasoning', 'Optimal task for your specialty')}

CONTEXT PROVIDED:
- Swarm state: {len(context.get('other_agents_working', []))} agents active
- Files to check: {len(context.get('check_these_files', []))}
- Coordination needed: {len(context.get('coordinate_with', []))}

READY TO EXECUTE: Yes
================================
"""
        return brief.strip()

    def _get_agent_specialty(self, agent_id: str) -> str:
        """Get agent specialty."""
        specialties = {
            "Agent-1": "Integration & Core Systems",
            "Agent-2": "Architecture & Design",
            "Agent-3": "Infrastructure & DevOps",
            "Agent-4": "Quality Assurance (Captain)",
            "Agent-5": "Business Intelligence",
            "Agent-6": "Coordination & Communication",
            "Agent-7": "Web Development",
            "Agent-8": "Operations & Support",
        }
        return specialties.get(agent_id, "General")


class SwarmConflictDetector(IToolAdapter):
    """Detect if proposed work conflicts with active missions."""

    def get_name(self) -> str:
        return "conflict_detector"

    def get_description(self) -> str:
        return "Detect conflicts before starting work"

    def get_spec(self) -> dict[str, Any]:
        return {
            "name": self.get_name(),
            "description": self.get_description(),
            "parameters": {
                "agent": {"type": "string", "required": True},
                "file": {"type": "string", "required": False},
            },
        }

    def validate(self, **kwargs) -> tuple[bool, str | None]:
        if not kwargs.get("agent"):
            return False, "Agent ID required"
        return True, None

    def execute(self, **kwargs) -> dict[str, Any]:
        """Detect conflicts."""
        try:
            proposed_file = kwargs.get("file")
            agent_id = kwargs.get("agent")

            # Read all active missions
            conflicts = []
            workspace = Path("agent_workspaces")

            for i in range(1, 9):
                other_agent = f"Agent-{i}"
                if other_agent == agent_id:
                    continue

                status_file = workspace / other_agent / "status.json"
                if status_file.exists():
                    try:
                        status = json.load(open(status_file))
                        mission = status.get("current_mission", "")

                        # Check if proposed file mentioned in their mission
                        if proposed_file and proposed_file in mission:
                            conflicts.append(
                                {
                                    "agent": other_agent,
                                    "mission": mission,
                                    "conflict_type": "file_overlap",
                                }
                            )
                    except:
                        pass

            return {
                "success": True,
                "has_conflicts": len(conflicts) > 0,
                "conflicts": conflicts,
                "safe_to_proceed": len(conflicts) == 0,
                "recommendation": (
                    "Coordinate with agents listed" if conflicts else "Clear to proceed"
                ),
            }

        except Exception as e:
            return {"success": False, "error": str(e)}


class ContextPackageBuilder(IToolAdapter):
    """Build complete context package for any task."""

    def get_name(self) -> str:
        return "context_builder"

    def get_description(self) -> str:
        return "Build complete context package for task execution"

    def get_spec(self) -> dict[str, Any]:
        return {
            "name": self.get_name(),
            "description": self.get_description(),
            "parameters": {
                "agent": {"type": "string", "required": True},
                "task": {"type": "string", "required": True},
            },
        }

    def validate(self, **kwargs) -> tuple[bool, str | None]:
        if not kwargs.get("agent"):
            return False, "Agent ID required"
        if not kwargs.get("task"):
            return False, "Task description required"
        return True, None

    def execute(self, **kwargs) -> dict[str, Any]:
        """Build context package."""
        try:
            task_description = kwargs.get("task", "")
            agent_id = kwargs.get("agent", "Agent-1")

            package = {
                "task": task_description,
                "agent": agent_id,
                "timestamp": datetime.now().isoformat(),
                "context": {},
            }

            # 1. Related files
            package["context"]["files_to_review"] = self._find_related_files(task_description)

            # 2. Similar past work
            package["context"]["similar_work"] = self._find_similar_work(task_description, agent_id)

            # 3. Current violations
            package["context"]["current_violations"] = self._find_current_violations()

            # 4. Dependencies
            package["context"]["dependencies"] = self._find_dependencies(task_description)

            # 5. Coordination needs
            package["context"]["coordinate_with"] = self._find_coordination_needs(task_description)

            # 6. Success patterns
            package["context"]["success_patterns"] = self._find_success_patterns(task_description)

            # 7. Execution checklist
            package["execution_checklist"] = self._generate_checklist(task_description)

            return {
                "success": True,
                "package": package,
                "ready_to_execute": True,
                "context_completeness": self._calculate_completeness(package),
            }

        except Exception as e:
            return {"success": False, "error": str(e)}

    def _find_related_files(self, task: str) -> list[str]:
        """Find files related to task."""
        related = []
        keywords = task.lower().split()

        try:
            for keyword in keywords:
                if len(keyword) > 4:  # Meaningful keywords
                    files = list(Path("src").rglob(f"*{keyword}*.py"))
                    related.extend([str(f) for f in files[:5]])
        except:
            pass

        return list(set(related))[:10]  # Top 10 unique

    def _find_similar_work(self, task: str, agent_id: str) -> list[dict]:
        """Find similar past work."""
        similar = []

        try:
            # Check devlogs for similar work
            devlogs = Path("devlogs")
            if devlogs.exists():
                keywords = [w for w in task.lower().split() if len(w) > 4]
                for log in devlogs.glob("*.md"):
                    try:
                        content = open(log).read().lower()
                        if any(k in content for k in keywords):
                            similar.append({"devlog": log.name, "relevance": "keyword_match"})
                    except:
                        pass
        except:
            pass

        return similar[:5]  # Top 5

    def _find_current_violations(self) -> list[dict]:
        """Find current V2 violations."""
        violations = []

        try:
            # Quick scan for large files
            for py_file in Path("src").rglob("*.py"):
                try:
                    lines = len(open(py_file).readlines())
                    if lines > 400:
                        violations.append(
                            {"file": str(py_file), "lines": lines, "severity": "CRITICAL"}
                        )
                    elif lines > 350:
                        violations.append(
                            {"file": str(py_file), "lines": lines, "severity": "HIGH"}
                        )
                except:
                    pass

                # Limit to first 10 found
                if len(violations) >= 10:
                    break
        except:
            pass

        return violations

    def _find_dependencies(self, task: str) -> list[str]:
        """Find dependencies for task."""
        # Simplified - real implementation would analyze imports
        return []

    def _find_coordination_needs(self, task: str) -> list[str]:
        """Find which agents to coordinate with."""
        # Check if task involves files other agents are working on
        return []

    def _find_success_patterns(self, task: str) -> list[dict]:
        """Find patterns from successful similar tasks."""
        patterns = []

        try:
            # Look for "COMPLETE" devlogs with keywords
            devlogs = Path("devlogs")
            if devlogs.exists():
                keywords = [w for w in task.lower().split() if len(w) > 4]
                for log in devlogs.glob("*complete*.md"):
                    try:
                        content = open(log).read()
                        if any(k in content.lower() for k in keywords):
                            patterns.append(
                                {
                                    "pattern_source": log.name,
                                    "success_indicator": "completion_devlog",
                                }
                            )
                    except:
                        pass
        except:
            pass

        return patterns[:3]  # Top 3

    def _generate_checklist(self, task: str) -> list[str]:
        """Generate execution checklist."""
        return [
            "☐ Read all related files",
            "☐ Check for conflicts with other agents",
            "☐ Review similar past work",
            "☐ Plan modular structure",
            "☐ Execute with V2 compliance",
            "☐ Test thoroughly (zero errors)",
            "☐ Create documentation",
            "☐ Report completion to Captain",
        ]

    def _calculate_completeness(self, package: dict) -> float:
        """Calculate context completeness percentage."""
        total_sections = 7
        filled_sections = sum(
            [
                1 if package["context"].get("files_to_review") else 0,
                1 if package["context"].get("similar_work") else 0,
                1 if package["context"].get("current_violations") else 0,
                1 if package["context"].get("dependencies") else 0,
                1 if package["context"].get("coordinate_with") else 0,
                1 if package["context"].get("success_patterns") else 0,
                1 if package.get("execution_checklist") else 0,
            ]
        )

        return (filled_sections / total_sections) * 100


__all__ = ["SwarmMissionControl", "SwarmConflictDetector", "ContextPackageBuilder"]
