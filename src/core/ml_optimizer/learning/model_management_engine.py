#!/usr/bin/env python3
"""
ML Model Management Engine
==========================

Model management engine for ML optimization system.
Handles model persistence, state management, and training coordination.
V2 COMPLIANT: Focused model management under 300 lines.

@version 1.0.0 - V2 COMPLIANCE MODULAR MODEL MANAGEMENT
@license MIT
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
    """Model management engine for ML optimization"""
    
    def __init__(self, config: MLOptimizationConfig, pattern_engine: PatternLearningEngine):
        """Initialize model management engine with configuration and pattern engine"""
        self.config = config
        self.pattern_engine = pattern_engine
        self.model_states: Dict[str, ModelState] = {}
        self.management_lock = threading.Lock()
        self.is_training = False
        self.last_training_time: Optional[datetime] = None
    
    def create_model_state(self, model_id: str, model_type: str, 
                          initial_params: Optional[Dict[str, Any]] = None) -> ModelState:
        """Create a new model state"""
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
            raise RuntimeError(f"Failed to create model state: {e}")
    
    def get_model_state(self, model_id: str) -> Optional[ModelState]:
        """Get model state by ID"""
        return self.model_states.get(model_id)
    
    def update_model_state(self, model_id: str, updates: Dict[str, Any]) -> bool:
        """Update model state with new parameters"""
        try:
            with self.management_lock:
                if model_id in self.model_states:
                    model_state = self.model_states[model_id]
                    model_state.update_parameters(updates)
                    model_state.last_updated = datetime.now()
                    return True
                return False
        except Exception:
            return False
    
    def start_training(self, model_id: str) -> bool:
        """Start training for a specific model"""
        try:
            with self.management_lock:
                if self.is_training:
                    return False  # Already training
                
                if model_id not in self.model_states:
                    return False  # Model doesn't exist
                
                self.is_training = True
                self.last_training_time = datetime.now()
                
                # Update model state
                model_state = self.model_states[model_id]
                model_state.training_status = 'training'
                model_state.training_start_time = self.last_training_time
                
                return True
        except Exception:
            return False
    
    def complete_training(self, model_id: str, training_metrics: Optional[Dict[str, Any]] = None) -> bool:
        """Complete training for a specific model"""
        try:
            with self.management_lock:
                if not self.is_training:
                    return False  # Not currently training
                
                if model_id not in self.model_states:
                    return False  # Model doesn't exist
                
                self.is_training = False
                completion_time = datetime.now()
                
                # Update model state
                model_state = self.model_states[model_id]
                model_state.training_status = 'completed'
                model_state.training_end_time = completion_time
                
                if training_metrics:
                    model_state.update_parameters(training_metrics)
                
                # Calculate training duration
                if model_state.training_start_time:
                    duration = completion_time - model_state.training_start_time
                    model_state.metadata['training_duration_seconds'] = duration.total_seconds()
                
                return True
        except Exception:
            return False
    
    def save_models(self, save_path: Optional[str] = None) -> bool:
        """Save all models to disk"""
        if not self.config.enable_model_persistence:
            return False
        
        save_path = save_path or self.config.model_save_path
        
        try:
            os.makedirs(save_path, exist_ok=True)
            
            with self.management_lock:
                # Save model states
                models_file = os.path.join(save_path, "model_states.pkl")
                with open(models_file, 'wb') as f:
                    pickle.dump(self.model_states, f)
                
                # Save patterns
                patterns_data = self.pattern_engine.export_patterns()
                patterns_file = os.path.join(save_path, "learned_patterns.pkl")
                with open(patterns_file, 'wb') as f:
                    pickle.dump(patterns_data, f)
            
            return True
            
        except Exception as e:
            return False
    
    def load_models(self, load_path: Optional[str] = None) -> bool:
        """Load all models from disk"""
        if not self.config.enable_model_persistence:
            return False
        
        load_path = load_path or self.config.model_save_path
        
        try:
            with self.management_lock:
                # Load model states
                models_file = os.path.join(load_path, "model_states.pkl")
                if os.path.exists(models_file):
                    with open(models_file, 'rb') as f:
                        self.model_states = pickle.load(f)
                
                # Load patterns
                patterns_file = os.path.join(load_path, "learned_patterns.pkl")
                if os.path.exists(patterns_file):
                    with open(patterns_file, 'rb') as f:
                        patterns_data = pickle.load(f)
                    self.pattern_engine.import_patterns(patterns_data)
            
            return True
            
        except Exception as e:
            return False
    
    def get_model_statistics(self) -> Dict[str, Any]:
        """Get statistics about all models"""
        with self.management_lock:
            if not self.model_states:
                return {
                    'total_models': 0,
                    'model_types': {},
                    'training_status': {},
                    'is_training': self.is_training
                }
            
            model_types = {}
            training_status = {}
            
            for model_state in self.model_states.values():
                # Count by type
                model_type = model_state.model_type
                model_types[model_type] = model_types.get(model_type, 0) + 1
                
                # Count by training status
                status = model_state.training_status
                training_status[status] = training_status.get(status, 0) + 1
            
            return {
                'total_models': len(self.model_states),
                'model_types': model_types,
                'training_status': training_status,
                'is_training': self.is_training,
                'last_training_time': self.last_training_time.isoformat() if self.last_training_time else None
            }
    
    def delete_model(self, model_id: str) -> bool:
        """Delete a model and its state"""
        try:
            with self.management_lock:
                if model_id in self.model_states:
                    del self.model_states[model_id]
                    return True
                return False
        except Exception:
            return False
    
    def clear_all_models(self):
        """Clear all models and states"""
        with self.management_lock:
            self.model_states.clear()
            self.is_training = False
            self.last_training_time = None
    
    def export_model(self, model_id: str) -> Optional[Dict[str, Any]]:
        """Export a specific model for sharing"""
        with self.management_lock:
            if model_id in self.model_states:
                model_state = self.model_states[model_id]
                return {
                    'model_id': model_id,
                    'model_data': model_state.to_dict(),
                    'export_timestamp': datetime.now().isoformat()
                }
        return None
    
    def import_model(self, model_data: Dict[str, Any]) -> bool:
        """Import a model from exported data"""
        try:
            with self.management_lock:
                model_id = model_data.get('model_id')
                model_info = model_data.get('model_data', {})
                
                if not model_id or not model_info:
                    return False
                
                # Create model state from imported data
                model_state = ModelState.from_dict(model_info)
                self.model_states[model_id] = model_state
                
                return True
        except Exception:
            return False
    
    def get_training_status(self) -> Dict[str, Any]:
        """Get current training status"""
        with self.management_lock:
            return {
                'is_training': self.is_training,
                'last_training_time': self.last_training_time.isoformat() if self.last_training_time else None,
                'training_models': [
                    model_id for model_id, state in self.model_states.items()
                    if state.training_status == 'training'
                ]
            }


# Factory function for dependency injection
def create_model_management_engine(config: MLOptimizationConfig, 
                                 pattern_engine: PatternLearningEngine) -> ModelManagementEngine:
    """Factory function to create model management engine with dependencies"""
    return ModelManagementEngine(config, pattern_engine)


# Export for DI
__all__ = ['ModelManagementEngine', 'create_model_management_engine']
