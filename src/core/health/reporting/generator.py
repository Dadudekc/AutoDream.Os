"""
Agent Health Reporting Generator Module

Single Responsibility: Generate health reports, dashboards, and analytics.
Follows V2 coding standards: Clean OOP design, SRP compliance, TDD approach.
"""

import json
import logging
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Set, Callable, Any, Union
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import pandas as pd
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ReportType(Enum):
    """Types of health reports"""
    DAILY_SUMMARY = "daily_summary"
    WEEKLY_ANALYSIS = "weekly_analysis"
    MONTHLY_TREND = "monthly_trend"
    INCIDENT_REPORT = "incident_report"
    PERFORMANCE_REVIEW = "performance_review"
    CUSTOM_RANGE = "custom_range"


class ReportFormat(Enum):
    """Output formats for reports"""
    JSON = "json"
    CSV = "csv"
    HTML = "html"
    PDF = "pdf"
    MARKDOWN = "markdown"
    CONSOLE = "console"


class ChartType(Enum):
    """Types of charts for visualization"""
    LINE_CHART = "line_chart"
    BAR_CHART = "bar_chart"
    PIE_CHART = "pie_chart"
    HEATMAP = "heatmap"
    SCATTER_PLOT = "scatter_plot"
    HISTOGRAM = "histogram"


@dataclass
class ReportConfig:
    """Configuration for report generation"""
    report_type: ReportType
    format: ReportFormat
    include_charts: bool = True
    include_metrics: bool = True
    include_alerts: bool = True
    include_recommendations: bool = True
    time_range: Optional[Dict[str, datetime]] = None
    agents: Optional[List[str]] = None
    custom_parameters: Dict[str, Any] = field(default_factory=dict)


