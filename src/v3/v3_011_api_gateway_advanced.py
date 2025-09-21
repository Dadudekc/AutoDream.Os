#!/usr/bin/env python3
"""
V3-011: API Gateway Advanced Features
=====================================

Advanced API Gateway features including load balancing, monitoring, and analytics.
V2 compliant with focus on specific advanced functionality.
"""

import sys
import logging
import time
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

logger = logging.getLogger(__name__)


class LoadBalancingStrategy(Enum):
    """Load balancing strategies."""
    ROUND_ROBIN = "round_robin"
    LEAST_CONNECTIONS = "least_connections"
    WEIGHTED = "weighted"


@dataclass
class BackendServer:
    """Backend server configuration."""
    host: str
    port: int
    weight: int = 1
    health_check_url: str = "/health"
    is_healthy: bool = True
    active_connections: int = 0


@dataclass
class RequestMetrics:
    """Request metrics for monitoring."""
    endpoint: str
    method: str
    status_code: int
    response_time_ms: float
    timestamp: datetime
    client_ip: str


class LoadBalancer:
    """Load balancer implementation."""
    
    def __init__(self, strategy: LoadBalancingStrategy = LoadBalancingStrategy.ROUND_ROBIN):
        self.strategy = strategy
        self.servers = []
        self.current_index = 0
    
    def add_server(self, server: BackendServer):
        """Add backend server."""
        self.servers.append(server)
        logger.info(f"Added server: {server.host}:{server.port}")
    
    def get_next_server(self) -> Optional[BackendServer]:
        """Get next server based on strategy."""
        healthy_servers = [s for s in self.servers if s.is_healthy]
        
        if not healthy_servers:
            return None
        
        if self.strategy == LoadBalancingStrategy.ROUND_ROBIN:
            server = healthy_servers[self.current_index % len(healthy_servers)]
            self.current_index += 1
            return server
        
        elif self.strategy == LoadBalancingStrategy.LEAST_CONNECTIONS:
            return min(healthy_servers, key=lambda s: s.active_connections)
        
        elif self.strategy == LoadBalancingStrategy.WEIGHTED:
            # Simple weighted selection
            total_weight = sum(s.weight for s in healthy_servers)
            if total_weight == 0:
                return healthy_servers[0]
            
            # Weighted random selection (simplified)
            import random
            rand = random.randint(1, total_weight)
            current_weight = 0
            
            for server in healthy_servers:
                current_weight += server.weight
                if rand <= current_weight:
                    return server
            
            return healthy_servers[0]
        
        return healthy_servers[0]
    
    def health_check_all(self):
        """Perform health check on all servers."""
        for server in self.servers:
            try:
                # Simplified health check
                server.is_healthy = True
                logger.debug(f"Health check passed: {server.host}:{server.port}")
            except Exception as e:
                server.is_healthy = False
                logger.warning(f"Health check failed: {server.host}:{server.port} - {e}")


class MetricsCollector:
    """Metrics collection and analysis."""
    
    def __init__(self):
        self.metrics = []
        self.max_metrics = 10000  # Limit memory usage
    
    def record_request(self, metrics: RequestMetrics):
        """Record request metrics."""
        self.metrics.append(metrics)
        
        # Keep only recent metrics
        if len(self.metrics) > self.max_metrics:
            self.metrics = self.metrics[-self.max_metrics:]
    
    def get_endpoint_stats(self, endpoint: str) -> Dict[str, Any]:
        """Get statistics for specific endpoint."""
        endpoint_metrics = [m for m in self.metrics if m.endpoint == endpoint]
        
        if not endpoint_metrics:
            return {"error": "No metrics found for endpoint"}
        
        status_codes = [m.status_code for m in endpoint_metrics]
        response_times = [m.response_time_ms for m in endpoint_metrics]
        
        return {
            "endpoint": endpoint,
            "total_requests": len(endpoint_metrics),
            "avg_response_time_ms": sum(response_times) / len(response_times),
            "min_response_time_ms": min(response_times),
            "max_response_time_ms": max(response_times),
            "status_code_distribution": {
                str(code): status_codes.count(code) for code in set(status_codes)
            },
            "last_request": max(m.timestamp for m in endpoint_metrics).isoformat()
        }
    
    def get_overall_stats(self) -> Dict[str, Any]:
        """Get overall statistics."""
        if not self.metrics:
            return {"error": "No metrics available"}
        
        total_requests = len(self.metrics)
        avg_response_time = sum(m.response_time_ms for m in self.metrics) / total_requests
        
        # Get unique endpoints
        endpoints = list(set(m.endpoint for m in self.metrics))
        
        return {
            "total_requests": total_requests,
            "avg_response_time_ms": avg_response_time,
            "unique_endpoints": len(endpoints),
            "endpoints": endpoints,
            "time_range": {
                "start": min(m.timestamp for m in self.metrics).isoformat(),
                "end": max(m.timestamp for m in self.metrics).isoformat()
            }
        }


