"""
ML Learning Orchestrator Services
=================================

Service functionality for ML learning orchestration operations.
V2 Compliance: < 300 lines, single responsibility, service logic.

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
from .orchestrator_core import MLLearningOrchestratorCore


class MLLearningOrchestratorServices:
    """Service functionality for ML learning orchestration operations."""
    
    def __init__(self, orchestrator_core: MLLearningOrchestratorCore):
        """Initialize ML learning orchestrator services."""
        self.orchestrator_core = orchestrator_core
        self.logger = logging.getLogger(__name__)
        self.is_initialized = False
    
    def initialize(self) -> bool:
        """Initialize the orchestrator services."""
        try:
            if not self.orchestrator_core.is_initialized:
                raise Exception("Orchestrator core not initialized")
            
            self.is_initialized = True
            self.logger.info("ML Learning Orchestrator Services initialized")
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize ML Learning Orchestrator Services: {e}")
            return False
    
    async def make_prediction(self, session_id: str, input_data: Dict[str, Any]) -> Optional[MLPrediction]:
        """Make a prediction using a session's model."""
        try:
            if not self.is_initialized:
                raise RuntimeError("Orchestrator services not initialized")
            
            session = self.orchestrator_core.get_learning_session(session_id)
            if not session:
                self.logger.warning(f"Session {session_id} not found")
                return None
            
            # Use engine for prediction
            if self.orchestrator_core.engine:
                prediction = self.orchestrator_core.engine.predict(session_id, input_data)
                if prediction:
                    self.logger.info(f"Made prediction for session {session_id}")
                return prediction
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error making prediction: {e}")
            return None
    
    async def get_predictions(self, model_id: str = None) -> List[MLPrediction]:
        """Get predictions for a model or all models."""
        try:
            if not self.is_initialized:
                raise RuntimeError("Orchestrator services not initialized")
            
            if self.orchestrator_core.engine:
                if model_id:
                    return self.orchestrator_core.engine.get_predictions_by_model(model_id)
                else:
                    # Get all predictions (simplified)
                    return []
            
            return []
            
        except Exception as e:
            self.logger.error(f"Error getting predictions: {e}")
            return []
    
    async def train_model(self, session_id: str, training_data: List[Dict[str, Any]]) -> bool:
        """Train a model for a session."""
        try:
            if not self.is_initialized:
                raise RuntimeError("Orchestrator services not initialized")
            
            session = self.orchestrator_core.get_learning_session(session_id)
            if not session:
                self.logger.warning(f"Session {session_id} not found")
                return False
            
            # Use engine for training
            if self.orchestrator_core.engine:
                success = self.orchestrator_core.engine.train_model(session_id, training_data)
                if success:
                    self.logger.info(f"Trained model for session {session_id}")
                return success
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error training model: {e}")
            return False
    
    async def analyze_features(self, session_id: str, features: List[Dict[str, Any]]) -> Optional[FeatureAnalysis]:
        """Analyze features for a session."""
        try:
            if not self.is_initialized:
                raise RuntimeError("Orchestrator services not initialized")
            
            session = self.orchestrator_core.get_learning_session(session_id)
            if not session:
                self.logger.warning(f"Session {session_id} not found")
                return None
            
            # Use engine for feature analysis
            if self.orchestrator_core.engine:
                analysis = self.orchestrator_core.engine.analyze_features(features)
                if analysis:
                    self.logger.info(f"Analyzed features for session {session_id}")
                return analysis
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error analyzing features: {e}")
            return None
    
    async def get_session_performance(self, session_id: str) -> Dict[str, Any]:
        """Get performance metrics for a session."""
        try:
            if not self.is_initialized:
                raise RuntimeError("Orchestrator services not initialized")
            
            session = self.orchestrator_core.get_learning_session(session_id)
            if not session:
                return {'error': f'Session {session_id} not found'}
            
            # Get session metrics
            metrics = self.orchestrator_core.get_session_metrics(session_id)
            
            if not metrics:
                return {'message': 'No performance metrics available'}
            
            # Calculate performance summary
            avg_accuracy = sum(m.accuracy for m in metrics) / len(metrics)
            avg_loss = sum(m.loss for m in metrics) / len(metrics)
            
            return {
                'session_id': session_id,
                'average_accuracy': avg_accuracy,
                'average_loss': avg_loss,
                'metrics_count': len(metrics),
                'session_status': session.status.value,
                'last_updated': max(m.created_at for m in metrics).isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error getting session performance: {e}")
            return {'error': str(e)}
    
    async def generate_learning_report(self, session_id: str = None) -> Dict[str, Any]:
        """Generate a learning report for a session or all sessions."""
        try:
            if not self.is_initialized:
                raise RuntimeError("Orchestrator services not initialized")
            
            if session_id:
                sessions = [self.orchestrator_core.get_learning_session(session_id)]
                if not sessions[0]:
                    return {'error': f'Session {session_id} not found'}
            else:
                sessions = self.orchestrator_core.get_active_sessions()
            
            if not sessions:
                return {'message': 'No active sessions found'}
            
            # Generate report data
            report_data = {
                'report_type': 'learning_analysis',
                'total_sessions': len(sessions),
                'generated_at': datetime.now().isoformat(),
                'sessions': []
            }
            
            for session in sessions:
                session_data = {
                    'session_id': session.session_id,
                    'model_type': session.model_type.value,
                    'status': session.status.value,
                    'created_at': session.created_at.isoformat(),
                    'performance': await self.get_session_performance(session.session_id)
                }
                report_data['sessions'].append(session_data)
            
            self.logger.info(f"Generated learning report for {len(sessions)} sessions")
            return report_data
            
        except Exception as e:
            self.logger.error(f"Error generating learning report: {e}")
            return {'error': str(e)}
    
    def get_services_status(self) -> Dict[str, Any]:
        """Get services status."""
        if not self.is_initialized:
            return {'status': 'not_initialized'}
        
        return {
            'status': 'initialized',
            'orchestrator_core_initialized': self.orchestrator_core.is_initialized,
            'services_type': 'ml_learning_orchestration'
        }
    
    def shutdown(self):
        """Shutdown orchestrator services."""
        if not self.is_initialized:
            return
        
        self.logger.info("Shutting down ML Learning Orchestrator Services")
        self.is_initialized = False
