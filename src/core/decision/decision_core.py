#!/usr/bin/env python3
"""
Decision Core - Core Decision Engine
===================================

Core decision-making engine that orchestrates decision algorithms,
workflows, and execution. Follows V2 standards: SRP, OOP design.

Author: Agent-1 (Integration & Core Systems)
License: MIT
"""

import logging
import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional

from ..base_manager import BaseManager, ManagerConfig
from .constants import (
    AUTO_CLEANUP_COMPLETED_DECISIONS,
    CLEANUP_INTERVAL_MINUTES,
    DECISION_TIMEOUT_SECONDS,
    DEFAULT_CONFIDENCE_THRESHOLD,
    DEFAULT_MAX_CONCURRENT_DECISIONS,
    MAX_DECISION_HISTORY,
)
from .decision_metrics import DecisionMetrics
from .decision_algorithms import DecisionAlgorithmExecutor
from .decision_rules import DecisionRuleEngine
from .decision_types import (
    DecisionAlgorithm,
    DecisionConfidence,
    DecisionContext,
    DecisionPriority,
    DecisionRequest,
    DecisionResult,
    DecisionStatus,
    DecisionType,
    IntelligenceLevel,
)
from .decision_workflows import DecisionWorkflowExecutor
from .decision_tracking import DecisionTracker
from .cleanup_rules import (
    cleanup_completed_decisions,
    schedule_cleanup,
    should_cleanup,
)
from .reporting import DecisionReporter


@dataclass
class DecisionCoreConfig(ManagerConfig):
    """Configuration for :class:`DecisionCore`."""

    max_concurrent_decisions: int = DEFAULT_MAX_CONCURRENT_DECISIONS
    decision_timeout_seconds: int = DECISION_TIMEOUT_SECONDS
    default_confidence_threshold: float = DEFAULT_CONFIDENCE_THRESHOLD
    auto_cleanup_completed_decisions: bool = AUTO_CLEANUP_COMPLETED_DECISIONS
    cleanup_interval_minutes: int = CLEANUP_INTERVAL_MINUTES
    max_decision_history: int = MAX_DECISION_HISTORY


