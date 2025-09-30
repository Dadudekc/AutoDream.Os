#!/usr/bin/env python3
"""
Swarm Workflow Orchestrator
===========================

A powerful tool for coordinating collective intelligence workflows across all agents.
Makes complex multi-agent coordination as simple as a single command.
Refactored into modular components for V2 compliance.

Author: Agent-7 (Implementation Specialist)
License: MIT
V2 Compliance: ≤400 lines, modular design, comprehensive workflow orchestration
"""

# Import all components from refactored modules
from .swarm_workflow_orchestrator_core import SwarmWorkflowOrchestratorCore
from .swarm_workflow_orchestrator_main import (
    SwarmWorkflowOrchestrator,
    create_v2_trading_robot_workflow,
    main,
)
from .swarm_workflow_orchestrator_utils import SwarmWorkflowUtils

# Re-export main classes for backward compatibility
__all__ = [
    # Core classes
    "SwarmWorkflowOrchestratorCore",
    "SwarmWorkflowUtils",
    # Main orchestrator
    "SwarmWorkflowOrchestrator",
    # Workflow templates
    "create_v2_trading_robot_workflow",
    # CLI interface
    "main",
]


# For direct execution
if __name__ == "__main__":
    main()
