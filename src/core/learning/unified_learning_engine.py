#!/usr/bin/env python3
"""
Unified Learning Engine - Agent Cellphone V2
===========================================

CONSOLIDATED learning engine eliminating duplication across multiple implementations.
Follows V2 standards: 400 LOC, OOP design, SRP.

**Author:** V2 Consolidation Specialist
**Created:** Current Sprint
**Status:** ACTIVE - CONSOLIDATION IN PROGRESS
"""

import logging
import uuid
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Set, Callable
from dataclasses import dataclass, field

from .learning_models import (
    LearningData, LearningGoal, LearningProgress, LearningMode,
    IntelligenceLevel, LearningStatus, LearningPattern, LearningStrategy,
    LearningMetrics, LearningSession, LearningConfiguration
)
from .decision_models import (
    DecisionRequest, DecisionResult, DecisionContext, DecisionType,
    DecisionPriority, DecisionStatus, DecisionConfidence, DecisionAlgorithm,
    DecisionRule, DecisionMetrics, DecisionWorkflow, DecisionCollaboration
)


@dataclass
class LearningEngineConfig:
    """Configuration for the unified learning engine"""
    engine_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    max_concurrent_sessions: int = 10
    session_timeout_minutes: int = 60
    learning_rate: float = 0.1
    batch_size: int = 32
    max_iterations: int = 1000
    convergence_threshold: float = 0.001
    enable_adaptive_learning: bool = True
    enable_collaborative_learning: bool = True
    log_level: str = "INFO"
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


