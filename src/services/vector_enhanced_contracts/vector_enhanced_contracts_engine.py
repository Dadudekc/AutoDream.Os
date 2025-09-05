#!/usr/bin/env python3
"""
Vector Enhanced Contracts Engine - V2 Compliant Redirect
========================================================

V2 compliance redirect to modular vector enhanced contracts engine.
Original monolithic implementation refactored into focused modules.

Author: Agent-3 - Infrastructure & DevOps Specialist (V2 Refactoring)
Created: 2025-01-28
Purpose: V2 compliant modular vector enhanced contracts engine
"""

# V2 COMPLIANCE REDIRECT - Import from modular system
from .engine_core import VectorEnhancedContractsEngineCore
from .engine_services import VectorEnhancedContractsEngineServices

# Backward compatibility - create main engine class
class VectorEnhancedContractsEngine:
    """Main vector enhanced contracts engine - V2 compliant wrapper."""
    
    def __init__(self):
        """Initialize vector enhanced contracts engine."""
        self.core = VectorEnhancedContractsEngineCore()
        self.services = VectorEnhancedContractsEngineServices(self.core)
        self.is_initialized = False
    
    def initialize(self) -> bool:
        """Initialize the engine."""
        try:
            if not self.core.initialize():
                return False
            if not self.services.initialize():
                return False
            
            self.is_initialized = True
            return True
        except Exception as e:
            return False
    
    # Delegate core methods
    def create_contract(self, agent_id, task_type, priority, description):
        return self.core.create_contract(agent_id, task_type, priority, description)
    
    def get_contract(self, contract_id):
        return self.core.get_contract(contract_id)
    
    def update_contract_status(self, contract_id, status):
        return self.core.update_contract_status(contract_id, status)
    
    def get_contracts_by_agent(self, agent_id):
        return self.core.get_contracts_by_agent(agent_id)
    
    def get_contracts_by_status(self, status):
        return self.core.get_contracts_by_status(status)
    
    def add_recommendation(self, recommendation):
        return self.core.add_recommendation(recommendation)
    
    def get_recommendation(self, recommendation_id):
        return self.core.get_recommendation(recommendation_id)
    
    def get_recommendations_by_agent(self, agent_id):
        return self.core.get_recommendations_by_agent(agent_id)
    
    def add_performance_metrics(self, metrics):
        return self.core.add_performance_metrics(metrics)
    
    def get_performance_metrics(self, metrics_id):
        return self.core.get_performance_metrics(metrics_id)
    
    def get_performance_metrics_by_agent(self, agent_id):
        return self.core.get_performance_metrics_by_agent(agent_id)
    
    def add_agent_capability(self, capability):
        return self.core.add_agent_capability(capability)
    
    def get_agent_capability(self, capability_id):
        return self.core.get_agent_capability(capability_id)
    
    def get_agent_capabilities_by_agent(self, agent_id):
        return self.core.get_agent_capabilities_by_agent(agent_id)
    
    def add_optimization_result(self, result):
        return self.core.add_optimization_result(result)
    
    def get_optimization_result(self, result_id):
        return self.core.get_optimization_result(result_id)
    
    # Delegate service methods
    def assign_task_to_agent(self, agent_id, task_type, priority, description):
        return self.services.assign_task_to_agent(agent_id, task_type, priority, description)
    
    def get_next_task_for_agent(self, agent_id):
        return self.services.get_next_task_for_agent(agent_id)
    
    def complete_task(self, contract_id, completion_notes=""):
        return self.services.complete_task(contract_id, completion_notes)
    
    def get_agent_performance_summary(self, agent_id):
        return self.services.get_agent_performance_summary(agent_id)
    
    def generate_task_recommendation(self, agent_id, task_type, priority, description):
        return self.services.generate_task_recommendation(agent_id, task_type, priority, description)
    
    def get_contract_statistics(self):
        return self.services.get_contract_statistics()
    
    def get_engine_status(self):
        return self.core.get_core_status()
    
    def shutdown(self):
        """Shutdown engine."""
        if not self.is_initialized:
            return
        
        self.services.shutdown()
        self.core.shutdown()
        self.is_initialized = False

# Re-export for backward compatibility
__all__ = [
    'VectorEnhancedContractsEngine',
    'VectorEnhancedContractsEngineCore',
    'VectorEnhancedContractsEngineServices'
]