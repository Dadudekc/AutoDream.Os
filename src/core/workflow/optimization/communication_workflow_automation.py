#!/usr/bin/env python3
"""Communication Workflow Automation orchestrator.

This module coordinates configuration management, message routing and
optimization algorithms.  Previous implementations bundled all logic in a
single class which made maintenance difficult.  The orchestrator keeps the
components small and dedicated to their responsibilities while exposing a
simple facade for running the automation workflow.
"""
from datetime import datetime
import logging
from typing import Any, Dict

from .config_manager import ConfigManager
from .message_router import MessageRouter
from .optimization_algorithms import BatchOptimizer


class CommunicationWorkflowAutomation:
    """Orchestrate communication workflow automation components."""

    def __init__(
        self,
        config_manager: ConfigManager | None = None,
        router: MessageRouter | None = None,
        optimizer: BatchOptimizer | None = None,
    ) -> None:
        self.logger = logging.getLogger(__name__)
        self.config = config_manager or ConfigManager()
        self.router = router or MessageRouter(self.logger)
        self.optimizer = optimizer or BatchOptimizer(self.logger)

    def run(self) -> Dict[str, Any]:
        """Execute the automation workflow based on configuration."""
        results: Dict[str, Any] = {
            "timestamp": datetime.now().isoformat(),
            "config": self.config.as_dict(),
            "steps": [],
        }
        cfg = results["config"]
        if cfg.get("intelligent_routing"):
            results["steps"].append(
                self.router.implement_intelligent_message_routing()
            )
        if cfg.get("batch_processing"):
            results["steps"].append(
                self.optimizer.implement_batch_processing_automation()
            )
        return results
