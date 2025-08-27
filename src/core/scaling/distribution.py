"""Load distribution strategies for scaling manager."""

import hashlib
import logging
import time
from collections import defaultdict
from typing import Any, Dict, List

from .types import ScalingStrategy

logger = logging.getLogger(__name__)


class LoadDistributor:
    """Encapsulates load distribution algorithms."""

    def __init__(self) -> None:
        self.instance_connections = defaultdict(int)
        self.instance_response_times = defaultdict(list)
        self.instance_weights = defaultdict(float)
        self.current_instance_index = 0
        self.strategies = {
            ScalingStrategy.ROUND_ROBIN: self._round_robin,
            ScalingStrategy.LEAST_CONNECTIONS: self._least_connections,
            ScalingStrategy.WEIGHTED_ROUND_ROBIN: self._weighted_round_robin,
            ScalingStrategy.IP_HASH: self._ip_hash,
            ScalingStrategy.LEAST_RESPONSE_TIME: self._least_response_time,
            ScalingStrategy.CONSISTENT_HASH: self._consistent_hash,
        }
        self._setup_default_weights()

    def distribute(
        self, request_data: Dict[str, Any], strategy: ScalingStrategy, available: List[str]
    ) -> str:
        """Distribute load using the specified strategy."""
        if not available:
            return "no_instances_available"
        try:
            if strategy in self.strategies:
                return self.strategies[strategy](request_data, available)
            return self._fallback(available)
        except Exception as exc:  # pragma: no cover - defensive
            logger.error("Load distribution error: %s", exc)
            return available[0] if available else "error"

    # Strategy implementations -------------------------------------------------
    def _round_robin(self, request_data: Dict[str, Any], available: List[str]) -> str:
        if not available:
            return "no_instances"
        instance = available[self.current_instance_index % len(available)]
        self.current_instance_index += 1
        self._record(instance, "round_robin")
        return instance

    def _least_connections(self, request_data: Dict[str, Any], available: List[str]) -> str:
        if not available:
            return "no_instances"
        instance = min(available, key=lambda x: self.instance_connections[x])
        self._record(instance, "least_connections")
        return instance

    def _weighted_round_robin(self, request_data: Dict[str, Any], available: List[str]) -> str:
        if not available:
            return "no_instances"
        total = sum(self.instance_weights.get(inst, 1.0) for inst in available)
        if total <= 0:
            return available[0]
        current = 0.0
        for inst in available:
            current += self.instance_weights.get(inst, 1.0)
            if current >= total / 2:
                self._record(inst, "weighted_round_robin")
                return inst
        return available[-1]

    def _ip_hash(self, request_data: Dict[str, Any], available: List[str]) -> str:
        if not available:
            return "no_instances"
        client_ip = request_data.get("client_ip", "unknown")
        hash_value = int(hashlib.md5(client_ip.encode()).hexdigest(), 16)
        inst = available[hash_value % len(available)]
        self._record(inst, "ip_hash")
        return inst

    def _least_response_time(self, request_data: Dict[str, Any], available: List[str]) -> str:
        if not available:
            return "no_instances"
        inst = min(available, key=lambda x: self._avg_response_time(x))
        self._record(inst, "least_response_time")
        return inst

    def _consistent_hash(self, request_data: Dict[str, Any], available: List[str]) -> str:
        if not available:
            return "no_instances"
        key = str(request_data.get("request_id", time.time()))
        hash_value = int(hashlib.md5(key.encode()).hexdigest(), 16)
        inst = available[hash_value % len(available)]
        self._record(inst, "consistent_hash")
        return inst

    def _fallback(self, available: List[str]) -> str:
        return available[0] if available else "no_instances"

    # Helpers ------------------------------------------------------------------
    def _record(self, instance: str, strategy: str) -> None:
        self.instance_connections[instance] += 1
        # Placeholder for metrics collection

    def _avg_response_time(self, instance: str) -> float:
        times = self.instance_response_times.get(instance, [])
        return sum(times) / len(times) if times else 100.0

    def _setup_default_weights(self) -> None:
        for i in range(10):
            self.instance_weights[f"instance_{i}"] = 1.0
