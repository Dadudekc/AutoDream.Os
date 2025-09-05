"""
ML Learning Coordinator Core
===========================

Core coordination logic for ML learning operations.
V2 Compliance: < 300 lines, single responsibility, core coordination logic.

Author: Agent-3 - Infrastructure & DevOps Specialist
Mission: V2 Compliance Refactoring
"""

import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from .models import (
    LearningPattern, MLPrediction, ModelState, MLOptimizationMetrics,
    FeatureAnalysis, LearningSession,
    LearningStatus, ModelType, FeatureType
)
from ...ml_optimizer_models import MLConfiguration
from .engine import MLLearningEngine


class MLLearningCoordinatorCore:
    """Core ML learning coordination logic."""
    
    def __init__(self, engine: MLLearningEngine):
        """Initialize ML learning coordinator core."""
        self.engine = engine
        self.logger = logging.getLogger(__name__)
        self.is_initialized = False
        self.active_sessions: Dict[str, LearningSession] = {}
        self.learning_patterns: Dict[str, LearningPattern] = {}
        self.model_states: Dict[str, ModelState] = {}
        self.optimization_metrics: Dict[str, MLOptimizationMetrics] = {}
    
    def initialize(self) -> bool:
        """Initialize the coordinator core."""
        try:
            if not self.engine.is_initialized:
                raise Exception("Engine not initialized")
            
            self.is_initialized = True
            self.logger.info("ML Learning Coordinator Core initialized")
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize ML Learning Coordinator Core: {e}")
            return False
    
    def start_learning_session(self, session_id: str, model_type: ModelType, 
                             configuration: MLConfiguration) -> bool:
        """Start a new learning session."""
        try:
            if not self.is_initialized:
                raise RuntimeError("Coordinator core not initialized")
            
            if session_id in self.active_sessions:
                self.logger.warning(f"Session {session_id} already exists")
                return False
            
            # Create learning session
            session = LearningSession(
                session_id=session_id,
                model_type=model_type,
                configuration=configuration,
                status=LearningStatus.ACTIVE,
                created_at=datetime.now()
            )
            
            self.active_sessions[session_id] = session
            self.logger.info(f"Started learning session: {session_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error starting learning session: {e}")
            return False
    
    def stop_learning_session(self, session_id: str) -> bool:
        """Stop a learning session."""
        try:
            if not self.is_initialized:
                raise RuntimeError("Coordinator core not initialized")
            
            if session_id not in self.active_sessions:
                self.logger.warning(f"Session {session_id} not found")
                return False
            
            session = self.active_sessions[session_id]
            session.status = LearningStatus.COMPLETED
            session.completed_at = datetime.now()
            
            del self.active_sessions[session_id]
            self.logger.info(f"Stopped learning session: {session_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error stopping learning session: {e}")
            return False
    
    def get_learning_session(self, session_id: str) -> Optional[LearningSession]:
        """Get a learning session."""
        if not self.is_initialized:
            raise RuntimeError("Coordinator core not initialized")
        
        return self.active_sessions.get(session_id)
    
    def get_active_sessions(self) -> List[LearningSession]:
        """Get all active learning sessions."""
        if not self.is_initialized:
            raise RuntimeError("Coordinator core not initialized")
        
        return list(self.active_sessions.values())
    
    def add_learning_pattern(self, pattern: LearningPattern) -> bool:
        """Add a learning pattern."""
        try:
            if not self.is_initialized:
                raise RuntimeError("Coordinator core not initialized")
            
            self.learning_patterns[pattern.pattern_id] = pattern
            self.logger.debug(f"Added learning pattern: {pattern.pattern_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error adding learning pattern: {e}")
            return False
    
    def get_learning_pattern(self, pattern_id: str) -> Optional[LearningPattern]:
        """Get a learning pattern."""
        if not self.is_initialized:
            raise RuntimeError("Coordinator core not initialized")
        
        return self.learning_patterns.get(pattern_id)
    
    def get_learning_patterns_by_type(self, pattern_type: str) -> List[LearningPattern]:
        """Get learning patterns by type."""
        if not self.is_initialized:
            raise RuntimeError("Coordinator core not initialized")
        
        return [
            pattern for pattern in self.learning_patterns.values()
            if pattern.pattern_type == pattern_type
        ]
    
    def add_model_state(self, state: ModelState) -> bool:
        """Add a model state."""
        try:
            if not self.is_initialized:
                raise RuntimeError("Coordinator core not initialized")
            
            self.model_states[state.state_id] = state
            self.logger.debug(f"Added model state: {state.state_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error adding model state: {e}")
            return False
    
    def get_model_state(self, state_id: str) -> Optional[ModelState]:
        """Get a model state."""
        if not self.is_initialized:
            raise RuntimeError("Coordinator core not initialized")
        
        return self.model_states.get(state_id)
    
    def get_model_states_by_session(self, session_id: str) -> List[ModelState]:
        """Get model states by session."""
        if not self.is_initialized:
            raise RuntimeError("Coordinator core not initialized")
        
        return [
            state for state in self.model_states.values()
            if state.session_id == session_id
        ]
    
    def add_optimization_metrics(self, metrics: MLOptimizationMetrics) -> bool:
        """Add optimization metrics."""
        try:
            if not self.is_initialized:
                raise RuntimeError("Coordinator core not initialized")
            
            self.optimization_metrics[metrics.metrics_id] = metrics
            self.logger.debug(f"Added optimization metrics: {metrics.metrics_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error adding optimization metrics: {e}")
            return False
    
    def get_optimization_metrics(self, metrics_id: str) -> Optional[MLOptimizationMetrics]:
        """Get optimization metrics."""
        if not self.is_initialized:
            raise RuntimeError("Coordinator core not initialized")
        
        return self.optimization_metrics.get(metrics_id)
    
    def get_optimization_metrics_by_session(self, session_id: str) -> List[MLOptimizationMetrics]:
        """Get optimization metrics by session."""
        if not self.is_initialized:
            raise RuntimeError("Coordinator core not initialized")
        
        return [
            metrics for metrics in self.optimization_metrics.values()
            if metrics.session_id == session_id
        ]
    
    def get_core_status(self) -> Dict[str, Any]:
        """Get coordinator core status."""
        if not self.is_initialized:
            return {'status': 'not_initialized'}
        
        return {
            'status': 'initialized',
            'active_sessions_count': len(self.active_sessions),
            'learning_patterns_count': len(self.learning_patterns),
            'model_states_count': len(self.model_states),
            'optimization_metrics_count': len(self.optimization_metrics)
        }
    
    def shutdown(self):
        """Shutdown coordinator core."""
        if not self.is_initialized:
            return
        
        self.logger.info("Shutting down ML Learning Coordinator Core")
        self.is_initialized = False
