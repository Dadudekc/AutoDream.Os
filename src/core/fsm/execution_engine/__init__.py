#!/usr/bin/env python3
"""FSM execution engine package."""

from .core import FSMCore

FSMCoreV2 = FSMCore
FiniteStateMachine = FSMCore
WorkflowEngine = FSMCore

__all__ = ["FSMCore", "FSMCoreV2", "FiniteStateMachine", "WorkflowEngine"]
