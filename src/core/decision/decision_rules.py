#!/usr/bin/env python3
"""
Decision Rules - Rule Management and Evaluation
==============================================

Manages decision rules, their evaluation, and rule-based decision
making. Follows V2 standards: SRP, OOP design.

Author: Agent-1 (Integration & Core Systems)
License: MIT
"""

import logging
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass

from .decision_types import (
    DecisionRule, DecisionType, DecisionContext, DecisionRequest
)


@dataclass
class RuleEvaluationResult:
    """Result of rule evaluation"""
    rule_id: str
    matched: bool
    confidence: float
    action_taken: str
    evaluation_time: float
    context_used: Dict[str, Any]


@dataclass
class RulePerformance:
    """Rule performance metrics"""
    total_evaluations: int = 0
    successful_matches: int = 0
    action_success_rate: float = 0.0
    average_evaluation_time: float = 0.0
    last_evaluation: Optional[datetime] = None


class DecisionRuleEngine:
    """
    Decision Rule Engine
    
    Single Responsibility: Manage and evaluate decision rules
    efficiently with performance tracking and optimization.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.DecisionRuleEngine")
        
        # Rule storage
        self.rules: Dict[str, DecisionRule] = {}
        self.rule_performance: Dict[str, RulePerformance] = {}
        
        # Rule evaluation functions
        self.custom_evaluators: Dict[str, Callable] = {}
        
        # Rule categories
        self.rule_categories: Dict[str, List[str]] = {}
        
        self.logger.info("DecisionRuleEngine initialized")
    
    def initialize(self):
        """Initialize the rule engine"""
        try:
            self.logger.info("Initializing DecisionRuleEngine...")
            
            # Initialize default rules
            self._initialize_default_rules()
            
            # Initialize rule categories
            self._initialize_rule_categories()
            
            self.logger.info("DecisionRuleEngine initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize DecisionRuleEngine: {e}")
    
    def _initialize_default_rules(self):
        """Initialize default decision rules"""
        try:
            default_rules = [
                DecisionRule(
                    rule_id="high_priority_first",
                    name="High Priority First",
                    description="Always prioritize high priority decisions",
                    condition="priority >= 4",
                    action="execute_immediately",
                    priority=1,
                    decision_types=[DecisionType.PRIORITY_DETERMINATION, DecisionType.TASK_ASSIGNMENT]
                ),
                DecisionRule(
                    rule_id="collaborative_conflict",
                    name="Collaborative Conflict Resolution",
                    description="Use collaborative approach for conflict resolution",
                    condition="decision_type == 'conflict_resolution'",
                    action="use_collaborative_algorithm",
                    priority=2,
                    decision_types=[DecisionType.CONFLICT_RESOLUTION]
                ),
                DecisionRule(
                    rule_id="learning_optimization",
                    name="Learning Strategy Optimization",
                    description="Use learning-based approach for strategy decisions",
                    condition="decision_type == 'learning_strategy'",
                    action="use_learning_algorithm",
                    priority=2,
                    decision_types=[DecisionType.LEARNING_STRATEGY]
                ),
                DecisionRule(
                    rule_id="risk_assessment_required",
                    name="Risk Assessment Required",
                    description="Require risk assessment for high-stakes decisions",
                    condition="stakes == 'high'",
                    action="require_risk_assessment",
                    priority=3,
                    decision_types=[DecisionType.RISK_ASSESSMENT, DecisionType.QUALITY_ASSURANCE]
                ),
                DecisionRule(
                    rule_id="urgent_override",
                    name="Urgent Decision Override",
                    description="Override normal procedures for urgent decisions",
                    condition="urgency == 'critical'",
                    action="urgent_override",
                    priority=1,
                    decision_types=[DecisionType.TASK_ASSIGNMENT, DecisionType.PRIORITY_DETERMINATION]
                )
            ]
            
            for rule in default_rules:
                self.rules[rule.rule_id] = rule
                self.rule_performance[rule.rule_id] = RulePerformance()
            
            self.logger.info(f"Initialized {len(default_rules)} default decision rules")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize default rules: {e}")
    
    def _initialize_rule_categories(self):
        """Initialize rule categories for organization"""
        try:
            self.rule_categories = {
                "priority": ["high_priority_first", "urgent_override"],
                "collaboration": ["collaborative_conflict"],
                "learning": ["learning_optimization"],
                "risk": ["risk_assessment_required"],
                "workflow": ["standard_workflow", "custom_workflow"]
            }
            
            self.logger.info(f"Initialized {len(self.rule_categories)} rule categories")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize rule categories: {e}")
    
    def add_rule(self, rule: DecisionRule) -> bool:
        """Add a new decision rule"""
        try:
            if rule.rule_id in self.rules:
                self.logger.warning(f"Rule {rule.rule_id} already exists, updating")
            
            self.rules[rule.rule_id] = rule
            self.rule_performance[rule.rule_id] = RulePerformance()
            
            # Add to appropriate category
            self._categorize_rule(rule)
            
            self.logger.info(f"Added rule: {rule.rule_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to add rule: {e}")
            return False
    
    def _categorize_rule(self, rule: DecisionRule):
        """Automatically categorize a rule based on its properties"""
        try:
            # Simple categorization logic
            if "priority" in rule.condition.lower() or "urgent" in rule.name.lower():
                category = "priority"
            elif "collaborative" in rule.name.lower() or "conflict" in rule.name.lower():
                category = "collaboration"
            elif "learning" in rule.name.lower() or "strategy" in rule.name.lower():
                category = "learning"
            elif "risk" in rule.name.lower() or "assessment" in rule.name.lower():
                category = "risk"
            else:
                category = "workflow"
            
            if category not in self.rule_categories:
                self.rule_categories[category] = []
            
            if rule.rule_id not in self.rule_categories[category]:
                self.rule_categories[category].append(rule.rule_id)
                
        except Exception as e:
            self.logger.error(f"Failed to categorize rule: {e}")
    
    def remove_rule(self, rule_id: str) -> bool:
        """Remove a decision rule"""
        try:
            if rule_id in self.rules:
                # Remove from rules
                del self.rules[rule_id]
                
                # Remove from performance tracking
                self.rule_performance.pop(rule_id, None)
                
                # Remove from categories
                for category_rules in self.rule_categories.values():
                    if rule_id in category_rules:
                        category_rules.remove(rule_id)
                
                # Remove custom evaluator
                self.custom_evaluators.pop(rule_id, None)
                
                self.logger.info(f"Removed rule: {rule_id}")
                return True
            else:
                self.logger.warning(f"Rule {rule_id} not found for removal")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to remove rule: {e}")
            return False
    
    def evaluate_rules(self, context: DecisionContext, decision_type: DecisionType) -> List[RuleEvaluationResult]:
        """Evaluate all applicable rules for a decision context"""
        try:
            applicable_rules = [
                rule for rule in self.rules.values()
                if decision_type in rule.decision_types and rule.is_active
            ]
            
            # Sort rules by priority (higher priority first)
            applicable_rules.sort(key=lambda r: r.priority, reverse=True)
            
            evaluation_results = []
            
            for rule in applicable_rules:
                start_time = datetime.now()
                
                try:
                    # Evaluate rule condition
                    matched = self._evaluate_rule_condition(rule, context)
                    
                    # Calculate evaluation time
                    evaluation_time = (datetime.now() - start_time).total_seconds()
                    
                    # Create evaluation result
                    result = RuleEvaluationResult(
                        rule_id=rule.rule_id,
                        matched=matched,
                        confidence=1.0 if matched else 0.0,
                        action_taken=rule.action if matched else "no_action",
                        evaluation_time=evaluation_time,
                        context_used=self._extract_context_for_rule(rule, context)
                    )
                    
                    evaluation_results.append(result)
                    
                    # Update performance metrics
                    self._update_rule_performance(rule.rule_id, matched, evaluation_time)
                    
                    # If rule matched and has high priority, stop evaluation
                    if matched and rule.priority >= 3:
                        self.logger.info(f"High priority rule {rule.rule_id} matched, stopping evaluation")
                        break
                        
                except Exception as e:
                    self.logger.error(f"Error evaluating rule {rule.rule_id}: {e}")
                    # Continue with next rule
                    continue
            
            return evaluation_results
            
        except Exception as e:
            self.logger.error(f"Error evaluating rules: {e}")
            return []
    
    def _evaluate_rule_condition(self, rule: DecisionRule, context: DecisionContext) -> bool:
        """Evaluate if a rule condition is met"""
        try:
            # Check if custom evaluator exists
            if rule.rule_id in self.custom_evaluators:
                return self.custom_evaluators[rule.rule_id](rule, context)
            
            # Use default condition evaluation
            return self._evaluate_default_condition(rule.condition, context)
            
        except Exception as e:
            self.logger.error(f"Failed to evaluate rule condition: {e}")
            return False
    
    def _evaluate_default_condition(self, condition: str, context: DecisionContext) -> bool:
        """Evaluate default condition format"""
        try:
            # Simple condition evaluation (can be enhanced with expression parsing)
            if "priority" in condition:
                # Extract priority value from context
                priority_value = context.context_data.get("priority", 0)
                if ">=" in condition:
                    threshold = int(condition.split(">=")[1])
                    return priority_value >= threshold
                elif "<=" in condition:
                    threshold = int(condition.split("<=")[1])
                    return priority_value <= threshold
                elif "==" in condition:
                    threshold = int(condition.split("==")[1])
                    return priority_value == threshold
            
            if "decision_type" in condition:
                # Extract decision type from context
                decision_type = context.decision_type
                if "==" in condition:
                    expected_type = condition.split("==")[1].strip().strip("'")
                    return decision_type == expected_type
            
            if "stakes" in condition:
                # Extract stakes value from context
                stakes_value = context.context_data.get("stakes", "low")
                if "==" in condition:
                    expected_stakes = condition.split("==")[1].strip().strip("'")
                    return stakes_value == expected_stakes
            
            if "urgency" in condition:
                # Extract urgency value from context
                urgency_value = context.context_data.get("urgency", "normal")
                if "==" in condition:
                    expected_urgency = condition.split("==")[1].strip().strip("'")
                    return urgency_value == expected_urgency
            
            # Default: condition not recognized
            return False
            
        except Exception as e:
            self.logger.error(f"Failed to evaluate default condition: {e}")
            return False
    
    def _extract_context_for_rule(self, rule: DecisionRule, context: DecisionContext) -> Dict[str, Any]:
        """Extract relevant context data for rule evaluation"""
        try:
            relevant_data = {}
            
            # Extract basic context information
            relevant_data["decision_type"] = context.decision_type
            relevant_data["agent_id"] = context.agent_id
            
            # Extract context data based on rule condition
            if "priority" in rule.condition:
                relevant_data["priority"] = context.context_data.get("priority", 0)
            
            if "stakes" in rule.condition:
                relevant_data["stakes"] = context.context_data.get("stakes", "low")
            
            if "urgency" in rule.condition:
                relevant_data["urgency"] = context.context_data.get("urgency", "normal")
            
            # Extract constraints and risk factors
            if context.constraints:
                relevant_data["constraints"] = context.constraints
            
            if context.risk_factors:
                relevant_data["risk_factors"] = context.risk_factors
            
            return relevant_data
            
        except Exception as e:
            self.logger.error(f"Failed to extract context for rule: {e}")
            return {}
    
    def _update_rule_performance(self, rule_id: str, matched: bool, evaluation_time: float):
        """Update rule performance metrics"""
        try:
            if rule_id not in self.rule_performance:
                self.rule_performance[rule_id] = RulePerformance()
            
            performance = self.rule_performance[rule_id]
            performance.total_evaluations += 1
            performance.last_evaluation = datetime.now()
            
            if matched:
                performance.successful_matches += 1
            
            # Update success rate
            performance.action_success_rate = (
                performance.successful_matches / performance.total_evaluations
            ) if performance.total_evaluations > 0 else 0.0
            
            # Update average evaluation time
            current_avg = performance.average_evaluation_time
            total_evaluations = performance.total_evaluations
            new_avg = ((current_avg * (total_evaluations - 1)) + evaluation_time) / total_evaluations
            performance.average_evaluation_time = new_avg
            
        except Exception as e:
            self.logger.error(f"Failed to update rule performance: {e}")
    
    def register_custom_evaluator(self, rule_id: str, evaluator: Callable):
        """Register a custom evaluator function for a rule"""
        try:
            if rule_id in self.rules:
                self.custom_evaluators[rule_id] = evaluator
                self.logger.info(f"Registered custom evaluator for rule: {rule_id}")
            else:
                raise ValueError(f"Rule {rule_id} not found")
                
        except Exception as e:
            self.logger.error(f"Failed to register custom evaluator: {e}")
            raise
    
    def get_rule(self, rule_id: str) -> Optional[DecisionRule]:
        """Get a rule by ID"""
        return self.rules.get(rule_id)
    
    def get_rules_by_category(self, category: str) -> List[DecisionRule]:
        """Get all rules in a specific category"""
        try:
            if category not in self.rule_categories:
                return []
            
            rule_ids = self.rule_categories[category]
            return [self.rules[rule_id] for rule_id in rule_ids if rule_id in self.rules]
            
        except Exception as e:
            self.logger.error(f"Failed to get rules by category: {e}")
            return []
    
    def get_rules_by_decision_type(self, decision_type: DecisionType) -> List[DecisionRule]:
        """Get all rules applicable to a specific decision type"""
        try:
            return [
                rule for rule in self.rules.values()
                if decision_type in rule.decision_types and rule.is_active
            ]
            
        except Exception as e:
            self.logger.error(f"Failed to get rules by decision type: {e}")
            return []
    
    def get_rule_performance(self, rule_id: str) -> Optional[RulePerformance]:
        """Get performance metrics for a specific rule"""
        return self.rule_performance.get(rule_id)
    
    def get_all_rule_performance(self) -> Dict[str, RulePerformance]:
        """Get performance metrics for all rules"""
        return self.rule_performance.copy()
    
    def get_rule_count(self) -> int:
        """Get the total number of rules"""
        return len(self.rules)
    
    def get_rule_ids(self) -> List[str]:
        """Get list of all rule IDs"""
        return list(self.rules.keys())
    
    def get_categories(self) -> List[str]:
        """Get list of all rule categories"""
        return list(self.rule_categories.keys())
    
    def get_rules_summary(self) -> Dict[str, Any]:
        """Get summary of all rules"""
        try:
            summary = {
                "total_rules": len(self.rules),
                "active_rules": len([r for r in self.rules.values() if r.is_active]),
                "categories": {},
                "decision_type_coverage": {}
            }
            
            # Category breakdown
            for category, rule_ids in self.rule_categories.items():
                summary["categories"][category] = len(rule_ids)
            
            # Decision type coverage
            decision_types = set()
            for rule in self.rules.values():
                decision_types.update(rule.decision_types)
            
            for decision_type in decision_types:
                summary["decision_type_coverage"][decision_type] = len([
                    r for r in self.rules.values()
                    if decision_type in r.decision_types
                ])
            
            return summary
            
        except Exception as e:
            self.logger.error(f"Failed to get rules summary: {e}")
            return {"error": str(e)}

