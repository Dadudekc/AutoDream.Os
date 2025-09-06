#!/usr/bin/env python3
"""
Swarm Coordination Orchestrator - V2 Compliance Module
=====================================================

Main orchestrator for swarm coordination operations.
Refactored from 362-line monolithic file into focused modules.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

import asyncio
import time
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
import logging

from ..coordination_models import (
    CoordinationConfig,
    CoordinationTask,
    CoordinationResult,
    CoordinationMetrics,
    CoordinationStrategy,
    CoordinationPriority,
    CoordinationStatus,
    create_default_config,
    create_coordination_task,
    create_coordination_result,
    create_coordination_metrics,
)
from ..engines.task_coordination_engine import TaskCoordinationEngine
from ..engines.performance_monitoring_engine import PerformanceMonitoringEngine

# Import coordination utilities with fallback
try:
    from ...utils.coordination_utils import CoordinationUtils
    from ...utils.agent_matching import AgentMatchingUtils
    from ...utils.performance_metrics import PerformanceMetricsUtils
    from ...utils.vector_insights import VectorInsightsUtils
except ImportError:
    # Fallback implementations
    class CoordinationUtils:
        @staticmethod
        def optimize_coordination(*args, **kwargs):
            return {}

    class AgentMatchingUtils:
        @staticmethod
        def find_best_agent(*args, **kwargs):
            return "Agent-1"

    class PerformanceMetricsUtils:
        @staticmethod
        def calculate_efficiency(*args, **kwargs):
            return 0.8

    class VectorInsightsUtils:
        @staticmethod
        def get_insights(*args, **kwargs):
            return {}


class SwarmCoordinationEnhancer:
    """Main orchestrator for swarm coordination enhancement system.

    Provides unified interface to all coordination capabilities while maintaining V2
    compliance through modular architecture.
    """

    def __init__(self, config: Optional[CoordinationConfig] = None):
        """Initialize swarm coordination enhancer."""
        self.logger = logging.getLogger(__name__)
        self.config = config or create_default_config()

        # Validate configuration
        try:
            self.config.validate()
        except Exception as e:
            self.logger.error(f"Invalid configuration: {e}")
            raise

        # Initialize engines
        self.task_engine = TaskCoordinationEngine(self.config)
        self.performance_engine = PerformanceMonitoringEngine(self.config)

        # Initialize utility components
        self.coordination_utils = CoordinationUtils()
        self.agent_matching = AgentMatchingUtils()
        self.performance_metrics = PerformanceMetricsUtils()
        self.vector_insights = VectorInsightsUtils()

        # System state
        self.is_active = False
        self.start_time = None

        self.logger.info("🚀 Swarm Coordination Enhancer initialized")

    def start_coordination(self) -> bool:
        """Start coordination system."""
        try:
            if self.is_active:
                self.logger.warning("Coordination system is already active")
                return True

            self.is_active = True
            self.start_time = datetime.now()

            self.logger.info("Swarm coordination system started")
            return True

        except Exception as e:
            self.logger.error(f"Failed to start coordination system: {e}")
            return False

    def stop_coordination(self) -> bool:
        """Stop coordination system."""
        try:
            if not self.is_active:
                self.logger.warning("Coordination system is not active")
                return True

            self.is_active = False

            self.logger.info("Swarm coordination system stopped")
            return True

        except Exception as e:
            self.logger.error(f"Failed to stop coordination system: {e}")
            return False

    async def coordinate_task(self, task: CoordinationTask) -> CoordinationResult:
        """Coordinate execution of a task."""
        if not self.is_active:
            return self._create_error_result(task, "Coordination system is not active")

        try:
            # Coordinate task through task engine
            result = await self.task_engine.coordinate_task(task)

            # Update performance metrics
            self.performance_engine.update_metrics(result)

            return result

        except Exception as e:
            self.logger.error(f"Failed to coordinate task {task.task_id}: {e}")
            return self._create_error_result(task, str(e))

    def _create_error_result(
        self, task: CoordinationTask, error_message: str
    ) -> CoordinationResult:
        """Create error result for failed task."""
        return create_coordination_result(
            task_id=task.task_id,
            success=False,
            error_message=error_message,
            result_data={"error": error_message},
        )

    def get_coordination_summary(self) -> Dict[str, Any]:
        """Get comprehensive coordination summary."""
        uptime = None
        if self.start_time:
            uptime = (datetime.now() - self.start_time).total_seconds()

        task_summary = self.task_engine.get_task_summary()
        performance_summary = self.performance_engine.get_performance_summary()

        return {
            "system_info": {
                "is_active": self.is_active,
                "uptime_seconds": uptime,
                "start_time": self.start_time.isoformat() if self.start_time else None,
            },
            "task_coordination": task_summary,
            "performance_monitoring": performance_summary,
            "configuration": {
                "max_concurrent_tasks": self.config.max_concurrent_tasks,
                "task_timeout_seconds": self.config.task_timeout_seconds,
                "enable_priority_queues": self.config.enable_priority_queues,
                "performance_monitoring_enabled": (
                    self.config.enable_performance_monitoring
                ),
            },
        }

    def get_performance_metrics(self) -> CoordinationMetrics:
        """Get current performance metrics."""
        return self.performance_engine.metrics

    def reset_metrics(self) -> None:
        """Reset all metrics and statistics."""
        self.performance_engine.reset_metrics()
        self.task_engine.clear_completed_tasks()
        self.logger.info("All metrics and statistics reset")
