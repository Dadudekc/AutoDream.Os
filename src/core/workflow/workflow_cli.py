#!/usr/bin/env python3
"""
Workflow CLI - V2 Core Workflow Command Line Interface

This module provides CLI interface for workflow testing and management.
Follows V2 standards: ≤100 lines, single responsibility, clean OOP design.

Author: Agent-4 (Quality Assurance)
License: MIT
"""

import argparse
import logging
import sys

from src.utils.stability_improvements import stability_manager, safe_import
from typing import Dict, Any

try:
    from .workflow_orchestrator import WorkflowOrchestrator
    from .workflow_executor import WorkflowExecutor
    from .workflow_planner import WorkflowPlanner
    from .workflow_types import WorkflowTask, WorkflowCondition, TaskPriority
except ImportError:
    # Fallback for standalone usage
    from workflow_orchestrator import WorkflowOrchestrator
    from workflow_executor import WorkflowExecutor
    from workflow_planner import WorkflowPlanner
    from workflow_types import WorkflowTask, WorkflowCondition, TaskPriority

logger = logging.getLogger(__name__)


class WorkflowCLI:
    """
    Command-line interface for workflow automation testing
    
    Responsibilities:
    - CLI interface for testing
    - Basic workflow operations
    - Help and documentation
    """

    def __init__(self):
        """Initialize the workflow CLI"""
        self.orchestrator = WorkflowOrchestrator()
        self.executor = WorkflowExecutor()
        self.planner = WorkflowPlanner()
        self.setup_logging()

    def setup_logging(self):
        """Setup logging for CLI operations"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def run_smoke_test(self) -> bool:
        """Run basic functionality test for workflow system"""
        try:
            print("🧪 Running Workflow System Smoke Test...")
            
            # Test 1: Create workflow
            print("  Testing workflow creation...")
            task_definitions = [
                {
                    "task_id": "task1",
                    "name": "Test Task 1",
                    "description": "First test task",
                    "estimated_duration": 30
                },
                {
                    "task_id": "task2", 
                    "name": "Test Task 2",
                    "description": "Second test task",
                    "estimated_duration": 45,
                    "dependencies": ["task1"]
                }
            ]
            
            success = self.orchestrator.create_workflow(
                "test_workflow",
                "Test Workflow",
                "Test workflow for smoke testing",
                task_definitions
            )
            
            if not success:
                print("  ❌ Workflow creation failed")
                return False
            
            print("  ✅ Workflow creation successful")
            
            # Test 2: Start execution
            print("  Testing workflow execution...")
            execution_id = self.orchestrator.start_workflow_execution("test_workflow")
            
            if not execution_id:
                print("  ❌ Workflow execution start failed")
                return False
            
            print("  ✅ Workflow execution started")
            
            # Test 3: Get status
            print("  Testing status retrieval...")
            status = self.orchestrator.get_execution_status(execution_id)
            
            if not status:
                print("  ❌ Status retrieval failed")
                return False
            
            print("  ✅ Status retrieval successful")
            
            # Test 4: Get summary
            print("  Testing summary retrieval...")
            summary = self.orchestrator.get_workflow_summary()
            
            if not summary:
                print("  ❌ Summary retrieval failed")
                return False
            
            print("  ✅ Summary retrieval successful")
            
            print("🎉 All smoke tests passed!")
            return True
            
        except Exception as e:
            print(f"❌ Smoke test failed: {e}")
            return False

    def create_sample_workflow(self) -> bool:
        """Create a sample workflow for testing"""
        try:
            print("🏗️ Creating sample workflow...")
            
            # Create a simple sequential workflow
            task_definitions = [
                {
                    "task_id": "init",
                    "name": "Initialize System",
                    "description": "Initialize the workflow system",
                    "estimated_duration": 10,
                    "priority": TaskPriority.HIGH
                },
                {
                    "task_id": "process",
                    "name": "Process Data",
                    "description": "Process workflow data",
                    "estimated_duration": 60,
                    "dependencies": ["init"],
                    "priority": TaskPriority.MEDIUM
                },
                {
                    "task_id": "finalize",
                    "name": "Finalize Workflow",
                    "description": "Complete workflow execution",
                    "estimated_duration": 20,
                    "dependencies": ["process"],
                    "priority": TaskPriority.LOW
                }
            ]
            
            success = self.orchestrator.create_workflow(
                "sample_workflow",
                "Sample Workflow",
                "A sample workflow for testing purposes",
                task_definitions
            )
            
            if success:
                print("✅ Sample workflow created successfully")
                return True
            else:
                print("❌ Sample workflow creation failed")
                return False
                
        except Exception as e:
            print(f"❌ Sample workflow creation failed: {e}")
            return False

    def list_workflows(self) -> bool:
        """List all available workflows"""
        try:
            summary = self.orchestrator.get_workflow_summary()
            
            print("📋 Workflow Summary:")
            print(f"  Total Workflows: {summary.get('total_workflows', 0)}")
            print(f"  Total Executions: {summary.get('total_executions', 0)}")
            print(f"  Active Executions: {summary.get('active_executions', 0)}")
            print(f"  Registered Agents: {summary.get('registered_agents', 0)}")
            print(f"  Available Resources: {summary.get('available_resources', 0)}")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to list workflows: {e}")
            return False

    def main(self):
        """Main CLI entry point"""
        parser = argparse.ArgumentParser(
            description="Workflow Automation CLI - V2 Standards Compliant"
        )
        
        parser.add_argument(
            "--test", 
            action="store_true",
            help="Run smoke tests"
        )
        
        parser.add_argument(
            "--create-sample",
            action="store_true", 
            help="Create sample workflow"
        )
        
        parser.add_argument(
            "--list",
            action="store_true",
            help="List all workflows"
        )
        
        parser.add_argument(
            "--version",
            action="version",
            version="Workflow CLI v2.0.0"
        )
        
        args = parser.parse_args()
        
        if args.test:
            success = self.run_smoke_test()
            sys.exit(0 if success else 1)
        elif args.create_sample:
            success = self.create_sample_workflow()
            sys.exit(0 if success else 1)
        elif args.list:
            success = self.list_workflows()
            sys.exit(0 if success else 1)
        else:
            parser.print_help()
            print("\n💡 Try --test to run smoke tests")


if __name__ == "__main__":
    cli = WorkflowCLI()
    cli.main()
