#!/usr/bin/env python3
"""
Contract Management CLI - Agent Cellphone V2
===========================================

Simple CLI wrapper for agents to manage their contracts.
Usage: python contract_cli.py [COMMAND] [OPTIONS]

Author: Agent-4 (Captain)
Purpose: Easy contract management for agents
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

try:
    from core.task_management.contract_management_system import ContractCLI
except ImportError:
    print("❌ Error: Could not import contract management system")
    print("Make sure you're running from the repository root directory")
    sys.exit(1)

def main():
    """Main CLI entry point"""
    cli = ContractCLI()
    cli.run(sys.argv[1:])

if __name__ == "__main__":
    main()
