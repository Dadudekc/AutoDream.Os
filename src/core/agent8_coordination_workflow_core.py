#!/usr/bin/env python3
"""
Agent-8 Coordination Workflow Core
================================
Core logic for Agent-8 coordination workflow integration
V2 Compliant: ≤400 lines, focused coordination logic
"""

import json
from dataclasses import asdict, dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any


class CoordinationStatus(Enum):
    """Coordination status enumeration"""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskPriority(Enum):
    """Task priority enumeration"""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class CoordinationTask:
    """Coordination task structure"""

    task_id: str
    agent_id: str
    description: str
    priority: TaskPriority
    status: CoordinationStatus
    created_at: str
    assigned_at: str
    completed_at: str
    dependencies: list[str]
    metadata: dict[str, Any]

    def __post_init__(self):
        if isinstance(self.priority, str):
            self.priority = TaskPriority(self.priority)
        if isinstance(self.status, str):
            self.status = CoordinationStatus(self.status)


@dataclass
class AgentWorkload:
    """Agent workload tracking"""

    agent_id: str
    active_tasks: int
    completed_tasks: int
    failed_tasks: int
    current_capacity: int
    max_capacity: int
    last_activity: str
    performance_score: float


class Agent8CoordinationWorkflowCore:
    """Core logic for Agent-8 coordination workflow integration system"""

    def __init__(self, workflow_dir: str = "coordination_workflow"):
        self.workflow_dir = Path(workflow_dir)
        self.workflow_dir.mkdir(exist_ok=True)

        # Task management
        self.tasks: dict[str, CoordinationTask] = {}
        self.task_queue: list[str] = []
        self.completed_tasks: list[str] = []

        # Agent management
        self.agent_workloads: dict[str, AgentWorkload] = {}
        self.agent_capabilities: dict[str, list[str]] = {}

        # Workflow settings
        self.max_concurrent_tasks = 10
        self.task_timeout_hours = 24
        self.auto_reassignment_enabled = True

        self.load_workflow_state()

    def manage_workflow_operations(self, action: str, **kwargs) -> Any:
        """Consolidated workflow operations"""
        if action == "load_state":
            self.load_workflow_state()
            return True
        elif action == "save_state":
            self.save_workflow_state()
            return True
        elif action == "register_agent":
            self.register_agent(
                kwargs["agent_id"], kwargs["capabilities"], kwargs.get("max_capacity", 5)
            )
            return True
        elif action == "create_task":
            return self.create_task(
                kwargs["agent_id"],
                kwargs["description"],
                kwargs.get("priority", TaskPriority.MEDIUM),
                kwargs.get("dependencies"),
                kwargs.get("metadata"),
            )
        elif action == "assign_task":
            return self.assign_task(kwargs["task_id"], kwargs.get("agent_id"))
        elif action == "complete_task":
            return self.complete_task(kwargs["task_id"], kwargs.get("success", True))
        elif action == "get_status":
            return self.get_workflow_status()
        elif action == "get_performance":
            return self.get_agent_performance_report(kwargs.get("agent_id"))
        elif action == "auto_assign":
            return self.auto_assign_pending_tasks()
        return None

    def load_workflow_state(self) -> None:
        """Load workflow state from disk"""
        state_file = self.workflow_dir / "workflow_state.json"
        if state_file.exists():
            try:
                with open(state_file) as f:
                    data = json.load(f)

                # Load tasks
                for task_id, task_data in data.get("tasks", {}).items():
                    self.tasks[task_id] = CoordinationTask(**task_data)

                # Load task queue
                self.task_queue = data.get("task_queue", [])
                self.completed_tasks = data.get("completed_tasks", [])

                # Load agent workloads
                for agent_id, workload_data in data.get("agent_workloads", {}).items():
                    self.agent_workloads[agent_id] = AgentWorkload(**workload_data)

                # Load agent capabilities
                self.agent_capabilities = data.get("agent_capabilities", {})

            except Exception as e:
                print(f"Warning: Failed to load workflow state: {e}")

    def save_workflow_state(self) -> None:
        """Save workflow state to disk"""
        state_file = self.workflow_dir / "workflow_state.json"
        try:
            data = {
                "tasks": {k: asdict(v) for k, v in self.tasks.items()},
                "task_queue": self.task_queue,
                "completed_tasks": self.completed_tasks,
                "agent_workloads": {k: asdict(v) for k, v in self.agent_workloads.items()},
                "agent_capabilities": self.agent_capabilities,
                "last_updated": datetime.now().isoformat(),
            }

            with open(state_file, "w") as f:
                json.dump(data, f, indent=2)

        except Exception as e:
            print(f"Error saving workflow state: {e}")

    def register_agent(self, agent_id: str, capabilities: list[str], max_capacity: int = 5) -> None:
        """Register agent with coordination system"""
        self.agent_capabilities[agent_id] = capabilities
        self.agent_workloads[agent_id] = AgentWorkload(
            agent_id=agent_id,
            active_tasks=0,
            completed_tasks=0,
            failed_tasks=0,
            current_capacity=max_capacity,
            max_capacity=max_capacity,
            last_activity=datetime.now().isoformat(),
            performance_score=1.0,
        )
        self.save_workflow_state()

    def create_task(
        self,
        agent_id: str,
        description: str,
        priority: TaskPriority = TaskPriority.MEDIUM,
        dependencies: list[str] = None,
        metadata: dict[str, Any] = None,
    ) -> str:
        """Create new coordination task"""
        task_id = f"task_{len(self.tasks) + 1}_{int(datetime.now().timestamp())}"

        task = CoordinationTask(
            task_id=task_id,
            agent_id=agent_id,
            description=description,
            priority=priority,
            status=CoordinationStatus.PENDING,
            created_at=datetime.now().isoformat(),
            assigned_at="",
            completed_at="",
            dependencies=dependencies or [],
            metadata=metadata or {},
        )

        self.tasks[task_id] = task

        # Add to queue if dependencies are met
        if self._dependencies_met(task_id):
            self.task_queue.append(task_id)
            self._sort_task_queue()

        self.save_workflow_state()
        return task_id

    def assign_task(self, task_id: str, agent_id: str = None) -> bool:
        """Assign task to agent"""
        if task_id not in self.tasks:
            return False

        task = self.tasks[task_id]

        # Use provided agent_id or find best available agent
        if agent_id is None:
            agent_id = self._find_best_agent_for_task(task)

        if agent_id is None:
            return False

        # Check if agent has capacity
        if not self._agent_has_capacity(agent_id):
            return False

        # Assign task
        task.agent_id = agent_id
        task.status = CoordinationStatus.IN_PROGRESS
        task.assigned_at = datetime.now().isoformat()

        # Update agent workload
        self.agent_workloads[agent_id].active_tasks += 1
        self.agent_workloads[agent_id].last_activity = datetime.now().isoformat()

        # Remove from queue
        if task_id in self.task_queue:
            self.task_queue.remove(task_id)

        self.save_workflow_state()
        return True

    def complete_task(self, task_id: str, success: bool = True) -> bool:
        """Mark task as completed"""
        if task_id not in self.tasks:
            return False

        task = self.tasks[task_id]
        agent_id = task.agent_id

        # Update task status
        if success:
            task.status = CoordinationStatus.COMPLETED
            self.completed_tasks.append(task_id)
        else:
            task.status = CoordinationStatus.FAILED

        task.completed_at = datetime.now().isoformat()

        # Update agent workload
        if agent_id in self.agent_workloads:
            self.agent_workloads[agent_id].active_tasks -= 1
            if success:
                self.agent_workloads[agent_id].completed_tasks += 1
                # Improve performance score
                self.agent_workloads[agent_id].performance_score = min(
                    2.0, self.agent_workloads[agent_id].performance_score + 0.1
                )
            else:
                self.agent_workloads[agent_id].failed_tasks += 1
                # Decrease performance score
                self.agent_workloads[agent_id].performance_score = max(
                    0.1, self.agent_workloads[agent_id].performance_score - 0.1
                )

            self.agent_workloads[agent_id].last_activity = datetime.now().isoformat()

        # Check for dependent tasks that can now be queued
        self._update_dependent_tasks(task_id)

        self.save_workflow_state()
        return True

    def _dependencies_met(self, task_id: str) -> bool:
        """Check if task dependencies are met"""
        task = self.tasks[task_id]

        for dep_id in task.dependencies:
            if dep_id not in self.tasks:
                return False

            dep_task = self.tasks[dep_id]
            if dep_task.status != CoordinationStatus.COMPLETED:
                return False

        return True

    def _sort_task_queue(self) -> None:
        """Sort task queue by priority and creation time"""

        def task_priority(task_id: str) -> tuple[int, str]:
            task = self.tasks[task_id]
            priority_order = {
                TaskPriority.CRITICAL: 0,
                TaskPriority.HIGH: 1,
                TaskPriority.MEDIUM: 2,
                TaskPriority.LOW: 3,
            }
            return (priority_order.get(task.priority, 2), task.created_at)

        self.task_queue.sort(key=task_priority)

    def _find_best_agent_for_task(self, task: CoordinationTask) -> str | None:
        """Find best available agent for task"""
        best_agent = None
        best_score = -1

        for agent_id, workload in self.agent_workloads.items():
            if not self._agent_has_capacity(agent_id):
                continue

            # Check if agent has required capabilities
            if not self._agent_has_capabilities(agent_id, task.description):
                continue

            # Calculate agent score
            score = self._calculate_agent_score(agent_id, task)

            if score > best_score:
                best_score = score
                best_agent = agent_id

        return best_agent

    def _agent_has_capacity(self, agent_id: str) -> bool:
        """Check if agent has capacity for new task"""
        if agent_id not in self.agent_workloads:
            return False

        workload = self.agent_workloads[agent_id]
        return workload.active_tasks < workload.current_capacity

    def _agent_has_capabilities(self, agent_id: str, task_description: str) -> bool:
        """Check if agent has required capabilities for task"""
        if agent_id not in self.agent_capabilities:
            return False

        capabilities = self.agent_capabilities[agent_id]
        task_lower = task_description.lower()

        # Simple capability matching
        for capability in capabilities:
            if capability.lower() in task_lower:
                return True

        return True

    def _calculate_agent_score(self, agent_id: str, task: CoordinationTask) -> float:
        """Calculate agent suitability score for task"""
        workload = self.agent_workloads[agent_id]

        # Base score from performance
        score = workload.performance_score

        # Bonus for low current workload
        capacity_ratio = workload.active_tasks / workload.current_capacity
        score += (1.0 - capacity_ratio) * 0.5

        # Bonus for recent activity
        last_activity = datetime.fromisoformat(workload.last_activity)
        hours_since_activity = (datetime.now() - last_activity).total_seconds() / 3600
        if hours_since_activity < 1:
            score += 0.3

        return score

    def _update_dependent_tasks(self, completed_task_id: str) -> None:
        """Update dependent tasks that can now be queued"""
        for task_id, task in self.tasks.items():
            if task.status == CoordinationStatus.PENDING and completed_task_id in task.dependencies:
                if self._dependencies_met(task_id):
                    if task_id not in self.task_queue:
                        self.task_queue.append(task_id)
                        self._sort_task_queue()

    def get_workflow_status(self) -> dict[str, Any]:
        """Get comprehensive workflow status"""
        total_tasks = len(self.tasks)
        pending_tasks = len(
            [t for t in self.tasks.values() if t.status == CoordinationStatus.PENDING]
        )
        in_progress_tasks = len(
            [t for t in self.tasks.values() if t.status == CoordinationStatus.IN_PROGRESS]
        )
        completed_tasks = len(
            [t for t in self.tasks.values() if t.status == CoordinationStatus.COMPLETED]
        )
        failed_tasks = len(
            [t for t in self.tasks.values() if t.status == CoordinationStatus.FAILED]
        )

        return {
            "total_tasks": total_tasks,
            "pending_tasks": pending_tasks,
            "in_progress_tasks": in_progress_tasks,
            "completed_tasks": completed_tasks,
            "failed_tasks": failed_tasks,
            "task_queue_length": len(self.task_queue),
            "registered_agents": len(self.agent_workloads),
            "active_agents": len([w for w in self.agent_workloads.values() if w.active_tasks > 0]),
            "last_updated": datetime.now().isoformat(),
        }

    def get_agent_performance_report(self, agent_id: str = None) -> dict[str, Any]:
        """Get agent performance report"""
        if agent_id:
            if agent_id not in self.agent_workloads:
                return {}

            workload = self.agent_workloads[agent_id]
            return {
                "agent_id": agent_id,
                "active_tasks": workload.active_tasks,
                "completed_tasks": workload.completed_tasks,
                "failed_tasks": workload.failed_tasks,
                "success_rate": workload.completed_tasks
                / (workload.completed_tasks + workload.failed_tasks)
                if (workload.completed_tasks + workload.failed_tasks) > 0
                else 0,
                "performance_score": workload.performance_score,
                "last_activity": workload.last_activity,
                "current_capacity": workload.current_capacity,
                "max_capacity": workload.max_capacity,
            }
        else:
            # Return report for all agents
            return {
                agent_id: self.get_agent_performance_report(agent_id)
                for agent_id in self.agent_workloads.keys()
            }

    def auto_assign_pending_tasks(self) -> int:
        """Automatically assign pending tasks to available agents"""
        assigned_count = 0

        for task_id in self.task_queue.copy():
            if self.assign_task(task_id):
                assigned_count += 1

        return assigned_count

