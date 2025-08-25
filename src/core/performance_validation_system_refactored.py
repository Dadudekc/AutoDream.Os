#!/usr/bin/env python3
"""Orchestrator linking the performance validation modules."""
import argparse
import json
import logging
from typing import Any, Dict, Optional

from .agent_manager import AgentManager
from .config.config_manager import ConfigManager
from .assignment_engine import ContractManager
from .workflow import (
    WorkflowOrchestrator as AdvancedWorkflowEngine,
)
from .performance_validation_core import PerformanceValidationCore
from .performance_validation_tester import PerformanceValidationTester
from .performance_validation_reporter import PerformanceValidationReporter
from .performance_validation_config import PerformanceValidationConfig

logger = logging.getLogger(__name__)


class PerformanceValidationSystem:
    """High-level interface for running performance validation."""

    def __init__(
        self,
        agent_manager: AgentManager,
        config_manager: ConfigManager,
        contract_manager: ContractManager,
        workflow_engine: AdvancedWorkflowEngine,
        config: Optional[PerformanceValidationConfig] = None,
    ) -> None:
        self.core = PerformanceValidationCore(
            agent_manager, config_manager, contract_manager, workflow_engine, config
        )
        self.tester = PerformanceValidationTester(self.core)
        self.reporter = PerformanceValidationReporter(self.core)

    def run_comprehensive_benchmark(self) -> str:
        return self.core.run_comprehensive_benchmark(self.tester, self.reporter)

    def get_latest_performance_report(self):
        return self.core.get_latest_performance_report()

    def get_benchmark_summary(self):
        return self.core.get_benchmark_summary()

    def get_active_alerts(self):
        return self.core.get_active_alerts()

    def get_alert_summary(self):
        return self.core.get_alert_summary()

    def run_smoke_test(self) -> bool:
        try:
            benchmark_id = self.run_comprehensive_benchmark()
            if not benchmark_id:
                return False
            if not self.get_latest_performance_report():
                return False
            summary = self.get_benchmark_summary()
            if "total_benchmarks" not in summary:
                return False
            return True
        except Exception as e:
            logger.error(f"Smoke test failed: {e}")
            return False


def run_smoke_test() -> bool:
    """Run basic functionality test for PerformanceValidationSystem."""
    try:
        config_manager = ConfigManager()
        agent_manager = AgentManager()
        contract_manager = ContractManager(agent_manager, config_manager)

        class MockWorkflowEngine:
            def __init__(self):
                self.workflows: Dict[str, Any] = {}

        workflow_engine = MockWorkflowEngine()

        perf_system = PerformanceValidationSystem(
            agent_manager, config_manager, contract_manager, workflow_engine
        )
        success = perf_system.run_smoke_test()
        if success:
            logger.info("✅ PerformanceValidationSystem Smoke Test PASSED")
        else:
            logger.error("❌ PerformanceValidationSystem Smoke Test FAILED")
        return success
    except Exception as e:
        logger.error(f"❌ PerformanceValidationSystem Smoke Test FAILED: {e}")
        return False


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Performance Validation System CLI"
    )
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    parser.add_argument(
        "--benchmark", action="store_true", help="Run comprehensive benchmark"
    )
    parser.add_argument("--summary", action="store_true", help="Show benchmark summary")
    parser.add_argument("--report", action="store_true", help="Show latest performance report")

    args = parser.parse_args()

    if args.test:
        run_smoke_test()
        return

    config_manager = ConfigManager()
    agent_manager = AgentManager()
    contract_manager = ContractManager(agent_manager, config_manager)

    class MockWorkflowEngine:
        def __init__(self):
            self.workflows: Dict[str, Any] = {}

    workflow_engine = MockWorkflowEngine()

    perf_system = PerformanceValidationSystem(
        agent_manager, config_manager, contract_manager, workflow_engine
    )

    if args.benchmark:
        benchmark_id = perf_system.run_comprehensive_benchmark()
        print(f"Benchmark completed: {benchmark_id}")

    if args.summary:
        summary = perf_system.get_benchmark_summary()
        print("Benchmark Summary:")
        print(json.dumps(summary, indent=2))

    if args.report:
        report = perf_system.get_latest_performance_report()
        if report:
            formatted = perf_system.core.report_generator.format_report_as_text(report)
            print(formatted)
        else:
            print("No performance reports available")


if __name__ == "__main__":
    main()
