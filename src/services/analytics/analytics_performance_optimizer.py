#!/usr/bin/env python3
"""
Analytics Performance Optimizer - V2 Compliant
==============================================

Analytics performance optimization service with caching, parallel processing, and resource management.
V2 COMPLIANT: Under 400 lines, single responsibility.

Author: Agent-5 (Business Intelligence Specialist)
License: MIT
"""

import logging
import time
import threading
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class PerformanceMetrics:
    """Performance metrics tracking."""
    
    def __init__(self):
        self.metrics = defaultdict(list)
        self.lock = threading.RLock()
    
    def record_metric(self, metric_name: str, value: float, timestamp: Optional[datetime] = None) -> None:
        """Record a performance metric."""
        if timestamp is None:
            timestamp = datetime.now()
        
        with self.lock:
            self.metrics[metric_name].append({
                "value": value,
                "timestamp": timestamp
            })
    
    def get_metric_stats(self, metric_name: str, time_window_minutes: int = 60) -> Dict[str, Any]:
        """Get statistics for a specific metric."""
        with self.lock:
            if metric_name not in self.metrics:
                return {"error": "Metric not found"}
            
            # Filter by time window
            cutoff_time = datetime.now() - timedelta(minutes=time_window_minutes)
            recent_metrics = [
                m for m in self.metrics[metric_name] 
                if m["timestamp"] >= cutoff_time
            ]
            
            if not recent_metrics:
                return {"error": "No data in time window"}
            
            values = [m["value"] for m in recent_metrics]
            
            return {
                "count": len(values),
                "min": min(values),
                "max": max(values),
                "avg": sum(values) / len(values),
                "latest": values[-1],
                "time_window_minutes": time_window_minutes
            }


class CacheOptimizer:
    """Cache optimization engine."""
    
    def __init__(self, max_cache_size: int = 1000):
        self.max_cache_size = max_cache_size
        self.cache = {}
        self.access_times = {}
        self.access_counts = {}
        self.lock = threading.RLock()
        self.optimization_stats = {
            'cache_hits': 0,
            'cache_misses': 0,
            'evictions': 0,
            'optimizations': 0
        }
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        with self.lock:
            if key in self.cache:
                self.access_times[key] = datetime.now()
                self.access_counts[key] = self.access_counts.get(key, 0) + 1
                self.optimization_stats['cache_hits'] += 1
                return self.cache[key]
            else:
                self.optimization_stats['cache_misses'] += 1
                return None
    
    def set(self, key: str, value: Any, ttl_seconds: int = 3600) -> None:
        """Set value in cache."""
        with self.lock:
            # Evict if cache is full
            if len(self.cache) >= self.max_cache_size and key not in self.cache:
                self._evict_least_used()
            
            self.cache[key] = value
            self.access_times[key] = datetime.now()
            self.access_counts[key] = 0
    
    def _evict_least_used(self) -> None:
        """Evict least recently used item."""
        if not self.cache:
            return
        
        # Find least recently used item
        lru_key = min(self.access_times.keys(), key=lambda k: self.access_times[k])
        
        # Remove from cache
        del self.cache[lru_key]
        del self.access_times[lru_key]
        del self.access_counts[lru_key]
        
        self.optimization_stats['evictions'] += 1
    
    def optimize_cache(self) -> Dict[str, Any]:
        """Optimize cache performance."""
        with self.lock:
            # Remove expired items
            current_time = datetime.now()
            expired_keys = []
            
            for key, access_time in self.access_times.items():
                if (current_time - access_time).total_seconds() > 3600:  # 1 hour TTL
                    expired_keys.append(key)
            
            for key in expired_keys:
                if key in self.cache:
                    del self.cache[key]
                    del self.access_times[key]
                    del self.access_counts[key]
            
            self.optimization_stats['optimizations'] += 1
            
            return {
                "cache_size": len(self.cache),
                "expired_removed": len(expired_keys),
                "hit_rate": self._calculate_hit_rate()
            }
    
    def _calculate_hit_rate(self) -> float:
        """Calculate cache hit rate."""
        total_requests = self.optimization_stats['cache_hits'] + self.optimization_stats['cache_misses']
        if total_requests == 0:
            return 0.0
        return self.optimization_stats['cache_hits'] / total_requests


