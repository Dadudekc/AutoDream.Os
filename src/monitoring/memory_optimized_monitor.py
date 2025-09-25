#!/usr/bin/env python3
"""
Memory-Optimized Performance Monitor
====================================

Optimized version with reduced memory footprint and efficient data structures.
V2 Compliance: ≤400 lines, focused on memory efficiency.
"""

import asyncio
import time
import logging
import json
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
import psutil
import weakref
from collections import deque

logger = logging.getLogger(__name__)


@dataclass
class LightweightSnapshot:
    """Lightweight performance snapshot with minimal memory usage."""
    
    timestamp: float  # Unix timestamp instead of datetime object
    cpu_percent: float
    memory_mb: float
    active_connections: int
    error_count: int
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "timestamp": datetime.fromtimestamp(self.timestamp).isoformat(),
            "cpu_percent": self.cpu_percent,
            "memory_mb": self.memory_mb,
            "active_connections": self.active_connections,
            "error_count": self.error_count
        }


class MemoryOptimizedMonitor:
    """Memory-optimized performance monitoring system."""
    
    def __init__(self, project_root: Path, max_history: int = 100):
        self.project_root = project_root
        self.max_history = max_history  # Limit history size
        self.is_monitoring = False
        self.monitoring_task: Optional[asyncio.Task] = None
        
        # Use deque for efficient memory usage
        self.performance_history: deque = deque(maxlen=max_history)
        self.component_metrics: Dict[str, Dict[str, Any]] = {}
        
        # Alert thresholds
        self.alert_thresholds = {
            "cpu_percent": 80.0,
            "memory_mb": 1000.0,
            "error_rate": 0.1
        }
        
        # Monitoring state - use simple counters
        self.start_time = time.time()
        self.total_requests = 0
        self.total_errors = 0
        self.lock = threading.RLock()
        
        # Component references - use weak references
        self.component_refs: Dict[str, weakref.ref] = {}
    
    def register_component(self, component_name: str, component_ref):
        """Register component with weak reference."""
        with self.lock:
            self.component_refs[component_name] = weakref.ref(component_ref)
            self.component_metrics[component_name] = {
                "total_requests": 0,
                "successful_requests": 0,
                "failed_requests": 0,
                "last_activity": time.time()
            }
            logger.info(f"Registered component: {component_name}")
    
    def record_request(self, component_name: str, success: bool):
        """Record request with minimal memory usage."""
        with self.lock:
            if component_name not in self.component_metrics:
                self.component_metrics[component_name] = {
                    "total_requests": 0,
                    "successful_requests": 0,
                    "failed_requests": 0,
                    "last_activity": time.time()
                }
            
            metrics = self.component_metrics[component_name]
            metrics["total_requests"] += 1
            metrics["last_activity"] = time.time()
            
            if success:
                metrics["successful_requests"] += 1
            else:
                metrics["failed_requests"] += 1
                self.total_errors += 1
            
            self.total_requests += 1
    
    async def collect_system_metrics(self) -> LightweightSnapshot:
        """Collect metrics with minimal memory allocation."""
        try:
            # Get system metrics efficiently
            cpu_percent = psutil.cpu_percent(interval=0.1)  # Shorter interval
            memory = psutil.virtual_memory()
            
            # Get active connections efficiently
            try:
                connections = len(psutil.net_connections())
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                connections = 0
            
            return LightweightSnapshot(
                timestamp=time.time(),
                cpu_percent=cpu_percent,
                memory_mb=memory.used / 1024 / 1024,
                active_connections=connections,
                error_count=self.total_errors
            )
            
        except Exception as e:
            logger.error(f"Failed to collect metrics: {e}")
            return LightweightSnapshot(
                timestamp=time.time(),
                cpu_percent=0.0,
                memory_mb=0.0,
                active_connections=0,
                error_count=0
            )
    
    async def check_alerts(self, snapshot: LightweightSnapshot):
        """Check for alerts with minimal processing."""
        alerts = []
        
        if snapshot.cpu_percent > self.alert_thresholds["cpu_percent"]:
            alerts.append(f"High CPU: {snapshot.cpu_percent:.1f}%")
        
        if snapshot.memory_mb > self.alert_thresholds["memory_mb"]:
            alerts.append(f"High memory: {snapshot.memory_mb:.1f}MB")
        
        # Check error rate
        if self.total_requests > 0:
            error_rate = self.total_errors / self.total_requests
            if error_rate > self.alert_thresholds["error_rate"]:
                alerts.append(f"High error rate: {error_rate:.1%}")
        
        if alerts:
            logger.warning(f"Alerts: {'; '.join(alerts)}")
            await self._handle_alerts(alerts, snapshot)
    
    async def _handle_alerts(self, alerts: List[str], snapshot: LightweightSnapshot):
        """Handle alerts with minimal memory usage."""
        # Simple alert logging - no complex data structures
        alert_data = {
            "timestamp": datetime.fromtimestamp(snapshot.timestamp).isoformat(),
            "alerts": alerts,
            "cpu": snapshot.cpu_percent,
            "memory": snapshot.memory_mb
        }
        
        # Write to file efficiently
        alert_file = self.project_root / "logs" / "alerts.jsonl"
        alert_file.parent.mkdir(exist_ok=True)
        
        with open(alert_file, 'a') as f:
            f.write(json.dumps(alert_data) + '\n')
    
    async def monitoring_loop(self, interval: int = 60):
        """Optimized monitoring loop with longer intervals."""
        logger.info("Starting memory-optimized monitoring...")
        
        while self.is_monitoring:
            try:
                # Collect metrics
                snapshot = await self.collect_system_metrics()
                
                # Store snapshot (deque automatically manages size)
                self.performance_history.append(snapshot)
                
                # Check for alerts
                await self.check_alerts(snapshot)
                
                # Log status (less frequently)
                logger.debug(f"CPU: {snapshot.cpu_percent:.1f}%, Memory: {snapshot.memory_mb:.1f}MB")
                
                # Wait for next interval
                await asyncio.sleep(interval)
                
            except Exception as e:
                logger.error(f"Monitoring error: {e}")
                await asyncio.sleep(interval)
    
    async def start_monitoring(self, interval: int = 60):
        """Start monitoring with configurable interval."""
        if self.is_monitoring:
            logger.warning("Monitoring already started")
            return
        
        self.is_monitoring = True
        self.monitoring_task = asyncio.create_task(self.monitoring_loop(interval))
        logger.info(f"Memory-optimized monitoring started (interval: {interval}s)")
    
    async def stop_monitoring(self):
        """Stop monitoring."""
        if not self.is_monitoring:
            logger.warning("Monitoring not started")
            return
        
        self.is_monitoring = False
        
        if self.monitoring_task:
            self.monitoring_task.cancel()
            try:
                await self.monitoring_task
            except asyncio.CancelledError:
                pass
        
        logger.info("Memory-optimized monitoring stopped")
    
    def get_current_status(self) -> Dict[str, Any]:
        """Get current status with minimal memory usage."""
        current_time = time.time()
        uptime = current_time - self.start_time
        
        # Get recent metrics
        recent_snapshots = list(self.performance_history)[-5:]  # Last 5 only
        
        if recent_snapshots:
            avg_cpu = sum(s.cpu_percent for s in recent_snapshots) / len(recent_snapshots)
            avg_memory = sum(s.memory_mb for s in recent_snapshots) / len(recent_snapshots)
        else:
            avg_cpu = 0.0
            avg_memory = 0.0
        
        return {
            "uptime_seconds": uptime,
            "monitoring_active": self.is_monitoring,
            "total_requests": self.total_requests,
            "total_errors": self.total_errors,
            "error_rate": self.total_errors / self.total_requests if self.total_requests > 0 else 0,
            "recent_cpu_avg": avg_cpu,
            "recent_memory_avg": avg_memory,
            "history_size": len(self.performance_history),
            "component_count": len(self.component_metrics)
        }
    
    def get_memory_usage(self) -> Dict[str, Any]:
        """Get memory usage statistics."""
        import sys
        
        # Get current process memory
        process = psutil.Process()
        memory_info = process.memory_info()
        
        # Estimate object sizes
        history_size = len(self.performance_history) * 50  # Rough estimate
        metrics_size = len(self.component_metrics) * 100  # Rough estimate
        
        return {
            "process_memory_mb": memory_info.rss / 1024 / 1024,
            "history_objects": len(self.performance_history),
            "estimated_history_memory_kb": history_size,
            "component_metrics_count": len(self.component_metrics),
            "estimated_metrics_memory_kb": metrics_size,
            "total_estimated_memory_kb": history_size + metrics_size
        }
    
    def clear_old_data(self):
        """Clear old data to free memory."""
        with self.lock:
            # Clear old history (deque already manages this)
            old_size = len(self.performance_history)
            
            # Clear old component metrics
            current_time = time.time()
            for component_name, metrics in self.component_metrics.items():
                if current_time - metrics["last_activity"] > 3600:  # 1 hour
                    del self.component_metrics[component_name]
            
            logger.info(f"Cleared old data, freed memory")
    
    def save_lightweight_report(self) -> bool:
        """Save lightweight report with minimal data."""
        try:
            report = {
                "report_time": datetime.now().isoformat(),
                "status": self.get_current_status(),
                "memory_usage": self.get_memory_usage(),
                "recent_snapshots": [
                    snapshot.to_dict() 
                    for snapshot in list(self.performance_history)[-10:]  # Last 10 only
                ]
            }
            
            report_path = self.project_root / "logs" / "lightweight_report.json"
            report_path.parent.mkdir(exist_ok=True)
            
            with open(report_path, 'w') as f:
                json.dump(report, f, indent=2)
            
            logger.info(f"Lightweight report saved: {report_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save report: {e}")
            return False


# Global lightweight monitor instance
_global_lightweight_monitor: Optional[MemoryOptimizedMonitor] = None


def get_lightweight_monitor() -> MemoryOptimizedMonitor:
    """Get global lightweight monitor instance."""
    global _global_lightweight_monitor
    if _global_lightweight_monitor is None:
        _global_lightweight_monitor = MemoryOptimizedMonitor(Path("."))
    return _global_lightweight_monitor


async def start_lightweight_monitoring(interval: int = 60):
    """Start lightweight monitoring."""
    monitor = get_lightweight_monitor()
    await monitor.start_monitoring(interval)


async def stop_lightweight_monitoring():
    """Stop lightweight monitoring."""
    monitor = get_lightweight_monitor()
    await monitor.stop_monitoring()