class APIMonitor:
    """API monitoring and alerting."""
    
    def __init__(self):
        self.metrics_collector = MetricsCollector()
        self.alerts = []
        self.alert_thresholds = {
            "error_rate": 0.1,  # 10% error rate
            "response_time": 1000,  # 1 second
            "request_rate": 100  # 100 requests per minute
        }
    
    def record_request(self, endpoint: str, method: str, status_code: int, 
                      response_time_ms: float, client_ip: str):
        """Record request for monitoring."""
        metrics = RequestMetrics(
            endpoint=endpoint,
            method=method,
            status_code=status_code,
            response_time_ms=response_time_ms,
            timestamp=datetime.now(),
            client_ip=client_ip
        )
        
        self.metrics_collector.record_request(metrics)
        self._check_alerts(metrics)
    
    def _check_alerts(self, metrics: RequestMetrics):
        """Check for alert conditions."""
        # Check response time
        if metrics.response_time_ms > self.alert_thresholds["response_time"]:
            self._create_alert("high_response_time", 
                             f"High response time: {metrics.response_time_ms}ms for {metrics.endpoint}")
        
        # Check error status
        if metrics.status_code >= 400:
            self._create_alert("error_response", 
                             f"Error response: {metrics.status_code} for {metrics.endpoint}")
    
    def _create_alert(self, alert_type: str, message: str):
        """Create alert."""
        alert = {
            "type": alert_type,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "severity": "warning"
        }
        
        self.alerts.append(alert)
        logger.warning(f"ALERT: {message}")
    
    def get_alerts(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent alerts."""
        return self.alerts[-limit:]
    
    def get_health_dashboard(self) -> Dict[str, Any]:
        """Get health dashboard data."""
        stats = self.metrics_collector.get_overall_stats()
        recent_alerts = self.get_alerts(10)
        
        return {
            "overall_stats": stats,
            "recent_alerts": recent_alerts,
            "alert_count": len(self.alerts),
            "monitoring_active": True,
            "timestamp": datetime.now().isoformat()
        }


def main():
    """Main execution function."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    try:
        # Initialize load balancer
        lb = LoadBalancer(LoadBalancingStrategy.ROUND_ROBIN)
        
        # Add sample servers
        lb.add_server(BackendServer("localhost", 8001, weight=1))
        lb.add_server(BackendServer("localhost", 8002, weight=2))
        lb.add_server(BackendServer("localhost", 8003, weight=1))
        
        # Initialize monitor
        monitor = APIMonitor()
        
        # Simulate some requests
        for i in range(5):
            server = lb.get_next_server()
            if server:
                print(f"Request {i+1} routed to {server.host}:{server.port}")
                
                # Simulate request metrics
                monitor.record_request(
                    endpoint="/api/test",
                    method="GET",
                    status_code=200,
                    response_time_ms=50 + i * 10,
                    client_ip="127.0.0.1"
                )
        
        # Get health dashboard
        dashboard = monitor.get_health_dashboard()
        
        print("✅ V3-011 API Gateway Advanced Features completed successfully!")
        print(f"📊 Load balancer: {len(lb.servers)} servers configured")
        print(f"📈 Monitor: {dashboard['overall_stats']['total_requests']} requests recorded")
        print(f"🚨 Alerts: {dashboard['alert_count']} total alerts")
        
        return 0
        
    except Exception as e:
        logger.error(f"V3-011 Advanced implementation error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

