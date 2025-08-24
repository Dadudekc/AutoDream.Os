#!/usr/bin/env python3
"""
Continuous Quality Monitor System
================================
Enterprise-grade continuous quality monitoring and validation.
Target: 300 LOC, Maximum: 350 LOC.
Focus: Real-time monitoring, automated alerts, quality improvement tracking.
"""

import os
import sys
import time
import json
import threading

from src.utils.stability_improvements import stability_manager, safe_import
from pathlib import Path
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import quality gates and V2 services
try:
    from services.automated_quality_gates import AutomatedQualityGates
    from services.enterprise_quality_assurance import EnterpriseQualityAssurance
    from services.integration_monitoring import V2IntegrationMonitoring
except ImportError as e:
    print(f"Import warning: {e}")
    # Fallback mock services for monitoring
    AutomatedQualityGates = None
    EnterpriseQualityAssurance = None
    V2IntegrationMonitoring = None


@dataclass
class QualityAlert:
    """Quality alert notification"""

    alert_id: str
    severity: str  # LOW, MEDIUM, HIGH, CRITICAL
    message: str
    file_path: str
    quality_score: float
    threshold: float
    timestamp: float
    recommendations: List[str]


@dataclass
class QualityTrend:
    """Quality trend analysis"""

    metric_name: str
    current_value: float
    previous_value: float
    trend_direction: str  # IMPROVING, DECLINING, STABLE
    change_percentage: float
    trend_strength: str  # STRONG, MODERATE, WEAK


