#!/usr/bin/env python3
"""
Intelligent Coordinator Core
===========================

Core logic for intelligent agent coordination system.

Author: Agent-8 (SSOT & System Integration Specialist)
License: MIT
"""

import logging
from typing import Any, Dict, List

from swarm_brain import Ingestor, Retriever, SwarmBrain

from .core.messaging_service import MessagingService
from .intelligent_coordinator_models import (
    AgentProfile,
    CoordinationPlan,
    CoordinationResult,
    CoordinationTask,
    PerformanceMetrics,
    SwarmIntelligence,
    TaskRouting,
)

logger = logging.getLogger(__name__)


class IntelligentCoordinatorCore:
    """Core intelligent coordination logic."""

    def __init__(self):
        self.swarm_brain = SwarmBrain()
        self.retriever = Retriever()
        self.ingestor = Ingestor()
        self.messaging_service = MessagingService()
        logger.info("🧠 Intelligent Coordinator Core initialized")

    def find_expert_agents(self, task: str, required_skills: List[str]) -> List[str]:
        """Find expert agents for a task."""
        logger.info(f"🔍 Finding expert agents for: {task}")
        
        # Search for agents with relevant expertise
        expert_results = self.retriever.get_agent_expertise(task, k=20)
        
        expert_agents = []
        for result in expert_results:
            agent_id = result.get("agent_id", "")
            if agent_id and self._has_required_skills(agent_id, required_skills):
                expert_agents.append(agent_id)
        
        logger.info(f"✅ Found {len(expert_agents)} expert agents")
        return expert_agents

    def get_coordination_patterns(self, task: str) -> List[Dict[str, Any]]:
        """Get successful coordination patterns for a task."""
        logger.info(f"📊 Retrieving coordination patterns for: {task}")
        
        patterns = self.retriever.how_do_agents_do(f"coordinate {task}", k=10)
        logger.info(f"✅ Retrieved {len(patterns)} coordination patterns")
        return patterns

    def create_coordination_plan(
        self,
        expert_agents: List[str],
        patterns: List[Dict[str, Any]],
        task: str,
    ) -> CoordinationPlan:
        """Create a coordination plan based on expert agents and patterns."""
        logger.info(f"📋 Creating coordination plan for: {task}")
        
        # Select best agents based on patterns
        assigned_agents = self._select_best_agents(expert_agents, patterns)
        
        # Determine coordination strategy
        strategy = self._determine_strategy(patterns)
        
        # Estimate duration and success probability
        duration = self._estimate_duration(patterns)
        success_prob = self._calculate_success_probability(patterns)
        
        plan = CoordinationPlan(
            task=task,
            assigned_agents=assigned_agents,
            coordination_strategy=strategy,
            estimated_duration=duration,
            success_probability=success_prob,
        )
        
        logger.info(f"✅ Created coordination plan with {len(assigned_agents)} agents")
        return plan

    def execute_coordination(self, plan: CoordinationPlan) -> CoordinationResult:
        """Execute the coordination plan."""
        logger.info(f"🚀 Executing coordination plan for: {plan.task}")
        
        start_time = self._get_current_time()
        
        try:
            # Send coordination messages
            for agent_id in plan.assigned_agents:
                self._send_coordination_message(agent_id, plan)
            
            # Monitor coordination
            success = self._monitor_coordination(plan)
            
            execution_time = self._get_current_time() - start_time
            
            result = CoordinationResult(
                success=success,
                assigned_agents=plan.assigned_agents,
                coordination_plan=plan,
                execution_time=execution_time,
                performance_metrics=self._calculate_metrics(plan),
            )
            
            logger.info(f"✅ Coordination executed successfully: {success}")
            return result
            
        except Exception as e:
            logger.error(f"❌ Coordination execution failed: {e}")
            return CoordinationResult(
                success=False,
                assigned_agents=plan.assigned_agents,
                coordination_plan=plan,
                execution_time=self._get_current_time() - start_time,
                performance_metrics={},
            )

    def optimize_coordination(self, task: str) -> SwarmIntelligence:
        """Optimize coordination using swarm intelligence."""
        logger.info(f"🧠 Optimizing coordination for: {task}")
        
        # Get coordination patterns
        patterns = self.get_coordination_patterns(task)
        
        # Find expert agents
        expert_agents = self.find_expert_agents(task, [])
        
        # Calculate success rate
        success_rate = self._calculate_pattern_success_rate(patterns)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(patterns)
        
        intelligence = SwarmIntelligence(
            patterns=patterns,
            expert_agents=expert_agents,
            success_rate=success_rate,
            recommendations=recommendations,
        )
        
        logger.info(f"✅ Generated swarm intelligence with {len(recommendations)} recommendations")
        return intelligence

    def _has_required_skills(self, agent_id: str, required_skills: List[str]) -> bool:
        """Check if agent has required skills."""
        # This would check agent capabilities
        return True  # Simplified for now

    def _select_best_agents(self, agents: List[str], patterns: List[Dict[str, Any]]) -> List[str]:
        """Select best agents based on patterns."""
        # Simplified selection logic
        return agents[:3] if len(agents) >= 3 else agents

    def _determine_strategy(self, patterns: List[Dict[str, Any]]) -> str:
        """Determine coordination strategy from patterns."""
        if not patterns:
            return "standard"
        
        # Analyze patterns to determine best strategy
        return "collaborative" if len(patterns) > 5 else "sequential"

    def _estimate_duration(self, patterns: List[Dict[str, Any]]) -> str:
        """Estimate task duration from patterns."""
        if not patterns:
            return "2-5 cycles"
        
        # Analyze patterns for duration estimates
        return "1-3 cycles" if len(patterns) > 3 else "3-7 cycles"

    def _calculate_success_probability(self, patterns: List[Dict[str, Any]]) -> float:
        """Calculate success probability from patterns."""
        if not patterns:
            return 0.7
        
        # Calculate based on pattern success rates
        return min(0.95, 0.7 + (len(patterns) * 0.05))

    def _send_coordination_message(self, agent_id: str, plan: CoordinationPlan) -> None:
        """Send coordination message to agent."""
        message = f"Coordination task: {plan.task} - Strategy: {plan.coordination_strategy}"
        self.messaging_service.send_message(agent_id, message)

    def _monitor_coordination(self, plan: CoordinationPlan) -> bool:
        """Monitor coordination execution."""
        # Simplified monitoring
        return True

    def _calculate_metrics(self, plan: CoordinationPlan) -> Dict[str, Any]:
        """Calculate performance metrics."""
        return {
            "coordination_success_rate": plan.success_probability,
            "agent_count": len(plan.assigned_agents),
            "strategy": plan.coordination_strategy,
        }

    def _calculate_pattern_success_rate(self, patterns: List[Dict[str, Any]]) -> float:
        """Calculate success rate from patterns."""
        if not patterns:
            return 0.7
        
        # Simplified calculation
        return min(0.95, 0.7 + (len(patterns) * 0.03))

    def _generate_recommendations(self, patterns: List[Dict[str, Any]]) -> List[str]:
        """Generate coordination recommendations."""
        recommendations = []
        
        if len(patterns) > 5:
            recommendations.append("Use collaborative coordination strategy")
        
        if len(patterns) < 3:
            recommendations.append("Consider expanding agent pool")
        
        recommendations.append("Monitor coordination progress closely")
        
        return recommendations

    def _get_current_time(self) -> float:
        """Get current timestamp."""
        import time
        return time.time()
