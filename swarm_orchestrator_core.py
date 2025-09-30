#!/usr/bin/env python3
"""
Core logic for swarm orchestrator.
"""

import subprocess
import sys


class SwarmOrchestrator:
    """Quick access to swarm orchestration commands."""
    
    def __init__(self):
        """Initialize the orchestrator."""
        self.orchestrator_path = "src/tools/swarm_workflow_orchestrator.py"
    
    def show_help(self):
        """Show help information."""
        print("🐝 SWARM WORKFLOW ORCHESTRATOR")
        print("=" * 50)
        print("Quick access to collective intelligence coordination")
        print("")
        print("Commands:")
        print("  create-v2-robot    Create V2 Trading Robot workflow")
        print("  execute-v2-robot   Execute V2 Trading Robot workflow")
        print("  list               List all workflows")
        print("  status <name>      Get workflow status")
        print("  help               Show this help")
        print("")
        print("Examples:")
        print("  python swarm_orchestrator.py create-v2-robot")
        print("  python swarm_orchestrator.py execute-v2-robot")
        print("  python swarm_orchestrator.py status v2-robot")
    
    def create_v2_robot(self):
        """Create V2 Trading Robot workflow."""
        print("🚀 Creating V2 Trading Robot workflow...")
        subprocess.run([
            sys.executable,
            self.orchestrator_path,
            "create",
            "--name",
            "V2 Trading Robot",
            "--description",
            "Transform Tesla Trading Robot into V2-compliant masterpiece",
            "--template",
            "v2_trading_robot",
        ])
    
    def execute_v2_robot(self):
        """Execute V2 Trading Robot workflow."""
        print("🤖 Executing V2 Trading Robot workflow...")
        subprocess.run([
            sys.executable,
            self.orchestrator_path,
            "execute",
            "--workflow",
            "V2 Trading Robot",
        ])
    
    def list_workflows(self):
        """List all workflows."""
        print("📋 Listing workflows...")
        subprocess.run([sys.executable, self.orchestrator_path, "list"])
    
    def get_status(self, workflow_name):
        """Get workflow status."""
        print(f"📊 Getting status for {workflow_name}...")
        subprocess.run([
            sys.executable,
            self.orchestrator_path,
            "status",
            "--workflow",
            workflow_name,
        ])
    
    def show_detailed_help(self):
        """Show detailed help information."""
        print("🐝 SWARM WORKFLOW ORCHESTRATOR HELP")
        print("=" * 50)
        print("This tool makes complex multi-agent coordination simple!")
        print("")
        print("Key Features:")
        print("  • Automated workflow creation")
        print("  • Multi-agent message coordination")
        print("  • Task file generation")
        print("  • Progress tracking")
        print("  • V2 compliance enforcement")
        print("")
        print("Workflow Templates:")
        print("  • v2_trading_robot - Complete V2-compliant trading robot")
        print("  • custom - Create your own workflow")
        print("")
        print("🐝 WE. ARE. SWARM. - Orchestrate with intelligence!")
    
    def run_command(self, command, args=None):
        """Run a command."""
        if command == "create-v2-robot":
            self.create_v2_robot()
        elif command == "execute-v2-robot":
            self.execute_v2_robot()
        elif command == "list":
            self.list_workflows()
        elif command == "status":
            if not args or len(args) < 1:
                print("❌ Please specify workflow name")
                print("Usage: python swarm_orchestrator.py status <workflow-name>")
                return
            self.get_status(args[0])
        elif command == "help":
            self.show_detailed_help()
        else:
            print(f"❌ Unknown command: {command}")
            print("Run 'python swarm_orchestrator.py help' for usage information")
