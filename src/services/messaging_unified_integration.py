#!/usr/bin/env python3
"""
Messaging Unified Integration Service - V2 Compliance Module
=========================================================

Handles integration with unified logging and configuration systems.
Extracted from monolithic messaging_core.py for V2 compliance.

Responsibilities:
- Unified logging system integration
- Configuration system integration
- Metrics tracking integration
- Cross-system coordination

V2 Compliance: < 300 lines, single responsibility, unified systems integration.

Author: Agent-2 - Architecture & Design Specialist
License: MIT
"""


# Try to import unified systems for pattern elimination enhancement
try:
    # Import unified configuration system with hyphenated filename


    spec = importlib.util.spec_from_file_location(
        "unified_configuration_system",
        get_unified_utility().Path(__file__).parent.parent / "core" / "unified-configuration-system.py",
    )
    unified_config_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(unified_config_module)
    UnifiedConfigurationSystem = unified_config_module.UnifiedConfigurationSystem
    ConfigType = unified_config_module.ConfigType

    UNIFIED_SYSTEMS_AVAILABLE = True
except ImportError:
    UNIFIED_SYSTEMS_AVAILABLE = False


class MessagingUnifiedIntegration:
    """
    Service for unified systems integration.

    V2 Compliance: Centralized integration with unified logging and configuration.
    """

    def __init__(self):
        """Initialize unified integration service."""
        self.unified_logger = None
        self.unified_config = None
        self.metrics = None

        # Initialize unified systems if available
        self._initialize_unified_systems()

    def _initialize_unified_systems(self):
        """Initialize unified systems with fallback handling."""
        if UNIFIED_SYSTEMS_AVAILABLE:
            try:
                self.unified_logger = get_unified_logger()
                self.unified_config = UnifiedConfigurationSystem()
                self.metrics = MessagingMetrics()
            except Exception as e:
                get_logger(__name__).info(f"Warning: Unified systems initialization failed: {e}")
                self.unified_logger = None
                self.unified_config = None
                self.metrics = None
        else:
            get_logger(__name__).info("Info: Unified systems not available, using fallback mode")
            self.unified_logger = None
            self.unified_config = None
            self.metrics = None

    def get_logger(self):
        """
        Get unified logger instance.

        Returns:
            Logger instance or None if not available
        """
        return self.unified_logger

    def get_config_system(self):
        """
        Get unified configuration system instance.

        Returns:
            Configuration system instance or None if not available
        """
        return self.unified_config

    def get_metrics(self):
        """
        Get metrics tracking instance.

        Returns:
            Metrics instance or None if not available
        """
        return self.metrics

    def get_unified_logger().log_operation_start(operation)_start(
        self, operation: str, context: Dict[str, Any]
    ) -> Optional[str]:
        """
        Log operation start with unified logging.

        Args:
            operation: Operation name
            context: Context information

        Returns:
            Operation ID for tracking
        """
        if self.unified_logger:
            try:
                return self.unified_logger.start_operation(operation, "Agent-6")
            except Exception:
                pass
        return None

    def get_unified_logger().log_operation_start(operation)_complete(
        self,
        operation: str,
        context: Dict[str, Any],
        operation_id: Optional[str] = None,
    ):
        """
        Log operation completion with unified logging.

        Args:
            operation: Operation name
            context: Context information
            operation_id: Operation ID for tracking
        """
        if self.unified_logger:
            try:
                self.unified_logger.log(
                    agent_id="Agent-6",
                    level="INFO",
                    message=f"Operation completed: {operation}",
                    context=context,
                    correlation_id=operation_id,
                    parent_operation=operation,
                )
            except Exception:
                pass

    def get_unified_logger().log_operation_start(operation)_error(
        self,
        operation: str,
        error: str,
        context: Dict[str, Any],
        operation_id: Optional[str] = None,
    ):
        """
        Log operation error with unified logging.

        Args:
            operation: Operation name
            error: Error message
            context: Context information
            operation_id: Operation ID for tracking
        """
        if self.unified_logger:
            try:
                self.unified_logger.log(
                    agent_id="Agent-6",
                    level="ERROR",
                    message=f"Operation failed: {operation} - {error}",
                    context={**context, "error": error},
                    correlation_id=operation_id,
                    parent_operation=operation,
                )
            except Exception:
                pass

    def log_message_delivery(
        self,
        recipient: str,
        message_type: str,
        success: bool,
        operation_id: Optional[str] = None,
    ):
        """
        Log message delivery with unified logging.

        Args:
            recipient: Message recipient
            message_type: Type of message delivered
            success: Whether delivery was successful
            operation_id: Operation ID for tracking
        """
        if self.unified_logger:
            try:
                level = "INFO" if success else "WARNING"
                status = "successful" if success else "failed"

                self.unified_logger.log(
                    agent_id="Agent-6",
                    level=level,
                    message=f"Message delivery {status} to {recipient}",
                    context={
                        "recipient": recipient,
                        "message_type": message_type,
                        "delivery_success": success,
                        "v2_compliance": "unified_logging",
                    },
                    correlation_id=operation_id,
                    parent_operation="message_delivery",
                )
            except Exception:
                pass

    def get_configuration_value(
        self, config_type: str, key: str, default: Any = None
    ) -> Any:
        """
        Get configuration value from unified configuration system.

        Args:
            config_type: Type of configuration
            key: Configuration key
            default: Default value if not found

        Returns:
            Configuration value or default
        """
        if self.unified_config:
            try:
                return self.unified_config.get_config_value(config_type, key, default)
            except Exception:
                pass
        return default

    def set_configuration_value(self, config_type: str, key: str, value: Any) -> bool:
        """
        Set configuration value in unified configuration system.

        Args:
            config_type: Type of configuration
            key: Configuration key
            value: Value to set

        Returns:
            bool: True if successful
        """
        if self.unified_config:
            try:
                return self.unified_config.set_config_value(config_type, key, value)
            except Exception:
                pass
        return False

    def record_metric(
        self, metric_name: str, value: float, tags: Dict[str, str] = None
    ):
        """
        Record metric with unified metrics system.

        Args:
            metric_name: Name of the metric
            value: Metric value
            tags: Additional tags for the metric
        """
        if self.metrics:
            try:
                self.metrics.record_metric(metric_name, value, tags or {})
            except Exception:
                pass

    def get_system_health(self) -> Dict[str, Any]:
        """
        Get system health status from unified systems.

        Returns:
            Dict containing system health information
        """
        health_status = {
            "unified_logging": self.unified_logger is not None,
            "unified_config": self.unified_config is not None,
            "metrics_system": self.metrics is not None,
            "overall_health": "healthy",
        }

        # Determine overall health
        if not any(
            [
                health_status["unified_logging"],
                health_status["unified_config"],
                health_status["metrics_system"],
            ]
        ):
            health_status["overall_health"] = "degraded"
        elif all(
            [
                health_status["unified_logging"],
                health_status["unified_config"],
                health_status["metrics_system"],
            ]
        ):
            health_status["overall_health"] = "optimal"

        return health_status

    def get_integration_status(self) -> Dict[str, Any]:
        """
        Get integration status with unified systems.

        Returns:
            Dict containing integration status
        """
        return {
            "unified_systems_available": UNIFIED_SYSTEMS_AVAILABLE,
            "logging_integration": self.unified_logger is not None,
            "config_integration": self.unified_config is not None,
            "metrics_integration": self.metrics is not None,
            "v2_compliance_level": "high" if UNIFIED_SYSTEMS_AVAILABLE else "medium",
            "pattern_elimination": UNIFIED_SYSTEMS_AVAILABLE,
        }

    def validate_unified_systems(self) -> Dict[str, Any]:
        """
        Validate unified systems integration.

        Returns:
            Dict containing validation results
        """
        validation_results = {
            "overall_valid": True,
            "issues": [],
            "recommendations": [],
        }

        # Check unified systems availability
        if not get_unified_validator().validate_required(UNIFIED_SYSTEMS_AVAILABLE):
            validation_results["issues"].append("Unified systems not available")
            validation_results["recommendations"].append(
                "Install unified systems for enhanced V2 compliance"
            )
            validation_results["overall_valid"] = False

        # Validate individual systems
        if self.unified_logger is None:
            validation_results["issues"].append(
                "Unified logging system not initialized"
            )
            validation_results["recommendations"].append(
                "Check unified logging system configuration"
            )

        if self.unified_config is None:
            validation_results["issues"].append(
                "Unified configuration system not initialized"
            )
            validation_results["recommendations"].append(
                "Check unified configuration system setup"
            )

        if self.metrics is None:
            validation_results["issues"].append("Metrics system not initialized")
            validation_results["recommendations"].append(
                "Check metrics system configuration"
            )

        return validation_results


# Factory function for dependency injection
def create_messaging_unified_integration() -> MessagingUnifiedIntegration:
    """
    Factory function to create MessagingUnifiedIntegration.
    """
    return MessagingUnifiedIntegration()


# Export service interface
__all__ = ["MessagingUnifiedIntegration", "create_messaging_unified_integration"]
