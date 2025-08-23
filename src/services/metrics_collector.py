"""
Metrics Collector for Agent_Cellphone_V2_Repository
Various metrics collectors for system, application, and custom metrics.
"""

import asyncio
import logging
import time
import psutil
import platform
from typing import List, Dict, Any, Callable, Optional
from abc import ABC, abstractmethod

# Import from our performance monitor
from .performance_monitor import MetricsCollector, MetricData, MetricType

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SystemMetricsCollector(MetricsCollector):
    """Collector for system-level metrics (CPU, memory, disk, network)."""

    def __init__(self, collection_interval: int = 60):
        super().__init__(collection_interval)
        self.collect_cpu = True
        self.collect_memory = True
        self.collect_disk = True
        self.collect_network = True
        self.hostname = platform.node()

        logger.info("System metrics collector initialized")

    async def collect_metrics(self) -> List[MetricData]:
        """Collect system metrics."""
        metrics = []
        current_time = time.time()
        base_tags = {"host": self.hostname, "collector": "system"}

        try:
            # CPU metrics
            if self.collect_cpu:
                cpu_percent = psutil.cpu_percent(interval=1)
                metrics.append(
                    MetricData(
                        metric_name="cpu_usage_percent",
                        metric_type=MetricType.GAUGE,
                        value=cpu_percent,
                        timestamp=current_time,
                        tags=base_tags.copy(),
                        unit="percent",
                        description="CPU usage percentage",
                    )
                )

                # Per-CPU metrics
                cpu_percents = psutil.cpu_percent(interval=1, percpu=True)
                for i, cpu_pct in enumerate(cpu_percents):
                    cpu_tags = base_tags.copy()
                    cpu_tags["cpu"] = str(i)
                    metrics.append(
                        MetricData(
                            metric_name="cpu_usage_percent_per_core",
                            metric_type=MetricType.GAUGE,
                            value=cpu_pct,
                            timestamp=current_time,
                            tags=cpu_tags,
                            unit="percent",
                            description=f"CPU usage percentage for core {i}",
                        )
                    )

                # Load average (Unix-like systems)
                try:
                    load_avg = psutil.getloadavg()
                    for i, period in enumerate(["1min", "5min", "15min"]):
                        load_tags = base_tags.copy()
                        load_tags["period"] = period
                        metrics.append(
                            MetricData(
                                metric_name="load_average",
                                metric_type=MetricType.GAUGE,
                                value=load_avg[i],
                                timestamp=current_time,
                                tags=load_tags,
                                unit="count",
                                description=f"Load average for {period}",
                            )
                        )
                except (AttributeError, OSError):
                    # getloadavg not available on Windows
                    pass

            # Memory metrics
            if self.collect_memory:
                memory = psutil.virtual_memory()
                metrics.extend(
                    [
                        MetricData(
                            metric_name="memory_usage_percent",
                            metric_type=MetricType.GAUGE,
                            value=memory.percent,
                            timestamp=current_time,
                            tags=base_tags.copy(),
                            unit="percent",
                            description="Memory usage percentage",
                        ),
                        MetricData(
                            metric_name="memory_total_bytes",
                            metric_type=MetricType.GAUGE,
                            value=memory.total,
                            timestamp=current_time,
                            tags=base_tags.copy(),
                            unit="bytes",
                            description="Total memory in bytes",
                        ),
                        MetricData(
                            metric_name="memory_available_bytes",
                            metric_type=MetricType.GAUGE,
                            value=memory.available,
                            timestamp=current_time,
                            tags=base_tags.copy(),
                            unit="bytes",
                            description="Available memory in bytes",
                        ),
                        MetricData(
                            metric_name="memory_used_bytes",
                            metric_type=MetricType.GAUGE,
                            value=memory.used,
                            timestamp=current_time,
                            tags=base_tags.copy(),
                            unit="bytes",
                            description="Used memory in bytes",
                        ),
                    ]
                )

                # Swap metrics
                swap = psutil.swap_memory()
                metrics.extend(
                    [
                        MetricData(
                            metric_name="swap_usage_percent",
                            metric_type=MetricType.GAUGE,
                            value=swap.percent,
                            timestamp=current_time,
                            tags=base_tags.copy(),
                            unit="percent",
                            description="Swap usage percentage",
                        ),
                        MetricData(
                            metric_name="swap_total_bytes",
                            metric_type=MetricType.GAUGE,
                            value=swap.total,
                            timestamp=current_time,
                            tags=base_tags.copy(),
                            unit="bytes",
                            description="Total swap in bytes",
                        ),
                        MetricData(
                            metric_name="swap_used_bytes",
                            metric_type=MetricType.GAUGE,
                            value=swap.used,
                            timestamp=current_time,
                            tags=base_tags.copy(),
                            unit="bytes",
                            description="Used swap in bytes",
                        ),
                    ]
                )

            # Disk metrics
            if self.collect_disk:
                disk_partitions = psutil.disk_partitions()
                for partition in disk_partitions:
                    try:
                        disk_usage = psutil.disk_usage(partition.mountpoint)
                        disk_tags = base_tags.copy()
                        disk_tags["device"] = partition.device
                        disk_tags["mountpoint"] = partition.mountpoint
                        disk_tags["fstype"] = partition.fstype

                        metrics.extend(
                            [
                                MetricData(
                                    metric_name="disk_usage_percent",
                                    metric_type=MetricType.GAUGE,
                                    value=disk_usage.percent,
                                    timestamp=current_time,
                                    tags=disk_tags.copy(),
                                    unit="percent",
                                    description="Disk usage percentage",
                                ),
                                MetricData(
                                    metric_name="disk_total_bytes",
                                    metric_type=MetricType.GAUGE,
                                    value=disk_usage.total,
                                    timestamp=current_time,
                                    tags=disk_tags.copy(),
                                    unit="bytes",
                                    description="Total disk space in bytes",
                                ),
                                MetricData(
                                    metric_name="disk_used_bytes",
                                    metric_type=MetricType.GAUGE,
                                    value=disk_usage.used,
                                    timestamp=current_time,
                                    tags=disk_tags.copy(),
                                    unit="bytes",
                                    description="Used disk space in bytes",
                                ),
                                MetricData(
                                    metric_name="disk_free_bytes",
                                    metric_type=MetricType.GAUGE,
                                    value=disk_usage.free,
                                    timestamp=current_time,
                                    tags=disk_tags.copy(),
                                    unit="bytes",
                                    description="Free disk space in bytes",
                                ),
                            ]
                        )
                    except PermissionError:
                        # Skip partitions we can't access
                        continue

                # Disk I/O metrics
                try:
                    disk_io = psutil.disk_io_counters()
                    if disk_io:
                        metrics.extend(
                            [
                                MetricData(
                                    metric_name="disk_read_bytes_total",
                                    metric_type=MetricType.COUNTER,
                                    value=disk_io.read_bytes,
                                    timestamp=current_time,
                                    tags=base_tags.copy(),
                                    unit="bytes",
                                    description="Total bytes read from disk",
                                ),
                                MetricData(
                                    metric_name="disk_write_bytes_total",
                                    metric_type=MetricType.COUNTER,
                                    value=disk_io.write_bytes,
                                    timestamp=current_time,
                                    tags=base_tags.copy(),
                                    unit="bytes",
                                    description="Total bytes written to disk",
                                ),
                                MetricData(
                                    metric_name="disk_read_count_total",
                                    metric_type=MetricType.COUNTER,
                                    value=disk_io.read_count,
                                    timestamp=current_time,
                                    tags=base_tags.copy(),
                                    unit="count",
                                    description="Total disk read operations",
                                ),
                                MetricData(
                                    metric_name="disk_write_count_total",
                                    metric_type=MetricType.COUNTER,
                                    value=disk_io.write_count,
                                    timestamp=current_time,
                                    tags=base_tags.copy(),
                                    unit="count",
                                    description="Total disk write operations",
                                ),
                            ]
                        )
                except AttributeError:
                    # disk_io_counters not available on all platforms
                    pass

            # Network metrics
            if self.collect_network:
                try:
                    net_io = psutil.net_io_counters()
                    if net_io:
                        metrics.extend(
                            [
                                MetricData(
                                    metric_name="network_bytes_sent_total",
                                    metric_type=MetricType.COUNTER,
                                    value=net_io.bytes_sent,
                                    timestamp=current_time,
                                    tags=base_tags.copy(),
                                    unit="bytes",
                                    description="Total bytes sent over network",
                                ),
                                MetricData(
                                    metric_name="network_bytes_recv_total",
                                    metric_type=MetricType.COUNTER,
                                    value=net_io.bytes_recv,
                                    timestamp=current_time,
                                    tags=base_tags.copy(),
                                    unit="bytes",
                                    description="Total bytes received over network",
                                ),
                                MetricData(
                                    metric_name="network_packets_sent_total",
                                    metric_type=MetricType.COUNTER,
                                    value=net_io.packets_sent,
                                    timestamp=current_time,
                                    tags=base_tags.copy(),
                                    unit="count",
                                    description="Total packets sent over network",
                                ),
                                MetricData(
                                    metric_name="network_packets_recv_total",
                                    metric_type=MetricType.COUNTER,
                                    value=net_io.packets_recv,
                                    timestamp=current_time,
                                    tags=base_tags.copy(),
                                    unit="count",
                                    description="Total packets received over network",
                                ),
                            ]
                        )

                        # Error counters
                        if hasattr(net_io, "errin") and hasattr(net_io, "errout"):
                            metrics.extend(
                                [
                                    MetricData(
                                        metric_name="network_errors_in_total",
                                        metric_type=MetricType.COUNTER,
                                        value=net_io.errin,
                                        timestamp=current_time,
                                        tags=base_tags.copy(),
                                        unit="count",
                                        description="Total network input errors",
                                    ),
                                    MetricData(
                                        metric_name="network_errors_out_total",
                                        metric_type=MetricType.COUNTER,
                                        value=net_io.errout,
                                        timestamp=current_time,
                                        tags=base_tags.copy(),
                                        unit="count",
                                        description="Total network output errors",
                                    ),
                                ]
                            )
                except AttributeError:
                    # net_io_counters not available on all platforms
                    pass

        except Exception as e:
            logger.error(f"Error collecting system metrics: {e}")

        logger.debug(f"Collected {len(metrics)} system metrics")
        return metrics