@dataclass
class HealthReport:
    """Generated health report"""
    report_id: str
    report_type: ReportType
    format: ReportFormat
    generated_at: datetime
    time_range: Dict[str, datetime]
    summary: Dict[str, Any]
    metrics_data: Dict[str, Any]
    alerts_data: Dict[str, Any]
    charts: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ChartData:
    """Data for chart generation"""
    chart_type: ChartType
    title: str
    x_data: List[Any]
    y_data: List[Any]
    labels: Optional[List[str]] = None
    colors: Optional[List[str]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class HealthReportingGenerator:
    """
    Health reporting and analytics generation
    
    Single Responsibility: Generate comprehensive health reports, create
    visualizations, and provide analytics insights.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """Initialize the reporting generator"""
        self.config = config or {}
        self.reports_dir = Path(self.config.get("reports_dir", "health_reports"))
        self.charts_dir = Path(self.config.get("charts_dir", "health_charts"))
        self.templates_dir = Path(self.config.get("templates_dir", "report_templates"))
        
        # Create directories if they don't exist
        self.reports_dir.mkdir(exist_ok=True)
        self.charts_dir.mkdir(exist_ok=True)
        self.templates_dir.mkdir(exist_ok=True)
        
        # Report generation settings
        self.default_time_range = self.config.get("default_time_range", 24)  # hours
        self.max_data_points = self.config.get("max_data_points", 1000)
        self.chart_style = self.config.get("chart_style", "seaborn-v0_8")
        
        # Initialize matplotlib style
        try:
            plt.style.use(self.chart_style)
        except Exception:
            plt.style.use('default')
        
        logger.info("HealthReportingGenerator initialized")

    def generate_report(
        self,
        health_data: Dict[str, Any],
        alerts_data: Dict[str, Any],
        config: ReportConfig,
    ) -> HealthReport:
        """Generate a comprehensive health report"""
        try:
            logger.info(f"Generating {config.report_type.value} report...")
            
            # Generate unique report ID
            report_id = f"health_report_{config.report_type.value}_{int(time.time())}"
            
            # Determine time range
            time_range = self._determine_time_range(config)
            
            # Generate report sections
            summary = self._generate_summary(health_data, alerts_data, time_range)
            metrics_data = self._generate_metrics_data(health_data, time_range)
            alerts_data_section = self._generate_alerts_data(alerts_data, time_range)
            
            # Generate charts if requested
            charts = []
            if config.include_charts:
                charts = self._generate_charts(health_data, alerts_data, time_range, config)
            
            # Generate recommendations
            recommendations = []
            if config.include_recommendations:
                recommendations = self._generate_recommendations(health_data, alerts_data, summary)
            
            # Create report
            report = HealthReport(
                report_id=report_id,
                report_type=config.report_type,
                format=config.format,
                generated_at=datetime.now(),
                time_range=time_range,
                summary=summary,
                metrics_data=metrics_data,
                alerts_data=alerts_data_section,
                charts=charts,
                recommendations=recommendations,
                metadata={
                    "config": {
                        "report_type": config.report_type.value,
                        "format": config.format.value,
                        "include_charts": config.include_charts,
                        "include_metrics": config.include_metrics,
                        "include_alerts": config.include_alerts,
                        "include_recommendations": config.include_recommendations,
                        "time_range": config.time_range,
                    },
                    "generator_version": "1.0.0",
                },
            )
            
            # Save report
            self._save_report(report, config.format)
            
            logger.info(f"Report generated successfully: {report_id}")
            return report
            
        except Exception as e:
            logger.error(f"Error generating report: {e}")
            raise

    def _determine_time_range(self, config: ReportConfig) -> Dict[str, datetime]:
        """Determine the time range for the report"""
        end_time = datetime.now()
        
        if config.time_range:
            return config.time_range
        
        # Default time ranges based on report type
        if config.report_type == ReportType.DAILY_SUMMARY:
            start_time = end_time - timedelta(hours=24)
        elif config.report_type == ReportType.WEEKLY_ANALYSIS:
            start_time = end_time - timedelta(days=7)
        elif config.report_type == ReportType.MONTHLY_TREND:
            start_time = end_time - timedelta(days=30)
        else:
            start_time = end_time - timedelta(hours=self.default_time_range)
        
        return {
            "start": start_time,
            "end": end_time,
        }

    def _generate_summary(
        self,
        health_data: Dict[str, Any],
        alerts_data: Dict[str, Any],
        time_range: Dict[str, datetime],
    ) -> Dict[str, Any]:
        """Generate executive summary of health status"""
        try:
            # Count agents by health status
            status_counts = {}
            total_agents = 0
            avg_health_score = 0.0
            
            # Handle both dict and dataclass objects
            if hasattr(health_data, "agents"):
                # Dataclass object
                agents = health_data.agents
                total_agents = len(agents) if agents else 0
                
                for agent_id, agent_data in agents.items():
                    status = getattr(agent_data, "overall_status", "unknown")
                    status_counts[status] = status_counts.get(status, 0) + 1
                    
                    health_score = getattr(agent_data, "health_score", 0.0)
                    avg_health_score += health_score
            elif isinstance(health_data, dict) and "agents" in health_data:
                # Dictionary
                agents = health_data["agents"]
                total_agents = len(agents)
                
                for agent_id, agent_data in agents.items():
                    # Handle both dict and HealthSnapshot objects
                    if hasattr(agent_data, "overall_status"):
                        # HealthSnapshot object
                        status = getattr(agent_data, "overall_status", "unknown")
                        health_score = getattr(agent_data, "health_score", 0.0)
                    else:
                        # Dictionary
                        status = agent_data.get("overall_status", "unknown")
                        health_score = agent_data.get("health_score", 0.0)
                    
                    status_counts[status] = status_counts.get(status, 0) + 1
                    avg_health_score += health_score
                
            if total_agents > 0:
                avg_health_score /= total_agents
            
            # Count alerts by severity
            alert_counts = {}
            total_alerts = 0
            
            # Handle different data structures for alerts
            alerts = []
            
            if hasattr(alerts_data, "alerts"):
                # Dataclass object with alerts attribute
                alerts = alerts_data.alerts or []
            elif isinstance(alerts_data, dict):
                if "alerts" in alerts_data:
                    # Dictionary with alerts key
                    alerts = alerts_data["alerts"]
                elif isinstance(alerts_data.get("alerts", None), list):
                    # Direct list of alerts
                    alerts = alerts_data["alerts"]
                else:
                    # Try to treat the whole thing as a list of alerts
                    alerts = alerts_data if isinstance(alerts_data, list) else []
            elif isinstance(alerts_data, list):
                # Direct list of alerts
                alerts = alerts_data
            
            if alerts:
                total_alerts = len(alerts)
                
                for alert in alerts:
                    # Handle both dict and HealthAlert objects
                    if hasattr(alert, "severity"):
                        # HealthAlert object
                        severity = getattr(alert, "severity", "unknown")
                    else:
                        # Dictionary
                        severity = alert.get("severity", "unknown")
                    
                    alert_counts[severity] = alert_counts.get(severity, 0) + 1
            
            # Calculate overall health score
            overall_health = "excellent"
            if avg_health_score < 50:
                overall_health = "critical"
            elif avg_health_score < 70:
                overall_health = "poor"
            elif avg_health_score < 85:
                overall_health = "fair"
            elif avg_health_score < 95:
                overall_health = "good"
            
            return {
                "overall_health": overall_health,
                "total_agents": total_agents,
                "agents_by_status": status_counts,
                "average_health_score": round(avg_health_score, 2),
                "total_alerts": total_alerts,
                "alerts_by_severity": alert_counts,
                "time_range": {
                    "start": time_range["start"].isoformat(),
                    "end": time_range["end"].isoformat(),
                    "duration_hours": round((time_range["end"] - time_range["start"]).total_seconds() / 3600, 2),
                },
                "generated_at": datetime.now().isoformat(),
            }
            
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            return {"error": str(e)}

    def _generate_metrics_data(
        self,
        health_data: Dict[str, Any],
        time_range: Dict[str, datetime],
    ) -> Dict[str, Any]:
        """Generate detailed metrics data for the report"""
        try:
            metrics_data = {}
            
            # Handle both dict and dataclass objects
            if hasattr(health_data, "agents"):
                # Dataclass object
                agents = health_data.agents
                if agents:
                    for agent_id, agent_data in agents.items():
                        agent_metrics = {
                            "overall_status": getattr(agent_data, "overall_status", "unknown"),
                            "health_score": getattr(agent_data, "health_score", 0.0),
                            "last_update": getattr(agent_data, "timestamp", ""),
                            "metrics": {},
                        }
                        
                        # Extract individual metrics
                        if hasattr(agent_data, "metrics") and agent_data.metrics:
                            for metric_type, metric_data in agent_data.metrics.items():
                                agent_metrics["metrics"][metric_type] = {
                                    "value": getattr(metric_data, "value", 0.0),
                                    "unit": getattr(metric_data, "unit", ""),
                                    "status": getattr(metric_data, "status", "unknown"),
                                    "timestamp": getattr(metric_data, "timestamp", ""),
                                }
                        
                        metrics_data[agent_id] = agent_metrics
            elif isinstance(health_data, dict) and "agents" in health_data:
                # Dictionary
                agents = health_data["agents"]
                
                for agent_id, agent_data in agents.items():
                    # Handle both dict and HealthSnapshot objects
                    if hasattr(agent_data, "overall_status"):
                        # HealthSnapshot object
                        agent_metrics = {
                            "overall_status": getattr(agent_data, "overall_status", "unknown"),
                            "health_score": getattr(agent_data, "health_score", 0.0),
                            "last_update": getattr(agent_data, "timestamp", ""),
                            "metrics": {},
                        }
                        
                        # Extract individual metrics
                        if hasattr(agent_data, "metrics") and agent_data.metrics:
                            for metric_type, metric_data in agent_data.metrics.items():
                                agent_metrics["metrics"][metric_type] = {
                                    "value": getattr(metric_data, "value", 0.0),
                                    "unit": getattr(metric_data, "unit", ""),
                                    "status": getattr(metric_data, "status", "unknown"),
                                    "timestamp": getattr(metric_data, "timestamp", ""),
                                }
                    else:
                        # Dictionary
                        agent_metrics = {
                            "overall_status": agent_data.get("overall_status", "unknown"),
                            "health_score": agent_data.get("health_score", 0.0),
                            "last_update": agent_data.get("timestamp", ""),
                            "metrics": {},
                        }
                        
                        # Extract individual metrics
                        if "metrics" in agent_data:
                            for metric_type, metric_data in agent_data["metrics"].items():
                                agent_metrics["metrics"][metric_type] = {
                                    "value": metric_data.get("value", 0.0),
                                    "unit": metric_data.get("unit", ""),
                                    "status": metric_data.get("status", "unknown"),
                                    "timestamp": metric_data.get("timestamp", ""),
                                }
                    
                    metrics_data[agent_id] = agent_metrics
            
            return metrics_data
            
        except Exception as e:
            logger.error(f"Error generating metrics data: {e}")
            return {"error": str(e)}

    def _generate_alerts_data(
        self,
        alerts_data: Dict[str, Any],
        time_range: Dict[str, datetime],
    ) -> Dict[str, Any]:
        """Generate alerts data for the report"""
        try:
            alerts_summary = {
                "total_alerts": 0,
                "alerts_by_severity": {},
                "alerts_by_agent": {},
                "recent_alerts": [],
                "escalated_alerts": [],
            }
            
            # Handle different data structures
            alerts = []
            
            if hasattr(alerts_data, "alerts"):
                # Dataclass object with alerts attribute
                alerts = alerts_data.alerts or []
            elif isinstance(alerts_data, dict):
                if "alerts" in alerts_data:
                    # Dictionary with alerts key
                    alerts = alerts_data["alerts"]
                elif isinstance(alerts_data.get("alerts", None), list):
                    # Direct list of alerts
                    alerts = alerts_data["alerts"]
                else:
                    # Try to treat the whole thing as a list of alerts
                    alerts = alerts_data if isinstance(alerts_data, list) else []
            elif isinstance(alerts_data, list):
                # Direct list of alerts
                alerts = alerts_data
            
            if alerts:
                alerts_summary["total_alerts"] = len(alerts)
                
                for alert in alerts:
                    # Handle both dict and HealthAlert objects
                    if hasattr(alert, "severity"):
                        # HealthAlert object
                        severity = getattr(alert, "severity", "unknown")
                        agent_id = getattr(alert, "agent_id", "unknown")
                        alert_time = getattr(alert, "timestamp", datetime.now())
                        escalation_level = getattr(alert, "escalation_level", "level_1")
                    else:
                        # Dictionary
                        severity = alert.get("severity", "unknown")
                        agent_id = alert.get("agent_id", "unknown")
                        alert_time = alert.get("timestamp", datetime.now())
                        escalation_level = alert.get("escalation_level", "level_1")
                    
                    # Count by severity
                    alerts_summary["alerts_by_severity"][severity] = alerts_summary["alerts_by_severity"].get(severity, 0) + 1
                    
                    # Count by agent
                    alerts_summary["alerts_by_agent"][agent_id] = alerts_summary["alerts_by_agent"].get(agent_id, 0) + 1
                    
                    # Check if recent
                    if isinstance(alert_time, str):
                        try:
                            alert_time = datetime.fromisoformat(alert_time)
                        except:
                            alert_time = datetime.now()
                    if alert_time >= time_range["start"]:
                        alerts_summary["recent_alerts"].append(alert)
                    
                    # Check if escalated
                    if escalation_level != "level_1":
                        alerts_summary["escalated_alerts"].append(alert)
            
            return alerts_summary
            
        except Exception as e:
            logger.error(f"Error generating alerts data: {e}")
            return {"error": str(e)}

    def _generate_charts(
        self,
        health_data: Dict[str, Any],
        alerts_data: Dict[str, Any],
        time_range: Dict[str, datetime],
        config: ReportConfig,
    ) -> List[str]:
        """Generate charts for the report"""
        try:
            charts = []
            
            # Health score trend chart
            health_score_chart = self._create_health_score_chart(health_data, time_range)
            if health_score_chart:
                charts.append(health_score_chart)
            
            # Status distribution chart
            status_dist_chart = self._create_status_distribution_chart(health_data)
            if status_dist_chart:
                charts.append(status_dist_chart)
            
            # Alerts timeline chart
            alerts_chart = self._create_alerts_timeline_chart(alerts_data, time_range)
            if alerts_chart:
                charts.append(alerts_chart)
            
            # Metrics comparison chart
            metrics_chart = self._create_metrics_comparison_chart(health_data)
            if metrics_chart:
                charts.append(metrics_chart)
            
            return charts
            
        except Exception as e:
            logger.error(f"Error generating charts: {e}")
            return []

    def _create_health_score_chart(
        self,
        health_data: Dict[str, Any],
        time_range: Dict[str, datetime],
    ) -> Optional[str]:
        """Create health score trend chart"""
        try:
            if "agents" not in health_data:
                return None
            
            # Prepare data for plotting
            timestamps = []
            health_scores = []
            agent_labels = []
            
            agents = health_data["agents"]
            for agent_id, agent_data in agents.items():
                timestamp_str = agent_data.get("timestamp", "")
                if timestamp_str:
                    try:
                        timestamp = datetime.fromisoformat(timestamp_str)
                        if time_range["start"] <= timestamp <= time_range["end"]:
                            timestamps.append(timestamp)
                            health_scores.append(agent_data.get("health_score", 0.0))
                            agent_labels.append(agent_id)
                    except ValueError:
                        continue
            
            if not timestamps:
                return None
            
            # Create chart
            plt.figure(figsize=(12, 6))
            plt.plot(timestamps, health_scores, marker='o', linestyle='-', linewidth=2, markersize=6)
            
            # Customize chart
            plt.title("Agent Health Scores Over Time", fontsize=16, fontweight='bold')
            plt.xlabel("Time", fontsize=12)
            plt.ylabel("Health Score", fontsize=12)
            plt.grid(True, alpha=0.3)
            
            # Format x-axis
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
            plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=1))
            plt.xticks(rotation=45)
            
            # Add value labels
            for i, (timestamp, score, label) in enumerate(zip(timestamps, health_scores, agent_labels)):
                plt.annotate(f"{label}\n{score:.1f}", 
                            (timestamp, score), 
                            textcoords="offset points", 
                            xytext=(0,10), 
                            ha='center',
                            fontsize=8)
            
            plt.tight_layout()
            
            # Save chart
            chart_path = self.charts_dir / f"health_scores_{int(time.time())}.png"
            plt.savefig(chart_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            return str(chart_path)
            
        except Exception as e:
            logger.error(f"Error creating health score chart: {e}")
            return None

    def _create_status_distribution_chart(self, health_data: Dict[str, Any]) -> Optional[str]:
        """Create status distribution pie chart"""
        try:
            if "agents" not in health_data:
                return None
            
            # Count agents by status
            status_counts = {}
            agents = health_data["agents"]
            
            for agent_data in agents.values():
                status = agent_data.get("overall_status", "unknown")
                status_counts[status] = status_counts.get(status, 0) + 1
            
            if not status_counts:
                return None
            
            # Create chart
            plt.figure(figsize=(10, 8))
            
            # Define colors for different statuses
            colors = {
                "excellent": "#2E8B57",  # Sea Green
                "good": "#32CD32",       # Lime Green
                "warning": "#FFD700",    # Gold
                "critical": "#DC143C",   # Crimson
                "offline": "#696969",    # Dim Gray
                "unknown": "#C0C0C0",    # Silver
            }
            
            # Prepare data
            labels = list(status_counts.keys())
            sizes = list(status_counts.values())
            chart_colors = [colors.get(status, "#C0C0C0") for status in labels]
            
            # Create pie chart
            wedges, texts, autotexts = plt.pie(sizes, labels=labels, colors=chart_colors, 
                                              autopct='%1.1f%%', startangle=90)
            
            # Customize chart
            plt.title("Agent Health Status Distribution", fontsize=16, fontweight='bold')
            
            # Enhance text appearance
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
            
            for text in texts:
                text.set_fontsize(12)
            
            plt.axis('equal')
            plt.tight_layout()
            
            # Save chart
            chart_path = self.charts_dir / f"status_distribution_{int(time.time())}.png"
            plt.savefig(chart_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            return str(chart_path)
            
        except Exception as e:
            logger.error(f"Error creating status distribution chart: {e}")
            return None

    def _create_alerts_timeline_chart(
        self,
        alerts_data: Dict[str, Any],
        time_range: Dict[str, datetime],
    ) -> Optional[str]:
        """Create alerts timeline chart"""
        try:
            if "alerts" not in alerts_data:
                return None
            
            alerts = alerts_data["alerts"]
            if not alerts:
                return None
            
            # Prepare data for plotting
            alert_times = []
            alert_severities = []
            
            for alert in alerts:
                timestamp_str = alert.get("timestamp", "")
                if timestamp_str:
                    try:
                        timestamp = datetime.fromisoformat(timestamp_str)
                        if time_range["start"] <= timestamp <= time_range["end"]:
                            alert_times.append(timestamp)
                            alert_severities.append(alert.get("severity", "unknown"))
                    except ValueError:
                        continue
            
            if not alert_times:
                return None
            
            # Create chart
            plt.figure(figsize=(14, 8))
            
            # Define severity colors
            severity_colors = {
                "info": "#3498db",      # Blue
                "warning": "#f39c12",   # Orange
                "critical": "#e74c3c",  # Red
                "emergency": "#8e44ad", # Purple
            }
            
            # Plot alerts by time
            for severity in set(alert_severities):
                severity_times = [time for time, sev in zip(alert_times, alert_severities) if sev == severity]
                if severity_times:
                    plt.scatter(severity_times, [severity] * len(severity_times), 
                               c=severity_colors.get(severity, "#95a5a6"),
                               s=100, alpha=0.7, label=severity.title())
            
            # Customize chart
            plt.title("Alerts Timeline", fontsize=16, fontweight='bold')
            plt.xlabel("Time", fontsize=12)
            plt.ylabel("Severity", fontsize=12)
            plt.grid(True, alpha=0.3)
            plt.legend()
            
            # Format x-axis
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
            plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=1))
            plt.xticks(rotation=45)
            
            plt.tight_layout()
            
            # Save chart
            chart_path = self.charts_dir / f"alerts_timeline_{int(time.time())}.png"
            plt.savefig(chart_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            return str(chart_path)
            
        except Exception as e:
            logger.error(f"Error creating alerts timeline chart: {e}")
            return None

    def _create_metrics_comparison_chart(self, health_data: Dict[str, Any]) -> Optional[str]:
        """Create metrics comparison bar chart"""
        try:
            if "agents" not in health_data:
                return None
            
            agents = health_data["agents"]
            if not agents:
                return None
            
            # Prepare data for plotting
            agent_ids = []
            cpu_usage = []
            memory_usage = []
            
            for agent_id, agent_data in agents.items():
                agent_ids.append(agent_id)
                
                # Extract CPU and memory usage
                cpu_val = 0.0
                memory_val = 0.0
                
                if "metrics" in agent_data:
                    metrics = agent_data["metrics"]
                    if "cpu_usage" in metrics:
                        cpu_val = metrics["cpu_usage"].get("value", 0.0)
                    if "memory_usage" in metrics:
                        memory_val = metrics["memory_usage"].get("value", 0.0)
                
                cpu_usage.append(cpu_val)
                memory_usage.append(memory_val)
            
            if not agent_ids:
                return None
            
            # Create chart
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
            
            # CPU usage chart
            x_pos = range(len(agent_ids))
            bars1 = ax1.bar(x_pos, cpu_usage, color='#3498db', alpha=0.7)
            ax1.set_title("CPU Usage by Agent", fontsize=14, fontweight='bold')
            ax1.set_ylabel("CPU Usage (%)", fontsize=12)
            ax1.set_xticks(x_pos)
            ax1.set_xticklabels(agent_ids, rotation=45)
            ax1.grid(True, alpha=0.3)
            
            # Add value labels on bars
            for bar, value in zip(bars1, cpu_usage):
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width()/2., height + 1,
                        f'{value:.1f}%', ha='center', va='bottom')
            
            # Memory usage chart
            bars2 = ax2.bar(x_pos, memory_usage, color='#e74c3c', alpha=0.7)
            ax2.set_title("Memory Usage by Agent", fontsize=14, fontweight='bold')
            ax2.set_ylabel("Memory Usage (%)", fontsize=12)
            ax2.set_xticks(x_pos)
            ax2.set_xticklabels(agent_ids, rotation=45)
            ax2.grid(True, alpha=0.3)
            
            # Add value labels on bars
            for bar, value in zip(bars2, memory_usage):
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2., height + 1,
                        f'{value:.1f}%', ha='center', va='bottom')
            
            plt.tight_layout()
            
            # Save chart
            chart_path = self.charts_dir / f"metrics_comparison_{int(time.time())}.png"
            plt.savefig(chart_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            return str(chart_path)
            
        except Exception as e:
            logger.error(f"Error creating metrics comparison chart: {e}")
            return None

    def _generate_recommendations(
        self,
        health_data: Dict[str, Any],
        alerts_data: Dict[str, Any],
        summary: Dict[str, Any],
    ) -> List[str]:
        """Generate actionable recommendations based on health data"""
        recommendations = []
        
        try:
            # Check overall health score
            avg_health_score = summary.get("average_health_score", 100.0)
            if avg_health_score < 70:
                recommendations.append("Overall system health is poor. Immediate attention required.")
            elif avg_health_score < 85:
                recommendations.append("System health needs improvement. Review and optimize performance.")
            
            # Check for critical alerts
            critical_alerts = summary.get("alerts_by_severity", {}).get("critical", 0)
            if critical_alerts > 0:
                recommendations.append(f"Address {critical_alerts} critical alerts immediately.")
            
            # Check for offline agents
            offline_agents = summary.get("agents_by_status", {}).get("offline", 0)
            if offline_agents > 0:
                recommendations.append(f"Investigate {offline_agents} offline agents.")
            
            # Check for high resource usage
            high_cpu_agents = []
            high_memory_agents = []
            
            # Handle both dict and dataclass objects
            if hasattr(health_data, "agents"):
                # Dataclass object
                agents = health_data.agents
                if agents:
                    for agent_id, agent_data in agents.items():
                        if hasattr(agent_data, "metrics") and agent_data.metrics:
                            metrics = agent_data.metrics
                            
                            # Check CPU usage
                            if hasattr(metrics, "cpu_usage") and metrics.cpu_usage:
                                cpu_val = getattr(metrics.cpu_usage, "value", 0.0)
                                if cpu_val > 90:
                                    high_cpu_agents.append(agent_id)
                            
                            # Check memory usage
                            if hasattr(metrics, "memory_usage") and metrics.memory_usage:
                                memory_val = getattr(metrics.memory_usage, "value", 0.0)
                                if memory_val > 90:
                                    high_memory_agents.append(agent_id)
            elif isinstance(health_data, dict) and "agents" in health_data:
                # Dictionary
                agents = health_data["agents"]
                for agent_id, agent_data in agents.items():
                    # Handle both dict and HealthSnapshot objects
                    if hasattr(agent_data, "metrics"):
                        # HealthSnapshot object
                        metrics = agent_data.metrics
                        
                        # Check CPU usage
                        if hasattr(metrics, "cpu_usage") and metrics.cpu_usage:
                            cpu_val = getattr(metrics.cpu_usage, "value", 0.0)
                            if cpu_val > 90:
                                high_cpu_agents.append(agent_id)
                        
                        # Check memory usage
                        if hasattr(metrics, "memory_usage") and metrics.memory_usage:
                            memory_val = getattr(metrics.memory_usage, "value", 0.0)
                            if memory_val > 90:
                                high_memory_agents.append(agent_id)
                    elif "metrics" in agent_data:
                        # Dictionary
                        metrics = agent_data["metrics"]
                        
                        # Check CPU usage
                        if "cpu_usage" in metrics:
                            cpu_val = metrics["cpu_usage"].get("value", 0.0)
                            if cpu_val > 90:
                                high_cpu_agents.append(agent_id)
                        
                        # Check memory usage
                        if "memory_usage" in metrics:
                            memory_val = metrics["memory_usage"].get("value", 0.0)
                            if memory_val > 90:
                                high_memory_agents.append(agent_id)
            
            if high_cpu_agents:
                recommendations.append(f"High CPU usage detected on agents: {', '.join(high_cpu_agents)}")
            
            if high_memory_agents:
                recommendations.append(f"High memory usage detected on agents: {', '.join(high_memory_agents)}")
            
            # Add general recommendations
            if not recommendations:
                recommendations.append("System health is good. Continue monitoring and maintenance.")
            
            recommendations.append("Review alert thresholds and adjust if necessary.")
            recommendations.append("Schedule regular health checkups and maintenance.")
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            recommendations.append("Error generating recommendations. Check system logs.")
        
        return recommendations

    def _save_report(self, report: HealthReport, format: ReportFormat):
        """Save the report in the specified format"""
        try:
            if format == ReportFormat.JSON:
                self._save_json_report(report)
            elif format == ReportFormat.CSV:
                self._save_csv_report(report)
            elif format == ReportFormat.HTML:
                self._save_html_report(report)
            elif format == ReportFormat.MARKDOWN:
                self._save_markdown_report(report)
            elif format == ReportFormat.CONSOLE:
                self._save_console_report(report)
            else:
                logger.warning(f"Unsupported format: {format}")
                
        except Exception as e:
            logger.error(f"Error saving report: {e}")

    def _save_json_report(self, report: HealthReport):
        """Save report as JSON"""
        report_path = self.reports_dir / f"{report.report_id}.json"
        
        try:
            # Create a clean dictionary for JSON serialization
            report_dict = {
                "report_id": report.report_id,
                "report_type": report.report_type.value,
                "format": report.format.value,
                "generated_at": report.generated_at.isoformat(),
                "time_range": {
                    "start": report.time_range["start"].isoformat(),
                    "end": report.time_range["end"].isoformat(),
                },
                "summary": report.summary,
                "metrics_data": report.metrics_data,
                "alerts_data": report.alerts_data,
                "charts": report.charts,
                "recommendations": report.recommendations,
                "metadata": report.metadata,
            }
            
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(report_dict, f, indent=2, ensure_ascii=False)
            
            logger.info(f"JSON report saved: {report_path}")
            
        except Exception as e:
            logger.error(f"Error saving JSON report: {e}")
            # Try to save a minimal version
            try:
                minimal_dict = {
                    "report_id": report.report_id,
                    "report_type": str(report.report_type),
                    "format": str(report.format),
                    "generated_at": str(report.generated_at),
                    "error": "Full report could not be serialized",
                }
                with open(report_path, 'w', encoding='utf-8') as f:
                    json.dump(minimal_dict, f, indent=2, ensure_ascii=False)
                logger.info(f"Minimal JSON report saved: {report_path}")
            except Exception as e2:
                logger.error(f"Failed to save even minimal report: {e2}")

    def _save_csv_report(self, report: HealthReport):
        """Save report as CSV"""
        report_path = self.reports_dir / f"{report.report_id}.csv"
        
        # Create CSV data
        csv_data = []
        
        # Summary section
        csv_data.append(["SUMMARY"])
        for key, value in report.summary.items():
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    csv_data.append([f"{key}.{sub_key}", sub_value])
            else:
                csv_data.append([key, value])
        
        csv_data.append([])  # Empty row
        
        # Metrics section
        csv_data.append(["METRICS"])
        for agent_id, agent_data in report.metrics_data.items():
            csv_data.append([f"Agent: {agent_id}"])
            for metric_type, metric_data in agent_data.get("metrics", {}).items():
                csv_data.append([f"  {metric_type}", metric_data.get("value", ""), metric_data.get("unit", "")])
        
        # Save CSV
        import csv
        with open(report_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(csv_data)
        
        logger.info(f"CSV report saved: {report_path}")

    def _save_html_report(self, report: HealthReport):
        """Save report as HTML"""
        report_path = self.reports_dir / f"{report.report_id}.html"
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Health Report - {report.report_type.value}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background-color: #f0f0f0; padding: 20px; border-radius: 5px; }}
        .section {{ margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }}
        .metric {{ margin: 10px 0; padding: 10px; background-color: #f9f9f9; }}
        .chart {{ text-align: center; margin: 20px 0; }}
        .recommendation {{ background-color: #fff3cd; padding: 10px; margin: 10px 0; border-left: 4px solid #ffc107; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Health Report</h1>
        <p><strong>Type:</strong> {report.report_type.value}</p>
        <p><strong>Generated:</strong> {report.generated_at.strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p><strong>Time Range:</strong> {report.time_range['start'].strftime('%Y-%m-%d %H:%M:%S')} to {report.time_range['end'].strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    <div class="section">
        <h2>Summary</h2>
        <p><strong>Overall Health:</strong> {report.summary.get('overall_health', 'Unknown')}</p>
        <p><strong>Total Agents:</strong> {report.summary.get('total_agents', 0)}</p>
        <p><strong>Average Health Score:</strong> {report.summary.get('average_health_score', 0.0)}</p>
        <p><strong>Total Alerts:</strong> {report.summary.get('total_alerts', 0)}</p>
    </div>
    
    <div class="section">
        <h2>Recommendations</h2>
        {''.join([f'<div class="recommendation">{rec}</div>' for rec in report.recommendations])}
    </div>
    
    <div class="section">
        <h2>Charts</h2>
        {''.join([f'<div class="chart"><img src="{chart}" alt="Chart" style="max-width: 100%; height: auto;"></div>' for chart in report.charts])}
    </div>
</body>
</html>
        """
        
        with open(report_path, 'w') as f:
            f.write(html_content)
        
        logger.info(f"HTML report saved: {report_path}")

    def _save_markdown_report(self, report: HealthReport):
        """Save report as Markdown"""
        report_path = self.reports_dir / f"{report.report_id}.md"
        
        markdown_content = f"""# Health Report

**Type:** {report.report_type.value}  
**Generated:** {report.generated_at.strftime('%Y-%m-%d %H:%M:%S')}  
**Time Range:** {report.time_range['start'].strftime('%Y-%m-%d %H:%M:%S')} to {report.time_range['end'].strftime('%Y-%m-%d %H:%M:%S')}

## Summary

- **Overall Health:** {report.summary.get('overall_health', 'Unknown')}
- **Total Agents:** {report.summary.get('total_agents', 0)}
- **Average Health Score:** {report.summary.get('average_health_score', 0.0)}
- **Total Alerts:** {report.summary.get('total_alerts', 0)}

## Recommendations

{chr(10).join([f'- {rec}' for rec in report.recommendations])}

## Charts

{chr(10).join([f'![Chart]({chart})' for chart in report.charts])}
        """
        
        with open(report_path, 'w') as f:
            f.write(markdown_content)
        
        logger.info(f"Markdown report saved: {report_path}")

    def _save_console_report(self, report: HealthReport):
        """Display report in console"""
        print("\n" + "="*80)
        print("HEALTH REPORT")
        print("="*80)
        print(f"Type: {report.report_type.value}")
        print(f"Generated: {report.generated_at.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Time Range: {report.time_range['start'].strftime('%Y-%m-%d %H:%M:%S')} to {report.time_range['end'].strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        print("SUMMARY:")
        print(f"  Overall Health: {report.summary.get('overall_health', 'Unknown')}")
        print(f"  Total Agents: {report.summary.get('total_agents', 0)}")
        print(f"  Average Health Score: {report.summary.get('average_health_score', 0.0)}")
        print(f"  Total Alerts: {report.summary.get('total_alerts', 0)}")
        print()
        
        print("RECOMMENDATIONS:")
        for rec in report.recommendations:
            print(f"  - {rec}")
        print()
        
        if report.charts:
            print("CHARTS GENERATED:")
            for chart in report.charts:
                print(f"  - {chart}")
        
        print("="*80)

    def get_report_history(self, limit: int = 50) -> List[HealthReport]:
        """Get history of generated reports"""
        try:
            reports = []
            json_files = list(self.reports_dir.glob("*.json"))
            
            # Sort by modification time (newest first)
            json_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            
            for json_file in json_files[:limit]:
                try:
                    with open(json_file, 'r') as f:
                        report_data = json.load(f)
                    
                    # Reconstruct datetime objects
                    report_data["generated_at"] = datetime.fromisoformat(report_data["generated_at"])
                    report_data["time_range"]["start"] = datetime.fromisoformat(report_data["time_range"]["start"])
                    report_data["time_range"]["end"] = datetime.fromisoformat(report_data["time_range"]["end"])
                    
                    report = HealthReport(**report_data)
                    reports.append(report)
                    
                except Exception as e:
                    logger.warning(f"Error loading report {json_file}: {e}")
                    continue
            
            return reports
            
        except Exception as e:
            logger.error(f"Error getting report history: {e}")
            return []

    def cleanup_old_reports(self, days_to_keep: int = 30):
        """Clean up old reports and charts"""
        try:
            cutoff_time = datetime.now() - timedelta(days=days_to_keep)
            
            # Clean up old reports
            json_files = list(self.reports_dir.glob("*.json"))
            for json_file in json_files:
                if json_file.stat().st_mtime < cutoff_time.timestamp():
                    json_file.unlink()
                    logger.info(f"Removed old report: {json_file}")
            
            # Clean up old charts
            chart_files = list(self.charts_dir.glob("*.png"))
            for chart_file in chart_files:
                if chart_file.stat().st_mtime < cutoff_time.timestamp():
                    chart_file.unlink()
                    logger.info(f"Removed old chart: {chart_file}")
                    
        except Exception as e:
            logger.error(f"Error cleaning up old reports: {e}")

    def run_smoke_test(self) -> bool:
        """Run smoke test to verify basic functionality"""
        try:
            logger.info("Running HealthReportingGenerator smoke test...")

            # Test basic initialization
            logger.info("Testing basic initialization...")
            assert self.reports_dir.exists()
            assert self.charts_dir.exists()
            assert self.templates_dir.exists()
            logger.info("Basic initialization passed")

            # Test report generation with mock data
            logger.info("Testing report generation...")
            mock_health_data = {
                "agents": {
                    "agent_1": {
                        "overall_status": "good",
                        "health_score": 85.0,
                        "timestamp": datetime.now().isoformat(),
                        "metrics": {
                            "cpu_usage": {"value": 45.0, "unit": "%", "status": "good"},
                            "memory_usage": {"value": 60.0, "unit": "%", "status": "good"},
                        }
                    }
                }
            }
            
            mock_alerts_data = {
                "alerts": [
                    {
                        "severity": "warning",
                        "agent_id": "agent_1",
                        "timestamp": datetime.now().isoformat(),
                        "message": "Test alert"
                    }
                ]
            }
            
            config = ReportConfig(
                report_type=ReportType.DAILY_SUMMARY,
                format=ReportFormat.JSON,
                include_charts=True,
                include_metrics=True,
                include_alerts=True,
                include_recommendations=True,
            )
            
            report = self.generate_report(mock_health_data, mock_alerts_data, config)
            assert report is not None
            assert report.report_id.startswith("health_report_")
            logger.info("Report generation passed")

            # Test chart generation
            logger.info("Testing chart generation...")
            assert len(report.charts) > 0, "No charts were generated"
            logger.info("Chart generation passed")

            # Test recommendations generation
            logger.info("Testing recommendations generation...")
            assert len(report.recommendations) > 0, "No recommendations were generated"
            logger.info("Recommendations generation passed")

            # Test report history
            logger.info("Testing report history...")
            history = self.get_report_history(limit=5)
            assert len(history) > 0, "No reports found in history"
            logger.info("Report history passed")

            # Cleanup test files
            logger.info("Cleaning up test files...")
            if report.report_id in [r.report_id for r in history]:
                # Remove test report
                test_report_file = self.reports_dir / f"{report.report_id}.json"
                if test_report_file.exists():
                    test_report_file.unlink()
            
            # Remove test charts
            for chart_path in report.charts:
                chart_file = Path(chart_path)
                if chart_file.exists():
                    chart_file.unlink()

            logger.info("✅ HealthReportingGenerator smoke test PASSED")
            return True

        except Exception as e:
            logger.error(f"❌ HealthReportingGenerator smoke test FAILED: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return False

    def shutdown(self):
        """Shutdown the reporting generator"""
        logger.info("HealthReportingGenerator shutdown complete")


def main():
    """CLI testing function"""
    import argparse

    parser = argparse.ArgumentParser(description="Health Reporting Generator CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    parser.add_argument("--cleanup", type=int, metavar="DAYS", help="Clean up reports older than DAYS days")

    args = parser.parse_args()

    generator = HealthReportingGenerator()

    if args.test:
        success = generator.run_smoke_test()
        generator.shutdown()
        exit(0 if success else 1)
    elif args.cleanup:
        generator.cleanup_old_reports(args.cleanup)
        generator.shutdown()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