class ContinuousQualityMonitor:
    """Continuous quality monitoring system for enterprise standards"""

    def __init__(self, config_path: str = "quality_monitor_config.json"):
        """Initialize continuous quality monitor"""
        self.config_path = config_path
        self.config = self._load_configuration()
        self.quality_gates = None
        self.monitoring_active = False
        self.monitor_thread = None
        self.quality_history = []
        self.alert_history = []
        self.trend_analysis = {}

        # Initialize V2 services
        self.enterprise_qa = (
            EnterpriseQualityAssurance() if EnterpriseQualityAssurance else None
        )
        self.integration_monitoring = (
            V2IntegrationMonitoring() if V2IntegrationMonitoring else None
        )

        # Initialize quality gates if available
        if AutomatedQualityGates:
            self.quality_gates = AutomatedQualityGates()

        # Alert callbacks
        self.alert_callbacks = []

    def _load_configuration(self) -> Dict:
        """Load quality monitoring configuration"""
        default_config = {
            "monitoring": {
                "enabled": True,
                "interval_seconds": 300,  # 5 minutes
                "auto_validation": True,
                "alert_thresholds": {
                    "critical": 60.0,
                    "high": 70.0,
                    "medium": 80.0,
                    "low": 90.0,
                },
            },
            "quality_gates": {
                "enforce_loc_compliance": True,
                "enforce_code_quality": True,
                "enforce_enterprise_standards": True,
                "enforce_test_coverage": True,
            },
            "trend_analysis": {
                "history_window_days": 7,
                "trend_threshold": 5.0,
                "improvement_target": 2.0,
            },
        }

        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, "r") as f:
                    return json.load(f)
            else:
                # Create default configuration
                with open(self.config_path, "w") as f:
                    json.dump(default_config, f, indent=2)
                return default_config
        except Exception as e:
            print(f"Configuration loading error: {e}")
            return default_config

    def start_monitoring(self, directory_path: str = None) -> bool:
        """Start continuous quality monitoring"""
        if self.monitoring_active:
            print("⚠️  Monitoring already active")
            return False

        if not directory_path:
            directory_path = os.getcwd()

        print(f"🚀 Starting continuous quality monitoring for: {directory_path}")

        self.monitoring_active = True
        self.monitor_thread = threading.Thread(
            target=self._monitoring_loop, args=(directory_path,), daemon=True
        )
        self.monitor_thread.start()

        print("✅ Continuous quality monitoring started")
        return True

    def stop_monitoring(self) -> bool:
        """Stop continuous quality monitoring"""
        if not self.monitoring_active:
            print("⚠️  Monitoring not active")
            return False

        print("🛑 Stopping continuous quality monitoring...")
        self.monitoring_active = False

        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=5)

        print("✅ Continuous quality monitoring stopped")
        return True

    def _monitoring_loop(self, directory_path: str):
        """Main monitoring loop"""
        while self.monitoring_active:
            try:
                # Perform quality validation
                validation_result = self._perform_quality_validation(directory_path)

                # Store in history
                self.quality_history.append(validation_result)

                # Analyze trends
                self._analyze_quality_trends()

                # Check for alerts
                self._check_quality_alerts(validation_result)

                # Wait for next monitoring cycle
                time.sleep(self.config["monitoring"]["interval_seconds"])

            except Exception as e:
                print(f"❌ Monitoring error: {e}")
                time.sleep(60)  # Wait 1 minute on error

    def _perform_quality_validation(self, directory_path: str) -> Dict:
        """Perform comprehensive quality validation"""
        if not self.quality_gates:
            return {"status": "error", "message": "Quality gates not available"}

        try:
            # Validate directory
            validation_result = self.quality_gates.validate_directory(directory_path)

            # Add monitoring metadata
            validation_result["monitor_timestamp"] = time.time()
            validation_result["monitor_cycle"] = len(self.quality_history) + 1

            return validation_result

        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "monitor_timestamp": time.time(),
                "monitor_cycle": len(self.quality_history) + 1,
            }

    def _analyze_quality_trends(self):
        """Analyze quality trends over time"""
        if len(self.quality_history) < 2:
            return

        # Get recent history window
        window_days = self.config["trend_analysis"]["history_window_days"]
        cutoff_time = time.time() - (window_days * 24 * 3600)

        recent_history = [
            h
            for h in self.quality_history
            if h.get("monitor_timestamp", 0) > cutoff_time
        ]

        if len(recent_history) < 2:
            return

        # Analyze quality score trends
        current_score = recent_history[-1].get("quality_score", 0)
        previous_score = recent_history[-2].get("quality_score", 0)

        change_percentage = (
            ((current_score - previous_score) / previous_score * 100)
            if previous_score > 0
            else 0
        )

        # Determine trend direction and strength
        if change_percentage > self.config["trend_analysis"]["trend_threshold"]:
            trend_direction = "IMPROVING"
            trend_strength = "STRONG" if abs(change_percentage) > 10 else "MODERATE"
        elif change_percentage < -self.config["trend_analysis"]["trend_threshold"]:
            trend_direction = "DECLINING"
            trend_strength = "STRONG" if abs(change_percentage) > 10 else "MODERATE"
        else:
            trend_direction = "STABLE"
            trend_strength = "WEAK"

        self.trend_analysis["quality_score"] = QualityTrend(
            metric_name="quality_score",
            current_value=current_score,
            previous_value=previous_score,
            trend_direction=trend_direction,
            change_percentage=change_percentage,
            trend_strength=trend_strength,
        )

    def _check_quality_alerts(self, validation_result: Dict):
        """Check for quality alerts and trigger notifications"""
        if validation_result.get("status") == "error":
            return

        quality_score = validation_result.get("quality_score", 0)
        thresholds = self.config["monitoring"]["alert_thresholds"]

        # Determine alert severity
        if quality_score <= thresholds["critical"]:
            severity = "CRITICAL"
        elif quality_score <= thresholds["high"]:
            severity = "HIGH"
        elif quality_score <= thresholds["medium"]:
            severity = "MEDIUM"
        elif quality_score <= thresholds["low"]:
            severity = "LOW"
        else:
            return  # No alert needed

        # Create alert
        alert = QualityAlert(
            alert_id=f"QUALITY-{int(time.time())}",
            severity=severity,
            message=f"Quality score {quality_score:.1f}% below {severity.lower()} threshold",
            file_path=validation_result.get("directory_path", "unknown"),
            quality_score=quality_score,
            threshold=thresholds.get(severity.lower(), 0),
            timestamp=time.time(),
            recommendations=self._generate_alert_recommendations(
                severity, quality_score
            ),
        )

        # Store alert
        self.alert_history.append(alert)

        # Trigger alert callbacks
        self._trigger_alert_callbacks(alert)

        print(f"🚨 Quality Alert: {severity} - {alert.message}")

    def _generate_alert_recommendations(
        self, severity: str, quality_score: float
    ) -> List[str]:
        """Generate recommendations based on alert severity"""
        recommendations = []

        if severity == "CRITICAL":
            recommendations.extend(
                [
                    "Immediate code review required",
                    "Consider code refactoring",
                    "Implement quality improvement plan",
                ]
            )
        elif severity == "HIGH":
            recommendations.extend(
                [
                    "Schedule code review",
                    "Address quality violations",
                    "Monitor quality trends",
                ]
            )
        elif severity == "MEDIUM":
            recommendations.extend(
                [
                    "Review quality metrics",
                    "Plan quality improvements",
                    "Set quality targets",
                ]
            )
        elif severity == "LOW":
            recommendations.extend(
                [
                    "Monitor quality trends",
                    "Maintain current standards",
                    "Plan incremental improvements",
                ]
            )

        return recommendations

    def _trigger_alert_callbacks(self, alert: QualityAlert):
        """Trigger registered alert callbacks"""
        for callback in self.alert_callbacks:
            try:
                callback(alert)
            except Exception as e:
                print(f"❌ Alert callback error: {e}")

    def register_alert_callback(self, callback: Callable[[QualityAlert], None]):
        """Register alert callback function"""
        self.alert_callbacks.append(callback)
        print(f"✅ Alert callback registered: {callback.__name__}")

    def get_quality_summary(self) -> Dict:
        """Get comprehensive quality summary"""
        if not self.quality_history:
            return {"status": "No quality data available"}

        # Calculate summary statistics
        total_validations = len(self.quality_history)
        successful_validations = len(
            [h for h in self.quality_history if h.get("status") != "error"]
        )

        quality_scores = [
            h.get("quality_score", 0)
            for h in self.quality_history
            if h.get("quality_score")
        ]
        average_score = (
            sum(quality_scores) / len(quality_scores) if quality_scores else 0
        )

        # Get recent trends
        recent_trends = {}
        if self.trend_analysis:
            for metric, trend in self.trend_analysis.items():
                recent_trends[metric] = asdict(trend)

        # Get alert summary
        alert_summary = {
            "total_alerts": len(self.alert_history),
            "critical_alerts": len(
                [a for a in self.alert_history if a.severity == "CRITICAL"]
            ),
            "high_alerts": len([a for a in self.alert_history if a.severity == "HIGH"]),
            "medium_alerts": len(
                [a for a in self.alert_history if a.severity == "MEDIUM"]
            ),
            "low_alerts": len([a for a in self.alert_history if a.severity == "LOW"]),
        }

        return {
            "monitoring_status": "active" if self.monitoring_active else "inactive",
            "total_validations": total_validations,
            "successful_validations": successful_validations,
            "success_rate": (successful_validations / total_validations * 100)
            if total_validations > 0
            else 0,
            "average_quality_score": average_score,
            "quality_grade": self._calculate_quality_grade(average_score),
            "recent_trends": recent_trends,
            "alert_summary": alert_summary,
            "last_validation": self.quality_history[-1].get("monitor_timestamp")
            if self.quality_history
            else None,
            "monitoring_started": self.quality_history[0].get("monitor_timestamp")
            if self.quality_history
            else None,
        }

    def _calculate_quality_grade(self, score: float) -> str:
        """Calculate quality grade based on score"""
        if score >= 95.0:
            return "A+"
        elif score >= 90.0:
            return "A"
        elif score >= 85.0:
            return "B+"
        elif score >= 80.0:
            return "B"
        elif score >= 75.0:
            return "C+"
        elif score >= 70.0:
            return "C"
        else:
            return "D"

    def export_monitoring_report(
        self, output_path: str = "continuous_quality_report.json"
    ):
        """Export comprehensive monitoring report"""
        report = {
            "timestamp": time.time(),
            "system": "Continuous Quality Monitor System",
            "configuration": self.config,
            "quality_summary": self.get_quality_summary(),
            "quality_history": self.quality_history[-50:],  # Last 50 entries
            "alert_history": [
                asdict(a) for a in self.alert_history[-20:]
            ],  # Last 20 alerts
            "trend_analysis": {k: asdict(v) for k, v in self.trend_analysis.items()},
            "recommendations": self._generate_monitoring_recommendations(),
        }

        with open(output_path, "w") as f:
            json.dump(report, f, indent=2)

        print(f"📊 Monitoring report exported to: {output_path}")
        return report

    def _generate_monitoring_recommendations(self) -> List[str]:
        """Generate monitoring system recommendations"""
        summary = self.get_quality_summary()
        recommendations = []

        if summary.get("average_quality_score", 0) < 80.0:
            recommendations.append(
                "Focus on improving overall code quality to meet enterprise standards"
            )

        if summary.get("alert_summary", {}).get("critical_alerts", 0) > 0:
            recommendations.append(
                "Address critical quality alerts immediately to prevent system degradation"
            )

        if summary.get("alert_summary", {}).get("high_alerts", 0) > 2:
            recommendations.append(
                "Implement quality improvement plan to reduce high-severity alerts"
            )

        if not self.monitoring_active:
            recommendations.append(
                "Enable continuous monitoring for proactive quality management"
            )

        if not recommendations:
            recommendations.append(
                "Quality monitoring system is performing well - maintain current standards"
            )

        return recommendations


