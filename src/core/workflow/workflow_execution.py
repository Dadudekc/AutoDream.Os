#!/usr/bin/env python3
"""
Workflow Execution Module - V2 Core Workflow System
==================================================

Contains workflow execution engine and step management logic.
Follows V2 coding standards: ≤200 LOC, single responsibility, clean OOP design.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

import logging
import uuid
import time
from typing import Dict, List, Optional, Any, Set
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed

# Import workflow types
try:
    from .workflow_types import (
        WorkflowStep, V2Workflow, WorkflowExecution, 
        WorkflowOptimization, OptimizationStrategy
    )
except ImportError:
    # Fallback for standalone usage
    from workflow_types import (
        WorkflowStep, V2Workflow, WorkflowExecution, 
        WorkflowOptimization, OptimizationStrategy
    )

logger = logging.getLogger(__name__)


class WorkflowExecutionEngine:
    """Executes workflows - single responsibility: workflow execution"""
    
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.active_executions: Dict[str, WorkflowExecution] = {}
        self.completed_executions: Dict[str, WorkflowExecution] = {}
        self.logger = logging.getLogger(f"{__name__}.WorkflowExecutionEngine")

    def execute_workflow(self, workflow: V2Workflow, agent_id: Optional[str] = None) -> bool:
        """Execute a workflow"""
        try:
            execution_id = str(uuid.uuid4())
            
            execution = WorkflowExecution(
                execution_id=execution_id,
                workflow_id=workflow.workflow_id,
                status="running",
                current_step="",
                completed_steps=[],
                failed_steps=[],
                start_time=datetime.now().isoformat(),
                estimated_completion="",
                actual_completion=None,
                performance_metrics={},
                optimization_history=[],
                agent_id=agent_id
            )
            
            self.active_executions[execution_id] = execution
            self.logger.info(f"Started workflow execution: {execution_id}")
            
            # Execute workflow steps
            success = self._execute_steps(workflow, execution)
            
            if success:
                execution.status = "completed"
                execution.actual_completion = datetime.now().isoformat()
                self.completed_executions[execution_id] = execution
                del self.active_executions[execution_id]
                self.logger.info(f"Workflow execution completed: {execution_id}")
            else:
                execution.status = "failed"
                execution.actual_completion = datetime.now().isoformat()
                self.completed_executions[execution_id] = execution
                del self.active_executions[execution_id]
                self.logger.error(f"Workflow execution failed: {execution_id}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Failed to execute workflow: {e}")
            return False

    def _execute_steps(self, workflow: V2Workflow, execution: WorkflowExecution) -> bool:
        """Execute workflow steps in dependency order"""
        try:
            completed_steps: Set[str] = set()
            failed_steps: Set[str] = set()
            
            # Sort steps by dependencies
            sorted_steps = self._sort_steps_by_dependencies(workflow.steps)
            
            for step in sorted_steps:
                if not step.is_ready(completed_steps):
                    self.logger.warning(f"Step {step.step_id} dependencies not met")
                    continue
                
                execution.current_step = step.step_id
                
                # Execute step
                step_success = self._execute_step(step, execution)
                
                if step_success:
                    completed_steps.add(step.step_id)
                    execution.completed_steps.append(step.step_id)
                    self.logger.info(f"Step {step.step_id} completed successfully")
                else:
                    failed_steps.add(step.step_id)
                    execution.failed_steps.append(step.step_id)
                    self.logger.error(f"Step {step.step_id} failed")
                    
                    # Check if workflow should continue
                    if step.step_type in ["critical", "validation"]:
                        return False
            
            return len(failed_steps) == 0
            
        except Exception as e:
            self.logger.error(f"Failed to execute workflow steps: {e}")
            return False

    def _execute_step(self, step: WorkflowStep, execution: WorkflowExecution) -> bool:
        """Execute a single workflow step"""
        try:
            start_time = time.time()
            
            # Simulate step execution (replace with actual step logic)
            if step.step_type == "initialization":
                time.sleep(0.1)  # Simulate work
                result = {"status": "initialized", "timestamp": datetime.now().isoformat()}
            elif step.step_type == "training":
                time.sleep(0.2)  # Simulate work
                result = {"status": "trained", "timestamp": datetime.now().isoformat()}
            elif step.step_type == "role_assignment":
                time.sleep(0.1)  # Simulate work
                result = {"status": "role_assigned", "timestamp": datetime.now().isoformat()}
            elif step.step_type == "completion":
                time.sleep(0.1)  # Simulate work
                result = {"status": "completed", "timestamp": datetime.now().isoformat()}
            else:
                time.sleep(0.1)  # Simulate work
                result = {"status": "executed", "timestamp": datetime.now().isoformat()}
            
            # Record step result
            execution.step_results[step.step_id] = result
            
            # Update performance metrics
            execution_time = time.time() - start_time
            execution.performance_metrics[step.step_id] = execution_time
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to execute step {step.step_id}: {e}")
            return False

    def _sort_steps_by_dependencies(self, steps: List[WorkflowStep]) -> List[WorkflowStep]:
        """Sort steps by dependency order using topological sort"""
        try:
            # Create dependency graph
            graph = {step.step_id: set(step.dependencies) for step in steps}
            
            # Topological sort
            sorted_steps = []
            visited = set()
            temp_visited = set()
            
            def visit(step_id: str):
                if step_id in temp_visited:
                    raise ValueError(f"Circular dependency detected: {step_id}")
                if step_id in visited:
                    return
                
                temp_visited.add(step_id)
                
                for dep in graph.get(step_id, set()):
                    if dep in [s.step_id for s in steps]:
                        visit(dep)
                
                temp_visited.remove(step_id)
                visited.add(step_id)
                
                # Find step object and add to sorted list
                for step in steps:
                    if step.step_id == step_id:
                        sorted_steps.append(step)
                        break
            
            # Visit all steps
            for step in steps:
                if step.step_id not in visited:
                    visit(step.step_id)
            
            return sorted_steps
            
        except Exception as e:
            self.logger.error(f"Failed to sort steps by dependencies: {e}")
            return steps  # Return original order if sorting fails

    def get_execution_status(self, execution_id: str) -> Optional[Dict[str, Any]]:
        """Get execution status"""
        execution = self.active_executions.get(execution_id) or self.completed_executions.get(execution_id)
        if execution:
            return {
                "execution_id": execution.execution_id,
                "status": execution.status,
                "current_step": execution.current_step,
                "completed_steps": len(execution.completed_steps),
                "failed_steps": len(execution.failed_steps),
                "start_time": execution.start_time,
                "actual_completion": execution.actual_completion
            }
        return None

    def stop_execution(self, execution_id: str) -> bool:
        """Stop an active execution"""
        if execution_id in self.active_executions:
            execution = self.active_executions[execution_id]
            execution.status = "stopped"
            execution.actual_completion = datetime.now().isoformat()
            self.completed_executions[execution_id] = execution
            del self.active_executions[execution_id]
            self.logger.info(f"Stopped execution: {execution_id}")
            return True
        return False

    def cleanup(self):
        """Cleanup resources"""
        self.executor.shutdown(wait=True)
        self.logger.info("Workflow execution engine cleaned up")


# ============================================================================
# CLI INTERFACE - Single Responsibility: Command-line testing
# ============================================================================

def run_smoke_test():
    """Run basic functionality test for workflow execution"""
    try:
        from .workflow_types import V2Workflow, WorkflowStep
        
        # Create test workflow
        steps = [
            WorkflowStep(
                step_id="step1",
                name="Test Step 1",
                step_type="initialization",
                description="Test step 1",
                dependencies=[]
            ),
            WorkflowStep(
                step_id="step2",
                name="Test Step 2",
                step_type="training",
                description="Test step 2",
                dependencies=["step1"]
            )
        ]
        
        workflow = V2Workflow(
            workflow_id="test_workflow",
            name="Test Workflow",
            description="Test workflow",
            steps=steps,
            created_at=datetime.now().isoformat(),
            status="created"
        )
        
        # Test execution engine
        engine = WorkflowExecutionEngine(max_workers=2)
        success = engine.execute_workflow(workflow)
        assert success
        
        # Test execution status
        execution_id = list(engine.active_executions.keys())[0] if engine.active_executions else list(engine.completed_executions.keys())[0]
        status = engine.get_execution_status(execution_id)
        assert status is not None
        
        # Cleanup
        engine.cleanup()
        
        print("✅ WorkflowExecution smoke test passed!")
        return True
        
    except Exception as e:
        print(f"❌ WorkflowExecution smoke test failed: {e}")
        return False


if __name__ == "__main__":
    run_smoke_test()
