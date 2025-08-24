"""
Agent Health Metrics Collection Module

Single Responsibility: Collect and process health metrics from various sources.
Follows V2 coding standards: Clean OOP design, SRP compliance, TDD approach.
"""

import asyncio
import json
import logging
import os
import psutil
import time
import threading
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Set, Callable, Any, Union
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MetricSource(Enum):
    """Sources of health metrics"""
    SYSTEM = "system"  # OS-level metrics
    PROCESS = "process"  # Process-level metrics
    APPLICATION = "application"  # Application-specific metrics
    NETWORK = "network"  # Network metrics
    CUSTOM = "custom"  # Custom metrics


class MetricCollectionMethod(Enum):
    """Methods for collecting metrics"""
    POLLING = "polling"  # Regular interval polling
    EVENT_DRIVEN = "event_driven"  # Event-based collection
    ON_DEMAND = "on_demand"  # Collection when requested
    CONTINUOUS = "continuous"  # Continuous monitoring


@dataclass
class MetricCollectionConfig:
    """Configuration for metric collection"""
    source: MetricSource
    method: MetricCollectionMethod
    interval: float  # seconds
    enabled: bool = True
    timeout: float = 30.0  # seconds
    retry_attempts: int = 3
    custom_parameters: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CollectedMetric:
    """Raw collected metric data"""
    source: MetricSource
    metric_name: str
    value: Union[float, int, str, bool]
    unit: str
    timestamp: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)
    quality_score: float = 1.0  # 0.0 to 1.0
    collection_latency: float = 0.0  # milliseconds


@dataclass
class MetricCollectionResult:
    """Result of a metric collection operation"""
    success: bool
    metrics: List[CollectedMetric]
    collection_time: datetime
    duration: float  # milliseconds
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


