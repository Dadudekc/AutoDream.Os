"""
ML Learning Orchestrator Core
=============================

Core orchestration logic for ML learning operations.
V2 Compliance: < 300 lines, single responsibility, core orchestration logic.

Author: Agent-3 - Infrastructure & DevOps Specialist
Mission: V2 Compliance Refactoring
"""

import asyncio
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
from .coordinator import MLLearningCoordinator


class MLLearningOrchestratorCore:
    """Core orchestration logic for ML learning operations."""
    
    def __init__(self):
        """Initialize ML learning orchestrator core."""
        self.logger = logging.getLogger(__name__)
        self.is_initialized = False
        self.engine: Optional[MLLearningEngine] = None
        self.coordinator: Optional[MLLearningCoordinator] = None
        self.active_sessions: Dict[str, LearningSession] = {}
        self.session_metrics: Dict[str, MLOptimizationMetrics] = {}
    
    def initialize(self) -> bool:
        """Initialize the orchestrator core."""
        try:
            # Initialize engine
            self.engine = MLLearningEngine()
            if not self.engine.initialize():
                raise Exception("Failed to initialize ML learning engine")
            
            # Initialize coordinator
            self.coordinator = MLLearningCoordinator(self.engine)
            if not self.coordinator.initialize():
                raise Exception("Failed to initialize ML learning coordinator")
            
            self.is_initialized = True
            self.logger.info("ML Learning Orchestrator Core initialized")
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize ML Learning Orchestrator Core: {e}")
            return False
    
    def start_learning_session(self, session_id: str, model_type: ModelType, 
                             configuration: MLConfiguration) -> bool:
        """Start a new learning session."""
        try:
            if not self.is_initialized:
                raise RuntimeError("Orchestrator core not initialized")
            
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
            
            # Start session in coordinator
            if self.coordinator:
                self.coordinator.start_learning_session(session_id, model_type, configuration)
            
            self.logger.info(f"Started learning session: {session_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error starting learning session: {e}")
            return False
    
    def stop_learning_session(self, session_id: str) -> bool:
        """Stop a learning session."""
        try:
            if not self.is_initialized:
                raise RuntimeError("Orchestrator core not initialized")
            
            if session_id not in self.active_sessions:
                self.logger.warning(f"Session {session_id} not found")
                return False
            
            session = self.active_sessions[session_id]
            session.status = LearningStatus.COMPLETED
            session.completed_at = datetime.now()
            
            # Stop session in coordinator
            if self.coordinator:
                self.coordinator.stop_learning_session(session_id)
            
            del self.active_sessions[session_id]
            self.logger.info(f"Stopped learning session: {session_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error stopping learning session: {e}")
            return False
    
    def get_learning_session(self, session_id: str) -> Optional[LearningSession]:
        """Get a learning session."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator core not initialized")
        
        return self.active_sessions.get(session_id)
    
    def get_active_sessions(self) -> List[LearningSession]:
        """Get all active learning sessions."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator core not initialized")
        
        return list(self.active_sessions.values())
    
    def add_session_metrics(self, session_id: str, metrics: MLOptimizationMetrics) -> bool:
        """Add metrics for a session."""
        try:
            if not self.is_initialized:
                raise RuntimeError("Orchestrator core not initialized")
            
            self.session_metrics[f"{session_id}_{metrics.metrics_id}"] = metrics
            self.logger.debug(f"Added metrics for session {session_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error adding session metrics: {e}")
            return False
    
    def get_session_metrics(self, session_id: str) -> List[MLOptimizationMetrics]:
        """Get metrics for a session."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator core not initialized")
        
        return [
            metrics for key, metrics in self.session_metrics.items()
            if key.startswith(f"{session_id}_")
        ]
    
    def get_core_status(self) -> Dict[str, Any]:
        """Get orchestrator core status."""
        if not self.is_initialized:
            return {'status': 'not_initialized'}
        
        return {
            'status': 'initialized',
            'active_sessions_count': len(self.active_sessions),
            'session_metrics_count': len(self.session_metrics),
            'engine_initialized': self.engine.is_initialized if self.engine else False,
            'coordinator_initialized': self.coordinator.is_initialized if self.coordinator else False
        }
    
    def shutdown(self):
        """Shutdown orchestrator core."""
        if not self.is_initialized:
            return
        
        self.logger.info("Shutting down ML Learning Orchestrator Core")
        
        # Stop all active sessions
        for session_id in list(self.active_sessions.keys()):
            self.stop_learning_session(session_id)
        
        # Shutdown components
        if self.coordinator:
            self.coordinator.shutdown()
        if self.engine:
            self.engine.shutdown()
        
        self.is_initialized = False
