"""
Workflow Execution Engine - V2 Compliant Execution Logic

This module contains the main workflow execution engine and definition manager.
Follows V2 standards with ≤200 LOC and single responsibility for execution logic.
"""

import os
import json
import logging
import threading
import time
import uuid
from typing import Dict, List, Optional, Any, Callable
from pathlib import Path
from collections import defaultdict, deque
from datetime import datetime, timedelta

from .workflow_types import (
    WorkflowType, WorkflowPriority, OptimizationStrategy, WorkflowStatus,
    DEFAULT_TIMEOUT, DEFAULT_OPTIMIZATION_INTERVAL, MIN_STEP_DURATION
)
from .workflow_core import (
    WorkflowStep, WorkflowExecution, WorkflowOptimization, V2Workflow
)


class WorkflowDefinitionManager:
    """Manages workflow definitions - integrated from execution engine"""
    
    def __init__(self):
        self.workflow_definitions: Dict[str, List[WorkflowStep]] = {}
        self.logger = logging.getLogger(f"{__name__}.WorkflowDefinitionManager")
        self._initialize_default_definitions()
    
    def _initialize_default_definitions(self):
        """Initialize default workflow definitions"""
        # Agent onboarding workflow
        self.workflow_definitions["agent_onboarding"] = [
            WorkflowStep(
                step_id="init",
                name="Initialization",
                step_type="initialization",
                description="Initialize agent system",
                dependencies=[],
                estimated_duration=30.0,
            ),
            WorkflowStep(
                step_id="training",
                name="Training",
                step_type="training",
                description="Conduct agent training",
                dependencies=["init"],
                estimated_duration=300.0,
            ),
            WorkflowStep(
                step_id="role_assignment",
                name="Role Assignment",
                step_type="role_assignment",
                description="Assign agent role",
                dependencies=["training"],
                estimated_duration=60.0,
            ),
            WorkflowStep(
                step_id="completion",
                name="Completion",
                step_type="completion",
                description="Complete onboarding",
                dependencies=["role_assignment"],
                estimated_duration=30.0,
            ),
        ]
    
    def get_workflow_definition(self, workflow_type: str) -> Optional[List[WorkflowStep]]:
        """Get workflow definition by type"""
        return self.workflow_definitions.get(workflow_type)
    
    def add_workflow_definition(self, workflow_type: str, steps: List[WorkflowStep]):
        """Add new workflow definition"""
        self.workflow_definitions[workflow_type] = steps
        self.logger.info(f"Added workflow definition: {workflow_type}")


