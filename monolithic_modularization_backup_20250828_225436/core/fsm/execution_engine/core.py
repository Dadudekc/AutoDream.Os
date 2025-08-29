#!/usr/bin/env python3
"""FSM execution engine core class."""

import logging
from collections import defaultdict, deque
from dataclasses import asdict
from typing import Dict, List, Optional, Set

from .common import (
    load_fsm_config,
    FSMConfig,
    StateDefinition,
    TransitionDefinition,
    WorkflowInstance,
    StateHandler,
    TransitionHandler,
)
from .state_manager import StateManager
from .transition_manager import TransitionManager
from .workflow_manager import WorkflowManager
from .execution_runner import ExecutionRunner
from .system_controller import SystemController
from .reporting import Reporting


class FSMCore(
    StateManager,
    TransitionManager,
    WorkflowManager,
    ExecutionRunner,
    SystemController,
    Reporting,
):
    """Finite state machine execution engine."""

    def __init__(
        self,
        config: Optional[FSMConfig] = None,
        config_file: Optional[str] = None,
    ) -> None:
        self.logger = logging.getLogger(f"{__name__}.FSMCore")

        # Core data structures
        self.states: Dict[str, StateDefinition] = {}
        self.transitions: Dict[str, List[TransitionDefinition]] = defaultdict(list)
        self.workflows: Dict[str, WorkflowInstance] = {}
        self.state_handlers: Dict[str, StateHandler] = {}
        self.transition_handlers: Dict[str, TransitionHandler] = {}

        # System state
        self.is_running = False
        self.active_workflows: Set[str] = set()
        self.workflow_queue: deque = deque()

        # Configuration
        if config is not None:
            self.config = asdict(config)
        else:
            self.config = load_fsm_config(config_file)
        self.max_concurrent_workflows = self.config.get("max_concurrent_workflows", 10)
        self.default_timeout = self.config.get("default_timeout", 300.0)
        self.enable_logging = self.config.get("enable_logging", True)

        # Monitoring
        self.monitoring_thread = None
        self.monitoring_active = False

        # Statistics
        self.total_workflows_executed = 0
        self.successful_workflows = 0
        self.failed_workflows = 0
        self.total_state_transitions = 0

        self.logger.info("✅ FSM Core initialized successfully")


__all__ = ["FSMCore"]
