#!/usr/bin/env python3
"""
FSM Execution Engine - Workflow execution management for FSM system

Single Responsibility: Execute workflows and manage state machine execution.
Follows V2 standards: ≤400 LOC, OOP design, SRP compliance.
"""

import logging
import time
import threading
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, Future

from fsm.states import StateStatus, WorkflowInstance, StateExecutionResult
from fsm_transitions import TransitionManager


class ExecutionEngine:
    """Executes FSM workflows and manages state machine execution."""
    
    def __init__(self, transition_manager: TransitionManager):
        self.transition_manager = transition_manager
        self.logger = logging.getLogger(__name__)
        self.executing_workflows: Dict[str, Dict[str, Any]] = {}
        self.execution_history: List[Dict[str, Any]] = []
        self.executor = ThreadPoolExecutor(max_workers=10)
        self.lock = threading.Lock()
        
    def start_workflow_execution(self, workflow: WorkflowInstance, 
                                initial_context: Dict[str, Any] = None) -> bool:
        """Start execution of a workflow."""
        try:
            with self.lock:
                if workflow.workflow_id in self.executing_workflows:
                    self.logger.warning(f"Workflow {workflow.workflow_id} already executing")
                    return False
                
                execution_context = {
                    "workflow": workflow,
                    "context": initial_context or {},
                    "start_time": datetime.now(),
                    "current_state": workflow.current_state,
                    "status": StateStatus.ACTIVE,
                    "execution_thread": None
                }
                
                self.executing_workflows[workflow.workflow_id] = execution_context
                
                # Start execution in separate thread
                future = self.executor.submit(self._execute_workflow, workflow.workflow_id)
                execution_context["execution_thread"] = future
                
                self.logger.info(f"Started workflow execution: {workflow.workflow_id}")
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to start workflow execution: {e}")
            return False
    
    def _execute_workflow(self, workflow_id: str) -> None:
        """Execute workflow in separate thread."""
        try:
            execution_context = self.executing_workflows.get(workflow_id)
            if not execution_context:
                self.logger.error(f"Execution context not found for workflow: {workflow_id}")
                return
            
            workflow = execution_context["workflow"]
            context = execution_context["context"]
            
            self.logger.info(f"Executing workflow: {workflow_id}")
            
            # Execute workflow until completion or failure
            while execution_context["status"] == StateStatus.ACTIVE:
                current_state = execution_context["current_state"]
                
                # Execute current state
                state_result = self._execute_state(workflow_id, current_state, context)
                
                if not state_result.success:
                    execution_context["status"] = StateStatus.FAILED
                    self.logger.error(f"State execution failed: {state_result.error_message}")
                    break
                
                # Find next state
                next_state = self._determine_next_state(workflow_id, current_state, context)
                
                if not next_state:
                    execution_context["status"] = StateStatus.COMPLETED
                    self.logger.info(f"Workflow {workflow_id} completed")
                    break
                
                # Execute transition
                transition_result = self.transition_manager.execute_transition(
                    current_state, next_state, workflow_id, context
                )
                
                if not transition_result.success:
                    execution_context["status"] = StateStatus.FAILED
                    self.logger.error(f"Transition failed: {transition_result.error_message}")
                    break
                
                # Update execution context
                execution_context["current_state"] = next_state
                workflow.current_state = next_state
                workflow.last_transition = datetime.now()
                
                # Update context with transition result
                context.update(transition_result.metadata or {})
                
                # Small delay to prevent tight loops
                time.sleep(0.1)
            
            # Record execution completion
            self._record_execution_completion(workflow_id, execution_context)
            
        except Exception as e:
            self.logger.error(f"Workflow execution failed: {e}")
            with self.lock:
                if workflow_id in self.executing_workflows:
                    self.executing_workflows[workflow_id]["status"] = StateStatus.FAILED
    
    def _execute_state(self, workflow_id: str, state_name: str, 
                      context: Dict[str, Any]) -> StateExecutionResult:
        """Execute a single state."""
        start_time = time.time()
        
        try:
            # Simple state execution (can be extended with actual state logic)
            self.logger.debug(f"Executing state: {state_name} for workflow: {workflow_id}")
            
            # Simulate state execution time
            time.sleep(0.01)
            
            execution_time = time.time() - start_time
            return StateExecutionResult(
                state_name=state_name,
                success=True,
                execution_time=execution_time,
                metadata={"workflow_id": workflow_id, "context": context}
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            return StateExecutionResult(
                state_name=state_name,
                success=False,
                execution_time=execution_time,
                error_message=str(e)
            )
    
    def _determine_next_state(self, workflow_id: str, current_state: str, 
                             context: Dict[str, Any]) -> Optional[str]:
        """Determine the next state based on current state and context."""
        try:
            available_transitions = self.transition_manager.get_available_transitions(current_state)
            
            if not available_transitions:
                return None
            
            # Simple logic: take first available transition
            # Can be extended with more sophisticated decision logic
            next_transition = available_transitions[0]
            return next_transition.to_state
            
        except Exception as e:
            self.logger.error(f"Failed to determine next state: {e}")
            return None
    
    def _record_execution_completion(self, workflow_id: str, execution_context: Dict[str, Any]) -> None:
        """Record workflow execution completion."""
        try:
            completion_record = {
                "workflow_id": workflow_id,
                "start_time": execution_context["start_time"],
                "end_time": datetime.now(),
                "final_status": execution_context["status"],
                "final_state": execution_context["current_state"],
                "context": execution_context["context"]
            }
            
            self.execution_history.append(completion_record)
            
            # Clean up execution context
            with self.lock:
                if workflow_id in self.executing_workflows:
                    del self.executing_workflows[workflow_id]
            
            self.logger.info(f"Workflow execution completed: {workflow_id}")
            
        except Exception as e:
            self.logger.error(f"Failed to record execution completion: {e}")
    
    def get_workflow_status(self, workflow_id: str) -> Optional[StateStatus]:
        """Get current status of a workflow."""
        with self.lock:
            if workflow_id in self.executing_workflows:
                return self.executing_workflows[workflow_id]["status"]
        
        # Check execution history
        for record in self.execution_history:
            if record["workflow_id"] == workflow_id:
                return record["final_status"]
        
        return None
    
    def stop_workflow_execution(self, workflow_id: str) -> bool:
        """Stop execution of a workflow."""
        try:
            with self.lock:
                if workflow_id not in self.executing_workflows:
                    self.logger.warning(f"Workflow {workflow_id} not executing")
                    return False
                
                execution_context = self.executing_workflows[workflow_id]
                execution_context["status"] = StateStatus.FAILED
                
                # Cancel execution thread if running
                if execution_context["execution_thread"]:
                    execution_context["execution_thread"].cancel()
                
                self.logger.info(f"Stopped workflow execution: {workflow_id}")
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to stop workflow execution: {e}")
            return False
    
    def get_execution_history(self, workflow_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get execution history, optionally filtered by workflow."""
        if workflow_id:
            return [record for record in self.execution_history 
                   if record["workflow_id"] == workflow_id]
        return self.execution_history.copy()
    
    def clear_execution_history(self) -> None:
        """Clear execution history."""
        self.execution_history.clear()
        self.logger.info("Execution history cleared")
    
    def shutdown(self) -> None:
        """Shutdown execution engine."""
        try:
            # Stop all executing workflows
            workflow_ids = list(self.executing_workflows.keys())
            for workflow_id in workflow_ids:
                self.stop_workflow_execution(workflow_id)
            
            # Shutdown thread pool
            self.executor.shutdown(wait=True)
            
            self.logger.info("Execution engine shutdown complete")
            
        except Exception as e:
            self.logger.error(f"Failed to shutdown execution engine: {e}")


class ExecutionMonitor:
    """Monitors workflow execution and provides metrics."""
    
    def __init__(self, execution_engine: ExecutionEngine):
        self.execution_engine = execution_engine
        self.logger = logging.getLogger(__name__)
        self.metrics: Dict[str, Any] = {
            "total_workflows": 0,
            "completed_workflows": 0,
            "failed_workflows": 0,
            "active_workflows": 0,
            "average_execution_time": 0.0
        }
    
    def update_metrics(self) -> None:
        """Update execution metrics."""
        try:
            history = self.execution_engine.get_execution_history()
            active_workflows = len(self.execution_engine.executing_workflows)
            
            self.metrics["total_workflows"] = len(history) + active_workflows
            self.metrics["active_workflows"] = active_workflows
            self.metrics["completed_workflows"] = len([r for r in history if r["final_status"] == StateStatus.COMPLETED])
            self.metrics["failed_workflows"] = len([r for r in history if r["final_status"] == StateStatus.FAILED])
            
            # Calculate average execution time
            completed_workflows = [r for r in history if r["final_status"] == StateStatus.COMPLETED]
            if completed_workflows:
                total_time = sum((r["end_time"] - r["start_time"]).total_seconds() 
                               for r in completed_workflows)
                self.metrics["average_execution_time"] = total_time / len(completed_workflows)
            
        except Exception as e:
            self.logger.error(f"Failed to update metrics: {e}")
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current execution metrics."""
        self.update_metrics()
        return self.metrics.copy()
    
    def get_workflow_performance(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get performance metrics for a specific workflow."""
        try:
            history = self.execution_engine.get_execution_history(workflow_id)
            if not history:
                return None
            
            record = history[0]  # Most recent execution
            execution_time = (record["end_time"] - record["start_time"]).total_seconds()
            
            return {
                "workflow_id": workflow_id,
                "execution_time": execution_time,
                "status": record["final_status"],
                "start_time": record["start_time"],
                "end_time": record["end_time"]
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get workflow performance: {e}")
            return None


def main():
    """CLI interface for FSM Execution Engine testing."""
    import argparse
    
    parser = argparse.ArgumentParser(description="FSM Execution Engine - V2 Standards Compliant")
    parser.add_argument("--test", action="store_true", help="Run smoke tests")
    
    args = parser.parse_args()
    
    if args.test:
        run_smoke_tests()
    else:
        parser.print_help()


def run_smoke_tests():
    """Run smoke tests for FSM Execution Engine."""
    print("🧪 Running FSM Execution Engine smoke tests...")
    
    # Test execution engine creation
    
    transition_manager = TransitionManager()
    execution_engine = ExecutionEngine(transition_manager)
    assert execution_engine is not None
    print("✅ ExecutionEngine creation test passed")
    
    # Test execution monitor
    monitor = ExecutionMonitor(execution_engine)
    assert monitor is not None
    print("✅ ExecutionMonitor creation test passed")
    
    # Test metrics
    metrics = monitor.get_metrics()
    assert isinstance(metrics, dict)
    print("✅ Metrics test passed")
    
    print("🎉 All smoke tests passed!")


if __name__ == "__main__":
    main()
