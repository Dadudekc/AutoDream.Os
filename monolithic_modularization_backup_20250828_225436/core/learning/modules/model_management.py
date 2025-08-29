#!/usr/bin/env python3
"""
Model Management Module - Agent Cellphone V2
==========================================

Extracted from unified_learning_engine.py to provide focused model lifecycle management.
Follows V2 standards: modular design, SRP, clean interfaces.

**Author:** Captain Agent-3 (MODULAR-007 Contract)
**Created:** Current Sprint
**Status:** ACTIVE - MODULARIZATION IN PROGRESS
"""

import logging
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass
from enum import Enum

from ..models import (
    LearningMetrics, LearningSession, LearningGoal, LearningStrategy
)
from ..decision_models import (
    DecisionAlgorithm, DecisionRule, DecisionWorkflow
)


class ModelStatus(Enum):
    """Model lifecycle status"""
    CREATED = "created"
    TRAINING = "training"
    ACTIVE = "active"
    INACTIVE = "inactive"
    DEPRECATED = "deprecated"
    ERROR = "error"


class ModelType(Enum):
    """Types of models managed"""
    LEARNING_STRATEGY = "learning_strategy"
    DECISION_ALGORITHM = "decision_algorithm"
    PERFORMANCE_PREDICTOR = "performance_predictor"
    COLLABORATION_OPTIMIZER = "collaboration_optimizer"
    ADAPTATION_ENGINE = "adaptation_engine"


@dataclass
class ModelMetadata:
    """Metadata for managed models"""
    model_id: str
    model_type: ModelType
    name: str
    description: str
    version: str
    created_at: datetime
    last_updated: datetime
    status: ModelStatus
    performance_score: float
    usage_count: int
    error_count: int


