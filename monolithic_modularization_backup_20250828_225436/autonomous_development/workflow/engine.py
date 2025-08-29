#!/usr/bin/env python3
"""
Workflow Engine - Autonomous Development
======================================

Manages and orchestrates autonomous development workflows.
Extracted from the main autonomous_development.py file to follow SRP.
"""

import time
import threading
import logging
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from datetime import datetime

from src.utils.stability_improvements import stability_manager, safe_import


@dataclass
class WorkflowStep:
    """Represents a single step in a development workflow"""
    
    step_id: str
    step_type: str  # 'code_review', 'documentation', 'testing', 'optimization'
    action: Callable
    dependencies: List[str] = None
    timeout: float = 30.0
    retry_count: int = 0
    max_retries: int = 3


class WorkflowEngine:
    """
    Manages autonomous development workflows and execution cycles.
    
    Responsibilities:
    - Workflow orchestration and execution
    - Cycle management and timing
    - Error handling and recovery
    - Performance monitoring
    """
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.WorkflowEngine")
        self.is_running = False
        self.workflow_thread = None
        self.cycle_count = 0
        self.active_workflows = {}
        self.workflow_history = []
        
        # Performance tracking
        self.start_time = None
        self.total_cycles = 0
        self.successful_cycles = 0
        self.failed_cycles = 0
        
        # Stability management
        self.stability_manager = stability_manager
        
    def start_workflow_engine(self) -> bool:
        """Start the workflow engine"""
        if self.is_running:
            self.logger.warning("Workflow engine already running")
            return False
            
        self.is_running = True
        self.start_time = datetime.now()
        self.logger.info("🚀 Workflow Engine Started")
        
        # Start workflow execution thread
        self.workflow_thread = threading.Thread(
            target=self._workflow_execution_loop, 
            daemon=True
        )
        self.workflow_thread.start()
        
        return True
        
    def stop_workflow_engine(self):
        """Stop the workflow engine"""
        self.is_running = False
        
        if self.workflow_thread and self.workflow_thread.is_alive():
            self.workflow_thread.join(timeout=5.0)
            
        self.logger.info("⏹️ Workflow Engine Stopped")
        
    def register_workflow(self, workflow_id: str, steps: List[WorkflowStep]) -> bool:
        """Register a new workflow with the engine"""
        try:
            if workflow_id in self.active_workflows:
                self.logger.warning(f"Workflow {workflow_id} already registered")
                return False
                
            self.active_workflows[workflow_id] = {
                'steps': steps,
                'current_step': 0,
                'status': 'registered',
                'start_time': datetime.now(),
                'completed_steps': []
            }
            
            self.logger.info(f"Workflow {workflow_id} registered with {len(steps)} steps")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to register workflow {workflow_id}: {e}")
            return False
            
    def execute_workflow(self, workflow_id: str) -> bool:
        """Execute a registered workflow"""
        if workflow_id not in self.active_workflows:
            self.logger.error(f"Workflow {workflow_id} not found")
            return False
            
        workflow = self.active_workflows[workflow_id]
        workflow['status'] = 'executing'
        
        try:
            for i, step in enumerate(workflow['steps']):
                if not self.is_running:
                    break
                    
                self.logger.info(f"Executing workflow {workflow_id}, step {i+1}/{len(workflow['steps'])}")
                
                # Execute step with timeout and retry logic
                success = self._execute_workflow_step(workflow_id, step, i)
                
                if success:
                    workflow['completed_steps'].append(step.step_id)
                    workflow['current_step'] = i + 1
                else:
                    self.logger.error(f"Workflow {workflow_id} failed at step {step.step_id}")
                    workflow['status'] = 'failed'
                    return False
                    
            workflow['status'] = 'completed'
            self.logger.info(f"Workflow {workflow_id} completed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Workflow {workflow_id} execution failed: {e}")
            workflow['status'] = 'failed'
            return False
            
    def _execute_workflow_step(self, workflow_id: str, step: WorkflowStep, step_index: int) -> bool:
        """Execute a single workflow step with retry logic"""
        for attempt in range(step.max_retries + 1):
            try:
                # Execute the step action
                result = step.action()
                
                if result:
                    self.logger.info(f"Workflow {workflow_id} step {step.step_id} completed")
                    return True
                else:
                    self.logger.warning(f"Workflow {workflow_id} step {step.step_id} returned False")
                    
            except Exception as e:
                self.logger.error(f"Workflow {workflow_id} step {step.step_id} attempt {attempt + 1} failed: {e}")
                
            # Wait before retry
            if attempt < step.max_retries:
                time.sleep(1.0)
                
        return False
        
    def _workflow_execution_loop(self):
        """Main workflow execution loop"""
        while self.is_running:
            try:
                start_time = time.time()
                
                # Execute pending workflows
                self._process_pending_workflows()
                
                # Update metrics
                self.cycle_count += 1
                self.total_cycles += 1
                
                # Brief pause between cycles
                time.sleep(2)
                
            except Exception as e:
                self.logger.error(f"Workflow execution cycle error: {e}")
                self.failed_cycles += 1
                time.sleep(5)  # Recovery pause
                
    def _process_pending_workflows(self):
        """Process all pending workflows"""
        for workflow_id, workflow in self.active_workflows.items():
            if workflow['status'] == 'registered':
                self.execute_workflow(workflow_id)
                
    def get_workflow_status(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get the current status of a workflow"""
        return self.active_workflows.get(workflow_id)
        
    def get_pending_actions(self) -> List[Dict[str, Any]]:
        """Get pending actions from workflow engine"""
        pending_actions = []
        for workflow_id, workflow in self.active_workflows.items():
            if workflow['status'] == 'registered':
                pending_actions.append({
                    'workflow_id': workflow_id,
                    'status': workflow['status'],
                    'steps_count': len(workflow['steps'])
                })
        return pending_actions
        
    def get_workflow_status(self) -> Dict[str, Any]:
        """Get workflow engine status"""
        return {
            'is_running': self.is_running,
            'active_workflows': len([w for w in self.active_workflows.values() if w['status'] == 'executing']),
            'registered_workflows': len([w for w in self.active_workflows.values() if w['status'] == 'registered']),
            'completed_workflows': len([w for w in self.active_workflows.values() if w['status'] == 'completed'])
        }
        
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get workflow engine performance metrics"""
        uptime = (datetime.now() - self.start_time).total_seconds() if self.start_time else 0
        
        return {
            'is_running': self.is_running,
            'uptime_seconds': uptime,
            'total_cycles': self.total_cycles,
            'successful_cycles': self.successful_cycles,
            'failed_cycles': self.failed_cycles,
            'active_workflows': len([w for w in self.active_workflows.values() if w['status'] == 'executing']),
            'registered_workflows': len([w for w in self.active_workflows.values() if w['status'] == 'registered']),
            'completed_workflows': len([w for w in self.active_workflows.values() if w['status'] == 'completed'])
        }
        
    def cleanup(self):
        """Cleanup workflow engine resources"""
        self.stop_workflow_engine()
