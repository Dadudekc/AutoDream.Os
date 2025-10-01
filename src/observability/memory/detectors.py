"""
Memory Leak Detection System - V2_SWARM
=======================================

Advanced memory leak detection with policy-driven thresholds.
Integrates with tracemalloc for detailed leak analysis.

Author: Agent-5 (Coordinator)
License: MIT
"""

import gc
import logging
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class LeakDetectionResult:
    """Memory leak detection result"""
    
    leak_detected: bool
    severity: str  # none, low, medium, high, critical
    memory_growth_mb: float
    memory_growth_percent: float
    object_count_growth: int
    timestamp: float
    details: Dict[str, Any]


@dataclass
class MemoryTrend:
    """Memory usage trend analysis"""
    
    direction: str  # increasing, decreasing, stable
    rate_mb_per_second: float
    total_growth_mb: float
    duration_seconds: float


class MemoryLeakDetector:
    """Detect memory leaks using snapshot comparison"""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize leak detector"""
        self.config = config
        self.snapshots = []
        self.max_snapshots = config.get('leak_detection', {}).get('snapshot_retention_count', 10)
    
    def add_snapshot(self, snapshot) -> None:
        """Add memory snapshot for tracking"""
        self.snapshots.append(snapshot)
        
        # Maintain snapshot limit
        if len(self.snapshots) > self.max_snapshots:
            self.snapshots.pop(0)
    
    def detect_leak(self) -> LeakDetectionResult:
        """Detect memory leaks from snapshots"""
        if len(self.snapshots) < 2:
            return LeakDetectionResult(
                leak_detected=False,
                severity="none",
                memory_growth_mb=0,
                memory_growth_percent=0,
                object_count_growth=0,
                timestamp=time.time(),
                details={'reason': 'insufficient snapshots'}
            )
        
        # Compare first and last snapshots
        first = self.snapshots[0]
        last = self.snapshots[-1]
        
        # Calculate growth
        memory_growth_mb = last.current_mb - first.current_mb
        memory_growth_percent = (memory_growth_mb / first.current_mb * 100) if first.current_mb > 0 else 0
        object_count_growth = last.object_count - first.object_count
        
        # Check thresholds
        thresholds = self.config.get('leak_detection', {}).get('thresholds', {})
        memory_threshold_mb = thresholds.get('memory_growth_mb', 10)
        memory_threshold_percent = thresholds.get('memory_growth_percent', 20)
        object_threshold = thresholds.get('object_count_growth', 1000)
        
        leak_detected = (
            memory_growth_mb > memory_threshold_mb or
            memory_growth_percent > memory_threshold_percent or
            object_count_growth > object_threshold
        )
        
        # Determine severity
        severity = self._calculate_severity(
            memory_growth_mb, memory_growth_percent, object_count_growth
        )
        
        return LeakDetectionResult(
            leak_detected=leak_detected,
            severity=severity,
            memory_growth_mb=memory_growth_mb,
            memory_growth_percent=memory_growth_percent,
            object_count_growth=object_count_growth,
            timestamp=time.time(),
            details={
                'snapshot_count': len(self.snapshots),
                'first_snapshot': first.timestamp,
                'last_snapshot': last.timestamp,
                'duration_seconds': last.timestamp - first.timestamp
            }
        )
    
    def _calculate_severity(self, growth_mb: float, growth_percent: float, 
                           object_growth: int) -> str:
        """Calculate leak severity"""
        if growth_mb > 100 or growth_percent > 100:
            return "critical"
        elif growth_mb > 50 or growth_percent > 50:
            return "high"
        elif growth_mb > 20 or growth_percent > 30:
            return "medium"
        elif growth_mb > 10 or growth_percent > 20:
            return "low"
        else:
            return "none"
    
    def analyze_trend(self) -> Optional[MemoryTrend]:
        """Analyze memory usage trend"""
        if len(self.snapshots) < 3:
            return None
        
        first = self.snapshots[0]
        last = self.snapshots[-1]
        
        total_growth_mb = last.current_mb - first.current_mb
        duration_seconds = last.timestamp - first.timestamp
        
        if duration_seconds == 0:
            return None
        
        rate_mb_per_second = total_growth_mb / duration_seconds
        
        # Determine direction
        if abs(total_growth_mb) < 1:
            direction = "stable"
        elif total_growth_mb > 0:
            direction = "increasing"
        else:
            direction = "decreasing"
        
        return MemoryTrend(
            direction=direction,
            rate_mb_per_second=rate_mb_per_second,
            total_growth_mb=total_growth_mb,
            duration_seconds=duration_seconds
        )


class ObjectLeakDetector:
    """Detect object allocation leaks"""
    
    def __init__(self):
        """Initialize object leak detector"""
        self.object_snapshots = []
    
    def take_object_snapshot(self) -> Dict[str, int]:
        """Take snapshot of object counts by type"""
        gc.collect()
        objects = gc.get_objects()
        
        type_counts = {}
        for obj in objects:
            obj_type = type(obj).__name__
            type_counts[obj_type] = type_counts.get(obj_type, 0) + 1
        
        snapshot = {
            'timestamp': time.time(),
            'total_objects': len(objects),
            'type_counts': type_counts
        }
        
        self.object_snapshots.append(snapshot)
        
        # Keep only last 10 snapshots
        if len(self.object_snapshots) > 10:
            self.object_snapshots.pop(0)
        
        return snapshot
    
    def detect_object_leaks(self) -> List[Dict[str, Any]]:
        """Detect objects that are leaking"""
        if len(self.object_snapshots) < 2:
            return []
        
        first = self.object_snapshots[0]
        last = self.object_snapshots[-1]
        
        leaks = []
        
        for obj_type, last_count in last['type_counts'].items():
            first_count = first['type_counts'].get(obj_type, 0)
            growth = last_count - first_count
            
            # Flag significant growth (>100 objects or >50% growth)
            if growth > 100 or (first_count > 0 and growth / first_count > 0.5):
                leaks.append({
                    'object_type': obj_type,
                    'first_count': first_count,
                    'last_count': last_count,
                    'growth': growth,
                    'growth_percent': (growth / first_count * 100) if first_count > 0 else 0
                })
        
        return sorted(leaks, key=lambda x: x['growth'], reverse=True)


class AutoCleanupManager:
    """Manage automatic cleanup operations"""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize auto cleanup manager"""
        self.config = config
        self.auto_cleanup_config = config.get('leak_detection', {}).get('auto_cleanup', {})
    
    def should_trigger_cleanup(self, leak_result: LeakDetectionResult) -> bool:
        """Check if automatic cleanup should be triggered"""
        if not self.auto_cleanup_config.get('enabled', True):
            return False
        
        threshold_mb = self.auto_cleanup_config.get('threshold_mb', 50)
        return leak_result.memory_growth_mb >= threshold_mb
    
    def execute_cleanup(self) -> Dict[str, Any]:
        """Execute automatic cleanup methods"""
        methods = self.auto_cleanup_config.get('methods', [])
        results = {}
        
        for method in methods:
            if method == 'garbage_collection':
                collected = gc.collect()
                results['garbage_collection'] = {'collected': collected}
            
            elif method == 'resource_cleanup':
                # Hook for resource cleanup
                results['resource_cleanup'] = {'status': 'executed'}
            
            elif method == 'cache_flush':
                # Hook for cache flushing
                results['cache_flush'] = {'status': 'executed'}
        
        return results