class ModelManagementModule:
    """
    Focused module for model lifecycle management
    
    This module handles:
    - Model creation and registration
    - Model lifecycle management
    - Performance monitoring and optimization
    - Model deprecation and cleanup
    """
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.models: Dict[str, Any] = {}
        self.model_metadata: Dict[str, ModelMetadata] = {}
        self.model_performance: Dict[str, List[float]] = {}
        self.model_usage: Dict[str, int] = {}
        self.model_errors: Dict[str, List[str]] = {}
        
        # Model lifecycle settings
        self.auto_deprecation_days = 30
        self.performance_threshold = 0.7
        self.max_error_count = 10
        
        self.logger.info("ModelManagementModule initialized")
    
    def register_model(
        self,
        model: Any,
        model_type: ModelType,
        name: str,
        description: str,
        version: str = "1.0.0"
    ) -> str:
        """Register a new model for management"""
        try:
            model_id = str(uuid.uuid4())
            current_time = datetime.now()
            
            # Create model metadata
            metadata = ModelMetadata(
                model_id=model_id,
                model_type=model_type,
                name=name,
                description=description,
                version=version,
                created_at=current_time,
                last_updated=current_time,
                status=ModelStatus.CREATED,
                performance_score=0.0,
                usage_count=0,
                error_count=0
            )
            
            # Store model and metadata
            self.models[model_id] = model
            self.model_metadata[model_id] = metadata
            self.model_performance[model_id] = []
            self.model_usage[model_id] = 0
            self.model_errors[model_id] = []
            
            self.logger.info(f"Registered model: {name} ({model_id}) of type {model_type.value}")
            return model_id
            
        except Exception as e:
            self.logger.error(f"Failed to register model: {e}")
            return ""
    
    def activate_model(self, model_id: str) -> bool:
        """Activate a registered model"""
        try:
            if model_id not in self.model_metadata:
                raise ValueError(f"Model {model_id} not found")
            
            metadata = self.model_metadata[model_id]
            metadata.status = ModelStatus.ACTIVE
            metadata.last_updated = datetime.now()
            
            self.logger.info(f"Activated model: {metadata.name} ({model_id})")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to activate model {model_id}: {e}")
            return False
    
    def deactivate_model(self, model_id: str) -> bool:
        """Deactivate a model"""
        try:
            if model_id not in self.model_metadata:
                raise ValueError(f"Model {model_id} not found")
            
            metadata = self.model_metadata[model_id]
            metadata.status = ModelStatus.INACTIVE
            metadata.last_updated = datetime.now()
            
            self.logger.info(f"Deactivated model: {metadata.name} ({model_id})")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to deactivate model {model_id}: {e}")
            return False
    
    def update_model_performance(self, model_id: str, performance_score: float) -> bool:
        """Update performance metrics for a model"""
        try:
            if model_id not in self.model_metadata:
                return False
            
            metadata = self.model_metadata[model_id]
            metadata.performance_score = performance_score
            metadata.last_updated = datetime.now()
            
            # Store performance history
            if model_id in self.model_performance:
                self.model_performance[model_id].append(performance_score)
                
                # Keep only last 100 performance scores
                if len(self.model_performance[model_id]) > 100:
                    self.model_performance[model_id] = self.model_performance[model_id][-100:]
            
            # Check if model should be deprecated due to poor performance
            if performance_score < self.performance_threshold:
                self.logger.warning(f"Model {metadata.name} performance below threshold: {performance_score}")
                
                # Auto-deprecate if performance is consistently poor
                recent_scores = self.model_performance[model_id][-5:] if len(self.model_performance[model_id]) >= 5 else []
                if recent_scores and all(score < self.performance_threshold for score in recent_scores):
                    self.logger.warning(f"Auto-deprecating model {metadata.name} due to poor performance")
                    self._deprecate_model(model_id, "Poor performance")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to update model performance: {e}")
            return False
    
    def record_model_usage(self, model_id: str) -> bool:
        """Record usage of a model"""
        try:
            if model_id not in self.model_metadata:
                return False
            
            metadata = self.model_metadata[model_id]
            metadata.usage_count += 1
            metadata.last_updated = datetime.now()
            
            if model_id in self.model_usage:
                self.model_usage[model_id] += 1
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to record model usage: {e}")
            return False
    
    def record_model_error(self, model_id: str, error_message: str) -> bool:
        """Record an error for a model"""
        try:
            if model_id not in self.model_metadata:
                return False
            
            metadata = self.model_metadata[model_id]
            metadata.error_count += 1
            metadata.last_updated = datetime.now()
            
            # Store error message
            if model_id in self.model_errors:
                self.model_errors[model_id].append(error_message)
                
                # Keep only last 20 error messages
                if len(self.model_errors[model_id]) > 20:
                    self.model_errors[model_id] = self.model_errors[model_id][-20:]
            
            # Check if model should be deprecated due to errors
            if metadata.error_count >= self.max_error_count:
                self.logger.warning(f"Model {metadata.name} error count exceeded threshold: {metadata.error_count}")
                self._deprecate_model(model_id, "Excessive errors")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to record model error: {e}")
            return False
    
    def _deprecate_model(self, model_id: str, reason: str) -> bool:
        """Deprecate a model"""
        try:
            if model_id not in self.model_metadata:
                return False
            
            metadata = self.model_metadata[model_id]
            metadata.status = ModelStatus.DEPRECATED
            metadata.last_updated = datetime.now()
            
            self.logger.warning(f"Deprecated model {metadata.name} ({model_id}): {reason}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to deprecate model {model_id}: {e}")
            return False
    
    def get_model_info(self, model_id: str) -> Optional[Dict[str, Any]]:
        """Get comprehensive information about a model"""
        try:
            if model_id not in self.model_metadata:
                return None
            
            metadata = self.model_metadata[model_id]
            performance_history = self.model_performance.get(model_id, [])
            usage_count = self.model_usage.get(model_id, 0)
            error_messages = self.model_errors.get(model_id, [])
            
            return {
                "model_id": model_id,
                "name": metadata.name,
                "description": metadata.description,
                "type": metadata.model_type.value,
                "version": metadata.version,
                "status": metadata.status.value,
                "created_at": metadata.created_at.isoformat(),
                "last_updated": metadata.last_updated.isoformat(),
                "current_performance": metadata.performance_score,
                "usage_count": usage_count,
                "error_count": metadata.error_count,
                "performance_history": performance_history[-10:] if performance_history else [],
                "recent_errors": error_messages[-5:] if error_messages else [],
                "age_days": (datetime.now() - metadata.created_at).days
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get model info: {e}")
            return None
    
    def get_all_models_info(self) -> Dict[str, Dict[str, Any]]:
        """Get information about all managed models"""
        try:
            models_info = {}
            
            for model_id in self.model_metadata:
                model_info = self.get_model_info(model_id)
                if model_info:
                    models_info[model_id] = model_info
            
            return models_info
            
        except Exception as e:
            self.logger.error(f"Failed to get all models info: {e}")
            return {}
    
    def get_models_by_type(self, model_type: ModelType) -> List[str]:
        """Get all model IDs of a specific type"""
        try:
            return [
                model_id for model_id, metadata in self.model_metadata.items()
                if metadata.model_type == model_type
            ]
        except Exception as e:
            self.logger.error(f"Failed to get models by type: {e}")
            return []
    
    def get_active_models(self) -> List[str]:
        """Get all active model IDs"""
        try:
            return [
                model_id for model_id, metadata in self.model_metadata.items()
                if metadata.status == ModelStatus.ACTIVE
            ]
        except Exception as e:
            self.logger.error(f"Failed to get active models: {e}")
            return []
    
    def cleanup_deprecated_models(self, older_than_days: Optional[int] = None) -> int:
        """Clean up deprecated models"""
        try:
            if older_than_days is None:
                older_than_days = self.auto_deprecation_days
            
            cutoff_date = datetime.now() - timedelta(days=older_than_days)
            cleaned_count = 0
            
            models_to_remove = []
            for model_id, metadata in self.model_metadata.items():
                if (metadata.status == ModelStatus.DEPRECATED and 
                    metadata.last_updated < cutoff_date):
                    models_to_remove.append(model_id)
            
            for model_id in models_to_remove:
                # Remove model and all associated data
                self.models.pop(model_id, None)
                self.model_metadata.pop(model_id, None)
                self.model_performance.pop(model_id, None)
                self.model_usage.pop(model_id, None)
                self.model_errors.pop(model_id, None)
                cleaned_count += 1
            
            self.logger.info(f"Cleaned up {cleaned_count} deprecated models")
            return cleaned_count
            
        except Exception as e:
            self.logger.error(f"Failed to cleanup deprecated models: {e}")
            return 0
    
    def optimize_model_performance(self, model_id: str) -> bool:
        """Attempt to optimize model performance"""
        try:
            if model_id not in self.model_metadata:
                return False
            
            metadata = self.model_metadata[model_id]
            performance_history = self.model_performance.get(model_id, [])
            
            if len(performance_history) < 5:
                self.logger.info(f"Insufficient performance data for optimization: {metadata.name}")
                return False
            
            # Simple optimization: analyze performance trends
            recent_avg = sum(performance_history[-5:]) / 5
            overall_avg = sum(performance_history) / len(performance_history)
            
            if recent_avg < overall_avg * 0.9:  # Performance declining
                self.logger.info(f"Model {metadata.name} performance declining, optimization needed")
                
                # For learning strategies, suggest parameter adjustments
                if metadata.model_type == ModelType.LEARNING_STRATEGY:
                    self._optimize_learning_strategy(model_id)
                
                # For decision algorithms, suggest rule adjustments
                elif metadata.model_type == ModelType.DECISION_ALGORITHM:
                    self._optimize_decision_algorithm(model_id)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to optimize model performance: {e}")
            return False
    
    def _optimize_learning_strategy(self, model_id: str):
        """Optimize learning strategy parameters"""
        try:
            model = self.models.get(model_id)
            if not model or not hasattr(model, 'parameters'):
                return
            
            # Simple parameter optimization
            if 'adaptation_rate' in model.parameters:
                current_rate = model.parameters['adaptation_rate']
                model.parameters['adaptation_rate'] = min(0.3, current_rate * 1.1)
            
            if 'learning_rate' in model.parameters:
                current_rate = model.parameters['learning_rate']
                model.parameters['learning_rate'] = min(0.2, current_rate * 1.1)
            
            self.logger.info(f"Optimized learning strategy parameters for model {model_id}")
            
        except Exception as e:
            self.logger.error(f"Failed to optimize learning strategy: {e}")
    
    def _optimize_decision_algorithm(self, model_id: str):
        """Optimize decision algorithm parameters"""
        try:
            model = self.models.get(model_id)
            if not model or not hasattr(model, 'performance_metrics'):
                return
            
            # Simple performance metric optimization
            if hasattr(model, 'performance_metrics'):
                metrics = model.performance_metrics
                if 'success_rate' in metrics and metrics['success_rate'] < 85.0:
                    # Suggest rule review
                    self.logger.info(f"Decision algorithm {model_id} success rate low, rule review recommended")
            
        except Exception as e:
            self.logger.error(f"Failed to optimize decision algorithm: {e}")
    
    def run_module_test(self) -> bool:
        """Run basic functionality test for the model management module"""
        try:
            # Test model registration
            test_model = {"test": "data"}
            model_id = self.register_model(
                test_model,
                ModelType.LEARNING_STRATEGY,
                "Test Model",
                "Test model for module validation"
            )
            
            if not model_id:
                return False
            
            # Test model activation
            if not self.activate_model(model_id):
                return False
            
            # Test performance update
            if not self.update_model_performance(model_id, 0.85):
                return False
            
            # Test usage recording
            if not self.record_model_usage(model_id):
                return False
            
            # Test model info retrieval
            model_info = self.get_model_info(model_id)
            if not model_info:
                return False
            
            # Test optimization
            if not self.optimize_model_performance(model_id):
                return False
            
            # Test cleanup
            self._deprecate_model(model_id, "Test deprecation")
            cleaned_count = self.cleanup_deprecated_models(older_than_days=0)
            if cleaned_count < 1:
                return False
            
            self.logger.info("✅ Model management module test passed")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Model management module test failed: {e}")
            return False
