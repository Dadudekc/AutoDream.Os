#!/usr/bin/env python3
"""
Vector Enhanced Contracts Orchestrator - V2 Compliance Module
============================================================

Main coordination logic for vector enhanced contracts operations.

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
from .vector_enhanced_contracts_engine import VectorEnhancedContractEngine


class VectorEnhancedContractService:
    """Main orchestrator for vector enhanced contracts operations."""

    def __init__(self, vector_db=None, lock_config=None):
        """Initialize vector enhanced contract service."""
        self.vector_db = vector_db
        self.lock_config = lock_config
        self.engine = VectorEnhancedContractEngine()

    # ================================
    # CORE CONTRACT OPERATIONS
    # ================================
    
    def get_optimal_task_assignment(self, agent_id: str, available_tasks: List[Dict[str, Any]] = None) -> Optional[ContractAssignment]:
        """Get optimal task assignment for agent."""
        if available_tasks is None:
            available_tasks = self._get_available_tasks()
        return self.engine.get_optimal_task_assignment(agent_id, available_tasks)

    def track_contract_progress(self, assignment_id: str, progress_percentage: float, status: ContractStatus = None) -> bool:
        """Track contract progress."""
        return self.engine.track_contract_progress(assignment_id, progress_percentage, status)

    def analyze_performance_patterns(self, agent_id: str) -> List[PerformanceTrend]:
        """Analyze performance patterns for agent."""
        return self.engine.analyze_performance_patterns(agent_id)

    def optimize_agent_assignments(self) -> List[OptimizationResult]:
        """Optimize agent assignments."""
        return self.engine.optimize_agent_assignments()

    def get_contract_recommendations(self, agent_id: str) -> List[TaskRecommendation]:
        """Get contract recommendations for agent."""
        return self.engine.get_contract_recommendations(agent_id)

    def update_agent_capabilities(self, agent_id: str, capabilities: AgentCapability) -> bool:
        """Update agent capabilities."""
        return self.engine.update_agent_capabilities(agent_id, capabilities)

    def get_performance_metrics(self, agent_id: str = None) -> Dict[str, Any]:
        """Get performance metrics."""
        return self.engine.get_performance_metrics(agent_id)

    # ================================
    # CONTRACT MANAGEMENT
    # ================================
    
    def create_contract_assignment(self, contract_id: str, agent_id: str, task_type: TaskType, 
                                 priority: PriorityLevel, estimated_duration: float = 0.0) -> ContractAssignment:
        """Create new contract assignment."""
        assignment = ContractAssignment(
            assignment_id=str(uuid.uuid4()),
            contract_id=contract_id,
            agent_id=agent_id,
            task_type=task_type,
            priority=priority,
            status=ContractStatus.ASSIGNED,
            estimated_duration=estimated_duration
        )
        
        self.engine.contract_assignments[assignment.assignment_id] = assignment
        return assignment

    def get_contract_assignment(self, assignment_id: str) -> Optional[ContractAssignment]:
        """Get contract assignment by ID."""
        return self.engine.contract_assignments.get(assignment_id)

    def get_agent_assignments(self, agent_id: str) -> List[ContractAssignment]:
        """Get all assignments for agent."""
        return [a for a in self.engine.contract_assignments.values() if a.agent_id == agent_id]

    def update_assignment_status(self, assignment_id: str, status: ContractStatus) -> bool:
        """Update assignment status."""
        assignment = self.engine.contract_assignments.get(assignment_id)
        if assignment:
            assignment.status = status
            if status == ContractStatus.COMPLETED:
                assignment.completed_at = datetime.now()
            return True
        return False

    # ================================
    # AGENT MANAGEMENT
    # ================================
    
    def register_agent(self, agent_id: str, capabilities: List[str], expertise_areas: List[str]) -> bool:
        """Register new agent."""
        agent_capability = AgentCapability(
            agent_id=agent_id,
            capabilities=capabilities,
            expertise_areas=expertise_areas,
            performance_score=0.5,  # Default score
            availability=True,
            current_load=0.0
        )
        return self.engine.update_agent_capabilities(agent_id, agent_capability)

    def get_agent_capability(self, agent_id: str) -> Optional[AgentCapability]:
        """Get agent capability."""
        return self.engine.agent_capabilities.get(agent_id)

    def get_all_agent_capabilities(self) -> Dict[str, AgentCapability]:
        """Get all agent capabilities."""
        return self.engine.agent_capabilities

    def update_agent_availability(self, agent_id: str, availability: bool) -> bool:
        """Update agent availability."""
        agent_capability = self.engine.agent_capabilities.get(agent_id)
        if agent_capability:
            agent_capability.availability = availability
            return True
        return False

    def update_agent_load(self, agent_id: str, load: float) -> bool:
        """Update agent current load."""
        agent_capability = self.engine.agent_capabilities.get(agent_id)
        if agent_capability:
            agent_capability.current_load = load
            return True
        return False

    # ================================
    # PERFORMANCE ANALYSIS
    # ================================
    
    def get_performance_trends(self, agent_id: str = None) -> List[PerformanceTrend]:
        """Get performance trends."""
        if agent_id:
            return [t for t in self.engine.performance_trends if t.agent_id == agent_id]
        return self.engine.performance_trends

    def get_optimization_results(self) -> List[OptimizationResult]:
        """Get optimization results."""
        return self.engine.optimization_results

    def calculate_agent_efficiency(self, agent_id: str) -> float:
        """Calculate agent efficiency score."""
        agent_assignments = self.get_agent_assignments(agent_id)
        if not agent_assignments:
            return 0.0
        
        completed_assignments = [a for a in agent_assignments if a.status == ContractStatus.COMPLETED]
        if not completed_assignments:
            return 0.0
        
        # Calculate efficiency based on completion rate and time accuracy
        completion_rate = len(completed_assignments) / len(agent_assignments)
        
        time_accuracy = 0.0
        for assignment in completed_assignments:
            if assignment.estimated_duration > 0 and assignment.actual_duration:
                accuracy = 1.0 - abs(assignment.actual_duration - assignment.estimated_duration) / assignment.estimated_duration
                time_accuracy += max(0, accuracy)
        
        time_accuracy = time_accuracy / len(completed_assignments) if completed_assignments else 0.0
        
        return (completion_rate + time_accuracy) / 2

    def get_contract_analytics(self) -> Dict[str, Any]:
        """Get comprehensive contract analytics."""
        assignments = list(self.engine.contract_assignments.values())
        
        if not assignments:
            return {"message": "No assignments available for analysis"}
        
        # Calculate statistics
        total_assignments = len(assignments)
        completed_assignments = len([a for a in assignments if a.status == ContractStatus.COMPLETED])
        active_assignments = len([a for a in assignments if a.status in [ContractStatus.ASSIGNED, ContractStatus.IN_PROGRESS]])
        
        # Task type distribution
        task_type_counts = {}
        for assignment in assignments:
            task_type = assignment.task_type.value
            task_type_counts[task_type] = task_type_counts.get(task_type, 0) + 1
        
        # Priority distribution
        priority_counts = {}
        for assignment in assignments:
            priority = assignment.priority.value
            priority_counts[priority] = priority_counts.get(priority, 0) + 1
        
        # Agent performance
        agent_performance = {}
        for agent_id in set(a.agent_id for a in assignments):
            agent_assignments = [a for a in assignments if a.agent_id == agent_id]
            agent_performance[agent_id] = {
                "total_assignments": len(agent_assignments),
                "completed_assignments": len([a for a in agent_assignments if a.status == ContractStatus.COMPLETED]),
                "efficiency_score": self.calculate_agent_efficiency(agent_id)
            }
        
        return {
            "total_assignments": total_assignments,
            "completed_assignments": completed_assignments,
            "active_assignments": active_assignments,
            "completion_rate": completed_assignments / total_assignments if total_assignments > 0 else 0,
            "task_type_distribution": task_type_counts,
            "priority_distribution": priority_counts,
            "agent_performance": agent_performance,
            "total_agents": len(self.engine.agent_capabilities),
            "total_recommendations": len(self.engine.task_recommendations),
            "total_trends": len(self.engine.performance_trends),
            "total_optimizations": len(self.engine.optimization_results)
        }

    # ================================
    # PRIVATE HELPER METHODS
    # ================================
    
    def _get_available_tasks(self) -> List[Dict[str, Any]]:
        """Get available tasks from vector database or other sources."""
        # This would typically query the vector database or other task sources
        # For now, return empty list as placeholder
        return []


# ================================
# GLOBAL INSTANCE
# ================================

_global_vector_enhanced_contract_service = None

def get_vector_enhanced_contract_service(vector_db=None, lock_config=None) -> VectorEnhancedContractService:
    """Get global vector enhanced contract service instance."""
    global _global_vector_enhanced_contract_service
    if _global_vector_enhanced_contract_service is None:
        _global_vector_enhanced_contract_service = VectorEnhancedContractService(vector_db, lock_config)
    return _global_vector_enhanced_contract_service


# ================================
# CONVENIENCE FUNCTIONS
# ================================

def get_optimal_task_assignment(agent_id: str, available_tasks: List[Dict[str, Any]] = None) -> Optional[ContractAssignment]:
    """Convenience function to get optimal task assignment."""
    service = get_vector_enhanced_contract_service()
    return service.get_optimal_task_assignment(agent_id, available_tasks)

def track_contract_progress(assignment_id: str, progress_percentage: float, status: ContractStatus = None) -> bool:
    """Convenience function to track contract progress."""
    service = get_vector_enhanced_contract_service()
    return service.track_contract_progress(assignment_id, progress_percentage, status)

def analyze_performance_patterns(agent_id: str) -> List[PerformanceTrend]:
    """Convenience function to analyze performance patterns."""
    service = get_vector_enhanced_contract_service()
    return service.analyze_performance_patterns(agent_id)

def optimize_agent_assignments() -> List[OptimizationResult]:
    """Convenience function to optimize agent assignments."""
    service = get_vector_enhanced_contract_service()
    return service.optimize_agent_assignments()

def get_contract_recommendations(agent_id: str) -> List[TaskRecommendation]:
    """Convenience function to get contract recommendations."""
    service = get_vector_enhanced_contract_service()
    return service.get_contract_recommendations(agent_id)

def update_agent_capabilities(agent_id: str, capabilities: AgentCapability) -> bool:
    """Convenience function to update agent capabilities."""
    service = get_vector_enhanced_contract_service()
    return service.update_agent_capabilities(agent_id, capabilities)

def get_performance_metrics(agent_id: str = None) -> Dict[str, Any]:
    """Convenience function to get performance metrics."""
    service = get_vector_enhanced_contract_service()
    return service.get_performance_metrics(agent_id)

def get_contract_analytics() -> Dict[str, Any]:
    """Convenience function to get contract analytics."""
    service = get_vector_enhanced_contract_service()
    return service.get_contract_analytics()
