#!/usr/bin/env python3
"""
ML Learning Orchestrator - V2 Compliant Redirect
================================================

V2 compliance redirect to modular ML learning orchestrator.
Original monolithic implementation refactored into focused modules.

Author: Agent-3 - Infrastructure & DevOps Specialist (V2 Refactoring)
Created: 2025-01-28
Purpose: V2 compliant modular ML learning orchestrator
"""

# V2 COMPLIANCE REDIRECT - Import from modular system
from .orchestrator_core import MLLearningOrchestratorCore
from .orchestrator_services import MLLearningOrchestratorServices

# Backward compatibility - create main orchestrator class
class MLLearningEngineOrchestrator:
    """Main ML learning engine orchestrator - V2 compliant wrapper."""
    
    def __init__(self):
        """Initialize ML learning engine orchestrator."""
        self.core = MLLearningOrchestratorCore()
        self.services = MLLearningOrchestratorServices(self.core)
        self.is_initialized = False
    
    def initialize(self) -> bool:
        """Initialize the orchestrator."""
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
    def start_learning_session(self, session_id, model_type, configuration):
        return self.core.start_learning_session(session_id, model_type, configuration)
    
    def stop_learning_session(self, session_id):
        return self.core.stop_learning_session(session_id)
    
    def get_learning_session(self, session_id):
        return self.core.get_learning_session(session_id)
    
    def get_active_sessions(self):
        return self.core.get_active_sessions()
    
    def add_session_metrics(self, session_id, metrics):
        return self.core.add_session_metrics(session_id, metrics)
    
    def get_session_metrics(self, session_id):
        return self.core.get_session_metrics(session_id)
    
    # Delegate service methods
    async def make_prediction(self, session_id, input_data):
        return await self.services.make_prediction(session_id, input_data)
    
    async def get_predictions(self, model_id=None):
        return await self.services.get_predictions(model_id)
    
    async def train_model(self, session_id, training_data):
        return await self.services.train_model(session_id, training_data)
    
    async def analyze_features(self, session_id, features):
        return await self.services.analyze_features(session_id, features)
    
    async def get_session_performance(self, session_id):
        return await self.services.get_session_performance(session_id)
    
    async def generate_learning_report(self, session_id=None):
        return await self.services.generate_learning_report(session_id)
    
    def get_orchestrator_status(self):
        return self.core.get_core_status()
    
    def shutdown(self):
        """Shutdown orchestrator."""
        if not self.is_initialized:
            return
        
        self.services.shutdown()
        self.core.shutdown()
        self.is_initialized = False

# Re-export for backward compatibility
__all__ = [
    'MLLearningEngineOrchestrator',
    'MLLearningOrchestratorCore',
    'MLLearningOrchestratorServices'
]