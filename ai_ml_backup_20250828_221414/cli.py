from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
import argparse
import json
import sys

        from agent_workspaces.meeting.contract_claiming_system import ContractClaimingSystem
from . import (

#!/usr/bin/env python3
"""
AI/ML Command Line Interface - Integrated Agent System
Provides comprehensive CLI access to all modularized AI/ML functionality
Integrated with the agent contract system for seamless workflow management

Usage:
    python -m src.ai_ml.cli --help
    python -m src.ai_ml.cli contracts --list
    python -m src.ai_ml.cli ai --models --list
    python -m src.ai_ml.cli ml --workflows --create "My Workflow"
"""


# Import all AI/ML modules
    AIManager, ModelManager, WorkflowAutomation,
    AIModel, MLWorkflow, MLFramework,
    create_ai_ml_system
)

# Import contract system
try:
    
    # Try to find the contract system
    repo_root = Path(__file__).parent.parent.parent
    contract_path = repo_root / "agent_workspaces" / "meeting" / "contract_claiming_system.py"
    
    if contract_path.exists():
        # Add to path and import
        sys.path.insert(0, str(repo_root))
        CONTRACT_SYSTEM_AVAILABLE = True
    else:
        CONTRACT_SYSTEM_AVAILABLE = False
        print("⚠️  Contract system not found - some features will be limited")
except ImportError:
    CONTRACT_SYSTEM_AVAILABLE = False
    print("⚠️  Contract system not available - some features will be limited")

