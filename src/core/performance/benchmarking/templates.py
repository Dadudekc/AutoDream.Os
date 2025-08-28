"""Templates for benchmark metric generation."""
from __future__ import annotations

import random
import time
from typing import Dict, Any, Callable

from .benchmark_types import BenchmarkType


# Individual benchmark templates --------------------------------------------

def cpu_template(duration: int, **_: Any) -> Dict[str, Any]:
    time.sleep(duration)
    return {
        "cpu_usage_avg": random.uniform(60.0, 95.0),
        "cpu_usage_peak": random.uniform(80.0, 100.0),
        "cpu_cores_utilized": random.randint(2, 8),
        "cpu_temperature": random.uniform(45.0, 75.0),
        "instructions_per_second": random.uniform(1_000_000, 5_000_000),
    }


def memory_template(duration: int, **_: Any) -> Dict[str, Any]:
    time.sleep(duration)
    return {
        "memory_usage_avg": random.uniform(40.0, 80.0),
        "memory_usage_peak": random.uniform(70.0, 95.0),
        "memory_allocated_mb": random.uniform(512, 2048),
        "memory_fragmentation": random.uniform(5.0, 25.0),
        "garbage_collection_time": random.uniform(10.0, 100.0),
    }


def disk_template(duration: int, **_: Any) -> Dict[str, Any]:
    time.sleep(duration)
    return {
        "read_speed_mbps": random.uniform(50.0, 500.0),
        "write_speed_mbps": random.uniform(30.0, 300.0),
        "iops_read": random.uniform(1_000, 10_000),
        "iops_write": random.uniform(500, 5_000),
        "latency_ms": random.uniform(1.0, 20.0),
    }


def network_template(duration: int, **_: Any) -> Dict[str, Any]:
    time.sleep(duration)
    return {
        "bandwidth_mbps": random.uniform(100.0, 1000.0),
        "latency_ms": random.uniform(5.0, 50.0),
        "packet_loss_percent": random.uniform(0.0, 5.0),
        "connections_active": random.randint(10, 100),
        "throughput_mbps": random.uniform(80.0, 900.0),
    }


def response_time_template(duration: int, **_: Any) -> Dict[str, Any]:
    time.sleep(duration)
    return {
        "response_time_avg_ms": random.uniform(50.0, 300.0),
        "response_time_p95_ms": random.uniform(100.0, 500.0),
        "response_time_p99_ms": random.uniform(200.0, 800.0),
        "response_time_min_ms": random.uniform(10.0, 100.0),
        "response_time_max_ms": random.uniform(400.0, 1000.0),
    }


def throughput_template(duration: int, **_: Any) -> Dict[str, Any]:
    time.sleep(duration)
    return {
        "throughput_ops_per_sec": random.uniform(100.0, 2000.0),
        "throughput_requests_per_sec": random.uniform(50.0, 1000.0),
        "throughput_data_mbps": random.uniform(10.0, 100.0),
        "concurrent_users": random.randint(10, 100),
        "efficiency_percent": random.uniform(70.0, 95.0),
    }


def concurrency_template(duration: int, **_: Any) -> Dict[str, Any]:
    time.sleep(duration)
    return {
        "max_concurrent_users": random.randint(50, 500),
        "concurrent_connections": random.randint(20, 200),
        "thread_utilization": random.uniform(60.0, 90.0),
        "context_switches": random.uniform(1_000, 10_000),
        "deadlock_detected": random.choice([True, False]),
    }


def generic_template(duration: int, **_: Any) -> Dict[str, Any]:
    time.sleep(duration)
    return {
        "execution_time_ms": random.uniform(100.0, 1000.0),
        "resource_usage_percent": random.uniform(30.0, 80.0),
        "success_rate_percent": random.uniform(85.0, 99.9),
        "error_count": random.randint(0, 10),
        "performance_score": random.uniform(0.5, 1.0),
    }


# Mapping of benchmark types to templates
TEMPLATES: Dict[BenchmarkType, Callable[..., Dict[str, Any]]] = {
    BenchmarkType.CPU: cpu_template,
    BenchmarkType.MEMORY: memory_template,
    BenchmarkType.DISK: disk_template,
    BenchmarkType.NETWORK: network_template,
    BenchmarkType.RESPONSE_TIME: response_time_template,
    BenchmarkType.THROUGHPUT: throughput_template,
    BenchmarkType.CONCURRENCY: concurrency_template,
    BenchmarkType.GENERIC: generic_template,
}

__all__ = ["TEMPLATES"]
