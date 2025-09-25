#!/usr/bin/env python3
"""
Agent Workflow Manager
======================

Manages complex multi-agent workflows with automated coordination,
status tracking, and dependency management.
V2 Compliance: ≤400 lines, focused management functionality.
"""

import json
import logging
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
import argparse
import sys

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from tools.workflow.core import (
    WorkflowStep, WorkflowDefinition, WorkflowValidator, 
    WorkflowScheduler, WorkflowStatusTracker
)
from tools.workflow.automation import WorkflowAutomation
from src.services.consolidated_messaging_service import ConsolidatedMessagingService

logger = logging.getLogger(__name__)


class WorkflowManager:
    """Manages complex multi-agent workflows."""
    
    def __init__(self, config_file: Optional[str] = None):
        """Initialize workflow manager."""
        self.logger = logging.getLogger(__name__)
        self.messaging_service = ConsolidatedMessagingService()
        self.automation = WorkflowAutomation()
        self.status_tracker = WorkflowStatusTracker()
        
        # Load configuration
        self.config = self._load_config(config_file)
        self.workflows_dir = Path(self.config.get("workflows_dir", "workflows"))
        self.workflows_dir.mkdir(exist_ok=True)
    
    def _load_config(self, config_file: Optional[str]) -> Dict[str, Any]:
        """Load configuration from file or use defaults."""
        default_config = {
            "workflows_dir": "workflows",
            "max_concurrent_workflows": 5,
            "default_timeout_minutes": 30,
            "retry_failed_steps": True,
            "max_retries": 3
        }
        
        if config_file and Path(config_file).exists():
            try:
                with open(config_file, 'r') as f:
                    user_config = json.load(f)
                default_config.update(user_config)
            except Exception as e:
                self.logger.warning(f"Could not load config file {config_file}: {e}")
        
        return default_config
    
    def create_workflow(self, workflow_id: str, name: str, description: str, 
                       steps: List[Dict[str, Any]]) -> WorkflowDefinition:
        """Create a new workflow definition."""
        workflow_steps = []
        for step_data in steps:
            step = WorkflowStep(
                step_id=step_data["step_id"],
                agent_id=step_data["agent_id"],
                task=step_data["task"],
                dependencies=step_data.get("dependencies", []),
                timeout_minutes=step_data.get("timeout_minutes", self.config["default_timeout_minutes"])
            )
            workflow_steps.append(step)
        
        workflow = WorkflowDefinition(
            workflow_id=workflow_id,
            name=name,
            description=description,
            steps=workflow_steps
        )
        
        # Validate workflow
        errors = WorkflowValidator.validate_workflow(workflow)
        if errors:
            raise ValueError(f"Workflow validation failed: {errors}")
        
        return workflow
    
    def save_workflow(self, workflow: WorkflowDefinition) -> bool:
        """Save workflow definition to file."""
        try:
            workflow_file = self.workflows_dir / f"{workflow.workflow_id}.json"
            with open(workflow_file, 'w') as f:
                json.dump(workflow.to_dict(), f, indent=2)
            
            self.logger.info(f"Saved workflow: {workflow.name}")
            return True
        except Exception as e:
            self.logger.error(f"Error saving workflow: {e}")
            return False
    
    def load_workflow(self, workflow_id: str) -> Optional[WorkflowDefinition]:
        """Load workflow definition from file."""
        try:
            workflow_file = self.workflows_dir / f"{workflow_id}.json"
            if not workflow_file.exists():
                self.logger.warning(f"Workflow file not found: {workflow_file}")
                return None
            
            with open(workflow_file, 'r') as f:
                data = json.load(f)
            
            return WorkflowDefinition.from_dict(data)
        except Exception as e:
            self.logger.error(f"Error loading workflow {workflow_id}: {e}")
            return None
    
    def execute_workflow(self, workflow: WorkflowDefinition) -> Dict[str, Any]:
        """Execute a complete workflow."""
        self.logger.info(f"Starting workflow execution: {workflow.name}")
        
        # Start tracking
        if not self.status_tracker.start_workflow(workflow):
            return {"success": False, "error": "Workflow already active"}
        
        try:
            # Get execution order
            execution_order = WorkflowScheduler.get_execution_order(workflow.steps)
            self.logger.info(f"Execution order: {execution_order}")
            
            # Execute steps in order
            results = {}
            for step_id in execution_order:
                step = next(s for s in workflow.steps if s.step_id == step_id)
                
                # Check if dependencies are completed
                if not self._check_dependencies(step, workflow.steps):
                    self.logger.error(f"Dependencies not met for step: {step_id}")
                    workflow.status = "failed"
                    return {"success": False, "error": f"Dependencies not met for {step_id}"}
                
                # Execute step
                step_result = self.automation.execute_workflow_step(step)
                results[step_id] = step_result
                
                # Check for failure
                if not step_result["success"]:
                    workflow.status = "failed"
                    self.status_tracker.complete_workflow(workflow.workflow_id, False)
                    return {"success": False, "error": f"Step {step_id} failed", "results": results}
            
            # Mark workflow as completed
            workflow.status = "completed"
            self.status_tracker.complete_workflow(workflow.workflow_id, True)
            
            self.logger.info(f"Workflow completed successfully: {workflow.name}")
            return {"success": True, "results": results}
            
        except Exception as e:
            workflow.status = "failed"
            self.status_tracker.complete_workflow(workflow.workflow_id, False)
            self.logger.error(f"Workflow execution failed: {e}")
            return {"success": False, "error": str(e)}
    
    def _check_dependencies(self, step: WorkflowStep, all_steps: List[WorkflowStep]) -> bool:
        """Check if all dependencies for a step are completed."""
        for dep_id in step.dependencies:
            dep_step = next((s for s in all_steps if s.step_id == dep_id), None)
            if not dep_step or dep_step.status != "completed":
                return False
        return True
    
    def get_workflow_status(self, workflow_id: str) -> Optional[str]:
        """Get the status of a workflow."""
        return self.status_tracker.get_workflow_status(workflow_id)
    
    def list_workflows(self) -> List[Dict[str, Any]]:
        """List all available workflows."""
        workflows = []
        for workflow_file in self.workflows_dir.glob("*.json"):
            try:
                with open(workflow_file, 'r') as f:
                    data = json.load(f)
                workflows.append({
                    "workflow_id": data["workflow_id"],
                    "name": data["name"],
                    "description": data["description"],
                    "status": data.get("status", "unknown"),
                    "created_at": data.get("created_at", "unknown")
                })
            except Exception as e:
                self.logger.warning(f"Could not load workflow {workflow_file}: {e}")
        
        return workflows
    
    def cancel_workflow(self, workflow_id: str) -> bool:
        """Cancel a running workflow."""
        if workflow_id in self.status_tracker.active_workflows:
            workflow = self.status_tracker.active_workflows[workflow_id]
            workflow.status = "cancelled"
            self.status_tracker.complete_workflow(workflow_id, False)
            self.logger.info(f"Cancelled workflow: {workflow.name}")
            return True
        return False