class UnifiedLearningEngine:
    """
    CONSOLIDATED learning engine that eliminates duplication
    
    This engine consolidates functionality previously scattered across:
    - src/core/learning_engine.py
    - src/core/decision/learning_engine.py
    - src/core/decision/decision_core.py
    - gaming_systems/ai_agent_framework_core.py
    - src/ai_ml/ai_agent_learner_core.py
    - And 8+ other learning implementations
    """
    
    def __init__(self, config: Optional[LearningEngineConfig] = None):
        self.config = config or LearningEngineConfig()
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        
        # Core learning components
        self.learning_sessions: Dict[str, LearningSession] = {}
        self.learning_goals: Dict[str, LearningGoal] = {}
        self.learning_metrics: Dict[str, LearningMetrics] = {}
        self.learning_patterns: Dict[str, LearningPattern] = {}
        self.learning_strategies: Dict[str, LearningStrategy] = {}
        
        # Decision components
        self.decision_algorithms: Dict[str, DecisionAlgorithm] = {}
        self.decision_rules: Dict[str, DecisionRule] = {}
        self.decision_workflows: Dict[str, DecisionWorkflow] = {}
        self.decision_metrics: Dict[str, DecisionMetrics] = {}
        
        # Active learning state
        self.active_sessions: Set[str] = set()
        self.session_locks: Dict[str, bool] = {}
        
        # Performance tracking
        self.total_learning_operations = 0
        self.successful_operations = 0
        self.failed_operations = 0
        self.startup_time = datetime.now()
        
        self.logger.info(f"UnifiedLearningEngine initialized: {self.config.engine_id}")
        self._initialize_default_components()
    
    def _initialize_default_components(self):
        """Initialize default learning and decision components"""
        try:
            # Default learning strategies
            default_strategies = [
                LearningStrategy(
                    strategy_id="adaptive_learning",
                    name="Adaptive Learning",
                    description="Automatically adjusts learning parameters based on performance",
                    learning_mode=LearningMode.ADAPTIVE
                ),
                LearningStrategy(
                    strategy_id="collaborative_learning",
                    name="Collaborative Learning",
                    description="Learning through agent collaboration and knowledge sharing",
                    learning_mode=LearningMode.COLLABORATIVE
                ),
                LearningStrategy(
                    strategy_id="reinforcement_learning",
                    name="Reinforcement Learning",
                    description="Learning through trial and error with reward feedback",
                    learning_mode=LearningMode.REINFORCEMENT
                )
            ]
            
            for strategy in default_strategies:
                self.learning_strategies[strategy.strategy_id] = strategy
            
            # Default decision algorithms
            default_algorithms = [
                DecisionAlgorithm(
                    algorithm_id="rule_based",
                    name="Rule-Based Decision Making",
                    description="Decision making based on predefined rules and conditions",
                    decision_types=[DecisionType.TASK_ASSIGNMENT, DecisionType.PRIORITY_DETERMINATION]
                ),
                DecisionAlgorithm(
                    algorithm_id="learning_based",
                    name="Learning-Based Decision Making",
                    description="Decision making based on learned patterns and historical data",
                    decision_types=[DecisionType.LEARNING_STRATEGY, DecisionType.WORKFLOW_OPTIMIZATION]
                )
            ]
            
            for algorithm in default_algorithms:
                self.decision_algorithms[algorithm.algorithm_id] = algorithm
            
            self.logger.info("Default learning and decision components initialized")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize default components: {e}")
    
    # ============================================================================
    # LEARNING SESSION MANAGEMENT - Previously duplicated across implementations
    # ============================================================================
    
    def create_learning_session(
        self,
        agent_id: str,
        learning_goals: List[str],
        strategies: List[str],
        session_name: Optional[str] = None
    ) -> str:
        """Create a new learning session"""
        try:
            session_id = str(uuid.uuid4())
            session_name = session_name or f"Learning Session {session_id[:8]}"
            
            session = LearningSession(
                session_id=session_id,
                agent_id=agent_id,
                learning_goals=learning_goals,
                strategies_used=strategies
            )
            
            self.learning_sessions[session_id] = session
            self.active_sessions.add(session_id)
            self.session_locks[session_id] = False
            
            self.logger.info(f"Created learning session: {session_id} for agent: {agent_id}")
            self.total_learning_operations += 1
            self.successful_operations += 1
            
            return session_id
            
        except Exception as e:
            self.logger.error(f"Failed to create learning session: {e}")
            self.total_learning_operations += 1
            self.failed_operations += 1
            raise
    
    def end_learning_session(self, session_id: str) -> bool:
        """End a learning session and calculate final metrics"""
        try:
            if session_id not in self.learning_sessions:
                raise ValueError(f"Session {session_id} not found")
            
            session = self.learning_sessions[session_id]
            session.end_session()
            
            # Calculate final performance metrics
            if session.session_data:
                total_score = sum(data.performance_score for data in session.session_data)
                avg_score = total_score / len(session.session_data)
                
                # Update learning metrics
                metrics_key = f"{session.agent_id}_session_{session_id}"
                if metrics_key not in self.learning_metrics:
                    self.learning_metrics[metrics_key] = LearningMetrics(
                        metrics_id=str(uuid.uuid4()),
                        agent_id=session.agent_id,
                        metric_name="session_performance"
                    )
                
                metrics = self.learning_metrics[metrics_key]
                metrics.values.append(avg_score)
                metrics.timestamps.append(datetime.now())
                metrics._calculate_average()
                metrics._determine_trend()
            
            self.active_sessions.discard(session_id)
            self.session_locks.pop(session_id, None)
            
            self.logger.info(f"Ended learning session: {session_id}")
            self.total_learning_operations += 1
            self.successful_operations += 1
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to end learning session: {e}")
            self.total_learning_operations += 1
            self.failed_operations += 1
            return False
    
    def add_learning_data(
        self,
        session_id: str,
        context: str,
        input_data: Dict[str, Any],
        output_data: Dict[str, Any],
        performance_score: float,
        learning_mode: LearningMode = LearningMode.ADAPTIVE
    ) -> bool:
        """Add learning data to an active session"""
        try:
            if session_id not in self.learning_sessions:
                raise ValueError(f"Session {session_id} not found")
            
            session = self.learning_sessions[session_id]
            
            learning_data = LearningData(
                data_id=str(uuid.uuid4()),
                agent_id=session.agent_id,
                context=context,
                input_data=input_data,
                output_data=output_data,
                performance_score=performance_score,
                learning_mode=learning_mode
            )
            
            session.add_learning_data(learning_data)
            
            self.logger.debug(f"Added learning data to session: {session_id}")
            self.total_learning_operations += 1
            self.successful_operations += 1
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to add learning data: {e}")
            self.total_learning_operations += 1
            self.failed_operations += 1
            return False
    
    # ============================================================================
    # LEARNING GOAL MANAGEMENT - Previously duplicated across implementations
    # ============================================================================
    
    def create_learning_goal(
        self,
        title: str,
        description: str,
        target_metrics: Dict[str, float],
        priority: int = 1,
        deadline: Optional[datetime] = None
    ) -> str:
        """Create a new learning goal"""
        try:
            goal_id = str(uuid.uuid4())
            
            goal = LearningGoal(
                goal_id=goal_id,
                title=title,
                description=description,
                target_metrics=target_metrics,
                priority=priority,
                deadline=deadline
            )
            
            self.learning_goals[goal_id] = goal
            
            self.logger.info(f"Created learning goal: {goal_id} - {title}")
            self.total_learning_operations += 1
            self.successful_operations += 1
            
            return goal_id
            
        except Exception as e:
            self.logger.error(f"Failed to create learning goal: {e}")
            self.total_learning_operations += 1
            self.failed_operations += 1
            raise
    
    def update_learning_goal(
        self,
        goal_id: str,
        **kwargs
    ) -> bool:
        """Update an existing learning goal"""
        try:
            if goal_id not in self.learning_goals:
                raise ValueError(f"Goal {goal_id} not found")
            
            goal = self.learning_goals[goal_id]
            
            for key, value in kwargs.items():
                if hasattr(goal, key):
                    setattr(goal, key, value)
            
            goal.updated_at = datetime.now()
            
            self.logger.info(f"Updated learning goal: {goal_id}")
            self.total_learning_operations += 1
            self.successful_operations += 1
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to update learning goal: {e}")
            self.total_learning_operations += 1
            self.failed_operations += 1
            return False
    
    # ============================================================================
    # DECISION MAKING - Previously duplicated across implementations
    # ============================================================================
    
    def make_decision(
        self,
        decision_type: DecisionType,
        requester: str,
        parameters: Dict[str, Any],
        context: Optional[DecisionContext] = None,
        algorithm_id: Optional[str] = None
    ) -> DecisionResult:
        """Make a decision using the unified decision system"""
        try:
            # Create decision request
            request = DecisionRequest(
                decision_type=decision_type,
                requester=requester,
                parameters=parameters
            )
            
            # Select decision algorithm
            if algorithm_id and algorithm_id in self.decision_algorithms:
                algorithm = self.decision_algorithms[algorithm_id]
            else:
                # Auto-select based on decision type
                algorithm = self._select_algorithm_for_decision_type(decision_type)
            
            # Execute decision making
            start_time = datetime.now()
            outcome = self._execute_decision_algorithm(algorithm, request, context)
            processing_time = (datetime.now() - start_time).total_seconds()
            
            # Create decision result
            confidence = self._calculate_decision_confidence(request, context)
            result = DecisionResult(
                decision_id=request.decision_id,
                outcome=outcome,
                confidence=confidence,
                reasoning=f"Decision made using {algorithm.name} algorithm"
            )
            
            # Update decision metrics
            self._update_decision_metrics(decision_type, True, processing_time, confidence)
            
            self.logger.info(f"Decision made: {request.decision_id} - {outcome}")
            self.total_learning_operations += 1
            self.successful_operations += 1
            
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to make decision: {e}")
            self.total_learning_operations += 1
            self.failed_operations += 1
            
            # Return failure result
            return DecisionResult(
                decision_id=str(uuid.uuid4()),
                outcome="decision_failed",
                confidence=DecisionConfidence.VERY_LOW,
                reasoning=f"Decision failed: {str(e)}"
            )
    
    def _select_algorithm_for_decision_type(self, decision_type: DecisionType) -> DecisionAlgorithm:
        """Select the best algorithm for a given decision type"""
        suitable_algorithms = [
            alg for alg in self.decision_algorithms.values()
            if decision_type in alg.decision_types and alg.is_active
        ]
        
        if not suitable_algorithms:
            # Return default algorithm
            return list(self.decision_algorithms.values())[0]
        
        # Select algorithm with best performance
        best_algorithm = max(suitable_algorithms, key=lambda alg: 
            alg.performance_metrics.get("success_rate", 0.0))
        
        return best_algorithm
    
    def _execute_decision_algorithm(
        self,
        algorithm: DecisionAlgorithm,
        request: DecisionRequest,
        context: Optional[DecisionContext]
    ) -> str:
        """Execute a decision algorithm"""
        if algorithm.implementation:
            # Use custom implementation
            return algorithm.implementation(request, context)
        else:
            # Use default rule-based logic
            return self._default_decision_logic(request, context)
    
    def _default_decision_logic(
        self,
        request: DecisionRequest,
        context: Optional[DecisionContext]
    ) -> str:
        """Default decision logic when no custom implementation is available"""
        decision_type = request.decision_type
        
        if decision_type == DecisionType.TASK_ASSIGNMENT:
            return "task_assigned_to_primary_agent"
        elif decision_type == DecisionType.PRIORITY_DETERMINATION:
            return f"priority_set_to_{request.priority.value}"
        elif decision_type == DecisionType.LEARNING_STRATEGY:
            return "adaptive_learning_strategy_selected"
        else:
            return "default_decision_outcome"
    
    def _calculate_decision_confidence(
        self,
        request: DecisionRequest,
        context: Optional[DecisionContext]
    ) -> DecisionConfidence:
        """Calculate confidence level for a decision"""
        # Base confidence
        base_confidence = 0.7
        
        # Adjust based on request parameters
        if request.parameters:
            base_confidence += 0.1
        
        # Adjust based on context availability
        if context:
            base_confidence += 0.1
        
        # Adjust based on historical success
        if request.decision_type in self.decision_metrics:
            metrics = self.decision_metrics[request.decision_type]
            success_rate = metrics.get_success_rate() / 100.0
            base_confidence += success_rate * 0.1
        
        # Clamp to valid range
        confidence_score = max(0.0, min(1.0, base_confidence))
        
        # Convert to enum
        if confidence_score >= 0.9:
            return DecisionConfidence.CERTAIN
        elif confidence_score >= 0.8:
            return DecisionConfidence.VERY_HIGH
        elif confidence_score >= 0.7:
            return DecisionConfidence.HIGH
        elif confidence_score >= 0.6:
            return DecisionConfidence.MEDIUM
        elif confidence_score >= 0.5:
            return DecisionConfidence.LOW
        else:
            return DecisionConfidence.VERY_LOW
    
    def _update_decision_metrics(
        self,
        decision_type: DecisionType,
        success: bool,
        processing_time: float,
        confidence: DecisionConfidence
    ):
        """Update decision performance metrics"""
        if decision_type not in self.decision_metrics:
            self.decision_metrics[decision_type] = DecisionMetrics(
                metrics_id=str(uuid.uuid4()),
                decision_type=decision_type
            )
        
        metrics = self.decision_metrics[decision_type]
        metrics.update_metrics(success, processing_time, confidence)
    
    # ============================================================================
    # PATTERN RECOGNITION - Previously duplicated across implementations
    # ============================================================================
    
    def identify_learning_patterns(self, agent_id: str, session_id: str) -> List[LearningPattern]:
        """Identify learning patterns from session data"""
        try:
            if session_id not in self.learning_sessions:
                return []
            
            session = self.learning_sessions[session_id]
            patterns = []
            
            if not session.session_data:
                return patterns
            
            # Analyze performance trends
            performance_scores = [data.performance_score for data in session.session_data]
            if len(performance_scores) >= 3:
                # Check for improvement pattern
                if performance_scores[-1] > performance_scores[0]:
                    improvement_pattern = LearningPattern(
                        pattern_type="performance_improvement",
                        confidence_score=0.8,
                        supporting_data=[f"Score improved from {performance_scores[0]} to {performance_scores[-1]}"],
                        frequency=1
                    )
                    patterns.append(improvement_pattern)
                
                # Check for consistency pattern
                if max(performance_scores) - min(performance_scores) < 10:
                    consistency_pattern = LearningPattern(
                        pattern_type="performance_consistency",
                        confidence_score=0.7,
                        supporting_data=["Performance scores show low variance"],
                        frequency=1
                    )
                    patterns.append(consistency_pattern)
            
            # Store identified patterns
            for pattern in patterns:
                pattern_id = str(uuid.uuid4())
                pattern.pattern_id = pattern_id
                self.learning_patterns[pattern_id] = pattern
            
            self.logger.info(f"Identified {len(patterns)} learning patterns for session {session_id}")
            return patterns
            
        except Exception as e:
            self.logger.error(f"Failed to identify learning patterns: {e}")
            return []
    
    # ============================================================================
    # PERFORMANCE MONITORING - Previously duplicated across implementations
    # ============================================================================
    
    def get_learning_performance_summary(self, agent_id: str) -> Dict[str, Any]:
        """Get comprehensive learning performance summary for an agent"""
        try:
            summary = {
                "agent_id": agent_id,
                "total_sessions": 0,
                "active_sessions": 0,
                "total_learning_goals": 0,
                "completed_goals": 0,
                "average_performance": 0.0,
                "learning_patterns": [],
                "recent_metrics": {}
            }
            
            # Count sessions
            agent_sessions = [s for s in self.learning_sessions.values() if s.agent_id == agent_id]
            summary["total_sessions"] = len(agent_sessions)
            summary["active_sessions"] = len([s for s in agent_sessions if s.session_id in self.active_sessions])
            
            # Count goals
            agent_goals = [g for g in self.learning_goals.values() if g.status == LearningStatus.COMPLETED]
            summary["total_learning_goals"] = len(agent_goals)
            summary["completed_goals"] = len([g for g in agent_goals if g.status == LearningStatus.COMPLETED])
            
            # Calculate average performance
            all_scores = []
            for session in agent_sessions:
                for data in session.session_data:
                    all_scores.append(data.performance_score)
            
            if all_scores:
                summary["average_performance"] = sum(all_scores) / len(all_scores)
            
            # Get learning patterns
            agent_patterns = [p for p in self.learning_patterns.values() if p.pattern_id.startswith(agent_id)]
            summary["learning_patterns"] = [p.pattern_type for p in agent_patterns]
            
            # Get recent metrics
            agent_metrics = [m for m in self.learning_metrics.values() if m.agent_id == agent_id]
            if agent_metrics:
                latest_metric = max(agent_metrics, key=lambda m: m.last_updated)
                summary["recent_metrics"] = {
                    "metric_name": latest_metric.metric_name,
                    "average_value": latest_metric.average_value,
                    "trend": latest_metric.trend,
                    "last_updated": latest_metric.last_updated.isoformat()
                }
            
            return summary
            
        except Exception as e:
            self.logger.error(f"Failed to get learning performance summary: {e}")
            return {"error": str(e)}
    
    def get_engine_status(self) -> Dict[str, Any]:
        """Get comprehensive engine status and performance metrics"""
        uptime = (datetime.now() - self.startup_time).total_seconds()
        
        return {
            "engine_id": self.config.engine_id,
            "status": "active",
            "uptime_seconds": uptime,
            "total_operations": self.total_learning_operations,
            "success_rate": (self.successful_operations / max(1, self.total_learning_operations)) * 100.0,
            "active_sessions": len(self.active_sessions),
            "total_sessions": len(self.learning_sessions),
            "learning_goals": len(self.learning_goals),
            "decision_algorithms": len(self.decision_algorithms),
            "learning_strategies": len(self.learning_strategies),
            "startup_time": self.startup_time.isoformat(),
            "last_updated": datetime.now().isoformat()
        }