class ApplicationMetricsCollector(MetricsCollector):
    """Collector for application-level metrics."""

    def __init__(self, collection_interval: int = 60):
        super().__init__(collection_interval)
        self.process = psutil.Process()
        self.app_name = "agent_cellphone_v2"

        # Request tracking
        self.request_count = 0
        self.response_times: List[float] = []
        self.error_count = 0

        logger.info("Application metrics collector initialized")

    async def collect_metrics(self) -> List[MetricData]:
        """Collect application metrics."""
        metrics = []
        current_time = time.time()
        base_tags = {"app": self.app_name, "collector": "application"}

        try:
            # Process metrics
            with self.process.oneshot():
                # CPU usage
                cpu_percent = self.process.cpu_percent()
                metrics.append(
                    MetricData(
                        metric_name="app_cpu_usage_percent",
                        metric_type=MetricType.GAUGE,
                        value=cpu_percent,
                        timestamp=current_time,
                        tags=base_tags.copy(),
                        unit="percent",
                        description="Application CPU usage percentage",
                    )
                )

                # Memory usage
                memory_info = self.process.memory_info()
                metrics.extend(
                    [
                        MetricData(
                            metric_name="app_memory_rss_bytes",
                            metric_type=MetricType.GAUGE,
                            value=memory_info.rss,
                            timestamp=current_time,
                            tags=base_tags.copy(),
                            unit="bytes",
                            description="Application RSS memory usage",
                        ),
                        MetricData(
                            metric_name="app_memory_vms_bytes",
                            metric_type=MetricType.GAUGE,
                            value=memory_info.vms,
                            timestamp=current_time,
                            tags=base_tags.copy(),
                            unit="bytes",
                            description="Application VMS memory usage",
                        ),
                    ]
                )

                # File descriptors (Unix-like systems)
                try:
                    num_fds = self.process.num_fds()
                    metrics.append(
                        MetricData(
                            metric_name="app_file_descriptors",
                            metric_type=MetricType.GAUGE,
                            value=num_fds,
                            timestamp=current_time,
                            tags=base_tags.copy(),
                            unit="count",
                            description="Number of open file descriptors",
                        )
                    )
                except (AttributeError, psutil.AccessDenied):
                    # num_fds not available on Windows or access denied
                    pass

                # Thread count
                num_threads = self.process.num_threads()
                metrics.append(
                    MetricData(
                        metric_name="app_threads",
                        metric_type=MetricType.GAUGE,
                        value=num_threads,
                        timestamp=current_time,
                        tags=base_tags.copy(),
                        unit="count",
                        description="Number of application threads",
                    )
                )

            # Request metrics
            metrics.extend(
                [
                    MetricData(
                        metric_name="app_requests_total",
                        metric_type=MetricType.COUNTER,
                        value=self.request_count,
                        timestamp=current_time,
                        tags=base_tags.copy(),
                        unit="count",
                        description="Total number of requests processed",
                    ),
                    MetricData(
                        metric_name="app_errors_total",
                        metric_type=MetricType.COUNTER,
                        value=self.error_count,
                        timestamp=current_time,
                        tags=base_tags.copy(),
                        unit="count",
                        description="Total number of errors",
                    ),
                ]
            )

            # Response time metrics
            if self.response_times:
                avg_response_time = sum(self.response_times) / len(self.response_times)
                max_response_time = max(self.response_times)
                min_response_time = min(self.response_times)

                metrics.extend(
                    [
                        MetricData(
                            metric_name="app_response_time_avg_seconds",
                            metric_type=MetricType.GAUGE,
                            value=avg_response_time,
                            timestamp=current_time,
                            tags=base_tags.copy(),
                            unit="seconds",
                            description="Average response time",
                        ),
                        MetricData(
                            metric_name="app_response_time_max_seconds",
                            metric_type=MetricType.GAUGE,
                            value=max_response_time,
                            timestamp=current_time,
                            tags=base_tags.copy(),
                            unit="seconds",
                            description="Maximum response time",
                        ),
                        MetricData(
                            metric_name="app_response_time_min_seconds",
                            metric_type=MetricType.GAUGE,
                            value=min_response_time,
                            timestamp=current_time,
                            tags=base_tags.copy(),
                            unit="seconds",
                            description="Minimum response time",
                        ),
                    ]
                )

                # Clear response times after collection
                self.response_times.clear()

        except Exception as e:
            logger.error(f"Error collecting application metrics: {e}")

        logger.debug(f"Collected {len(metrics)} application metrics")
        return metrics

    def record_request(self, response_time: float, error: bool = False):
        """Record a request for metrics collection."""
        self.request_count += 1
        self.response_times.append(response_time)
        if error:
            self.error_count += 1