def main():
    """Main CLI interface for workflow manager."""
    parser = argparse.ArgumentParser(description="Agent Workflow Manager")
    parser.add_argument("--config", help="Configuration file path")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Create workflow command
    create_parser = subparsers.add_parser("create", help="Create a new workflow")
    create_parser.add_argument("--workflow-id", required=True, help="Workflow ID")
    create_parser.add_argument("--name", required=True, help="Workflow name")
    create_parser.add_argument("--description", required=True, help="Workflow description")
    create_parser.add_argument("--steps", required=True, help="JSON file with steps definition")
    
    # Execute workflow command
    execute_parser = subparsers.add_parser("execute", help="Execute a workflow")
    execute_parser.add_argument("--workflow-id", required=True, help="Workflow ID to execute")
    
    # List workflows command
    list_parser = subparsers.add_parser("list", help="List all workflows")
    
    # Status command
    status_parser = subparsers.add_parser("status", help="Get workflow status")
    status_parser.add_argument("--workflow-id", required=True, help="Workflow ID")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    
    manager = WorkflowManager(args.config)
    
    if args.command == "create":
        # Load steps from file
        with open(args.steps, 'r') as f:
            steps_data = json.load(f)
        
        workflow = manager.create_workflow(
            args.workflow_id, args.name, args.description, steps_data
        )
        manager.save_workflow(workflow)
        print(f"Created workflow: {workflow.name}")
    
    elif args.command == "execute":
        workflow = manager.load_workflow(args.workflow_id)
        if workflow:
            result = manager.execute_workflow(workflow)
            print(f"Execution result: {result}")
        else:
            print(f"Workflow {args.workflow_id} not found")
    
    elif args.command == "list":
        workflows = manager.list_workflows()
        for workflow in workflows:
            print(f"{workflow['workflow_id']}: {workflow['name']} ({workflow['status']})")
    
    elif args.command == "status":
        status = manager.get_workflow_status(args.workflow_id)
        print(f"Workflow {args.workflow_id} status: {status}")


if __name__ == "__main__":
    main()