class DecisionCore(BaseManager):
    """
    Core Decision Engine - Orchestrates decision making process

    Single Responsibility: Coordinate decision algorithms, workflows, and rules
    to execute decisions efficiently and reliably.
    """

    def __init__(
        self, manager_id: str, name: str = "Decision Core", description: str = ""
    ):
        super().__init__(manager_id, name, description)

        # Configuration
        self.config = DecisionCoreConfig(
            manager_id=manager_id, name=name, description=description
        )

        # Core components
        self.algorithm_executor = DecisionAlgorithmExecutor()
        self.workflow_executor = DecisionWorkflowExecutor()
        self.rule_engine = DecisionRuleEngine()

        # Decision tracking and reporting
        self.tracker = DecisionTracker()
        self.reporter = DecisionReporter()

        # Backwards-compatible references
        self.active_decisions = self.tracker.active_decisions
        self.decision_history = self.tracker.decision_history
        self.pending_decisions = self.tracker.pending_decisions
        self.decision_metrics = self.reporter.decision_metrics

        # Performance tracking
        self.total_decisions_made = 0
        self.successful_decisions = 0
        self.failed_decisions = 0
        self.average_decision_time = 0.0

        self.logger.info(f"DecisionCore initialized: {manager_id}")

    def _on_start(self) -> bool:
        """Start decision core"""
        try:
            self.logger.info("Starting Decision Core...")

            # Initialize components
            self.algorithm_executor.initialize()
            self.workflow_executor.initialize()
            self.rule_engine.initialize()

            # Schedule cleanup if enabled
            if self.config.auto_cleanup_completed_decisions:
                schedule_cleanup(self.tracker)

            self.logger.info("Decision Core started successfully")
            return True

        except Exception as e:
            self.logger.error(f"Failed to start Decision Core: {e}")
            return False

    def _on_stop(self):
        """Stop decision core"""
        try:
            self.logger.info("Stopping Decision Core...")

            # Clear decision data
            self.active_decisions.clear()
            self.decision_history.clear()
            self.pending_decisions.clear()

            self.logger.info("Decision Core stopped successfully")

        except Exception as e:
            self.logger.error(f"Error during Decision Core shutdown: {e}")

    def _on_heartbeat(self):
        """Decision core heartbeat logic"""
        try:
            # Check for decision timeouts
            self.tracker.check_timeouts(
                self.config.decision_timeout_seconds, self.logger
            )

            # Perform cleanup if needed
            if self.config.auto_cleanup_completed_decisions and should_cleanup(
                self.tracker.last_cleanup_time,
                self.config.cleanup_interval_minutes,
            ):
                cleanup_completed_decisions(
                    self.tracker,
                    self.config.max_decision_history,
                    self.logger,
                )

            # Update metrics
            self.reporter.update_manager_metrics(self)

        except Exception as e:
            self.logger.error(f"Error during Decision Core heartbeat: {e}")

    def _on_initialize_resources(self) -> bool:
        """Initialize decision core resources"""
        try:
            # Resources are initialized in __init__
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize resources: {e}")
            return False

    def _on_cleanup_resources(self):
        """Cleanup decision core resources"""
        try:
            self.active_decisions.clear()
            self.decision_history.clear()
            self.pending_decisions.clear()
        except Exception as e:
            self.logger.error(f"Failed to cleanup resources: {e}")

    def _on_recovery_attempt(self, error: Exception, context: str) -> bool:
        """Attempt to recover from an error"""
        try:
            self.logger.warning(f"Recovery attempt for {context}: {error}")
            # Basic reset of tracking structures
            self.active_decisions.clear()
            self.pending_decisions.clear()
            return True
        except Exception as e:
            self.logger.error(f"Recovery failed: {e}")
            return False

    def make_decision(
        self,
        decision_type: DecisionType,
        requester: str,
        parameters: Dict[str, Any],
        priority: DecisionPriority = DecisionPriority.MEDIUM,
        algorithm_id: Optional[str] = None,
        workflow_id: Optional[str] = None,
        context: Optional[DecisionContext] = None,
    ) -> DecisionResult:
        """Make a decision using the unified decision system"""
        try:
            # Create decision request
            request = DecisionRequest(
                decision_type=decision_type,
                requester=requester,
                parameters=parameters,
                priority=priority,
            )

            # Track active decision
            self.tracker.start_decision(request, algorithm_id, workflow_id)

            # Execute decision
            start_time = datetime.now()
            result = self._execute_decision(request, algorithm_id, workflow_id, context)
            execution_time = (datetime.now() - start_time).total_seconds()

            # Update tracking
            self.tracker.complete_decision(request.decision_id, result, execution_time)

            # Update metrics
            self.reporter.update_execution_metrics(
                decision_type, True, execution_time, result.confidence
            )

            self.logger.info(f"Decision completed: {request.decision_id}")
            self.total_decisions_made += 1
            self.successful_decisions += 1

            if self.config.auto_cleanup_completed_decisions:
                cleanup_completed_decisions(
                    self.tracker,
                    self.config.max_decision_history,
                    self.logger,
                )

            return result

        except Exception as e:
            self.logger.error(f"Failed to make decision: {e}")

            # Create failure result
            result = DecisionResult(
                decision_id=request.decision_id
                if "request" in locals()
                else str(uuid.uuid4()),
                outcome="decision_failed",
                confidence=DecisionConfidence.VERY_LOW,
                reasoning=f"Decision failed: {str(e)}",
            )

            # Update tracking
            if "request" in locals():
                self.tracker.record_failure(request.decision_id, result, str(e))

            # Update metrics
            if "request" in locals():
                self.reporter.update_execution_metrics(
                    decision_type, False, 0.0, DecisionConfidence.VERY_LOW
                )

            self.total_decisions_made += 1
            self.failed_decisions += 1

            if self.config.auto_cleanup_completed_decisions:
                cleanup_completed_decisions(
                    self.tracker,
                    self.config.max_decision_history,
                    self.logger,
                )

            return result

    def _execute_decision(
        self,
        request: DecisionRequest,
        algorithm_id: Optional[str],
        workflow_id: Optional[str],
        context: Optional[DecisionContext],
    ) -> DecisionResult:
        """Execute a decision using the specified algorithm and workflow"""
        try:
            # Select algorithm
            if algorithm_id and algorithm_id in self.algorithm_executor.algorithms:
                algorithm = self.algorithm_executor.algorithms[algorithm_id]
            else:
                algorithm = self.algorithm_executor.select_algorithm_for_decision_type(
                    request.decision_type
                )

            # Select workflow
            if workflow_id and workflow_id in self.workflow_executor.workflows:
                workflow = self.workflow_executor.workflows[workflow_id]
            else:
                workflow = self.workflow_executor.select_workflow_for_decision_type(
                    request.decision_type
                )

            # Execute workflow steps
            outcome = self.workflow_executor.execute_workflow(
                workflow, request, algorithm, context
            )

            # Calculate confidence
            confidence = self._calculate_decision_confidence(
                request, context, algorithm
            )

            # Create result
            result = DecisionResult(
                decision_id=request.decision_id,
                outcome=outcome,
                confidence=confidence,
                reasoning=f"Decision executed using {algorithm.name} algorithm and {workflow.name} workflow",
            )

            return result

        except Exception as e:
            self.logger.error(f"Error executing decision: {e}")
            raise

    def _calculate_decision_confidence(
        self,
        request: DecisionRequest,
        context: Optional[DecisionContext],
        algorithm: DecisionAlgorithm,
    ) -> DecisionConfidence:
        """Calculate confidence level for a decision"""
        try:
            # Base confidence from algorithm
            base_confidence = algorithm.confidence_threshold

            # Adjust based on context
            if context and hasattr(context, "risk_factors") and context.risk_factors:
                risk_factor = len(context.risk_factors) * 0.1
                base_confidence = max(0.1, base_confidence - risk_factor)

            # Adjust based on priority
            priority_factor = request.priority.value * 0.1
            base_confidence = min(1.0, base_confidence + priority_factor)

            # Convert to DecisionConfidence enum
            if base_confidence >= 0.9:
                return DecisionConfidence.HIGH
            elif base_confidence >= 0.7:
                return DecisionConfidence.HIGH
            elif base_confidence >= 0.5:
                return DecisionConfidence.MEDIUM
            elif base_confidence >= 0.3:
                return DecisionConfidence.LOW
            else:
                return DecisionConfidence.LOW

        except Exception as e:
            self.logger.error(f"Error calculating decision confidence: {e}")
            return DecisionConfidence.MEDIUM

    def get_decision_status(self) -> Dict[str, Any]:
        """Get comprehensive decision status."""
        base_status = super().get_status()
        return self.reporter.build_status(self, base_status)