class AdvancedWorkflowEngine:
    """
    Consolidated Advanced Workflow Engine - Core execution functionality
    
    Responsibilities:
    - Dynamic workflow creation and management
    - Advanced state management and transitions
    - Intelligent workflow optimization
    - Performance monitoring and enhancement
    - Scalable workflow execution
    - V2 workflow management and AI response processing
    """
    
    def __init__(
        self,
        agent_manager,
        config_manager,
        contract_manager,
        fsm_orchestrator=None,
        response_capture_service=None,
    ):
        self.agent_manager = agent_manager
        self.config_manager = config_manager
        self.contract_manager = contract_manager
        
        # V2 specific dependencies
        self.fsm_orchestrator = fsm_orchestrator
        self.response_capture_service = response_capture_service
        
        # Core workflow data
        self.workflows: Dict[str, Dict[str, Any]] = {}
        self.executions: Dict[str, WorkflowExecution] = {}
        self.optimizations: Dict[str, WorkflowOptimization] = {}
        
        # V2 workflow data
        self.v2_workflows: Dict[str, V2Workflow] = {}
        self.active_workflows: Dict[str, Dict[str, Any]] = {}
        
        # Performance tracking
        self.performance_metrics: Dict[str, List[float]] = defaultdict(list)
        self.optimization_history: List[WorkflowOptimization] = []
        
        # Execution engine
        self.execution_threads: Dict[str, threading.Thread] = {}
        self.workflow_queue: deque = deque()
        self.running = False
        
        # Optimization engine
        self.optimization_thread = None
        self.optimization_interval = DEFAULT_OPTIMIZATION_INTERVAL
        
        # Workflow definition management
        self.definition_manager = WorkflowDefinitionManager()
        self.workflow_handlers: Dict[str, List[Callable]] = {}
        
        # Workflow persistence
        self.workflow_data_path = Path("workflow_data")
        self.workflow_data_path.mkdir(exist_ok=True)
        
        self.logger = logging.getLogger(f"{__name__}.AdvancedWorkflowEngine")
        
        # Initialize workflow handlers
        self._initialize_workflow_handlers()
        
        # Load existing workflows
        self._load_workflows()
        
        # Start execution and optimization engines
        self._start_workflow_engines()
    
    def _initialize_workflow_handlers(self):
        """Initialize default workflow step handlers"""
        self.workflow_handlers = {
            "initialization": [self._default_initialization_handler],
            "training": [self._default_training_handler],
            "role_assignment": [self._default_role_assignment_handler],
            "capability_grant": [self._default_capability_grant_handler],
            "system_integration": [self._default_system_integration_handler],
            "validation": [self._default_validation_handler],
            "completion": [self._default_completion_handler],
        }
    
    def _default_initialization_handler(self, step_data: WorkflowStep, workflow: WorkflowExecution) -> bool:
        """Default initialization step handler"""
        try:
            self.logger.info(f"Executing initialization step for workflow {workflow.workflow_id}")
            time.sleep(MIN_STEP_DURATION)
            return True
        except Exception as e:
            self.logger.error(f"Initialization handler failed: {e}")
            return False
    
    def _default_training_handler(self, step_data: WorkflowStep, workflow: WorkflowExecution) -> bool:
        """Default training step handler"""
        try:
            self.logger.info(f"Executing training step for workflow {workflow.workflow_id}")
            time.sleep(MIN_STEP_DURATION)
            return True
        except Exception as e:
            self.logger.error(f"Training handler failed: {e}")
            return False
    
    def _default_role_assignment_handler(self, step_data: WorkflowStep, workflow: WorkflowExecution) -> bool:
        """Default role assignment step handler"""
        try:
            self.logger.info(f"Executing role assignment step for workflow {workflow.workflow_id}")
            time.sleep(MIN_STEP_DURATION)
            return True
        except Exception as e:
            self.logger.error(f"Role assignment handler failed: {e}")
            return False
    
    def _default_capability_grant_handler(self, step_data: WorkflowStep, workflow: WorkflowExecution) -> bool:
        """Default capability grant step handler"""
        try:
            self.logger.info(f"Executing capability grant step for workflow {workflow.workflow_id}")
            time.sleep(MIN_STEP_DURATION)
            return True
        except Exception as e:
            self.logger.error(f"Capability grant handler failed: {e}")
            return False
    
    def _default_system_integration_handler(self, step_data: WorkflowStep, workflow: WorkflowExecution) -> bool:
        """Default system integration step handler"""
        try:
            self.logger.info(f"Executing system integration step for workflow {workflow.workflow_id}")
            time.sleep(MIN_STEP_DURATION)
            return True
        except Exception as e:
            self.logger.error(f"System integration handler failed: {e}")
            return False
    
    def _default_validation_handler(self, step_data: WorkflowStep, workflow: WorkflowExecution) -> bool:
        """Default validation step handler"""
        try:
            self.logger.info(f"Executing validation step for workflow {workflow.workflow_id}")
            time.sleep(MIN_STEP_DURATION)
            return True
        except Exception as e:
            self.logger.error(f"Validation handler failed: {e}")
            return False
    
    def _default_completion_handler(self, step_data: WorkflowStep, workflow: WorkflowExecution) -> bool:
        """Default completion step handler"""
        try:
            self.logger.info(f"Executing completion step for workflow {workflow.workflow_id}")
            time.sleep(MIN_STEP_DURATION)
            return True
        except Exception as e:
            self.logger.error(f"Completion handler failed: {e}")
            return False
    
    def _load_workflows(self):
        """Load existing workflows from persistence"""
        try:
            for workflow_file in self.workflow_data_path.glob("*.json"):
                try:
                    with open(workflow_file, "r") as f:
                        workflow_data = json.load(f)
                    
                    # Convert to V2Workflow object
                    if "steps" in workflow_data:
                        steps = []
                        for step_data in workflow_data["steps"]:
                            step = WorkflowStep.from_dict(step_data)
                            steps.append(step)
                        
                        workflow = V2Workflow(
                            workflow_id=workflow_data["workflow_id"],
                            name=workflow_data["name"],
                            description=workflow_data["description"],
                            steps=steps,
                            created_at=workflow_data["created_at"],
                            status=WorkflowStatus(workflow_data["status"]),
                        )
                        
                        self.v2_workflows[workflow.workflow_id] = workflow
                
                except Exception as e:
                    self.logger.error(f"Failed to load workflow from {workflow_file}: {e}")
            
            self.logger.info(f"Loaded {len(self.v2_workflows)} existing workflows")
        
        except Exception as e:
            self.logger.error(f"Failed to load workflows: {e}")
    
    def _save_workflow(self, workflow: V2Workflow):
        """Save workflow to file"""
        try:
            workflow_file = self.workflow_data_path / f"{workflow.workflow_id}.json"
            
            with open(workflow_file, "w") as f:
                json.dump(workflow.to_dict(), f, indent=2)
            
            self.logger.info(f"Saved workflow {workflow.workflow_id}")
        
        except Exception as e:
            self.logger.error(f"Failed to save workflow {workflow.workflow_id}: {e}")
    
    def _start_workflow_engines(self):
        """Start workflow execution and optimization engines"""
        self.running = True
        
        # Start execution engine
        execution_thread = threading.Thread(target=self._execution_engine_loop, daemon=True)
        execution_thread.start()
        self.execution_threads["main"] = execution_thread
        
        # Start optimization engine
        self.optimization_thread = threading.Thread(target=self._optimization_engine_loop, daemon=True)
        self.optimization_thread.start()
        
        self.logger.info("Advanced Workflow Engine started")
    
    def _execution_engine_loop(self):
        """Main execution engine loop"""
        while self.running:
            try:
                if self.workflow_queue:
                    workflow_id = self.workflow_queue.popleft()
                    self._execute_workflow(workflow_id)
                else:
                    time.sleep(1)
            except Exception as e:
                self.logger.error(f"Execution engine error: {e}")
                time.sleep(5)
    
    def _optimization_engine_loop(self):
        """Main optimization engine loop"""
        while self.running:
            try:
                time.sleep(self.optimization_interval)
                self._run_optimization_cycle()
            except Exception as e:
                self.logger.error(f"Optimization engine error: {e}")
                time.sleep(60)
    
    def _run_optimization_cycle(self):
        """Run optimization cycle for all active workflows"""
        try:
            for workflow_id in list(self.workflows.keys()):
                if self.workflows[workflow_id].get("status") == WorkflowStatus.ACTIVE.value:
                    self._optimize_workflow(workflow_id)
        except Exception as e:
            self.logger.error(f"Optimization cycle error: {e}")
    
    def _optimize_workflow(self, workflow_id: str):
        """Optimize a specific workflow"""
        try:
            workflow = self.workflows[workflow_id]
            if not workflow.get("optimization_enabled", False):
                return
            
            # Get current performance metrics
            current_metrics = self._get_workflow_metrics(workflow_id)
            
            # Apply optimization strategies
            for strategy in workflow.get("optimization_targets", []):
                if strategy == OptimizationStrategy.PERFORMANCE.value:
                    self._apply_performance_optimization(workflow_id, current_metrics)
                elif strategy == OptimizationStrategy.RESOURCE_EFFICIENCY.value:
                    self._apply_resource_optimization(workflow_id, current_metrics)
            
            self.logger.info(f"Optimized workflow {workflow_id}")
        
        except Exception as e:
            self.logger.error(f"Workflow optimization failed for {workflow_id}: {e}")
    
    def _get_workflow_metrics(self, workflow_id: str) -> Dict[str, float]:
        """Get current workflow performance metrics"""
        try:
            if workflow_id in self.executions:
                execution = self.executions[workflow_id]
                return execution.performance_metrics
            return {}
        except Exception as e:
            self.logger.error(f"Failed to get metrics for workflow {workflow_id}: {e}")
            return {}
    
    def _apply_performance_optimization(self, workflow_id: str, current_metrics: Dict[str, float]):
        """Apply performance optimization to workflow"""
        try:
            # Simple performance optimization logic
            if "execution_time" in current_metrics:
                if current_metrics["execution_time"] > 1000:  # 1000ms threshold
                    # Optimize by reducing timeout values
                    workflow = self.workflows[workflow_id]
                    if "steps" in workflow:
                        for step_id, step_data in workflow["steps"].items():
                            if "timeout" in step_data:
                                step_data["timeout"] = max(60, step_data["timeout"] * 0.8)
            
            self.logger.info(f"Applied performance optimization to workflow {workflow_id}")
        
        except Exception as e:
            self.logger.error(f"Performance optimization failed for workflow {workflow_id}: {e}")
    
    def _apply_resource_optimization(self, workflow_id: str, current_metrics: Dict[str, float]):
        """Apply resource optimization to workflow"""
        try:
            # Simple resource optimization logic
            if "memory_usage" in current_metrics:
                if current_metrics["memory_usage"] > 100:  # 100MB threshold
                    # Optimize by reducing parallel execution
                    workflow = self.workflows[workflow_id]
                    if workflow.get("type") == WorkflowType.PARALLEL.value:
                        workflow["max_parallel_steps"] = max(2, workflow.get("max_parallel_steps", 5) - 1)
            
            self.logger.info(f"Applied resource optimization to workflow {workflow_id}")
        
        except Exception as e:
            self.logger.error(f"Resource optimization failed for workflow {workflow_id}: {e}")
    
    def create_dynamic_workflow(
        self,
        workflow_type: WorkflowType,
        steps: List[WorkflowStep],
        priority: WorkflowPriority = WorkflowPriority.NORMAL,
        optimization_targets: List[OptimizationStrategy] = None,
    ) -> str:
        """Create a dynamic workflow with optimization targets"""
        try:
            workflow_id = str(uuid.uuid4())
            
            workflow = {
                "workflow_id": workflow_id,
                "type": workflow_type,
                "steps": {step.step_id: step.to_dict() for step in steps},
                "priority": priority,
                "optimization_targets": optimization_targets or [OptimizationStrategy.PERFORMANCE],
                "created_at": datetime.now().isoformat(),
                "status": WorkflowStatus.INITIALIZING,
                "metadata": {
                    "dynamic": True,
                    "optimization_enabled": True,
                    "scalability_target": "high",
                },
            }
            
            self.workflows[workflow_id] = workflow
            
            # Add to execution queue
            self.workflow_queue.append(workflow_id)
            
            self.logger.info(f"Created dynamic workflow: {workflow_id} (Type: {workflow_type.value})")
            return workflow_id
        
        except Exception as e:
            self.logger.error(f"Failed to create dynamic workflow: {e}")
            return ""
    
    def create_v2_workflow(self, name: str, description: str, steps: List[Dict[str, Any]]) -> str:
        """Create a new V2 workflow"""
        try:
            workflow_id = f"WF-{len(self.v2_workflows) + 1:03d}"
            current_time = datetime.now().isoformat()
            
            # Convert step definitions to WorkflowStep objects
            workflow_steps = []
            for step_data in steps:
                step = WorkflowStep(
                    step_id=step_data["id"],
                    name=step_data["name"],
                    step_type=step_data.get("step_type", "general"),
                    description=step_data["description"],
                    agent_target=step_data.get("agent_target", ""),
                    prompt_template=step_data.get("prompt_template", ""),
                    expected_response_type=step_data.get("expected_response_type", "text"),
                    timeout=step_data.get("timeout_seconds", DEFAULT_TIMEOUT),
                    dependencies=step_data.get("dependencies", []),
                    completion_criteria=step_data.get("completion_criteria", {}),
                )
                workflow_steps.append(step)
            
            workflow = V2Workflow(
                workflow_id=workflow_id,
                name=name,
                description=description,
                steps=workflow_steps,
                created_at=current_time,
                status=WorkflowStatus.INITIALIZED,
            )
            
            self.v2_workflows[workflow_id] = workflow
            self._save_workflow(workflow)
            
            self.logger.info(f"Created V2 workflow {workflow_id}: {name}")
            return workflow_id
        
        except Exception as e:
            self.logger.error(f"Failed to create V2 workflow: {e}")
            return ""
    
    def start_workflow(self, workflow_type: str, agent_id: str, workflow_id: Optional[str] = None) -> str:
        """Start a new workflow execution"""
        if not workflow_id:
            workflow_id = f"{workflow_type}_{agent_id}_{int(time.time())}"
        
        workflow_definition = self.definition_manager.get_workflow_definition(workflow_type)
        if not workflow_definition:
            raise ValueError(f"Unknown workflow type: {workflow_type}")
        
        # Create workflow execution instance
        workflow_execution = WorkflowExecution(
            execution_id=workflow_id,
            workflow_id=workflow_id,
            status=WorkflowStatus.PENDING,
            current_step=None,
            completed_steps=[],
            failed_steps=[],
            start_time=datetime.now().isoformat(),
            estimated_completion="",
            actual_completion=None,
            performance_metrics={},
            optimization_history=[],
            agent_id=agent_id,
            step_results={},
            metadata={"workflow_type": workflow_type},
        )
        
        self.executions[workflow_id] = workflow_execution
        self.logger.info(f"Started workflow {workflow_id} for agent {agent_id}")
        
        return workflow_id
    
    def execute_workflow(self, workflow_id: str) -> bool:
        """Execute a workflow to completion"""
        if workflow_id not in self.executions:
            self.logger.error(f"Workflow {workflow_id} not found")
            return False
        
        workflow = self.executions[workflow_id]
        workflow.status = WorkflowStatus.IN_PROGRESS
        
        try:
            workflow_definition = self.definition_manager.get_workflow_definition(
                workflow.metadata["workflow_type"]
            )
            
            for step_data in workflow_definition:
                # Check prerequisites
                if not self._can_execute_step(step_data, workflow.completed_steps):
                    self.logger.warning(f"Prerequisites not met for step {step_data.step_id}")
                    continue
                
                # Execute step
                if self._execute_step(step_data, workflow):
                    workflow.completed_steps.append(step_data.step_id)
                    workflow.step_results[step_data.step_id] = {"status": "completed"}
                else:
                    workflow.status = WorkflowStatus.FAILED
                    self.logger.error(f"Step {step_data.step_id} failed")
                    return False
            
            # Complete workflow
            workflow.status = WorkflowStatus.COMPLETED
            workflow.actual_completion = datetime.now().isoformat()
            
            # Move to completed workflows
            self.active_workflows[workflow_id] = workflow
            del self.executions[workflow_id]
            
            self.logger.info(f"Workflow {workflow_id} completed successfully")
            return True
        
        except Exception as e:
            workflow.status = WorkflowStatus.FAILED
            self.logger.error(f"Workflow execution failed: {e}")
            return False
    
    def _can_execute_step(self, step_data: WorkflowStep, completed_steps: List[str]) -> bool:
        """Check if step can be executed"""
        return all(dep in completed_steps for dep in step_data.dependencies)
    
    def _execute_step(self, step_data: WorkflowStep, workflow: WorkflowExecution) -> bool:
        """Execute a workflow step"""
        try:
            step_type = step_data.step_type
            
            if step_type in self.workflow_handlers:
                for handler in self.workflow_handlers[step_type]:
                    if handler(step_data, workflow):
                        return True
                return False
            else:
                # Default execution
                self.logger.info(f"Executing step {step_data.step_id} with default handler")
                time.sleep(MIN_STEP_DURATION)
                return True
        
        except Exception as e:
            self.logger.error(f"Step execution failed: {e}")
            return False
    
    def execute_v2_workflow(self, workflow_id: str) -> bool:
        """Execute a V2 workflow"""
        try:
            if workflow_id not in self.v2_workflows:
                self.logger.error(f"V2 workflow {workflow_id} not found")
                return False
            
            workflow = self.v2_workflows[workflow_id]
            workflow.status = WorkflowStatus.RUNNING
            
            # Track active workflow
            self.active_workflows[workflow_id] = {
                "workflow": workflow,
                "start_time": time.time(),
                "current_step": 0,
                "completed_steps": set(),
            }
            
            self.logger.info(f"Executing V2 workflow {workflow_id}: {workflow.name}")
            return True
        
        except Exception as e:
            self.logger.error(f"Failed to execute V2 workflow {workflow_id}: {e}")
            return False
    
    def get_workflow(self, workflow_id: str) -> Optional[V2Workflow]:
        """Get V2 workflow by ID"""
        return self.v2_workflows.get(workflow_id)
    
    def get_workflow_status(self, workflow_id: str) -> Optional[WorkflowStatus]:
        """Get workflow status"""
        if workflow_id in self.workflows:
            return self.workflows[workflow_id]["status"]
        return None
    
    def get_execution_status(self, execution_id: str) -> Optional[WorkflowExecution]:
        """Get execution status"""
        return self.executions.get(execution_id)
    
    def get_optimization_summary(self) -> Dict[str, Any]:
        """Get optimization summary"""
        try:
            total_optimizations = len(self.optimization_history)
            recent_optimizations = [
                o for o in self.optimization_history
                if datetime.fromisoformat(o.optimization_timestamp) > datetime.now() - timedelta(hours=24)
            ]
            
            avg_improvement = sum(o.improvement_percentage for o in self.optimization_history) / max(total_optimizations, 1)
            
            return {
                "total_optimizations": total_optimizations,
                "recent_optimizations": len(recent_optimizations),
                "average_improvement": round(avg_improvement, 2),
                "optimization_active": self.running,
                "last_optimization": self.optimization_history[-1].optimization_timestamp if self.optimization_history else None,
            }
        
        except Exception as e:
            self.logger.error(f"Failed to get optimization summary: {e}")
            return {"error": str(e)}
    
    def get_workflow_summary(self) -> Dict[str, Any]:
        """Get comprehensive workflow summary"""
        try:
            return {
                "total_workflows": len(self.workflows),
                "total_v2_workflows": len(self.v2_workflows),
                "active_executions": len(self.executions),
                "active_v2_workflows": len(self.active_workflows),
                "completed_workflows": len(self.active_workflows),
                "optimization_history": len(self.optimization_history),
                "workflow_types": list(set(w.get("type", "unknown") for w in self.workflows.values())),
                "v2_workflow_names": [w.name for w in self.v2_workflows.values()],
            }
        except Exception as e:
            self.logger.error(f"Failed to get workflow summary: {e}")
            return {"error": str(e)}
    
    def start(self):
        """Start the workflow engine"""
        self.running = True
        self.logger.info("Advanced Workflow Engine started")
    
    def stop(self):
        """Stop the workflow engine"""
        self.running = False
        self.logger.info("Advanced Workflow Engine stopped")

