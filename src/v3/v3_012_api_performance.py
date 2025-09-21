#!/usr/bin/env python3
"""
V3-012: API Performance Optimization
====================================

API performance monitoring and optimization with V2 compliance.
Focuses on performance tracking and optimization strategies.
"""

import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

from v3.v3_012_api_core import APIRequest, APIResponse, APIStatus


class PerformanceLevel(Enum):
    """Performance levels."""
    EXCELLENT = "excellent"
    GOOD = "good"
    ACCEPTABLE = "acceptable"
    POOR = "poor"
    CRITICAL = "critical"


@dataclass
class PerformanceMetric:
    """Performance metric structure."""
    metric_id: str
    request_id: str
    metric_name: str
    value: float
    unit: str
    timestamp: datetime
    level: PerformanceLevel


@dataclass
class PerformanceAlert:
    """Performance alert structure."""
    alert_id: str
    request_id: str
    metric_name: str
    threshold: float
    actual_value: float
    level: PerformanceLevel
    message: str
    triggered_at: datetime


class APIPerformanceMonitor:
    """API performance monitoring and optimization."""
    
    def __init__(self):
        self.metrics = []
        self.alerts = []
        self.performance_thresholds = {
            "response_time_ms": {"excellent": 100, "good": 300, "acceptable": 500, "poor": 1000},
            "throughput_rps": {"excellent": 100, "good": 50, "acceptable": 20, "poor": 10},
            "error_rate_percent": {"excellent": 1, "good": 5, "acceptable": 10, "poor": 20}
        }
    
    def track_request_performance(self, request: APIRequest, response: APIResponse):
        """Track request performance metrics."""
        # Response time metric
        self._add_metric(
            request.request_id, "response_time_ms", 
            response.response_time_ms, "ms", 
            self._get_performance_level("response_time_ms", response.response_time_ms)
        )
        
        # Success rate metric
        success_rate = 100.0 if response.status == APIStatus.SUCCESS else 0.0
        self._add_metric(
            request.request_id, "success_rate_percent", 
            success_rate, "%", 
            self._get_performance_level("error_rate_percent", 100 - success_rate)
        )
        
        # Check for performance alerts
        self._check_performance_alerts(request, response)
    
    def _add_metric(self, request_id: str, metric_name: str, value: float, 
                   unit: str, level: PerformanceLevel):
        """Add performance metric."""
        metric = PerformanceMetric(
            metric_id=f"{request_id}_{metric_name}_{int(datetime.now().timestamp())}",
            request_id=request_id,
            metric_name=metric_name,
            value=value,
            unit=unit,
            timestamp=datetime.now(),
            level=level
        )
        
        self.metrics.append(metric)
    
    def _get_performance_level(self, metric_name: str, value: float) -> PerformanceLevel:
        """Get performance level for metric value."""
        thresholds = self.performance_thresholds.get(metric_name, {})
        
        if value <= thresholds.get("excellent", 0):
            return PerformanceLevel.EXCELLENT
        elif value <= thresholds.get("good", 0):
            return PerformanceLevel.GOOD
        elif value <= thresholds.get("acceptable", 0):
            return PerformanceLevel.ACCEPTABLE
        elif value <= thresholds.get("poor", 0):
            return PerformanceLevel.POOR
        else:
            return PerformanceLevel.CRITICAL
    
    def _check_performance_alerts(self, request: APIRequest, response: APIResponse):
        """Check for performance alerts."""
        # Response time alert
        if response.response_time_ms > 1000:
            self._create_alert(
                request.request_id, "response_time_ms", 1000, 
                response.response_time_ms, PerformanceLevel.CRITICAL,
                f"High response time: {response.response_time_ms}ms"
            )
        
        # Error rate alert
        if response.status != APIStatus.SUCCESS:
            self._create_alert(
                request.request_id, "error_rate_percent", 10, 
                100, PerformanceLevel.POOR,
                f"Request failed: {response.status.value}"
            )
    
    def _create_alert(self, request_id: str, metric_name: str, threshold: float, 
                     actual_value: float, level: PerformanceLevel, message: str):
        """Create performance alert."""
        alert = PerformanceAlert(
            alert_id=f"{request_id}_{metric_name}_{int(datetime.now().timestamp())}",
            request_id=request_id,
            metric_name=metric_name,
            threshold=threshold,
            actual_value=actual_value,
            level=level,
            message=message,
            triggered_at=datetime.now()
        )
        
        self.alerts.append(alert)
        print(f"🚨 Performance Alert: {message}")
    
    def get_performance_summary(self, minutes: int = 5) -> Dict[str, Any]:
        """Get performance summary."""
        recent_metrics = self._get_recent_metrics(minutes)
        
        if not recent_metrics:
            return {"error": "No recent performance data"}
        
        # Calculate averages
        response_times = [m.value for m in recent_metrics if m.metric_name == "response_time_ms"]
        success_rates = [m.value for m in recent_metrics if m.metric_name == "success_rate_percent"]
        
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0
        avg_success_rate = sum(success_rates) / len(success_rates) if success_rates else 0
        
        # Count performance levels
        level_counts = {}
        for metric in recent_metrics:
            level = metric.level.value
            level_counts[level] = level_counts.get(level, 0) + 1
        
        return {
            "period_minutes": minutes,
            "total_metrics": len(recent_metrics),
            "average_response_time_ms": avg_response_time,
            "average_success_rate_percent": avg_success_rate,
            "performance_levels": level_counts,
            "active_alerts": len(self._get_active_alerts()),
            "timestamp": datetime.now().isoformat()
        }
    
    def _get_recent_metrics(self, minutes: int) -> List[PerformanceMetric]:
        """Get recent performance metrics."""
        cutoff_time = datetime.now() - timedelta(minutes=minutes)
        return [m for m in self.metrics if m.timestamp > cutoff_time]
    
    def _get_active_alerts(self) -> List[PerformanceAlert]:
        """Get active performance alerts."""
        # Return alerts from last 10 minutes
        cutoff_time = datetime.now() - timedelta(minutes=10)
        return [a for a in self.alerts if a.triggered_at > cutoff_time]
    
    def get_performance_recommendations(self) -> List[str]:
        """Get performance optimization recommendations."""
        recommendations = []
        recent_metrics = self._get_recent_metrics(5)
        
        if not recent_metrics:
            return ["No recent data for recommendations"]
        
        # Analyze response times
        response_times = [m.value for m in recent_metrics if m.metric_name == "response_time_ms"]
        if response_times:
            avg_response_time = sum(response_times) / len(response_times)
            if avg_response_time > 500:
                recommendations.append("Consider implementing caching to reduce response times")
            if avg_response_time > 1000:
                recommendations.append("Review database queries and optimize slow operations")
        
        # Analyze success rates
        success_rates = [m.value for m in recent_metrics if m.metric_name == "success_rate_percent"]
        if success_rates:
            avg_success_rate = sum(success_rates) / len(success_rates)
            if avg_success_rate < 95:
                recommendations.append("Investigate and fix API errors to improve success rate")
            if avg_success_rate < 90:
                recommendations.append("Implement better error handling and retry mechanisms")
        
        # Analyze performance levels
        critical_count = sum(1 for m in recent_metrics if m.level == PerformanceLevel.CRITICAL)
        if critical_count > 0:
            recommendations.append("Address critical performance issues immediately")
        
        if not recommendations:
            recommendations.append("Performance is within acceptable ranges")
        
        return recommendations


