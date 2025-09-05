"""
Dashboard Models
===============

Data models for performance dashboard operations.
V2 Compliance: < 300 lines, single responsibility, data modeling.

Author: Agent-3 - Infrastructure & DevOps Specialist
Mission: V2 Compliance Refactoring
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional, Union
from datetime import datetime, timedelta
from enum import Enum
import uuid


class DashboardStatus(Enum):
    """Dashboard status."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    MAINTENANCE = "maintenance"
    ERROR = "error"


class MetricType(Enum):
    """Metric type."""
    PERFORMANCE = "performance"
    MEMORY = "memory"
    CPU = "cpu"
    NETWORK = "network"
    DISK = "disk"
    CUSTOM = "custom"


class AlertLevel(Enum):
    """Alert level."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class PerformanceMetric:
    """Performance metric data."""
    metric_id: str
    name: str
    value: float
    unit: str
    metric_type: MetricType
    timestamp: datetime
    tags: Dict[str, str]
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class DashboardWidget:
    """Dashboard widget data."""
    widget_id: str
    name: str
    widget_type: str
    position: Dict[str, int]
    size: Dict[str, int]
    config: Dict[str, Any]
    data_source: str
    refresh_interval: int
    created_at: datetime
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class PerformanceAlert:
    """Performance alert data."""
    alert_id: str
    metric_name: str
    threshold: float
    current_value: float
    alert_level: AlertLevel
    message: str
    timestamp: datetime
    acknowledged: bool = False
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class DashboardConfig:
    """Dashboard configuration."""
    config_id: str
    name: str
    description: str
    refresh_interval: int
    auto_refresh: bool
    theme: str
    layout: Dict[str, Any]
    widgets: List[str]
    created_at: datetime
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class PerformanceReport:
    """Performance report data."""
    report_id: str
    title: str
    description: str
    metrics: List[PerformanceMetric]
    alerts: List[PerformanceAlert]
    summary: Dict[str, Any]
    generated_at: datetime
    period_start: datetime
    period_end: datetime
    
    def __post_init__(self):
        if self.generated_at is None:
            self.generated_at = datetime.now()


class DashboardModels:
    """Dashboard models and factory methods."""
    
    @staticmethod
    def create_performance_metric(
        name: str,
        value: float,
        unit: str,
        metric_type: MetricType,
        tags: Dict[str, str] = None
    ) -> PerformanceMetric:
        """Create performance metric."""
        return PerformanceMetric(
            metric_id=str(uuid.uuid4()),
            name=name,
            value=value,
            unit=unit,
            metric_type=metric_type,
            timestamp=datetime.now(),
            tags=tags or {}
        )
    
    @staticmethod
    def create_dashboard_widget(
        name: str,
        widget_type: str,
        position: Dict[str, int],
        size: Dict[str, int],
        config: Dict[str, Any],
        data_source: str,
        refresh_interval: int = 30
    ) -> DashboardWidget:
        """Create dashboard widget."""
        return DashboardWidget(
            widget_id=str(uuid.uuid4()),
            name=name,
            widget_type=widget_type,
            position=position,
            size=size,
            config=config,
            data_source=data_source,
            refresh_interval=refresh_interval,
            created_at=datetime.now()
        )
    
    @staticmethod
    def create_performance_alert(
        metric_name: str,
        threshold: float,
        current_value: float,
        alert_level: AlertLevel,
        message: str
    ) -> PerformanceAlert:
        """Create performance alert."""
        return PerformanceAlert(
            alert_id=str(uuid.uuid4()),
            metric_name=metric_name,
            threshold=threshold,
            current_value=current_value,
            alert_level=alert_level,
            message=message,
            timestamp=datetime.now()
        )
    
    @staticmethod
    def create_dashboard_config(
        name: str,
        description: str,
        refresh_interval: int = 30,
        auto_refresh: bool = True,
        theme: str = "default",
        layout: Dict[str, Any] = None,
        widgets: List[str] = None
    ) -> DashboardConfig:
        """Create dashboard config."""
        return DashboardConfig(
            config_id=str(uuid.uuid4()),
            name=name,
            description=description,
            refresh_interval=refresh_interval,
            auto_refresh=auto_refresh,
            theme=theme,
            layout=layout or {},
            widgets=widgets or [],
            created_at=datetime.now()
        )
    
    @staticmethod
    def create_performance_report(
        title: str,
        description: str,
        metrics: List[PerformanceMetric],
        alerts: List[PerformanceAlert],
        summary: Dict[str, Any],
        period_start: datetime,
        period_end: datetime
    ) -> PerformanceReport:
        """Create performance report."""
        return PerformanceReport(
            report_id=str(uuid.uuid4()),
            title=title,
            description=description,
            metrics=metrics,
            alerts=alerts,
            summary=summary,
            generated_at=datetime.now(),
            period_start=period_start,
            period_end=period_end
        )
    
    @staticmethod
    def validate_performance_metric(metric: PerformanceMetric) -> Dict[str, Any]:
        """Validate performance metric."""
        validation = {
            'is_valid': True,
            'warnings': [],
            'errors': []
        }
        
        if not metric.name:
            validation['errors'].append("Metric name is required")
            validation['is_valid'] = False
        
        if metric.value < 0:
            validation['warnings'].append("Negative metric value detected")
        
        if not metric.unit:
            validation['warnings'].append("Metric unit is recommended")
        
        return validation
    
    @staticmethod
    def validate_dashboard_widget(widget: DashboardWidget) -> Dict[str, Any]:
        """Validate dashboard widget."""
        validation = {
            'is_valid': True,
            'warnings': [],
            'errors': []
        }
        
        if not widget.name:
            validation['errors'].append("Widget name is required")
            validation['is_valid'] = False
        
        if not widget.widget_type:
            validation['errors'].append("Widget type is required")
            validation['is_valid'] = False
        
        if not widget.data_source:
            validation['warnings'].append("Data source is recommended")
        
        return validation
