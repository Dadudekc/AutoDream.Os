#!/usr/bin/env python3
"""
Agent Context Orchestrator - V2 Compliance Module
================================================

Main coordination logic for agent context operations.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

from typing import Any, Dict, List, Optional

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
)
from .agent_context_engine import AgentContextEngine


class AgentContextSystem:
    """Main orchestrator for agent context operations."""

    def __init__(self, agent_id: str, vector_db=None):
        """Initialize agent context system."""
        self.agent_id = agent_id
        self.vector_db = vector_db
        self.engine = AgentContextEngine()

    # ================================
    # CORE CONTEXT OPERATIONS
    # ================================
    
    def get_agent_context(self, agent_id: str = None) -> Optional[AgentContext]:
        """Get agent context."""
        target_id = agent_id or self.agent_id
        return self.engine.get_agent_context(target_id)

    def update_agent_context(self, agent_context: AgentContext) -> bool:
        """Update agent context."""
        return self.engine.update_agent_context(agent_context)

    def create_agent_context(self, agent_id: str, profile: AgentProfile) -> AgentContext:
        """Create new agent context."""
        return self.engine.create_agent_context(agent_id, profile)

    def get_recommendations(self, current_task: str = None, agent_id: str = None) -> List[Recommendation]:
        """Get recommendations for agent."""
        target_id = agent_id or self.agent_id
        return self.engine.get_recommendations(target_id, current_task)

    # ================================
    # PATTERN MANAGEMENT
    # ================================
    
    def add_communication_pattern(self, pattern: CommunicationPattern, agent_id: str = None) -> bool:
        """Add communication pattern."""
        target_id = agent_id or self.agent_id
        return self.engine.add_communication_pattern(target_id, pattern)

    def add_success_pattern(self, pattern: SuccessPattern, agent_id: str = None) -> bool:
        """Add success pattern."""
        target_id = agent_id or self.agent_id
        return self.engine.add_success_pattern(target_id, pattern)

    def add_collaboration_history(self, history: CollaborationHistory, agent_id: str = None) -> bool:
        """Add collaboration history."""
        target_id = agent_id or self.agent_id
        return self.engine.add_collaboration_history(target_id, history)

    def add_domain_expertise(self, expertise: DomainExpertise, agent_id: str = None) -> bool:
        """Add domain expertise."""
        target_id = agent_id or self.agent_id
        return self.engine.add_domain_expertise(target_id, expertise)

    def update_performance_metrics(self, metrics: PerformanceMetrics, agent_id: str = None) -> bool:
        """Update performance metrics."""
        target_id = agent_id or self.agent_id
        return self.engine.update_performance_metrics(target_id, metrics)

    # ================================
    # CONVENIENCE METHODS
    # ================================
    
    def get_agent_profile(self, agent_id: str = None) -> Optional[AgentProfile]:
        """Get agent profile."""
        agent_context = self.get_agent_context(agent_id)
        return agent_context.profile if agent_context else None

    def get_communication_patterns(self, agent_id: str = None) -> List[CommunicationPattern]:
        """Get communication patterns."""
        agent_context = self.get_agent_context(agent_id)
        return agent_context.communication_patterns if agent_context else []

    def get_success_patterns(self, agent_id: str = None) -> List[SuccessPattern]:
        """Get success patterns."""
        agent_context = self.get_agent_context(agent_id)
        return agent_context.success_patterns if agent_context else []

    def get_collaboration_history(self, agent_id: str = None) -> List[CollaborationHistory]:
        """Get collaboration history."""
        agent_context = self.get_agent_context(agent_id)
        return agent_context.collaboration_history if agent_context else []

    def get_domain_expertise(self, agent_id: str = None) -> List[DomainExpertise]:
        """Get domain expertise."""
        agent_context = self.get_agent_context(agent_id)
        return agent_context.domain_expertise if agent_context else []

    def get_performance_metrics(self, agent_id: str = None) -> Optional[PerformanceMetrics]:
        """Get performance metrics."""
        agent_context = self.get_agent_context(agent_id)
        return agent_context.performance_metrics if agent_context else None

    def get_context_metrics(self) -> ContextMetrics:
        """Get context metrics."""
        return self.engine.get_metrics()

    def get_agent_summary(self, agent_id: str = None) -> Dict[str, Any]:
        """Get comprehensive agent summary."""
        target_id = agent_id or self.agent_id
        agent_context = self.get_agent_context(target_id)
        
        if not agent_context:
            return {"error": "Agent not found"}
        
        return {
            "agent_id": target_id,
            "profile": agent_context.profile.__dict__,
            "communication_patterns_count": len(agent_context.communication_patterns),
            "success_patterns_count": len(agent_context.success_patterns),
            "collaboration_history_count": len(agent_context.collaboration_history),
            "domain_expertise_count": len(agent_context.domain_expertise),
            "performance_metrics": agent_context.performance_metrics.__dict__ if agent_context.performance_metrics else None,
            "last_updated": agent_context.last_updated.isoformat()
        }

    def get_recommendation_summary(self, agent_id: str = None) -> Dict[str, Any]:
        """Get recommendation summary."""
        target_id = agent_id or self.agent_id
        recommendations = self.get_recommendations(agent_id=target_id)
        
        if not recommendations:
            return {"message": "No recommendations available"}
        
        # Group by type
        by_type = {}
        for rec in recommendations:
            rec_type = rec.type.value
            if rec_type not in by_type:
                by_type[rec_type] = []
            by_type[rec_type].append(rec.to_dict())
        
        return {
            "total_recommendations": len(recommendations),
            "by_type": by_type,
            "high_priority": [r.to_dict() for r in recommendations if r.priority == "high"],
            "average_confidence": sum(r.confidence for r in recommendations) / len(recommendations)
        }

    def batch_update_agents(self, agent_updates: List[Dict[str, Any]]) -> Dict[str, bool]:
        """Batch update multiple agents."""
        results = {}
        for update in agent_updates:
            agent_id = update.get("agent_id")
            if agent_id:
                # Create or update agent context
                profile = AgentProfile(
                    agent_id=agent_id,
                    name=update.get("name", ""),
                    role=update.get("role", ""),
                    specialization=update.get("specialization", []),
                    experience_level=update.get("experience_level", "intermediate"),
                    communication_style=update.get("communication_style", "professional"),
                    preferred_task_types=update.get("preferred_task_types", [])
                )
                
                agent_context = self.create_agent_context(agent_id, profile)
                results[agent_id] = self.update_agent_context(agent_context)
        
        return results

    def get_system_health(self) -> Dict[str, Any]:
        """Get system health status."""
        metrics = self.get_context_metrics()
        
        health_score = 100.0
        
        # Adjust based on metrics
        if metrics.total_agents > 0:
            success_rate = metrics.successful_recommendations / max(metrics.total_recommendations, 1)
            health_score *= success_rate
        
        if metrics.total_agents == 0:
            health_score *= 0.5  # Penalty for no agents
        
        return {
            "health_score": health_score,
            "status": "healthy" if health_score > 80 else "degraded" if health_score > 50 else "critical",
            "total_agents": metrics.total_agents,
            "total_recommendations": metrics.total_recommendations,
            "success_rate": success_rate if metrics.total_recommendations > 0 else 0,
            "average_confidence": metrics.average_confidence
        }


# ================================
# GLOBAL INSTANCE
# ================================

_global_agent_context_system = None

def create_agent_context_system(agent_id: str, vector_db=None) -> AgentContextSystem:
    """Create agent context system instance."""
    return AgentContextSystem(agent_id, vector_db)


# ================================
# CONVENIENCE FUNCTIONS
# ================================

def get_agent_context(agent_id: str) -> Optional[AgentContext]:
    """Convenience function to get agent context."""
    system = create_agent_context_system(agent_id)
    return system.get_agent_context(agent_id)

def update_agent_context(agent_context: AgentContext) -> bool:
    """Convenience function to update agent context."""
    system = create_agent_context_system(agent_context.agent_id)
    return system.update_agent_context(agent_context)

def get_recommendations(agent_id: str, current_task: str = None) -> List[Recommendation]:
    """Convenience function to get recommendations."""
    system = create_agent_context_system(agent_id)
    return system.get_recommendations(current_task, agent_id)

def get_agent_profile(agent_id: str) -> Optional[AgentProfile]:
    """Convenience function to get agent profile."""
    system = create_agent_context_system(agent_id)
    return system.get_agent_profile(agent_id)

def get_communication_patterns(agent_id: str) -> List[CommunicationPattern]:
    """Convenience function to get communication patterns."""
    system = create_agent_context_system(agent_id)
    return system.get_communication_patterns(agent_id)

def get_success_patterns(agent_id: str) -> List[SuccessPattern]:
    """Convenience function to get success patterns."""
    system = create_agent_context_system(agent_id)
    return system.get_success_patterns(agent_id)

def get_collaboration_history(agent_id: str) -> List[CollaborationHistory]:
    """Convenience function to get collaboration history."""
    system = create_agent_context_system(agent_id)
    return system.get_collaboration_history(agent_id)

def get_domain_expertise(agent_id: str) -> List[DomainExpertise]:
    """Convenience function to get domain expertise."""
    system = create_agent_context_system(agent_id)
    return system.get_domain_expertise(agent_id)

def get_performance_metrics(agent_id: str) -> Optional[PerformanceMetrics]:
    """Convenience function to get performance metrics."""
    system = create_agent_context_system(agent_id)
    return system.get_performance_metrics(agent_id)

def get_context_metrics() -> ContextMetrics:
    """Convenience function to get context metrics."""
    engine = AgentContextEngine()
    return engine.get_metrics()
