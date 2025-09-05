#!/usr/bin/env python3
"""
ML Model Management Engine - KISS Simplified
============================================

Simplified model management engine for ML optimization system.
KISS PRINCIPLE: Keep It Simple, Stupid - streamlined model management.

Author: Agent-8 (SSOT & System Integration Specialist) - KISS Simplification
Original: Agent-7 (Web Development Specialist)
License: MIT
"""

import os
import pickle
import threading
from typing import Dict, List, Any, Optional
from datetime import datetime

from ..ml_optimizer_models import (
    MLOptimizationConfig, ModelState, create_model_state
)
from .pattern_learning_engine import PatternLearningEngine


class ModelManagementEngine:
    """Simplified model management engine for ML optimization"""
    
    def __init__(self, config: MLOptimizationConfig, pattern_engine: PatternLearningEngine):
        """Initialize model management engine - simplified."""
        self.config = config
        self.pattern_engine = pattern_engine
        self.model_states: Dict[str, ModelState] = {}
        self.management_lock = threading.Lock()
        self.is_training = False
        self.last_training_time: Optional[datetime] = None
    
    def create_model_state(self, model_id: str, model_type: str, 
                          initial_params: Optional[Dict[str, Any]] = None) -> ModelState:
        """Create a new model state - simplified."""
        try:
            with self.management_lock:
                model_state = create_model_state(
                    model_id=model_id,
                    model_type=model_type,
                    parameters=initial_params or {},
                    training_data_size=len(self.pattern_engine.training_data)
                )
                self.model_states[model_id] = model_state
                return model_state
        except Exception as e:
            print(f"Error creating model state: {e}")
            return None
    
    def get_model_state(self, model_id: str) -> Optional[ModelState]:
        """Get model state by ID - simplified."""
        try:
            with self.management_lock:
                return self.model_states.get(model_id)
        except Exception as e:
            print(f"Error getting model state: {e}")
            return None
    
    def update_model_state(self, model_id: str, updates: Dict[str, Any]) -> bool:
        """Update model state - simplified."""
        try:
            with self.management_lock:
                if model_id in self.model_states:
                    model_state = self.model_states[model_id]
                    for key, value in updates.items():
                        if hasattr(model_state, key):
                            setattr(model_state, key, value)
                    model_state.last_updated = datetime.now()
                    return True
                return False
        except Exception as e:
            print(f"Error updating model state: {e}")
            return False
    
    def save_model_state(self, model_id: str, file_path: str) -> bool:
        """Save model state to file - simplified."""
        try:
            with self.management_lock:
                if model_id in self.model_states:
                    with open(file_path, 'wb') as f:
                        pickle.dump(self.model_states[model_id], f)
                    return True
                return False
        except Exception as e:
            print(f"Error saving model state: {e}")
            return False
    
    def load_model_state(self, model_id: str, file_path: str) -> bool:
        """Load model state from file - simplified."""
        try:
            with self.management_lock:
                if os.path.exists(file_path):
                    with open(file_path, 'rb') as f:
                        model_state = pickle.load(f)
                    self.model_states[model_id] = model_state
                    return True
                return False
        except Exception as e:
            print(f"Error loading model state: {e}")
            return False
    
    def delete_model_state(self, model_id: str) -> bool:
        """Delete model state - simplified."""
        try:
            with self.management_lock:
                if model_id in self.model_states:
                    del self.model_states[model_id]
                    return True
                return False
        except Exception as e:
            print(f"Error deleting model state: {e}")
            return False
    
    def list_model_states(self) -> List[str]:
        """List all model state IDs - simplified."""
        try:
            with self.management_lock:
                return list(self.model_states.keys())
        except Exception as e:
            print(f"Error listing model states: {e}")
            return []
    
    def get_model_metrics(self, model_id: str) -> Optional[Dict[str, Any]]:
        """Get model metrics - simplified."""
        try:
            with self.management_lock:
                if model_id in self.model_states:
                    model_state = self.model_states[model_id]
                    return {
                        "model_id": model_id,
                        "model_type": model_state.model_type,
                        "accuracy": model_state.accuracy,
                        "loss": model_state.loss,
                        "epoch": model_state.epoch,
                        "last_updated": model_state.last_updated.isoformat()
                    }
                return None
        except Exception as e:
            print(f"Error getting model metrics: {e}")
            return None
    
    def start_training(self, model_id: str) -> bool:
        """Start training for a model - simplified."""
        try:
            with self.management_lock:
                if not self.is_training and model_id in self.model_states:
                    self.is_training = True
                    self.last_training_time = datetime.now()
                    return True
                return False
        except Exception as e:
            print(f"Error starting training: {e}")
            return False
    
    def stop_training(self, model_id: str) -> bool:
        """Stop training for a model - simplified."""
        try:
            with self.management_lock:
                if self.is_training and model_id in self.model_states:
                    self.is_training = False
                    return True
                return False
        except Exception as e:
            print(f"Error stopping training: {e}")
            return False
    
    def is_model_training(self) -> bool:
        """Check if any model is training - simplified."""
        try:
            with self.management_lock:
                return self.is_training
        except Exception as e:
            print(f"Error checking training status: {e}")
            return False
    
    def get_training_status(self) -> Dict[str, Any]:
        """Get training status - simplified."""
        try:
            with self.management_lock:
                return {
                    "is_training": self.is_training,
                    "last_training_time": self.last_training_time.isoformat() if self.last_training_time else None,
                    "total_models": len(self.model_states)
                }
        except Exception as e:
            print(f"Error getting training status: {e}")
            return {}
    
    def cleanup_old_models(self, days_old: int = 30) -> int:
        """Cleanup old models - simplified."""
        try:
            with self.management_lock:
                cutoff_date = datetime.now().timestamp() - (days_old * 24 * 60 * 60)
                old_models = []
                
                for model_id, model_state in self.model_states.items():
                    if model_state.last_updated.timestamp() < cutoff_date:
                        old_models.append(model_id)
                
                for model_id in old_models:
                    del self.model_states[model_id]
                
                return len(old_models)
        except Exception as e:
            print(f"Error cleaning up old models: {e}")
            return 0
    
    def get_engine_status(self) -> Dict[str, Any]:
        """Get engine status - simplified."""
        try:
            with self.management_lock:
                return {
                    "total_models": len(self.model_states),
                    "is_training": self.is_training,
                    "last_training_time": self.last_training_time.isoformat() if self.last_training_time else None,
                    "config_name": self.config.name if self.config else "unknown"
                }
        except Exception as e:
            print(f"Error getting engine status: {e}")
            return {}
    
    def shutdown(self) -> bool:
        """Shutdown engine - simplified."""
        try:
            with self.management_lock:
                self.is_training = False
                self.model_states.clear()
                return True
        except Exception as e:
            print(f"Error during shutdown: {e}")
            return False


# Global instance for backward compatibility
_global_model_management_engine: Optional[ModelManagementEngine] = None

def get_model_management_engine(config: MLOptimizationConfig, 
                               pattern_engine: PatternLearningEngine) -> ModelManagementEngine:
    """Returns a global instance of the ModelManagementEngine."""
    global _global_model_management_engine
    if _global_model_management_engine is None:
        _global_model_management_engine = ModelManagementEngine(config, pattern_engine)
    return _global_model_management_engine