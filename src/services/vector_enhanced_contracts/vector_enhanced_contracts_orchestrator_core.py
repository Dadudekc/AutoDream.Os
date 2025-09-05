#!/usr/bin/env python3
"""
Vector Enhanced Contracts Orchestrator Core - V2 Compliance Module
==================================================================

Core orchestration logic for vector enhanced contracts operations.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

import uuid
from typing import Any, Dict, List, Optional
from datetime import datetime

from .vector_enhanced_contracts_models import (
    ContractAssignment,
    TaskRecommendation,
    PerformanceMetrics,
    AgentCapability,
    ContractStatus,
    PriorityLevel,
    TaskType,
    AssignmentStrategy,
    PerformanceTrend,
    OptimizationResult,
)
from .vector_enhanced_contracts_engine import VectorEnhancedContractsEngine


class VectorEnhancedContractService:
    """Main orchestrator for vector enhanced contracts operations."""

    def __init__(self, vector_db=None, lock_config=None):
        """Initialize vector enhanced contract service."""
        self.vector_db = vector_db
        self.lock_config = lock_config
        self.engine = VectorEnhancedContractsEngine()

    # ================================
    # CORE CONTRACT OPERATIONS
    # ================================
    
    def get_optimal_task_assignment(self, agent_id: str, available_tasks: List[Dict[str, Any]] = None) -> Optional[ContractAssignment]:
        """Get optimal task assignment for agent."""
        if available_tasks is None:
            available_tasks = self._get_available_tasks()
        return self.engine.get_optimal_task_assignment(agent_id, available_tasks)

    def track_contract_progress(self, assignment_id: str, progress_percentage: float, status: ContractStatus = None) -> bool:
        """Track contract progress and update status."""
        return self.engine.track_contract_progress(assignment_id, progress_percentage, status)

    def complete_contract(self, assignment_id: str, completion_notes: str = None) -> bool:
        """Mark contract as completed."""
        return self.engine.complete_contract(assignment_id, completion_notes)

    def cancel_contract(self, assignment_id: str, reason: str = None) -> bool:
        """Cancel contract assignment."""
        return self.engine.cancel_contract(assignment_id, reason)

    def get_contract_status(self, assignment_id: str) -> Optional[ContractStatus]:
        """Get current contract status."""
        return self.engine.get_contract_status(assignment_id)

    def get_agent_contracts(self, agent_id: str) -> List[ContractAssignment]:
        """Get all contracts for specific agent."""
        return self.engine.get_agent_contracts(agent_id)

    def get_contract_history(self, agent_id: str = None) -> List[ContractAssignment]:
        """Get contract history for agent or all agents."""
        return self.engine.get_contract_history(agent_id)

    # ================================
    # TASK RECOMMENDATION OPERATIONS
    # ================================
    
    def generate_task_recommendations(self, agent_id: str, task_count: int = 5) -> List[TaskRecommendation]:
        """Generate task recommendations for agent."""
        return self.engine.generate_task_recommendations(agent_id, task_count)

    def get_recommendation_by_id(self, recommendation_id: str) -> Optional[TaskRecommendation]:
        """Get specific task recommendation by ID."""
        return self.engine.get_recommendation_by_id(recommendation_id)

    def update_recommendation_confidence(self, recommendation_id: str, confidence_score: float) -> bool:
        """Update recommendation confidence score."""
        return self.engine.update_recommendation_confidence(recommendation_id, confidence_score)

    def get_agent_recommendations(self, agent_id: str) -> List[TaskRecommendation]:
        """Get all recommendations for specific agent."""
        return self.engine.get_agent_recommendations(agent_id)

    # ================================
    # PERFORMANCE METRICS OPERATIONS
    # ================================
    
    def get_agent_performance_metrics(self, agent_id: str) -> Optional[PerformanceMetrics]:
        """Get performance metrics for agent."""
        return self.engine.get_agent_performance_metrics(agent_id)

    def update_agent_performance(self, agent_id: str, metrics_data: Dict[str, Any]) -> bool:
        """Update agent performance metrics."""
        return self.engine.update_agent_performance(agent_id, metrics_data)

    def get_performance_trends(self, agent_id: str) -> List[PerformanceTrend]:
        """Get performance trends for agent."""
        return self.engine.get_performance_trends(agent_id)

    def get_all_agent_metrics(self) -> List[PerformanceMetrics]:
        """Get performance metrics for all agents."""
        return self.engine.get_all_agent_metrics()

    # ================================
    # AGENT CAPABILITY OPERATIONS
    # ================================
    
    def get_agent_capabilities(self, agent_id: str) -> Optional[AgentCapability]:
        """Get agent capabilities."""
        return self.engine.get_agent_capabilities(agent_id)

    def update_agent_capabilities(self, agent_id: str, capabilities: List[str], expertise_areas: List[str] = None) -> bool:
        """Update agent capabilities and expertise areas."""
        return self.engine.update_agent_capabilities(agent_id, capabilities, expertise_areas)

    def get_agents_by_capability(self, capability: str) -> List[AgentCapability]:
        """Get agents with specific capability."""
        return self.engine.get_agents_by_capability(capability)

    def get_available_agents(self) -> List[AgentCapability]:
        """Get all available agents."""
        return self.engine.get_available_agents()

    # ================================
    # OPTIMIZATION OPERATIONS
    # ================================
    
    def run_optimization_analysis(self, optimization_type: str = "general") -> OptimizationResult:
        """Run optimization analysis."""
        return self.engine.run_optimization_analysis(optimization_type)

    def get_optimization_recommendations(self) -> List[str]:
        """Get optimization recommendations."""
        return self.engine.get_optimization_recommendations()

    def apply_optimization(self, optimization_id: str) -> bool:
        """Apply specific optimization."""
        return self.engine.apply_optimization(optimization_id)

    def get_optimization_history(self) -> List[OptimizationResult]:
        """Get optimization history."""
        return self.engine.get_optimization_history()

    # ================================
    # UTILITY OPERATIONS
    # ================================
    
    def _get_available_tasks(self) -> List[Dict[str, Any]]:
        """Get available tasks from system."""
        return self.engine._get_available_tasks()

    def get_system_status(self) -> Dict[str, Any]:
        """Get overall system status."""
        return self.engine.get_system_status()

    def health_check(self) -> Dict[str, Any]:
        """Perform health check."""
        return self.engine.health_check()

    def get_statistics(self) -> Dict[str, Any]:
        """Get system statistics."""
        return self.engine.get_statistics()
