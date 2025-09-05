#!/usr/bin/env python3
"""
ML Learning Coordinator - V2 Compliant Redirect
==============================================

V2 compliance redirect to modular ML learning coordinator.
Original monolithic implementation refactored into focused modules.

Author: Agent-3 - Infrastructure & DevOps Specialist (V2 Refactoring)
Created: 2025-01-28
Purpose: V2 compliant modular ML learning coordinator
"""

# V2 COMPLIANCE REDIRECT - Import from modular system
from .coordinator_core import MLLearningCoordinatorCore
from .coordinator_services import MLLearningCoordinatorServices

# Backward compatibility - create main coordinator class
class MLLearningCoordinator:
    """Main ML learning coordinator - V2 compliant wrapper."""
    
    def __init__(self, engine):
        """Initialize ML learning coordinator."""
        self.core = MLLearningCoordinatorCore(engine)
        self.services = MLLearningCoordinatorServices(self.core)
        self.is_initialized = False
    
    def initialize(self) -> bool:
        """Initialize the coordinator."""
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
    
    def add_learning_pattern(self, pattern):
        return self.core.add_learning_pattern(pattern)
    
    def get_learning_pattern(self, pattern_id):
        return self.core.get_learning_pattern(pattern_id)
    
    def get_learning_patterns_by_type(self, pattern_type):
        return self.core.get_learning_patterns_by_type(pattern_type)
    
    def add_model_state(self, state):
        return self.core.add_model_state(state)
    
    def get_model_state(self, state_id):
        return self.core.get_model_state(state_id)
    
    def get_model_states_by_session(self, session_id):
        return self.core.get_model_states_by_session(session_id)
    
    def add_optimization_metrics(self, metrics):
        return self.core.add_optimization_metrics(metrics)
    
    def get_optimization_metrics(self, metrics_id):
        return self.core.get_optimization_metrics(metrics_id)
    
    def get_optimization_metrics_by_session(self, session_id):
        return self.core.get_optimization_metrics_by_session(session_id)
    
    # Delegate service methods
    def analyze_learning_progress(self, session_id):
        return self.services.analyze_learning_progress(session_id)
    
    def generate_learning_report(self, session_id=None):
        return self.services.generate_learning_report(session_id)
    
    def optimize_learning_parameters(self, session_id):
        return self.services.optimize_learning_parameters(session_id)
    
    def monitor_learning_health(self):
        return self.services.monitor_learning_health()
    
    def get_coordinator_status(self):
        return self.core.get_core_status()
    
    def shutdown(self):
        """Shutdown coordinator."""
        if not self.is_initialized:
            return
        
        self.services.shutdown()
        self.core.shutdown()
        self.is_initialized = False

# Re-export for backward compatibility
__all__ = [
    'MLLearningCoordinator',
    'MLLearningCoordinatorCore',
    'MLLearningCoordinatorServices'
]