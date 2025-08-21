#!/usr/bin/env python3
"""
V2 Workflow Engine - Agent Cellphone V2
=======================================

Advanced workflow orchestration engine for V2 system.
Follows V2 standards: ≤ 200 LOC, SRP, OOP design, CLI interface.
"""

import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import threading
import time

logger = logging.getLogger(__name__)


class WorkflowState(Enum):
    """Workflow execution states"""
    INITIALIZED = "initialized"
    RUNNING = "running"
    WAITING_FOR_AI = "waiting_for_ai"
    PROCESSING_RESPONSE = "processing_response"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"


@dataclass
class V2WorkflowStep:
    """Individual step in a V2 workflow"""
    id: str
    name: str
    description: str
    agent_target: str
    prompt_template: str
    expected_response_type: str
    timeout_seconds: int = 300
    dependencies: List[str] = field(default_factory=list)
    completion_criteria: Dict[str, Any] = field(default_factory=dict)
    
    def is_ready(self, completed_steps: set) -> bool:
        """Check if step dependencies are satisfied"""
        return all(dep in completed_steps for dep in self.dependencies)


@dataclass
class V2Workflow:
    """V2 workflow definition"""
    workflow_id: str
    name: str
    description: str
    steps: List[V2WorkflowStep]
    created_at: str
    status: WorkflowState
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AIResponse:
    """Captured AI response from V2 system"""
    agent: str
    text: str
    timestamp: float
    message_id: str
    metadata: Dict[str, Any] = field(default_factory=dict)


