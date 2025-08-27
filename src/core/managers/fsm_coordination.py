#!/usr/bin/env python3
"""FSM coordination manager tying together FSM components."""

import logging
from typing import Any, Dict, List

from ..base_manager import BaseManager
from .fsm_state_transitions import FSMStateTransitionMixin
from .fsm_utils import (
    BridgeState,
    FSMCommunicationEvent,
    FSMTask,
    FSMUpdate,
)
from .fsm_analytics import FSMAnalyticsMixin
from .fsm_strategy import FSMStrategyMixin
from .fsm_operations import FSMOperationsMixin
from .fsm_persistence import FSMPersistenceMixin

logger = logging.getLogger(__name__)


class FSMSystemManager(
    FSMPersistenceMixin,
    FSMOperationsMixin,
    FSMStrategyMixin,
    FSMAnalyticsMixin,
    FSMStateTransitionMixin,
    BaseManager,
):
    """Unified FSM System Manager composed from dedicated mixins."""

    def __init__(self, config_path: str = "config/fsm_system_manager.json") -> None:
        super().__init__(
            manager_name="FSMSystemManager",
            config_path=config_path,
            enable_metrics=True,
            enable_events=True,
            enable_persistence=True,
        )

        self._tasks: Dict[str, FSMTask] = {}
        self._task_updates: List[FSMUpdate] = []
        self._communication_events: List[FSMCommunicationEvent] = []
        self._bridge_states: Dict[str, BridgeState] = {}

        self._task_execution_history: List[Dict[str, Any]] = []
        self._state_transition_history: List[Dict[str, Any]] = []
        self._communication_history: List[Dict[str, Any]] = []

        self.max_tasks_per_agent = 10
        self.task_timeout_hours = 24
        self.auto_cleanup_completed = True
        self.enable_discord_bridge = True

        self._load_manager_config()
        self._initialize_fsm_workspace()
        self._load_existing_tasks()
