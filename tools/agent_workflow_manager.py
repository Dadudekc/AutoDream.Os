#!/usr/bin/env python3
"""
Agent Workflow Manager - Automated Workflow Coordination System
==============================================================

Manages complex multi-agent workflows with automated coordination,
status tracking, and dependency management.

Author: Agent-4 (Captain & Operations Coordinator)
License: MIT
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
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.consolidated_messaging_service import ConsolidatedMessagingService

logger = logging.getLogger(__name__)


class WorkflowStep:
    """Represents a single step in a workflow."""
    
    def __init__(self, step_id: str, agent_id: str, task: str, 
                 dependencies: List[str] = None, timeout_minutes: int = 30):
        self.step_id = step_id
        self.agent_id = agent_id
        self.task = task
        self.dependencies = dependencies or []
        self.timeout_minutes = timeout_minutes
        self.status = "pending"  # pending, in_progress, completed, failed, timeout
        self.started_at = None
        self.completed_at = None
        self.result = None
        self.error = None

    def to_dict(self):
        return {
            "step_id": self.step_id,
            "agent_id": self.agent_id,
            "task": self.task,
            "dependencies": self.dependencies,
            "timeout_minutes": self.timeout_minutes,
            "status": self.status,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "result": self.result,
            "error": self.error
        }

    @classmethod
    def from_dict(cls, data: Dict):
        step = cls(
            step_id=data["step_id"],
            agent_id=data["agent_id"],
            task=data["task"],
            dependencies=data.get("dependencies", []),
            timeout_minutes=data.get("timeout_minutes", 30)
        )
        step.status = data.get("status", "pending")
        step.started_at = data.get("started_at")
        step.completed_at = data.get("completed_at")
        step.result = data.get("result")
        step.error = data.get("error")
        return step


class AgentWorkflowManager:
    """Manages multi-agent workflows with automated coordination."""
    
    def __init__(self, workflow_file: str, coords_file: str = "config/coordinates.json"):
        self.workflow_file = Path(workflow_file)
        self.coords_file = coords_file
        self.messaging_service = ConsolidatedMessagingService(coords_file)
        self.workflow_data = self._load_workflow()
        self.steps = self._initialize_steps()
        
    def _load_workflow(self) -> Dict:
        """Load workflow configuration from file."""
        if not self.workflow_file.exists():
            logger.error(f"Workflow file not found: {self.workflow_file}")
            return {}
        
        try:
            with open(self.workflow_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading workflow: {e}")
            return {}
    
    def _initialize_steps(self) -> List[WorkflowStep]:
        """Initialize workflow steps from configuration."""
        steps = []
        for step_data in self.workflow_data.get("steps", []):
            steps.append(WorkflowStep.from_dict(step_data))
        return steps
    
    def _save_workflow(self):
        """Save current workflow state to file."""
        workflow_data = {
            "name": self.workflow_data.get("name", "Unnamed Workflow"),
            "description": self.workflow_data.get("description", ""),
            "created_at": self.workflow_data.get("created_at", datetime.now().isoformat()),
            "steps": [step.to_dict() for step in self.steps]
        }
        
        try:
            with open(self.workflow_file, 'w') as f:
                json.dump(workflow_data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving workflow: {e}")
    
    def get_ready_steps(self) -> List[WorkflowStep]:
        """Get steps that are ready to execute (dependencies satisfied)."""
        ready_steps = []
        completed_step_ids = {step.step_id for step in self.steps if step.status == "completed"}
        
        for step in self.steps:
            if step.status == "pending":
                if all(dep in completed_step_ids for dep in step.dependencies):
                    ready_steps.append(step)
        
        return ready_steps
    
    def execute_step(self, step: WorkflowStep) -> bool:
        """Execute a single workflow step."""
        logger.info(f"Executing step {step.step_id} for {step.agent_id}")
        
        step.status = "in_progress"
        step.started_at = datetime.now().isoformat()
        self._save_workflow()
        
        try:
            # Send task to agent
            message = f"🎯 WORKFLOW TASK: {step.task}\n\nStep ID: {step.step_id}\nTimeout: {step.timeout_minutes} minutes"
            success = self.messaging_service.send_message(
                agent_id=step.agent_id,
                message=message,
                from_agent="WorkflowManager"
            )
            
            if success:
                logger.info(f"Task sent to {step.agent_id} for step {step.step_id}")
                return True
            else:
                step.status = "failed"
                step.error = "Failed to send message to agent"
                logger.error(f"Failed to send task to {step.agent_id}")
                return False
                
        except Exception as e:
            step.status = "failed"
            step.error = str(e)
            logger.error(f"Error executing step {step.step_id}: {e}")
            return False
    
    def check_timeouts(self):
        """Check for timed out steps."""
        current_time = datetime.now()
        
        for step in self.steps:
            if step.status == "in_progress" and step.started_at:
                started_time = datetime.fromisoformat(step.started_at)
                timeout_duration = timedelta(minutes=step.timeout_minutes)
                
                if current_time - started_time > timeout_duration:
                    step.status = "timeout"
                    step.error = f"Step timed out after {step.timeout_minutes} minutes"
                    logger.warning(f"Step {step.step_id} timed out")
                    self._save_workflow()
    
    def mark_step_completed(self, step_id: str, result: str = None):
        """Mark a step as completed."""
        for step in self.steps:
            if step.step_id == step_id:
                step.status = "completed"
                step.completed_at = datetime.now().isoformat()
                step.result = result
                logger.info(f"Step {step_id} marked as completed")
                self._save_workflow()
                break
    
    def mark_step_failed(self, step_id: str, error: str):
        """Mark a step as failed."""
        for step in self.steps:
            if step.step_id == step_id:
                step.status = "failed"
                step.error = error
                logger.error(f"Step {step_id} marked as failed: {error}")
                self._save_workflow()
                break
    
    def run_workflow(self, max_concurrent: int = 2):
        """Run the entire workflow with automated coordination."""
        logger.info(f"Starting workflow: {self.workflow_data.get('name', 'Unnamed')}")
        
        while True:
            # Check for timeouts
            self.check_timeouts()
            
            # Get ready steps
            ready_steps = self.get_ready_steps()
            
            if not ready_steps:
                # Check if all steps are completed
                completed_steps = [s for s in self.steps if s.status in ["completed", "failed", "timeout"]]
                if len(completed_steps) == len(self.steps):
                    logger.info("Workflow completed!")
                    break
            
            # Execute ready steps (up to max_concurrent)
            executing_steps = [s for s in self.steps if s.status == "in_progress"]
            available_slots = max_concurrent - len(executing_steps)
            
            for step in ready_steps[:available_slots]:
                self.execute_step(step)
            
            # Wait before next iteration
            time.sleep(10)  # Check every 10 seconds
    
    def get_status(self) -> Dict:
        """Get current workflow status."""
        status_counts = {}
        for step in self.steps:
            status_counts[step.status] = status_counts.get(step.status, 0) + 1
        
        return {
            "workflow_name": self.workflow_data.get("name", "Unnamed"),
            "total_steps": len(self.steps),
            "status_counts": status_counts,
            "steps": [step.to_dict() for step in self.steps]
        }
    
    def create_sample_workflow(self, output_file: str):
        """Create a sample workflow configuration."""
        sample_workflow = {
            "name": "Tesla Stock Forecast App Development",
            "description": "Complete development workflow for Tesla stock forecasting application",
            "created_at": datetime.now().isoformat(),
            "steps": [
                {
                    "step_id": "database_setup",
                    "agent_id": "Agent-4",
                    "task": "Set up PostgreSQL database schema and SQLAlchemy models",
                    "dependencies": [],
                    "timeout_minutes": 30
                },
                {
                    "step_id": "backend_api",
                    "agent_id": "Agent-1",
                    "task": "Develop RESTful API endpoints and WebSocket support",
                    "dependencies": ["database_setup"],
                    "timeout_minutes": 45
                },
                {
                    "step_id": "frontend_gui",
                    "agent_id": "Agent-2",
                    "task": "Create React frontend with charts and responsive design",
                    "dependencies": ["backend_api"],
                    "timeout_minutes": 60
                },
                {
                    "step_id": "ml_models",
                    "agent_id": "Agent-3",
                    "task": "Implement machine learning models for stock prediction",
                    "dependencies": ["database_setup"],
                    "timeout_minutes": 90
                },
                {
                    "step_id": "integration_testing",
                    "agent_id": "Agent-4",
                    "task": "Perform end-to-end integration testing",
                    "dependencies": ["backend_api", "frontend_gui", "ml_models"],
                    "timeout_minutes": 30
                },
                {
                    "step_id": "deployment",
                    "agent_id": "Agent-4",
                    "task": "Deploy application to production environment",
                    "dependencies": ["integration_testing"],
                    "timeout_minutes": 20
                }
            ]
        }
        
        try:
            with open(output_file, 'w') as f:
                json.dump(sample_workflow, f, indent=2)
            logger.info(f"Sample workflow created: {output_file}")
        except Exception as e:
            logger.error(f"Error creating sample workflow: {e}")


def main():
    """Main CLI interface for workflow manager."""
    parser = argparse.ArgumentParser(description="Agent Workflow Manager")
    parser.add_argument("--workflow", help="Workflow configuration file")
    parser.add_argument("--coords", default="config/coordinates.json", help="Coordinates file")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Run workflow
    run_parser = subparsers.add_parser("run", help="Run workflow")
    run_parser.add_argument("--max-concurrent", type=int, default=2, help="Max concurrent steps")
    
    # Status
    subparsers.add_parser("status", help="Get workflow status")
    
    # Mark step completed
    complete_parser = subparsers.add_parser("complete", help="Mark step as completed")
    complete_parser.add_argument("--step-id", required=True, help="Step ID to mark completed")
    complete_parser.add_argument("--result", help="Result message")
    
    # Mark step failed
    fail_parser = subparsers.add_parser("fail", help="Mark step as failed")
    fail_parser.add_argument("--step-id", required=True, help="Step ID to mark failed")
    fail_parser.add_argument("--error", required=True, help="Error message")
    
    # Create sample
    sample_parser = subparsers.add_parser("create-sample", help="Create sample workflow")
    sample_parser.add_argument("--output", required=True, help="Output file path")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        if args.command == "create-sample":
            # Create sample workflow without requiring workflow file
            sample_workflow = {
                "name": "Tesla Stock Forecast App Development",
                "description": "Complete development workflow for Tesla stock forecasting application",
                "created_at": datetime.now().isoformat(),
                "steps": [
                    {
                        "step_id": "database_setup",
                        "agent_id": "Agent-4",
                        "task": "Set up PostgreSQL database schema and SQLAlchemy models",
                        "dependencies": [],
                        "timeout_minutes": 30
                    },
                    {
                        "step_id": "backend_api",
                        "agent_id": "Agent-1",
                        "task": "Develop RESTful API endpoints and WebSocket support",
                        "dependencies": ["database_setup"],
                        "timeout_minutes": 45
                    },
                    {
                        "step_id": "frontend_gui",
                        "agent_id": "Agent-2",
                        "task": "Create React frontend with charts and responsive design",
                        "dependencies": ["backend_api"],
                        "timeout_minutes": 60
                    },
                    {
                        "step_id": "ml_models",
                        "agent_id": "Agent-3",
                        "task": "Implement machine learning models for stock prediction",
                        "dependencies": ["database_setup"],
                        "timeout_minutes": 90
                    },
                    {
                        "step_id": "integration_testing",
                        "agent_id": "Agent-4",
                        "task": "Perform end-to-end integration testing",
                        "dependencies": ["backend_api", "frontend_gui", "ml_models"],
                        "timeout_minutes": 30
                    },
                    {
                        "step_id": "deployment",
                        "agent_id": "Agent-4",
                        "task": "Deploy application to production environment",
                        "dependencies": ["integration_testing"],
                        "timeout_minutes": 20
                    }
                ]
            }
            
            try:
                with open(args.output, 'w') as f:
                    json.dump(sample_workflow, f, indent=2)
                print(f"🐝 WE ARE SWARM - Sample workflow created: {args.output}")
                return 0
            except Exception as e:
                print(f"🐝 WE ARE SWARM - Error creating sample workflow: {e}")
                return 1
        
        if not args.workflow:
            print("🐝 WE ARE SWARM - Error: --workflow required for this command")
            return 1
        
        manager = AgentWorkflowManager(args.workflow, args.coords)
        
        if args.command == "run":
            print(f"🐝 WE ARE SWARM - Starting workflow: {manager.workflow_data.get('name', 'Unnamed')}")
            manager.run_workflow(args.max_concurrent)
            print("🐝 WE ARE SWARM - Workflow completed")
            
        elif args.command == "status":
            status = manager.get_status()
            print(f"🐝 WE ARE SWARM - Workflow Status:")
            print(f"Name: {status['workflow_name']}")
            print(f"Total Steps: {status['total_steps']}")
            print(f"Status Counts: {status['status_counts']}")
            
        elif args.command == "complete":
            manager.mark_step_completed(args.step_id, args.result)
            print(f"🐝 WE ARE SWARM - Step {args.step_id} marked as completed")
            
        elif args.command == "fail":
            manager.mark_step_failed(args.step_id, args.error)
            print(f"🐝 WE ARE SWARM - Step {args.step_id} marked as failed")
        
        return 0
        
    except Exception as e:
        logger.error(f"Workflow error: {e}")
        print(f"🐝 WE ARE SWARM - Workflow error: {e}")
        return 1


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    sys.exit(main())
