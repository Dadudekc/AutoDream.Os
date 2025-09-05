#!/usr/bin/env python3
"""
SSOT Models - KISS Compliant
============================

Simple data models for SSOT operations.

Author: Agent-5 - Business Intelligence Specialist
License: MIT
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from datetime import datetime

@dataclass
class SSOTComponent:
    """SSOT component definition."""
    component_id: str
    name: str
    type: str
    status: str = "active"
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

@dataclass
class SSOTExecution:
    """SSOT execution record."""
    execution_id: str
    phase: str
    status: str
    started_at: datetime = None
    completed_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.started_at is None:
            self.started_at = datetime.now()

@dataclass
class SSOTValidation:
    """SSOT validation result."""
    validation_id: str
    component_id: str
    level: str
    passed: bool
    message: str = ""
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

@dataclass
class SSOTConfiguration:
    """SSOT configuration."""
    config_id: str
    name: str
    value: Any
    component_type: str
    priority: str = "normal"
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

@dataclass
class SSOTMetrics:
    """SSOT performance metrics."""
    metrics_id: str
    component_id: str
    metric_name: str
    value: float
    unit: str = ""
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

@dataclass
class SSOTReport:
    """SSOT status report."""
    report_id: str
    title: str
    status: str
    components: List[SSOTComponent]
    executions: List[SSOTExecution]
    validations: List[SSOTValidation]
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

# Simple factory functions
def create_ssot_component(component_id: str, name: str, type: str) -> SSOTComponent:
    """Create SSOT component."""
    return SSOTComponent(component_id=component_id, name=name, type=type)

def create_ssot_execution(execution_id: str, phase: str, status: str) -> SSOTExecution:
    """Create SSOT execution."""
    return SSOTExecution(execution_id=execution_id, phase=phase, status=status)

def create_ssot_validation(validation_id: str, component_id: str, level: str, passed: bool) -> SSOTValidation:
    """Create SSOT validation."""
    return SSOTValidation(validation_id=validation_id, component_id=component_id, level=level, passed=passed)

def create_ssot_configuration(config_id: str, name: str, value: Any, component_type: str) -> SSOTConfiguration:
    """Create SSOT configuration."""
    return SSOTConfiguration(config_id=config_id, name=name, value=value, component_type=component_type)

def create_ssot_metrics(metrics_id: str, component_id: str, metric_name: str, value: float) -> SSOTMetrics:
    """Create SSOT metrics."""
    return SSOTMetrics(metrics_id=metrics_id, component_id=component_id, metric_name=metric_name, value=value)

def create_ssot_report(report_id: str, title: str, status: str, components: List[SSOTComponent], executions: List[SSOTExecution], validations: List[SSOTValidation]) -> SSOTReport:
    """Create SSOT report."""
    return SSOTReport(report_id=report_id, title=title, status=status, components=components, executions=executions, validations=validations)

__all__ = [
    "SSOTComponent", "SSOTExecution", "SSOTValidation", "SSOTConfiguration", 
    "SSOTMetrics", "SSOTReport",
    "create_ssot_component", "create_ssot_execution", "create_ssot_validation",
    "create_ssot_configuration", "create_ssot_metrics", "create_ssot_report"
]