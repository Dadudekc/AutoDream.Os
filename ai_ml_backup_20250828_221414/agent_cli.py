#!/usr/bin/env python3
"""
Agent AI/ML CLI Launcher - Simplified Interface
Quick access to AI/ML functionality for agents with contract integration

Usage:
    python agent_cli.py --help
    python agent_cli.py contracts
    python agent_cli.py ai-status
    python agent_cli.py ml-status
    python agent_cli.py workflow-create "My Workflow"
"""

import argparse
import sys
from pathlib import Path

# Import the main CLI
try:
    from .cli import AIMLCLI
except ImportError:
    # Fallback for direct execution
    sys.path.insert(0, str(Path(__file__).parent))
    from cli import AIMLCLI

class AgentCLI:
    """Simplified CLI launcher for agents"""
    
    def __init__(self):
        self.cli = AIMLCLI()
    
    def run(self, args):
        """Run simplified agent commands"""
        if args.command == "contracts":
            self._show_contracts()
        elif args.command == "ai-status":
            self._show_ai_status()
        elif args.command == "ml-status":
            self._show_ml_status()
        elif args.command == "workflow-create":
            if not args.name:
                print("❌ Workflow name is required")
                return
            self._create_workflow(args.name, args.description)
        elif args.command == "system-status":
            self._show_system_status()
        elif args.command == "health-check":
            self._run_health_check()
        elif args.command == "quick-start":
            self._quick_start()
        else:
            print(f"❌ Unknown command: {args.command}")
            sys.exit(1)
    
    def _show_contracts(self):
        """Show available contracts"""
        if not self.cli.contract_system:
            print("❌ Contract system not available")
            return
        
        contracts = self.cli.contract_system.list_available_contracts()
        if contracts:
            print(f"\n📋 Available Contracts ({len(contracts)}):")
            print("=" * 80)
            for contract in contracts:
                print(f"🔹 {contract.get('contract_id', 'N/A')}: {contract.get('title', 'N/A')}")
                print(f"   🏆 Points: {contract.get('extra_credit_points', 0)}")
                print(f"   📂 Category: {contract.get('category', 'N/A')}")
                print(f"   📝 {contract.get('description', 'N/A')[:80]}...")
                print("-" * 40)
        else:
            print("❌ No available contracts found")
    
    def _show_ai_status(self):
        """Show AI system status"""
        print(f"\n🤖 AI System Status:")
        print("=" * 60)
        
        # AI Manager status
        ai_stats = self.cli.ai_manager.get_statistics()
        print(f"📊 AI Manager:")
        print(f"   Models: {ai_stats['total_models']}")
        print(f"   Workflows: {ai_stats['total_workflows']}")
        print(f"   API Keys: {ai_stats['total_api_keys']}")
        
        # Show recent models
        models = self.cli.ai_manager.list_models()
        if models:
            print(f"\n🔹 Recent Models:")
            for model in models[:5]:  # Show first 5
                print(f"   • {model.model_id}: {model.name} ({model.provider})")
        
        # Show recent workflows
        workflows = self.cli.ai_manager.list_workflows()
        if workflows:
            print(f"\n🔄 Recent Workflows:")
            for workflow in workflows[:5]:  # Show first 5
                print(f"   • {workflow.name}: {workflow.status}")
    
    def _show_ml_status(self):
        """Show ML system status"""
        print(f"\n🔧 ML System Status:")
        print("=" * 60)
        
        # Model Manager status
        ml_stats = self.cli.model_manager.get_statistics()
        print(f"📊 Model Manager:")
        print(f"   Models: {ml_stats['total_models']}")
        print(f"   Frameworks: {ml_stats['total_frameworks']}")
        print(f"   Models with Versions: {ml_stats['models_with_versions']}")
        
        # Show recent models
        models = self.cli.model_manager.list_models()
        if models:
            print(f"\n🔹 Recent Models:")
            for model in models[:5]:  # Show first 5
                versions = self.cli.model_manager.get_model_versions(model.model_id)
                latest_version = versions[-1] if versions else "N/A"
                print(f"   • {model.model_id}: {model.name} (v{latest_version})")
        
        # Show frameworks
        frameworks = self.cli.model_manager.list_frameworks()
        if frameworks:
            print(f"\n🔧 Frameworks:")
            for framework in frameworks:
                print(f"   • {framework.name} v{framework.version}")
    
    def _create_workflow(self, name, description):
        """Create a new workflow"""
        try:
            workflow = self.cli.ai_manager.create_workflow(
                name=name,
                description=description or f"Workflow created by agent: {name}"
            )
            print(f"✅ Workflow '{name}' created successfully!")
            print(f"📝 Description: {workflow.description}")
            print(f"📊 Status: {workflow.status}")
        except Exception as e:
            print(f"❌ Failed to create workflow: {e}")
    
    def _show_system_status(self):
        """Show overall system status"""
        print(f"\n🔍 AI/ML System Overview:")
        print("=" * 80)
        
        # AI Manager status
        ai_stats = self.cli.ai_manager.get_statistics()
        print(f"🤖 AI Manager: {ai_stats['total_models']} models, {ai_stats['total_workflows']} workflows")
        
        # Model Manager status
        ml_stats = self.cli.model_manager.get_statistics()
        print(f"🔧 Model Manager: {ml_stats['total_models']} models, {ml_stats['total_frameworks']} frameworks")
        
        # Workflow Automation status
        auto_stats = self.cli.workflow_automation.get_automation_statistics()
        print(f"⚡ Workflow Automation: {auto_stats['total_automation_rules']} rules, {auto_stats['scheduled_tasks']} tasks")
        
        # Contract system status
        if self.cli.contract_system:
            contracts = self.cli.contract_system.list_available_contracts()
            print(f"📋 Contract System: {len(contracts)} available contracts")
        else:
            print(f"📋 Contract System: Not Available")
        
        # Quick recommendations
        print(f"\n💡 Quick Actions:")
        if ai_stats['total_models'] == 0:
            print(f"   • Register your first AI model: python agent_cli.py ai-register")
        if ml_stats['total_models'] == 0:
            print(f"   • Add ML models to the system")
        if auto_stats['total_automation_rules'] == 0:
            print(f"   • Create automation rules for efficiency")
        if self.cli.contract_system and contracts:
            print(f"   • Claim available contracts for extra credit")
    
    def _run_health_check(self):
        """Run system health check"""
        print(f"\n🏥 System Health Check:")
        print("=" * 60)
        
        # Check AI Manager health
        try:
            ai_health = self.cli.ai_manager._check_ai_management_health()
            print(f"🤖 AI Manager: ✅ Healthy")
            if "warnings" in ai_health:
                for warning in ai_health["warnings"]:
                    print(f"   ⚠️  {warning}")
        except Exception as e:
            print(f"🤖 AI Manager: ❌ Unhealthy - {e}")
        
        # Check Model Manager health
        try:
            ml_health = self.cli.model_manager._check_model_health()
            print(f"🔧 Model Manager: ✅ Healthy")
            if "warnings" in ml_health:
                for warning in ml_health["warnings"]:
                    print(f"   ⚠️  {warning}")
        except Exception as e:
            print(f"🔧 Model Manager: ❌ Unhealthy - {e}")
        
        # Check contract system
        if self.cli.contract_system:
            try:
                contracts = self.cli.contract_system.list_available_contracts()
                print(f"📋 Contract System: ✅ Healthy ({len(contracts)} contracts available)")
            except Exception as e:
                print(f"📋 Contract System: ❌ Unhealthy - {e}")
        else:
            print(f"📋 Contract System: ⚠️  Not Available")
    
    def _quick_start(self):
        """Quick start guide for agents"""
        print(f"\n🚀 AI/ML Quick Start Guide for Agents:")
        print("=" * 80)
        
        print(f"\n1️⃣  Check System Status:")
        print(f"   python agent_cli.py system-status")
        
        print(f"\n2️⃣  View Available Contracts:")
        print(f"   python agent_cli.py contracts")
        
        print(f"\n3️⃣  Check AI/ML Capabilities:")
        print(f"   python agent_cli.py ai-status")
        print(f"   python agent_cli.py ml-status")
        
        print(f"\n4️⃣  Create Your First Workflow:")
        print(f"   python agent_cli.py workflow-create 'My First Workflow' --description 'Description'")
        
        print(f"\n5️⃣  Run Health Check:")
        print(f"   python agent_cli.py health-check")
        
        print(f"\n💡 Pro Tips:")
        print(f"   • Use 'python agent_cli.py --help' for detailed options")
        print(f"   • Check contracts regularly for extra credit opportunities")
        print(f"   • Monitor system health before starting complex tasks")
        print(f"   • Create automation rules to streamline your workflow")

def main():
    """Main agent CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Agent AI/ML CLI Launcher - Quick Access to AI/ML Functionality",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Quick Commands for Agents:
  contracts          - Show available contracts
  ai-status         - Show AI system status
  ml-status         - Show ML system status
  workflow-create   - Create a new workflow
  system-status     - Show overall system status
  health-check      - Run system health check
  quick-start       - Show quick start guide

Examples:
  python agent_cli.py contracts
  python agent_cli.py workflow-create "Data Processing" --description "Process data"
  python agent_cli.py system-status
        """
    )
    
    parser.add_argument("command", help="Command to execute")
    parser.add_argument("--name", help="Name for workflow creation")
    parser.add_argument("--description", help="Description for workflow creation")
    
    args = parser.parse_args()
    
    try:
        agent_cli = AgentCLI()
        agent_cli.run(args)
    except KeyboardInterrupt:
        print("\n👋 Operation cancelled by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