class NetworkMetricsCollector(MetricsCollector):
    """Collector for network-specific metrics."""

    def __init__(self, collection_interval: int = 60):
        super().__init__(collection_interval)
        self.monitored_ports: List[int] = []

        logger.info("Network metrics collector initialized")

    async def collect_metrics(self) -> List[MetricData]:
        """Collect network metrics."""
        metrics = []
        current_time = time.time()
        base_tags = {"collector": "network"}

        try:
            # Connection counts by state
            connections = psutil.net_connections()
            connection_states = {}

            for conn in connections:
                state = conn.status
                connection_states[state] = connection_states.get(state, 0) + 1

            for state, count in connection_states.items():
                state_tags = base_tags.copy()
                state_tags["state"] = state
                metrics.append(
                    MetricData(
                        metric_name="network_connections",
                        metric_type=MetricType.GAUGE,
                        value=count,
                        timestamp=current_time,
                        tags=state_tags,
                        unit="count",
                        description=f"Number of network connections in {state} state",
                    )
                )

            # Per-interface metrics
            net_io_per_nic = psutil.net_io_counters(pernic=True)
            for interface, stats in net_io_per_nic.items():
                iface_tags = base_tags.copy()
                iface_tags["interface"] = interface

                metrics.extend(
                    [
                        MetricData(
                            metric_name="network_interface_bytes_sent_total",
                            metric_type=MetricType.COUNTER,
                            value=stats.bytes_sent,
                            timestamp=current_time,
                            tags=iface_tags.copy(),
                            unit="bytes",
                            description=f"Bytes sent on interface {interface}",
                        ),
                        MetricData(
                            metric_name="network_interface_bytes_recv_total",
                            metric_type=MetricType.COUNTER,
                            value=stats.bytes_recv,
                            timestamp=current_time,
                            tags=iface_tags.copy(),
                            unit="bytes",
                            description=f"Bytes received on interface {interface}",
                        ),
                        MetricData(
                            metric_name="network_interface_packets_sent_total",
                            metric_type=MetricType.COUNTER,
                            value=stats.packets_sent,
                            timestamp=current_time,
                            tags=iface_tags.copy(),
                            unit="count",
                            description=f"Packets sent on interface {interface}",
                        ),
                        MetricData(
                            metric_name="network_interface_packets_recv_total",
                            metric_type=MetricType.COUNTER,
                            value=stats.packets_recv,
                            timestamp=current_time,
                            tags=iface_tags.copy(),
                            unit="count",
                            description=f"Packets received on interface {interface}",
                        ),
                    ]
                )

        except Exception as e:
            logger.error(f"Error collecting network metrics: {e}")

        logger.debug(f"Collected {len(metrics)} network metrics")
        return metrics

    def add_monitored_port(self, port: int):
        """Add a port to monitor for connections."""
        if port not in self.monitored_ports:
            self.monitored_ports.append(port)
            logger.info(f"Added port {port} to network monitoring")


