#!/usr/bin/env python3
"""
V3-018: Quality Monitoring
==========================

Quality monitoring and alerting with V2 compliance.
Focuses on continuous quality monitoring and alerting.
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

from v3.v3_018_quality_core import QualityLevel, QualityMetric, QualityCheck, QualityReport


class AlertType(Enum):
    """Alert types for quality monitoring."""
    QUALITY_DEGRADATION = "quality_degradation"
    THRESHOLD_BREACH = "threshold_breach"
    CRITICAL_ISSUE = "critical_issue"
    IMPROVEMENT_OPPORTUNITY = "improvement_opportunity"


@dataclass
class QualityAlert:
    """Quality alert structure."""
    alert_id: str
    component_id: str
    alert_type: AlertType
    metric: QualityMetric
    current_value: float
    threshold: float
    message: str
    severity: str
    triggered_at: datetime
    resolved_at: Optional[datetime] = None


@dataclass
class QualityTrend:
    """Quality trend analysis."""
    component_id: str
    metric: QualityMetric
    values: List[float]
    timestamps: List[datetime]
    trend_direction: str
    trend_strength: float


class QualityMonitor:
    """Quality monitoring and alerting system."""
    
    def __init__(self):
        self.alerts = []
        self.trends = {}
        self.monitoring_active = False
        self.alert_thresholds = {
            QualityMetric.CODE_COVERAGE: 70.0,
            QualityMetric.PERFORMANCE: 60.0,
            QualityMetric.SECURITY: 80.0,
            QualityMetric.MAINTAINABILITY: 60.0,
            QualityMetric.RELIABILITY: 80.0,
            QualityMetric.USABILITY: 60.0
        }
    
    def start_monitoring(self):
        """Start quality monitoring."""
        self.monitoring_active = True
        print("🔍 Quality monitoring started")
    
    def stop_monitoring(self):
        """Stop quality monitoring."""
        self.monitoring_active = False
        print("⏹️ Quality monitoring stopped")
    
    def monitor_quality_report(self, report: QualityReport):
        """Monitor quality report for alerts."""
        if not self.monitoring_active:
            return
        
        for check in report.checks:
            self._check_quality_alert(report.component_id, check)
            self._update_quality_trend(report.component_id, check)
    
    def _check_quality_alert(self, component_id: str, check: QualityCheck):
        """Check for quality alerts."""
        threshold = self.alert_thresholds.get(check.metric, 60.0)
        
        if check.current_value < threshold:
            alert_type = AlertType.THRESHOLD_BREACH
            if check.level == QualityLevel.CRITICAL:
                alert_type = AlertType.CRITICAL_ISSUE
            elif check.level == QualityLevel.POOR:
                alert_type = AlertType.QUALITY_DEGRADATION
            
            self._create_alert(
                component_id, alert_type, check.metric,
                check.current_value, threshold,
                f"Quality threshold breached for {check.metric.value}: {check.current_value:.1f} < {threshold:.1f}"
            )
        elif check.current_value > threshold * 1.2:
            self._create_alert(
                component_id, AlertType.IMPROVEMENT_OPPORTUNITY, check.metric,
                check.current_value, threshold,
                f"Quality improvement opportunity for {check.metric.value}: {check.current_value:.1f} > {threshold * 1.2:.1f}"
            )
    
    def _create_alert(self, component_id: str, alert_type: AlertType, metric: QualityMetric,
                     current_value: float, threshold: float, message: str):
        """Create quality alert."""
        alert = QualityAlert(
            alert_id=f"{component_id}_{metric.value}_{int(datetime.now().timestamp())}",
            component_id=component_id,
            alert_type=alert_type,
            metric=metric,
            current_value=current_value,
            threshold=threshold,
            message=message,
            severity=self._determine_severity(alert_type, current_value, threshold),
            triggered_at=datetime.now()
        )
        
        self.alerts.append(alert)
        print(f"🚨 Quality Alert: {message}")
    
    def _determine_severity(self, alert_type: AlertType, current_value: float, threshold: float) -> str:
        """Determine alert severity."""
        if alert_type == AlertType.CRITICAL_ISSUE:
            return "critical"
        elif alert_type == AlertType.QUALITY_DEGRADATION:
            return "high"
        elif alert_type == AlertType.THRESHOLD_BREACH:
            return "medium"
        else:
            return "low"
    
    def _update_quality_trend(self, component_id: str, check: QualityCheck):
        """Update quality trend for metric."""
        trend_key = f"{component_id}_{check.metric.value}"
        
        if trend_key not in self.trends:
            self.trends[trend_key] = QualityTrend(
                component_id=component_id,
                metric=check.metric,
                values=[],
                timestamps=[],
                trend_direction="stable",
                trend_strength=0.0
            )
        
        trend = self.trends[trend_key]
        trend.values.append(check.current_value)
        trend.timestamps.append(check.checked_at)
        
        # Keep only last 10 values
        if len(trend.values) > 10:
            trend.values = trend.values[-10:]
            trend.timestamps = trend.timestamps[-10:]
        
        # Calculate trend
        if len(trend.values) >= 3:
            trend.trend_direction, trend.trend_strength = self._calculate_trend(trend.values)
    
    def _calculate_trend(self, values: List[float]) -> tuple[str, float]:
        """Calculate trend direction and strength."""
        if len(values) < 3:
            return "stable", 0.0
        
        # Simple linear trend calculation
        n = len(values)
        x = list(range(n))
        y = values
        
        # Calculate slope
        x_mean = sum(x) / n
        y_mean = sum(y) / n
        
        numerator = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
        denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
        
        if denominator == 0:
            return "stable", 0.0
        
        slope = numerator / denominator
        
        if slope > 0.1:
            return "improving", abs(slope)
        elif slope < -0.1:
            return "degrading", abs(slope)
        else:
            return "stable", abs(slope)
    
    def get_active_alerts(self) -> List[QualityAlert]:
        """Get active quality alerts."""
        return [alert for alert in self.alerts if not alert.resolved_at]
    
    def resolve_alert(self, alert_id: str) -> bool:
        """Resolve quality alert."""
        for alert in self.alerts:
            if alert.alert_id == alert_id:
                alert.resolved_at = datetime.now()
                return True
        return False
    
    def get_quality_trends(self, component_id: str) -> List[QualityTrend]:
        """Get quality trends for component."""
        return [trend for trend in self.trends.values() if trend.component_id == component_id]
    
    def get_monitoring_summary(self) -> Dict[str, Any]:
        """Get monitoring summary."""
        active_alerts = self.get_active_alerts()
        
        alert_counts = {}
        for alert in active_alerts:
            alert_type = alert.alert_type.value
            alert_counts[alert_type] = alert_counts.get(alert_type, 0) + 1
        
        return {
            "monitoring_active": self.monitoring_active,
            "total_alerts": len(self.alerts),
            "active_alerts": len(active_alerts),
            "alert_types": alert_counts,
            "total_trends": len(self.trends),
            "last_alert": max(alert.triggered_at for alert in self.alerts).isoformat() if self.alerts else None
        }
    
    def get_quality_recommendations(self) -> List[str]:
        """Get quality improvement recommendations."""
        recommendations = []
        active_alerts = self.get_active_alerts()
        
        # Analyze alerts for recommendations
        critical_alerts = [alert for alert in active_alerts if alert.severity == "critical"]
        if critical_alerts:
            recommendations.append("Address critical quality issues immediately")
        
        high_alerts = [alert for alert in active_alerts if alert.severity == "high"]
        if high_alerts:
            recommendations.append("Focus on high-priority quality improvements")
        
        # Analyze trends for recommendations
        degrading_trends = [trend for trend in self.trends.values() if trend.trend_direction == "degrading"]
        if degrading_trends:
            recommendations.append("Investigate degrading quality trends")
        
        improving_trends = [trend for trend in self.trends.values() if trend.trend_direction == "improving"]
        if improving_trends:
            recommendations.append("Maintain current quality improvement efforts")
        
        if not recommendations:
            recommendations.append("Quality monitoring shows stable conditions")
        
        return recommendations


def main():
    """Main execution function."""
    print("🔍 V3-018 Quality Monitoring - Testing...")
    
    # Initialize quality monitor
    monitor = QualityMonitor()
    monitor.start_monitoring()
    
    # Test quality monitoring
    from v3.v3_018_quality_core import QualityChecker, QualityMetric
    
    checker = QualityChecker()
    
    # Create test quality report
    test_metrics = {
        QualityMetric.CODE_COVERAGE: 65.0,  # Below threshold
        QualityMetric.PERFORMANCE: 75.0,    # Above threshold
        QualityMetric.SECURITY: 85.0,       # Above threshold
        QualityMetric.MAINTAINABILITY: 55.0, # Below threshold
        QualityMetric.RELIABILITY: 90.0,    # Above threshold
        QualityMetric.USABILITY: 70.0       # Above threshold
    }
    
    report = checker.check_quality("test_component", "Test Component", test_metrics)
    
    # Monitor the report
    monitor.monitor_quality_report(report)
    
    # Get monitoring summary
    summary = monitor.get_monitoring_summary()
    
    print(f"\n📊 Monitoring Summary:")
    print(f"   Monitoring Active: {summary['monitoring_active']}")
    print(f"   Active Alerts: {summary['active_alerts']}")
    print(f"   Alert Types: {summary['alert_types']}")
    print(f"   Total Trends: {summary['total_trends']}")
    
    # Get active alerts
    active_alerts = monitor.get_active_alerts()
    
    print(f"\n🚨 Active Alerts:")
    for alert in active_alerts:
        print(f"   {alert.alert_type.value}: {alert.message}")
    
    # Get recommendations
    recommendations = monitor.get_quality_recommendations()
    
    print(f"\n💡 Quality Recommendations:")
    for rec in recommendations:
        print(f"   - {rec}")
    
    print("\n✅ V3-018 Quality Monitoring completed successfully!")
    return 0


if __name__ == "__main__":
    exit(main())

