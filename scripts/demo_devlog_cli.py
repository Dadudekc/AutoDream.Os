#!/usr/bin/env python3
"""
Devlog CLI Demo - Agent Cellphone V2
====================================

Demonstrates how agents can use the new devlog CLI system.
Shows creating, searching, and managing devlogs.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import subprocess
import sys
from pathlib import Path

def run_command(command: str, description: str) -> bool:
    """Run a command and show the result"""
    print(f"\n🎯 {description}")
    print("="*60)
    print(f"Command: {command}")
    print("-" * 60)
    
    try:
        result = subprocess.run(command.split(), capture_output=True, text=True, timeout=30)
        
        if result.stdout:
            print("✅ Output:")
            print(result.stdout)
        
        if result.stderr:
            print("⚠️  Warnings:")
            print(result.stderr)
        
        if result.returncode == 0:
            print("✅ Command executed successfully")
            return True
        else:
            print(f"❌ Command failed with return code: {result.returncode}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Command timed out")
        return False
    except Exception as e:
        print(f"❌ Error running command: {e}")
        return False

def main():
    """Main demo function"""
    print("🎖️  DEVLOG CLI SYSTEM DEMO")
    print("="*60)
    print("This demo shows how agents can use the new devlog CLI system")
    print("to create, search, and manage project devlogs.")
    print()
    print("✅ Features:")
    print("  • Create devlog entries via CLI")
    print("  • Store in knowledge database")
    print("  • Post to Discord automatically")
    print("  • Search and review project history")
    print("  • Uses existing architecture")
    print()
    
    # Demo 1: Show help
    run_command("python -m src.core.devlog_cli --help", "Demo 1: Show CLI Help")
    
    # Demo 2: Show system status
    run_command("python -m src.core.devlog_cli status", "Demo 2: Show System Status")
    
    # Demo 3: Create a demo devlog entry
    demo_content = """This is a demo devlog entry created by the demo script.
It shows how agents can easily create devlogs via CLI.

Key benefits:
- Simple command-line interface
- Automatic knowledge database storage
- Discord integration
- Searchable project history
- Metadata tracking

This system follows our V2 coding standards and uses existing architecture."""
    
    create_command = f'python -m src.core.devlog_cli create --title "Devlog CLI Demo Entry" --content "{demo_content}" --agent "demo-agent" --category "project_update" --tags "demo,cli,devlog,integration" --priority "normal"'
    
    run_command(create_command, "Demo 3: Create Demo Devlog Entry")
    
    # Demo 4: Search for the demo entry
    run_command("python -m src.core.devlog_cli search --query 'Devlog CLI Demo'", "Demo 4: Search for Demo Entry")
    
    # Demo 5: Show recent entries
    run_command("python -m src.core.devlog_cli recent --limit 3", "Demo 5: Show Recent Entries")
    
    print("\n🎉 DEVLOG CLI DEMO COMPLETED!")
    print("="*60)
    print("✅ What we've demonstrated:")
    print("  • CLI help and status")
    print("  • Creating devlog entries")
    print("  • Searching devlogs")
    print("  • Viewing recent entries")
    print()
    print("🚀 Agents can now use:")
    print("  • python -m src.core.devlog_cli create --title 'Title' --content 'Content'")
    print("  • python -m src.core.devlog_cli search --query 'search term'")
    print("  • python -m src.core.devlog_cli recent --limit 10")
    print("  • python -m src.core.devlog_cli status")
    print()
    print("💡 This system:")
    print("  • Uses existing KnowledgeDatabase")
    print("  • Integrates with Discord")
    print("  • Follows V2 coding standards")
    print("  • Provides knowledge base for project ideas")
    print("  • Enables agent collaboration via devlogs")

if __name__ == "__main__":
    main()
