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
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

from ..base_manager import BaseManager, ManagerStatus, ManagerPriority, ManagerMetrics, ManagerConfig
from .decision_models import (
    DecisionRequest, DecisionResult, DecisionContext, DecisionType,
    DecisionPriority, DecisionStatus, DecisionConfidence, DecisionAlgorithm,
    DecisionRule, DecisionMetrics, DecisionWorkflow
)
from .decision_algorithms import DecisionAlgorithmExecutor
from .decision_workflows import DecisionWorkflowExecutor
from .decision_rules import DecisionRuleEngine


@dataclass
class DecisionCoreConfig(ManagerConfig):
    """Configuration for Decision Core"""
    max_concurrent_decisions: int = 100
    decision_timeout_seconds: int = 300
    default_confidence_threshold: float = 0.7
    auto_cleanup_completed_decisions: bool = True
    cleanup_interval_minutes: int = 15
    max_decision_history: int = 1000


class DecisionCore(BaseManager):
    """
    Core Decision Engine - Orchestrates decision making process
    
    Single Responsibility: Coordinate decision algorithms, workflows, and rules
    to execute decisions efficiently and reliably.
    """
    
    def __init__(self, manager_id: str, name: str = "Decision Core", description: str = ""):
        super().__init__(manager_id, name, description)
        
        # Configuration
        self.config = DecisionCoreConfig(
            manager_id=manager_id,
            name=name,
            description=description
        )
        
        # Core components
        self.algorithm_executor = DecisionAlgorithmExecutor()
        self.workflow_executor = DecisionWorkflowExecutor()
        self.rule_engine = DecisionRuleEngine()
        
        # Decision tracking
        self.active_decisions: Dict[str, Dict[str, Any]] = {}
        self.decision_history: List[DecisionResult] = []
        self.pending_decisions: Dict[str, DecisionRequest] = {}
        
        # Performance tracking
        self.total_decisions_made = 0
        self.successful_decisions = 0
        self.failed_decisions = 0
        self.average_decision_time = 0.0
        
        # Cleanup scheduling
        self.last_cleanup_time: Optional[datetime] = None
        
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
                self._schedule_cleanup()
            
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
            self._check_decision_timeouts()
            
            # Perform cleanup if needed
            if (self.config.auto_cleanup_completed_decisions and 
                self._should_perform_cleanup()):
                self._cleanup_completed_decisions()
            
            # Update metrics
            self._update_decision_metrics()
            
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
        context: Optional[DecisionContext] = None
    ) -> DecisionResult:
        """Make a decision using the unified decision system"""
        try:
            # Create decision request
            request = DecisionRequest(
                decision_type=decision_type,
                requester=requester,
                parameters=parameters,
                priority=priority
            )
            
            # Store in pending decisions
            self.pending_decisions[request.decision_id] = request
            
            # Track active decision
            self.active_decisions[request.decision_id] = {
                "request": request,
                "start_time": datetime.now(),
                "status": "processing",
                "algorithm_id": algorithm_id,
                "workflow_id": workflow_id
            }
            
            # Execute decision
            start_time = datetime.now()
            result = self._execute_decision(request, algorithm_id, workflow_id, context)
            execution_time = (datetime.now() - start_time).total_seconds()
            
            # Update tracking
            self.active_decisions[request.decision_id]["status"] = "completed"
            self.active_decisions[request.decision_id]["result"] = result
            self.active_decisions[request.decision_id]["execution_time"] = execution_time
            
            # Move to history
            self.decision_history.append(result)
            self.pending_decisions.pop(request.decision_id, None)
            
            # Update metrics
            self._update_decision_execution_metrics(decision_type, True, execution_time, result.confidence)
            
            self.logger.info(f"Decision completed: {request.decision_id}")
            self.total_decisions_made += 1
            self.successful_decisions += 1
            
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to make decision: {e}")
            
            # Create failure result
            result = DecisionResult(
                decision_id=request.decision_id if 'request' in locals() else str(uuid.uuid4()),
                outcome="decision_failed",
                confidence=DecisionConfidence.VERY_LOW,
                reasoning=f"Decision failed: {str(e)}"
            )
            
            # Update tracking
            if 'request' in locals() and request.decision_id in self.active_decisions:
                self.active_decisions[request.decision_id]["status"] = "failed"
                self.active_decisions[request.decision_id]["result"] = result
                self.active_decisions[request.decision_id]["error"] = str(e)
            
            # Update metrics
            if 'request' in locals():
                self._update_decision_execution_metrics(decision_type, False, 0.0, DecisionConfidence.VERY_LOW)
            
            self.total_decisions_made += 1
            self.failed_decisions += 1
            
            return result
    
    def _execute_decision(
        self,
        request: DecisionRequest,
        algorithm_id: Optional[str],
        workflow_id: Optional[str],
        context: Optional[DecisionContext]
    ) -> DecisionResult:
        """Execute a decision using the specified algorithm and workflow"""
        try:
            # Select algorithm
            if algorithm_id and algorithm_id in self.algorithm_executor.algorithms:
                algorithm = self.algorithm_executor.algorithms[algorithm_id]
            else:
                algorithm = self.algorithm_executor.select_algorithm_for_decision_type(request.decision_type)
            
            # Select workflow
            if workflow_id and workflow_id in self.workflow_executor.workflows:
                workflow = self.workflow_executor.workflows[workflow_id]
            else:
                workflow = self.workflow_executor.select_workflow_for_decision_type(request.decision_type)
            
            # Execute workflow steps
            outcome = self.workflow_executor.execute_workflow(workflow, request, algorithm, context)
            
            # Calculate confidence
            confidence = self._calculate_decision_confidence(request, context, algorithm)
            
            # Create result
            result = DecisionResult(
                decision_id=request.decision_id,
                outcome=outcome,
                confidence=confidence,
                reasoning=f"Decision executed using {algorithm.name} algorithm and {workflow.name} workflow"
            )
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error executing decision: {e}")
            raise
    
    def _calculate_decision_confidence(
        self,
        request: DecisionRequest,
        context: Optional[DecisionContext],
        algorithm: DecisionAlgorithm
    ) -> DecisionConfidence:
        """Calculate confidence level for a decision"""
        try:
            # Base confidence from algorithm
            base_confidence = algorithm.parameters.get("confidence_threshold", 0.7)
            
            # Adjust based on context
            if context and context.risk_factors:
                risk_factor = len(context.risk_factors) * 0.1
                base_confidence = max(0.1, base_confidence - risk_factor)
            
            # Adjust based on priority
            priority_factor = request.priority.value * 0.1
            base_confidence = min(1.0, base_confidence + priority_factor)
            
            # Convert to DecisionConfidence enum
            if base_confidence >= 0.9:
                return DecisionConfidence.VERY_HIGH
            elif base_confidence >= 0.7:
                return DecisionConfidence.HIGH
            elif base_confidence >= 0.5:
                return DecisionConfidence.MEDIUM
            elif base_confidence >= 0.3:
                return DecisionConfidence.LOW
            else:
                return DecisionConfidence.VERY_LOW
                
        except Exception as e:
            self.logger.error(f"Error calculating decision confidence: {e}")
            return DecisionConfidence.MEDIUM
    
    def _update_decision_execution_metrics(
        self,
        decision_type: DecisionType,
        success: bool,
        execution_time: float,
        confidence: DecisionConfidence
    ):
        """Update decision execution metrics"""
        try:
            if decision_type not in self.decision_metrics:
                self.decision_metrics[decision_type] = DecisionMetrics(
                    metrics_id=str(uuid.uuid4()),
                    decision_type=decision_type
                )
            
            metrics = self.decision_metrics[decision_type]
            metrics.update_metrics(success, execution_time, confidence)
            
        except Exception as e:
            self.logger.error(f"Failed to update decision metrics: {e}")
    
    def _update_decision_metrics(self):
        """Update decision performance metrics"""
        try:
            # Update manager metrics
            self.metrics.operations_processed = self.total_decisions_made
            self.metrics.errors_count = self.failed_decisions
            
            # Calculate success rate
            if self.total_decisions_made > 0:
                success_rate = (self.successful_decisions / self.total_decisions_made) * 100.0
                self.metrics.performance_score = success_rate
            
            # Update last operation time
            self.metrics.last_operation = datetime.now()
            
        except Exception as e:
            self.logger.error(f"Failed to update decision metrics: {e}")
    
    def _check_decision_timeouts(self):
        """Check for decisions that have exceeded timeout"""
        try:
            current_time = datetime.now()
            timed_out_decisions = []
            
            for decision_id, decision_data in self.active_decisions.items():
                if decision_data["status"] == "processing":
                    start_time = decision_data["start_time"]
                    elapsed_time = (current_time - start_time).total_seconds()
                    
                    if elapsed_time > self.config.decision_timeout_seconds:
                        timed_out_decisions.append(decision_id)
            
            # Handle timed out decisions
            for decision_id in timed_out_decisions:
                self.active_decisions[decision_id]["status"] = "timeout"
                self.active_decisions[decision_id]["result"] = DecisionResult(
                    decision_id=decision_id,
                    outcome="decision_timeout",
                    confidence=DecisionConfidence.VERY_LOW,
                    reasoning="Decision exceeded timeout limit"
                )
                
                self.logger.warning(f"Decision {decision_id} timed out")
            
        except Exception as e:
            self.logger.error(f"Error checking decision timeouts: {e}")
    
    def _schedule_cleanup(self):
        """Schedule automatic cleanup of completed decisions"""
        self.last_cleanup_time = datetime.now()
        self.logger.info("Scheduled automatic cleanup of completed decisions")
    
    def _should_perform_cleanup(self) -> bool:
        """Check if cleanup should be performed"""
        if not self.last_cleanup_time:
            return True
        
        time_since_cleanup = datetime.now() - self.last_cleanup_time
        return time_since_cleanup.total_seconds() >= (self.config.cleanup_interval_minutes * 60)
    
    def _cleanup_completed_decisions(self):
        """Clean up completed decisions"""
        try:
            current_time = datetime.now()
            decisions_to_cleanup = []
            
            # Find completed decisions
            for decision_id, decision_data in self.active_decisions.items():
                if decision_data["status"] in ["completed", "failed"]:
                    decisions_to_cleanup.append(decision_id)
            
            # Clean up completed decisions
            for decision_id in decisions_to_cleanup:
                self.active_decisions.pop(decision_id, None)
            
            # Limit decision history
            if len(self.decision_history) > self.config.max_decision_history:
                excess = len(self.decision_history) - self.config.max_decision_history
                self.decision_history = self.decision_history[excess:]
            
            if decisions_to_cleanup:
                self.logger.info(f"Cleaned up {len(decisions_to_cleanup)} completed decisions")
            
            self.last_cleanup_time = current_time
            
        except Exception as e:
            self.logger.error(f"Error during decision cleanup: {e}")
    
    def get_decision_status(self) -> Dict[str, Any]:
        """Get comprehensive decision status"""
        base_status = super().get_status()
        
        decision_status = {
            **base_status,
            "decision_algorithms": len(self.algorithm_executor.algorithms),
            "decision_workflows": len(self.workflow_executor.workflows),
            "decision_rules": len(self.rule_engine.rules),
            "active_decisions": len(self.active_decisions),
            "pending_decisions": len(self.pending_decisions),
            "decision_history_size": len(self.decision_history),
            "decision_operations": {
                "total": self.total_decisions_made,
                "successful": self.successful_decisions,
                "failed": self.failed_decisions,
                "success_rate": (self.successful_decisions / max(1, self.total_decisions_made)) * 100.0,
                "average_execution_time": self.average_decision_time
            },
            "cleanup_status": {
                "auto_cleanup_enabled": self.config.auto_cleanup_completed_decisions,
                "last_cleanup": self.last_cleanup_time.isoformat() if self.last_cleanup_time else None,
                "cleanup_interval_minutes": self.config.cleanup_interval_minutes
            }
        }
        
        return decision_status