class QueryOptimizer:
    """Query optimization engine."""
    
    def __init__(self):
        self.query_cache = {}
        self.query_stats = defaultdict(int)
        self.optimization_rules = {
            'max_query_time': 5.0,  # seconds
            'max_result_size': 10000,
            'parallel_threshold': 1000
        }
    
    def optimize_query(self, query: str, estimated_rows: int) -> Dict[str, Any]:
        """Optimize a query based on estimated parameters."""
        optimization_suggestions = []
        
        # Check query complexity
        if len(query) > 1000:
            optimization_suggestions.append("Consider breaking down complex query into smaller parts")
        
        # Check estimated result size
        if estimated_rows > self.optimization_rules['max_result_size']:
            optimization_suggestions.append("Consider adding LIMIT clause or pagination")
        
        # Check for parallel processing opportunity
        if estimated_rows > self.optimization_rules['parallel_threshold']:
            optimization_suggestions.append("Query suitable for parallel processing")
        
        # Check for common optimization patterns
        if 'SELECT *' in query.upper():
            optimization_suggestions.append("Consider selecting specific columns instead of *")
        
        if 'ORDER BY' in query.upper() and 'LIMIT' not in query.upper():
            optimization_suggestions.append("Consider adding LIMIT when using ORDER BY")
        
        return {
            "query": query,
            "estimated_rows": estimated_rows,
            "optimization_suggestions": optimization_suggestions,
            "optimization_score": self._calculate_optimization_score(query, estimated_rows)
        }
    
    def _calculate_optimization_score(self, query: str, estimated_rows: int) -> float:
        """Calculate query optimization score."""
        score = 1.0
        
        # Penalize long queries
        if len(query) > 1000:
            score -= 0.2
        
        # Penalize large result sets
        if estimated_rows > self.optimization_rules['max_result_size']:
            score -= 0.3
        
        # Penalize SELECT *
        if 'SELECT *' in query.upper():
            score -= 0.1
        
        return max(0.0, score)


class ResourceManager:
    """Resource management for analytics operations."""
    
    def __init__(self):
        self.resource_usage = {}
        self.resource_limits = {
            'memory_mb': 1024,
            'cpu_percent': 80,
            'disk_io_mbps': 100,
            'network_mbps': 50
        }
        self.lock = threading.RLock()
    
    def check_resource_availability(self, required_resources: Dict[str, float]) -> Tuple[bool, List[str]]:
        """Check if required resources are available."""
        with self.lock:
            available = True
            constraints = []
            
            for resource, required in required_resources.items():
                if resource in self.resource_limits:
                    current_usage = self.resource_usage.get(resource, 0)
                    if current_usage + required > self.resource_limits[resource]:
                        available = False
                        constraints.append(f"{resource} limit exceeded")
            
            return available, constraints
    
    def allocate_resources(self, resources: Dict[str, float]) -> bool:
        """Allocate resources for an operation."""
        with self.lock:
            available, constraints = self.check_resource_availability(resources)
            
            if available:
                for resource, amount in resources.items():
                    self.resource_usage[resource] = self.resource_usage.get(resource, 0) + amount
                return True
            else:
                logger.warning(f"Resource allocation failed: {constraints}")
                return False
    
    def release_resources(self, resources: Dict[str, float]) -> None:
        """Release allocated resources."""
        with self.lock:
            for resource, amount in resources.items():
                if resource in self.resource_usage:
                    self.resource_usage[resource] = max(0, self.resource_usage[resource] - amount)


