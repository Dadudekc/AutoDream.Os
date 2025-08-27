#!/usr/bin/env python3
"""High-level scaling manager orchestrating monitor→decide→execute pipeline."""

import json
import logging
import threading
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..base_manager import BaseManager
from ..scaling import (
    LoadDistributor,
    ResourceMonitor,
    ScalingConfig,
    ScalingDecision,
    ScalingMetrics,
    ScalingDecider,
    ScalingExecutor,
    ScalingStatus,
    ScalingStrategy,
)
from ..scaling import forecasting, intelligence, optimization, patterns, reporting

logger = logging.getLogger(__name__)


class ScalingManager(BaseManager):
    """Coordinates scaling operations via dedicated components."""

    def __init__(self, config_path: str = "config/scaling_manager.json") -> None:
        super().__init__(
            manager_name="ScalingManager",
            config_path=config_path,
            enable_metrics=True,
            enable_events=True,
            enable_persistence=True,
        )
        # Configuration and state ------------------------------------------------
        self.scaling_config = ScalingConfig()
        self.current_instances = self.scaling_config.min_instances
        self.target_instances = self.scaling_config.min_instances
        self.scaling_status = ScalingStatus.IDLE
        self.metrics_history: List[ScalingMetrics] = []
        self.decision_history: List[ScalingDecision] = []
        self.performance_alerts: List[Dict[str, Any]] = []
        self.scaling_patterns: Dict[str, Any] = {}
        self.thresholds = {
            "cpu_utilization": 80.0,
            "memory_utilization": 85.0,
            "response_time": 200.0,
            "error_rate": 5.0,
            "scaling_frequency": 10,
        }
        # Component instances ----------------------------------------------------
        self.resource_monitor = ResourceMonitor()
        self.scaling_decider = ScalingDecider()
        self.scaling_executor = ScalingExecutor()
        self.distributor = LoadDistributor()
        # Monitoring helpers (unused but kept for compatibility) -----------------
        self.is_monitoring = False
        self.monitor_thread: Optional[threading.Thread] = None
        # Initialization ---------------------------------------------------------
        self._load_manager_config()
        self._initialize_workspace()

    # Core pipeline -------------------------------------------------------------
    def process_metrics(
        self, cpu_utilization: float, memory_utilization: float
    ) -> ScalingDecision:
        metrics = self.resource_monitor.collect(
            self.current_instances, cpu_utilization, memory_utilization
        )
        decision = self.scaling_decider.decide(metrics, self.scaling_config)
        new_instances, status = self.scaling_executor.execute(
            decision.action, self.current_instances, self.scaling_config
        )
        self.current_instances = new_instances
        self.scaling_status = status
        self.metrics_history.append(metrics)
        self.decision_history.append(decision)
        return decision

    def distribute_load(
        self,
        request_data: Dict[str, Any],
        strategy: ScalingStrategy,
        available_instances: List[str],
    ) -> str:
        """Delegate load distribution to the LoadDistributor."""
        return self.distributor.distribute(request_data, strategy, available_instances)

    # Delegated advanced capabilities ------------------------------------------
    def analyze_scaling_patterns(self, time_range_hours: int = 24) -> Dict[str, Any]:
        return patterns.analyze_scaling_patterns(self, time_range_hours)

    def create_intelligent_scaling_strategy(
        self, strategy_type: str, parameters: Dict[str, Any]
    ) -> str:
        return intelligence.create_intelligent_scaling_strategy(
            self, strategy_type, parameters
        )

    def execute_intelligent_scaling(
        self, strategy_id: str, current_metrics: ScalingMetrics
    ) -> Dict[str, Any]:
        return intelligence.execute_intelligent_scaling(self, strategy_id, current_metrics)

    def predict_scaling_needs(
        self, time_horizon_minutes: int = 30
    ) -> List[Dict[str, Any]]:
        return forecasting.predict_scaling_needs(self, time_horizon_minutes)

    def optimize_scaling_automatically(self) -> Dict[str, Any]:
        return optimization.optimize_scaling_automatically(self)

    def generate_scaling_report(self, report_type: str = "comprehensive") -> Dict[str, Any]:
        return reporting.generate_scaling_report(self, report_type)

    # Utility methods ----------------------------------------------------------
    def _initialize_workspace(self) -> None:
        self.workspace_path = Path("agent_workspaces")
        self.workspace_path.mkdir(exist_ok=True)
        logger.info("Scaling workspace initialized")

    def _load_manager_config(self) -> None:
        try:
            if Path(self.config_path).exists():
                with open(self.config_path, "r") as f:
                    config = json.load(f)
                if "scaling" in config:
                    sc = config["scaling"]
                    self.scaling_config.min_instances = sc.get("min_instances", 1)
                    self.scaling_config.max_instances = sc.get("max_instances", 10)
                    self.scaling_config.target_cpu_utilization = sc.get(
                        "target_cpu_utilization", 70.0
                    )
                    self.scaling_config.target_memory_utilization = sc.get(
                        "target_memory_utilization", 80.0
                    )
            else:
                logger.warning("Scaling config file not found: %s", self.config_path)
        except Exception as exc:  # pragma: no cover - defensive
            logger.error("Failed to load scaling config: %s", exc)

    def cleanup(self) -> None:
        try:
            if getattr(self, "is_monitoring", False) and hasattr(self, "stop_monitoring"):
                self.stop_monitoring()
            logger.info("ScalingManager cleanup completed")
        except Exception as exc:  # pragma: no cover - defensive
            logger.error("ScalingManager cleanup failed: %s", exc)
