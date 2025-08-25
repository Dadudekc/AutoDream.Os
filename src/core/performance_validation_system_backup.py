#!/usr/bin/env python3
"""Backup Performance Validation System orchestrator.

This module provides a thin wrapper around the modular performance
validation components. It preserves the public API of the original
monolithic implementation while delegating metrics collection,
validation, reporting and alerting to dedicated modules.
"""

import logging
import uuid
from datetime import datetime
from typing import List

from src.utils.stability_improvements import stability_manager, safe_import

from .agent_manager import AgentManager, AgentStatus, AgentCapability, AgentInfo
from .config.config_manager import ConfigManager
from .assignment_engine import ContractManager
from .contract_models import ContractPriority, ContractStatus
from .workflow import (
    WorkflowOrchestrator as AdvancedWorkflowEngine,
    WorkflowType,
    TaskPriority as WorkflowPriority,
    WorkflowTask as WorkflowStep,
)

# Extracted performance modules
from .performance.metrics.collector import (
    MetricsCollector,
    BenchmarkType,
    PerformanceLevel,
    PerformanceBenchmark,
)
from .performance.validation.rules import ValidationRules, OptimizationTarget
from .performance.reporting.generator import ReportGenerator, SystemPerformanceReport
from .performance.alerts.manager import AlertManager, AlertSeverity, AlertType

logger = logging.getLogger(__name__)


class PerformanceValidationSystem:
    """Orchestrates performance benchmarking using modular components."""

    def __init__(
        self,
        agent_manager: AgentManager,
        config_manager: ConfigManager,
        contract_manager: ContractManager,
        workflow_engine: AdvancedWorkflowEngine,
    ):
        self.agent_manager = agent_manager
        self.config_manager = config_manager
        self.contract_manager = contract_manager
        self.workflow_engine = workflow_engine

        # Modular components
        self.metrics_collector = MetricsCollector()
        self.validation_rules = ValidationRules()
        self.report_generator = ReportGenerator()
        self.alert_manager = AlertManager()

        self._setup_alert_handlers()
        self.logger = logging.getLogger(f"{__name__}.PerformanceValidationSystem")

    def run_comprehensive_benchmark(self) -> str:
        """Run the full benchmark suite using modular components."""
        try:
            benchmark_id = str(uuid.uuid4())
            start_time = datetime.now()

            self.logger.info(f"Starting comprehensive benchmark: {benchmark_id}")

            benchmarks = [
                self._run_response_time_benchmark(),
                self._run_throughput_benchmark(),
                self._run_scalability_benchmark(),
                self._run_reliability_benchmark(),
                self._run_latency_benchmark(),
            ]

            overall = self.validation_rules.calculate_overall_performance_level(benchmarks)

            recommendations: List[str] = []
            for benchmark in benchmarks:
                recommendations.extend(
                    self.validation_rules.generate_optimization_recommendations(benchmark)
                )
                self.alert_manager.check_benchmark_for_alerts(benchmark)

            # Deduplicate recommendations while preserving order
            unique_recommendations: List[str] = []
            seen = set()
            for rec in recommendations:
                if rec not in seen:
                    unique_recommendations.append(rec)
                    seen.add(rec)

            self.report_generator.generate_performance_report(
                benchmarks, overall, unique_recommendations
            )

            duration = (datetime.now() - start_time).total_seconds()
            self.logger.info(
                f"Completed comprehensive benchmark: {benchmark_id} "
                f"(Duration: {duration:.2f}s, Level: {overall.value})"
            )
            return benchmark_id

        except Exception as e:
            self.logger.error(f"Comprehensive benchmark failed: {e}")
            return ""

    # --- Benchmark placeholders -------------------------------------------------
    def _run_response_time_benchmark(self) -> PerformanceBenchmark:
        raise NotImplementedError("Response time benchmark not implemented in backup system")

    def _run_throughput_benchmark(self) -> PerformanceBenchmark:
        raise NotImplementedError("Throughput benchmark not implemented in backup system")

    def _run_scalability_benchmark(self) -> PerformanceBenchmark:
        raise NotImplementedError("Scalability benchmark not implemented in backup system")

    def _run_reliability_benchmark(self) -> PerformanceBenchmark:
        raise NotImplementedError("Reliability benchmark not implemented in backup system")

    def _run_latency_benchmark(self) -> PerformanceBenchmark:
        raise NotImplementedError("Latency benchmark not implemented in backup system")

    # --- Alert utilities --------------------------------------------------------
    def get_active_alerts(self):
        return self.alert_manager.get_active_alerts()

    def get_alert_summary(self):
        return self.alert_manager.get_alert_summary()

    def _setup_alert_handlers(self) -> None:
        """Register default alert handlers that log warnings."""

        def log_alert(alert):
            self.logger.warning(
                f"{alert.severity.value.upper()} alert: {alert.title} - {alert.message}"
            )

        # Register the same handler for all severities for simplicity
        self.alert_manager.register_alert_handler(AlertSeverity.CRITICAL, log_alert)
        self.alert_manager.register_alert_handler(AlertSeverity.HIGH, log_alert)
        self.alert_manager.register_alert_handler(AlertSeverity.MEDIUM, log_alert)
        self.alert_manager.register_alert_handler(AlertSeverity.LOW, log_alert)


__all__ = ["PerformanceValidationSystem"]

