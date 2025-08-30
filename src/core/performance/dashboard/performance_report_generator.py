#!/usr/bin/env python3
"""
Performance Report Generator - Stall Prevention Dashboard
=======================================================

Generates comprehensive performance reports for stall prevention systems.
Provides insights, trends, and optimization recommendations.

Author: Agent-6 - Performance Optimization Manager
License: MIT
"""

import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import asdict

logger = logging.getLogger(__name__)


class PerformanceReportGenerator:
    """Generates comprehensive performance reports"""
    
    def __init__(self, dashboard_data: Dict[str, Any]):
        self.dashboard_data = dashboard_data
        self.report_timestamp = datetime.now()
    
    def generate_full_report(self) -> Dict[str, Any]:
        """Generate comprehensive performance report"""
        try:
            report = {
                "report_metadata": self._generate_metadata(),
                "executive_summary": self._generate_executive_summary(),
                "performance_metrics": self._analyze_performance_metrics(),
                "health_analysis": self._analyze_system_health(),
                "alert_summary": self._analyze_alerts(),
                "trend_analysis": self._analyze_trends(),
                "optimization_recommendations": self._generate_recommendations(),
                "action_items": self._generate_action_items()
            }
            
            return report
            
        except Exception as e:
            logger.error(f"Error generating full report: {e}")
            return {"error": str(e)}
    
    def _generate_metadata(self) -> Dict[str, Any]:
        """Generate report metadata"""
        return {
            "report_id": f"PERF-{int(datetime.now().timestamp())}",
            "generated_at": self.report_timestamp.isoformat(),
            "report_type": "Stall Prevention Performance Report",
            "data_source": "Stall Prevention Dashboard",
            "time_range": "Last 24 hours",
            "generator": "Agent-6 Performance Report Generator"
        }
    
    def _generate_executive_summary(self) -> Dict[str, Any]:
        """Generate executive summary"""
        try:
            overall_health = self.dashboard_data.get("overall_health_score", 0.5)
            total_alerts = len(self.dashboard_data.get("alerts", []))
            critical_alerts = len([a for a in self.dashboard_data.get("alerts", []) 
                                if a.get("severity") == "critical"])
            
            summary = {
                "overall_system_health": f"{overall_health:.1%}",
                "health_status": self._get_health_status(overall_health),
                "total_alerts": total_alerts,
                "critical_alerts": critical_alerts,
                "system_uptime": f"{self.dashboard_data.get('uptime_seconds', 0) / 3600:.1f} hours",
                "performance_rating": self._get_performance_rating(overall_health),
                "key_findings": self._get_key_findings(overall_health, critical_alerts)
            }
            
            return summary
            
        except Exception as e:
            logger.error(f"Error generating executive summary: {e}")
            return {"error": str(e)}
    
    def _analyze_performance_metrics(self) -> Dict[str, Any]:
        """Analyze performance metrics"""
        try:
            metrics = self.dashboard_data.get("stall_metrics", [])
            if not metrics:
                return {"status": "No metrics available"}
            
            # Group metrics by name
            metric_groups = {}
            for metric in metrics:
                name = metric.get("name")
                if name not in metric_groups:
                    metric_groups[name] = []
                metric_groups[name].append(metric)
            
            analysis = {}
            for metric_name, metric_list in metric_groups.items():
                values = [m.get("value", 0) for m in metric_list]
                analysis[metric_name] = {
                    "current_value": values[-1] if values else 0,
                    "average_value": sum(values) / len(values) if values else 0,
                    "min_value": min(values) if values else 0,
                    "max_value": max(values) if values else 0,
                    "trend": self._calculate_trend(values),
                    "status": self._get_metric_status(metric_name, values[-1] if values else 0)
                }
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing performance metrics: {e}")
            return {"error": str(e)}
    
    def _analyze_system_health(self) -> Dict[str, Any]:
        """Analyze system health metrics"""
        try:
            health_metrics = self.dashboard_data.get("health_metrics", {})
            analysis = {}
            
            for component, health_data in health_metrics.items():
                health_score = health_data.get("health_score", 0.5)
                analysis[component] = {
                    "health_score": f"{health_score:.1%}",
                    "status": health_data.get("status", "unknown"),
                    "last_check": health_data.get("last_check", "unknown"),
                    "issues": health_data.get("issues", []),
                    "recommendations": health_data.get("recommendations", []),
                    "health_trend": self._get_health_trend(health_score)
                }
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing system health: {e}")
            return {"error": str(e)}
    
    def _analyze_alerts(self) -> Dict[str, Any]:
        """Analyze performance alerts"""
        try:
            alerts = self.dashboard_data.get("alerts", [])
            if not alerts:
                return {"status": "No alerts in the last 24 hours"}
            
            # Group alerts by severity
            severity_counts = {}
            component_counts = {}
            
            for alert in alerts:
                severity = alert.get("severity", "unknown")
                component = alert.get("component", "unknown")
                
                severity_counts[severity] = severity_counts.get(severity, 0) + 1
                component_counts[component] = component_counts.get(component, 0) + 1
            
            # Get recent critical alerts
            critical_alerts = [a for a in alerts if a.get("severity") == "critical"][-5:]
            
            analysis = {
                "total_alerts": len(alerts),
                "severity_distribution": severity_counts,
                "component_distribution": component_counts,
                "recent_critical_alerts": critical_alerts,
                "alert_trend": self._get_alert_trend(alerts)
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing alerts: {e}")
            return {"error": str(e)}
    
    def _analyze_trends(self) -> Dict[str, Any]:
        """Analyze performance trends"""
        try:
            metrics = self.dashboard_data.get("stall_metrics", [])
            if len(metrics) < 2:
                return {"status": "Insufficient data for trend analysis"}
            
            # Simple trend analysis
            trends = {}
            for metric_name in set(m.get("name") for m in metrics):
                metric_values = [m.get("value", 0) for m in metrics if m.get("name") == metric_name]
                if len(metric_values) >= 2:
                    trends[metric_name] = {
                        "trend": self._calculate_trend(metric_values),
                        "change_percentage": self._calculate_change_percentage(metric_values),
                        "stability": self._calculate_stability(metric_values)
                    }
            
            return trends
            
        except Exception as e:
            logger.error(f"Error analyzing trends: {e}")
            return {"error": str(e)}
    
    def _generate_recommendations(self) -> List[Dict[str, Any]]:
        """Generate optimization recommendations"""
        try:
            recommendations = []
            
            # CPU usage recommendations
            cpu_usage = self._get_latest_metric("cpu_usage", 0)
            if cpu_usage > 80:
                recommendations.append({
                    "priority": "high",
                    "category": "system_resources",
                    "title": "Optimize CPU Usage",
                    "description": f"Current CPU usage is {cpu_usage:.1f}%, exceeding 80% threshold",
                    "action": "Review CPU-intensive operations and consider horizontal scaling",
                    "expected_impact": "Reduce system load and improve response times"
                })
            
            # Memory usage recommendations
            memory_usage = self._get_latest_metric("memory_usage", 0)
            if memory_usage > 85:
                recommendations.append({
                    "priority": "high",
                    "category": "system_resources",
                    "title": "Optimize Memory Usage",
                    "description": f"Current memory usage is {memory_usage:.1f}%, exceeding 85% threshold",
                    "action": "Investigate memory leaks and optimize memory allocation",
                    "expected_impact": "Prevent memory-related crashes and improve stability"
                })
            
            # Response time recommendations
            response_time = self._get_latest_metric("response_time", 0)
            if response_time > 1000:
                recommendations.append({
                    "priority": "medium",
                    "category": "performance",
                    "title": "Optimize Response Time",
                    "description": f"Current response time is {response_time:.1f}ms, exceeding 1000ms threshold",
                    "action": "Identify and optimize critical code paths",
                    "expected_impact": "Improve user experience and system responsiveness"
                })
            
            # Stall rate recommendations
            stall_rate = self._get_latest_metric("stall_detection_rate", 0)
            if stall_rate > 0.05:
                recommendations.append({
                    "priority": "high",
                    "category": "stall_prevention",
                    "title": "Improve Stall Prevention",
                    "description": f"Current stall rate is {stall_rate:.3f}, exceeding 0.05 threshold",
                    "action": "Review stall prevention mechanisms and error handling",
                    "expected_impact": "Reduce system stalls and improve reliability"
                })
            
            if not recommendations:
                recommendations.append({
                    "priority": "low",
                    "category": "monitoring",
                    "title": "Continue Monitoring",
                    "description": "System performance is currently optimal",
                    "action": "Maintain current monitoring and alerting",
                    "expected_impact": "Sustain optimal performance levels"
                })
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            return [{"error": str(e)}]
    
    def _generate_action_items(self) -> List[Dict[str, Any]]:
        """Generate actionable items"""
        try:
            action_items = []
            
            # High priority actions
            critical_alerts = len([a for a in self.dashboard_data.get("alerts", []) 
                                if a.get("severity") == "critical"])
            if critical_alerts > 0:
                action_items.append({
                    "priority": "immediate",
                    "title": "Address Critical Alerts",
                    "description": f"Resolve {critical_alerts} critical performance alerts",
                    "assigned_to": "System Administrator",
                    "due_date": "Today",
                    "estimated_effort": "2-4 hours"
                })
            
            # Medium priority actions
            overall_health = self.dashboard_data.get("overall_health_score", 0.5)
            if overall_health < 0.7:
                action_items.append({
                    "priority": "high",
                    "title": "System Health Review",
                    "description": "Review and optimize system components with low health scores",
                    "assigned_to": "Performance Team",
                    "due_date": "This week",
                    "estimated_effort": "1-2 days"
                })
            
            # Low priority actions
            action_items.append({
                "priority": "low",
                "title": "Performance Documentation",
                "description": "Update performance documentation and runbooks",
                "assigned_to": "Documentation Team",
                "due_date": "Next week",
                "estimated_effort": "4-6 hours"
            })
            
            return action_items
            
        except Exception as e:
            logger.error(f"Error generating action items: {e}")
            return [{"error": str(e)}]
    
    def _get_health_status(self, health_score: float) -> str:
        """Get health status description"""
        if health_score >= 0.9:
            return "Excellent"
        elif health_score >= 0.8:
            return "Good"
        elif health_score >= 0.7:
            return "Fair"
        elif health_score >= 0.6:
            return "Poor"
        else:
            return "Critical"
    
    def _get_performance_rating(self, health_score: float) -> str:
        """Get performance rating"""
        if health_score >= 0.9:
            return "A+ (Outstanding)"
        elif health_score >= 0.8:
            return "A (Excellent)"
        elif health_score >= 0.7:
            return "B (Good)"
        elif health_score >= 0.6:
            return "C (Fair)"
        else:
            return "D (Poor)"
    
    def _get_key_findings(self, health_score: float, critical_alerts: int) -> List[str]:
        """Get key findings"""
        findings = []
        
        if health_score >= 0.8:
            findings.append("System performance is excellent with no major issues detected")
        elif health_score >= 0.7:
            findings.append("System performance is good with minor optimization opportunities")
        else:
            findings.append("System performance requires attention and optimization")
        
        if critical_alerts > 0:
            findings.append(f"Critical alerts require immediate attention ({critical_alerts} active)")
        
        if health_score < 0.6:
            findings.append("System health is below acceptable thresholds - immediate action required")
        
        return findings
    
    def _calculate_trend(self, values: List[float]) -> str:
        """Calculate trend from values"""
        if len(values) < 2:
            return "stable"
        
        recent_avg = sum(values[-3:]) / min(3, len(values))
        older_avg = sum(values[:-3]) / max(1, len(values) - 3)
        
        if recent_avg > older_avg * 1.1:
            return "increasing"
        elif recent_avg < older_avg * 0.9:
            return "decreasing"
        else:
            return "stable"
    
    def _calculate_change_percentage(self, values: List[float]) -> float:
        """Calculate percentage change"""
        if len(values) < 2:
            return 0.0
        
        return ((values[-1] - values[0]) / values[0]) * 100
    
    def _calculate_stability(self, values: List[float]) -> str:
        """Calculate stability rating"""
        if len(values) < 2:
            return "unknown"
        
        variance = sum((x - sum(values)/len(values))**2 for x in values) / len(values)
        if variance < 0.01:
            return "very_stable"
        elif variance < 0.1:
            return "stable"
        elif variance < 0.5:
            return "moderate"
        else:
            return "unstable"
    
    def _get_metric_status(self, metric_name: str, value: float) -> str:
        """Get metric status"""
        thresholds = {
            "cpu_usage": 80.0,
            "memory_usage": 85.0,
            "response_time": 1000.0,
            "stall_detection_rate": 0.1
        }
        
        threshold = thresholds.get(metric_name, 100.0)
        if value <= threshold * 0.5:
            return "excellent"
        elif value <= threshold * 0.7:
            return "good"
        elif value <= threshold * 0.9:
            return "warning"
        elif value <= threshold:
            return "critical"
        else:
            return "emergency"
    
    def _get_health_trend(self, health_score: float) -> str:
        """Get health trend"""
        if health_score >= 0.9:
            return "maintaining_excellence"
        elif health_score >= 0.8:
            return "stable_good"
        elif health_score >= 0.7:
            return "stable_fair"
        else:
            return "degrading"
    
    def _get_alert_trend(self, alerts: List[Dict[str, Any]]) -> str:
        """Get alert trend"""
        if not alerts:
            return "no_alerts"
        
        recent_alerts = [a for a in alerts if a.get("timestamp", "") > 
                        (datetime.now() - timedelta(hours=1)).isoformat()]
        
        if len(recent_alerts) > len(alerts) * 0.5:
            return "increasing"
        elif len(recent_alerts) < len(alerts) * 0.2:
            return "decreasing"
        else:
            return "stable"
    
    def _get_latest_metric(self, metric_name: str, default_value: float) -> float:
        """Get latest value for a specific metric"""
        try:
            metrics = self.dashboard_data.get("stall_metrics", [])
            for metric in reversed(metrics):
                if metric.get("name") == metric_name:
                    return metric.get("value", default_value)
            return default_value
        except Exception as e:
            logger.error(f"Error getting latest metric: {e}")
            return default_value
    
    def export_report(self, filepath: str, format_type: str = "json"):
        """Export report to file"""
        try:
            report = self.generate_full_report()
            
            if format_type.lower() == "json":
                with open(filepath, 'w') as f:
                    json.dump(report, f, indent=2, default=str)
            else:
                # Could add CSV or other formats here
                raise ValueError(f"Unsupported format: {format_type}")
            
            logger.info(f"Performance report exported to {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Error exporting report: {e}")
            return False


def main():
    """Main entry point for testing"""
    print("📊 Performance Report Generator - Agent-6")
    print("=" * 50)
    
    # Sample dashboard data for testing
    sample_data = {
        "overall_health_score": 0.85,
        "uptime_seconds": 86400,
        "stall_metrics": [
            {"name": "cpu_usage", "value": 75.0},
            {"name": "memory_usage", "value": 80.0},
            {"name": "response_time", "value": 800.0}
        ],
        "alerts": [],
        "health_metrics": {}
    }
    
    # Generate report
    generator = PerformanceReportGenerator(sample_data)
    report = generator.generate_full_report()
    
    # Export report
    output_file = f"performance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    if generator.export_report(output_file):
        print(f"✅ Report generated and exported to {output_file}")
    else:
        print("❌ Failed to export report")


if __name__ == "__main__":
    main()
