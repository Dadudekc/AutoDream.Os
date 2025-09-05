"""
Vector Enhanced Contracts Engine Services
========================================

Service functionality for vector enhanced contracts operations.
V2 Compliance: < 300 lines, single responsibility, service logic.

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
from .engine_core import VectorEnhancedContractsEngineCore


class VectorEnhancedContractsEngineServices:
    """Service functionality for vector enhanced contracts operations."""
    
    def __init__(self, engine_core: VectorEnhancedContractsEngineCore):
        """Initialize vector enhanced contracts engine services."""
        self.engine_core = engine_core
        self.is_initialized = False
    
    def initialize(self) -> bool:
        """Initialize the engine services."""
        try:
            if not self.engine_core.is_initialized:
                raise Exception("Engine core not initialized")
            
            self.is_initialized = True
            return True
        except Exception as e:
            return False
    
    def assign_task_to_agent(self, agent_id: str, task_type: TaskType, 
                           priority: PriorityLevel, description: str) -> ContractAssignment:
        """Assign a task to an agent."""
        if not self.is_initialized:
            raise RuntimeError("Engine services not initialized")
        
        return self.engine_core.create_contract(agent_id, task_type, priority, description)
    
    def get_next_task_for_agent(self, agent_id: str) -> Optional[ContractAssignment]:
        """Get the next available task for an agent."""
        if not self.is_initialized:
            raise RuntimeError("Engine services not initialized")
        
        # Get pending contracts for agent
        agent_contracts = self.engine_core.get_contracts_by_agent(agent_id)
        pending_contracts = [c for c in agent_contracts if c.status == ContractStatus.PENDING]
        
        if not pending_contracts:
            return None
        
        # Sort by priority and creation time
        pending_contracts.sort(key=lambda x: (x.priority.value, x.created_at))
        return pending_contracts[0]
    
    def complete_task(self, contract_id: str, completion_notes: str = "") -> bool:
        """Mark a task as completed."""
        if not self.is_initialized:
            raise RuntimeError("Engine services not initialized")
        
        contract = self.engine_core.get_contract(contract_id)
        if not contract:
            return False
        
        # Update contract status
        success = self.engine_core.update_contract_status(contract_id, ContractStatus.COMPLETED)
        if success:
            contract.completion_notes = completion_notes
            contract.completed_at = datetime.now()
        
        return success
    
    def get_agent_performance_summary(self, agent_id: str) -> Dict[str, Any]:
        """Get performance summary for an agent."""
        if not self.is_initialized:
            raise RuntimeError("Engine services not initialized")
        
        # Get agent contracts
        agent_contracts = self.engine_core.get_contracts_by_agent(agent_id)
        
        # Get performance metrics
        performance_metrics = self.engine_core.get_performance_metrics_by_agent(agent_id)
        
        # Calculate summary
        total_tasks = len(agent_contracts)
        completed_tasks = len([c for c in agent_contracts if c.status == ContractStatus.COMPLETED])
        pending_tasks = len([c for c in agent_contracts if c.status == ContractStatus.PENDING])
        
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        return {
            'agent_id': agent_id,
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'pending_tasks': pending_tasks,
            'completion_rate': completion_rate,
            'performance_metrics_count': len(performance_metrics)
        }
    
    def generate_task_recommendation(self, agent_id: str, task_type: TaskType, 
                                   priority: PriorityLevel, description: str) -> TaskRecommendation:
        """Generate a task recommendation."""
        if not self.is_initialized:
            raise RuntimeError("Engine services not initialized")
        
        recommendation_id = str(uuid.uuid4())
        recommendation = TaskRecommendation(
            recommendation_id=recommendation_id,
            agent_id=agent_id,
            task_type=task_type,
            priority=priority,
            description=description,
            confidence_score=0.8,  # Default confidence
            created_at=datetime.now()
        )
        
        self.engine_core.add_recommendation(recommendation)
        return recommendation
    
    def get_contract_statistics(self) -> Dict[str, Any]:
        """Get contract statistics."""
        if not self.is_initialized:
            raise RuntimeError("Engine services not initialized")
        
        all_contracts = list(self.engine_core.contracts.values())
        
        if not all_contracts:
            return {'message': 'No contracts found'}
        
        # Calculate statistics
        total_contracts = len(all_contracts)
        completed_contracts = len([c for c in all_contracts if c.status == ContractStatus.COMPLETED])
        pending_contracts = len([c for c in all_contracts if c.status == ContractStatus.PENDING])
        
        # Group by priority
        priority_counts = {}
        for contract in all_contracts:
            priority = contract.priority.value
            priority_counts[priority] = priority_counts.get(priority, 0) + 1
        
        # Group by task type
        task_type_counts = {}
        for contract in all_contracts:
            task_type = contract.task_type.value
            task_type_counts[task_type] = task_type_counts.get(task_type, 0) + 1
        
        return {
            'total_contracts': total_contracts,
            'completed_contracts': completed_contracts,
            'pending_contracts': pending_contracts,
            'completion_rate': (completed_contracts / total_contracts * 100) if total_contracts > 0 else 0,
            'priority_distribution': priority_counts,
            'task_type_distribution': task_type_counts
        }
    
    def get_services_status(self) -> Dict[str, Any]:
        """Get services status."""
        if not self.is_initialized:
            return {'status': 'not_initialized'}
        
        return {
            'status': 'initialized',
            'engine_core_initialized': self.engine_core.is_initialized,
            'services_type': 'vector_enhanced_contracts'
        }
    
    def shutdown(self):
        """Shutdown engine services."""
        if not self.is_initialized:
            return
        
        self.is_initialized = False
