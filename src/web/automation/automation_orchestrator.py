"""Automation Orchestrator module aggregator."""

from .automation_orchestrator_core import (
    AutomationOrchestrator,
    create_automation_orchestrator,
    run_automation_pipeline,
)
from .automation_orchestrator_config import OrchestrationConfig, EXAMPLE_PIPELINES

__all__ = [
    "AutomationOrchestrator",
    "OrchestrationConfig",
    "create_automation_orchestrator",
    "run_automation_pipeline",
    "EXAMPLE_PIPELINES",
]
