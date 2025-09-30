#!/usr/bin/env python3
"""
Dual Role Comprehensive Mission System V2 - V2 Compliant
====================================================

V2 compliant version of Dual Role Comprehensive Mission System using modular architecture.
Maintains all functionality while achieving V2 compliance (≤400 lines).

Author: Agent-7 (Web Development Specialist)
License: MIT
"""

import logging
from datetime import datetime
from typing import Any

from .mission_assessment import MissionAssessmentEngine
from .mission_models import (
    AgentCapability,
    MissionAssessment,
    MissionConfiguration,
    MissionProgress,
    MissionTask,
    TaskStatus,
)

logger = logging.getLogger(__name__)


class DualRoleComprehensiveMissionV2:
    """V2 compliant Dual Role Comprehensive Mission System."""

    def __init__(self, config: MissionConfiguration = None):
        """Initialize V2 mission system."""
        self.config = config or MissionConfiguration(
            mission_name="Dual Role Comprehensive Mission V2",
            version="2.0",
            max_concurrent_tasks=5,
            timeout_seconds=300.0,
            retry_attempts=3,
            quality_threshold=0.8,
            auto_escalation=True,
            notification_enabled=True,
            log_level="INFO",
        )

        self.assessment_engine = MissionAssessmentEngine()
        self.mission_progress = MissionProgress(
            mission_id="dual_role_v2",
            total_tasks=len(list(MissionTask)),
            completed_tasks=0,
            failed_tasks=0,
            in_progress_tasks=0,
            overall_progress=0.0,
            overall_score=0.0,
            start_time=datetime.now(),
            last_update=datetime.now(),
            estimated_completion=None,
        )

        self.agent_capabilities: dict[str, AgentCapability] = {}
        self.active_tasks: dict[str, MissionAssessment] = {}

        logger.info("Dual Role Comprehensive Mission V2 initialized")

    def register_agent_capability(
        self, agent_id: str, role: str, capabilities: list[str], expertise_level: float = 0.8
    ):
        """Register agent capability."""
        capability = AgentCapability(
            agent_id=agent_id,
            role=role,
            capabilities=capabilities,
            expertise_level=expertise_level,
            availability=True,
            current_workload=0.0,
            performance_score=0.8,
            last_assessment=datetime.now(),
        )

        self.agent_capabilities[agent_id] = capability
        logger.info(f"Agent capability registered: {agent_id}")

    def start_mission(self) -> dict[str, Any]:
        """Start the comprehensive mission."""
        try:
            self.mission_progress.start_time = datetime.now()
            self.mission_progress.last_update = datetime.now()

            # Initialize all tasks as pending
            for task in MissionTask:
                self.active_tasks[task.value] = None

            logger.info("Dual Role Comprehensive Mission V2 started")

            return {
                "success": True,
                "mission_id": self.mission_progress.mission_id,
                "start_time": self.mission_progress.start_time.isoformat(),
                "total_tasks": self.mission_progress.total_tasks,
                "config": {
                    "max_concurrent_tasks": self.config.max_concurrent_tasks,
                    "quality_threshold": self.config.quality_threshold,
                    "timeout_seconds": self.config.timeout_seconds,
                },
            }

        except Exception as e:
            logger.error(f"Error starting mission: {e}")
            return {"success": False, "error": str(e)}

    def execute_task(
        self, task: MissionTask, agent_id: str, details: dict[str, Any] = None
    ) -> dict[str, Any]:
        """Execute a specific mission task."""
        try:
            # Check agent availability
            if agent_id not in self.agent_capabilities:
                return {"success": False, "error": f"Agent {agent_id} not registered"}

            capability = self.agent_capabilities[agent_id]
            if not capability.is_available():
                return {"success": False, "error": f"Agent {agent_id} not available"}

            # Check concurrent task limit
            active_count = len([t for t in self.active_tasks.values() if t is not None])
            if active_count >= self.config.max_concurrent_tasks:
                return {"success": False, "error": "Maximum concurrent tasks reached"}

            # Execute assessment
            assessment = self.assessment_engine.assess_task(task, agent_id, details)
            self.active_tasks[task.value] = assessment

            # Update progress
            self._update_mission_progress()

            # Update agent workload
            capability.current_workload += 0.1  # Simulate workload increase

            logger.info(f"Task executed: {task.value} by {agent_id}")

            return {
                "success": True,
                "task": task.value,
                "agent_id": agent_id,
                "assessment": assessment.to_dict(),
                "mission_progress": self._get_progress_summary(),
            }

        except Exception as e:
            logger.error(f"Error executing task {task.value}: {e}")
            return {"success": False, "error": str(e)}

    def complete_task(self, task: MissionTask, final_score: float = None) -> dict[str, Any]:
        """Complete a task and update progress."""
        try:
            if task.value not in self.active_tasks or self.active_tasks[task.value] is None:
                return {"success": False, "error": f"Task {task.value} not active"}

            assessment = self.active_tasks[task.value]

            # Update assessment with final score if provided
            if final_score is not None:
                assessment.score = final_score
                assessment.status = TaskStatus.COMPLETED if final_score >= 70 else TaskStatus.FAILED

            # Mark as completed
            assessment.status = TaskStatus.COMPLETED
            assessment.progress = 100.0

            # Update progress
            self._update_mission_progress()

            # Clear from active tasks
            self.active_tasks[task.value] = None

            logger.info(f"Task completed: {task.value}")

            return {
                "success": True,
                "task": task.value,
                "final_assessment": assessment.to_dict(),
                "mission_progress": self._get_progress_summary(),
            }

        except Exception as e:
            logger.error(f"Error completing task {task.value}: {e}")
            return {"success": False, "error": str(e)}

    def get_mission_status(self) -> dict[str, Any]:
        """Get comprehensive mission status."""
        return {
            "mission_info": {
                "mission_id": self.mission_progress.mission_id,
                "version": self.config.version,
                "start_time": self.mission_progress.start_time.isoformat(),
                "last_update": self.mission_progress.last_update.isoformat(),
            },
            "progress": self._get_progress_summary(),
            "agent_capabilities": {
                agent_id: {
                    "role": cap.role,
                    "availability": cap.availability,
                    "workload": cap.current_workload,
                    "capability_score": cap.get_capability_score(),
                }
                for agent_id, cap in self.agent_capabilities.items()
            },
            "active_tasks": {
                task_name: assessment.to_dict() if assessment else None
                for task_name, assessment in self.active_tasks.items()
            },
            "assessment_summary": self.assessment_engine.get_assessment_summary(),
        }

    def _update_mission_progress(self):
        """Update mission progress metrics."""
        total_tasks = len(list(MissionTask))
        completed = len(
            [
                a
                for a in self.active_tasks.values()
                if a is not None and a.status == TaskStatus.COMPLETED
            ]
        )
        failed = len(
            [
                a
                for a in self.active_tasks.values()
                if a is not None and a.status == TaskStatus.FAILED
            ]
        )
        in_progress = len([a for a in self.active_tasks.values() if a is not None])

        self.mission_progress.completed_tasks = completed
        self.mission_progress.failed_tasks = failed
        self.mission_progress.in_progress_tasks = in_progress
        self.mission_progress.overall_progress = (
            (completed / total_tasks * 100) if total_tasks > 0 else 0
        )

        # Calculate overall score
        assessments = [a for a in self.active_tasks.values() if a is not None]
        if assessments:
            self.mission_progress.overall_score = sum(a.score for a in assessments) / len(
                assessments
            )

        self.mission_progress.last_update = datetime.now()

    def _get_progress_summary(self) -> dict[str, Any]:
        """Get progress summary."""
        return {
            "total_tasks": self.mission_progress.total_tasks,
            "completed_tasks": self.mission_progress.completed_tasks,
            "failed_tasks": self.mission_progress.failed_tasks,
            "in_progress_tasks": self.mission_progress.in_progress_tasks,
            "completion_percentage": self.mission_progress.get_completion_percentage(),
            "success_rate": self.mission_progress.get_success_rate(),
            "overall_score": self.mission_progress.overall_score,
            "overall_progress": self.mission_progress.overall_progress,
        }

    def validate_mission_integrity(self) -> dict[str, Any]:
        """Validate mission system integrity."""
        validation_result = {"valid": True, "errors": [], "warnings": [], "components_checked": 3}

        # Validate configuration
        if not self.config.is_valid():
            validation_result["valid"] = False
            validation_result["errors"].append("Invalid mission configuration")

        # Check agent capabilities
        if not self.agent_capabilities:
            validation_result["warnings"].append("No agent capabilities registered")

        # Check assessment engine
        summary = self.assessment_engine.get_assessment_summary()
        if summary["total_assessments"] == 0:
            validation_result["warnings"].append("No assessments performed yet")

        return validation_result
