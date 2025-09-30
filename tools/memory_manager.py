#!/usr/bin/env python3
"""
Memory Management System
========================

Comprehensive memory management system with leak detection, optimization,
and monitoring capabilities for the V2_SWARM project.

Author: Agent-7 (Implementation Specialist)
License: MIT
V2 Compliance: ≤400 lines, comprehensive memory management
"""

import gc
import json
import logging
import psutil
import threading
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class MemoryStats:
    """Memory usage statistics."""
    timestamp: float
    memory_mb: float
    cpu_percent: float
    objects_count: int
    garbage_count: int
    memory_percent: float


class MemoryManager:
    """Comprehensive memory management system."""
    
    def __init__(self, project_root: Path):
        """Initialize memory manager."""
        self.project_root = project_root
        self.stats_history: List[MemoryStats] = []
        self.is_monitoring = False
        self.monitor_thread: Optional[threading.Thread] = None
        self.alert_threshold_mb = 1000.0
        self.cleanup_interval = 300  # 5 minutes
        
        # Memory optimization settings
        self.auto_cleanup = True
        self.gc_threshold = 1000  # Trigger GC when objects exceed this
        self.max_history = 1000  # Keep last 1000 stats
        
        logger.info("Memory Manager initialized")

    def get_current_stats(self) -> MemoryStats:
        """Get current memory statistics."""
        process = psutil.Process()
        memory_info = process.memory_info()
        memory_percent = process.memory_percent()
        
        stats = MemoryStats(
            timestamp=time.time(),
            memory_mb=memory_info.rss / 1024 / 1024,
            cpu_percent=process.cpu_percent(),
            objects_count=len(gc.get_objects()),
            garbage_count=len(gc.garbage),
            memory_percent=memory_percent
        )
        
        return stats

    def record_stats(self, stats: MemoryStats):
        """Record memory statistics."""
        self.stats_history.append(stats)
        
        # Keep only recent history
        if len(self.stats_history) > self.max_history:
            self.stats_history = self.stats_history[-self.max_history:]
        
        # Check for memory issues
        self._check_memory_alerts(stats)

    def _check_memory_alerts(self, stats: MemoryStats):
        """Check for memory-related alerts."""
        alerts = []
        
        # High memory usage
        if stats.memory_mb > self.alert_threshold_mb:
            alerts.append(f"🚨 High memory usage: {stats.memory_mb:.1f}MB")
        
        # High object count
        if stats.objects_count > self.gc_threshold:
            alerts.append(f"📦 High object count: {stats.objects_count}")
        
        # High garbage count
        if stats.garbage_count > 100:
            alerts.append(f"🗑️ High garbage count: {stats.garbage_count}")
        
        # Memory trend analysis
        if len(self.stats_history) >= 10:
            recent_memory = [s.memory_mb for s in self.stats_history[-10:]]
            if all(recent_memory[i] < recent_memory[i+1] for i in range(len(recent_memory)-1)):
                alerts.append("📈 Memory leak detected: continuous growth trend")
        
        # Log alerts
        for alert in alerts:
            logger.warning(alert)
        
        # Auto-cleanup if enabled
        if self.auto_cleanup and alerts:
            self.force_cleanup()

    def force_cleanup(self) -> Dict[str, int]:
        """Force memory cleanup."""
        logger.info("Performing forced memory cleanup...")
        
        # Garbage collection
        collected = gc.collect()
        
        # Clear garbage
        gc.garbage.clear()
        
        # Get stats after cleanup
        stats_after = self.get_current_stats()
        
        cleanup_stats = {
            "objects_collected": collected,
            "memory_freed_mb": 0,  # Would need before/after comparison
            "garbage_cleared": len(gc.garbage),
            "objects_after": stats_after.objects_count
        }
        
        logger.info(f"Cleanup complete: {collected} objects collected")
        return cleanup_stats

    def start_monitoring(self, interval: float = 30.0):
        """Start continuous memory monitoring."""
        if self.is_monitoring:
            logger.warning("Monitoring already active")
            return
        
        self.is_monitoring = True
        self.monitor_thread = threading.Thread(
            target=self._monitoring_loop,
            args=(interval,),
            daemon=True
        )
        self.monitor_thread.start()
        
        logger.info(f"Memory monitoring started (interval: {interval}s)")

    def stop_monitoring(self):
        """Stop memory monitoring."""
        self.is_monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        logger.info("Memory monitoring stopped")

    def _monitoring_loop(self, interval: float):
        """Main monitoring loop."""
        while self.is_monitoring:
            try:
                stats = self.get_current_stats()
                self.record_stats(stats)
                
                # Periodic cleanup
                if len(self.stats_history) % (self.cleanup_interval // interval) == 0:
                    self.force_cleanup()
                
                time.sleep(interval)
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(interval)

    def get_memory_summary(self) -> Dict[str, Any]:
        """Get comprehensive memory summary."""
        if not self.stats_history:
            return {"error": "No memory data available"}
        
        current_stats = self.stats_history[-1]
        
        # Calculate trends
        if len(self.stats_history) >= 10:
            recent_memory = [s.memory_mb for s in self.stats_history[-10:]]
            memory_trend = "increasing" if recent_memory[-1] > recent_memory[0] else "stable"
        else:
            memory_trend = "insufficient_data"
        
        # Calculate averages
        avg_memory = sum(s.memory_mb for s in self.stats_history) / len(self.stats_history)
        avg_objects = sum(s.objects_count for s in self.stats_history) / len(self.stats_history)
        
        summary = {
            "current_memory_mb": current_stats.memory_mb,
            "current_objects": current_stats.objects_count,
            "current_garbage": current_stats.garbage_count,
            "memory_trend": memory_trend,
            "average_memory_mb": avg_memory,
            "average_objects": avg_objects,
            "total_snapshots": len(self.stats_history),
            "monitoring_active": self.is_monitoring,
            "last_cleanup": datetime.now().isoformat()
        }
        
        return summary

    def export_memory_report(self, output_file: Path = None) -> str:
        """Export comprehensive memory report."""
        if not output_file:
            output_file = self.project_root / "memory_management_report.json"
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "project_root": str(self.project_root),
            "summary": self.get_memory_summary(),
            "stats_history": [
                {
                    "timestamp": stats.timestamp,
                    "memory_mb": stats.memory_mb,
                    "cpu_percent": stats.cpu_percent,
                    "objects_count": stats.objects_count,
                    "garbage_count": stats.garbage_count,
                    "memory_percent": stats.memory_percent
                }
                for stats in self.stats_history[-100:]  # Last 100 snapshots
            ],
            "recommendations": self._generate_recommendations()
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Memory report exported to: {output_file}")
        return str(output_file)

    def _generate_recommendations(self) -> List[str]:
        """Generate memory optimization recommendations."""
        recommendations = []
        
        if not self.stats_history:
            return ["No memory data available for recommendations"]
        
        current_stats = self.stats_history[-1]
        
        # Memory usage recommendations
        if current_stats.memory_mb > 500:
            recommendations.append("💾 Consider reducing memory usage - current usage is high")
        
        if current_stats.objects_count > 10000:
            recommendations.append("📦 High object count detected - consider object pooling")
        
        if current_stats.garbage_count > 50:
            recommendations.append("🗑️ High garbage count - ensure proper cleanup")
        
        # Trend-based recommendations
        if len(self.stats_history) >= 10:
            recent_memory = [s.memory_mb for s in self.stats_history[-10:]]
            if all(recent_memory[i] < recent_memory[i+1] for i in range(len(recent_memory)-1)):
                recommendations.append("📈 Memory leak detected - investigate resource cleanup")
        
        # General recommendations
        recommendations.extend([
            "🔧 Enable automatic cleanup for better memory management",
            "📊 Monitor memory usage regularly to detect issues early",
            "🧹 Use context managers for file and database operations",
            "⚡ Consider using weak references for large object graphs"
        ])
        
        return recommendations


def main():
    """Main function for memory management."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Memory Management System")
    parser.add_argument("--project-root", default=".", help="Project root directory")
    parser.add_argument("--monitor", action="store_true", help="Start monitoring mode")
    parser.add_argument("--interval", type=float, default=30.0, help="Monitoring interval")
    parser.add_argument("--cleanup", action="store_true", help="Force cleanup")
    parser.add_argument("--report", action="store_true", help="Generate report")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    
    project_root = Path(args.project_root)
    manager = MemoryManager(project_root)
    
    if args.cleanup:
        cleanup_stats = manager.force_cleanup()
        print(f"🧹 Cleanup completed: {cleanup_stats}")
    
    if args.report:
        report_file = manager.export_memory_report()
        summary = manager.get_memory_summary()
        print(f"\n📊 Memory Summary:")
        print(f"💾 Current memory: {summary.get('current_memory_mb', 0):.1f}MB")
        print(f"📦 Current objects: {summary.get('current_objects', 0)}")
        print(f"📈 Memory trend: {summary.get('memory_trend', 'unknown')}")
        print(f"📄 Report saved: {report_file}")
    
    if args.monitor:
        try:
            manager.start_monitoring(args.interval)
            print(f"🔍 Memory monitoring started (interval: {args.interval}s)")
            print("Press Ctrl+C to stop...")
            
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            manager.stop_monitoring()
            print("\n🛑 Monitoring stopped")


if __name__ == "__main__":
    main()
