#!/usr/bin/env python3
"""
Decision Manager - Agent Cellphone V2
====================================

Modular decision manager that orchestrates decision algorithms,
workflows, and rules. Follows V2 standards: SRP, OOP design.

Author: Agent-1 (Integration & Core Systems)
License: MIT
"""

import logging
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

from ..base_manager import BaseManager, ManagerStatus, ManagerPriority, ManagerMetrics, ManagerConfig
from .decision_types import (
    DecisionRequest, DecisionResult, DecisionContext, DecisionType,
    DecisionPriority, DecisionStatus, DecisionConfidence, IntelligenceLevel,
    DecisionRule
)
from .decision_core import DecisionCore
from .decision_algorithms import DecisionAlgorithmExecutor
from .decision_workflows import DecisionWorkflowExecutor
from .decision_rules import DecisionRuleEngine


@dataclass
class DecisionManagerConfig(ManagerConfig):
    """Configuration for Decision Manager"""
    max_concurrent_decisions: int = 100
    decision_timeout_seconds: int = 300
    enable_rule_based_decisions: bool = True
    enable_learning_based_decisions: bool = True
    enable_collaborative_decisions: bool = True
    default_confidence_threshold: float = 0.7
    auto_cleanup_completed_decisions: bool = True
    cleanup_interval_minutes: int = 15
    max_decision_history: int = 1000


