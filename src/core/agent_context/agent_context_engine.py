#!/usr/bin/env python3
"""
Agent Context Engine - V2 Compliance Module
==========================================

Core business logic for agent context operations.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

import time
from typing import Any, Dict, List, Optional
from datetime import datetime

from .agent_context_models import (
    AgentContext,
    Recommendation,
    ContextMetrics,
    AgentProfile,
    CommunicationPattern,
    SuccessPattern,
    CollaborationHistory,
    DomainExpertise,
    PerformanceMetrics,
    RecommendationType,
    ConfidenceLevel,
)


class AgentContextEngine:
    """Core engine for agent context operations."""

    def __init__(self):
        """Initialize agent context engine."""
        self.agent_contexts: Dict[str, AgentContext] = {}
        self.metrics = ContextMetrics()

    def get_agent_context(self, agent_id: str) -> Optional[AgentContext]:
        """Get agent context by ID."""
        return self.agent_contexts.get(agent_id)

    def update_agent_context(self, agent_context: AgentContext) -> bool:
        """Update agent context."""
        try:
            agent_context.last_updated = datetime.now()
            self.agent_contexts[agent_context.agent_id] = agent_context
            self.metrics.total_agents = len(self.agent_contexts)
            return True
        except Exception:
            return False

    def create_agent_context(self, agent_id: str, profile: AgentProfile) -> AgentContext:
        """Create new agent context."""
        agent_context = AgentContext(
            agent_id=agent_id,
            profile=profile,
            performance_metrics=PerformanceMetrics(agent_id=agent_id)
        )
        self.update_agent_context(agent_context)
        return agent_context

    def get_recommendations(self, agent_id: str, current_task: str = None) -> List[Recommendation]:
        """Get recommendations for agent."""
        start_time = time.time()
        
        try:
            agent_context = self.get_agent_context(agent_id)
            if not agent_context:
                return []
            
            recommendations = []
            
            # Task recommendations
            if current_task:
                task_recs = self._get_task_recommendations(agent_context, current_task)
                recommendations.extend(task_recs)
            
            # Communication recommendations
            comm_recs = self._get_communication_recommendations(agent_context)
            recommendations.extend(comm_recs)
            
            # Collaboration recommendations
            collab_recs = self._get_collaboration_recommendations(agent_context)
            recommendations.extend(collab_recs)
            
            # Performance recommendations
            perf_recs = self._get_performance_recommendations(agent_context)
            recommendations.extend(perf_recs)
            
            execution_time = (time.time() - start_time) * 1000
            self._update_metrics("recommendations", True, execution_time)
            
            return recommendations
            
        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            self._update_metrics("recommendations", False, execution_time)
            return []

    def add_communication_pattern(self, agent_id: str, pattern: CommunicationPattern) -> bool:
        """Add communication pattern."""
        try:
            agent_context = self.get_agent_context(agent_id)
            if agent_context:
                agent_context.communication_patterns.append(pattern)
                self.metrics.total_communication_patterns += 1
                return True
            return False
        except Exception:
            return False

    def add_success_pattern(self, agent_id: str, pattern: SuccessPattern) -> bool:
        """Add success pattern."""
        try:
            agent_context = self.get_agent_context(agent_id)
            if agent_context:
                agent_context.success_patterns.append(pattern)
                self.metrics.total_success_patterns += 1
                return True
            return False
        except Exception:
            return False

    def add_collaboration_history(self, agent_id: str, history: CollaborationHistory) -> bool:
        """Add collaboration history."""
        try:
            agent_context = self.get_agent_context(agent_id)
            if agent_context:
                agent_context.collaboration_history.append(history)
                self.metrics.total_collaborations += 1
                return True
            return False
        except Exception:
            return False

    def add_domain_expertise(self, agent_id: str, expertise: DomainExpertise) -> bool:
        """Add domain expertise."""
        try:
            agent_context = self.get_agent_context(agent_id)
            if agent_context:
                agent_context.domain_expertise.append(expertise)
                self.metrics.total_domain_expertise += 1
                return True
            return False
        except Exception:
            return False

    def update_performance_metrics(self, agent_id: str, metrics: PerformanceMetrics) -> bool:
        """Update performance metrics."""
        try:
            agent_context = self.get_agent_context(agent_id)
            if agent_context:
                agent_context.performance_metrics = metrics
                return True
            return False
        except Exception:
            return False

    def get_metrics(self) -> ContextMetrics:
        """Get context metrics."""
        return self.metrics

    # ================================
    # PRIVATE HELPER METHODS
    # ================================
    
    def _get_task_recommendations(self, agent_context: AgentContext, current_task: str) -> List[Recommendation]:
        """Get task-specific recommendations."""
        recommendations = []
        
        # Analyze task type and provide recommendations
        if "refactor" in current_task.lower():
            recommendations.append(Recommendation(
                recommendation_id=f"task_refactor_{agent_context.agent_id}",
                type=RecommendationType.TASK,
                description="Focus on modular design and V2 compliance",
                confidence=0.9,
                reasoning="Refactoring tasks require careful architecture planning",
                priority="high",
                implementation_effort="medium",
                expected_impact="high"
            ))
        
        if "test" in current_task.lower():
            recommendations.append(Recommendation(
                recommendation_id=f"task_test_{agent_context.agent_id}",
                type=RecommendationType.TASK,
                description="Implement comprehensive test coverage",
                confidence=0.8,
                reasoning="Testing ensures code quality and reliability",
                priority="high",
                implementation_effort="medium",
                expected_impact="high"
            ))
        
        return recommendations

    def _get_communication_recommendations(self, agent_context: AgentContext) -> List[Recommendation]:
        """Get communication recommendations."""
        recommendations = []
        
        # Analyze communication patterns
        if len(agent_context.communication_patterns) < 3:
            recommendations.append(Recommendation(
                recommendation_id=f"comm_pattern_{agent_context.agent_id}",
                type=RecommendationType.COMMUNICATION,
                description="Increase communication frequency with team",
                confidence=0.7,
                reasoning="More communication patterns improve collaboration",
                priority="medium",
                implementation_effort="low",
                expected_impact="medium"
            ))
        
        return recommendations

    def _get_collaboration_recommendations(self, agent_context: AgentContext) -> List[Recommendation]:
        """Get collaboration recommendations."""
        recommendations = []
        
        # Analyze collaboration history
        if len(agent_context.collaboration_history) < 2:
            recommendations.append(Recommendation(
                recommendation_id=f"collab_history_{agent_context.agent_id}",
                type=RecommendationType.COLLABORATION,
                description="Seek more collaboration opportunities",
                confidence=0.8,
                reasoning="Collaboration improves learning and outcomes",
                priority="medium",
                implementation_effort="low",
                expected_impact="high"
            ))
        
        return recommendations

    def _get_performance_recommendations(self, agent_context: AgentContext) -> List[Recommendation]:
        """Get performance recommendations."""
        recommendations = []
        
        if agent_context.performance_metrics:
            if agent_context.performance_metrics.task_completion_rate < 0.8:
                recommendations.append(Recommendation(
                    recommendation_id=f"perf_completion_{agent_context.agent_id}",
                    type=RecommendationType.PERFORMANCE,
                    description="Focus on task completion efficiency",
                    confidence=0.9,
                    reasoning="Low completion rate indicates need for improvement",
                    priority="high",
                    implementation_effort="medium",
                    expected_impact="high"
                ))
            
            if agent_context.performance_metrics.quality_score < 0.7:
                recommendations.append(Recommendation(
                    recommendation_id=f"perf_quality_{agent_context.agent_id}",
                    type=RecommendationType.PERFORMANCE,
                    description="Improve code quality and review processes",
                    confidence=0.8,
                    reasoning="Quality score indicates need for better practices",
                    priority="high",
                    implementation_effort="medium",
                    expected_impact="high"
                ))
        
        return recommendations

    def _update_metrics(self, operation: str, success: bool, execution_time: float) -> None:
        """Update metrics."""
        if operation == "recommendations":
            self.metrics.total_recommendations += 1
            if success:
                self.metrics.successful_recommendations += 1
            else:
                self.metrics.failed_recommendations += 1
        
        self.metrics.last_updated = datetime.now()
