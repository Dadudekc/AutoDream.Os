"""
Report Types - V2 Modular Architecture
======================================

Data structures for performance reports.
Follows V2 standards: OOP design, SRP, no strict LOC limits.

Author: V2 SWARM CAPTAIN
License: MIT
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum


class ReportFormat(Enum):
    """Report output formats."""
    JSON = "json"
    TEXT = "text"
    HTML = "html"
    CSV = "csv"


class ReportStatus(Enum):
    """Report generation status."""
    PENDING = "pending"
    GENERATING = "generating"
    COMPLETED = "completed"
    FAILED = "failed"


class MetricType(Enum):
    """Metric types for reporting."""
    GAUGE = "gauge"
    COUNTER = "counter"
    HISTOGRAM = "histogram"
    TIMER = "timer"


@dataclass
class ReportMetric:
    """Individual metric in a report."""
    name: str
    value: float
    unit: str
    metric_type: MetricType
    timestamp: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metric to dictionary."""
        return {
            "name": self.name,
            "value": self.value,
            "unit": self.unit,
            "metric_type": self.metric_type.value,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata
        }


@dataclass
class ReportSection:
    """Section within a performance report."""
    name: str
    title: str
    description: str
    metrics: List[ReportMetric] = field(default_factory=list)
    subsections: List['ReportSection'] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def add_metric(self, metric: ReportMetric):
        """Add a metric to this section."""
        self.metrics.append(metric)
    
    def add_subsection(self, subsection: 'ReportSection'):
        """Add a subsection to this section."""
        self.subsections.append(subsection)
    
    def get_metric(self, metric_name: str) -> Optional[ReportMetric]:
        """Get metric by name."""
        for metric in self.metrics:
            if metric.name == metric_name:
                return metric
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert section to dictionary."""
        return {
            "name": self.name,
            "title": self.title,
            "description": self.description,
            "metrics": [m.to_dict() for m in self.metrics],
            "subsections": [s.to_dict() for s in self.subsections],
            "metadata": self.metadata
        }


@dataclass
class PerformanceReport:
    """Complete performance report."""
    report_id: str
    title: str
    description: str
    timestamp: datetime
    sections: List[ReportSection] = field(default_factory=list)
    format: ReportFormat = ReportFormat.JSON
    status: ReportStatus = ReportStatus.PENDING
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def add_section(self, section: ReportSection):
        """Add a section to the report."""
        self.sections.append(section)
    
    def get_section(self, section_name: str) -> Optional[ReportSection]:
        """Get section by name."""
        for section in self.sections:
            if section.name == section_name:
                return section
        return None
    
    def get_summary_metrics(self) -> List[ReportMetric]:
        """Get all metrics from all sections."""
        metrics = []
        for section in self.sections:
            metrics.extend(section.metrics)
            # Recursively get metrics from subsections
            for subsection in section.subsections:
                metrics.extend(subsection.metrics)
        return metrics
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert report to dictionary."""
        return {
            "report_id": self.report_id,
            "title": self.title,
            "description": self.description,
            "timestamp": self.timestamp.isoformat(),
            "format": self.format.value,
            "status": self.status.value,
            "sections": [s.to_dict() for s in self.sections],
            "metadata": self.metadata
        }
