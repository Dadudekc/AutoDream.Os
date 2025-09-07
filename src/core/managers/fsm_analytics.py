#!/usr/bin/env python3
"""FSM analytics mixin."""

import logging
import time
from datetime import datetime
from typing import Any, Dict, List

from .fsm_utils import TaskPriority, TaskState

logger = logging.getLogger(__name__)


class FSMAnalyticsMixin:
    """Mixin providing analytics and reporting helpers for the FSM system."""

    def analyze_fsm_performance_patterns(self, time_range_hours: int = 24) -> Dict[str, Any]:
        """Analyze FSM performance patterns for optimization insights"""
        try:
            recent_time = time.time() - (time_range_hours * 3600)

            performance_analysis = {
                "total_tasks": len(self._tasks),
                "active_tasks": 0,
                "completed_tasks": 0,
                "failed_tasks": 0,
                "state_transition_patterns": {},
                "task_completion_times": {},
                "agent_performance": {},
                "optimization_opportunities": [],
            }

            for task in self._tasks.values():
                if task.state == TaskState.COMPLETED:
                    performance_analysis["completed_tasks"] += 1
                elif task.state == TaskState.FAILED:
                    performance_analysis["failed_tasks"] += 1
                elif task.state in [TaskState.IN_PROGRESS, TaskState.ONBOARDING]:
                    performance_analysis["active_tasks"] += 1

            recent_transitions = [
                t for t in self._state_transition_history if t["timestamp"] > recent_time
            ]
            if recent_transitions:
                transition_counts: Dict[str, int] = {}
                for transition in recent_transitions:
                    from_state = transition.get("from_state", "unknown")
                    to_state = transition.get("to_state", "unknown")
                    key = f"{from_state}->{to_state}"
                    transition_counts[key] = transition_counts.get(key, 0) + 1
                performance_analysis["state_transition_patterns"] = transition_counts

            agent_task_counts: Dict[str, Dict[str, int]] = {}
            for task in self._tasks.values():
                agent = task.assigned_agent
                if agent not in agent_task_counts:
                    agent_task_counts[agent] = {"total": 0, "completed": 0, "failed": 0}
                agent_task_counts[agent]["total"] += 1
                if task.state == TaskState.COMPLETED:
                    agent_task_counts[agent]["completed"] += 1
                elif task.state == TaskState.FAILED:
                    agent_task_counts[agent]["failed"] += 1
            performance_analysis["agent_performance"] = agent_task_counts

            if performance_analysis["failed_tasks"] > performance_analysis["completed_tasks"] * 0.2:
                performance_analysis["optimization_opportunities"].append(
                    "High failure rate - investigate task complexity or agent capabilities"
                )
            if performance_analysis["active_tasks"] > len(self._tasks) * 0.8:
                performance_analysis["optimization_opportunities"].append(
                    "High active task ratio - consider task prioritization or agent allocation"
                )

            logger.info("FSM performance analysis completed")
            return performance_analysis
        except Exception as e:  # pragma: no cover - log failure path
            logger.error(f"Failed to analyze FSM performance patterns: {e}")
            return {"error": str(e)}

    def predict_fsm_needs(self, time_horizon_minutes: int = 30) -> List[Dict[str, Any]]:
        """Predict potential FSM needs based on current patterns"""
        try:
            predictions: List[Dict[str, Any]] = []
            performance_analysis = self.analyze_fsm_performance_patterns(time_horizon_minutes / 60)

            active_tasks = performance_analysis.get("active_tasks", 0)
            total_tasks = performance_analysis.get("total_tasks", 1)
            if active_tasks / total_tasks > 0.8:
                predictions.append(
                    {
                        "issue_type": "task_overload",
                        "probability": 0.9,
                        "estimated_time_to_threshold": time_horizon_minutes * 0.3,
                        "severity": "high",
                        "recommended_action": "Prioritize tasks or add more agents",
                    }
                )

            if len(self._communication_events) > 100:
                predictions.append(
                    {
                        "issue_type": "communication_bottleneck",
                        "probability": 0.8,
                        "estimated_time_to_threshold": time_horizon_minutes * 0.5,
                        "severity": "medium",
                        "recommended_action": "Optimize communication patterns",
                    }
                )

            if len(self._state_transition_history) > 50:
                predictions.append(
                    {
                        "issue_type": "state_transition_issues",
                        "probability": 0.7,
                        "estimated_time_to_threshold": time_horizon_minutes * 0.8,
                        "severity": "medium",
                        "recommended_action": "Review state transition logic",
                    }
                )

            logger.info(
                "FSM needs prediction completed: %d predictions identified",
                len(predictions),
            )
            return predictions
        except Exception as e:  # pragma: no cover - log failure path
            logger.error(f"Failed to predict FSM needs: {e}")
            return []

    def generate_fsm_report(self, report_type: str = "comprehensive") -> Dict[str, Any]:
        """Generate comprehensive FSM system report"""
        try:
            report: Dict[str, Any] = {
                "report_id": f"fsm_system_report_{int(time.time())}",
                "generated_at": datetime.now().isoformat(),
                "report_type": report_type,
                "summary": {},
                "detailed_metrics": {},
                "task_summary": {},
                "recommendations": [],
            }

            total_tasks = len(self._tasks)
            active_tasks = len(
                [t for t in self._tasks.values() if t.state in [TaskState.IN_PROGRESS, TaskState.ONBOARDING]]
            )
            completed_tasks = len(
                [t for t in self._tasks.values() if t.state == TaskState.COMPLETED]
            )
            failed_tasks = len([t for t in self._tasks.values() if t.state == TaskState.FAILED])

            report["summary"] = {
                "total_tasks": total_tasks,
                "active_tasks": active_tasks,
                "completed_tasks": completed_tasks,
                "failed_tasks": failed_tasks,
                "success_rate": completed_tasks / total_tasks if total_tasks > 0 else 0,
                "system_status": self.status.value,
            }

            if self._tasks:
                priority_distribution: Dict[str, int] = {}
                state_distribution: Dict[str, int] = {}
                agent_distribution: Dict[str, int] = {}

                for task in self._tasks.values():
                    priority_distribution[task.priority.value] = (
                        priority_distribution.get(task.priority.value, 0) + 1
                    )
                    state_distribution[task.state.value] = (
                        state_distribution.get(task.state.value, 0) + 1
                    )
                    agent_distribution[task.assigned_agent] = (
                        agent_distribution.get(task.assigned_agent, 0) + 1
                    )

                report["detailed_metrics"] = {
                    "priority_distribution": priority_distribution,
                    "state_distribution": state_distribution,
                    "agent_distribution": agent_distribution,
                    "total_updates": len(self._task_updates),
                    "total_communication_events": len(self._communication_events),
                }

            if self._tasks:
                recent_tasks = sorted(
                    self._tasks.values(), key=lambda t: t.updated_at, reverse=True
                )[:10]
                report["task_summary"] = {
                    "recent_tasks": [
                        {
                            "id": t.id,
                            "title": t.title,
                            "state": t.state.value,
                            "agent": t.assigned_agent,
                        }
                        for t in recent_tasks
                    ],
                    "high_priority_tasks": [
                        t.id
                        for t in self._tasks.values()
                        if t.priority in [TaskPriority.HIGH, TaskPriority.CRITICAL]
                    ],
                    "blocked_tasks": [
                        t.id for t in self._tasks.values() if t.state == TaskState.BLOCKED
                    ],
                }

            performance_analysis = self.analyze_fsm_performance_patterns()
            for opportunity in performance_analysis.get("optimization_opportunities", []):
                report["recommendations"].append(opportunity)

            if total_tasks > 0:
                if active_tasks / total_tasks > 0.8:
                    report["recommendations"].append(
                        "High active task ratio - consider task prioritization"
                    )
                if failed_tasks / total_tasks > 0.2:
                    report["recommendations"].append(
                        "High failure rate - investigate task complexity"
                    )

            logger.info("FSM system report generated: %s", report["report_id"])
            return report
        except Exception as e:  # pragma: no cover - log failure path
            logger.error(f"Failed to generate FSM system report: {e}")
            return {"error": str(e)}