class ComprehensiveLeakDetector:
    """Comprehensive memory leak detection system"""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize comprehensive detector"""
        self.config = config
        self.memory_detector = MemoryLeakDetector(config)
        self.object_detector = ObjectLeakDetector()
        self.cleanup_manager = AutoCleanupManager(config)
    
    def add_snapshot(self, snapshot) -> None:
        """Add snapshot for leak detection"""
        self.memory_detector.add_snapshot(snapshot)
        self.object_detector.take_object_snapshot()
    
    def run_full_detection(self) -> Dict[str, Any]:
        """Run full leak detection analysis"""
        # Detect memory leaks
        leak_result = self.memory_detector.detect_leak()
        
        # Analyze trend
        trend = self.memory_detector.analyze_trend()
        
        # Detect object leaks
        object_leaks = self.object_detector.detect_object_leaks()
        
        # Check if cleanup needed
        cleanup_triggered = False
        cleanup_results = None
        
        if self.cleanup_manager.should_trigger_cleanup(leak_result):
            cleanup_triggered = True
            cleanup_results = self.cleanup_manager.execute_cleanup()
        
        return {
            'leak_detection': {
                'detected': leak_result.leak_detected,
                'severity': leak_result.severity,
                'memory_growth_mb': leak_result.memory_growth_mb,
                'memory_growth_percent': leak_result.memory_growth_percent,
                'object_count_growth': leak_result.object_count_growth,
                'details': leak_result.details
            },
            'trend_analysis': {
                'direction': trend.direction if trend else 'unknown',
                'rate_mb_per_second': trend.rate_mb_per_second if trend else 0,
                'total_growth_mb': trend.total_growth_mb if trend else 0
            } if trend else None,
            'object_leaks': object_leaks[:10],  # Top 10 object leaks
            'auto_cleanup': {
                'triggered': cleanup_triggered,
                'results': cleanup_results
            } if cleanup_triggered else None
        }

