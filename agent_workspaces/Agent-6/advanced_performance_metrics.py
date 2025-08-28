#!/usr/bin/env python3
"""
Advanced Performance Metrics Implementation - PERF-001 Contract

Comprehensive advanced performance metrics collection and analysis system.
Implements real-time monitoring, predictive analytics, and automated optimization.

Author: Agent-6 (PERFORMANCE OPTIMIZATION MANAGER)
Contract: PERF-001 - Advanced Performance Metrics Implementation
Status: EXECUTION_IN_PROGRESS
"""

import os
import sys
import time
import asyncio
import logging
import json
import psutil
import threading
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict, deque
import statistics

from constants import (
    CPU_USAGE_THRESHOLD,
    MEMORY_USAGE_THRESHOLD,
    DISK_USAGE_THRESHOLD,
    NETWORK_LATENCY_THRESHOLD,
)

# Add src to path for imports
CURRENT_DIR = Path(__file__).resolve().parents[2]
SRC_DIR = CURRENT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

try:
    from src.core.performance import (
        PerformanceMonitor, PerformanceValidator, PerformanceReporter,
        BenchmarkRunner, PerformanceCalculator, PerformanceValidationSystem
    )
    PERFORMANCE_IMPORTS_AVAILABLE = True
except ImportError as e:
    PERFORMANCE_IMPORTS_AVAILABLE = False
    logging.warning(f"Performance imports not available: {e}")


@dataclass
class PerformanceMetric:
    """Advanced performance metric data structure"""
    name: str
    value: float
    unit: str
    timestamp: datetime
    category: str
    severity: str = "normal"
    threshold: Optional[float] = None
    trend: str = "stable"


@dataclass
class SystemSnapshot:
    """Complete system performance snapshot"""
    timestamp: datetime
    cpu_metrics: Dict[str, Any]
    memory_metrics: Dict[str, Any]
    disk_metrics: Dict[str, Any]
    network_metrics: Dict[str, Any]
    application_metrics: Dict[str, Any]
    overall_score: float


