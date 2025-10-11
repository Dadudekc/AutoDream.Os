"""
Base Manager Helper Utilities
==============================

Extract helper methods from base_manager.py for V2 compliance.

Author: Agent-2 - Architecture & Design Specialist
License: MIT
"""

from typing import Any


class ManagerPropertySync:
    """Helper for syncing backward compatibility properties."""

    @staticmethod
    def sync_properties(manager, state_tracker, metrics_tracker) -> None:
        """Sync backward compatibility properties with trackers."""
        manager.manager_type = state_tracker.manager_type
        manager.manager_name = state_tracker.manager_name
        manager.manager_id = state_tracker.manager_id
        manager.state = state_tracker.state
        manager.initialized_at = state_tracker.initialized_at
        manager.last_operation_at = state_tracker.last_operation_at
        manager.last_error = state_tracker.last_error
        manager.context = state_tracker.context
        manager.config = state_tracker.config
        manager.operation_count = metrics_tracker.operation_count
        manager.success_count = metrics_tracker.success_count
        manager.error_count = metrics_tracker.error_count


class ManagerStatusHelper:
    """Helper for manager status and health operations."""

    @staticmethod
    def get_comprehensive_status(
        manager, state_tracker, metrics_tracker, status_manager, logger
    ) -> dict[str, Any]:
        """Get comprehensive manager status."""
        try:
            base_status = status_manager.get_component_status(state_tracker.manager_id)
            manager_status = state_tracker.get_status_dict()
            manager_status.update(metrics_tracker.get_metrics_for_status())

            if base_status:
                manager_status.update(base_status)

            return manager_status

        except Exception as e:
            logger.error(f"Error getting status for {state_tracker.manager_name}: {e}")
            return {
                "manager_id": state_tracker.manager_id,
                "state": "error",
                "error": str(e),
                "last_error": str(e),
            }


class ManagerConfigHelper:
    """Helper for configuration management operations."""

    @staticmethod
    def update_config(
        manager,
        updates: dict[str, Any],
        state_tracker,
        validation_manager,
        configuration_manager,
        logger,
    ) -> bool:
        """Update manager configuration."""
        try:
            # Validate configuration updates
            validation_result = validation_manager.validate_config(
                config_data=updates, component_type=state_tracker.manager_type.value
            )

            if not validation_result.is_valid:
                logger.error(f"Invalid configuration updates: {validation_result.errors}")
                return False

            # Update configuration
            success = configuration_manager.update_component_config(
                component_id=state_tracker.manager_id, updates=updates
            )

            if success:
                state_tracker.config.update(updates)
                logger.info(f"Configuration updated for {state_tracker.manager_name}")
                ManagerPropertySync.sync_properties(manager, state_tracker, manager.metrics_tracker)
                return True
            else:
                logger.error(f"Failed to update configuration for {state_tracker.manager_name}")
                return False

        except Exception as e:
            logger.error(f"Error updating configuration for {state_tracker.manager_name}: {e}")
            return False
