"""
Manager Lifecycle - Base Manager Lifecycle Helpers
==================================================
Extracted from base_manager.py for V2 compliance.
Author: Agent-5 (refactored from Agent-2's base_manager.py) | License: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..shared_utilities import CleanupManager, InitializationManager, StatusManager
    from .contracts import ManagerContext
    from .manager_state import ManagerStateTracker


class ManagerLifecycleHelper:
    """Helps with manager initialization and cleanup using Phase 1 utilities."""

    def __init__(
        self,
        state_tracker: ManagerStateTracker,
        initialization_manager: InitializationManager,
        cleanup_manager: CleanupManager,
        status_manager: StatusManager,
        logger: Any,
    ):
        """Initialize lifecycle helper."""
        self.state_tracker = state_tracker
        self.initialization_manager = initialization_manager
        self.cleanup_manager = cleanup_manager
        self.status_manager = status_manager
        self.logger = logger

    def initialize(self, context: ManagerContext, manager_state_enum: Any) -> bool:
        """Handle standard initialization using Phase 1 InitializationManager."""
        try:
            self.state_tracker.set_state(manager_state_enum.INITIALIZING)
            self.state_tracker.context = context
            self.state_tracker.config = context.config.copy()
            self.logger.info(f"Initializing {self.state_tracker.manager_name} manager")
            init_context = {
                "manager_id": self.state_tracker.manager_id,
                "manager_type": self.state_tracker.manager_type.value,
                "config": self.state_tracker.config,
                "timestamp": context.timestamp,
            }
            success = self.initialization_manager.initialize_component(
                component_id=self.state_tracker.manager_id,
                component_type="manager",
                context=init_context,
            )
            if success:
                self.state_tracker.mark_initialized()
                self.status_manager.register_component(
                    component_id=self.state_tracker.manager_id,
                    component_type=self.state_tracker.manager_type.value,
                    metadata={
                        "manager_name": self.state_tracker.manager_name,
                        "initialized_at": self.state_tracker.initialized_at.isoformat(),
                        "config_keys": list(self.state_tracker.config.keys()),
                    },
                )
                self.logger.info(
                    f"{self.state_tracker.manager_name} manager initialized successfully"
                )
                return True
            else:
                self.state_tracker.mark_error("Initialization failed")
                self.logger.error(f"Failed to initialize {self.state_tracker.manager_name} manager")
                return False
        except Exception as e:
            self.state_tracker.mark_error(str(e))
            self.logger.error(
                f"Exception during initialization of {self.state_tracker.manager_name}: {e}"
            )
            return False

    def cleanup(self, context: ManagerContext, manager_state_enum: Any) -> bool:
        """Handle standard cleanup using Phase 1 CleanupManager."""
        try:
            self.state_tracker.set_state(manager_state_enum.CLEANING_UP)
            self.logger.info(f"Cleaning up {self.state_tracker.manager_name} manager")
            cleanup_context = {
                "manager_id": self.state_tracker.manager_id,
                "manager_type": self.state_tracker.manager_type.value,
            }
            success = self.cleanup_manager.cleanup_component(
                component_id=self.state_tracker.manager_id,
                component_type="manager",
                context=cleanup_context,
            )
            if success:
                self.state_tracker.set_state(manager_state_enum.TERMINATED)
                self.status_manager.unregister_component(self.state_tracker.manager_id)
                self.logger.info(
                    f"{self.state_tracker.manager_name} manager cleaned up successfully"
                )
                return True
            else:
                self.state_tracker.mark_error("Cleanup failed")
                self.logger.error(f"Failed to cleanup {self.state_tracker.manager_name} manager")
                return False
        except Exception as e:
            self.state_tracker.mark_error(str(e))
            self.logger.error(f"Exception during cleanup of {self.state_tracker.manager_name}: {e}")
            return False