class AnalyticsPerformanceOptimizer:
    """Main analytics performance optimizer."""
    
    def __init__(self):
        self.performance_metrics = PerformanceMetrics()
        self.cache_optimizer = CacheOptimizer()
        self.query_optimizer = QueryOptimizer()
        self.resource_manager = ResourceManager()
        self.optimization_stats = {
            'total_optimizations': 0,
            'performance_improvements': 0,
            'resource_optimizations': 0,
            'cache_optimizations': 0
        }
    
    def optimize_analytics_operation(self, operation_type: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize an analytics operation."""
        start_time = time.time()
        
        try:
            optimization_result = {
                "operation_type": operation_type,
                "optimization_timestamp": datetime.now().isoformat(),
                "optimizations_applied": [],
                "performance_improvements": {},
                "resource_usage": {}
            }
            
            # Cache optimization
            if "cache_key" in parameters:
                cache_result = self.cache_optimizer.get(parameters["cache_key"])
                if cache_result:
                    optimization_result["optimizations_applied"].append("cache_hit")
                    optimization_result["performance_improvements"]["cache_savings"] = "100%"
                else:
                    optimization_result["optimizations_applied"].append("cache_miss")
            
            # Query optimization
            if "query" in parameters:
                query_result = self.query_optimizer.optimize_query(
                    parameters["query"], 
                    parameters.get("estimated_rows", 1000)
                )
                optimization_result["optimizations_applied"].extend(
                    query_result["optimization_suggestions"]
                )
                optimization_result["performance_improvements"]["query_score"] = query_result["optimization_score"]
            
            # Resource optimization
            if "required_resources" in parameters:
                available, constraints = self.resource_manager.check_resource_availability(
                    parameters["required_resources"]
                )
                if available:
                    self.resource_manager.allocate_resources(parameters["required_resources"])
                    optimization_result["optimizations_applied"].append("resources_allocated")
                else:
                    optimization_result["optimizations_applied"].append(f"resource_constraints: {constraints}")
            
            # Record performance metrics
            execution_time = time.time() - start_time
            self.performance_metrics.record_metric("optimization_time", execution_time)
            self.performance_metrics.record_metric("operation_type", 1, datetime.now())
            
            optimization_result["execution_time_seconds"] = execution_time
            optimization_result["optimization_successful"] = True
            
            self.optimization_stats['total_optimizations'] += 1
            if execution_time < 1.0:  # Consider it a performance improvement
                self.optimization_stats['performance_improvements'] += 1
            
            return optimization_result
            
        except Exception as e:
            logger.error(f"Error optimizing analytics operation: {e}")
            return {
                "error": str(e),
                "operation_type": operation_type,
                "optimization_timestamp": datetime.now().isoformat(),
                "optimization_successful": False
            }
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Get comprehensive performance report."""
        try:
            # Get cache optimization stats
            cache_stats = self.cache_optimizer.optimize_cache()
            
            # Get performance metrics
            optimization_time_stats = self.performance_metrics.get_metric_stats("optimization_time")
            
            # Get resource usage
            resource_usage = dict(self.resource_manager.resource_usage)
            
            return {
                "performance_report": {
                    "optimization_stats": self.optimization_stats,
                    "cache_performance": cache_stats,
                    "optimization_times": optimization_time_stats,
                    "resource_usage": resource_usage,
                    "resource_limits": self.resource_manager.resource_limits
                },
                "recommendations": self._generate_performance_recommendations(cache_stats, optimization_time_stats),
                "generation_timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error generating performance report: {e}")
            return {"error": str(e)}
    
    def _generate_performance_recommendations(self, cache_stats: Dict[str, Any], 
                                            time_stats: Dict[str, Any]) -> List[str]:
        """Generate performance recommendations."""
        recommendations = []
        
        # Cache recommendations
        if cache_stats.get("hit_rate", 0) < 0.8:
            recommendations.append("Consider increasing cache size or improving cache key strategy")
        
        # Time-based recommendations
        if time_stats.get("avg", 0) > 2.0:
            recommendations.append("Optimization times are high - consider parallel processing")
        
        # Resource recommendations
        if self.resource_manager.resource_usage.get("memory_mb", 0) > 800:
            recommendations.append("Memory usage is high - consider memory optimization")
        
        return recommendations


# Global optimizer instance
_global_performance_optimizer = None


def get_analytics_performance_optimizer() -> AnalyticsPerformanceOptimizer:
    """Get global analytics performance optimizer."""
    global _global_performance_optimizer
    if _global_performance_optimizer is None:
        _global_performance_optimizer = AnalyticsPerformanceOptimizer()
    return _global_performance_optimizer


if __name__ == "__main__":
    # Example usage
    optimizer = get_analytics_performance_optimizer()
    
    # Test optimization
    result = optimizer.optimize_analytics_operation("data_analysis", {
        "cache_key": "test_analysis",
        "query": "SELECT * FROM large_table ORDER BY timestamp",
        "estimated_rows": 50000,
        "required_resources": {"memory_mb": 100, "cpu_percent": 20}
    })
    
    print(f"Optimization result: {result}")
    
    # Get performance report
    report = optimizer.get_performance_report()
    print(f"Performance report: {report}")