class CustomMetricsCollector(MetricsCollector):
    """Collector for custom application-specific metrics."""

    def __init__(self, collection_interval: int = 60):
        super().__init__(collection_interval)
        self.custom_metrics: Dict[str, Callable[[], Union[float, int]]] = {}

        logger.info("Custom metrics collector initialized")

    async def collect_metrics(self) -> List[MetricData]:
        """Collect custom metrics."""
        metrics = []
        current_time = time.time()
        base_tags = {"collector": "custom"}

        for metric_name, metric_func in self.custom_metrics.items():
            try:
                value = metric_func()
                metrics.append(
                    MetricData(
                        metric_name=metric_name,
                        metric_type=MetricType.GAUGE,
                        value=value,
                        timestamp=current_time,
                        tags=base_tags.copy(),
                        unit="",
                        description=f"Custom metric: {metric_name}",
                    )
                )
            except Exception as e:
                logger.error(f"Error collecting custom metric {metric_name}: {e}")

        logger.debug(f"Collected {len(metrics)} custom metrics")
        return metrics

    def add_custom_metric(self, name: str, func: Callable[[], Union[float, int]]):
        """Add a custom metric function."""
        self.custom_metrics[name] = func
        logger.info(f"Added custom metric: {name}")

    def remove_custom_metric(self, name: str):
        """Remove a custom metric."""
        if name in self.custom_metrics:
            del self.custom_metrics[name]
            logger.info(f"Removed custom metric: {name}")


# Export all classes
__all__ = [
    "SystemMetricsCollector",
    "ApplicationMetricsCollector",
    "NetworkMetricsCollector",
    "CustomMetricsCollector",
]