class AIMLCLI:
    """Comprehensive CLI for AI/ML functionality with contract integration"""
    
    def __init__(self):
        self.ai_manager = None
        self.model_manager = None
        self.workflow_automation = None
        self.contract_system = None
        
        # Initialize systems
        self._initialize_systems()
    
    def _initialize_systems(self):
        """Initialize AI/ML and contract systems"""
        try:
            # Initialize AI/ML system
            self.ai_manager, self.model_manager, self.workflow_automation = create_ai_ml_system()
            
            # Initialize contract system if available
            if CONTRACT_SYSTEM_AVAILABLE:
                repo_root = Path(__file__).parent.parent.parent
                task_list_path = repo_root / "agent_workspaces" / "meeting" / "task_list.json"
                if task_list_path.exists():
                    self.contract_system = ContractClaimingSystem(str(task_list_path))
                else:
                    print("⚠️  Task list not found - contract features disabled")
            
        except Exception as e:
            print(f"❌ Error initializing systems: {e}")
    
    def run(self, args):
        """Main CLI entry point"""
        if args.command == "contracts":
            self._handle_contracts(args)
        elif args.command == "ai":
            self._handle_ai(args)
        elif args.command == "ml":
            self._handle_ml(args)
        elif args.command == "workflows":
            self._handle_workflows(args)
        elif args.command == "models":
            self._handle_models(args)
        elif args.command == "automation":
            self._handle_automation(args)
        elif args.command == "system":
            self._handle_system(args)
        else:
            print(f"❌ Unknown command: {args.command}")
            sys.exit(1)
    
    def _handle_contracts(self, args):
        """Handle contract-related commands"""
        if not self.contract_system:
            print("❌ Contract system not available")
            return
        
        if args.action == "list":
            if args.category:
                contracts = self.contract_system.list_available_contracts(args.category)
            else:
                contracts = self.contract_system.list_available_contracts()
            
            if contracts:
                print(f"\n📋 Available Contracts ({len(contracts)}):")
                print("=" * 80)
                for contract in contracts:
                    print(f"🔹 {contract.get('contract_id', 'N/A')}: {contract.get('title', 'N/A')}")
                    print(f"   Points: {contract.get('extra_credit_points', 0)} | Category: {contract.get('category', 'N/A')}")
                    print(f"   Description: {contract.get('description', 'N/A')[:100]}...")
                    print("-" * 40)
            else:
                print("❌ No available contracts found")
        
        elif args.action == "claim":
            if not args.contract_id or not args.agent_id:
                print("❌ --contract-id and --agent-id are required for claiming")
                return
            
            result = self.contract_system.claim_contract(args.contract_id, args.agent_id)
            if result["success"]:
                print(f"✅ {result['message']}")
                contract = result["contract"]
                print(f"📊 Contract: {contract.get('title', 'N/A')}")
                print(f"🏆 Points: {contract.get('extra_credit_points', 0)}")
            else:
                print(f"❌ {result['message']}")
        
        elif args.action == "status":
            if not args.contract_id:
                print("❌ --contract-id is required for status check")
                return
            
            result = self.contract_system.get_contract_status(args.contract_id)
            if result["success"]:
                contract = result["contract"]
                print(f"\n📊 Contract Status: {contract.get('contract_id', 'N/A')}")
                print(f"📋 Title: {contract.get('title', 'N/A')}")
                print(f"📈 Status: {contract.get('status', 'N/A')}")
                print(f"🤖 Claimed by: {contract.get('claimed_by', 'N/A')}")
                print(f"📈 Progress: {contract.get('progress', 'N/A')}")
                print(f"🏆 Points: {contract.get('extra_credit_points', 0)}")
            else:
                print(f"❌ {result['message']}")
    
    def _handle_ai(self, args):
        """Handle AI-related commands"""
        if args.action == "models":
            if args.subaction == "list":
                models = self.ai_manager.list_models()
                if models:
                    print(f"\n🤖 AI Models ({len(models)}):")
                    print("=" * 60)
                    for model in models:
                        print(f"🔹 {model.model_id}: {model.name}")
                        print(f"   Provider: {model.provider} | Version: {model.version}")
                        print(f"   Type: {model.model_type} | Status: {model.status}")
                        print("-" * 30)
                else:
                    print("❌ No AI models registered")
            
            elif args.subaction == "register":
                # Create a sample model for demonstration
                model = AIModel(
                    model_id=args.model_id,
                    name=args.name or args.model_id,
                    provider=args.provider or "unknown",
                    model_type=args.model_type or "generic",
                    version=args.version or "1.0.0"
                )
                
                if self.ai_manager.register_model(model):
                    print(f"✅ Model {args.model_id} registered successfully")
                else:
                    print(f"❌ Failed to register model {args.model_id}")
        
        elif args.action == "workflows":
            if args.subaction == "list":
                workflows = self.ai_manager.list_workflows()
                if workflows:
                    print(f"\n🔄 AI Workflows ({len(workflows)}):")
                    print("=" * 60)
                    for workflow in workflows:
                        print(f"🔹 {workflow.name}: {workflow.description}")
                        print(f"   Status: {workflow.status} | Created: {workflow.created_at}")
                        print("-" * 30)
                else:
                    print("❌ No AI workflows created")
            
            elif args.subaction == "create":
                if not args.name:
                    print("❌ --name is required for creating workflows")
                    return
                
                workflow = self.ai_manager.create_workflow(
                    name=args.name,
                    description=args.description or ""
                )
                print(f"✅ Workflow '{args.name}' created successfully")
        
        elif args.action == "execute":
            if not args.workflow_name:
                print("❌ --workflow-name is required for execution")
                return
            
            if self.ai_manager.execute_workflow(args.workflow_name):
                print(f"✅ Workflow '{args.workflow_name}' executed successfully")
            else:
                print(f"❌ Failed to execute workflow '{args.workflow_name}'")
    
    def _handle_ml(self, args):
        """Handle ML-related commands"""
        if args.action == "frameworks":
            if args.subaction == "list":
                frameworks = self.model_manager.list_frameworks()
                if frameworks:
                    print(f"\n🔧 ML Frameworks ({len(frameworks)}):")
                    print("=" * 60)
                    for framework in frameworks:
                        print(f"🔹 {framework.name} v{framework.version}")
                        print(f"   Supported Models: {', '.join(framework.supported_models)}")
                        print("-" * 30)
                else:
                    print("❌ No ML frameworks registered")
            
            elif args.subaction == "register":
                # This would require a concrete framework implementation
                print("⚠️  Framework registration requires concrete implementation")
        
        elif args.action == "models":
            if args.subaction == "list":
                models = self.model_manager.list_models()
                if models:
                    print(f"\n🤖 ML Models ({len(models)}):")
                    print("=" * 60)
                    for model in models:
                        print(f"🔹 {model.model_id}: {model.name}")
                        print(f"   Versions: {', '.join(self.model_manager.get_model_versions(model.model_id))}")
                        print(f"   Last Accessed: {self.model_manager.model_metadata.get(model.model_id, {}).get('last_accessed', 'N/A')}")
                        print("-" * 30)
                else:
                    print("❌ No ML models registered")
            
            elif args.subaction == "search":
                if not args.query:
                    print("❌ --query is required for model search")
                    return
                
                results = self.model_manager.search_models(args.query)
                if results:
                    print(f"\n🔍 Search Results for '{args.query}' ({len(results)}):")
                    print("=" * 60)
                    for model in results:
                        print(f"🔹 {model.model_id}: {model.name}")
                        print(f"   Provider: {model.provider} | Type: {model.model_type}")
                        print("-" * 30)
                else:
                    print(f"❌ No models found matching '{args.query}'")
    
    def _handle_workflows(self, args):
        """Handle workflow automation commands"""
        if args.action == "rules":
            if args.subaction == "list":
                rules = self.workflow_automation.list_automation_rules()
                if rules:
                    print(f"\n⚡ Automation Rules ({len(rules)}):")
                    print("=" * 60)
                    for rule_name in rules:
                        rule = self.workflow_automation.get_automation_rule(rule_name)
                        print(f"🔹 {rule_name}")
                        print(f"   Enabled: {rule.get('enabled', True)}")
                        print(f"   Executions: {rule.get('execution_count', 0)}")
                        print(f"   Created: {rule.get('created_at', 'N/A')}")
                        print("-" * 30)
                else:
                    print("❌ No automation rules defined")
            
            elif args.subaction == "add":
                if not args.rule_name:
                    print("❌ --rule-name is required for adding rules")
                    return
                
                # Simple rule creation for demonstration
                conditions = {"model_count": 0}
                actions = [{"type": "create_workflow", "parameters": {"name": "default"}}]
                
                if self.workflow_automation.add_automation_rule(
                    args.rule_name, conditions, actions
                ):
                    print(f"✅ Automation rule '{args.rule_name}' added successfully")
                else:
                    print(f"❌ Failed to add automation rule '{args.rule_name}'")
        
        elif args.action == "tasks":
            if args.subaction == "list":
                tasks = self.workflow_automation.list_scheduled_tasks()
                if tasks:
                    print(f"\n⏰ Scheduled Tasks ({len(tasks)}):")
                    print("=" * 60)
                    for task in tasks:
                        print(f"🔹 {task['name']}")
                        print(f"   Schedule: {task['schedule']}")
                        print(f"   Next Run: {task['next_run']}")
                        print("-" * 30)
                else:
                    print("❌ No scheduled tasks")
    
    def _handle_models(self, args):
        """Handle model-specific commands"""
        if args.action == "info":
            if not args.model_id:
                print("❌ --model-id is required for model info")
                return
            
            model = self.model_manager.get_model(args.model_id)
            if model:
                print(f"\n📊 Model Information: {args.model_id}")
                print("=" * 60)
                print(f"Name: {model.name}")
                print(f"Provider: {model.provider}")
                print(f"Type: {model.model_type}")
                print(f"Version: {model.version}")
                print(f"Status: {model.status}")
                
                metadata = self.model_manager.model_metadata.get(args.model_id, {})
                if metadata:
                    print(f"Registered: {metadata.get('registered_at', 'N/A')}")
                    print(f"Last Accessed: {metadata.get('last_accessed', 'N/A')}")
                    print(f"Access Count: {metadata.get('access_count', 0)}")
            else:
                print(f"❌ Model {args.model_id} not found")
        
        elif args.action == "validate":
            if not args.model_id:
                print("❌ --model-id is required for model validation")
                return
            
            if self.model_manager.validate_model(args.model_id):
                print(f"✅ Model {args.model_id} validation successful")
            else:
                print(f"❌ Model {args.model_id} validation failed")
    
    def _handle_automation(self, args):
        """Handle automation-specific commands"""
        if args.action == "process":
            # Process automation rules with current context
            context = {
                "model_count": len(self.model_manager.list_models()),
                "workflow_count": len(self.ai_manager.list_workflows()),
                "timestamp": datetime.now().isoformat()
            }
            
            executed_count = self.workflow_automation.process_automation_rules(context)
            print(f"✅ Processed {executed_count} automation rules")
        
        elif args.action == "stats":
            stats = self.workflow_automation.get_automation_statistics()
            print(f"\n📊 Automation Statistics:")
            print("=" * 60)
            print(f"Total Rules: {stats['total_automation_rules']}")
            print(f"Enabled Rules: {stats['enabled_rules']}")
            print(f"Disabled Rules: {stats['disabled_rules']}")
            print(f"Total Executions: {stats['total_rule_executions']}")
            print(f"Scheduled Tasks: {stats['scheduled_tasks']}")
    
    def _handle_system(self, args):
        """Handle system-level commands"""
        if args.action == "status":
            print(f"\n🔍 AI/ML System Status:")
            print("=" * 60)
            
            # AI Manager status
            ai_stats = self.ai_manager.get_statistics()
            print(f"🤖 AI Manager:")
            print(f"   Models: {ai_stats['total_models']}")
            print(f"   Workflows: {ai_stats['total_workflows']}")
            print(f"   API Keys: {ai_stats['total_api_keys']}")
            
            # Model Manager status
            ml_stats = self.model_manager.get_statistics()
            print(f"🔧 Model Manager:")
            print(f"   Models: {ml_stats['total_models']}")
            print(f"   Frameworks: {ml_stats['total_frameworks']}")
            
            # Workflow Automation status
            auto_stats = self.workflow_automation.get_automation_statistics()
            print(f"⚡ Workflow Automation:")
            print(f"   Rules: {auto_stats['total_automation_rules']}")
            print(f"   Scheduled Tasks: {auto_stats['scheduled_tasks']}")
            
            # Contract system status
            if self.contract_system:
                print(f"📋 Contract System: Available")
            else:
                print(f"📋 Contract System: Not Available")
        
        elif args.action == "health":
            print(f"\n🏥 System Health Check:")
            print("=" * 60)
            
            # Check AI Manager health
            try:
                ai_health = self.ai_manager._check_ai_management_health()
                print(f"🤖 AI Manager: ✅ Healthy")
                if "warnings" in ai_health:
                    for warning in ai_health["warnings"]:
                        print(f"   ⚠️  {warning}")
            except Exception as e:
                print(f"🤖 AI Manager: ❌ Unhealthy - {e}")
            
            # Check Model Manager health
            try:
                ml_health = self.model_manager._check_model_health()
                print(f"🔧 Model Manager: ✅ Healthy")
                if "warnings" in ml_health:
                    for warning in ml_health["warnings"]:
                        print(f"   ⚠️  {warning}")
            except Exception as e:
                print(f"🔧 Model Manager: ❌ Unhealthy - {e}")

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="AI/ML Command Line Interface - Integrated Agent System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Contract Management
  python -m src.ai_ml.cli contracts --list
  python -m src.ai_ml.cli contracts --claim --contract-id CONTRACT-001 --agent-id Agent-7
  
  # AI Management
  python -m src.ai_ml.cli ai --models --list
  python -m src.ai_ml.cli ai --workflows --create "My Workflow" --description "Description"
  
  # ML Operations
  python -m src.ai_ml.cli ml --frameworks --list
  python -m src.ai_ml.cli ml --models --search --query "bert"
  
  # Workflow Automation
  python -m src.ai_ml.cli workflows --rules --list
  python -m src.ai_ml.cli automation --process
  
  # System Management
  python -m src.ai_ml.cli system --status
  python -m src.ai_ml.cli system --health
        """
    )
    
    # Main command
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Contracts command
    contracts_parser = subparsers.add_parser("contracts", help="Contract management")
    contracts_parser.add_argument("action", choices=["list", "claim", "status"], help="Contract action")
    contracts_parser.add_argument("--category", help="Filter by category")
    contracts_parser.add_argument("--contract-id", help="Contract ID")
    contracts_parser.add_argument("--agent-id", help="Agent ID")
    
    # AI command
    ai_parser = subparsers.add_parser("ai", help="AI management")
    ai_parser.add_argument("action", choices=["models", "workflows", "execute"], help="AI action")
    ai_parser.add_argument("subaction", choices=["list", "register", "create"], help="Sub-action")
    ai_parser.add_argument("--model-id", help="Model ID")
    ai_parser.add_argument("--name", help="Name")
    ai_parser.add_argument("--provider", help="Provider")
    ai_parser.add_argument("--model-type", help="Model type")
    ai_parser.add_argument("--version", help="Version")
    ai_parser.add_argument("--description", help="Description")
    ai_parser.add_argument("--workflow-name", help="Workflow name")
    
    # ML command
    ml_parser = subparsers.add_parser("ml", help="ML operations")
    ml_parser.add_argument("action", choices=["frameworks", "models"], help="ML action")
    ml_parser.add_argument("subaction", choices=["list", "register", "search"], help="Sub-action")
    ml_parser.add_argument("--query", help="Search query")
    
    # Workflows command
    workflows_parser = subparsers.add_parser("workflows", help="Workflow automation")
    workflows_parser.add_argument("action", choices=["rules", "tasks"], help="Workflow action")
    workflows_parser.add_argument("subaction", choices=["list", "add"], help="Sub-action")
    workflows_parser.add_argument("--rule-name", help="Rule name")
    
    # Models command
    models_parser = subparsers.add_parser("models", help="Model operations")
    models_parser.add_argument("action", choices=["info", "validate"], help="Model action")
    models_parser.add_argument("--model-id", help="Model ID")
    
    # Automation command
    automation_parser = subparsers.add_parser("automation", help="Automation operations")
    automation_parser.add_argument("action", choices=["process", "stats"], help="Automation action")
    
    # System command
    system_parser = subparsers.add_parser("system", help="System management")
    system_parser.add_argument("action", choices=["status", "health"], help="System action")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        cli = AIMLCLI()
        cli.run(args)
    except KeyboardInterrupt:
        print("\n👋 Operation cancelled by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