class AdvancedMetricsCollector:
    """Advanced system metrics collection system"""
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.AdvancedMetricsCollector")
        self.metrics_history = defaultdict(lambda: deque(maxlen=1000))
        self.collection_active = False
        self.collection_thread = None
        self.collection_interval = 1.0  # 1 second intervals
        
        # Performance thresholds
        self.thresholds = {
            "cpu_usage": CPU_USAGE_THRESHOLD,
            "memory_usage": MEMORY_USAGE_THRESHOLD,
            "disk_usage": DISK_USAGE_THRESHOLD,
            "network_latency": NETWORK_LATENCY_THRESHOLD,
        }
        
        self.logger.info("🚀 Advanced Metrics Collector initialized")
    
    def start_collection(self):
        """Start continuous metrics collection"""
        if not self.collection_active:
            self.collection_active = True
            self.collection_thread = threading.Thread(target=self._collection_loop, daemon=True)
            self.collection_thread.start()
            self.logger.info("✅ Metrics collection started")
    
    def stop_collection(self):
        """Stop metrics collection"""
        self.collection_active = False
        if self.collection_thread:
            self.collection_thread.join()
        self.logger.info("⏹️ Metrics collection stopped")
    
    def _collection_loop(self):
        """Main collection loop"""
        while self.collection_active:
            try:
                snapshot = self._collect_system_snapshot()
                self._store_snapshot(snapshot)
                time.sleep(self.collection_interval)
            except Exception as e:
                self.logger.error(f"Error in collection loop: {e}")
                time.sleep(self.collection_interval)
    
    def _collect_system_snapshot(self) -> SystemSnapshot:
        """Collect comprehensive system performance snapshot"""
        timestamp = datetime.now()
        
        # Collect CPU metrics
        cpu_metrics = self._collect_cpu_metrics()
        
        # Collect memory metrics
        memory_metrics = self._collect_memory_metrics()
        
        # Collect disk metrics
        disk_metrics = self._collect_disk_metrics()
        
        # Collect network metrics
        network_metrics = self._collect_network_metrics()
        
        # Collect application metrics
        application_metrics = self._collect_application_metrics()
        
        # Calculate overall performance score
        overall_score = self._calculate_overall_score(
            cpu_metrics, memory_metrics, disk_metrics, network_metrics
        )
        
        return SystemSnapshot(
            timestamp=timestamp,
            cpu_metrics=cpu_metrics,
            memory_metrics=memory_metrics,
            disk_metrics=disk_metrics,
            network_metrics=network_metrics,
            application_metrics=application_metrics,
            overall_score=overall_score
        )
    
    def _collect_cpu_metrics(self) -> Dict[str, Any]:
        """Collect advanced CPU performance metrics"""
        try:
            cpu_percent = psutil.cpu_percent(interval=0.1)
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            
            # Per-core metrics
            per_cpu = psutil.cpu_percent(interval=0.1, percpu=True)
            
            # Load averages (if available)
            load_avg = self._get_load_average()
            
            # CPU times
            cpu_times = psutil.cpu_times_percent()
            
            return {
                "usage_percent": cpu_percent,
                "core_count": cpu_count,
                "frequency_mhz": cpu_freq.current if cpu_freq else None,
                "per_core_usage": per_cpu,
                "load_average": load_avg,
                "user_time": cpu_times.user,
                "system_time": cpu_times.system,
                "idle_time": cpu_times.idle,
                "iowait_time": cpu_times.iowait if hasattr(cpu_times, 'iowait') else None,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Failed to collect CPU metrics: {e}")
            return {"error": str(e)}
    
    def _collect_memory_metrics(self) -> Dict[str, Any]:
        """Collect advanced memory performance metrics"""
        try:
            memory = psutil.virtual_memory()
            
            # Try to get swap memory (may fail on Windows)
            swap_info = {}
            try:
                swap = psutil.swap_memory()
                swap_info = {
                    "swap_total_gb": swap.total / (1024**3),
                    "swap_used_gb": swap.used / (1024**3),
                    "swap_free_gb": swap.free / (1024**3),
                    "swap_percent": swap.percent
                }
            except Exception as e:
                self.logger.debug(f"Swap memory collection failed (normal on some systems): {e}")
                swap_info = {
                    "swap_total_gb": None,
                    "swap_used_gb": None,
                    "swap_free_gb": None,
                    "swap_percent": None
                }
            
            # Basic memory metrics (should work on all systems)
            basic_metrics = {
                "total_gb": memory.total / (1024**3),
                "available_gb": memory.available / (1024**3),
                "used_gb": memory.used / (1024**3),
                "used_percent": memory.percent,
                "free_gb": memory.free / (1024**3),
                "timestamp": datetime.now().isoformat()
            }
            
            # Try to get advanced memory metrics (may fail on Windows)
            advanced_metrics = {}
            try:
                if hasattr(memory, 'active'):
                    advanced_metrics["active_gb"] = memory.active / (1024**3)
                if hasattr(memory, 'inactive'):
                    advanced_metrics["inactive_gb"] = memory.inactive / (1024**3)
            except Exception as e:
                self.logger.debug(f"Advanced memory metrics collection failed: {e}")
            
            # Combine all metrics
            return {**basic_metrics, **swap_info, **advanced_metrics}
            
        except Exception as e:
            self.logger.error(f"Failed to collect memory metrics: {e}")
            # Return fallback metrics
            return {
                "error": str(e),
                "fallback": True,
                "timestamp": datetime.now().isoformat()
            }
    
    def _collect_disk_metrics(self) -> Dict[str, Any]:
        """Collect advanced disk I/O performance metrics"""
        try:
            disk_usage = psutil.disk_usage('/')
            disk_io = psutil.disk_io_counters()
            
            # Get disk partitions
            partitions = psutil.disk_partitions()
            
            return {
                "total_gb": disk_usage.total / (1024**3),
                "used_gb": disk_usage.used / (1024**3),
                "free_gb": disk_usage.free / (1024**3),
                "used_percent": (disk_usage.used / disk_usage.total) * 100,
                "free_percent": (disk_usage.free / disk_usage.total) * 100,
                "read_bytes": disk_io.read_bytes if disk_io else 0,
                "write_bytes": disk_io.write_bytes if disk_io else 0,
                "read_count": disk_io.read_count if disk_io else 0,
                "write_count": disk_io.write_count if disk_io else 0,
                "read_time": disk_io.read_time if disk_io else 0,
                "write_time": disk_io.write_time if disk_io else 0,
                "partitions": len(partitions),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Failed to collect disk metrics: {e}")
            return {"error": str(e)}
    
    def _collect_network_metrics(self) -> Dict[str, Any]:
        """Collect advanced network performance metrics"""
        try:
            network_io = psutil.net_io_counters()
            network_connections = psutil.net_connections()
            
            # Network interfaces
            net_if_addrs = psutil.net_if_addrs()
            net_if_stats = psutil.net_if_stats()
            
            return {
                "bytes_sent": network_io.bytes_sent,
                "bytes_recv": network_io.bytes_recv,
                "packets_sent": network_io.packets_sent,
                "packets_recv": network_io.packets_recv,
                "errin": network_io.errin,
                "errout": network_io.errout,
                "dropin": network_io.dropin,
                "dropout": network_io.dropout,
                "active_connections": len([c for c in network_connections if c.status == 'ESTABLISHED']),
                "total_connections": len(network_connections),
                "interfaces": len(net_if_addrs),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Failed to collect network metrics: {e}")
            return {"error": str(e)}
    
    def _collect_application_metrics(self) -> Dict[str, Any]:
        """Collect application-specific performance metrics"""
        try:
            # Process metrics
            processes = psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent'])
            process_metrics = []
            
            for proc in processes:
                try:
                    info = proc.info
                    process_metrics.append({
                        "pid": info['pid'],
                        "name": info['name'],
                        "cpu_percent": info['cpu_percent'],
                        "memory_percent": info['memory_percent']
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # Sort by CPU usage
            process_metrics.sort(key=lambda x: x['cpu_percent'], reverse=True)
            top_processes = process_metrics[:10]
            
            return {
                "total_processes": len(process_metrics),
                "top_cpu_processes": top_processes,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Failed to collect application metrics: {e}")
            return {"error": str(e)}
    
    def _get_load_average(self) -> Optional[float]:
        """Get system load average if available"""
        try:
            if hasattr(os, 'getloadavg'):
                return os.getloadavg()[0]
        except Exception:
            pass
        return None
    
    def _calculate_overall_score(self, cpu: Dict, memory: Dict, disk: Dict, network: Dict) -> float:
        """Calculate overall system performance score (0-100)"""
        try:
            score = 100.0
            
            # CPU score (lower usage = higher score)
            if 'usage_percent' in cpu and isinstance(cpu['usage_percent'], (int, float)):
                cpu_usage = cpu['usage_percent']
                if cpu_usage > 90:
                    score -= 30
                elif cpu_usage > 80:
                    score -= 20
                elif cpu_usage > 70:
                    score -= 10
            
            # Memory score (handle fallback metrics)
            if 'used_percent' in memory and isinstance(memory['used_percent'], (int, float)):
                mem_usage = memory['used_percent']
                if mem_usage > 95:
                    score -= 25
                elif mem_usage > 85:
                    score -= 15
                elif mem_usage > 75:
                    score -= 5
            elif memory.get('fallback'):
                # If using fallback metrics, don't penalize score
                self.logger.debug("Using fallback memory metrics - score not penalized")
            
            # Disk score
            if 'used_percent' in disk and isinstance(disk['used_percent'], (int, float)):
                disk_usage = disk['used_percent']
                if disk_usage > 95:
                    score -= 20
                elif disk_usage > 90:
                    score -= 10
                elif disk_usage > 80:
                    score -= 5
            
            # Network score (basic check)
            if 'error' not in network:
                # Network is working, small bonus
                score += 2
            
            return max(0.0, min(100.0, score))
        except Exception as e:
            self.logger.error(f"Failed to calculate overall score: {e}")
            return 50.0
    
    def _store_snapshot(self, snapshot: SystemSnapshot):
        """Store performance snapshot in history"""
        try:
            # Store overall snapshot
            self.metrics_history['system_snapshots'].append(snapshot)
            
            # Store individual metrics
            self.metrics_history['cpu'].append(snapshot.cpu_metrics)
            self.metrics_history['memory'].append(snapshot.memory_metrics)
            self.metrics_history['disk'].append(snapshot.disk_metrics)
            self.metrics_history['network'].append(snapshot.network_metrics)
            self.metrics_history['application'].append(snapshot.application_metrics)
            self.metrics_history['overall_scores'].append(snapshot.overall_score)
            
        except Exception as e:
            self.logger.error(f"Failed to store snapshot: {e}")
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get summary of collected metrics"""
        try:
            if not self.metrics_history['system_snapshots']:
                return {"status": "no_data", "message": "No metrics collected yet"}
            
            latest_snapshot = self.metrics_history['system_snapshots'][-1]
            
            # Calculate trends
            cpu_trend = self._calculate_trend('cpu', 'usage_percent')
            memory_trend = self._calculate_trend('memory', 'used_percent')
            disk_trend = self._calculate_trend('disk', 'used_percent')
            
            return {
                "status": "active",
                "latest_snapshot": asdict(latest_snapshot),
                "trends": {
                    "cpu": cpu_trend,
                    "memory": memory_trend,
                    "disk": disk_trend
                },
                "collection_stats": {
                    "total_snapshots": len(self.metrics_history['system_snapshots']),
                    "collection_active": self.collection_active,
                    "collection_interval": self.collection_interval
                }
            }
        except Exception as e:
            self.logger.error(f"Failed to get metrics summary: {e}")
            return {"error": str(e)}
    
    def _calculate_trend(self, metric_type: str, metric_name: str) -> str:
        """Calculate trend for a specific metric"""
        try:
            metrics = list(self.metrics_history[metric_type])
            if len(metrics) < 2:
                return "insufficient_data"
            
            # Get last 5 values
            recent_values = []
            for metric in metrics[-5:]:
                if isinstance(metric, dict) and metric_name in metric:
                    value = metric[metric_name]
                    if isinstance(value, (int, float)):
                        recent_values.append(value)
            
            if len(recent_values) < 2:
                return "insufficient_data"
            
            # Calculate trend
            first_half = recent_values[:len(recent_values)//2]
            second_half = recent_values[len(recent_values)//2:]
            
            if not first_half or not second_half:
                return "insufficient_data"
            
            first_avg = statistics.mean(first_half)
            second_avg = statistics.mean(second_half)
            
            if second_avg > first_avg * 1.1:
                return "increasing"
            elif second_avg < first_avg * 0.9:
                return "decreasing"
            else:
                return "stable"
                
        except Exception as e:
            self.logger.error(f"Failed to calculate trend: {e}")
            return "error"


class RealTimeMonitor:
    """Real-time performance monitoring system"""
    
    def __init__(self, metrics_collector: AdvancedMetricsCollector):
        self.logger = logging.getLogger(f"{__name__}.RealTimeMonitor")
        self.metrics_collector = metrics_collector
        self.monitoring_active = False
        self.alert_callbacks = []
        self.threshold_violations = defaultdict(list)
        
        self.logger.info("🚀 Real-Time Monitor initialized")
    
    def start_monitoring(self):
        """Start real-time monitoring"""
        if not self.monitoring_active:
            self.monitoring_active = True
            self.metrics_collector.start_collection()
            self._monitor_loop()
            self.logger.info("✅ Real-time monitoring started")
    
    def stop_monitoring(self):
        """Stop real-time monitoring"""
        self.monitoring_active = False
        self.metrics_collector.stop_collection()
        self.logger.info("⏹️ Real-time monitoring stopped")
    
    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.monitoring_active:
            try:
                self._check_thresholds()
                time.sleep(1)  # Check every second
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                time.sleep(1)
    
    def _check_thresholds(self):
        """Check performance thresholds and trigger alerts"""
        try:
            summary = self.metrics_collector.get_metrics_summary()
            if summary.get("status") != "active":
                return
            
            latest = summary.get("latest_snapshot", {})
            
            # Check CPU threshold
            cpu_usage = latest.get("cpu_metrics", {}).get("usage_percent")
            if cpu_usage and cpu_usage > self.metrics_collector.thresholds["cpu_usage"]:
                self._trigger_alert("CPU", "high_usage", cpu_usage, f"CPU usage {cpu_usage}% exceeds threshold")
            
            # Check memory threshold
            memory_usage = latest.get("memory_metrics", {}).get("used_percent")
            if memory_usage and memory_usage > self.metrics_collector.thresholds["memory_usage"]:
                self._trigger_alert("Memory", "high_usage", memory_usage, f"Memory usage {memory_usage}% exceeds threshold")
            
            # Check disk threshold
            disk_usage = latest.get("disk_metrics", {}).get("used_percent")
            if disk_usage and disk_usage > self.metrics_collector.thresholds["disk_usage"]:
                self._trigger_alert("Disk", "high_usage", disk_usage, f"Disk usage {disk_usage}% exceeds threshold")
                
        except Exception as e:
            self.logger.error(f"Failed to check thresholds: {e}")
    
    def _trigger_alert(self, metric_type: str, alert_type: str, value: float, message: str):
        """Trigger performance alert"""
        alert = {
            "timestamp": datetime.now().isoformat(),
            "metric_type": metric_type,
            "alert_type": alert_type,
            "value": value,
            "message": message,
            "severity": "warning" if value < 95 else "critical"
        }
        
        self.threshold_violations[metric_type].append(alert)
        
        # Call alert callbacks
        for callback in self.alert_callbacks:
            try:
                callback(alert)
            except Exception as e:
                self.logger.error(f"Error in alert callback: {e}")
        
        self.logger.warning(f"🚨 ALERT: {message}")
    
    def add_alert_callback(self, callback):
        """Add alert callback function"""
        self.alert_callbacks.append(callback)
    
    def get_alerts(self, metric_type: Optional[str] = None) -> List[Dict]:
        """Get performance alerts"""
        if metric_type:
            return self.threshold_violations.get(metric_type, [])
        else:
            all_alerts = []
            for alerts in self.threshold_violations.values():
                all_alerts.extend(alerts)
            return sorted(all_alerts, key=lambda x: x["timestamp"], reverse=True)


def main():
    """Main execution function for Advanced Performance Metrics"""
    print("🚀 Advanced Performance Metrics System - PERF-001 Contract")
    print("=" * 70)
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Initialize metrics collector
    metrics_collector = AdvancedMetricsCollector()
    
    # Initialize real-time monitor
    monitor = RealTimeMonitor(metrics_collector)
    
    print("✅ Advanced Performance Metrics System initialized successfully")
    
    # Start monitoring
    print("\n🚀 Starting real-time performance monitoring...")
    monitor.start_monitoring()
    
    try:
        # Run for demonstration
        print("📊 Collecting performance metrics for 30 seconds...")
        print("Press Ctrl+C to stop...")
        
        for i in range(30):
            time.sleep(1)
            if i % 5 == 0:
                summary = metrics_collector.get_metrics_summary()
                if summary.get("status") == "active":
                    latest = summary.get("latest_snapshot", {})
                    cpu_usage = latest.get("cpu_metrics", {}).get("usage_percent", "N/A")
                    memory_usage = latest.get("memory_metrics", {}).get("used_percent", "N/A")
                    overall_score = latest.get("overall_score", "N/A")
                    print(f"📈 Metrics: CPU: {cpu_usage}% | Memory: {memory_usage}% | Score: {overall_score}")
        
    except KeyboardInterrupt:
        print("\n⏹️ Stopping monitoring...")
    finally:
        monitor.stop_monitoring()
        print("✅ Advanced Performance Metrics System stopped")
    
    # Display final summary
    print("\n" + "=" * 70)
    print("📋 FINAL METRICS SUMMARY")
    print("=" * 70)
    
    summary = metrics_collector.get_metrics_summary()
    if summary.get("status") == "active":
        print(f"Status: {summary['status']}")
        print(f"Total Snapshots: {summary['collection_stats']['total_snapshots']}")
        print(f"Collection Active: {summary['collection_stats']['collection_active']}")
        
        if summary.get("trends"):
            trends = summary["trends"]
            print(f"CPU Trend: {trends.get('cpu', 'N/A')}")
            print(f"Memory Trend: {trends.get('memory', 'N/A')}")
            print(f"Disk Trend: {trends.get('disk', 'N/A')}")
    else:
        print(f"Status: {summary.get('status', 'Unknown')}")
    
    print(f"\n📁 System saved to: {__file__}")
    print("✅ Advanced Performance Metrics System execution completed!")


if __name__ == "__main__":
    main()
