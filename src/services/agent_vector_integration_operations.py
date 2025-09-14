#!/usr/bin/env python3
"""
Agent Vector Integration Operations - V2 Compliance Module
==========================================================

Main orchestrator for extended agent vector integration operations.
V2 Compliance: < 100 lines, facade pattern, single responsibility.

REFACTORED: Split into focused operation classes for V2 compliance
- WorkflowOptimizer: Workflow optimization operations
- SwarmIntelligenceManager: Swarm intelligence operations
- PerformanceAnalyzer: Performance analysis operations
- LearningRecommender: Learning recommendation operations

Author: Agent-2 (Architecture & Design Specialist) - V2 Refactoring
Mission: V2 Compliance Refactoring
"""

from .learning_recommender import LearningRecommender
from .performance_analyzer import PerformanceAnalyzer
from .swarm_intelligence_manager import SwarmIntelligenceManager
from .workflow_optimizer import WorkflowOptimizer


class AgentVectorIntegrationOperations:
    """Main orchestrator for extended agent vector integration operations.

    V2 Compliance: < 100 lines, facade pattern, single responsibility.
    This class orchestrates all extended operation components.
    """

    def __init__(self, agent_id: str, config_path: str | None = None):
        """Initialize agent vector integration operations orchestrator."""
        self.agent_id = agent_id

        # Initialize specialized operation components
        self.workflow_optimizer = WorkflowOptimizer(agent_id, config_path)
        self.swarm_intelligence = SwarmIntelligenceManager(agent_id, config_path)
        self.performance_analyzer = PerformanceAnalyzer(agent_id, config_path)
        self.learning_recommender = LearningRecommender(agent_id, config_path)

    def optimize_agent_workflow(self, workflow_data):
        """Delegate to workflow optimizer."""
        return self.workflow_optimizer.optimize_agent_workflow(workflow_data)

    def get_swarm_intelligence(self, query: str):
        """Delegate to swarm intelligence manager."""
        return self.swarm_intelligence.get_swarm_intelligence(query)

    def analyze_agent_performance(self):
        """Delegate to performance analyzer."""
        return self.performance_analyzer.analyze_agent_performance()

    def get_learning_recommendations(self):
        """Delegate to learning recommender."""
        return self.learning_recommender.get_learning_recommendations()

    def sync_with_swarm(self):
        """Delegate to swarm intelligence manager."""
        return self.swarm_intelligence.sync_with_swarm()

    def get_integration_health(self):
        """Delegate to performance analyzer."""
        return self.performance_analyzer.get_integration_health()
