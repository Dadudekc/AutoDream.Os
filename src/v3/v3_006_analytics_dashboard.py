"""
V3-006 Analytics Dashboard
Interactive performance visualization and monitoring dashboard
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

class ChartType(Enum):
    """Types of dashboard charts"""
    LINE_CHART = "line"
    BAR_CHART = "bar"
    PIE_CHART = "pie"
    GAUGE = "gauge"
    TABLE = "table"

@dataclass
class DashboardWidget:
    """Dashboard widget configuration"""
    widget_id: str
    title: str
    chart_type: ChartType
    data_source: str
    refresh_interval: int = 30  # seconds
    position: Dict[str, int] = None
    size: Dict[str, int] = None
    
    def __post_init__(self):
        if self.position is None:
            self.position = {"x": 0, "y": 0}
        if self.size is None:
            self.size = {"width": 300, "height": 200}

class AnalyticsDashboard:
    """Main analytics dashboard system"""
    
    def __init__(self):
        self.widgets: List[DashboardWidget] = []
        self.data_cache: Dict[str, Any] = {}
        self.last_refresh = {}
        self.default_widgets = self._create_default_widgets()
        
    def _create_default_widgets(self) -> List[DashboardWidget]:
        """Create default dashboard widgets"""
        return [
            DashboardWidget(
                widget_id="cpu_usage",
                title="CPU Usage",
                chart_type=ChartType.GAUGE,
                data_source="performance.cpu_usage",
                refresh_interval=5,
                position={"x": 0, "y": 0},
                size={"width": 300, "height": 200}
            ),
            DashboardWidget(
                widget_id="memory_usage",
                title="Memory Usage",
                chart_type=ChartType.GAUGE,
                data_source="performance.memory_usage",
                refresh_interval=5,
                position={"x": 320, "y": 0},
                size={"width": 300, "height": 200}
            ),
            DashboardWidget(
                widget_id="disk_io",
                title="Disk I/O",
                chart_type=ChartType.LINE_CHART,
                data_source="performance.disk_io",
                refresh_interval=10,
                position={"x": 0, "y": 220},
                size={"width": 620, "height": 200}
            ),
            DashboardWidget(
                widget_id="network_io",
                title="Network I/O",
                chart_type=ChartType.LINE_CHART,
                data_source="performance.network_io",
                refresh_interval=10,
                position={"x": 0, "y": 440},
                size={"width": 620, "height": 200}
            ),
            DashboardWidget(
                widget_id="alerts",
                title="Recent Alerts",
                chart_type=ChartType.TABLE,
                data_source="performance.alerts",
                refresh_interval=15,
                position={"x": 640, "y": 0},
                size={"width": 400, "height": 300}
            )
        ]
    
    def add_widget(self, widget: DashboardWidget):
        """Add widget to dashboard"""
        self.widgets.append(widget)
        
    def remove_widget(self, widget_id: str):
        """Remove widget from dashboard"""
        self.widgets = [w for w in self.widgets if w.widget_id != widget_id]
        
    def get_widget_data(self, widget_id: str, performance_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get data for specific widget"""
        widget = next((w for w in self.widgets if w.widget_id == widget_id), None)
        if not widget:
            return {}
            
        # Check if data needs refresh
        now = datetime.now()
        last_refresh = self.last_refresh.get(widget_id, datetime.min)
        
        if (now - last_refresh).seconds < widget.refresh_interval:
            return self.data_cache.get(widget_id, {})
            
        # Generate widget data based on type
        data = self._generate_widget_data(widget, performance_data)
        
        # Cache the data
        self.data_cache[widget_id] = data
        self.last_refresh[widget_id] = now
        
        return data
        
    def _generate_widget_data(self, widget: DashboardWidget, performance_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate data for widget based on type and data source"""
        data = {
            "widget_id": widget.widget_id,
            "title": widget.title,
            "chart_type": widget.chart_type.value,
            "timestamp": datetime.now().isoformat()
        }
        
        if widget.chart_type == ChartType.GAUGE:
            data.update(self._generate_gauge_data(widget, performance_data))
        elif widget.chart_type == ChartType.LINE_CHART:
            data.update(self._generate_line_chart_data(widget, performance_data))
        elif widget.chart_type == ChartType.TABLE:
            data.update(self._generate_table_data(widget, performance_data))
            
        return data
        
    def _generate_gauge_data(self, widget: DashboardWidget, performance_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate gauge chart data"""
        value = self._get_data_value(widget.data_source, performance_data)
        
        return {
            "value": value,
            "max_value": 100,
            "unit": "%",
            "color": self._get_gauge_color(value)
        }
        
    def _generate_line_chart_data(self, widget: DashboardWidget, performance_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate line chart data"""
        # Simulate historical data for line charts
        data_points = []
        base_value = self._get_data_value(widget.data_source, performance_data)
        
        for i in range(20):  # Last 20 data points
            timestamp = datetime.now() - timedelta(minutes=i)
            value = base_value + (i * 0.1)  # Simulate trend
            data_points.append({
                "timestamp": timestamp.isoformat(),
                "value": value
            })
            
        return {
            "data_points": data_points,
            "unit": "bytes/s",
            "color": "#3498db"
        }
        
    def _generate_table_data(self, widget: DashboardWidget, performance_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate table data"""
        alerts = performance_data.get("recent_alerts", [])
        
        return {
            "headers": ["Type", "Value", "Threshold", "Time"],
            "rows": [
                [
                    alert.get("type", ""),
                    f"{alert.get('value', 0):.1f}",
                    f"{alert.get('threshold', 0):.1f}",
                    alert.get("timestamp", "")[:19]  # Remove microseconds
                ]
                for alert in alerts[:10]  # Show last 10 alerts
            ]
        }
        
    def _get_data_value(self, data_source: str, performance_data: Dict[str, Any]) -> float:
        """Get value from data source path"""
        try:
            parts = data_source.split(".")
            value = performance_data
            for part in parts:
                value = value[part]
            return float(value)
        except (KeyError, TypeError, ValueError):
            return 0.0
            
    def _get_gauge_color(self, value: float) -> str:
        """Get color for gauge based on value"""
        if value < 50:
            return "#2ecc71"  # Green
        elif value < 80:
            return "#f39c12"  # Orange
        else:
            return "#e74c3c"  # Red
            
    def get_dashboard_config(self) -> Dict[str, Any]:
        """Get complete dashboard configuration"""
        return {
            "dashboard_id": "v3_performance_dashboard",
            "title": "V3 Performance Analytics Dashboard",
            "refresh_interval": 30,
            "widgets": [
                {
                    "widget_id": widget.widget_id,
                    "title": widget.title,
                    "chart_type": widget.chart_type.value,
                    "data_source": widget.data_source,
                    "refresh_interval": widget.refresh_interval,
                    "position": widget.position,
                    "size": widget.size
                }
                for widget in self.widgets
            ],
            "created_at": datetime.now().isoformat(),
            "version": "1.0.0"
        }
        
    def render_dashboard(self, performance_data: Dict[str, Any]) -> Dict[str, Any]:
        """Render complete dashboard with data"""
        dashboard_data = {
            "config": self.get_dashboard_config(),
            "data": {},
            "timestamp": datetime.now().isoformat()
        }
        
        # Get data for each widget
        for widget in self.widgets:
            dashboard_data["data"][widget.widget_id] = self.get_widget_data(
                widget.widget_id, performance_data
            )
            
        return dashboard_data

class DashboardManager:
    """Dashboard management and API"""
    
    def __init__(self):
        self.dashboard = AnalyticsDashboard()
        self.dashboard.widgets = self.dashboard.default_widgets
        
    def get_dashboard(self, performance_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get rendered dashboard"""
        return self.dashboard.render_dashboard(performance_data)
        
    def add_custom_widget(self, widget_config: Dict[str, Any]):
        """Add custom widget to dashboard"""
        widget = DashboardWidget(
            widget_id=widget_config["widget_id"],
            title=widget_config["title"],
            chart_type=ChartType(widget_config["chart_type"]),
            data_source=widget_config["data_source"],
            refresh_interval=widget_config.get("refresh_interval", 30),
            position=widget_config.get("position", {"x": 0, "y": 0}),
            size=widget_config.get("size", {"width": 300, "height": 200})
        )
        self.dashboard.add_widget(widget)
        
    def export_dashboard_config(self, filepath: str):
        """Export dashboard configuration to file"""
        config = self.dashboard.get_dashboard_config()
        with open(filepath, 'w') as f:
            json.dump(config, f, indent=2)
            
    def import_dashboard_config(self, filepath: str):
        """Import dashboard configuration from file"""
        with open(filepath, 'r') as f:
            config = json.load(f)
            
        # Clear existing widgets
        self.dashboard.widgets = []
        
        # Add widgets from config
        for widget_config in config.get("widgets", []):
            self.add_custom_widget(widget_config)

# Global dashboard manager instance
dashboard_manager = DashboardManager()

def get_performance_dashboard(performance_data: Dict[str, Any]) -> Dict[str, Any]:
    """Get performance analytics dashboard"""
    return dashboard_manager.get_dashboard(performance_data)

def add_dashboard_widget(widget_config: Dict[str, Any]):
    """Add widget to performance dashboard"""
    dashboard_manager.add_custom_widget(widget_config)

if __name__ == "__main__":
    # Test dashboard with sample data
    sample_data = {
        "cpu_usage": 45.2,
        "memory_usage": 67.8,
        "disk_io": 1024000,
        "network_io": 2048000,
        "recent_alerts": [
            {
                "type": "high_cpu",
                "value": 85.5,
                "threshold": 80.0,
                "timestamp": "2025-01-18T16:30:00"
            }
        ]
    }
    
    dashboard = get_performance_dashboard(sample_data)
    print(f"Dashboard: {json.dumps(dashboard, indent=2)}")


