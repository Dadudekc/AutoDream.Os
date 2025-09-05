"""
Dashboard Orchestrator
======================

Main orchestrator for performance dashboard operations.
V2 Compliance: < 300 lines, single responsibility, orchestration logic.

Author: Agent-3 - Infrastructure & DevOps Specialist
Mission: V2 Compliance Refactoring
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from .models import (
    PerformanceMetric, DashboardWidget, PerformanceAlert, DashboardConfig,
    PerformanceReport, MetricType, AlertLevel, DashboardStatus, DashboardModels
)
from .engine import DashboardEngine
from .reporter import DashboardReporter


class PerformanceDashboardOrchestrator:
    """Main orchestrator for performance dashboard system."""
    
    def __init__(self):
        """Initialize performance dashboard orchestrator."""
        self.engine = DashboardEngine()
        self.reporter = DashboardReporter(self.engine)
        self.logger = logging.getLogger(__name__)
        self.is_initialized = False
    
    async def initialize(self) -> bool:
        """Initialize the orchestrator."""
        try:
            self.logger.info("Initializing Performance Dashboard Orchestrator")
            
            # Initialize engine
            if not self.engine.initialize():
                raise Exception("Failed to initialize engine")
            
            # Initialize reporter
            if not self.reporter.initialize():
                raise Exception("Failed to initialize reporter")
            
            self.is_initialized = True
            self.logger.info("Performance Dashboard Orchestrator initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Performance Dashboard Orchestrator: {e}")
            return False
    
    async def add_metric(self, name: str, value: float, unit: str, 
                        metric_type: MetricType, tags: Dict[str, str] = None) -> bool:
        """Add performance metric."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        metric = DashboardModels.create_performance_metric(
            name=name,
            value=value,
            unit=unit,
            metric_type=metric_type,
            tags=tags
        )
        
        return self.engine.add_metric(metric)
    
    async def add_widget(self, name: str, widget_type: str, position: Dict[str, int],
                        size: Dict[str, int], config: Dict[str, Any],
                        data_source: str, refresh_interval: int = 30) -> bool:
        """Add dashboard widget."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        widget = DashboardModels.create_dashboard_widget(
            name=name,
            widget_type=widget_type,
            position=position,
            size=size,
            config=config,
            data_source=data_source,
            refresh_interval=refresh_interval
        )
        
        return self.engine.add_widget(widget)
    
    async def add_alert(self, metric_name: str, threshold: float, 
                       current_value: float, alert_level: AlertLevel,
                       message: str) -> bool:
        """Add performance alert."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        alert = DashboardModels.create_performance_alert(
            metric_name=metric_name,
            threshold=threshold,
            current_value=current_value,
            alert_level=alert_level,
            message=message
        )
        
        return self.engine.add_alert(alert)
    
    async def add_config(self, name: str, description: str, 
                        refresh_interval: int = 30, auto_refresh: bool = True,
                        theme: str = "default", layout: Dict[str, Any] = None,
                        widgets: List[str] = None) -> bool:
        """Add dashboard config."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        config = DashboardModels.create_dashboard_config(
            name=name,
            description=description,
            refresh_interval=refresh_interval,
            auto_refresh=auto_refresh,
            theme=theme,
            layout=layout,
            widgets=widgets
        )
        
        return self.engine.add_config(config)
    
    async def get_metrics(self, metric_type: MetricType = None, 
                         hours: int = 24) -> List[PerformanceMetric]:
        """Get performance metrics."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        if metric_type:
            return self.engine.get_metrics_by_type(metric_type)
        else:
            return self.engine.get_recent_metrics(hours)
    
    async def get_widgets(self, widget_type: str = None) -> List[DashboardWidget]:
        """Get dashboard widgets."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        if widget_type:
            return self.engine.get_widgets_by_type(widget_type)
        else:
            return list(self.engine.widgets.values())
    
    async def get_alerts(self, active_only: bool = True) -> List[PerformanceAlert]:
        """Get performance alerts."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        if active_only:
            return self.engine.get_active_alerts()
        else:
            return list(self.engine.alerts.values())
    
    async def acknowledge_alert(self, alert_id: str) -> bool:
        """Acknowledge alert."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return self.engine.acknowledge_alert(alert_id)
    
    async def generate_report(self, report_type: str = "summary", 
                             hours: int = 24, **kwargs) -> Dict[str, Any]:
        """Generate performance report."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        if report_type == "metrics":
            metric_type = kwargs.get('metric_type')
            return self.reporter.generate_metrics_report(metric_type, hours)
        elif report_type == "alerts":
            alert_level = kwargs.get('alert_level')
            return self.reporter.generate_alerts_report(alert_level, hours)
        elif report_type == "summary":
            return self.reporter.generate_summary_report(hours)
        else:
            raise ValueError(f"Unknown report type: {report_type}")
    
    async def export_report(self, report_data: Dict[str, Any], 
                           format: str = 'json') -> str:
        """Export report."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return self.reporter.export_report(report_data, format)
    
    async def save_report(self, report_data: Dict[str, Any], 
                         filename: str = None) -> str:
        """Save report to file."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return self.reporter.save_report(report_data, filename)
    
    async def get_dashboard_status(self) -> Dict[str, Any]:
        """Get dashboard status."""
        if not self.is_initialized:
            return {'status': 'not_initialized'}
        
        return self.engine.get_dashboard_data()
    
    async def get_report_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get report history."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return self.reporter.get_report_history(limit)
    
    async def cleanup_old_data(self, days: int = 7):
        """Cleanup old data."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        self.engine.cleanup_old_data(days)
        self.reporter.cleanup_old_reports(days)
    
    async def shutdown(self):
        """Shutdown orchestrator."""
        if not self.is_initialized:
            return
        
        self.logger.info("Shutting down Performance Dashboard Orchestrator")
        self.engine.shutdown()
        self.is_initialized = False
        self.logger.info("Performance Dashboard Orchestrator shutdown complete")
