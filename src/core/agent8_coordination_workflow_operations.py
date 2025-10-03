#!/usr/bin/env python3
"""
Agent-8 Coordination Workflow Operations
=======================================
Operations and utilities for Agent-8 coordination workflow
V2 Compliant: ≤400 lines, focused operations
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
import sys

sys.path.insert(0, str(project_root))

from src.core.agent8_coordination_workflow_core import (
    Agent8CoordinationWorkflowCore,
    CoordinationStatus,
    CoordinationTask,
    TaskPriority,
)


class Agent8CoordinationWorkflowOperations:
    """Operations and utilities for coordination workflow management"""

    def __init__(self, workflow: Agent8CoordinationWorkflowCore = None):
        self.workflow = workflow or Agent8CoordinationWorkflowCore()

    def manage_operations(self, action: str, **kwargs) -> Any:
        """Consolidated operations management"""
        if action == "bulk_create_tasks":
            return self.bulk_create_tasks(kwargs["tasks_data"], kwargs.get("auto_assign", False))
        elif action == "export_workflow":
            return self.export_workflow(kwargs["output_file"])
        elif action == "import_workflow":
            return self.import_workflow(kwargs["input_file"])
        elif action == "validate_workflow":
            return self.validate_workflow()
        elif action == "cleanup_completed":
            return self.cleanup_completed_tasks(kwargs.get("days", 30))
        elif action == "backup_workflow":
            return self.backup_workflow(kwargs["backup_dir"])
        elif action == "restore_workflow":
            return self.restore_workflow(kwargs["backup_file"])
        elif action == "analyze_performance":
            return self.analyze_workflow_performance(kwargs.get("days", 30))
        elif action == "optimize_workflow":
            return self.optimize_workflow()
        elif action == "monitor_tasks":
            return self.monitor_task_progress()
        return None

    def bulk_create_tasks(
        self, tasks_data: list[dict[str, Any]], auto_assign: bool = False
    ) -> dict[str, Any]:
        """Bulk create tasks from data"""
        results = {"success": True, "created": 0, "failed": 0, "errors": [], "task_ids": []}

        for task_data in tasks_data:
            try:
                # Validate required fields
                required_fields = ["agent_id", "description"]
                if not all(field in task_data for field in required_fields):
                    results["failed"] += 1
                    results["errors"].append(f"Missing required fields: {required_fields}")
                    continue

                # Create task
                task_id = self.workflow.manage_workflow_operations(
                    "create_task",
                    agent_id=task_data["agent_id"],
                    description=task_data["description"],
                    priority=TaskPriority(task_data.get("priority", "medium")),
                    dependencies=task_data.get("dependencies", []),
                    metadata=task_data.get("metadata", {}),
                )

                results["created"] += 1
                results["task_ids"].append(task_id)

            except Exception as e:
                results["failed"] += 1
                results["errors"].append(f"Error creating task: {e}")

        # Auto-assign if requested
        if auto_assign and results["created"] > 0:
            assigned = self.workflow.manage_workflow_operations("auto_assign")
            results["auto_assigned"] = assigned

        return results

    def export_workflow(self, output_file: str) -> bool:
        """Export workflow state to file"""
        try:
            status = self.workflow.manage_workflow_operations("get_status")
            performance = self.workflow.manage_workflow_operations("get_performance")

            export_data = {
                "export_timestamp": datetime.now().isoformat(),
                "workflow_status": status,
                "agent_performance": performance,
                "tasks": {
                    task_id: {
                        "task_id": task.task_id,
                        "agent_id": task.agent_id,
                        "description": task.description,
                        "priority": task.priority.value,
                        "status": task.status.value,
                        "created_at": task.created_at,
                        "assigned_at": task.assigned_at,
                        "completed_at": task.completed_at,
                        "dependencies": task.dependencies,
                        "metadata": task.metadata,
                    }
                    for task_id, task in self.workflow.tasks.items()
                },
                "agent_workloads": {
                    agent_id: {
                        "agent_id": workload.agent_id,
                        "active_tasks": workload.active_tasks,
                        "completed_tasks": workload.completed_tasks,
                        "failed_tasks": workload.failed_tasks,
                        "current_capacity": workload.current_capacity,
                        "max_capacity": workload.max_capacity,
                        "last_activity": workload.last_activity,
                        "performance_score": workload.performance_score,
                    }
                    for agent_id, workload in self.workflow.agent_workloads.items()
                },
                "agent_capabilities": self.workflow.agent_capabilities,
            }

            with open(output_file, "w") as f:
                json.dump(export_data, f, indent=2)

            return True

        except Exception as e:
            print(f"Error exporting workflow: {e}")
            return False

    def import_workflow(self, input_file: str) -> bool:
        """Import workflow state from file"""
        try:
            with open(input_file) as f:
                import_data = json.load(f)

            # Validate import data structure
            if "tasks" not in import_data:
                print("Invalid import file format")
                return False

            # Clear existing workflow state
            self.workflow.tasks.clear()
            self.workflow.task_queue.clear()
            self.workflow.completed_tasks.clear()
            self.workflow.agent_workloads.clear()
            self.workflow.agent_capabilities.clear()

            # Import tasks
            imported_tasks = 0
            for task_id, task_data in import_data["tasks"].items():
                try:
                    task = CoordinationTask(
                        task_id=task_data["task_id"],
                        agent_id=task_data["agent_id"],
                        description=task_data["description"],
                        priority=TaskPriority(task_data["priority"]),
                        status=CoordinationStatus(task_data["status"]),
                        created_at=task_data["created_at"],
                        assigned_at=task_data["assigned_at"],
                        completed_at=task_data["completed_at"],
                        dependencies=task_data["dependencies"],
                        metadata=task_data["metadata"],
                    )

                    self.workflow.tasks[task_id] = task
                    imported_tasks += 1

                except Exception as e:
                    print(f"Error importing task {task_id}: {e}")

            # Import agent workloads
            for agent_id, workload_data in import_data.get("agent_workloads", {}).items():
                try:
                    from src.core.agent8_coordination_workflow_core import AgentWorkload

                    workload = AgentWorkload(**workload_data)
                    self.workflow.agent_workloads[agent_id] = workload
                except Exception as e:
                    print(f"Error importing workload for {agent_id}: {e}")

            # Import agent capabilities
            self.workflow.agent_capabilities = import_data.get("agent_capabilities", {})

            # Save imported state
            self.workflow.manage_workflow_operations("save_state")
            print(f"Successfully imported {imported_tasks} tasks")
            return True

        except Exception as e:
            print(f"Error importing workflow: {e}")
            return False

    def validate_workflow(self) -> dict[str, Any]:
        """Validate workflow integrity"""
        validation_report = {
            "valid": True,
            "issues": [],
            "statistics": {
                "total_tasks": len(self.workflow.tasks),
                "invalid_tasks": 0,
                "orphaned_dependencies": 0,
                "invalid_agents": 0,
            },
        }

        # Validate tasks
        for task_id, task in self.workflow.tasks.items():
            # Check if agent exists
            if task.agent_id not in self.workflow.agent_workloads:
                validation_report["statistics"]["invalid_agents"] += 1
                validation_report["issues"].append(
                    f"Task {task_id} references non-existent agent {task.agent_id}"
                )

            # Check dependencies
            for dep_id in task.dependencies:
                if dep_id not in self.workflow.tasks:
                    validation_report["statistics"]["orphaned_dependencies"] += 1
                    validation_report["issues"].append(
                        f"Task {task_id} has orphaned dependency {dep_id}"
                    )

        # Validate agent workloads
        for agent_id, workload in self.workflow.agent_workloads.items():
            if workload.active_tasks < 0:
                validation_report["statistics"]["invalid_tasks"] += 1
                validation_report["issues"].append(f"Agent {agent_id} has negative active tasks")

            if workload.performance_score < 0 or workload.performance_score > 2:
                validation_report["statistics"]["invalid_tasks"] += 1
                validation_report["issues"].append(
                    f"Agent {agent_id} has invalid performance score"
                )

        if validation_report["issues"]:
            validation_report["valid"] = False

        return validation_report

    def cleanup_completed_tasks(self, days: int = 30) -> dict[str, Any]:
        """Clean up old completed tasks"""
        cutoff_date = datetime.now() - timedelta(days=days)

        cleanup_report = {"success": True, "removed": 0, "errors": []}

        tasks_to_remove = []

        for task_id, task in self.workflow.tasks.items():
            if task.status == CoordinationStatus.COMPLETED:
                try:
                    completed_at = datetime.fromisoformat(task.completed_at)
                    if completed_at < cutoff_date:
                        tasks_to_remove.append(task_id)
                except Exception as e:
                    cleanup_report["errors"].append(f"Error processing task {task_id}: {e}")

        # Remove old completed tasks
        for task_id in tasks_to_remove:
            try:
                del self.workflow.tasks[task_id]
                if task_id in self.workflow.completed_tasks:
                    self.workflow.completed_tasks.remove(task_id)
                cleanup_report["removed"] += 1
            except Exception as e:
                cleanup_report["errors"].append(f"Error removing task {task_id}: {e}")

        # Save cleaned state
        if cleanup_report["removed"] > 0:
            self.workflow.manage_workflow_operations("save_state")

        return cleanup_report

    def backup_workflow(self, backup_dir: str) -> bool:
        """Create backup of workflow"""
        try:
            backup_path = Path(backup_dir)
            backup_path.mkdir(parents=True, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = backup_path / f"workflow_backup_{timestamp}.json"

            # Export workflow
            return self.export_workflow(str(backup_file))

        except Exception as e:
            print(f"Error creating backup: {e}")
            return False

    def restore_workflow(self, backup_file: str) -> bool:
        """Restore workflow from backup"""
        try:
            # Create backup of current workflow
            current_backup = f"workflow_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            self.export_workflow(current_backup)

            # Restore from backup
            return self.import_workflow(backup_file)

        except Exception as e:
            print(f"Error restoring workflow: {e}")
            return False

    def analyze_workflow_performance(self, days: int = 30) -> dict[str, Any]:
        """Analyze workflow performance over time"""
        cutoff_date = datetime.now() - timedelta(days=days)

        analysis_report = {
            "analysis_period_days": days,
            "total_tasks": len(self.workflow.tasks),
            "completed_tasks": 0,
            "failed_tasks": 0,
            "average_completion_time": 0,
            "agent_performance": {},
            "priority_breakdown": {},
            "task_trends": {"daily_completions": {}, "daily_failures": {}},
        }

        completion_times = []

        for task_id, task in self.workflow.tasks.items():
            try:
                created_at = datetime.fromisoformat(task.created_at)
                if created_at >= cutoff_date:
                    if task.status == CoordinationStatus.COMPLETED:
                        analysis_report["completed_tasks"] += 1
                        if task.completed_at:
                            completed_at = datetime.fromisoformat(task.completed_at)
                            completion_time = (
                                completed_at - created_at
                            ).total_seconds() / 3600  # hours
                            completion_times.append(completion_time)
                    elif task.status == CoordinationStatus.FAILED:
                        analysis_report["failed_tasks"] += 1

                    # Priority breakdown
                    priority = task.priority.value
                    if priority not in analysis_report["priority_breakdown"]:
                        analysis_report["priority_breakdown"][priority] = 0
                    analysis_report["priority_breakdown"][priority] += 1

            except Exception as e:
                print(f"Error analyzing task {task_id}: {e}")

        # Calculate average completion time
        if completion_times:
            analysis_report["average_completion_time"] = sum(completion_times) / len(
                completion_times
            )

        # Agent performance analysis
        for agent_id, workload in self.workflow.agent_workloads.items():
            analysis_report["agent_performance"][agent_id] = {
                "completed_tasks": workload.completed_tasks,
                "failed_tasks": workload.failed_tasks,
                "success_rate": workload.completed_tasks
                / (workload.completed_tasks + workload.failed_tasks)
                if (workload.completed_tasks + workload.failed_tasks) > 0
                else 0,
                "performance_score": workload.performance_score,
                "current_load": workload.active_tasks / workload.max_capacity
                if workload.max_capacity > 0
                else 0,
            }

        return analysis_report

    def optimize_workflow(self) -> dict[str, Any]:
        """Optimize workflow by reassigning tasks and balancing load"""
        optimization_report = {
            "success": True,
            "reassigned_tasks": 0,
            "balanced_agents": 0,
            "errors": [],
        }

        # Reassign tasks from overloaded agents
        for task_id, task in self.workflow.tasks.items():
            if task.status == CoordinationStatus.IN_PROGRESS:
                agent_id = task.agent_id
                if agent_id in self.workflow.agent_workloads:
                    workload = self.workflow.agent_workloads[agent_id]
                    capacity_ratio = workload.active_tasks / workload.max_capacity

                    # If agent is overloaded (>80% capacity), try to reassign
                    if capacity_ratio > 0.8:
                        # Find better agent
                        best_agent = self.workflow._find_best_agent_for_task(task)
                        if best_agent and best_agent != agent_id:
                            try:
                                # Reassign task
                                task.agent_id = best_agent
                                self.workflow.agent_workloads[agent_id].active_tasks -= 1
                                self.workflow.agent_workloads[best_agent].active_tasks += 1
                                optimization_report["reassigned_tasks"] += 1
                            except Exception as e:
                                optimization_report["errors"].append(
                                    f"Error reassigning task {task_id}: {e}"
                                )

        # Balance agent capacities based on performance
        for agent_id, workload in self.workflow.agent_workloads.items():
            if workload.performance_score > 1.5:  # High performer
                # Increase capacity
                workload.max_capacity = min(10, workload.max_capacity + 1)
                workload.current_capacity = workload.max_capacity
                optimization_report["balanced_agents"] += 1
            elif workload.performance_score < 0.5:  # Low performer
                # Decrease capacity
                workload.max_capacity = max(1, workload.max_capacity - 1)
                workload.current_capacity = workload.max_capacity
                optimization_report["balanced_agents"] += 1

        # Save optimized state
        if (
            optimization_report["reassigned_tasks"] > 0
            or optimization_report["balanced_agents"] > 0
        ):
            self.workflow.manage_workflow_operations("save_state")

        return optimization_report

    def monitor_task_progress(self) -> dict[str, Any]:
        """Monitor current task progress and identify bottlenecks"""
        monitor_report = {
            "timestamp": datetime.now().isoformat(),
            "active_tasks": 0,
            "stuck_tasks": 0,
            "bottlenecks": [],
            "agent_utilization": {},
            "recommendations": [],
        }

        # Analyze active tasks
        for task_id, task in self.workflow.tasks.items():
            if task.status == CoordinationStatus.IN_PROGRESS:
                monitor_report["active_tasks"] += 1

                # Check for stuck tasks (assigned but no progress for >24 hours)
                try:
                    assigned_at = datetime.fromisoformat(task.assigned_at)
                    hours_since_assigned = (datetime.now() - assigned_at).total_seconds() / 3600

                    if hours_since_assigned > 24:
                        monitor_report["stuck_tasks"] += 1
                        monitor_report["bottlenecks"].append(
                            {
                                "task_id": task_id,
                                "agent_id": task.agent_id,
                                "hours_stuck": hours_since_assigned,
                                "description": task.description,
                            }
                        )
                except Exception:
                    pass

        # Calculate agent utilization
        for agent_id, workload in self.workflow.agent_workloads.items():
            utilization = (
                workload.active_tasks / workload.max_capacity if workload.max_capacity > 0 else 0
            )
            monitor_report["agent_utilization"][agent_id] = {
                "utilization": utilization,
                "active_tasks": workload.active_tasks,
                "max_capacity": workload.max_capacity,
                "performance_score": workload.performance_score,
            }

        # Generate recommendations
        if monitor_report["stuck_tasks"] > 0:
            monitor_report["recommendations"].append("Consider reassigning stuck tasks")

        overloaded_agents = [
            agent_id
            for agent_id, util in monitor_report["agent_utilization"].items()
            if util["utilization"] > 0.9
        ]

        if overloaded_agents:
            monitor_report["recommendations"].append(
                f"Agents {', '.join(overloaded_agents)} are overloaded"
            )

        underutilized_agents = [
            agent_id
            for agent_id, util in monitor_report["agent_utilization"].items()
            if util["utilization"] < 0.3 and util["active_tasks"] == 0
        ]

        if underutilized_agents:
            monitor_report["recommendations"].append(
                f"Agents {', '.join(underutilized_agents)} are underutilized"
            )

        return monitor_report
