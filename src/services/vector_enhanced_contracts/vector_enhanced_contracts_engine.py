#!/usr/bin/env python3
"""
Vector Enhanced Contracts Engine - V2 Compliance Module
======================================================

Core business logic for vector enhanced contracts operations.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

import time
import uuid
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta

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


class VectorEnhancedContractEngine:
    """Core engine for vector enhanced contracts operations."""

    def __init__(self):
        """Initialize vector enhanced contract engine."""
        self.contract_assignments: Dict[str, ContractAssignment] = {}
        self.agent_capabilities: Dict[str, AgentCapability] = {}
        self.performance_metrics: Dict[str, PerformanceMetrics] = {}
        self.task_recommendations: List[TaskRecommendation] = []
        self.performance_trends: List[PerformanceTrend] = []
        self.optimization_results: List[OptimizationResult] = []

    # ================================
    # CORE CONTRACT OPERATIONS
    # ================================
    
    def get_optimal_task_assignment(self, agent_id: str, available_tasks: List[Dict[str, Any]]) -> Optional[ContractAssignment]:
        """Get optimal task assignment for agent."""
        start_time = time.time()
        
        try:
            agent_capability = self.agent_capabilities.get(agent_id)
            if not agent_capability or not agent_capability.availability:
                return None
            
            # Find best matching task
            best_task = self._find_best_matching_task(agent_capability, available_tasks)
            if not best_task:
                return None
            
            # Create assignment
            assignment = ContractAssignment(
                assignment_id=str(uuid.uuid4()),
                contract_id=best_task.get("contract_id", ""),
                agent_id=agent_id,
                task_type=TaskType(best_task.get("task_type", "refactoring")),
                priority=PriorityLevel(best_task.get("priority", "medium")),
                status=ContractStatus.ASSIGNED,
                estimated_duration=best_task.get("estimated_duration", 0.0),
                metadata=best_task.get("metadata", {})
            )
            
            self.contract_assignments[assignment.assignment_id] = assignment
            execution_time = (time.time() - start_time) * 1000
            
            return assignment
            
        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            return None

    def track_contract_progress(self, assignment_id: str, progress_percentage: float, status: ContractStatus = None) -> bool:
        """Track contract progress."""
        try:
            assignment = self.contract_assignments.get(assignment_id)
            if not assignment:
                return False
            
            assignment.progress_percentage = progress_percentage
            if status:
                assignment.status = status
            
            if progress_percentage >= 100.0:
                assignment.status = ContractStatus.COMPLETED
                assignment.completed_at = datetime.now()
                if assignment.assigned_at:
                    assignment.actual_duration = (assignment.completed_at - assignment.assigned_at).total_seconds() / 3600
            
            return True
        except Exception:
            return False

    def analyze_performance_patterns(self, agent_id: str) -> List[PerformanceTrend]:
        """Analyze performance patterns for agent."""
        try:
            agent_assignments = [a for a in self.contract_assignments.values() if a.agent_id == agent_id]
            if not agent_assignments:
                return []
            
            # Analyze completion times
            completion_times = [a.actual_duration for a in agent_assignments if a.actual_duration is not None]
            if len(completion_times) < 2:
                return []
            
            # Calculate trend
            avg_early = sum(completion_times[:len(completion_times)//2]) / (len(completion_times)//2)
            avg_late = sum(completion_times[len(completion_times)//2:]) / (len(completion_times) - len(completion_times)//2)
            
            trend_direction = "improving" if avg_late < avg_early else "declining" if avg_late > avg_early else "stable"
            trend_strength = abs(avg_late - avg_early) / max(avg_early, avg_late, 0.1)
            
            trend = PerformanceTrend(
                agent_id=agent_id,
                trend_type="completion_time",
                trend_direction=trend_direction,
                trend_strength=min(trend_strength, 1.0),
                key_factors=["task_complexity", "agent_experience", "resource_availability"],
                recommendations=self._generate_trend_recommendations(trend_direction),
                confidence=0.8
            )
            
            self.performance_trends.append(trend)
            return [trend]
            
        except Exception:
            return []

    def optimize_agent_assignments(self) -> List[OptimizationResult]:
        """Optimize agent assignments."""
        try:
            # Analyze current assignment distribution
            agent_loads = {}
            for assignment in self.contract_assignments.values():
                if assignment.status in [ContractStatus.ASSIGNED, ContractStatus.IN_PROGRESS]:
                    agent_loads[assignment.agent_id] = agent_loads.get(assignment.agent_id, 0) + 1
            
            if not agent_loads:
                return []
            
            # Calculate load balance
            loads = list(agent_loads.values())
            avg_load = sum(loads) / len(loads)
            load_variance = sum((load - avg_load) ** 2 for load in loads) / len(loads)
            
            # Generate optimization recommendations
            recommendations = []
            if load_variance > avg_load * 0.5:  # High variance
                recommendations.append("Implement load balancing across agents")
                recommendations.append("Redistribute tasks based on agent capabilities")
            
            optimization = OptimizationResult(
                optimization_id=str(uuid.uuid4()),
                optimization_type="load_balancing",
                before_metrics={"load_variance": load_variance, "average_load": avg_load},
                after_metrics={"target_variance": avg_load * 0.2, "target_load": avg_load},
                improvement_percentage=min((load_variance - avg_load * 0.2) / load_variance * 100, 50),
                recommendations=recommendations,
                implementation_effort="medium",
                expected_impact="high"
            )
            
            self.optimization_results.append(optimization)
            return [optimization]
            
        except Exception:
            return []

    def get_contract_recommendations(self, agent_id: str) -> List[TaskRecommendation]:
        """Get contract recommendations for agent."""
        try:
            agent_capability = self.agent_capabilities.get(agent_id)
            if not agent_capability:
                return []
            
            recommendations = []
            
            # Generate recommendations based on agent capabilities
            for task_type in agent_capability.preferred_task_types:
                recommendation = TaskRecommendation(
                    recommendation_id=str(uuid.uuid4()),
                    agent_id=agent_id,
                    task_type=task_type,
                    priority=PriorityLevel.MEDIUM,
                    confidence_score=agent_capability.performance_score,
                    reasoning=f"Agent has expertise in {task_type.value} tasks",
                    expected_duration=self._estimate_task_duration(task_type),
                    required_capabilities=agent_capability.capabilities
                )
                recommendations.append(recommendation)
            
            self.task_recommendations.extend(recommendations)
            return recommendations
            
        except Exception:
            return []

    def update_agent_capabilities(self, agent_id: str, capabilities: AgentCapability) -> bool:
        """Update agent capabilities."""
        try:
            capabilities.last_updated = datetime.now()
            self.agent_capabilities[agent_id] = capabilities
            return True
        except Exception:
            return False

    def get_performance_metrics(self, agent_id: str = None) -> Dict[str, Any]:
        """Get performance metrics."""
        if agent_id:
            metrics = self.performance_metrics.get(agent_id)
            return metrics.to_dict() if metrics else {}
        
        return {
            "total_agents": len(self.agent_capabilities),
            "total_assignments": len(self.contract_assignments),
            "active_assignments": len([a for a in self.contract_assignments.values() if a.status in [ContractStatus.ASSIGNED, ContractStatus.IN_PROGRESS]]),
            "completed_assignments": len([a for a in self.contract_assignments.values() if a.status == ContractStatus.COMPLETED]),
            "total_recommendations": len(self.task_recommendations),
            "total_trends": len(self.performance_trends),
            "total_optimizations": len(self.optimization_results)
        }

    # ================================
    # PRIVATE HELPER METHODS
    # ================================
    
    def _find_best_matching_task(self, agent_capability: AgentCapability, available_tasks: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Find best matching task for agent."""
        if not available_tasks:
            return None
        
        best_task = None
        best_score = 0.0
        
        for task in available_tasks:
            score = self._calculate_task_match_score(agent_capability, task)
            if score > best_score:
                best_score = score
                best_task = task
        
        return best_task if best_score > 0.5 else None

    def _calculate_task_match_score(self, agent_capability: AgentCapability, task: Dict[str, Any]) -> float:
        """Calculate task match score for agent."""
        score = 0.0
        
        # Check task type preference
        task_type = task.get("task_type", "refactoring")
        if TaskType(task_type) in agent_capability.preferred_task_types:
            score += 0.4
        
        # Check capability match
        required_capabilities = task.get("required_capabilities", [])
        if required_capabilities:
            capability_match = len(set(required_capabilities) & set(agent_capability.capabilities)) / len(required_capabilities)
            score += capability_match * 0.4
        
        # Check current load
        if agent_capability.current_load < 0.8:  # Not overloaded
            score += 0.2
        
        return score

    def _estimate_task_duration(self, task_type: TaskType) -> float:
        """Estimate task duration based on type."""
        duration_map = {
            TaskType.REFACTORING: 4.0,
            TaskType.TESTING: 2.0,
            TaskType.DOCUMENTATION: 1.5,
            TaskType.OPTIMIZATION: 3.0,
            TaskType.INTEGRATION: 5.0,
            TaskType.DEBUGGING: 2.5,
            TaskType.FEATURE_DEVELOPMENT: 6.0,
            TaskType.MAINTENANCE: 1.0
        }
        return duration_map.get(task_type, 2.0)

    def _generate_trend_recommendations(self, trend_direction: str) -> List[str]:
        """Generate recommendations based on trend direction."""
        if trend_direction == "improving":
            return ["Continue current practices", "Share successful strategies with team"]
        elif trend_direction == "declining":
            return ["Review recent changes", "Consider additional training", "Adjust workload"]
        else:
            return ["Maintain current performance level", "Look for optimization opportunities"]
