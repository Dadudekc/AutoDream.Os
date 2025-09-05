"""
Vector Enhanced Contracts Engine Core
====================================

Core business logic for vector enhanced contracts operations.
V2 Compliance: < 300 lines, single responsibility, core engine logic.

Author: Agent-3 - Infrastructure & DevOps Specialist
Mission: V2 Compliance Refactoring
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


class VectorEnhancedContractsEngineCore:
    """Core business logic for vector enhanced contracts operations."""
    
    def __init__(self):
        """Initialize vector enhanced contracts engine core."""
        self.contracts: Dict[str, ContractAssignment] = {}
        self.recommendations: Dict[str, TaskRecommendation] = {}
        self.performance_metrics: Dict[str, PerformanceMetrics] = {}
        self.agent_capabilities: Dict[str, AgentCapability] = {}
        self.optimization_results: Dict[str, OptimizationResult] = {}
        self.is_initialized = False
    
    def initialize(self) -> bool:
        """Initialize the engine core."""
        try:
            self.is_initialized = True
            return True
        except Exception as e:
            return False
    
    def create_contract(self, agent_id: str, task_type: TaskType, 
                       priority: PriorityLevel, description: str) -> ContractAssignment:
        """Create a new contract assignment."""
        contract_id = str(uuid.uuid4())
        contract = ContractAssignment(
            contract_id=contract_id,
            agent_id=agent_id,
            task_type=task_type,
            priority=priority,
            description=description,
            status=ContractStatus.PENDING,
            created_at=datetime.now()
        )
        self.contracts[contract_id] = contract
        return contract
    
    def get_contract(self, contract_id: str) -> Optional[ContractAssignment]:
        """Get a contract by ID."""
        return self.contracts.get(contract_id)
    
    def update_contract_status(self, contract_id: str, status: ContractStatus) -> bool:
        """Update contract status."""
        if contract_id in self.contracts:
            self.contracts[contract_id].status = status
            self.contracts[contract_id].updated_at = datetime.now()
            return True
        return False
    
    def get_contracts_by_agent(self, agent_id: str) -> List[ContractAssignment]:
        """Get all contracts for an agent."""
        return [c for c in self.contracts.values() if c.agent_id == agent_id]
    
    def get_contracts_by_status(self, status: ContractStatus) -> List[ContractAssignment]:
        """Get all contracts by status."""
        return [c for c in self.contracts.values() if c.status == status]
    
    def add_recommendation(self, recommendation: TaskRecommendation) -> bool:
        """Add a task recommendation."""
        self.recommendations[recommendation.recommendation_id] = recommendation
        return True
    
    def get_recommendation(self, recommendation_id: str) -> Optional[TaskRecommendation]:
        """Get a recommendation by ID."""
        return self.recommendations.get(recommendation_id)
    
    def get_recommendations_by_agent(self, agent_id: str) -> List[TaskRecommendation]:
        """Get recommendations for an agent."""
        return [r for r in self.recommendations.values() if r.agent_id == agent_id]
    
    def add_performance_metrics(self, metrics: PerformanceMetrics) -> bool:
        """Add performance metrics."""
        self.performance_metrics[metrics.metrics_id] = metrics
        return True
    
    def get_performance_metrics(self, metrics_id: str) -> Optional[PerformanceMetrics]:
        """Get performance metrics by ID."""
        return self.performance_metrics.get(metrics_id)
    
    def get_performance_metrics_by_agent(self, agent_id: str) -> List[PerformanceMetrics]:
        """Get performance metrics for an agent."""
        return [m for m in self.performance_metrics.values() if m.agent_id == agent_id]
    
    def add_agent_capability(self, capability: AgentCapability) -> bool:
        """Add agent capability."""
        self.agent_capabilities[capability.capability_id] = capability
        return True
    
    def get_agent_capability(self, capability_id: str) -> Optional[AgentCapability]:
        """Get agent capability by ID."""
        return self.agent_capabilities.get(capability_id)
    
    def get_agent_capabilities_by_agent(self, agent_id: str) -> List[AgentCapability]:
        """Get capabilities for an agent."""
        return [c for c in self.agent_capabilities.values() if c.agent_id == agent_id]
    
    def add_optimization_result(self, result: OptimizationResult) -> bool:
        """Add optimization result."""
        self.optimization_results[result.result_id] = result
        return True
    
    def get_optimization_result(self, result_id: str) -> Optional[OptimizationResult]:
        """Get optimization result by ID."""
        return self.optimization_results.get(result_id)
    
    def get_core_status(self) -> Dict[str, Any]:
        """Get engine core status."""
        if not self.is_initialized:
            return {'status': 'not_initialized'}
        
        return {
            'status': 'initialized',
            'contracts_count': len(self.contracts),
            'recommendations_count': len(self.recommendations),
            'performance_metrics_count': len(self.performance_metrics),
            'agent_capabilities_count': len(self.agent_capabilities),
            'optimization_results_count': len(self.optimization_results)
        }
    
    def shutdown(self):
        """Shutdown engine core."""
        if not self.is_initialized:
            return
        
        self.is_initialized = False
