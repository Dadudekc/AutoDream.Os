"""
Legacy Manager Adapter - Phase-2 Manager Consolidation
======================================================

Provides backward compatibility for legacy managers.
Maps legacy manager calls to new core managers.

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

from __future__ import annotations
from typing import Dict, Any, Optional, Type
from ..contracts import Manager, ManagerContext, ManagerResult
from ..core_resource_manager import CoreResourceManager
from ..core_configuration_manager import CoreConfigurationManager
from ..core_execution_manager import CoreExecutionManager
from ..core_monitoring_manager import CoreMonitoringManager
from ..core_service_manager import CoreServiceManager


class LegacyManagerAdapter(Manager):
    """Adapter for legacy managers to use new core managers."""

    def __init__(self, legacy_name: str, core_manager: Manager):
        """Initialize legacy manager adapter."""
        self.legacy_name = legacy_name
        self.core_manager = core_manager

    def initialize(self, context: ManagerContext) -> bool:
        """Initialize legacy manager adapter."""
        return self.core_manager.initialize(context)

    def execute(
        self, context: ManagerContext, operation: str, payload: Dict[str, Any]
    ) -> ManagerResult:
        """Execute operation through core manager."""
        # Map legacy operations to core operations
        mapped_operation = self._map_operation(operation)
        mapped_payload = self._map_payload(operation, payload)

        return self.core_manager.execute(context, mapped_operation, mapped_payload)

    def cleanup(self, context: ManagerContext) -> bool:
        """Cleanup legacy manager adapter."""
        return self.core_manager.cleanup(context)

    def get_status(self) -> Dict[str, Any]:
        """Get legacy manager status."""
        status = self.core_manager.get_status()
        status["legacy_name"] = self.legacy_name
        status["adapter_type"] = "legacy"
        return status

    def _map_operation(self, operation: str) -> str:
        """Map legacy operation to core operation."""
        operation_mapping = {
            # FileManager operations
            "read_file": "file_operation",
            "write_file": "file_operation",
            "copy_file": "file_operation",
            "move_file": "file_operation",
            "delete_file": "file_operation",
            "file_exists": "file_operation",
            "list_directory": "file_operation",
            "create_directory": "file_operation",
            "get_file_size": "file_operation",
            # AgentContextManager operations
            "set_agent_context": "context_operation",
            "get_agent_context": "context_operation",
            "update_agent_context": "context_operation",
            "delete_agent_context": "context_operation",
            "get_all_agents": "context_operation",
            "clear_all_contexts": "context_operation",
            # ConfigurationManager operations
            "load_config": "load_config",
            "save_config": "save_config",
            "validate_config": "validate_config",
            "get_all_configs": "get_all_configs",
            "export_config": "export_config",
            "import_config": "import_config",
            # ExecutionManager operations
            "execute_task": "execute_task",
            "register_protocol": "register_protocol",
            "get_execution_status": "get_execution_status",
            "create_task": "create_task",
            "cancel_task": "cancel_task",
            "list_tasks": "list_tasks",
            "list_protocols": "list_protocols",
            # MonitoringManager operations
            "create_alert": "create_alert",
            "record_metric": "record_metric",
            "create_widget": "create_widget",
            "get_alerts": "get_alerts",
            "get_metrics": "get_metrics",
            "get_widgets": "get_widgets",
            "acknowledge_alert": "acknowledge_alert",
            "resolve_alert": "resolve_alert",
            # ServiceManager operations
            "onboard_agent": "onboard_agent",
            "recover_from_error": "recover_from_error",
            "process_results": "process_results",
            "start_onboarding": "start_onboarding",
            "complete_onboarding": "complete_onboarding",
            "register_recovery_strategy": "register_recovery_strategy",
            "get_onboarding_status": "get_onboarding_status",
            "get_recovery_strategies": "get_recovery_strategies",
            "get_results": "get_results",
        }

        return operation_mapping.get(operation, operation)

    def _map_payload(self, operation: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Map legacy payload to core payload."""
        if operation.startswith("file_"):
            return self._map_file_payload(operation, payload)
        elif operation.startswith("context_"):
            return self._map_context_payload(operation, payload)
        elif operation.startswith("config_"):
            return self._map_config_payload(operation, payload)
        elif operation.startswith("task_") or operation.startswith("execution_"):
            return self._map_execution_payload(operation, payload)
        elif (
            operation.startswith("alert_")
            or operation.startswith("metric_")
            or operation.startswith("widget_")
        ):
            return self._map_monitoring_payload(operation, payload)
        elif (
            operation.startswith("onboard_")
            or operation.startswith("recover_")
            or operation.startswith("result_")
        ):
            return self._map_service_payload(operation, payload)
        else:
            return payload

    def _map_file_payload(
        self, operation: str, payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Map file operation payload."""
        mapped = {"file_operation": operation}

        if operation == "read_file":
            mapped["file_path"] = payload.get("file_path", "")
        elif operation == "write_file":
            mapped["file_path"] = payload.get("file_path", "")
            mapped["content"] = payload.get("content", "")
        elif operation == "copy_file":
            mapped["file_path"] = payload.get("source", "")
            mapped["destination"] = payload.get("destination", "")
        elif operation == "move_file":
            mapped["file_path"] = payload.get("source", "")
            mapped["destination"] = payload.get("destination", "")
        elif operation == "delete_file":
            mapped["file_path"] = payload.get("file_path", "")
        elif operation == "file_exists":
            mapped["file_path"] = payload.get("file_path", "")
        elif operation == "list_directory":
            mapped["file_path"] = payload.get("directory", "")
        elif operation == "create_directory":
            mapped["file_path"] = payload.get("directory", "")
        elif operation == "get_file_size":
            mapped["file_path"] = payload.get("file_path", "")

        return mapped

    def _map_context_payload(
        self, operation: str, payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Map context operation payload."""
        mapped = {"context_operation": operation}

        if operation == "set_agent_context":
            mapped["agent_id"] = payload.get("agent_id", "")
            mapped["context_data"] = payload.get("context", {})
        elif operation == "get_agent_context":
            mapped["agent_id"] = payload.get("agent_id", "")
        elif operation == "update_agent_context":
            mapped["agent_id"] = payload.get("agent_id", "")
            mapped["updates"] = payload.get("updates", {})
        elif operation == "delete_agent_context":
            mapped["agent_id"] = payload.get("agent_id", "")

        return mapped

    def _map_config_payload(
        self, operation: str, payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Map configuration operation payload."""
        mapped = {}

        if operation == "load_config":
            mapped["config_key"] = payload.get("config_key", "")
        elif operation == "save_config":
            mapped["config_key"] = payload.get("config_key", "")
            mapped["config_data"] = payload.get("config_data", {})
        elif operation == "validate_config":
            mapped["config_data"] = payload.get("config_data", {})
        elif operation == "export_config":
            mapped["config_key"] = payload.get("config_key", "")
            mapped["export_path"] = payload.get("export_path", "")
        elif operation == "import_config":
            mapped["import_path"] = payload.get("import_path", "")
            mapped["config_key"] = payload.get("config_key", "")

        return mapped

    def _map_execution_payload(
        self, operation: str, payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Map execution operation payload."""
        mapped = {}

        if operation == "execute_task":
            mapped["task_id"] = payload.get("task_id", "")
            mapped["task_data"] = payload.get("task_data", {})
        elif operation == "register_protocol":
            mapped["protocol_name"] = payload.get("protocol_name", "")
            mapped["protocol_data"] = payload.get("protocol_data", {})
        elif operation == "get_execution_status":
            mapped["execution_id"] = payload.get("execution_id", "")
        elif operation == "create_task":
            mapped["task_id"] = payload.get("task_id", "")
            mapped["task_type"] = payload.get("task_type", "general")
            mapped["task_data"] = payload.get("task_data", {})
            mapped["priority"] = payload.get("priority", 1)
        elif operation == "cancel_task":
            mapped["task_id"] = payload.get("task_id", "")
        elif operation == "list_tasks":
            mapped["status_filter"] = payload.get("status_filter")
            mapped["task_type_filter"] = payload.get("task_type_filter")
        elif operation == "list_protocols":
            mapped["protocol_type_filter"] = payload.get("protocol_type_filter")

        return mapped

    def _map_monitoring_payload(
        self, operation: str, payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Map monitoring operation payload."""
        mapped = {}

        if operation == "create_alert":
            mapped["alert_data"] = payload
        elif operation == "record_metric":
            mapped["metric_name"] = payload.get("metric_name", "")
            mapped["metric_value"] = payload.get("metric_value")
        elif operation == "create_widget":
            mapped["widget_data"] = payload
        elif operation == "get_alerts":
            mapped["level_filter"] = payload.get("level_filter")
            mapped["status_filter"] = payload.get("status_filter")
            mapped["source_filter"] = payload.get("source_filter")
        elif operation == "get_metrics":
            mapped["metric_name_filter"] = payload.get("metric_name_filter")
            mapped["include_history"] = payload.get("include_history", False)
        elif operation == "get_widgets":
            mapped["widget_type_filter"] = payload.get("widget_type_filter")
            mapped["enabled_only"] = payload.get("enabled_only", False)
        elif operation == "acknowledge_alert":
            mapped["alert_id"] = payload.get("alert_id", "")
            mapped["acknowledged_by"] = payload.get("acknowledged_by", "system")
        elif operation == "resolve_alert":
            mapped["alert_id"] = payload.get("alert_id", "")
            mapped["resolved_by"] = payload.get("resolved_by", "system")
            mapped["resolution_notes"] = payload.get("resolution_notes", "")

        return mapped

    def _map_service_payload(
        self, operation: str, payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Map service operation payload."""
        mapped = {}

        if operation == "onboard_agent":
            mapped["agent_data"] = payload
        elif operation == "recover_from_error":
            mapped["error_data"] = payload
        elif operation == "process_results":
            mapped["results_data"] = payload
        elif operation == "start_onboarding":
            mapped["session_id"] = payload.get("session_id", "")
        elif operation == "complete_onboarding":
            mapped["session_id"] = payload.get("session_id", "")
            mapped["success"] = payload.get("success", True)
            mapped["notes"] = payload.get("notes", "")
        elif operation == "register_recovery_strategy":
            mapped["strategy_name"] = payload.get("strategy_name", "")
            mapped["strategy_type"] = payload.get("strategy_type", "retry")
            mapped["conditions"] = payload.get("conditions", {})
            mapped["actions"] = payload.get("actions", [])
            mapped["enabled"] = payload.get("enabled", True)
        elif operation == "get_onboarding_status":
            mapped["session_id"] = payload.get("session_id", "")
        elif operation == "get_recovery_strategies":
            mapped["strategy_type_filter"] = payload.get("strategy_type_filter")
        elif operation == "get_results":
            mapped["result_type_filter"] = payload.get("result_type_filter")
            mapped["status_filter"] = payload.get("status_filter")

        return mapped


# Legacy manager factory
def create_legacy_manager_adapter(legacy_name: str) -> LegacyManagerAdapter:
    """Create a legacy manager adapter."""
    # Map legacy names to core managers
    manager_mapping = {
        "FileManager": CoreResourceManager(),
        "AgentContextManager": CoreResourceManager(),
        "FileLockManager": CoreResourceManager(),
        "ConfigurationManager": CoreConfigurationManager(),
        "DiscordConfigurationManager": CoreConfigurationManager(),
        "ConfigManager": CoreConfigurationManager(),
        "ExecutionManager": CoreExecutionManager(),
        "TaskManager": CoreExecutionManager(),
        "ProtocolManager": CoreExecutionManager(),
        "AlertManager": CoreMonitoringManager(),
        "MetricManager": CoreMonitoringManager(),
        "WidgetManager": CoreMonitoringManager(),
        "GamingAlertManager": CoreMonitoringManager(),
        "ArchitecturalOnboardingManager": CoreServiceManager(),
        "ErrorRecoveryManager": CoreServiceManager(),
        "ResultsManager": CoreServiceManager(),
    }

    core_manager = manager_mapping.get(legacy_name)
    if not core_manager:
        raise ValueError(f"Unknown legacy manager: {legacy_name}")

    return LegacyManagerAdapter(legacy_name, core_manager)
