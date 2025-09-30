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
from swarm_orchestrator_core import SwarmOrchestrator


def main():
    """Quick access to swarm orchestration commands."""
    if len(sys.argv) < 2:
        orchestrator = SwarmOrchestrator()
        orchestrator.show_help()
        return

    command = sys.argv[1]
    args = sys.argv[2:] if len(sys.argv) > 2 else None
    
    orchestrator = SwarmOrchestrator()
    orchestrator.run_command(command, args)


if __name__ == "__main__":
    main()