def main():
    """Run continuous quality monitor system"""
    print("🚀 Continuous Quality Monitor System")
    print("Enterprise Quality Monitoring")
    print("=" * 50)

    # Initialize monitor
    monitor = ContinuousQualityMonitor()

    # Start monitoring current directory
    current_dir = os.getcwd()
    print(f"🔍 Starting quality monitoring for: {current_dir}")

    # Start monitoring
    monitor.start_monitoring(current_dir)

    # Wait for initial validation
    print("⏳ Waiting for initial quality validation...")
    time.sleep(10)

    # Get quality summary
    summary = monitor.get_quality_summary()
    print(f"\n📊 Quality Summary:")
    print(f"   Monitoring Status: {summary['monitoring_status']}")
    print(f"   Total Validations: {summary['total_validations']}")
    print(f"   Success Rate: {summary['success_rate']:.1f}%")
    print(f"   Average Quality Score: {summary['average_quality_score']:.1f}")
    print(f"   Quality Grade: {summary['quality_grade']}")

    # Export report
    report = monitor.export_monitoring_report()

    print(f"\n✅ Continuous quality monitoring started!")
    print(f"📁 Report saved to: continuous_quality_report.json")
    print(f"🔍 Monitor will continue running in background...")

    return report


if __name__ == "__main__":
    main()