class HealthMetricsCollector:
    """
    Health metrics collection and processing
    
    Single Responsibility: Collect health metrics from various sources
    including system, process, and application metrics.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """Initialize the metrics collector"""
        self.config = config or {}
        self.collection_active = False
        self.collectors: Dict[MetricSource, Callable] = {}
        self.collection_configs: Dict[str, MetricCollectionConfig] = {}
        self.collection_thread: Optional[threading.Thread] = None
        self.executor = ThreadPoolExecutor(max_workers=8)
        self.metric_callbacks: Set[Callable] = set()
        self.collection_history: List[MetricCollectionResult] = []
        
        # Initialize default collectors
        self._initialize_default_collectors()
        self._initialize_default_configs()
        
        # Collection intervals
        self.system_metrics_interval = self.config.get("system_metrics_interval", 30)
        self.process_metrics_interval = self.config.get("process_metrics_interval", 15)
        self.application_metrics_interval = self.config.get("application_metrics_interval", 60)
        
        logger.info("HealthMetricsCollector initialized with default collectors")

    def _initialize_default_collectors(self):
        """Initialize default metric collectors"""
        self.collectors[MetricSource.SYSTEM] = self._collect_system_metrics
        self.collectors[MetricSource.PROCESS] = self._collect_process_metrics
        self.collectors[MetricSource.APPLICATION] = self._collect_application_metrics
        self.collectors[MetricSource.NETWORK] = self._collect_network_metrics

    def _initialize_default_configs(self):
        """Initialize default collection configurations"""
        default_configs = [
            MetricCollectionConfig(
                source=MetricSource.SYSTEM,
                method=MetricCollectionMethod.POLLING,
                interval=30.0,
                enabled=True,
                timeout=10.0,
                retry_attempts=2,
            ),
            MetricCollectionConfig(
                source=MetricSource.PROCESS,
                method=MetricCollectionMethod.POLLING,
                interval=15.0,
                enabled=True,
                timeout=5.0,
                retry_attempts=2,
            ),
            MetricCollectionConfig(
                source=MetricSource.APPLICATION,
                method=MetricCollectionMethod.POLLING,
                interval=60.0,
                enabled=True,
                timeout=15.0,
                retry_attempts=3,
            ),
            MetricCollectionConfig(
                source=MetricSource.NETWORK,
                method=MetricCollectionMethod.POLLING,
                interval=45.0,
                enabled=True,
                timeout=10.0,
                retry_attempts=2,
            ),
        ]

        for config in default_configs:
            self.collection_configs[config.source.value] = config

    def start(self):
        """Start metric collection"""
        if self.collection_active:
            logger.warning("Metric collection already active")
            return

        self.collection_active = True
        self.collection_thread = threading.Thread(target=self._collection_loop, daemon=True)
        self.collection_thread.start()
        logger.info("Health metrics collection started")

    def stop(self):
        """Stop metric collection"""
        self.collection_active = False
        if self.collection_thread:
            self.collection_thread.join(timeout=5)
        self.executor.shutdown(wait=True)
        logger.info("Health metrics collection stopped")

    def _collection_loop(self):
        """Main collection loop"""
        while self.collection_active:
            try:
                # Collect metrics from all enabled sources
                for source, config in self.collection_configs.items():
                    if config.enabled and self._should_collect(config):
                        self._schedule_collection(source, config)

                time.sleep(1)  # Check every second

            except Exception as e:
                logger.error(f"Error in collection loop: {e}")
                time.sleep(10)  # Wait before retrying

    def _should_collect(self, config: MetricCollectionConfig) -> bool:
        """Check if it's time to collect metrics for a source"""
        # For now, use simple time-based collection
        # In a real implementation, this could be more sophisticated
        return True

    def _schedule_collection(self, source: str, config: MetricCollectionConfig):
        """Schedule metric collection for a source"""
        try:
            if config.method == MetricCollectionMethod.POLLING:
                # Submit to thread pool for async execution
                future = self.executor.submit(self._execute_collection, source, config)
                future.add_done_callback(lambda f: self._handle_collection_result(f, source))

        except Exception as e:
            logger.error(f"Error scheduling collection for {source}: {e}")

    def _execute_collection(self, source: str, config: MetricCollectionConfig) -> MetricCollectionResult:
        """Execute metric collection for a source"""
        start_time = time.time()
        collection_time = datetime.now()
        metrics = []
        errors = []
        warnings = []

        try:
            # Get the appropriate collector function
            collector_func = self.collectors.get(MetricSource(source))
            if not collector_func:
                errors.append(f"No collector found for source: {source}")
                return MetricCollectionResult(
                    success=False,
                    metrics=[],
                    collection_time=collection_time,
                    duration=(time.time() - start_time) * 1000,
                    errors=errors,
                    warnings=warnings,
                )

            # Execute collection with timeout
            if config.timeout > 0:
                # Use asyncio for timeout handling
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    result = asyncio.wait_for(
                        loop.run_in_executor(None, collector_func),
                        timeout=config.timeout
                    )
                    metrics = result
                except asyncio.TimeoutError:
                    errors.append(f"Collection timeout for {source}")
                finally:
                    loop.close()
            else:
                metrics = collector_func()

            # Validate collected metrics
            validated_metrics = self._validate_metrics(metrics, source)
            metrics = validated_metrics

            duration = (time.time() - start_time) * 1000

            result = MetricCollectionResult(
                success=len(errors) == 0,
                metrics=metrics,
                collection_time=collection_time,
                duration=duration,
                errors=errors,
                warnings=warnings,
            )

            # Store in history
            self.collection_history.append(result)

            # Notify subscribers
            self._notify_metric_updates(source, metrics)

            return result

        except Exception as e:
            errors.append(f"Collection error for {source}: {str(e)}")
            duration = (time.time() - start_time) * 1000
            
            result = MetricCollectionResult(
                success=False,
                metrics=[],
                collection_time=collection_time,
                duration=duration,
                errors=errors,
                warnings=warnings,
            )

            self.collection_history.append(result)
            return result

    def _handle_collection_result(self, future, source: str):
        """Handle the result of a collection operation"""
        try:
            result = future.result()
            if result.success:
                logger.debug(f"Collection completed for {source}: {len(result.metrics)} metrics")
            else:
                logger.warning(f"Collection failed for {source}: {result.errors}")
        except Exception as e:
            logger.error(f"Error handling collection result for {source}: {e}")

    def _collect_system_metrics(self) -> List[CollectedMetric]:
        """Collect system-level health metrics"""
        metrics = []
        start_time = time.time()

        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            metrics.append(CollectedMetric(
                source=MetricSource.SYSTEM,
                metric_name="cpu_usage",
                value=cpu_percent,
                unit="%",
                timestamp=datetime.now(),
                metadata={"cores": psutil.cpu_count()},
                collection_latency=(time.time() - start_time) * 1000,
            ))

            # Memory usage
            memory = psutil.virtual_memory()
            metrics.append(CollectedMetric(
                source=MetricSource.SYSTEM,
                metric_name="memory_usage",
                value=memory.percent,
                unit="%",
                timestamp=datetime.now(),
                metadata={
                    "total_gb": round(memory.total / (1024**3), 2),
                    "available_gb": round(memory.available / (1024**3), 2),
                },
                collection_latency=(time.time() - start_time) * 1000,
            ))

            # Disk usage
            disk = psutil.disk_usage('/')
            metrics.append(CollectedMetric(
                source=MetricSource.SYSTEM,
                metric_name="disk_usage",
                value=disk.percent,
                unit="%",
                timestamp=datetime.now(),
                metadata={
                    "total_gb": round(disk.total / (1024**3), 2),
                    "free_gb": round(disk.free / (1024**3), 2),
                },
                collection_latency=(time.time() - start_time) * 1000,
            ))

            # Network I/O
            network = psutil.net_io_counters()
            metrics.append(CollectedMetric(
                source=MetricSource.SYSTEM,
                metric_name="network_bytes_sent",
                value=network.bytes_sent,
                unit="bytes",
                timestamp=datetime.now(),
                metadata={"interface": "total"},
                collection_latency=(time.time() - start_time) * 1000,
            ))

            metrics.append(CollectedMetric(
                source=MetricSource.SYSTEM,
                metric_name="network_bytes_recv",
                value=network.bytes_recv,
                unit="bytes",
                timestamp=datetime.now(),
                metadata={"interface": "total"},
                collection_latency=(time.time() - start_time) * 1000,
            ))

        except Exception as e:
            logger.error(f"Error collecting system metrics: {e}")

        return metrics

    def _collect_process_metrics(self) -> List[CollectedMetric]:
        """Collect process-level health metrics"""
        metrics = []
        start_time = time.time()

        try:
            current_process = psutil.Process()

            # Process CPU usage
            cpu_percent = current_process.cpu_percent()
            metrics.append(CollectedMetric(
                source=MetricSource.PROCESS,
                metric_name="process_cpu_usage",
                value=cpu_percent,
                unit="%",
                timestamp=datetime.now(),
                metadata={"pid": current_process.pid},
                collection_latency=(time.time() - start_time) * 1000,
            ))

            # Process memory usage
            memory_info = current_process.memory_info()
            memory_percent = current_process.memory_percent()
            metrics.append(CollectedMetric(
                source=MetricSource.PROCESS,
                metric_name="process_memory_usage",
                value=memory_percent,
                unit="%",
                timestamp=datetime.now(),
                metadata={
                    "rss_mb": round(memory_info.rss / (1024**2), 2),
                    "vms_mb": round(memory_info.vms / (1024**2), 2),
                },
                collection_latency=(time.time() - start_time) * 1000,
            ))

            # Process threads
            num_threads = current_process.num_threads()
            metrics.append(CollectedMetric(
                source=MetricSource.PROCESS,
                metric_name="process_threads",
                value=num_threads,
                unit="count",
                timestamp=datetime.now(),
                metadata={"pid": current_process.pid},
                collection_latency=(time.time() - start_time) * 1000,
            ))

            # Process file descriptors (Unix-like systems)
            try:
                num_fds = current_process.num_fds()
                metrics.append(CollectedMetric(
                    source=MetricSource.PROCESS,
                    metric_name="process_file_descriptors",
                    value=num_fds,
                    unit="count",
                    timestamp=datetime.now(),
                    metadata={"pid": current_process.pid},
                    collection_latency=(time.time() - start_time) * 1000,
                ))
            except (AttributeError, psutil.AccessDenied):
                # Windows doesn't have num_fds
                pass

        except Exception as e:
            logger.error(f"Error collecting process metrics: {e}")

        return metrics

    def _collect_application_metrics(self) -> List[CollectedMetric]:
        """Collect application-specific health metrics"""
        metrics = []
        start_time = time.time()

        try:
            # Application uptime
            uptime = time.time() - self._get_start_time()
            metrics.append(CollectedMetric(
                source=MetricSource.APPLICATION,
                metric_name="application_uptime",
                value=uptime,
                unit="seconds",
                timestamp=datetime.now(),
                metadata={"start_time": self._get_start_time()},
                collection_latency=(time.time() - start_time) * 1000,
            ))

            # Python version and environment
            import sys
            metrics.append(CollectedMetric(
                source=MetricSource.APPLICATION,
                metric_name="python_version",
                value=sys.version,
                unit="version",
                timestamp=datetime.now(),
                metadata={"platform": sys.platform},
                collection_latency=(time.time() - start_time) * 1000,
            ))

            # Working directory
            import os
            metrics.append(CollectedMetric(
                source=MetricSource.APPLICATION,
                metric_name="working_directory",
                value=os.getcwd(),
                unit="path",
                timestamp=datetime.now(),
                metadata={"exists": os.path.exists(os.getcwd())},
                collection_latency=(time.time() - start_time) * 1000,
            ))

            # Environment variables count
            env_count = len(os.environ)
            metrics.append(CollectedMetric(
                source=MetricSource.APPLICATION,
                metric_name="environment_variables",
                value=env_count,
                unit="count",
                timestamp=datetime.now(),
                metadata={},
                collection_latency=(time.time() - start_time) * 1000,
            ))

        except Exception as e:
            logger.error(f"Error collecting application metrics: {e}")

        return metrics

    def _collect_network_metrics(self) -> List[CollectedMetric]:
        """Collect network-related health metrics"""
        metrics = []
        start_time = time.time()

        try:
            # Network connections
            connections = psutil.net_connections()
            active_connections = len([c for c in connections if c.status == 'ESTABLISHED'])
            
            metrics.append(CollectedMetric(
                source=MetricSource.NETWORK,
                metric_name="active_connections",
                value=active_connections,
                unit="count",
                timestamp=datetime.now(),
                metadata={"total_connections": len(connections)},
                collection_latency=(time.time() - start_time) * 1000,
            ))

            # Network interfaces
            interfaces = psutil.net_if_addrs()
            interface_count = len(interfaces)
            
            metrics.append(CollectedMetric(
                source=MetricSource.NETWORK,
                metric_name="network_interfaces",
                value=interface_count,
                unit="count",
                timestamp=datetime.now(),
                metadata={"interface_names": list(interfaces.keys())},
                collection_latency=(time.time() - start_time) * 1000,
            ))

            # DNS resolution test
            try:
                import socket
                start_dns = time.time()
                socket.gethostbyname("localhost")
                dns_latency = (time.time() - start_dns) * 1000
                
                metrics.append(CollectedMetric(
                    source=MetricSource.NETWORK,
                    metric_name="dns_resolution_latency",
                    value=dns_latency,
                    unit="ms",
                    timestamp=datetime.now(),
                    metadata={"host": "localhost"},
                    collection_latency=(time.time() - start_time) * 1000,
                ))
            except Exception:
                # DNS resolution failed
                pass

        except Exception as e:
            logger.error(f"Error collecting network metrics: {e}")

        return metrics

    def _get_start_time(self) -> float:
        """Get application start time"""
        # In a real application, this would be stored when the app starts
        # For now, we'll use a default value
        return time.time() - 3600  # Assume 1 hour ago

    def _validate_metrics(self, metrics: List[CollectedMetric], source: str) -> List[CollectedMetric]:
        """Validate collected metrics for quality and consistency"""
        validated_metrics = []

        for metric in metrics:
            try:
                # Basic validation
                if metric.value is None:
                    logger.warning(f"Skipping metric with None value: {metric.metric_name}")
                    continue

                # Check for reasonable value ranges
                if self._is_value_reasonable(metric):
                    validated_metrics.append(metric)
                else:
                    logger.warning(f"Metric value out of reasonable range: {metric.metric_name} = {metric.value}")

            except Exception as e:
                logger.error(f"Error validating metric {metric.metric_name}: {e}")

        return validated_metrics

    def _is_value_reasonable(self, metric: CollectedMetric) -> bool:
        """Check if a metric value is within reasonable bounds"""
        try:
            if isinstance(metric.value, (int, float)):
                # CPU usage should be 0-100%
                if "cpu" in metric.metric_name.lower() and metric.unit == "%":
                    return 0 <= metric.value <= 100

                # Memory usage should be 0-100%
                if "memory" in metric.metric_name.lower() and metric.unit == "%":
                    return 0 <= metric.value <= 100

                # Disk usage should be 0-100%
                if "disk" in metric.metric_name.lower() and metric.unit == "%":
                    return 0 <= metric.value <= 100

                # Latency should be positive
                if "latency" in metric.metric_name.lower() or "time" in metric.metric_name.lower():
                    return metric.value >= 0

                # Counts should be non-negative
                if metric.unit in ["count", "bytes"]:
                    return metric.value >= 0

            return True  # Default to accepting the value

        except Exception:
            return True  # If validation fails, accept the value

    def _notify_metric_updates(self, source: str, metrics: List[CollectedMetric]):
        """Notify subscribers of new metrics"""
        for callback in self.metric_callbacks:
            try:
                callback(source, metrics)
            except Exception as e:
                logger.error(f"Error in metric update callback: {e}")

    def collect_metrics_on_demand(self, source: MetricSource) -> MetricCollectionResult:
        """Collect metrics on demand for a specific source"""
        config = self.collection_configs.get(source.value)
        if not config:
            return MetricCollectionResult(
                success=False,
                metrics=[],
                collection_time=datetime.now(),
                duration=0.0,
                errors=[f"No configuration found for source: {source.value}"],
            )

        # For on-demand collection, don't use async timeout
        try:
            start_time = time.time()
            collection_time = datetime.now()
            
            # Get the appropriate collector function
            collector_func = self.collectors.get(source)
            if not collector_func:
                return MetricCollectionResult(
                    success=False,
                    metrics=[],
                    collection_time=collection_time,
                    duration=(time.time() - start_time) * 1000,
                    errors=[f"No collector found for source: {source.value}"],
                )
            
            # Execute collection directly
            metrics = collector_func()
            
            # Validate collected metrics
            validated_metrics = self._validate_metrics(metrics, source.value)
            
            duration = (time.time() - start_time) * 1000
            
            result = MetricCollectionResult(
                success=True,
                metrics=validated_metrics,
                collection_time=collection_time,
                duration=duration,
                errors=[],
                warnings=[],
            )
            
            # Store in history
            self.collection_history.append(result)
            
            return result
            
        except Exception as e:
            duration = (time.time() - start_time) * 1000
            result = MetricCollectionResult(
                success=False,
                metrics=[],
                collection_time=collection_time,
                duration=duration,
                errors=[f"Collection error for {source.value}: {str(e)}"],
                warnings=[],
            )
            self.collection_history.append(result)
            return result

    def get_collection_history(
        self, source: Optional[str] = None, limit: int = 100
    ) -> List[MetricCollectionResult]:
        """Get collection history with optional filtering"""
        history = self.collection_history

        if source:
            history = [h for h in history if any(
                m.source.value == source for m in h.metrics
            )]

        # Return most recent results
        return sorted(history, key=lambda x: x.collection_time, reverse=True)[:limit]

    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get summary of collected metrics"""
        total_collections = len(self.collection_history)
        successful_collections = len([h for h in self.collection_history if h.success])
        total_metrics = sum(len(h.metrics) for h in self.collection_history)

        # Calculate average collection duration
        if total_collections > 0:
            avg_duration = sum(h.duration for h in self.collection_history) / total_collections
        else:
            avg_duration = 0.0

        # Count metrics by source
        source_counts = {}
        for result in self.collection_history:
            for metric in result.metrics:
                source = metric.source.value
                source_counts[source] = source_counts.get(source, 0) + 1

        return {
            "total_collections": total_collections,
            "successful_collections": successful_collections,
            "success_rate": round(successful_collections / max(total_collections, 1) * 100, 2),
            "total_metrics": total_metrics,
            "average_collection_duration_ms": round(avg_duration, 2),
            "metrics_by_source": source_counts,
            "collection_active": self.collection_active,
            "last_update": datetime.now().isoformat(),
        }

    def subscribe_to_metric_updates(self, callback: Callable):
        """Subscribe to metric update notifications"""
        self.metric_callbacks.add(callback)

    def unsubscribe_from_metric_updates(self, callback: Callable):
        """Unsubscribe from metric update notifications"""
        self.metric_callbacks.discard(callback)

    def add_custom_collector(
        self, source: MetricSource, collector_func: Callable, config: MetricCollectionConfig
    ):
        """Add a custom metric collector"""
        self.collectors[source] = collector_func
        self.collection_configs[source.value] = config
        logger.info(f"Custom collector added for source: {source.value}")

    def run_smoke_test(self) -> bool:
        """Run smoke test to verify basic functionality"""
        try:
            logger.info("Running HealthMetricsCollector smoke test...")

            # Test basic initialization
            logger.info("Testing basic initialization...")
            assert self.collection_active is False
            assert len(self.collectors) > 0
            assert len(self.collection_configs) > 0
            logger.info("Basic initialization passed")

            # Test system metrics collection
            logger.info("Testing system metrics collection...")
            system_metrics = self._collect_system_metrics()
            assert len(system_metrics) > 0, f"Expected system metrics but got {len(system_metrics)}"
            logger.info("System metrics collection passed")

            # Test process metrics collection
            logger.info("Testing process metrics collection...")
            process_metrics = self._collect_process_metrics()
            assert len(process_metrics) > 0, f"Expected process metrics but got {len(process_metrics)}"
            logger.info("Process metrics collection passed")

            # Test application metrics collection
            logger.info("Testing application metrics collection...")
            app_metrics = self._collect_application_metrics()
            assert len(app_metrics) > 0, f"Expected application metrics but got {len(app_metrics)}"
            logger.info("Application metrics collection passed")

            # Test on-demand collection
            logger.info("Testing on-demand collection...")
            result = self.collect_metrics_on_demand(MetricSource.SYSTEM)
            assert result.success, f"On-demand collection failed: {result.errors}"
            assert len(result.metrics) > 0, "No metrics returned from on-demand collection"
            logger.info("On-demand collection passed")

            # Test metrics summary
            logger.info("Testing metrics summary...")
            summary = self.get_metrics_summary()
            assert "total_collections" in summary
            assert "total_metrics" in summary
            logger.info("Metrics summary passed")

            logger.info("✅ HealthMetricsCollector smoke test PASSED")
            return True

        except Exception as e:
            logger.error(f"❌ HealthMetricsCollector smoke test FAILED: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return False

    def shutdown(self):
        """Shutdown the metrics collector"""
        self.stop()
        logger.info("HealthMetricsCollector shutdown complete")


def main():
    """CLI testing function"""
    import argparse

    parser = argparse.ArgumentParser(description="Health Metrics Collector CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    parser.add_argument("--collect", choices=["system", "process", "application", "network"], 
                       help="Collect metrics from specific source")

    args = parser.parse_args()

    collector = HealthMetricsCollector()

    if args.test:
        success = collector.run_smoke_test()
        collector.shutdown()
        exit(0 if success else 1)
    elif args.collect:
        source_map = {
            "system": MetricSource.SYSTEM,
            "process": MetricSource.PROCESS,
            "application": MetricSource.APPLICATION,
            "network": MetricSource.NETWORK,
        }
        result = collector.collect_metrics_on_demand(source_map[args.collect])
        print(f"Collection result: {result}")
        collector.shutdown()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