class V2WorkflowEngine:
    """
    V2 Workflow Engine - Single responsibility: Advanced workflow orchestration.
    
    This service manages:
    - Workflow definition and execution
    - AI response monitoring and processing
    - Multi-agent coordination
    - Workflow state management
    
    NOTE: This class now delegates to the consolidated AdvancedWorkflowEngine
    """
    
    def __init__(self, fsm_orchestrator, agent_manager, response_capture_service):
        """Initialize V2 Workflow Engine."""
        self.fsm_orchestrator = fsm_orchestrator
        self.agent_manager = agent_manager
        self.response_capture_service = response_capture_service
        
        # Import consolidated workflow engine
        try:
            from ..core.advanced_workflow_engine import AdvancedWorkflowEngine
            self.workflow_engine = AdvancedWorkflowEngine(
                agent_manager, None, None, fsm_orchestrator, response_capture_service
            )
            self.workflows = self.workflow_engine.v2_workflows
            self.active_workflows = self.workflow_engine.active_workflows
        except ImportError:
            self.workflow_engine = None
            self.workflows = {}
            self.active_workflows = {}
        
        self.logger = self._setup_logging()
        
        # Start monitoring thread
        self.monitoring = False
        self.monitor_thread = None
        self._start_monitoring()
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for the service."""
        logger = logging.getLogger("V2WorkflowEngine")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def create_workflow(self, name: str, description: str, 
                       steps: List[Dict[str, Any]]) -> str:
        """Create a new V2 workflow"""
        try:
            workflow_id = f"WF-{len(self.workflows) + 1:03d}"
            current_time = datetime.now().isoformat()
            
            # Convert step definitions to V2WorkflowStep objects
            workflow_steps = []
            for step_data in steps:
                step = V2WorkflowStep(
                    id=step_data["id"],
                    name=step_data["name"],
                    description=step_data["description"],
                    agent_target=step_data["agent_target"],
                    prompt_template=step_data["prompt_template"],
                    expected_response_type=step_data.get("expected_response_type", "text"),
                    timeout_seconds=step_data.get("timeout_seconds", 300),
                    dependencies=step_data.get("dependencies", []),
                    completion_criteria=step_data.get("completion_criteria", {})
                )
                workflow_steps.append(step)
            
            workflow = V2Workflow(
                workflow_id=workflow_id,
                name=name,
                description=description,
                steps=workflow_steps,
                created_at=current_time,
                status=WorkflowState.INITIALIZED
            )
            
            self.workflows[workflow_id] = workflow
            self._save_workflow(workflow)
            
            self.logger.info(f"Created V2 workflow {workflow_id}: {name}")
            return workflow_id
            
        except Exception as e:
            self.logger.error(f"Failed to create workflow: {e}")
            return ""
    
    def execute_workflow(self, workflow_id: str) -> bool:
        """Execute a V2 workflow"""
        try:
            if workflow_id not in self.workflows:
                self.logger.error(f"Workflow {workflow_id} not found")
                return False
            
            workflow = self.workflows[workflow_id]
            workflow.status = WorkflowState.RUNNING
            
            # Initialize execution state
            execution_state = {
                "workflow_id": workflow_id,
                "current_step": 0,
                "completed_steps": set(),
                "failed_steps": set(),
                "start_time": time.time(),
                "ai_responses": []
            }
            
            self.active_workflows[workflow_id] = execution_state
            
            # Start execution
            self._execute_next_step(workflow_id)
            
            self.logger.info(f"Started execution of workflow {workflow_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to execute workflow {workflow_id}: {e}")
            return False
    
    def _execute_next_step(self, workflow_id: str):
        """Execute the next step in a workflow"""
        try:
            workflow = self.workflows[workflow_id]
            execution_state = self.active_workflows[workflow_id]
            
            # Find next ready step
            for i, step in enumerate(workflow.steps):
                if (i not in execution_state["completed_steps"] and 
                    i not in execution_state["failed_steps"] and
                    step.is_ready(execution_state["completed_steps"])):
                    
                    # Execute step
                    self._execute_step(workflow_id, i, step)
                    break
            else:
                # All steps completed
                workflow.status = WorkflowState.COMPLETED
                self._save_workflow(workflow)
                self.logger.info(f"Workflow {workflow_id} completed successfully")
                
        except Exception as e:
            self.logger.error(f"Error executing next step in workflow {workflow_id}: {e}")
            workflow = self.workflows[workflow_id]
            workflow.status = WorkflowState.FAILED
            self._save_workflow(workflow)
    
    def _execute_step(self, workflow_id: str, step_index: int, step: V2WorkflowStep):
        """Execute a single workflow step"""
        try:
            # Create FSM task for step execution
            task_id = self.fsm_orchestrator.create_task(
                title=f"Workflow Step: {step.name}",
                description=step.description,
                assigned_agent=step.agent_target,
                priority="normal"
            )
            
            if task_id:
                # Update execution state
                execution_state = self.active_workflows[workflow_id]
                execution_state["current_step"] = step_index
                
                # Monitor for AI response
                self._monitor_step_response(workflow_id, step_index, step, task_id)
                
                self.logger.info(f"Executing step {step_index} in workflow {workflow_id}")
            else:
                self.logger.error(f"Failed to create FSM task for step {step_index}")
                
        except Exception as e:
            self.logger.error(f"Error executing step {step_index}: {e}")
    
    def _monitor_step_response(self, workflow_id: str, step_index: int, 
                              step: V2WorkflowStep, task_id: str):
        """Monitor for AI response to complete step"""
        try:
            # This would integrate with the V2 response capture system
            # For now, we'll simulate step completion after a delay
            def complete_step():
                time.sleep(step.timeout_seconds)
                self._complete_step(workflow_id, step_index, step, task_id)
            
            # Start monitoring thread
            monitor_thread = threading.Thread(target=complete_step, daemon=True)
            monitor_thread.start()
            
        except Exception as e:
            self.logger.error(f"Error monitoring step response: {e}")
    
    def _complete_step(self, workflow_id: str, step_index: int, 
                      step: V2WorkflowStep, task_id: str):
        """Complete a workflow step"""
        try:
            execution_state = self.active_workflows[workflow_id]
            execution_state["completed_steps"].add(step_index)
            
            # Update FSM task status
            self.fsm_orchestrator.update_task_status(task_id, "completed")
            
            # Execute next step
            self._execute_next_step(workflow_id)
            
        except Exception as e:
            self.logger.error(f"Error completing step {step_index}: {e}")
    
    def get_workflow_status(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get workflow execution status"""
        if workflow_id not in self.workflows:
            return None
        
        workflow = self.workflows[workflow_id]
        execution_state = self.active_workflows.get(workflow_id, {})
        
        return {
            "workflow_id": workflow_id,
            "name": workflow.name,
            "status": workflow.status.value,
            "total_steps": len(workflow.steps),
            "completed_steps": len(execution_state.get("completed_steps", set())),
            "failed_steps": len(execution_state.get("failed_steps", set())),
            "current_step": execution_state.get("current_step", 0),
            "start_time": execution_state.get("start_time", 0)
        }
    
    def _start_monitoring(self):
        """Start workflow monitoring"""
        if not self.monitoring:
            self.monitoring = True
            self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self.monitor_thread.start()
            self.logger.info("V2 Workflow monitoring started")
    
    def _monitor_loop(self):
        """Workflow monitoring loop"""
        while self.monitoring:
            try:
                # Check for stalled workflows
                current_time = time.time()
                for workflow_id, execution_state in self.active_workflows.items():
                    if (execution_state.get("start_time", 0) > 0 and
                        current_time - execution_state["start_time"] > 3600):  # 1 hour
                        self.logger.warning(f"Workflow {workflow_id} may be stalled")
                
                time.sleep(60)  # Check every minute
                
            except Exception as e:
                self.logger.error(f"Workflow monitoring error: {e}")
                time.sleep(60)
    
    def _save_workflow(self, workflow: V2Workflow):
        """Save workflow to file"""
        try:
            workflow_file = self.workflow_data_path / f"{workflow.workflow_id}.json"
            
            workflow_data = {
                "workflow_id": workflow.workflow_id,
                "name": workflow.name,
                "description": workflow.description,
                "status": workflow.status.value,
                "created_at": workflow.created_at,
                "metadata": workflow.metadata,
                "steps": [
                    {
                        "id": step.id,
                        "name": step.name,
                        "description": step.description,
                        "agent_target": step.agent_target,
                        "prompt_template": step.prompt_template,
                        "expected_response_type": step.expected_response_type,
                        "timeout_seconds": step.timeout_seconds,
                        "dependencies": step.dependencies,
                        "completion_criteria": step.completion_criteria
                    }
                    for step in workflow.steps
                ]
            }
            
            with open(workflow_file, "w") as f:
                json.dump(workflow_data, f, indent=2)
                
        except Exception as e:
            self.logger.error(f"Failed to save workflow {workflow.workflow_id}: {e}")
    
    def _load_workflows(self):
        """Load existing workflows from files"""
        try:
            for workflow_file in self.workflow_data_path.glob("*.json"):
                try:
                    with open(workflow_file, "r") as f:
                        workflow_data = json.load(f)
                    
                    # Reconstruct workflow steps
                    steps = []
                    for step_data in workflow_data["steps"]:
                        step = V2WorkflowStep(
                            id=step_data["id"],
                            name=step_data["name"],
                            description=step_data["description"],
                            agent_target=step_data["agent_target"],
                            prompt_template=step_data["prompt_template"],
                            expected_response_type=step_data["expected_response_type"],
                            timeout_seconds=step_data["timeout_seconds"],
                            dependencies=step_data["dependencies"],
                            completion_criteria=step_data["completion_criteria"]
                        )
                        steps.append(step)
                    
                    workflow = V2Workflow(
                        workflow_id=workflow_data["workflow_id"],
                        name=workflow_data["name"],
                        description=workflow_data["description"],
                        steps=steps,
                        created_at=workflow_data["created_at"],
                        status=WorkflowState(workflow_data["status"]),
                        metadata=workflow_data.get("metadata", {})
                    )
                    
                    self.workflows[workflow.workflow_id] = workflow
                    
                except Exception as e:
                    self.logger.error(f"Failed to load workflow from {workflow_file}: {e}")
                    
        except Exception as e:
            self.logger.error(f"Failed to load workflows: {e}")
    
    def get_system_summary(self) -> Dict[str, Any]:
        """Get V2 workflow system summary"""
        return {
            "total_workflows": len(self.workflows),
            "active_workflows": len(self.active_workflows),
            "completed_workflows": len([w for w in self.workflows.values() 
                                     if w.status == WorkflowState.COMPLETED]),
            "failed_workflows": len([w for w in self.workflows.values() 
                                   if w.status == WorkflowState.FAILED]),
            "monitoring_active": self.monitoring
        }