class APICache:
    """Simple API response caching."""
    
    def __init__(self, ttl_seconds: int = 300):
        self.cache = {}
        self.ttl_seconds = ttl_seconds
    
    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """Get cached response."""
        if key in self.cache:
            entry = self.cache[key]
            if datetime.now() < entry["expires_at"]:
                return entry["data"]
            else:
                del self.cache[key]
        return None
    
    def set(self, key: str, data: Dict[str, Any]):
        """Set cached response."""
        self.cache[key] = {
            "data": data,
            "expires_at": datetime.now() + timedelta(seconds=self.ttl_seconds)
        }
    
    def clear(self):
        """Clear cache."""
        self.cache.clear()
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        now = datetime.now()
        active_entries = sum(1 for entry in self.cache.values() if entry["expires_at"] > now)
        
        return {
            "total_entries": len(self.cache),
            "active_entries": active_entries,
            "expired_entries": len(self.cache) - active_entries,
            "ttl_seconds": self.ttl_seconds
        }


def main():
    """Main execution function."""
    print("⚡ V3-012 API Performance Optimization - Testing...")
    
    # Initialize performance monitor
    monitor = APIPerformanceMonitor()
    
    # Initialize cache
    cache = APICache(ttl_seconds=300)
    
    # Simulate API requests and responses
    from v3.v3_012_api_core import APIRequest, APIResponse, HTTPMethod, APIStatus
    
    # Create sample request
    request = APIRequest(
        request_id="test_001",
        method=HTTPMethod.GET,
        url="https://api.dreamos.com/users",
        headers={"Content-Type": "application/json"},
        data=None,
        timeout=30,
        retry_count=0,
        created_at=datetime.now()
    )
    
    # Create sample response
    response = APIResponse(
        request_id="test_001",
        status=APIStatus.SUCCESS,
        status_code=200,
        data={"users": [{"id": 1, "name": "Test User"}]},
        error_message=None,
        response_time_ms=150.5,
        created_at=datetime.now()
    )
    
    # Track performance
    monitor.track_request_performance(request, response)
    
    # Test caching
    cache.set("users", {"users": [{"id": 1, "name": "Test User"}]})
    cached_data = cache.get("users")
    
    # Get performance summary
    summary = monitor.get_performance_summary(5)
    recommendations = monitor.get_performance_recommendations()
    cache_stats = cache.get_cache_stats()
    
    print(f"\n📊 Performance Summary:")
    print(f"   Average Response Time: {summary['average_response_time_ms']:.2f}ms")
    print(f"   Average Success Rate: {summary['average_success_rate_percent']:.1f}%")
    print(f"   Active Alerts: {summary['active_alerts']}")
    
    print(f"\n💡 Recommendations:")
    for rec in recommendations:
        print(f"   - {rec}")
    
    print(f"\n🗄️ Cache Stats:")
    print(f"   Total Entries: {cache_stats['total_entries']}")
    print(f"   Active Entries: {cache_stats['active_entries']}")
    print(f"   TTL: {cache_stats['ttl_seconds']}s")
    
    print("\n✅ V3-012 API Performance Optimization completed successfully!")
    return 0


if __name__ == "__main__":
    exit(main())

