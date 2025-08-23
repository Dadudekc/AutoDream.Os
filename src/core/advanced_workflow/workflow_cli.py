"""
Workflow CLI Interface - V2 Compliant Command Line Interface

This module provides a CLI interface for testing and managing workflows.
Follows V2 standards with ≤100 LOC and single responsibility for CLI operations.
"""

import argparse
import json
import logging
import sys
from typing import Dict, Any, Optional

from .workflow_execution import AdvancedWorkflowEngine
from .workflow_validation import WorkflowValidator
from .workflow_types import WorkflowType, WorkflowPriority, OptimizationStrategy


class WorkflowCLI:
    """Command line interface for workflow management and testing"""
    
    def __init__(self):
        self.engine: Optional[AdvancedWorkflowEngine] = None
        self.validator = WorkflowValidator()
        self.logger = logging.getLogger(f"{__name__}.WorkflowCLI")
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    def setup_mock_dependencies(self):
        """Setup mock dependencies for testing"""
        class MockAgentManager:
            def get_available_agents(self):
                return []
        
        class MockConfigManager:
            def get_config(self, section, key, default):
                return default
        
        class MockContractManager:
            pass
        
        self.engine = AdvancedWorkflowEngine(
            agent_manager=MockAgentManager(),
            config_manager=MockConfigManager(),
            contract_manager=MockContractManager()
        )
    
    def run_smoke_test(self) -> bool:
        """Run basic functionality test for the workflow engine"""
        try:
            if not self.engine:
                self.setup_mock_dependencies()
            
            # Test V2 workflow creation
            steps = [
                {
                    "id": "step1",
                    "name": "Test Step",
                    "description": "Test workflow step",
                    "step_type": "general",
                }
            ]
            
            workflow_id = self.engine.create_v2_workflow(
                "Test Workflow", "Test Description", steps
            )
            
            if not workflow_id:
                print("❌ Failed to create V2 workflow")
                return False
            
            if workflow_id not in self.engine.v2_workflows:
                print("❌ Created workflow not found in engine")
                return False
            
            # Test workflow execution
            success = self.engine.execute_v2_workflow(workflow_id)
            if not success:
                print("❌ Failed to execute V2 workflow")
                return False
            
            # Test summary
            summary = self.engine.get_workflow_summary()
            if summary["total_v2_workflows"] != 1:
                print("❌ Workflow summary count mismatch")
                return False
            
            print("✅ AdvancedWorkflowEngine smoke test passed!")
            return True
        
        except Exception as e:
            print(f"❌ AdvancedWorkflowEngine smoke test failed: {e}")
            return False
    
    def create_workflow(self, name: str, description: str, steps_file: str) -> bool:
        """Create a workflow from a JSON steps file"""
        try:
            if not self.engine:
                self.setup_mock_dependencies()
            
            # Load steps from file
            with open(steps_file, 'r') as f:
                steps = json.load(f)
            
            workflow_id = self.engine.create_v2_workflow(name, description, steps)
            if workflow_id:
                print(f"✅ Created workflow: {workflow_id}")
                return True
            else:
                print("❌ Failed to create workflow")
                return False
        
        except Exception as e:
            print(f"❌ Error creating workflow: {e}")
            return False
    
    def list_workflows(self) -> bool:
        """List all workflows"""
        try:
            if not self.engine:
                self.setup_mock_dependencies()
            
            summary = self.engine.get_workflow_summary()
            
            print(f"\n📊 Workflow Summary:")
            print(f"  Total Workflows: {summary['total_workflows']}")
            print(f"  Total V2 Workflows: {summary['total_v2_workflows']}")
            print(f"  Active Executions: {summary['active_executions']}")
            print(f"  Active V2 Workflows: {summary['active_v2_workflows']}")
            
            if summary['v2_workflow_names']:
                print(f"\n📋 V2 Workflows:")
                for name in summary['v2_workflow_names']:
                    print(f"  - {name}")
            
            return True
        
        except Exception as e:
            print(f"❌ Error listing workflows: {e}")
            return False
    
    def validate_workflow(self, workflow_id: str) -> bool:
        """Validate a specific workflow"""
        try:
            if not self.engine:
                self.setup_mock_dependencies()
            
            workflow = self.engine.get_workflow(workflow_id)
            if not workflow:
                print(f"❌ Workflow {workflow_id} not found")
                return False
            
            # Validate workflow definition
            is_valid, messages = self.validator.validate_workflow_definition(workflow)
            
            print(f"\n🔍 Validation Results for {workflow_id}:")
            if is_valid:
                print("✅ Workflow is valid")
            else:
                print("❌ Workflow has validation errors")
            
            if messages:
                for msg in messages:
                    if msg.startswith("❌"):
                        print(f"  {msg}")
                    else:
                        print(f"  ⚠️  {msg}")
            
            return is_valid
        
        except Exception as e:
            print(f"❌ Error validating workflow: {e}")
            return False
    
    def get_optimization_summary(self) -> bool:
        """Get optimization summary"""
        try:
            if not self.engine:
                self.setup_mock_dependencies()
            
            summary = self.engine.get_optimization_summary()
            
            print(f"\n⚡ Optimization Summary:")
            print(f"  Total Optimizations: {summary['total_optimizations']}")
            print(f"  Recent Optimizations: {summary['recent_optimizations']}")
            print(f"  Average Improvement: {summary['average_improvement']}%")
            print(f"  Optimization Active: {summary['optimization_active']}")
            
            if summary.get('last_optimization'):
                print(f"  Last Optimization: {summary['last_optimization']}")
            
            return True
        
        except Exception as e:
            print(f"❌ Error getting optimization summary: {e}")
            return False
    
    def run_command(self, args) -> bool:
        """Run the appropriate command based on arguments"""
        if args.command == "test":
            return self.run_smoke_test()
        elif args.command == "create":
            return self.create_workflow(args.name, args.description, args.steps_file)
        elif args.command == "list":
            return self.list_workflows()
        elif args.command == "validate":
            return self.validate_workflow(args.workflow_id)
        elif args.command == "optimization":
            return self.get_optimization_summary()
        else:
            print(f"❌ Unknown command: {args.command}")
            return False


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(description="Workflow Management CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Test command
    subparsers.add_parser("test", help="Run smoke test")
    
    # Create command
    create_parser = subparsers.add_parser("create", help="Create a new workflow")
    create_parser.add_argument("name", help="Workflow name")
    create_parser.add_argument("description", help="Workflow description")
    create_parser.add_argument("steps_file", help="JSON file containing workflow steps")
    
    # List command
    subparsers.add_parser("list", help="List all workflows")
    
    # Validate command
    validate_parser = subparsers.add_parser("validate", help="Validate a workflow")
    validate_parser.add_argument("workflow_id", help="Workflow ID to validate")
    
    # Optimization command
    subparsers.add_parser("optimization", help="Get optimization summary")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    cli = WorkflowCLI()
    success = cli.run_command(args)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())

