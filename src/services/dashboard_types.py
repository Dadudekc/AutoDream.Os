#!/usr/bin/env python3
"""
Dashboard Types and Enums - V2 Dashboard System

This module contains all the data structures, enums, and types
for the dashboard frontend system.
Follows V2 coding standards: ≤200 LOC, OOP design, SRP
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, Any


class ChartType(Enum):
    """Types of charts available for dashboard widgets."""
    LINE = "line"
    BAR = "bar"
    PIE = "pie"
    GAUGE = "gauge"
    AREA = "area"
    SCATTER = "scatter"
    HISTOGRAM = "histogram"
    HEATMAP = "heatmap"
    TABLE = "table"


@dataclass
class DashboardWidget:
    """Dashboard widget configuration."""
    widget_id: str
    title: str
    chart_type: ChartType
    metric_name: str
    refresh_interval: int = 5  # seconds
    width: int = 6  # grid columns (1-12)
    height: int = 4  # grid rows
    position_x: int = 0
    position_y: int = 0
    options: Dict[str, Any] = field(default_factory=dict)
    filters: Dict[str, str] = field(default_factory=dict)
    aggregation: str = "raw"  # raw, avg, max, min, sum
    time_range: int = 3600  # seconds (1 hour default)


@dataclass
class DashboardLayout:
    """Dashboard layout configuration."""
    columns: int = 12
    rows: int = 8
    widget_spacing: int = 10
    responsive: bool = True
    theme: str = "dark"  # dark, light
    auto_refresh: bool = True
    refresh_interval: int = 5  # seconds


@dataclass
class DashboardConfig:
    """Dashboard configuration settings."""
    title: str = "Agent Cellphone V2 - Performance Dashboard"
    websocket_url: str = "ws://localhost:8080/ws"
    default_theme: str = "dark"
    default_refresh_interval: int = 5
    enable_notifications: bool = True
    enable_animations: bool = True



