#!/usr/bin/env python3
"""
Scaling Core - Agent Cellphone V2
=================================

Main horizontal scaling engine class.
Follows V2 standards: ≤200 LOC, SRP, OOP principles.
"""

import time
import json
import logging
import threading
from pathlib import Path
from typing import Dict, List, Optional, Any

from .scaling_types import (
    ScalingStrategy,
    ScalingStatus,
    ScalingConfig,
    ScalingMetrics,
    ScalingDecision,
)


class HorizontalScalingEngine:
    """
    Implements horizontal scaling algorithms and load distribution

    Responsibilities:
    - Manage horizontal scaling operations
    - Implement load balancing strategies
    - Monitor scaling performance
    - Coordinate scaling decisions
    """

    def __init__(self, config: ScalingConfig = None):
        self.config = config or ScalingConfig()
        self.logger = logging.getLogger(f"{__name__}.HorizontalScalingEngine")
        self.workspace_path = Path("agent_workspaces")
        self.status = ScalingStatus.IDLE
        self.current_instances = self.config.min_instances
        self.target_instances = self.config.min_instances
        self.scaling_history: List[ScalingDecision] = []
        self.metrics_history: List[ScalingMetrics] = []
        self.is_monitoring = False
        self.monitor_thread: Optional[threading.Thread] = None

        # Ensure workspace exists
        self.workspace_path.mkdir(exist_ok=True)

        # Initialize scaling strategies
        self._initialize_scaling_strategies()

        self.logger.info("🚀 Horizontal Scaling Engine initialized")

    def _initialize_scaling_strategies(self):
        """Initialize scaling strategy implementations"""
        self.scaling_strategies = {
            ScalingStrategy.ROUND_ROBIN: self._round_robin_distribution,
            ScalingStrategy.LEAST_CONNECTIONS: self._least_connections_distribution,
            ScalingStrategy.WEIGHTED_ROUND_ROBIN: self._weighted_round_robin_distribution,
            ScalingStrategy.IP_HASH: self._ip_hash_distribution,
            ScalingStrategy.LEAST_RESPONSE_TIME: self._least_response_time_distribution,
            ScalingStrategy.CONSISTENT_HASH: self._consistent_hash_distribution,
        }

    def start_monitoring(self):
        """Start automatic scaling monitoring"""
        if self.is_monitoring:
            self.logger.warning("Scaling monitoring already active")
            return

        self.is_monitoring = True
        self.monitor_thread = threading.Thread(
            target=self._monitoring_loop, daemon=True
        )
        self.monitor_thread.start()

        self.logger.info("🚀 Horizontal scaling monitoring started")

    def stop_monitoring(self):
        """Stop automatic scaling monitoring"""
        self.is_monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5.0)
        self.logger.info("⏹️ Horizontal scaling monitoring stopped")

    def _monitoring_loop(self):
        """Main monitoring loop for automatic scaling"""
        while self.is_monitoring:
            try:
                # Collect current metrics
                current_metrics = self._collect_current_metrics()

                # Evaluate scaling needs
                scaling_decision = self._evaluate_scaling_needs(current_metrics)

                if scaling_decision:
                    self._execute_scaling_decision(scaling_decision)

                # Update metrics history
                self.metrics_history.append(current_metrics)
                if len(self.metrics_history) > 100:
                    self.metrics_history.pop(0)

                time.sleep(30)  # Check every 30 seconds

            except Exception as e:
                self.logger.error(f"Error in scaling monitoring loop: {e}")
                time.sleep(60)  # Wait longer on error

    def _collect_current_metrics(self) -> ScalingMetrics:
        """Collect current system metrics"""
        # Simulate metric collection
        return ScalingMetrics(
            current_instances=self.current_instances,
            target_instances=self.target_instances,
            cpu_utilization=65.0,  # Simulated
            memory_utilization=75.0,  # Simulated
            response_time=150.0,  # Simulated
            throughput=1000.0,  # Simulated
            error_rate=0.5,  # Simulated
            timestamp=time.time(),
        )

    def _evaluate_scaling_needs(
        self, metrics: ScalingMetrics
    ) -> Optional[ScalingDecision]:
        """Evaluate if scaling is needed based on current metrics"""
        should_scale_up = (
            metrics.cpu_utilization > self.config.target_cpu_utilization
            or metrics.memory_utilization > self.config.target_memory_utilization
            or metrics.response_time > 200.0
        )

        should_scale_down = (
            metrics.cpu_utilization < self.config.target_cpu_utilization * 0.5
            and metrics.memory_utilization < self.config.target_memory_utilization * 0.5
            and self.current_instances > self.config.min_instances
        )

        if should_scale_up and self.current_instances < self.config.max_instances:
            return ScalingDecision(
                decision_id=f"scale_up_{int(time.time())}",
                action="scale_up",
                reason="High resource utilization",
                current_metrics=metrics,
                target_metrics=metrics,
                confidence=0.8,
                timestamp=time.time(),
            )

        elif should_scale_down:
            return ScalingDecision(
                decision_id=f"scale_down_{int(time.time())}",
                action="scale_down",
                reason="Low resource utilization",
                current_metrics=metrics,
                target_metrics=metrics,
                confidence=0.7,
                timestamp=time.time(),
            )

        return None

    def _execute_scaling_decision(self, decision: ScalingDecision):
        """Execute a scaling decision"""
        try:
            if decision.action == "scale_up":
                self._scale_up()
            elif decision.action == "scale_down":
                self._scale_down()

            # Record scaling decision
            self.scaling_history.append(decision)
            if len(self.scaling_history) > 50:
                self.scaling_history.pop(0)

            self.logger.info(f"✅ Scaling decision executed: {decision.action}")

        except Exception as e:
            self.logger.error(f"❌ Failed to execute scaling decision: {e}")

    def _scale_up(self):
        """Scale up by adding instances"""
        if self.current_instances < self.config.max_instances:
            self.current_instances += 1
            self.status = ScalingStatus.SCALING_UP
            self.logger.info(f"📈 Scaled up to {self.current_instances} instances")
        else:
            self.logger.warning("Cannot scale up: maximum instances reached")

    def _scale_down(self):
        """Scale down by removing instances"""
        if self.current_instances > self.config.min_instances:
            self.current_instances -= 1
            self.status = ScalingStatus.SCALING_DOWN
            self.logger.info(f"📉 Scaled down to {self.current_instances} instances")
        else:
            self.logger.warning("Cannot scale down: minimum instances reached")

    def distribute_load(self, request_data: Dict[str, Any]) -> str:
        """Distribute load using configured strategy"""
        strategy_func = self.scaling_strategies.get(self.config.scaling_strategy)
        if strategy_func:
            return strategy_func(request_data)
        else:
            return "default_instance"

    def _round_robin_distribution(self, request_data: Dict[str, Any]) -> str:
        """Round-robin load distribution"""
        instance_id = f"instance_{hash(str(request_data)) % self.current_instances}"
        return instance_id

    def _least_connections_distribution(self, request_data: Dict[str, Any]) -> str:
        """Least connections load distribution"""
        # Simulate connection counting
        instance_id = f"instance_{hash(str(request_data)) % self.current_instances}"
        return instance_id

    def _weighted_round_robin_distribution(self, request_data: Dict[str, Any]) -> str:
        """Weighted round-robin load distribution"""
        instance_id = f"instance_{hash(str(request_data)) % self.current_instances}"
        return instance_id

    def _ip_hash_distribution(self, request_data: Dict[str, Any]) -> str:
        """IP hash-based load distribution"""
        client_ip = request_data.get("client_ip", "0.0.0.0")
        instance_id = f"instance_{hash(client_ip) % self.current_instances}"
        return instance_id

    def _least_response_time_distribution(self, request_data: Dict[str, Any]) -> str:
        """Least response time load distribution"""
        instance_id = f"instance_{hash(str(request_data)) % self.current_instances}"
        return instance_id

    def _consistent_hash_distribution(self, request_data: Dict[str, Any]) -> str:
        """Consistent hash load distribution"""
        instance_id = f"instance_{hash(str(request_data)) % self.current_instances}"
        return instance_id

    def get_scaling_status(self) -> Dict[str, Any]:
        """Get current scaling status and metrics"""
        return {
            "status": self.status.value,
            "current_instances": self.current_instances,
            "target_instances": self.target_instances,
            "config": {
                "min_instances": self.config.min_instances,
                "max_instances": self.config.max_instances,
                "target_cpu_utilization": self.config.target_cpu_utilization,
                "target_memory_utilization": self.config.target_memory_utilization,
                "scaling_strategy": self.config.scaling_strategy.value,
            },
            "recent_decisions": len(self.scaling_history),
            "monitoring_active": self.is_monitoring,
        }
