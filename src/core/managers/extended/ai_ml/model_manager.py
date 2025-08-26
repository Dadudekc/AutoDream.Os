#!/usr/bin/env python3
"""
Extended Model Manager - Agent Cellphone V2
==========================================

Consolidated ModelManager inheriting from BaseManager.
Follows V2 standards: OOP, SRP, clean production-grade code.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import logging
from typing import Dict, List, Optional, Any, Union
from datetime import datetime

from src.core.base_manager import BaseManager


class ExtendedModelManager(BaseManager):
    """Extended Model Manager - inherits from BaseManager for unified functionality"""
    
    def __init__(self, config_path: str = "config/ai_ml/model_manager.json"):
        super().__init__(
            manager_name="ExtendedModelManager",
            config_path=config_path,
            enable_metrics=True,
            enable_events=True,
            enable_persistence=True
        )
        
        # Initialize model-specific functionality
        self.models: Dict[str, Dict[str, Any]] = {}
        self.model_registry: Dict[str, str] = {}
        self.model_versions: Dict[str, List[str]] = {}
        
        # Load model configuration
        self._load_model_config()
        
        logger.info("ExtendedModelManager initialized successfully")
    
    def _load_model_config(self):
        """Load model-specific configuration"""
        try:
            if self.config:
                model_config = self.config.get("models", {})
                self.model_registry = model_config.get("registry", {})
                self.model_versions = model_config.get("versions", {})
                
                # Emit configuration loaded event
                self.emit_event("model_config_loaded", {
                    "models_count": len(self.models),
                    "registry_count": len(self.model_registry),
                    "versions_count": len(self.model_versions)
                })
        except Exception as e:
            logger.error(f"Error loading model config: {e}")
    
    def register_model(self, model_name: str, model_info: Dict[str, Any]) -> bool:
        """Register a new model"""
        try:
            # Validate required fields
            required_fields = ["type", "version", "framework"]
            for field in required_fields:
                if field not in model_info:
                    raise ValueError(f"Missing required field: {field}")
            
            # Add metadata
            model_info["registered_at"] = self.last_activity.isoformat()
            model_info["status"] = "active"
            
            self.models[model_name] = model_info
            
            # Update registry
            self.model_registry[model_name] = model_info["type"]
            
            # Update versions
            if model_name not in self.model_versions:
                self.model_versions[model_name] = []
            self.model_versions[model_name].append(model_info["version"])
            
            # Update metrics
            self.metrics.total_operations += 1
            self.metrics.successful_operations += 1
            
            # Emit model registered event
            self.emit_event("model_registered", {
                "model_name": model_name,
                "model_type": model_info["type"],
                "version": model_info["version"],
                "total_models": len(self.models)
            })
            
            logger.info(f"Registered model: {model_name} (v{model_info['version']})")
            return True
        except Exception as e:
            logger.error(f"Error registering model {model_name}: {e}")
            self.metrics.failed_operations += 1
            return False
    
    def get_model(self, model_name: str) -> Optional[Dict[str, Any]]:
        """Get model information by name"""
        model = self.models.get(model_name)
        if model:
            # Update metrics
            self.metrics.total_operations += 1
            self.metrics.successful_operations += 1
            
            # Emit model retrieved event
            self.emit_event("model_retrieved", {"model_name": model_name})
            
        return model
    
    def list_models(self, model_type: Optional[str] = None) -> List[str]:
        """List all models, optionally filtered by type"""
        if model_type:
            models = [
                name for name, info in self.models.items()
                if info.get("type") == model_type
            ]
        else:
            models = list(self.models.keys())
        
        return models
    
    def get_model_versions(self, model_name: str) -> List[str]:
        """Get all versions of a specific model"""
        return self.model_versions.get(model_name, [])
    
    def update_model_status(self, model_name: str, status: str) -> bool:
        """Update model status"""
        try:
            if model_name not in self.models:
                return False
            
            self.models[model_name]["status"] = status
            self.models[model_name]["last_updated"] = self.last_activity.isoformat()
            
            # Emit status updated event
            self.emit_event("model_status_updated", {
                "model_name": model_name,
                "new_status": status
            })
            
            logger.info(f"Updated model {model_name} status to: {status}")
            return True
        except Exception as e:
            logger.error(f"Error updating model {model_name} status: {e}")
            return False
    
    def deactivate_model(self, model_name: str) -> bool:
        """Deactivate a model"""
        return self.update_model_status(model_name, "inactive")
    
    def activate_model(self, model_name: str) -> bool:
        """Activate a model"""
        return self.update_model_status(model_name, "active")
    
    def get_model_metrics(self, model_name: str) -> Dict[str, Any]:
        """Get performance metrics for a specific model"""
        model = self.get_model(model_name)
        if not model:
            return {}
        
        # Extract metrics from model info
        metrics = {
            "model_name": model_name,
            "type": model.get("type"),
            "version": model.get("version"),
            "status": model.get("status"),
            "registered_at": model.get("registered_at"),
            "last_updated": model.get("last_updated"),
            "framework": model.get("framework"),
            "parameters": model.get("parameters", 0),
            "accuracy": model.get("accuracy", 0.0),
            "inference_time": model.get("inference_time", 0.0)
        }
        
        return metrics
    
    def search_models(self, criteria: Dict[str, Any]) -> List[str]:
        """Search models based on criteria"""
        try:
            matching_models = []
            
            for name, info in self.models.items():
                matches = True
                
                for key, value in criteria.items():
                    if key not in info or info[key] != value:
                        matches = False
                        break
                
                if matches:
                    matching_models.append(name)
            
            return matching_models
        except Exception as e:
            logger.error(f"Error searching models: {e}")
            return []
    
    def get_model_registry(self) -> Dict[str, str]:
        """Get the complete model registry"""
        return self.model_registry.copy()
    
    def get_manager_status(self) -> Dict[str, Any]:
        """Get extended manager status including model metrics"""
        base_status = super().get_manager_status()
        
        # Add model-specific status
        model_status = {
            "total_models": len(self.models),
            "active_models": len([m for m in self.models.values() if m.get("status") == "active"]),
            "inactive_models": len([m for m in self.models.values() if m.get("status") == "inactive"]),
            "model_types": list(set(m.get("type") for m in self.models.values())),
            "total_versions": sum(len(versions) for versions in self.model_versions.values())
        }
        
        base_status.update(model_status)
        return base_status

