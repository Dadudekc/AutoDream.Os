#!/usr/bin/env python3
"""
Extended AI Manager - Agent Cellphone V2
=======================================

Consolidated AIManager inheriting from BaseManager.
Follows V2 standards: OOP, SRP, clean production-grade code.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any

from src.core.base_manager import BaseManager


class ExtendedAIManager(BaseManager):
    """Extended AI Manager - inherits from BaseManager for unified functionality"""
    
    def __init__(self, config_path: str = "config/ai_ml/ai_manager.json"):
        super().__init__(
            manager_name="ExtendedAIManager",
            config_path=config_path,
            enable_metrics=True,
            enable_events=True,
            enable_persistence=True
        )
        
        # Initialize AI-specific functionality
        self.models: Dict[str, Any] = {}
        self.active_workflows: Dict[str, Any] = {}
        self.api_keys = {}
        
        # Load AI configuration
        self._load_ai_config()
        
        logger.info("ExtendedAIManager initialized successfully")
    
    def _load_ai_config(self):
        """Load AI-specific configuration"""
        try:
            if self.config:
                ai_config = self.config.get("ai_ml", {})
                self.api_keys = ai_config.get("api_keys", {})
                
                # Emit configuration loaded event
                self.emit_event("ai_config_loaded", {
                    "models_count": len(self.models),
                    "workflows_count": len(self.active_workflows),
                    "api_keys_count": len(self.api_keys)
                })
        except Exception as e:
            logger.error(f"Error loading AI config: {e}")
    
    def register_model(self, model: Any) -> bool:
        """Register an AI model"""
        try:
            model_name = getattr(model, 'name', str(id(model)))
            self.models[model_name] = model
            
            # Update metrics
            self.metrics.total_operations += 1
            self.metrics.successful_operations += 1
            
            # Emit model registered event
            self.emit_event("model_registered", {
                "model_name": model_name,
                "total_models": len(self.models)
            })
            
            logger.info(f"Registered model: {model_name}")
            return True
        except Exception as e:
            logger.error(f"Error registering model {model_name}: {e}")
            self.metrics.failed_operations += 1
            return False
    
    def get_model(self, model_name: str) -> Optional[Any]:
        """Get a registered model by name"""
        model = self.models.get(model_name)
        if model:
            # Update metrics
            self.metrics.total_operations += 1
            self.metrics.successful_operations += 1
            
            # Emit model retrieved event
            self.emit_event("model_retrieved", {"model_name": model_name})
            
        return model
    
    def list_models(self) -> List[str]:
        """List all registered model names"""
        return list(self.models.keys())
    
    def create_workflow(self, name: str, description: str) -> Dict[str, Any]:
        """Create a new ML workflow"""
        try:
            workflow = {
                "name": name,
                "description": description,
                "status": "created",
                "steps": [],
                "created_at": self.last_activity.isoformat()
            }
            
            self.active_workflows[name] = workflow
            
            # Update metrics
            self.metrics.total_operations += 1
            self.metrics.successful_operations += 1
            
            # Emit workflow created event
            self.emit_event("workflow_created", {
                "workflow_name": name,
                "total_workflows": len(self.active_workflows)
            })
            
            logger.info(f"Created workflow: {name}")
            return workflow
        except Exception as e:
            logger.error(f"Error creating workflow {name}: {e}")
            self.metrics.failed_operations += 1
            return {}
    
    def get_workflow(self, name: str) -> Optional[Dict[str, Any]]:
        """Get a workflow by name"""
        return self.active_workflows.get(name)
    
    def list_workflows(self) -> List[str]:
        """List all active workflow names"""
        return list(self.active_workflows.keys())
    
    def get_api_key(self, service: str) -> Optional[str]:
        """Get API key for a specific service"""
        api_key = self.api_keys.get(service)
        if api_key:
            # Emit API key retrieved event
            self.emit_event("api_key_retrieved", {"service": service})
        return api_key
    
    def execute_workflow(self, workflow_name: str) -> bool:
        """Execute a workflow"""
        workflow = self.get_workflow(workflow_name)
        if not workflow:
            logger.error(f"Workflow not found: {workflow_name}")
            return False

        try:
            logger.info(f"Executing workflow: {workflow_name}")
            workflow["status"] = "running"
            
            # Emit workflow execution started event
            self.emit_event("workflow_execution_started", {
                "workflow_name": workflow_name
            })

            # Execute each step
            for step in workflow.get("steps", []):
                if step.get("status") == "pending":
                    step["status"] = "running"
                    # Here you would implement actual step execution
                    step["status"] = "completed"

            workflow["status"] = "completed"
            
            # Update metrics
            self.metrics.total_operations += 1
            self.metrics.successful_operations += 1
            
            # Emit workflow completed event
            self.emit_event("workflow_execution_completed", {
                "workflow_name": workflow_name,
                "status": "completed"
            })
            
            logger.info(f"Workflow completed: {workflow_name}")
            return True

        except Exception as e:
            logger.error(f"Error executing workflow {workflow_name}: {e}")
            workflow["status"] = "failed"
            
            # Update metrics
            self.metrics.failed_operations += 1
            
            # Emit workflow failed event
            self.emit_event("workflow_execution_failed", {
                "workflow_name": workflow_name,
                "error": str(e)
            })
            
            return False
    
    def add_workflow_step(self, workflow_name: str, step_name: str, step_type: str = "task") -> bool:
        """Add a step to a workflow"""
        try:
            workflow = self.get_workflow(workflow_name)
            if not workflow:
                return False
            
            step = {
                "name": step_name,
                "type": step_type,
                "status": "pending",
                "created_at": self.last_activity.isoformat()
            }
            
            workflow["steps"].append(step)
            
            # Emit step added event
            self.emit_event("workflow_step_added", {
                "workflow_name": workflow_name,
                "step_name": step_name,
                "step_type": step_type
            })
            
            return True
        except Exception as e:
            logger.error(f"Error adding step to workflow: {e}")
            return False
    
    def get_manager_status(self) -> Dict[str, Any]:
        """Get extended manager status including AI metrics"""
        base_status = super().get_manager_status()
        
        # Add AI-specific status
        ai_status = {
            "models_registered": len(self.models),
            "active_workflows": len(self.active_workflows),
            "api_keys_available": len(self.api_keys),
            "workflow_execution_success_rate": self._calculate_workflow_success_rate()
        }
        
        base_status.update(ai_status)
        return base_status
    
    def _calculate_workflow_success_rate(self) -> float:
        """Calculate workflow execution success rate"""
        if not self.active_workflows:
            return 0.0
        
        completed_workflows = [
            w for w in self.active_workflows.values()
            if w.get("status") in ["completed", "failed"]
        ]
        
        if not completed_workflows:
            return 0.0
        
        successful_workflows = [
            w for w in completed_workflows
            if w.get("status") == "completed"
        ]
        
        return (len(successful_workflows) / len(completed_workflows)) * 100.0

