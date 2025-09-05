#!/usr/bin/env python3
"""
Agent Context Package - KISS Compliant
=====================================

Simple agent context system.

Author: Agent-5 - Business Intelligence Specialist
License: MIT
"""

from .agent_context_orchestrator import AgentContextSystem

# Simple aliases
AgentContext = AgentContextSystem

__version__ = "2.0.0"
__all__ = ["AgentContextSystem", "AgentContext"]
