"""Core utilities for the Performance Validation System."""
import logging
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from .agent_manager import AgentManager
from .config.config_manager import ConfigManager
from .assignment_engine import ContractManager
from .workflow import (
    WorkflowOrchestrator as AdvancedWorkflowEngine,
)
from .performance.metrics.collector import (
    MetricsCollector,
    BenchmarkType,
    PerformanceLevel,
    PerformanceBenchmark,
)
from .performance.validation.rules import ValidationRules
from .performance.reporting.generator import ReportGenerator, SystemPerformanceReport
from .performance.alerts.manager import AlertManager, AlertSeverity
from .performance_validation_config import PerformanceValidationConfig


class PerformanceValidationCore:
    """Holds shared state and common helpers for validation modules."""

    def __init__(
        self,
        agent_manager: AgentManager,
        config_manager: ConfigManager,
        contract_manager: ContractManager,
        workflow_engine: AdvancedWorkflowEngine,
        config: Optional[PerformanceValidationConfig] = None,
    ) -> None:
        self.agent_manager = agent_manager
        self.config_manager = config_manager
        self.contract_manager = contract_manager
        self.workflow_engine = workflow_engine
        self.config = config or PerformanceValidationConfig()

        self.metrics_collector = MetricsCollector()
        self.validation_rules = ValidationRules()
        self.report_generator = ReportGenerator()
        self.alert_manager = AlertManager()
        self.logger = logging.getLogger(f"{__name__}.PerformanceValidationCore")
        self._setup_alert_handlers()

    # ------------------------------------------------------------------
    # Benchmark orchestration
    # ------------------------------------------------------------------
    def run_comprehensive_benchmark(self, tester, reporter) -> str:
        """Run all benchmark types using provided tester and reporter."""
        benchmark_id = str(uuid.uuid4())
        start_time = datetime.now()
        self.logger.info(f"Starting comprehensive benchmark: {benchmark_id}")

        benchmark_results = [
            tester.run_response_time_benchmark(),
            tester.run_throughput_benchmark(),
            tester.run_scalability_benchmark(),
            tester.run_reliability_benchmark(),
            tester.run_latency_benchmark(),
        ]

        report = reporter.generate_report(benchmark_results)

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        self.logger.info(
            f"Completed comprehensive benchmark: {benchmark_id} "
            f"(Duration: {duration:.2f}s, Level: {report.overall_performance_level.value})"
        )
        return benchmark_id

    # ------------------------------------------------------------------
    # Utility helpers
    # ------------------------------------------------------------------
    def create_failed_benchmark(
        self, benchmark_type: BenchmarkType, test_name: str
    ) -> PerformanceBenchmark:
        """Create a placeholder benchmark when execution fails."""
        return PerformanceBenchmark(
            benchmark_id=str(uuid.uuid4()),
            benchmark_type=benchmark_type,
            test_name=test_name,
            start_time=datetime.now().isoformat(),
            end_time=datetime.now().isoformat(),
            duration=0.0,
            metrics={},
            target_metrics={},
            performance_level=PerformanceLevel.NOT_READY,
            optimization_recommendations=[
                "Benchmark execution failed - investigate system issues"
            ],
        )

    def get_latest_performance_report(self) -> Optional[SystemPerformanceReport]:
        """Return the most recent performance report."""
        return self.report_generator.get_latest_report()

    def get_benchmark_summary(self) -> Dict[str, Any]:
        """Return summary statistics for benchmarks."""
        return self.metrics_collector.get_benchmark_summary()

    def get_active_alerts(self) -> List:
        """Expose active alerts from the alert manager."""
        return self.alert_manager.get_active_alerts()

    def get_alert_summary(self) -> Dict[str, Any]:
        """Return summary of all alerts."""
        return self.alert_manager.get_alert_summary()

    # ------------------------------------------------------------------
    # Alert handlers
    # ------------------------------------------------------------------
    def _setup_alert_handlers(self) -> None:
        def critical_alert_handler(alert):
            self.logger.critical(
                f"CRITICAL ALERT: {alert.title} - {alert.message}"
            )

        def high_alert_handler(alert):
            self.logger.error(
                f"HIGH ALERT: {alert.title} - {alert.message}"
            )

        def medium_alert_handler(alert):
            self.logger.warning(
                f"MEDIUM ALERT: {alert.title} - {alert.message}"
            )

        def low_alert_handler(alert):
            self.logger.info(f"LOW ALERT: {alert.title} - {alert.message}")

        self.alert_manager.register_alert_handler(
            AlertSeverity.CRITICAL, critical_alert_handler
        )
        self.alert_manager.register_alert_handler(
            AlertSeverity.HIGH, high_alert_handler
        )
        self.alert_manager.register_alert_handler(
            AlertSeverity.MEDIUM, medium_alert_handler
        )
        self.alert_manager.register_alert_handler(
            AlertSeverity.LOW, low_alert_handler
        )
