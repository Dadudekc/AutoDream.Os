#!/usr/bin/env python3
"""
Memory Monitor - Real-time Memory Leak Detection
===============================================

Real-time memory monitoring and leak detection tool.
Monitors memory usage and alerts on potential leaks.

Author: Agent-7 (Implementation Specialist)
License: MIT
"""

import gc
import logging
import psutil
import time
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List

logger = logging.getLogger(__name__)


@dataclass
class MemorySnapshot:
    """Memory usage snapshot."""
    timestamp: float
    memory_mb: float
    cpu_percent: float
    objects_count: int
    garbage_count: int


class MemoryMonitor:
    """Real-time memory monitoring system."""
    
    def __init__(self, alert_threshold_mb: float = 1000.0):
        """Initialize memory monitor."""
        self.alert_threshold = alert_threshold_mb
        self.snapshots: List[MemorySnapshot] = []
        self.is_monitoring = False
        
    def take_snapshot(self) -> MemorySnapshot:
        """Take a memory snapshot."""
        process = psutil.Process()
        memory_info = process.memory_info()
        
        snapshot = MemorySnapshot(
            timestamp=time.time(),
            memory_mb=memory_info.rss / 1024 / 1024,
            cpu_percent=process.cpu_percent(),
            objects_count=len(gc.get_objects()),
            garbage_count=len(gc.garbage)
        )
        
        self.snapshots.append(snapshot)
        
        # Keep only last 100 snapshots
        if len(self.snapshots) > 100:
            self.snapshots = self.snapshots[-100:]
            
        return snapshot
    
    def check_for_leaks(self) -> List[str]:
        """Check for potential memory leaks."""
        alerts = []
        
        if len(self.snapshots) < 10:
            return alerts
            
        # Check for increasing memory trend
        recent_snapshots = self.snapshots[-10:]
        memory_trend = [s.memory_mb for s in recent_snapshots]
        
        if all(memory_trend[i] < memory_trend[i+1] for i in range(len(memory_trend)-1)):
            alerts.append(f"🚨 Memory leak detected: {memory_trend[-1]:.1f}MB")
            
        # Check for high memory usage
        current_memory = recent_snapshots[-1].memory_mb
        if current_memory > self.alert_threshold:
            alerts.append(f"⚠️ High memory usage: {current_memory:.1f}MB")
            
        # Check for garbage collection issues
        if recent_snapshots[-1].garbage_count > 100:
            alerts.append(f"🗑️ High garbage count: {recent_snapshots[-1].garbage_count}")
            
        return alerts
    
    def force_cleanup(self):
        """Force garbage collection and cleanup."""
        collected = gc.collect()
        logger.info(f"Garbage collection freed {collected} objects")
        return collected
    
    def start_monitoring(self, interval: float = 30.0):
        """Start continuous monitoring."""
        self.is_monitoring = True
        logger.info(f"Memory monitoring started (interval: {interval}s)")
        
        while self.is_monitoring:
            snapshot = self.take_snapshot()
            alerts = self.check_for_leaks()
            
            if alerts:
                for alert in alerts:
                    logger.warning(alert)
                    
            time.sleep(interval)
    
    def stop_monitoring(self):
        """Stop monitoring."""
        self.is_monitoring = False
        logger.info("Memory monitoring stopped")


def main():
    """Main function for memory monitoring."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Memory Monitor")
    parser.add_argument("--interval", type=float, default=30.0, help="Monitoring interval in seconds")
    parser.add_argument("--threshold", type=float, default=1000.0, help="Memory alert threshold in MB")
    parser.add_argument("--cleanup", action="store_true", help="Force cleanup before monitoring")
    
    args = parser.parse_args()
    
    logging.basicConfig(level=logging.INFO)
    
    monitor = MemoryMonitor(args.threshold)
    
    if args.cleanup:
        monitor.force_cleanup()
    
    try:
        monitor.start_monitoring(args.interval)
    except KeyboardInterrupt:
        monitor.stop_monitoring()


if __name__ == "__main__":
    main()