class DecisionManager(BaseManager):
    """
    Modular Decision Manager - Orchestrates decision components
    
    This manager coordinates the modular decision system:
    - DecisionCore: Main decision orchestration
    - DecisionAlgorithmExecutor: Algorithm management and execution
    - DecisionWorkflowExecutor: Workflow management and execution
    - DecisionRuleEngine: Rule management and evaluation
    
    Single Responsibility: Coordinate modular decision components
    for unified decision-making capabilities.
    """
    
    def __init__(self, manager_id: str, name: str = "Decision Manager", description: str = ""):
        super().__init__(manager_id, name, description)
        
        # Configuration
        self.decision_config = DecisionManagerConfig(
            manager_id=manager_id,
            name=name,
            description=description
        )
        
        # Core decision system
        self.decision_core = DecisionCore(manager_id, f"{name} Core", description)
        
        # Specialized components
        self.algorithm_executor = DecisionAlgorithmExecutor()
        self.workflow_executor = DecisionWorkflowExecutor()
        self.rule_engine = DecisionRuleEngine()
        
        # Integration state
        self.integration_status = {
            "core_system": "CONNECTED",
            "algorithm_system": "CONNECTED",
            "workflow_system": "CONNECTED",
            "rule_system": "CONNECTED",
            "integration_active": True,
            "last_health_check": datetime.now().isoformat()
        }
        
        self.logger.info(f"DecisionManager initialized: {manager_id}")
    
    def _on_start(self) -> bool:
        """Start decision manager"""
        try:
            self.logger.info("Starting Decision Manager...")
            
            # Start core system
            if not self.decision_core.start():
                self.logger.error("Failed to start decision core")
                return False
            
            # Initialize specialized components
            self.algorithm_executor.initialize()
            self.workflow_executor.initialize()
            self.rule_engine.initialize()
            
            self.logger.info("Decision Manager started successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start Decision Manager: {e}")
            return False
    
    def _on_stop(self):
        """Stop decision manager"""
        try:
            self.logger.info("Stopping Decision Manager...")
            
            # Stop core system
            self.decision_core.stop()
            
            self.logger.info("Decision Manager stopped successfully")
            
        except Exception as e:
            self.logger.error(f"Error during Decision Manager shutdown: {e}")
    
    def _on_heartbeat(self):
        """Decision manager heartbeat logic"""
        try:
            # Update integration health
            self._update_integration_health()
            
        except Exception as e:
            self.logger.error(f"Error during Decision Manager heartbeat: {e}")

    def _on_initialize_resources(self) -> bool:
        """Initialize decision manager resources"""
        try:
            self.integration_status["last_health_check"] = datetime.now().isoformat()
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize resources: {e}")
            return False

    def _on_cleanup_resources(self):
        """Cleanup decision manager resources"""
        try:
            self.decision_core.stop()
            self.integration_status["integration_active"] = False
        except Exception as e:
            self.logger.error(f"Failed to cleanup resources: {e}")

    def _on_recovery_attempt(self, error: Exception, context: str) -> bool:
        """Attempt to recover from an error"""
        try:
            self.logger.warning(f"Recovery attempt for {context}: {error}")
            self.integration_status["last_error"] = str(error)
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
        """Make a decision using the modular decision system"""
        try:
            # Delegate to decision core
            return self.decision_core.make_decision(
                decision_type=decision_type,
                requester=requester,
                parameters=parameters,
                priority=priority,
                algorithm_id=algorithm_id,
                workflow_id=workflow_id,
                context=context
            )
            
        except Exception as e:
            self.logger.error(f"Failed to make decision: {e}")
            raise
    
    def create_advanced_decision_algorithm(self, algorithm_type: str, parameters: Dict[str, Any]) -> str:
        """Create an advanced decision algorithm"""
        try:
            return self.algorithm_executor.create_advanced_algorithm(algorithm_type, parameters)
            
        except Exception as e:
            self.logger.error(f"Failed to create advanced decision algorithm: {e}")
            raise
    
    def execute_intelligent_rule_engine(self, decision_request: DecisionRequest) -> DecisionResult:
        """Execute intelligent rule engine with dynamic rule evaluation"""
        try:
            # Create decision context
            decision_context = DecisionContext(
                decision_id=decision_request.request_id,
                decision_type=decision_request.decision_type,
                timestamp=datetime.now().isoformat(),
                agent_id=decision_request.requester,
                context_data=decision_request.parameters,
                constraints=[],
                objectives=[],
                risk_factors=[]
            )
            
            # Evaluate rules
            rule_results = self.rule_engine.evaluate_rules(
                decision_context, decision_request.decision_type
            )
            
            # Find best matching rule
            best_rule = None
            for result in rule_results:
                if result.matched:
                    best_rule = self.rule_engine.get_rule(result.rule_id)
                    break
            
            if best_rule:
                # Execute decision based on rule action
                if best_rule.action == "use_collaborative_algorithm":
                    algorithm = self.algorithm_executor.get_algorithm("collaborative")
                elif best_rule.action == "use_learning_algorithm":
                    algorithm = self.algorithm_executor.get_algorithm("learning_based")
                elif best_rule.action == "execute_immediately":
                    algorithm = self.algorithm_executor.get_algorithm("rule_based")
                else:
                    algorithm = self.algorithm_executor.select_algorithm_for_decision_type(
                        decision_request.decision_type
                    )
                
                # Execute decision
                outcome = self.algorithm_executor.execute_algorithm(
                    algorithm, decision_request, decision_context
                )
                
                # Create result
                result = DecisionResult(
                    decision_id=decision_request.decision_id,
                    outcome=outcome,
                    confidence=DecisionConfidence.HIGH,
                    reasoning=f"Decision made using intelligent rule engine with rule: {best_rule.name}"
                )
                
                return result
            else:
                # No rules matched, use default decision
                return self.decision_core.make_decision(
                    decision_request.decision_type,
                    decision_request.requester,
                    decision_request.parameters,
                    decision_request.priority
                )
                
        except Exception as e:
            self.logger.error(f"Failed to execute intelligent rule engine: {e}")
            raise
    
    def coordinate_collaborative_decision(self, decision_request: DecisionRequest, participant_agents: List[str]) -> DecisionResult:
        """Coordinate collaborative decision making across multiple agents"""
        try:
            # Create collaborative decision context
            collaboration_context = DecisionContext(
                decision_id=decision_request.decision_id,
                decision_type=decision_request.decision_type,
                timestamp=datetime.now().isoformat(),
                agent_id=decision_request.requester,
                context_data={
                    **decision_request.parameters,
                    "participant_agents": participant_agents,
                    "collaboration_type": "multi_agent"
                },
                constraints=[],
                objectives=[],
                risk_factors=[]
            )
            
            # Use collaborative algorithm
            collaborative_algorithm = self.algorithm_executor.get_algorithm("collaborative")
            if not collaborative_algorithm:
                raise ValueError("Collaborative algorithm not available")
            
            # Execute collaborative decision
            outcome = self.algorithm_executor.execute_algorithm(
                collaborative_algorithm, decision_request, collaboration_context
            )
            
            # Create result
            result = DecisionResult(
                decision_id=decision_request.decision_id,
                outcome=outcome,
                confidence=DecisionConfidence.HIGH,
                reasoning=f"Collaborative decision with {len(participant_agents)} participants"
            )
            
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to coordinate collaborative decision: {e}")
            raise
    
    def assess_decision_risk(self, decision_context: DecisionContext) -> Dict[str, Any]:
        """Assess risk factors for a decision and provide mitigation strategies"""
        try:
            # Use risk-aware algorithm for assessment
            risk_algorithm = self.algorithm_executor.get_algorithm("risk_aware")
            if not risk_algorithm:
                # Fallback risk assessment
                return self._fallback_risk_assessment(decision_context)
            
            # Execute risk assessment
            risk_outcome = self.algorithm_executor.execute_algorithm(
                risk_algorithm, 
                DecisionRequest(
                    decision_type=DecisionType.RISK_ASSESSMENT,
                    requester=decision_context.agent_id,
                    parameters={"context": decision_context.context_data}
                ),
                decision_context
            )
            
            # Parse risk assessment outcome
            risk_assessment = self._parse_risk_assessment_outcome(risk_outcome, decision_context)
            
            return risk_assessment
            
        except Exception as e:
            self.logger.error(f"Failed to assess decision risk: {e}")
            return {"risk_level": "unknown", "risk_score": 0.0, "error": str(e)}
    
    def _fallback_risk_assessment(self, decision_context: DecisionContext) -> Dict[str, Any]:
        """Fallback risk assessment when risk algorithm is not available"""
        try:
            risk_assessment = {
                "risk_level": "low",
                "risk_score": 0.0,
                "risk_factors": [],
                "mitigation_strategies": [],
                "confidence_impact": 0.0
            }
            
            # Simple risk scoring based on context
            context_risk_score = 0.0
            if "high_stakes" in decision_context.context_data:
                context_risk_score += 0.3
            if "tight_deadline" in decision_context.context_data:
                context_risk_score += 0.2
            if "resource_constraints" in decision_context.context_data:
                context_risk_score += 0.2
            
            # Determine risk level
            if context_risk_score >= 0.7:
                risk_assessment["risk_level"] = "high"
            elif context_risk_score >= 0.4:
                risk_assessment["risk_level"] = "medium"
            else:
                risk_assessment["risk_level"] = "low"
            
            risk_assessment["risk_score"] = context_risk_score
            risk_assessment["confidence_impact"] = 1.0 - context_risk_score
            
            return risk_assessment
            
        except Exception as e:
            self.logger.error(f"Failed to perform fallback risk assessment: {e}")
            return {"risk_level": "unknown", "risk_score": 0.0, "error": str(e)}
    
    def _parse_risk_assessment_outcome(self, outcome: str, context: DecisionContext) -> Dict[str, Any]:
        """Parse risk assessment algorithm outcome"""
        try:
            risk_assessment = {
                "risk_level": "low",
                "risk_score": 0.0,
                "risk_factors": [],
                "mitigation_strategies": [],
                "confidence_impact": 0.0
            }
            
            # Parse outcome string to determine risk level
            if "high_risk" in outcome.lower():
                risk_assessment["risk_level"] = "high"
                risk_assessment["risk_score"] = 0.8
                risk_assessment["mitigation_strategies"] = [
                    "Implement phased approach with checkpoints",
                    "Increase monitoring and validation frequency",
                    "Prepare fallback options and contingency plans"
                ]
            elif "medium_risk" in outcome.lower():
                risk_assessment["risk_level"] = "medium"
                risk_assessment["risk_score"] = 0.5
                risk_assessment["mitigation_strategies"] = [
                    "Add intermediate validation steps",
                    "Implement progress tracking and alerts"
                ]
            else:
                risk_assessment["risk_level"] = "low"
                risk_assessment["risk_score"] = 0.2
                risk_assessment["mitigation_strategies"] = ["Standard monitoring and validation"]
            
            risk_assessment["confidence_impact"] = 1.0 - risk_assessment["risk_score"]
            
            return risk_assessment
            
        except Exception as e:
            self.logger.error(f"Failed to parse risk assessment outcome: {e}")
            return {"risk_level": "unknown", "risk_score": 0.0, "error": str(e)}
    
    def create_workflow_from_template(self, template_name: str, workflow_name: str, description: str = "") -> str:
        """Create a new workflow from a template"""
        try:
            return self.workflow_executor.create_workflow_from_template(
                template_name, workflow_name, description
            )
            
        except Exception as e:
            self.logger.error(f"Failed to create workflow from template: {e}")
            raise
    
    def add_decision_rule(self, rule: DecisionRule) -> bool:
        """Add a new decision rule"""
        try:
            return self.rule_engine.add_rule(rule)
            
        except Exception as e:
            self.logger.error(f"Failed to add decision rule: {e}")
            return False
    
    def evaluate_decision_rules(self, context: DecisionContext, decision_type: DecisionType) -> List[Any]:
        """Evaluate decision rules for a context"""
        try:
            return self.rule_engine.evaluate_rules(context, decision_type)
            
        except Exception as e:
            self.logger.error(f"Failed to evaluate decision rules: {e}")
            return []
    
    def get_decision_status(self) -> Dict[str, Any]:
        """Get comprehensive decision status"""
        try:
            # Get core status
            core_status = self.decision_core.get_decision_status()
            
            # Get component statuses
            algorithm_status = {
                "total_algorithms": self.algorithm_executor.get_algorithm_count(),
                "algorithm_ids": self.algorithm_executor.get_algorithm_ids()
            }
            
            workflow_status = {
                "total_workflows": self.workflow_executor.get_workflow_count(),
                "workflow_ids": self.workflow_executor.get_workflow_ids(),
                "templates": self.workflow_executor.get_workflow_templates()
            }
            
            rule_status = {
                "total_rules": self.rule_engine.get_rule_count(),
                "rule_ids": self.rule_engine.get_rule_ids(),
                "categories": self.rule_engine.get_categories()
            }
            
            # Compile comprehensive status
            decision_status = {
                **core_status,
                "integration_status": self.integration_status,
                "algorithm_system": algorithm_status,
                "workflow_system": workflow_status,
                "rule_system": rule_status,
                "modular_architecture": {
                    "core_system": "DecisionCore",
                    "algorithm_system": "DecisionAlgorithmExecutor",
                    "workflow_system": "DecisionWorkflowExecutor",
                    "rule_system": "DecisionRuleEngine"
                }
            }
            
            return decision_status
            
        except Exception as e:
            self.logger.error(f"Failed to get decision status: {e}")
            return {"error": str(e)}
    
    def _update_integration_health(self):
        """Update integration system health status"""
        try:
            # Check core system health
            core_health = "healthy"
            if not self.decision_core.is_running:
                core_health = "stopped"
            
            # Check component health
            algorithm_health = "healthy"
            workflow_health = "healthy"
            rule_health = "healthy"
            
            # Update integration status
            self.integration_status.update({
                "core_system": core_health,
                "algorithm_system": algorithm_health,
                "workflow_system": workflow_health,
                "rule_system": rule_health,
                "integration_active": all([
                    core_health == "healthy",
                    algorithm_health == "healthy",
                    workflow_health == "healthy",
                    rule_health == "healthy"
                ]),
                "last_health_check": datetime.now().isoformat()
            })
            
        except Exception as e:
            self.logger.error(f"Failed to update integration health: {e}")
    
    def get_integration_health(self) -> Dict[str, Any]:
        """Get integration system health status"""
        try:
            health_status = {
                "overall_health": "healthy",
                "core_system": {
                    "status": self.integration_status["core_system"],
                    "running": self.decision_core.is_running
                },
                "algorithm_system": {
                    "status": self.integration_status["algorithm_system"],
                    "algorithms_count": self.algorithm_executor.get_algorithm_count()
                },
                "workflow_system": {
                    "status": self.integration_status["workflow_system"],
                    "workflows_count": self.workflow_executor.get_workflow_count()
                },
                "rule_system": {
                    "status": self.integration_status["rule_system"],
                    "rules_count": self.rule_engine.get_rule_count()
                },
                "integration": {
                    "active": self.integration_status["integration_active"],
                    "last_health_check": self.integration_status["last_health_check"]
                }
            }
            
            # Determine overall health
            if any([
                health_status["core_system"]["status"] != "healthy",
                health_status["algorithm_system"]["status"] != "healthy",
                health_status["workflow_system"]["status"] != "healthy",
                health_status["rule_system"]["status"] != "healthy"
            ]):
                health_status["overall_health"] = "degraded"
            
            return health_status
            
        except Exception as e:
            self.logger.error(f"Failed to get integration health: {e}")
            return {"overall_health": "unknown", "error": str(e)}
