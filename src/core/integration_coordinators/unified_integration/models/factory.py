"""
Integration Models Factory - V2 Compliance Module
================================================

Factory for creating integration models.

V2 Compliance: < 300 lines, single responsibility, factory.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

from typing import Dict, Any, List
from datetime import datetime

from .core_models import (
    IntegrationMetrics,
    OptimizationConfig,
    PerformanceReport,
    OptimizationRecommendation,
)
from .config_models import (
    IntegrationConfig,
    IntegrationTask,
    IntegrationRequest,
    IntegrationResponse,
)


class IntegrationModels:
    """Factory class for creating integration models."""

    @staticmethod
    def create_integration_metrics(
        total_integrations: int,
        successful_integrations: int,
        failed_integrations: int,
        average_response_time: float,
    ) -> IntegrationMetrics:
        """Create integration metrics."""
        return IntegrationMetrics(
            total_integrations=total_integrations,
            successful_integrations=successful_integrations,
            failed_integrations=failed_integrations,
            average_response_time=average_response_time,
            last_updated=datetime.now(),
        )

    @staticmethod
    def create_optimization_config(
        enable_caching: bool = True,
        max_retries: int = 3,
        timeout_seconds: int = 30,
        batch_size: int = 100,
    ) -> OptimizationConfig:
        """Create optimization config."""
        return OptimizationConfig(
            enable_caching=enable_caching,
            max_retries=max_retries,
            timeout_seconds=timeout_seconds,
            batch_size=batch_size,
        )

    @staticmethod
    def create_integration_config(
        config_id: str,
        name: str,
        description: str,
        enabled: bool = True,
        parameters: Dict[str, Any] = None,
    ) -> IntegrationConfig:
        """Create integration config."""
        return IntegrationConfig(
            config_id=config_id,
            name=name,
            description=description,
            enabled=enabled,
            parameters=parameters or {},
            created_at=datetime.now(),
        )

    @staticmethod
    def create_integration_task(
        task_id: str,
        task_type: str,
        status: str = "PENDING",
        parameters: Dict[str, Any] = None,
    ) -> IntegrationTask:
        """Create integration task."""
        return IntegrationTask(
            task_id=task_id,
            task_type=task_type,
            status=status,
            parameters=parameters or {},
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
