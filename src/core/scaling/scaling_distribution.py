#!/usr/bin/env python3
"""
Scaling Distribution - Agent Cellphone V2
=========================================

Load distribution and balancing functionality.
Follows V2 standards: ≤200 LOC, SRP, OOP principles.
"""

import time
import hashlib
import logging

from src.utils.stability_improvements import stability_manager, safe_import
from typing import Dict, List, Any, Optional
from collections import defaultdict

from .scaling_types import ScalingStrategy, ScalingMetrics


class LoadDistributor:
    """
    Handles load distribution across multiple instances.

    Responsibilities:
    - Implement various load balancing algorithms
    - Track instance health and performance
    - Optimize load distribution
    - Monitor distribution metrics
    """

    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.LoadDistributor")
        self.instance_connections = defaultdict(int)
        self.instance_response_times = defaultdict(list)
        self.instance_weights = defaultdict(float)
        self.distribution_history = []
        self.current_instance_index = 0

        # Initialize default weights
        self._initialize_default_weights()

    def _initialize_default_weights(self):
        """Initialize default instance weights"""
        for i in range(10):  # Support up to 10 instances
            instance_id = f"instance_{i}"
            self.instance_weights[instance_id] = 1.0

    def distribute_load(
        self,
        request_data: Dict[str, Any],
        strategy: ScalingStrategy,
        available_instances: List[str],
    ) -> str:
        """Distribute load using specified strategy"""
        if not available_instances:
            return "no_instances_available"

        try:
            if strategy == ScalingStrategy.ROUND_ROBIN:
                return self._round_robin_distribution(available_instances)
            elif strategy == ScalingStrategy.LEAST_CONNECTIONS:
                return self._least_connections_distribution(available_instances)
            elif strategy == ScalingStrategy.WEIGHTED_ROUND_ROBIN:
                return self._weighted_round_robin_distribution(available_instances)
            elif strategy == ScalingStrategy.IP_HASH:
                return self._ip_hash_distribution(request_data, available_instances)
            elif strategy == ScalingStrategy.LEAST_RESPONSE_TIME:
                return self._least_response_time_distribution(available_instances)
            elif strategy == ScalingStrategy.CONSISTENT_HASH:
                return self._consistent_hash_distribution(
                    request_data, available_instances
                )
            else:
                return self._fallback_distribution(available_instances)

        except Exception as e:
            self.logger.error(f"Load distribution error: {e}")
            return available_instances[0] if available_instances else "error"

    def _round_robin_distribution(self, available_instances: List[str]) -> str:
        """Round-robin load distribution"""
        if not available_instances:
            return "no_instances"

        instance = available_instances[
            self.current_instance_index % len(available_instances)
        ]
        self.current_instance_index += 1

        # Record distribution
        self._record_distribution(instance, "round_robin")

        return instance

    def _least_connections_distribution(self, available_instances: List[str]) -> str:
        """Least connections load distribution"""
        if not available_instances:
            return "no_instances"

        # Find instance with least connections
        instance = min(available_instances, key=lambda x: self.instance_connections[x])

        # Increment connection count
        self.instance_connections[instance] += 1

        # Record distribution
        self._record_distribution(instance, "least_connections")

        return instance

    def _weighted_round_robin_distribution(self, available_instances: List[str]) -> str:
        """Weighted round-robin load distribution"""
        if not available_instances:
            return "no_instances"

        # Calculate total weight
        total_weight = sum(self.instance_weights[inst] for inst in available_instances)
        if total_weight <= 0:
            return available_instances[0]

        # Use weighted selection
        current_weight = 0
        target_weight = (self.current_instance_index % 100) / 100.0 * total_weight

        for instance in available_instances:
            current_weight += self.instance_weights[instance]
            if current_weight >= target_weight:
                self.current_instance_index += 1
                self._record_distribution(instance, "weighted_round_robin")
                return instance

        # Fallback to first instance
        return available_instances[0]

    def _ip_hash_distribution(
        self, request_data: Dict[str, Any], available_instances: List[str]
    ) -> str:
        """IP hash-based load distribution"""
        if not available_instances:
            return "no_instances"

        # Extract client IP
        client_ip = request_data.get("client_ip", "0.0.0.0")

        # Hash the IP and select instance
        hash_value = hash(client_ip)
        instance_index = abs(hash_value) % len(available_instances)
        instance = available_instances[instance_index]

        # Record distribution
        self._record_distribution(instance, "ip_hash")

        return instance

    def _least_response_time_distribution(self, available_instances: List[str]) -> str:
        """Least response time load distribution"""
        if not available_instances:
            return "no_instances"

        # Find instance with best response time
        best_instance = available_instances[0]
        best_response_time = float("inf")

        for instance in available_instances:
            response_times = self.instance_response_times[instance]
            if response_times:
                avg_response_time = sum(response_times) / len(response_times)
                if avg_response_time < best_response_time:
                    best_response_time = avg_response_time
                    best_instance = instance

        # Record distribution
        self._record_distribution(best_instance, "least_response_time")

        return best_instance

    def _consistent_hash_distribution(
        self, request_data: Dict[str, Any], available_instances: List[str]
    ) -> str:
        """Consistent hash load distribution"""
        if not available_instances:
            return "no_instances"

        # Create consistent hash key from request data
        request_key = str(sorted(request_data.items()))
        hash_value = int(hashlib.md5(request_key.encode()).hexdigest(), 16)

        # Select instance using consistent hashing
        instance_index = hash_value % len(available_instances)
        instance = available_instances[instance_index]

        # Record distribution
        self._record_distribution(instance, "consistent_hash")

        return instance

    def _fallback_distribution(self, available_instances: List[str]) -> str:
        """Fallback distribution method"""
        if not available_instances:
            return "no_instances"

        instance = available_instances[0]
        self._record_distribution(instance, "fallback")
        return instance

    def _record_distribution(self, instance: str, strategy: str):
        """Record distribution decision"""
        distribution_record = {
            "timestamp": time.time(),
            "instance": instance,
            "strategy": strategy,
            "connections": self.instance_connections[instance],
        }

        self.distribution_history.append(distribution_record)

        # Keep only recent history
        if len(self.distribution_history) > 1000:
            self.distribution_history.pop(0)

    def update_instance_metrics(self, instance: str, response_time: float):
        """Update instance performance metrics"""
        self.instance_response_times[instance].append(response_time)

        # Keep only recent response times
        if len(self.instance_response_times[instance]) > 100:
            self.instance_response_times[instance].pop(0)

    def set_instance_weight(self, instance: str, weight: float):
        """Set custom weight for an instance"""
        self.instance_weights[instance] = max(0.0, weight)
        self.logger.info(f"Set weight for {instance}: {weight}")

    def get_distribution_stats(self) -> Dict[str, Any]:
        """Get load distribution statistics"""
        total_distributions = len(self.distribution_history)
        if total_distributions == 0:
            return {"error": "No distribution history"}

        # Calculate strategy usage
        strategy_counts = defaultdict(int)
        for record in self.distribution_history:
            strategy_counts[record["strategy"]] += 1

        # Calculate average response times
        avg_response_times = {}
        for instance, response_times in self.instance_response_times.items():
            if response_times:
                avg_response_times[instance] = sum(response_times) / len(response_times)

        return {
            "total_distributions": total_distributions,
            "strategy_usage": dict(strategy_counts),
            "instance_connections": dict(self.instance_connections),
            "average_response_times": avg_response_times,
            "instance_weights": dict(self.instance_weights),
        }

    def reset_metrics(self):
        """Reset all distribution metrics"""
        self.instance_connections.clear()
        self.instance_response_times.clear()
        self.distribution_history.clear()
        self.current_instance_index = 0
        self._initialize_default_weights()
        self.logger.info("Distribution metrics reset")
