#!/usr/bin/env python3
"""
Extended Dev Workflow Manager - inherits from BaseManager for unified functionality

This manager consolidates development workflow management functionality
from src/ai_ml/dev_workflow_manager.py into a V2-compliant system.
"""

import logging
import subprocess
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from pathlib import Path
from datetime import datetime

from src.core.base_manager import BaseManager
from src.utils.stability_improvements import stability_manager, safe_import

# Configure logging
logger = logging.getLogger(__name__)


@dataclass
class WorkflowStep:
    """A step in the development workflow."""
    name: str
    description: str
    command: str
    dependencies: List[str] = field(default_factory=list)
    timeout: int = 300
    retry_count: int = 3
    required: bool = True
    ai_assisted: bool = False


@dataclass
class WorkflowResult:
    """Result of a workflow step."""
    success: bool
    output: str
    error: Optional[str] = None
    duration: float = 0.0
    retries: int = 0
    ai_suggestions: List[str] = field(default_factory=list)


class ExtendedDevWorkflowManager(BaseManager):
    """Extended Dev Workflow Manager - inherits from BaseManager for unified functionality"""
    
    def __init__(self, config_path: str = "config/ai_ml/dev_workflow_manager.json"):
        super().__init__(
            manager_name="ExtendedDevWorkflowManager",
            config_path=config_path,
            enable_metrics=True,
            enable_events=True,
            enable_persistence=True
        )
        
        # Workflow management state
        self.project_path: Optional[Path] = None
        self.processor: Optional[Any] = None
        self.coordinator: Optional[Any] = None
        
        # Workflow execution state
        self.active_workflows: Dict[str, Dict[str, Any]] = {}
        self.workflow_history: List[Dict[str, Any]] = []
        self.step_results: Dict[str, Dict[str, WorkflowResult]] = {}
        
        # Execution settings
        self.default_timeout = 300
        self.max_retries = 3
        self.enable_ai_assistance = True
        self.parallel_execution = False
        
        # Initialize workflow components
        self._initialize_workflow_components()
        
        logger.info(f"ExtendedDevWorkflowManager initialized successfully")
    
    def _initialize_workflow_components(self):
        """Initialize workflow management components"""
        try:
            # Load configuration overrides
            if self.config:
                self.default_timeout = self.config.get("default_timeout", 300)
                self.max_retries = self.config.get("max_retries", 3)
                self.enable_ai_assistance = self.config.get("enable_ai_assistance", True)
                self.parallel_execution = self.config.get("parallel_execution", False)
            
            logger.info("✅ Dev workflow components initialized")
            
        except Exception as e:
            logger.error(f"❌ Error initializing dev workflow components: {e}")
    
    def set_project_path(self, project_path: str) -> bool:
        """Set the project path for workflow execution"""
        try:
            self.project_path = Path(project_path)
            if not self.project_path.exists():
                logger.warning(f"⚠️ Project path does not exist: {project_path}")
                return False
            
            # Emit project path set event
            self.emit_event("project_path_set", {
                "project_path": str(self.project_path),
                "timestamp": datetime.now().isoformat()
            })
            
            logger.info(f"✅ Project path set to: {self.project_path}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error setting project path: {e}")
            return False
    
    def set_processor(self, processor: Any) -> bool:
        """Set the AI processor for workflow execution"""
        try:
            self.processor = processor
            
            # Emit processor set event
            self.emit_event("processor_set", {
                "processor_type": type(processor).__name__,
                "timestamp": datetime.now().isoformat()
            })
            
            logger.info(f"✅ AI processor set: {type(processor).__name__}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error setting processor: {e}")
            return False
    
    def set_coordinator(self, coordinator: Any) -> bool:
        """Set the workflow coordinator"""
        try:
            self.coordinator = coordinator
            
            # Emit coordinator set event
            self.emit_event("coordinator_set", {
                "coordinator_type": type(coordinator).__name__,
                "timestamp": datetime.now().isoformat()
            })
            
            logger.info(f"✅ Workflow coordinator set: {type(coordinator).__name__}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error setting coordinator: {e}")
            return False
    
    def execute_workflow(self, workflow_name: str, **kwargs) -> Dict[str, WorkflowResult]:
        """Execute a named workflow and return step results"""
        try:
            if not self.coordinator:
                logger.error("❌ No workflow coordinator set")
                return {}
            
            if not self.project_path:
                logger.error("❌ No project path set")
                return {}
            
            # Get workflow steps from coordinator
            steps = self.coordinator.get_workflow(workflow_name)
            if not steps:
                logger.warning(f"⚠️ No workflow found: {workflow_name}")
                return {}
            
            # Initialize workflow execution
            workflow_id = f"{workflow_name}_{datetime.now().timestamp()}"
            self.active_workflows[workflow_id] = {
                "name": workflow_name,
                "start_time": datetime.now(),
                "status": "running",
                "steps": steps,
                "kwargs": kwargs
            }
            
            # Emit workflow start event
            self.emit_event("workflow_started", {
                "workflow_id": workflow_id,
                "workflow_name": workflow_name,
                "steps_count": len(steps),
                "timestamp": datetime.now().isoformat()
            })
            
            # Execute workflow steps
            results: Dict[str, WorkflowResult] = {}
            for step in steps:
                result = self._execute_step(step, workflow_id, **kwargs)
                results[step.name] = result
                
                # Stop execution if required step fails
                if not result.success and step.required:
                    logger.error(f"❌ Required step failed: {step.name}")
                    break
            
            # Update workflow status
            self.active_workflows[workflow_id]["status"] = "completed"
            self.active_workflows[workflow_id]["end_time"] = datetime.now()
            self.active_workflows[workflow_id]["results"] = results
            
            # Store results
            self.step_results[workflow_id] = results
            
            # Move to history
            self.workflow_history.append(self.active_workflows[workflow_id])
            del self.active_workflows[workflow_id]
            
            # Emit workflow completed event
            self.emit_event("workflow_completed", {
                "workflow_id": workflow_id,
                "workflow_name": workflow_name,
                "success_count": sum(1 for r in results.values() if r.success),
                "total_steps": len(results),
                "timestamp": datetime.now().isoformat()
            })
            
            logger.info(f"✅ Workflow completed: {workflow_name}")
            return results
            
        except Exception as e:
            logger.error(f"❌ Error executing workflow {workflow_name}: {e}")
            
            # Emit workflow error event
            self.emit_event("workflow_error", {
                "workflow_name": workflow_name,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
            
            return {}
    
    def _execute_step(self, step: WorkflowStep, workflow_id: str, **kwargs) -> WorkflowResult:
        """Execute a single workflow step"""
        start_time = time.time()
        retries = 0
        
        while retries <= step.retry_count:
            try:
                logger.info(f"🔄 Executing step: {step.name} (attempt {retries + 1})")
                
                # Execute command
                result = subprocess.run(
                    step.command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=step.timeout,
                    cwd=self.project_path
                )
                
                # Process result
                success = result.returncode == 0
                output = result.stdout
                error = result.stderr if not success else None
                
                # Generate AI suggestions if AI-assisted and step failed
                ai_suggestions = []
                if step.ai_assisted and not success and self.processor:
                    try:
                        ai_suggestions = self._generate_ai_suggestions(step, error, **kwargs)
                    except Exception as e:
                        logger.warning(f"⚠️ Failed to generate AI suggestions: {e}")
                
                # Create result
                step_result = WorkflowResult(
                    success=success,
                    output=output,
                    error=error,
                    duration=time.time() - start_time,
                    retries=retries,
                    ai_suggestions=ai_suggestions
                )
                
                # Emit step completed event
                self.emit_event("workflow_step_completed", {
                    "workflow_id": workflow_id,
                    "step_name": step.name,
                    "success": success,
                    "duration": step_result.duration,
                    "retries": retries,
                    "timestamp": datetime.now().isoformat()
                })
                
                if success:
                    logger.info(f"✅ Step completed: {step.name}")
                    return step_result
                else:
                    logger.warning(f"⚠️ Step failed: {step.name} (attempt {retries + 1})")
                    retries += 1
                    
            except subprocess.TimeoutExpired:
                logger.error(f"❌ Step timeout: {step.name}")
                retries += 1
                
            except Exception as e:
                logger.error(f"❌ Step execution error: {step.name} - {e}")
                retries += 1
        
        # All retries exhausted
        logger.error(f"❌ Step failed after {retries} attempts: {step.name}")
        
        return WorkflowResult(
            success=False,
            output="",
            error=f"Step failed after {retries} attempts",
            duration=time.time() - start_time,
            retries=retries,
            ai_suggestions=[]
        )
    
    def _generate_ai_suggestions(self, step: WorkflowStep, error: str, **kwargs) -> List[str]:
        """Generate AI suggestions for failed steps"""
        try:
            if not self.processor:
                return []
            
            # Create context for AI analysis
            context = {
                "step_name": step.name,
                "step_description": step.description,
                "command": step.command,
                "error": error,
                "project_path": str(self.project_path),
                "kwargs": kwargs
            }
            
            # Use processor to generate suggestions
            suggestions = self.processor.analyze_step_failure(context)
            return suggestions if isinstance(suggestions, list) else []
            
        except Exception as e:
            logger.warning(f"⚠️ Error generating AI suggestions: {e}")
            return []
    
    def get_workflow_status(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific workflow"""
        # Check active workflows
        if workflow_id in self.active_workflows:
            return self.active_workflows[workflow_id]
        
        # Check workflow history
        for workflow in self.workflow_history:
            if workflow.get("workflow_id") == workflow_id:
                return workflow
        
        return None
    
    def get_active_workflows(self) -> Dict[str, Dict[str, Any]]:
        """Get all currently active workflows"""
        return self.active_workflows.copy()
    
    def get_workflow_history(self) -> List[Dict[str, Any]]:
        """Get workflow execution history"""
        return self.workflow_history.copy()
    
    def get_step_results(self, workflow_id: str) -> Dict[str, WorkflowResult]:
        """Get results for a specific workflow"""
        return self.step_results.get(workflow_id, {}).copy()
    
    def clear_workflow_history(self, max_history: int = 100):
        """Clear old workflow history entries"""
        try:
            if len(self.workflow_history) > max_history:
                removed_count = len(self.workflow_history) - max_history
                self.workflow_history = self.workflow_history[-max_history:]
                
                # Emit history cleared event
                self.emit_event("workflow_history_cleared", {
                    "removed_count": removed_count,
                    "remaining_count": len(self.workflow_history),
                    "timestamp": datetime.now().isoformat()
                })
                
                logger.info(f"✅ Cleared {removed_count} old workflow history entries")
                
        except Exception as e:
            logger.error(f"❌ Error clearing workflow history: {e}")
    
    def get_dev_workflow_metrics(self) -> Dict[str, Any]:
        """Get dev workflow management performance metrics"""
        try:
            total_workflows = len(self.workflow_history)
            successful_workflows = sum(1 for w in self.workflow_history if w.get("status") == "completed")
            total_steps = sum(len(w.get("results", {})) for w in self.workflow_history)
            successful_steps = sum(
                sum(1 for r in step_results.values() if r.success)
                for step_results in self.step_results.values()
            )
            
            # Calculate average workflow duration
            durations = []
            for workflow in self.workflow_history:
                if "start_time" in workflow and "end_time" in workflow:
                    duration = (workflow["end_time"] - workflow["start_time"]).total_seconds()
                    durations.append(duration)
            
            avg_duration = sum(durations) / len(durations) if durations else 0
            
            return {
                "total_workflows_executed": total_workflows,
                "successful_workflows": successful_workflows,
                "workflow_success_rate": (successful_workflows / total_workflows * 100) if total_workflows > 0 else 0,
                "total_steps_executed": total_steps,
                "successful_steps": successful_steps,
                "step_success_rate": (successful_steps / total_steps * 100) if total_steps > 0 else 0,
                "average_workflow_duration": avg_duration,
                "active_workflows": len(self.active_workflows),
                "workflow_history_size": len(self.workflow_history),
                "uptime": self.get_uptime(),
                "last_activity": self.last_activity.isoformat() if self.last_activity else None
            }
            
        except Exception as e:
            logger.error(f"❌ Error generating dev workflow metrics: {e}")
            return {}

