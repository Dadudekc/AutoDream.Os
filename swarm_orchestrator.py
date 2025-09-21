#!/usr/bin/env python3
"""
Swarm Orchestrator - Quick Access
=================================

Quick access to the Swarm Workflow Orchestrator for easy agent coordination.

Usage:
    python swarm_orchestrator.py create-v2-robot
    python swarm_orchestrator.py execute-v2-robot
    python swarm_orchestrator.py list
    python swarm_orchestrator.py status v2-robot
"""

import sys
import subprocess
from pathlib import Path

def main():
    """Quick access to swarm orchestration commands."""
    if len(sys.argv) < 2:
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
        return
    
    command = sys.argv[1]
    
    if command == "create-v2-robot":
        print("🚀 Creating V2 Trading Robot workflow...")
        subprocess.run([
            sys.executable, 
            "src/tools/swarm_workflow_orchestrator.py",
            "create",
            "--name", "V2 Trading Robot",
            "--description", "Transform Tesla Trading Robot into V2-compliant masterpiece",
            "--template", "v2_trading_robot"
        ])
    
    elif command == "execute-v2-robot":
        print("🤖 Executing V2 Trading Robot workflow...")
        subprocess.run([
            sys.executable,
            "src/tools/swarm_workflow_orchestrator.py",
            "execute",
            "--workflow", "V2 Trading Robot"
        ])
    
    elif command == "list":
        print("📋 Listing workflows...")
        subprocess.run([
            sys.executable,
            "src/tools/swarm_workflow_orchestrator.py",
            "list"
        ])
    
    elif command == "status":
        if len(sys.argv) < 3:
            print("❌ Please specify workflow name")
            print("Usage: python swarm_orchestrator.py status <workflow-name>")
            return
        
        workflow_name = sys.argv[2]
        print(f"📊 Getting status for {workflow_name}...")
        subprocess.run([
            sys.executable,
            "src/tools/swarm_workflow_orchestrator.py",
            "status",
            "--workflow", workflow_name
        ])
    
    elif command == "help":
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
    
    else:
        print(f"❌ Unknown command: {command}")
        print("Run 'python swarm_orchestrator.py help' for usage information")

if __name__ == "__main__":
    main()



