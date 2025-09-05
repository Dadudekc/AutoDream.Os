"""
Agent Optimizer - V2 Compliant Module
====================================

Optimizes agent assignment and recommendations.
Extracted from intelligent_context_optimization.py for V2 compliance.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

import time
from typing import Any, Dict, List
from datetime import datetime

from ..intelligent_context_models import (
    MissionContext,
    AgentCapability,
    SearchResult,
    AgentRecommendation,
    RiskAssessment,
    SuccessPrediction,
    MissionPhase,
    AgentStatus,
    RiskLevel,
)


class AgentOptimizer:
    """
    Optimizes agent assignment and recommendations.
    
    Handles agent scoring, specialization matching,
    and recommendation generation.
    """
    
    def __init__(self, engine):
        """Initialize agent optimizer."""
        self.engine = engine
    
    def optimize_agent_assignment(self, mission: MissionContext) -> Dict[str, Any]:
        """Optimize agent assignment for mission."""
        start_time = time.time()
        
        try:
            recommendations = []
            
            for agent_id, capability in self.engine.agent_capabilities.items():
                if capability.availability_status == AgentStatus.AVAILABLE.value:
                    score = self._calculate_agent_score(capability, mission)
                    specialization = self._calculate_specialization_match(capability, mission)
                    
                    recommendation = AgentRecommendation(
                        agent_id=agent_id,
                        recommendation_score=score,
                        specialization_match=specialization,
                        estimated_completion_time=self._estimate_completion_time(capability, mission),
                        confidence_level=self._calculate_confidence_level(capability, mission)
                    )
                    
                    recommendations.append(recommendation)
            
            # Sort by recommendation score
            recommendations.sort(key=lambda x: x.recommendation_score, reverse=True)
            
            execution_time = (time.time() - start_time) * 1000
            self.engine._update_metrics("agent_assignment", True, execution_time)
            
            return {
                'recommendations': recommendations,
                'total_agents_considered': len(recommendations),
                'execution_time_ms': execution_time
            }
            
        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            self.engine._update_metrics("agent_assignment", False, execution_time)
            return {
                'recommendations': [],
                'total_agents_considered': 0,
                'execution_time_ms': execution_time,
                'error': str(e)
            }
    
    def _calculate_agent_score(self, capability: AgentCapability, mission: MissionContext) -> float:
        """Calculate agent recommendation score."""
        score = 0.0
        
        # Base score from success rate
        score += capability.success_rate * 0.4
        
        # Workload consideration
        if capability.current_workload < 5:
            score += 0.3
        elif capability.current_workload < 10:
            score += 0.2
        else:
            score += 0.1
        
        # Specialization match
        if capability.primary_role.lower() in mission.mission_type.lower():
            score += 0.3
        
        return min(1.0, score)
    
    def _calculate_specialization_match(self, capability: AgentCapability, mission: MissionContext) -> str:
        """Calculate specialization match."""
        if capability.primary_role.lower() in mission.mission_type.lower():
            return "exact_match"
        elif any(skill in mission.mission_type.lower() for skill in capability.skills):
            return "partial_match"
        else:
            return "no_match"
    
    def _estimate_completion_time(self, capability: AgentCapability, mission: MissionContext) -> float:
        """Estimate completion time for agent."""
        base_time = 60.0  # Base 60 minutes
        
        # Adjust based on workload
        workload_factor = 1.0 + (capability.current_workload * 0.1)
        
        # Adjust based on mission complexity
        complexity_factor = 1.0 + (len(mission.critical_path) * 0.05)
        
        # Adjust based on agent experience
        experience_factor = 1.0 - (capability.success_rate * 0.2)
        
        return base_time * workload_factor * complexity_factor * experience_factor
    
    def _calculate_confidence_level(self, capability: AgentCapability, mission: MissionContext) -> float:
        """Calculate confidence level for recommendation."""
        confidence = 0.5  # Base confidence
        
        # Increase confidence based on success rate
        confidence += capability.success_rate * 0.3
        
        # Increase confidence based on specialization match
        if capability.primary_role.lower() in mission.mission_type.lower():
            confidence += 0.2
        
        # Decrease confidence based on workload
        if capability.current_workload > 10:
            confidence -= 0.1
        
        return max(0.0, min(1.0, confidence))
    
    def get_agent_recommendations(self, mission: MissionContext, limit: int = 5) -> List[AgentRecommendation]:
        """Get top agent recommendations for mission."""
        result = self.optimize_agent_assignment(mission)
        recommendations = result.get('recommendations', [])
        
        return recommendations[:limit]
    
    def get_agent_availability(self) -> Dict[str, Any]:
        """Get agent availability summary."""
        available_count = 0
        busy_count = 0
        
        for capability in self.engine.agent_capabilities.values():
            if capability.availability_status == AgentStatus.AVAILABLE.value:
                available_count += 1
            else:
                busy_count += 1
        
        return {
            'total_agents': len(self.engine.agent_capabilities),
            'available_agents': available_count,
            'busy_agents': busy_count,
            'availability_rate': available_count / max(len(self.engine.agent_capabilities), 1)
        }
    
    def get_agent_performance_summary(self) -> Dict[str, Any]:
        """Get agent performance summary."""
        if not self.engine.agent_capabilities:
            return {}
        
        success_rates = [cap.success_rate for cap in self.engine.agent_capabilities.values()]
        workloads = [cap.current_workload for cap in self.engine.agent_capabilities.values()]
        
        return {
            'average_success_rate': sum(success_rates) / len(success_rates),
            'average_workload': sum(workloads) / len(workloads),
            'max_success_rate': max(success_rates),
            'min_success_rate': min(success_rates),
            'max_workload': max(workloads),
            'min_workload': min(workloads)
        }
    
    def get_optimizer_status(self) -> Dict[str, Any]:
        """Get optimizer status."""
        return {
            'agent_count': len(self.engine.agent_capabilities),
            'availability': self.get_agent_availability(),
            'performance': self.get_agent_performance_summary()
        }
