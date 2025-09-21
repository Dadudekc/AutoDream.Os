#!/usr/bin/env python3
"""
V3-018: Quality Assurance Coordinator
=====================================

V2 compliant quality assurance coordinator.
"""

import json
from datetime import datetime
from typing import Dict, List, Any, Optional

# Import quality modules
from v3.v3_018_quality_core import QualityChecker, QualityLevel, QualityMetric, QualityReport
from v3.v3_018_quality_monitoring import QualityMonitor, AlertType, QualityAlert


class QualityAssuranceCoordinator:
    """Coordinates quality assurance components."""
    
    def __init__(self):
        self.quality_checker = QualityChecker()
        self.quality_monitor = QualityMonitor()
        self.is_initialized = False
    
    def initialize(self):
        """Initialize quality assurance system."""
        try:
            self.quality_monitor.start_monitoring()
            self.is_initialized = True
            print("🔍 Quality Assurance Coordinator initialized successfully")
            return True
        except Exception as e:
            print(f"❌ Initialization error: {e}")
            return False
    
    def check_component_quality(self, component_id: str, component_name: str,
                               metrics: Dict[QualityMetric, float]) -> QualityReport:
        """Check quality for a component."""
        if not self.is_initialized:
            return self._create_error_report(component_id, component_name, "Quality assurance not initialized")
        
        report = self.quality_checker.check_quality(component_id, component_name, metrics)
        self.quality_monitor.monitor_quality_report(report)
        return report
    
    def _create_error_report(self, component_id: str, component_name: str, error_message: str) -> QualityReport:
        """Create error quality report."""
        return QualityReport(
            report_id=f"error_{component_id}_{int(datetime.now().timestamp())}",
            component_id=component_id,
            component_name=component_name,
            checks=[],
            overall_score=0.0,
            overall_level=QualityLevel.CRITICAL,
            generated_at=datetime.now()
        )
    
    def get_quality_summary(self) -> Dict[str, Any]:
        """Get comprehensive quality summary."""
        if not self.is_initialized:
            return {"error": "Quality assurance not initialized"}
        
        checker_summary = self.quality_checker.get_quality_summary()
        monitoring_summary = self.quality_monitor.get_monitoring_summary()
        active_alerts = self.quality_monitor.get_active_alerts()
        
        return {
            "quality_checker": checker_summary,
            "monitoring": monitoring_summary,
            "active_alerts": [
                {
                    "alert_id": alert.alert_id,
                    "component_id": alert.component_id,
                    "alert_type": alert.alert_type.value,
                    "metric": alert.metric.value,
                    "current_value": alert.current_value,
                    "threshold": alert.threshold,
                    "message": alert.message,
                    "severity": alert.severity,
                    "triggered_at": alert.triggered_at.isoformat()
                }
                for alert in active_alerts
            ],
            "total_alerts": len(active_alerts),
            "timestamp": datetime.now().isoformat()
        }
    
    def get_component_quality(self, component_id: str) -> Optional[QualityReport]:
        """Get quality report for specific component."""
        return self.quality_checker.get_component_quality(component_id)
    
    def resolve_quality_alert(self, alert_id: str) -> bool:
        """Resolve quality alert."""
        return self.quality_monitor.resolve_alert(alert_id)
    
    def get_quality_recommendations(self) -> List[str]:
        """Get quality improvement recommendations."""
        return self.quality_monitor.get_quality_recommendations()
    
    def export_quality_report(self, report_id: str, filepath: str) -> bool:
        """Export quality report to file."""
        return self.quality_checker.export_quality_report(report_id, filepath)
    
    def get_quality_trends(self, component_id: str) -> List[Dict[str, Any]]:
        """Get quality trends for component."""
        trends = self.quality_monitor.get_quality_trends(component_id)
        
        return [
            {
                "component_id": trend.component_id,
                "metric": trend.metric.value,
                "values": trend.values,
                "timestamps": [ts.isoformat() for ts in trend.timestamps],
                "trend_direction": trend.trend_direction,
                "trend_strength": trend.trend_strength
            }
            for trend in trends
        ]
    
    def set_alert_threshold(self, metric: QualityMetric, threshold: float) -> bool:
        """Set alert threshold for metric."""
        try:
            self.quality_monitor.alert_thresholds[metric] = threshold
            print(f"✅ Set alert threshold for {metric.value}: {threshold}")
            return True
        except Exception as e:
            print(f"❌ Failed to set threshold: {e}")
            return False
    
    def get_alert_thresholds(self) -> Dict[str, float]:
        """Get current alert thresholds."""
        return {
            metric.value: threshold 
            for metric, threshold in self.quality_monitor.alert_thresholds.items()
        }
    
    def export_quality_data(self, filepath: str) -> bool:
        """Export all quality data to file."""
        try:
            quality_data = {
                "quality_summary": self.get_quality_summary(),
                "alert_thresholds": self.get_alert_thresholds(),
                "exported_at": datetime.now().isoformat()
            }
            
            with open(filepath, 'w') as f:
                json.dump(quality_data, f, indent=2, default=str)
            
            print(f"📊 Quality data exported to {filepath}")
            return True
            
        except Exception as e:
            print(f"❌ Export error: {e}")
            return False
    
    def stop_monitoring(self):
        """Stop quality monitoring."""
        self.quality_monitor.stop_monitoring()
        print("⏹️ Quality monitoring stopped")
    
    def restart_monitoring(self):
        """Restart quality monitoring."""
        self.quality_monitor.start_monitoring()
        print("🔄 Quality monitoring restarted")


def main():
    """Main execution function."""
    print("🔍 V3-018 Quality Assurance Coordinator - Testing...")
    
    try:
        coordinator = QualityAssuranceCoordinator()
        coordinator.initialize()
        
        print("\n🔍 Testing quality checking...")
        
        test_metrics = {
            QualityMetric.CODE_COVERAGE: 85.5,
            QualityMetric.PERFORMANCE: 78.2,
            QualityMetric.SECURITY: 92.1,
            QualityMetric.MAINTAINABILITY: 67.8,
            QualityMetric.RELIABILITY: 88.9,
            QualityMetric.USABILITY: 73.4
        }
        
        report = coordinator.check_component_quality("test_component", "Test Component", test_metrics)
        
        print(f"   Component: {report.component_name}")
        print(f"   Overall Score: {report.overall_score:.1f}")
        print(f"   Overall Level: {report.overall_level.value}")
        print(f"   Total Checks: {len(report.checks)}")
        
        summary = coordinator.get_quality_summary()
        
        print(f"\n📊 Quality Summary:")
        print(f"   Total Reports: {summary['quality_checker']['total_reports']}")
        print(f"   Average Score: {summary['quality_checker']['average_score']:.1f}")
        print(f"   Active Alerts: {summary['total_alerts']}")
        print(f"   Monitoring Active: {summary['monitoring']['monitoring_active']}")
        
        recommendations = coordinator.get_quality_recommendations()
        
        print(f"\n💡 Quality Recommendations:")
        for rec in recommendations:
            print(f"   - {rec}")
        
        coordinator.export_quality_data("quality_assurance_data.json")
        
        print("\n✅ V3-018 Quality Assurance Coordinator completed successfully!")
        return 0
        
    except Exception as e:
        print(f"❌ V3-018 implementation error: {e}")
        return 1


if __name__ == "__main__":
    exit(main())


