#!/usr/bin/env python3
"""
SWARM HEALTH MONITOR - V2 COMPLIANT MODULE
==========================================

Main swarm health monitoring orchestrator.
V2 compliant version with modular architecture.

Author: Agent-4 (Strategic Oversight & Emergency Intervention Manager)
License: MIT
"""

from __future__ import annotations

import json
import logging
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List

from .health_metrics import SwarmHealthReport
from .health_monitor_core import HealthMonitorCore

logger = logging.getLogger(__name__)


class SwarmHealthMonitor:
    """V2 compliant swarm health monitoring system."""
    
    def __init__(self, monitoring_interval: int = 30):
        self.logger = logging.getLogger(__name__)
        self.monitoring_interval = monitoring_interval
        
        # Initialize core monitoring
        self.core = HealthMonitorCore()
        
        # Monitoring state
        self.is_monitoring = False
        self.monitoring_task = None
        
        # Start monitoring
        self._start_monitoring()
    
    def _start_monitoring(self):
        """Start continuous health monitoring."""
        import threading
        
        def monitoring_loop():
            while True:
                try:
                    self._perform_health_check()
                    time.sleep(self.monitoring_interval)
                except Exception as e:
                    self.logger.error(f"Health monitoring error: {e}")
                    time.sleep(60)  # Wait longer on error
        
        self.monitoring_task = threading.Thread(target=monitoring_loop, daemon=True)
        self.monitoring_task.start()
        self.is_monitoring = True
        self.logger.info("Swarm health monitoring started")
    
    def _perform_health_check(self):
        """Perform comprehensive health check."""
        import asyncio
        
        async def async_health_check():
            try:
                # Check agent health
                await self.core.check_agent_health()
                
                # Check system metrics
                await self.core.check_system_metrics()
                
                # Check routing health
                await self.core.check_routing_health()
                
                # Check messaging health
                await self.core.check_messaging_health()
                
                # Generate health report
                report = await self.core.generate_health_report()
                
                # Store report
                self.core.store_health_report(report)
                
                # Check for critical issues
                await self.core.check_critical_issues(report)
                
            except Exception as e:
                self.logger.error(f"Health check failed: {e}")
        
        # Run async health check
        asyncio.run(async_health_check())
    
    def get_current_health(self) -> SwarmHealthReport:
        """Get current health status."""
        return self.core.get_current_health()
    
    def get_health_history(self, hours: int = 24) -> List[SwarmHealthReport]:
        """Get health history for specified hours."""
        return self.core.get_health_history(hours)
    
    def export_health_report(self, filepath: str):
        """Export health report to file."""
        try:
            report = self.get_current_health()
            
            # Convert to serializable format
            report_data = {
                "timestamp": report.timestamp.isoformat(),
                "overall_health": report.overall_health,
                "health_score": report.health_score,
                "agent_statuses": {
                    agent_id: {
                        "agent_id": status.agent_id,
                        "is_online": status.is_online,
                        "last_heartbeat": status.last_heartbeat.isoformat(),
                        "response_time_ms": status.response_time_ms,
                        "consecutive_failures": status.consecutive_failures,
                        "health_score": status.health_score,
                        "status": status.status,
                        "last_error": status.last_error
                    }
                    for agent_id, status in report.agent_statuses.items()
                },
                "system_metrics": {
                    name: {
                        "name": metric.name,
                        "value": metric.value,
                        "unit": metric.unit,
                        "timestamp": metric.timestamp.isoformat(),
                        "threshold_warning": metric.threshold_warning,
                        "threshold_critical": metric.threshold_critical,
                        "status": metric.status
                    }
                    for name, metric in report.system_metrics.items()
                },
                "routing_health": report.routing_health,
                "messaging_health": report.messaging_health,
                "critical_issues": report.critical_issues,
                "recommendations": report.recommendations
            }
            
            # Write to file
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Health report exported to {filepath}")
            
        except Exception as e:
            self.logger.error(f"Failed to export health report: {e}")
    
    def stop_monitoring(self):
        """Stop health monitoring."""
        self.is_monitoring = False
        if self.monitoring_task:
            self.monitoring_task.join(timeout=5)
        self.logger.info("Swarm health monitoring stopped")


# Global swarm health monitor instance
_swarm_health_monitor = None


def get_swarm_health_monitor() -> SwarmHealthMonitor:
    """Get global swarm health monitor instance."""
    global _swarm_health_monitor
    if _swarm_health_monitor is None:
        _swarm_health_monitor = SwarmHealthMonitor()
    return _swarm_health_monitor


# Convenience functions
def get_current_swarm_health() -> SwarmHealthReport:
    """Get current swarm health status."""
    monitor = get_swarm_health_monitor()
    return monitor.get_current_health()


def export_swarm_health_report(filepath: str):
    """Export swarm health report to file."""
    monitor = get_swarm_health_monitor()
    monitor.export_health_report(filepath)


def get_swarm_health_history(hours: int = 24) -> List[SwarmHealthReport]:
    """Get swarm health history."""
    monitor = get_swarm_health_monitor()
    return monitor.get_health_history(hours)