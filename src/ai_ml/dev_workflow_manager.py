"""Development workflow manager handling execution logic with BaseManager inheritance."""
from __future__ import annotations

import subprocess
import time
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Optional, Any
from datetime import datetime

from ..core.base_manager import BaseManager, ManagerStatus, ManagerPriority

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

    step_name: str
    success: bool
    output: str
    error: Optional[str] = None
    execution_time: float = 0.0
    ai_suggestions: List[str] = field(default_factory=list)


class DevWorkflowManager(BaseManager):
    """
    Execute workflow steps and manage results
    
    Now inherits from BaseManager for unified functionality
    """

    def __init__(self, project_path: Path, processor, coordinator):
        """Initialize dev workflow manager with BaseManager"""
        super().__init__(
            manager_id="dev_workflow_manager",
            name="Development Workflow Manager",
            description="Executes workflow steps and manages results"
        )
        
        self.project_path = Path(project_path)
        self.processor = processor
        self.coordinator = coordinator
        
        # Workflow tracking
        self.active_workflows: Dict[str, Dict[str, WorkflowResult]] = {}
        self.workflow_history: List[Dict[str, Any]] = []
        self.step_execution_stats: Dict[str, Dict[str, Any]] = {}
        
        self.logger.info("Development Workflow Manager initialized")
    
    # ============================================================================
    # BaseManager Abstract Method Implementations
    # ============================================================================
    
    def _on_start(self) -> bool:
        """Initialize development workflow system"""
        try:
            self.logger.info("Starting Development Workflow Manager...")
            
            # Clear workflow data
            self.active_workflows.clear()
            self.workflow_history.clear()
            self.step_execution_stats.clear()
            
            # Validate project path
            if not self.project_path.exists():
                raise RuntimeError(f"Project path does not exist: {self.project_path}")
            
            self.logger.info("Development Workflow Manager started successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start Development Workflow Manager: {e}")
            return False
    
    def _on_stop(self):
        """Cleanup development workflow system"""
        try:
            self.logger.info("Stopping Development Workflow Manager...")
            
            # Save workflow history
            self._save_workflow_history()
            
            # Clear data
            self.active_workflows.clear()
            self.workflow_history.clear()
            self.step_execution_stats.clear()
            
            self.logger.info("Development Workflow Manager stopped successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to stop Development Workflow Manager: {e}")
    
    def _on_heartbeat(self):
        """Development workflow manager heartbeat"""
        try:
            # Check workflow health
            self._check_workflow_health()
            
            # Clean up completed workflows
            self._cleanup_completed_workflows()
            
            # Update metrics
            self.record_operation("heartbeat", True, 0.0)
            
        except Exception as e:
            self.logger.error(f"Heartbeat error: {e}")
            self.record_operation("heartbeat", False, 0.0)
    
    def _on_initialize_resources(self) -> bool:
        """Initialize development workflow resources"""
        try:
            # Initialize data structures
            self.active_workflows = {}
            self.workflow_history = []
            self.step_execution_stats = {}
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize resources: {e}")
            return False
    
    def _on_cleanup_resources(self):
        """Cleanup development workflow resources"""
        try:
            # Clear data
            self.active_workflows.clear()
            self.workflow_history.clear()
            self.step_execution_stats.clear()
            
        except Exception as e:
            self.logger.error(f"Failed to cleanup resources: {e}")
    
    def _on_recovery_attempt(self, error: Exception, context: str) -> bool:
        """Attempt recovery from errors"""
        try:
            self.logger.info(f"Attempting recovery for {context}")
            
            # Reset workflow state
            self.active_workflows.clear()
            self.step_execution_stats.clear()
            
            # Validate project path
            if not self.project_path.exists():
                self.logger.error("Project path validation failed during recovery")
                return False
            
            self.logger.info("Recovery successful")
            return True
            
        except Exception as e:
            self.logger.error(f"Recovery failed: {e}")
            return False
    
    # ============================================================================
    # Development Workflow Management Methods
    # ============================================================================
    
    def execute_workflow(self, workflow_name: str, **kwargs) -> Dict[str, WorkflowResult]:
        """Execute a named workflow and return step results."""
        try:
            self.logger.info(f"Executing workflow: {workflow_name}")
            
            # Get workflow steps
            steps = self.coordinator.get_workflow(workflow_name)
            if not steps:
                self.logger.error(f"No workflow found: {workflow_name}")
                return {}
            
            # Initialize workflow tracking
            workflow_id = f"{workflow_name}_{int(time.time())}"
            self.active_workflows[workflow_id] = {}
            results: Dict[str, WorkflowResult] = {}
            
            # Execute each step
            for step in steps:
                result = self._execute_step(step, **kwargs)
                results[step.name] = result
                self.active_workflows[workflow_id][step.name] = result
                
                # Track step execution stats
                self._track_step_execution(step, result)
                
                # Break if required step fails
                if not result.success and step.required:
                    self.logger.warning(f"Required step {step.name} failed, stopping workflow")
                    break
            
            # Record workflow completion
            self._record_workflow_completion(workflow_name, workflow_id, results)
            
            # Record operation
            self.record_operation("execute_workflow", True, 0.0)
            
            return results
            
        except Exception as e:
            self.logger.error(f"Failed to execute workflow {workflow_name}: {e}")
            self.record_operation("execute_workflow", False, 0.0)
            return {}

    def _execute_step(self, step: WorkflowStep, **kwargs) -> WorkflowResult:
        """Execute a single workflow step"""
        try:
            start = time.time()
            
            if step.ai_assisted:
                output = self.processor.execute_ai_assisted_step(
                    step, self.project_path, **kwargs
                )
            else:
                output = self._execute_command(step.command, step.timeout)
            
            exec_time = time.time() - start
            suggestions: List[str] = []
            
            if step.ai_assisted:
                suggestions = self.processor.get_ai_suggestions(step, output)
            
            result = WorkflowResult(
                step_name=step.name,
                success=True,
                output=output,
                execution_time=exec_time,
                ai_suggestions=suggestions,
            )
            
            # Record operation
            self.record_operation("execute_step", True, exec_time)
            
            return result
            
        except subprocess.TimeoutExpired:
            exec_time = time.time() - start
            result = WorkflowResult(
                step_name=step.name,
                success=False,
                output="",
                error=f"Step timed out after {step.timeout} seconds",
                execution_time=exec_time,
            )
            
            # Record operation
            self.record_operation("execute_step", False, exec_time)
            
            return result
            
        except Exception as e:
            exec_time = time.time() - start
            result = WorkflowResult(
                step_name=step.name,
                success=False,
                output="",
                error=str(e),
                execution_time=exec_time,
            )
            
            # Record operation
            self.record_operation("execute_step", False, exec_time)
            
            return result

    def _execute_command(self, command: str, timeout: int) -> str:
        """Execute shell command safely."""
        try:
            result = subprocess.run(
                command.split(),
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=self.project_path,
            )
            
            if result.returncode != 0:
                raise subprocess.CalledProcessError(
                    result.returncode, command, result.stdout, result.stderr
                )
            
            return result.stdout
            
        except Exception as e:
            self.logger.error(f"Command execution failed: {e}")
            raise
    
    # ============================================================================
    # Private Helper Methods
    # ============================================================================
    
    def _track_step_execution(self, step: WorkflowStep, result: WorkflowResult):
        """Track step execution statistics"""
        try:
            if step.name not in self.step_execution_stats:
                self.step_execution_stats[step.name] = {
                    "total_executions": 0,
                    "successful_executions": 0,
                    "failed_executions": 0,
                    "total_execution_time": 0.0,
                    "average_execution_time": 0.0
                }
            
            stats = self.step_execution_stats[step.name]
            stats["total_executions"] += 1
            stats["total_execution_time"] += result.execution_time
            
            if result.success:
                stats["successful_executions"] += 1
            else:
                stats["failed_executions"] += 1
            
            stats["average_execution_time"] = stats["total_execution_time"] / stats["total_executions"]
            
        except Exception as e:
            self.logger.error(f"Failed to track step execution: {e}")
    
    def _record_workflow_completion(self, workflow_name: str, workflow_id: str, results: Dict[str, WorkflowResult]):
        """Record workflow completion in history"""
        try:
            workflow_record = {
                "workflow_name": workflow_name,
                "workflow_id": workflow_id,
                "timestamp": datetime.now().isoformat(),
                "total_steps": len(results),
                "successful_steps": len([r for r in results.values() if r.success]),
                "failed_steps": len([r for r in results.values() if not r.success]),
                "total_execution_time": sum(r.execution_time for r in results.values()),
                "results": {name: {
                    "success": result.success,
                    "execution_time": result.execution_time,
                    "error": result.error
                } for name, result in results.items()}
            }
            
            self.workflow_history.append(workflow_record)
            
            # Remove from active workflows
            if workflow_id in self.active_workflows:
                del self.active_workflows[workflow_id]
            
            # Keep history manageable
            if len(self.workflow_history) > 1000:
                self.workflow_history = self.workflow_history[-500:]
                
        except Exception as e:
            self.logger.error(f"Failed to record workflow completion: {e}")
    
    def _save_workflow_history(self):
        """Save workflow history (placeholder for future persistence)"""
        try:
            # TODO: Implement persistence to database/file
            self.logger.debug("Workflow history saved")
            
        except Exception as e:
            self.logger.error(f"Failed to save workflow history: {e}")
    
    def _check_workflow_health(self):
        """Check workflow health status"""
        try:
            # Check for stuck workflows
            current_time = datetime.now()
            
            for workflow_id, steps in list(self.active_workflows.items()):
                if len(steps) > 0:
                    # Check if workflow has been active too long
                    # This is a simplified check - in practice you'd track workflow start time
                    if len(steps) > 50:  # Arbitrary threshold
                        self.logger.warning(f"Workflow {workflow_id} has many steps: {len(steps)}")
                        
        except Exception as e:
            self.logger.error(f"Failed to check workflow health: {e}")
    
    def _cleanup_completed_workflows(self):
        """Clean up completed workflows"""
        try:
            # This is handled in _record_workflow_completion
            # Additional cleanup logic can be added here if needed
            pass
            
        except Exception as e:
            self.logger.error(f"Failed to cleanup completed workflows: {e}")
    
    def get_workflow_stats(self) -> Dict[str, Any]:
        """Get workflow execution statistics"""
        try:
            stats = {
                "active_workflows": len(self.active_workflows),
                "workflow_history_size": len(self.workflow_history),
                "step_execution_stats": self.step_execution_stats,
                "manager_status": self.status.value,
                "manager_uptime": self.metrics.uptime_seconds
            }
            
            # Record operation
            self.record_operation("get_workflow_stats", True, 0.0)
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Failed to get workflow stats: {e}")
            self.record_operation("get_workflow_stats", False, 0.0)
            return {"error": str(e)}
    
    def get_step_performance(self, step_name: str) -> Dict[str, Any]:
        """Get performance statistics for a specific step"""
        try:
            if step_name not in self.step_execution_stats:
                return {"error": f"Step {step_name} not found"}
            
            stats = self.step_execution_stats[step_name].copy()
            
            # Calculate success rate
            if stats["total_executions"] > 0:
                stats["success_rate"] = (stats["successful_executions"] / stats["total_executions"]) * 100
                stats["failure_rate"] = (stats["failed_executions"] / stats["total_executions"]) * 100
            else:
                stats["success_rate"] = 0.0
                stats["failure_rate"] = 0.0
            
            # Record operation
            self.record_operation("get_step_performance", True, 0.0)
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Failed to get step performance for {step_name}: {e}")
            self.record_operation("get_step_performance", False, 0.0)
            return {"error": str(e)}
