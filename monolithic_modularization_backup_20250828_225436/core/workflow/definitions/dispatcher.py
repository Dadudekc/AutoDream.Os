#!/usr/bin/env python3
"""
Workflow Definition Dispatcher
==============================

Loads workflow definition modules dynamically.
Follows V2 standards: modular, single responsibility.

Author: Agent-3 (Workflow Unification)
License: MIT
"""

import importlib
import pkgutil
from typing import Dict

from ..types.workflow_models import WorkflowDefinition


def load_workflow_definitions() -> Dict[str, WorkflowDefinition]:
    """Dynamically load workflow definitions from this package."""
    workflows: Dict[str, WorkflowDefinition] = {}
    package = importlib.import_module(__name__.rsplit(".", 1)[0])
    for _, module_name, _ in pkgutil.iter_modules(package.__path__):
        if module_name == "dispatcher":
            continue
        module = importlib.import_module(f"{package.__name__}.{module_name}")
        module_workflows = getattr(module, "get_workflows", None)
        if callable(module_workflows):
            workflows.update(module_workflows())
    return workflows
