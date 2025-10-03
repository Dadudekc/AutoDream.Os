#!/usr/bin/env python3
"""
Workflow System - Simple Agent Coordination
==========================================

Simple workflow system that uses messaging instead of complex coordination files.
Replaces all the complex coordination systems with simple workflow chains.

Author: Agent-4 (Captain & Operations Coordinator)
License: MIT
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import logging

from .messaging_service import ConsolidatedMessagingService

logger = logging.getLogger(__name__)


@dataclass
class WorkflowStep:
    """Single step in a workflow."""
    agent: str
    task: str
    priority: str = "normal"
    completed: bool = False
    timestamp: Optional[datetime] = None


class WorkflowChain:
    """Simple workflow chain using messaging system."""
    
    def __init__(self, messaging_service: ConsolidatedMessagingService):
        """Initialize workflow chain."""
        self.messaging = messaging_service
        self.steps: List[WorkflowStep] = []
        self.current_step = 0
    
    def add_step(self, agent: str, task: str, priority: str = "normal"):
        """Add a step to the workflow."""
        step = WorkflowStep(
            agent=agent,
            task=task,
            priority=priority,
            timestamp=datetime.now()
        )
        self.steps.append(step)
        logger.info(f"Added workflow step: {agent} - {task}")
    
    def execute_next(self) -> bool:
        """Execute the next step in the workflow."""
        if self.current_step >= len(self.steps):
            logger.info("Workflow completed")
            return False
        
        step = self.steps[self.current_step]
        
        # Send message to agent
        self.messaging.send_message(
            agent=step.agent,
            message=step.task,
            priority=step.priority
        )
        
        logger.info(f"Executed workflow step {self.current_step + 1}: {step.agent} - {step.task}")
        self.current_step += 1
        return True
    
    def execute_all(self):
        """Execute all remaining steps in the workflow."""
        while self.execute_next():
            pass
    
    def get_status(self) -> Dict[str, Any]:
        """Get workflow status."""
        return {
            'total_steps': len(self.steps),
            'current_step': self.current_step,
            'completed_steps': self.current_step,
            'remaining_steps': len(self.steps) - self.current_step,
            'progress_percent': (self.current_step / len(self.steps) * 100) if self.steps else 0
        }


class WorkflowManager:
    """Manages multiple workflows using messaging system."""
    
    def __init__(self):
        """Initialize workflow manager."""
        self.messaging = ConsolidatedMessagingService()
        self.workflows: Dict[str, WorkflowChain] = {}
    
    def create_workflow(self, name: str) -> WorkflowChain:
        """Create a new workflow."""
        workflow = WorkflowChain(self.messaging)
        self.workflows[name] = workflow
        logger.info(f"Created workflow: {name}")
        return workflow
    
    def get_workflow(self, name: str) -> Optional[WorkflowChain]:
        """Get workflow by name."""
        return self.workflows.get(name)
    
    def execute_workflow(self, name: str):
        """Execute a workflow."""
        workflow = self.get_workflow(name)
        if workflow:
            workflow.execute_all()
        else:
            logger.error(f"Workflow {name} not found")
    
    def get_all_status(self) -> Dict[str, Any]:
        """Get status of all workflows."""
        status = {}
        for name, workflow in self.workflows.items():
            status[name] = workflow.get_status()
        return status


# Predefined workflows to replace complex coordination files
class PredefinedWorkflows:
    """Predefined workflows that replace complex coordination systems."""
    
    @staticmethod
    def testing_coordination(messaging: ConsolidatedMessagingService) -> WorkflowChain:
        """Testing coordination workflow."""
        workflow = WorkflowChain(messaging)
        workflow.add_step("Agent-7", "Implement testing validation", "normal")
        workflow.add_step("Agent-8", "Review testing implementation", "normal")
        workflow.add_step("Agent-4", "Approve testing implementation", "normal")
        return workflow
    
    @staticmethod
    def qa_coordination(messaging: ConsolidatedMessagingService) -> WorkflowChain:
        """QA coordination workflow."""
        workflow = WorkflowChain(messaging)
        workflow.add_step("Agent-6", "Perform QA validation", "normal")
        workflow.add_step("Agent-8", "Review QA results", "normal")
        workflow.add_step("Agent-4", "Approve QA results", "normal")
        return workflow
    
    @staticmethod
    def integration_coordination(messaging: ConsolidatedMessagingService) -> WorkflowChain:
        """Integration coordination workflow."""
        workflow = WorkflowChain(messaging)
        workflow.add_step("Agent-1", "Implement integration components", "normal")
        workflow.add_step("Agent-8", "Review integration", "normal")
        workflow.add_step("Agent-4", "Approve integration", "normal")
        return workflow
    
    @staticmethod
    def deployment_coordination(messaging: ConsolidatedMessagingService) -> WorkflowChain:
        """Deployment coordination workflow."""
        workflow = WorkflowChain(messaging)
        workflow.add_step("Agent-3", "Prepare deployment environment", "normal")
        workflow.add_step("Agent-7", "Deploy application", "normal")
        workflow.add_step("Agent-4", "Monitor deployment", "normal")
        return workflow


# Simple workflow execution functions
def execute_testing_workflow():
    """Execute testing workflow using messaging."""
    messaging = ConsolidatedMessagingService()
    workflow = PredefinedWorkflows.testing_coordination(messaging)
    workflow.execute_all()


def execute_qa_workflow():
    """Execute QA workflow using messaging."""
    messaging = ConsolidatedMessagingService()
    workflow = PredefinedWorkflows.qa_coordination(messaging)
    workflow.execute_all()


def execute_integration_workflow():
    """Execute integration workflow using messaging."""
    messaging = ConsolidatedMessagingService()
    workflow = PredefinedWorkflows.integration_coordination(messaging)
    workflow.execute_all()


def execute_deployment_workflow():
    """Execute deployment workflow using messaging."""
    messaging = ConsolidatedMessagingService()
    workflow = PredefinedWorkflows.deployment_coordination(messaging)
    workflow.execute_all()