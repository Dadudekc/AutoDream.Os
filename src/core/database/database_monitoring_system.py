#!/usr/bin/env python3
"""
V3-003: Database Monitoring System - Modular Entry Point
=======================================================

Modular database monitoring system using component architecture.
V2 Compliant: ≤400 lines, single responsibility, KISS principle.
"""

import asyncio
import logging
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import asdict

from .monitoring import (
    MetricsCollector, 
    HealthChecker, 
    AlertManager,
    DatabaseMetric,
    HealthCheck,
    Alert,
    HealthStatus
)

logger = logging.getLogger(__name__)


class DatabaseMonitoringSystem:
    """Modular database monitoring system."""
    
    def __init__(self):
        """Initialize modular database monitoring system."""
        self.metrics: List[DatabaseMetric] = []
        self.health_checks: List[HealthCheck] = []
        self.is_running = False
        self.monitoring_tasks: Dict[str, asyncio.Task] = {}
        
        # Initialize components
        self.metrics_collector = MetricsCollector()
        self.health_checker = HealthChecker()
        self.alert_manager = AlertManager()
        
        logger.info("📊 Modular Database Monitoring System initialized")
    
    async def start_monitoring(self) -> bool:
        """Start database monitoring."""
        try:
            self.is_running = True
            self.monitoring_tasks["cleanup"] = asyncio.create_task(self._cleanup_old_data())
            logger.info("✅ Database monitoring started")
            return True
        except Exception as e:
            logger.error(f"❌ Error starting monitoring: {e}")
            return False
    
    async def stop_monitoring(self) -> bool:
        """Stop database monitoring."""
        try:
            self.is_running = False
            for task in self.monitoring_tasks.values():
                task.cancel()
            self.monitoring_tasks.clear()
            logger.info("✅ Database monitoring stopped")
            return True
        except Exception as e:
            logger.error(f"❌ Error stopping monitoring: {e}")
            return False
    
    async def collect_metrics(self, node_config: Dict[str, Any]) -> List[DatabaseMetric]:
        """Collect metrics from a database node."""
        try:
            metrics = await self.metrics_collector.collect_metrics(node_config)
            self.metrics.extend(metrics)
            
            # Check for alerts
            new_alerts = await self.alert_manager.check_metrics_for_alerts(metrics)
            
            logger.debug(f"📊 Collected {len(metrics)} metrics from node: {node_config['node_id']}")
            return metrics
            
        except Exception as e:
            logger.error(f"❌ Error collecting metrics: {e}")
            return []
    
    async def perform_health_check(self, node_config: Dict[str, Any]) -> HealthCheck:
        """Perform health check on a database node."""
        try:
            health_check = await self.health_checker.perform_health_check(node_config)
            self.health_checks.append(health_check)
            return health_check
        except Exception as e:
            logger.error(f"❌ Error performing health check: {e}")
            return HealthCheck(
                check_name="error",
                status=HealthStatus.UNHEALTHY,
                message=f"Health check failed: {e}",
                timestamp=datetime.now(timezone.utc),
                response_time_ms=0.0
            )
    
    async def get_monitoring_dashboard(self) -> Dict[str, Any]:
        """Get monitoring dashboard data."""
        try:
            dashboard = {
                "system_status": {
                    "is_running": self.is_running,
                    "total_metrics": len(self.metrics),
                    "total_health_checks": len(self.health_checks),
                    "health_status": self._get_overall_health_status()
                },
                "recent_metrics": self._get_recent_metrics(limit=100),
                "active_alerts": await self.alert_manager.get_active_alerts(),
                "health_summary": self._get_health_summary(),
                "performance_summary": self._get_performance_summary()
            }
            
            return dashboard
            
        except Exception as e:
            logger.error(f"❌ Error getting monitoring dashboard: {e}")
            return {"error": str(e)}
    
    async def _cleanup_old_data(self):
        """Clean up old monitoring data."""
        try:
            while self.is_running:
                await asyncio.sleep(3600)  # Run every hour
                
                # Clean up old metrics (keep last 1000)
                if len(self.metrics) > 1000:
                    self.metrics = self.metrics[-1000:]
                
                # Clean up old health checks (keep last 500)
                if len(self.health_checks) > 500:
                    self.health_checks = self.health_checks[-500:]
                
                # Clean up old alerts
                await self.alert_manager.cleanup_old_alerts(hours=24)
                
                logger.debug("🧹 Cleaned up old monitoring data")
                
        except asyncio.CancelledError:
            logger.info("🔄 Cleanup task cancelled")
        except Exception as e:
            logger.error(f"❌ Error in cleanup task: {e}")
    
    def _get_overall_health_status(self) -> str:
        """Get overall health status."""
        if not self.health_checks:
            return "unknown"
        
        recent_checks = [h for h in self.health_checks 
                        if h.timestamp > datetime.now(timezone.utc) - timedelta(minutes=5)]
        
        if not recent_checks:
            return "unknown"
        
        unhealthy_count = len([h for h in recent_checks if h.status == HealthStatus.UNHEALTHY])
        degraded_count = len([h for h in recent_checks if h.status == HealthStatus.DEGRADED])
        
        if unhealthy_count > 0:
            return "unhealthy"
        elif degraded_count > 0:
            return "degraded"
        else:
            return "healthy"
    
    def _get_recent_metrics(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent metrics."""
        recent_metrics = sorted(self.metrics, key=lambda x: x.timestamp, reverse=True)[:limit]
        return [asdict(metric) for metric in recent_metrics]
    
    def _get_health_summary(self) -> Dict[str, Any]:
        """Get health summary."""
        recent_checks = [h for h in self.health_checks 
                        if h.timestamp > datetime.now(timezone.utc) - timedelta(minutes=10)]
        
        summary = {
            "total_checks": len(recent_checks),
            "healthy": len([h for h in recent_checks if h.status == HealthStatus.HEALTHY]),
            "degraded": len([h for h in recent_checks if h.status == HealthStatus.DEGRADED]),
            "unhealthy": len([h for h in recent_checks if h.status == HealthStatus.UNHEALTHY]),
            "unknown": len([h for h in recent_checks if h.status == HealthStatus.UNKNOWN])
        }
        
        return summary
    
    def _get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary."""
        recent_metrics = [m for m in self.metrics 
                         if m.timestamp > datetime.now(timezone.utc) - timedelta(minutes=10)]
        
        if not recent_metrics:
            return {"error": "No recent metrics available"}
        
        summary = {
            "total_metrics": len(recent_metrics),
            "metrics_by_type": {},
            "average_response_time": 0.0
        }
        
        # Group metrics by type
        for metric in recent_metrics:
            metric_type = metric.metric_type.value
            if metric_type not in summary["metrics_by_type"]:
                summary["metrics_by_type"][metric_type] = 0
            summary["metrics_by_type"][metric_type] += 1
        
        return summary
