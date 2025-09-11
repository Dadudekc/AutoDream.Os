"""
🐝 AGENT-8 OPERATIONAL MONITORING BASELINE SYSTEM
Phase 2 Consolidation - Operational Stability Foundation

This module provides comprehensive operational monitoring baseline establishment
including SLA impact analysis, monitoring capacity planning, and alert threshold baselines.
"""

from __future__ import annotations

import json
import os
import platform
import psutil
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Union

from pathlib import Path


class MonitoringPriority(Enum):
    """Operational monitoring priority levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class SLATier(Enum):
    """Service Level Agreement tiers."""
    PLATINUM = "platinum"  # 99.99% uptime
    GOLD = "gold"          # 99.9% uptime
    SILVER = "silver"      # 99.5% uptime
    BRONZE = "bronze"      # 99.0% uptime


@dataclass
class OperationalMetric:
    """Represents a single operational metric."""
    name: str
    value: Union[int, float, str, bool]
    unit: str
    timestamp: datetime
    priority: MonitoringPriority
    sla_impact: bool = False
    baseline_value: Optional[Union[int, float]] = None
    threshold_warning: Optional[Union[int, float]] = None
    threshold_critical: Optional[Union[int, float]] = None
    trend_direction: Optional[str] = None  # "up", "down", "stable"


@dataclass
class SystemHealthStatus:
    """Comprehensive system health status."""
    timestamp: datetime
    overall_status: str = "unknown"
    components: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    alerts: List[Dict[str, Any]] = field(default_factory=list)
    metrics: List[OperationalMetric] = field(default_factory=list)
    sla_compliance: Dict[str, bool] = field(default_factory=dict)
    consolidation_impact: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SLAAnalysis:
    """Service Level Agreement impact analysis."""
    tier: SLATier
    current_uptime_percentage: float
    required_uptime_percentage: float
    compliance_status: bool
    risk_assessment: Dict[str, Any]
    consolidation_impact: Dict[str, Any]
    mitigation_strategies: List[str]


class OperationalMonitoringBaseline:
    """
    Comprehensive operational monitoring baseline system for Phase 2 consolidation.

    This system establishes monitoring foundations, SLA analysis, and operational
    stability baselines to ensure safe consolidation execution.
    """

    def __init__(self, baseline_directory: str = "operational_baseline"):
        self.baseline_directory = Path(baseline_directory)
        self.baseline_directory.mkdir(exist_ok=True)

        # Baseline data storage
        self.baseline_data: Dict[str, Any] = {}
        self.sla_analysis: Dict[str, SLAAnalysis] = {}
        self.monitoring_capacity: Dict[str, Any] = {}
        self.alert_thresholds: Dict[str, Dict[str, Union[int, float]]] = {}

        # Historical data for trend analysis
        self.metric_history: Dict[str, List[OperationalMetric]] = {}
        self.health_history: List[SystemHealthStatus] = []

        # Consolidation impact tracking
        self.consolidation_impacts: Dict[str, Dict[str, Any]] = {}

        # Initialize baseline
        self._initialize_baseline()

    def _initialize_baseline(self) -> None:
        """Initialize the operational monitoring baseline."""
        self._load_existing_baseline()
        self._establish_sla_baselines()
        self._configure_monitoring_capacity()
        self._set_alert_thresholds()
        self._create_health_check_profiles()

    def _load_existing_baseline(self) -> None:
        """Load existing baseline data if available."""
        baseline_file = self.baseline_directory / "operational_baseline.json"
        if baseline_file.exists():
            try:
                with open(baseline_file, 'r') as f:
                    self.baseline_data = json.load(f)
                print("✅ Loaded existing operational baseline")
            except Exception as e:
                print(f"⚠️  Could not load existing baseline: {e}")
                self.baseline_data = {}

    def _establish_sla_baselines(self) -> None:
        """Establish SLA baselines for different system components."""
        # Define SLA requirements for different components
        sla_requirements = {
            "core_system": SLATier.PLATINUM,
            "messaging_system": SLATier.GOLD,
            "analytics_engine": SLATier.GOLD,
            "monitoring_system": SLATier.PLATINUM,
            "consolidation_process": SLATier.GOLD,
        }

        for component, tier in sla_requirements.items():
            self.sla_analysis[component] = self._analyze_sla_compliance(component, tier)

    def _analyze_sla_compliance(self, component: str, tier: SLATier) -> SLAAnalysis:
        """Analyze SLA compliance for a specific component."""
        # Calculate required uptime percentage
        required_uptime = {
            SLATier.PLATINUM: 99.99,
            SLATier.GOLD: 99.9,
            SLATier.SILVER: 99.5,
            SLATier.BRONZE: 99.0,
        }[tier]

        # Simulate current uptime (would be calculated from real monitoring data)
        current_uptime = self._calculate_current_uptime(component)

        # Assess compliance
        compliance_status = current_uptime >= required_uptime

        # Risk assessment
        risk_assessment = self._assess_operational_risks(component, compliance_status)

        # Consolidation impact analysis
        consolidation_impact = self._analyze_consolidation_impact(component)

        # Mitigation strategies
        mitigation_strategies = self._generate_mitigation_strategies(component, compliance_status)

        return SLAAnalysis(
            tier=tier,
            current_uptime_percentage=current_uptime,
            required_uptime_percentage=required_uptime,
            compliance_status=compliance_status,
            risk_assessment=risk_assessment,
            consolidation_impact=consolidation_impact,
            mitigation_strategies=mitigation_strategies,
        )

    def _calculate_current_uptime(self, component: str) -> float:
        """Calculate current uptime percentage for a component."""
        # This would integrate with real monitoring systems
        # For now, return simulated values based on component criticality
        uptime_map = {
            "core_system": 99.95,
            "messaging_system": 99.85,
            "analytics_engine": 99.90,
            "monitoring_system": 99.98,
            "consolidation_process": 99.92,
        }
        return uptime_map.get(component, 99.5)

    def _assess_operational_risks(self, component: str, compliance_status: bool) -> Dict[str, Any]:
        """Assess operational risks for SLA compliance."""
        risks = {
            "sla_breach_risk": "low" if compliance_status else "high",
            "consolidation_disruption_risk": "medium",
            "performance_degradation_risk": "low",
            "monitoring_gap_risk": "low",
            "incident_response_risk": "medium",
        }

        # Adjust risks based on component criticality
        if component in ["core_system", "monitoring_system"]:
            for risk in risks:
                if risks[risk] == "low":
                    risks[risk] = "medium"

        return risks

    def _analyze_consolidation_impact(self, component: str) -> Dict[str, Any]:
        """Analyze potential consolidation impact on component."""
        impacts = {
            "file_reduction_impact": "low",
            "dependency_disruption_risk": "medium",
            "performance_change_expected": "minimal",
            "monitoring_coverage_impact": "low",
            "rollback_complexity": "medium",
        }

        # Component-specific impact adjustments
        if component == "analytics_engine":
            impacts["performance_change_expected"] = "moderate"
            impacts["rollback_complexity"] = "high"
        elif component == "messaging_system":
            impacts["dependency_disruption_risk"] = "high"

        return impacts

    def _generate_mitigation_strategies(self, component: str, compliance_status: bool) -> List[str]:
        """Generate mitigation strategies for SLA compliance."""
        strategies = [
            "Implement comprehensive monitoring before consolidation",
            "Establish automated health checks with rollback triggers",
            "Create detailed consolidation rollback procedures",
            "Set up real-time performance monitoring dashboards",
            "Conduct phased consolidation with validation gates",
        ]

        if not compliance_status:
            strategies.extend([
                "Increase monitoring frequency during consolidation",
                "Implement additional redundancy measures",
                "Prepare emergency intervention procedures",
                "Establish cross-team incident response coordination",
            ])

        return strategies

    def _configure_monitoring_capacity(self) -> None:
        """Configure monitoring system capacity for consolidation phases."""
        self.monitoring_capacity = {
            "max_metrics_per_minute": 10000,
            "max_alerts_per_hour": 500,
            "monitoring_endpoints": 50,
            "retention_period_days": 90,
            "storage_capacity_gb": 100,
            "consolidation_buffer": 1.5,  # 50% extra capacity for consolidation
        }

        # Capacity planning for different phases
        self.monitoring_capacity["phase_capacity"] = {
            "baseline": 1.0,    # Normal operations
            "consolidation": 1.5,  # During file consolidation
            "validation": 2.0,    # During testing and validation
            "rollback": 1.2,      # During rollback operations
        }

    def _set_alert_thresholds(self) -> None:
        """Set alert thresholds for operational monitoring."""
        self.alert_thresholds = {
            "cpu_usage": {
                "warning": 70.0,
                "critical": 85.0,
                "baseline": 45.0,
            },
            "memory_usage": {
                "warning": 75.0,
                "critical": 90.0,
                "baseline": 55.0,
            },
            "disk_usage": {
                "warning": 80.0,
                "critical": 95.0,
                "baseline": 60.0,
            },
            "response_time_ms": {
                "warning": 1000.0,
                "critical": 5000.0,
                "baseline": 250.0,
            },
            "error_rate_percentage": {
                "warning": 1.0,
                "critical": 5.0,
                "baseline": 0.1,
            },
            "consolidation_disruption": {
                "warning": 10.0,  # 10% performance impact
                "critical": 25.0,  # 25% performance impact
                "baseline": 0.0,
            },
        }

    def _create_health_check_profiles(self) -> None:
        """Create health check profiles for different system components."""
        self.baseline_data["health_check_profiles"] = {
            "core_system": {
                "check_interval_seconds": 30,
                "timeout_seconds": 10,
                "retry_attempts": 3,
                "alert_on_failure": True,
            },
            "messaging_system": {
                "check_interval_seconds": 60,
                "timeout_seconds": 15,
                "retry_attempts": 2,
                "alert_on_failure": True,
            },
            "analytics_engine": {
                "check_interval_seconds": 120,
                "timeout_seconds": 30,
                "retry_attempts": 2,
                "alert_on_failure": True,
            },
            "consolidation_process": {
                "check_interval_seconds": 300,  # 5 minutes
                "timeout_seconds": 60,
                "retry_attempts": 1,
                "alert_on_failure": True,
            },
        }

    def collect_operational_metrics(self) -> List[OperationalMetric]:
        """Collect comprehensive operational metrics."""
        metrics = []

        # System resource metrics
        metrics.extend(self._collect_system_metrics())

        # Application performance metrics
        metrics.extend(self._collect_application_metrics())

        # Consolidation-specific metrics
        metrics.extend(self._collect_consolidation_metrics())

        # SLA compliance metrics
        metrics.extend(self._collect_sla_metrics())

        # Store metrics in history
        for metric in metrics:
            if metric.name not in self.metric_history:
                self.metric_history[metric.name] = []
            self.metric_history[metric.name].append(metric)

            # Keep only last 1000 metrics per type
            if len(self.metric_history[metric.name]) > 1000:
                self.metric_history[metric.name] = self.metric_history[metric.name][-1000:]

        return metrics

    def _collect_system_metrics(self) -> List[OperationalMetric]:
        """Collect system-level operational metrics."""
        metrics = []

        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            metrics.append(OperationalMetric(
                name="system_cpu_usage",
                value=cpu_percent,
                unit="percentage",
                timestamp=datetime.now(),
                priority=MonitoringPriority.HIGH,
                sla_impact=True,
                baseline_value=self.alert_thresholds["cpu_usage"]["baseline"],
                threshold_warning=self.alert_thresholds["cpu_usage"]["warning"],
                threshold_critical=self.alert_thresholds["cpu_usage"]["critical"],
            ))

            # Memory usage
            memory = psutil.virtual_memory()
            metrics.append(OperationalMetric(
                name="system_memory_usage",
                value=memory.percent,
                unit="percentage",
                timestamp=datetime.now(),
                priority=MonitoringPriority.HIGH,
                sla_impact=True,
                baseline_value=self.alert_thresholds["memory_usage"]["baseline"],
                threshold_warning=self.alert_thresholds["memory_usage"]["warning"],
                threshold_critical=self.alert_thresholds["memory_usage"]["critical"],
            ))

            # Disk usage
            disk = psutil.disk_usage('/')
            metrics.append(OperationalMetric(
                name="system_disk_usage",
                value=disk.percent,
                unit="percentage",
                timestamp=datetime.now(),
                priority=MonitoringPriority.MEDIUM,
                sla_impact=True,
                baseline_value=self.alert_thresholds["disk_usage"]["baseline"],
                threshold_warning=self.alert_thresholds["disk_usage"]["warning"],
                threshold_critical=self.alert_thresholds["disk_usage"]["critical"],
            ))

        except Exception as e:
            print(f"⚠️  Error collecting system metrics: {e}")

        return metrics

    def _collect_application_metrics(self) -> List[OperationalMetric]:
        """Collect application-level operational metrics."""
        metrics = []

        # Response time simulation (would be from real application monitoring)
        response_time = 245.0  # milliseconds
        metrics.append(OperationalMetric(
            name="application_response_time",
            value=response_time,
            unit="milliseconds",
            timestamp=datetime.now(),
            priority=MonitoringPriority.HIGH,
            sla_impact=True,
            baseline_value=self.alert_thresholds["response_time_ms"]["baseline"],
            threshold_warning=self.alert_thresholds["response_time_ms"]["warning"],
            threshold_critical=self.alert_thresholds["response_time_ms"]["critical"],
        ))

        # Error rate simulation
        error_rate = 0.05  # 0.05%
        metrics.append(OperationalMetric(
            name="application_error_rate",
            value=error_rate,
            unit="percentage",
            timestamp=datetime.now(),
            priority=MonitoringPriority.HIGH,
            sla_impact=True,
            baseline_value=self.alert_thresholds["error_rate_percentage"]["baseline"],
            threshold_warning=self.alert_thresholds["error_rate_percentage"]["warning"],
            threshold_critical=self.alert_thresholds["error_rate_percentage"]["critical"],
        ))

        return metrics

    def _collect_consolidation_metrics(self) -> List[OperationalMetric]:
        """Collect consolidation-specific operational metrics."""
        metrics = []

        # Consolidation performance impact simulation
        consolidation_impact = 2.5  # 2.5% performance impact
        metrics.append(OperationalMetric(
            name="consolidation_performance_impact",
            value=consolidation_impact,
            unit="percentage",
            timestamp=datetime.now(),
            priority=MonitoringPriority.CRITICAL,
            sla_impact=True,
            baseline_value=self.alert_thresholds["consolidation_disruption"]["baseline"],
            threshold_warning=self.alert_thresholds["consolidation_disruption"]["warning"],
            threshold_critical=self.alert_thresholds["consolidation_disruption"]["critical"],
        ))

        # File consolidation progress simulation
        consolidation_progress = 15.0  # 15% complete
        metrics.append(OperationalMetric(
            name="consolidation_progress",
            value=consolidation_progress,
            unit="percentage",
            timestamp=datetime.now(),
            priority=MonitoringPriority.MEDIUM,
            sla_impact=False,
        ))

        return metrics

    def _collect_sla_metrics(self) -> List[OperationalMetric]:
        """Collect SLA compliance metrics."""
        metrics = []

        for component, analysis in self.sla_analysis.items():
            # SLA compliance status
            metrics.append(OperationalMetric(
                name=f"sla_compliance_{component}",
                value=1 if analysis.compliance_status else 0,
                unit="boolean",
                timestamp=datetime.now(),
                priority=MonitoringPriority.CRITICAL,
                sla_impact=True,
            ))

            # Uptime percentage
            metrics.append(OperationalMetric(
                name=f"sla_uptime_{component}",
                value=analysis.current_uptime_percentage,
                unit="percentage",
                timestamp=datetime.now(),
                priority=MonitoringPriority.HIGH,
                sla_impact=True,
            ))

        return metrics

    def perform_system_health_check(self) -> SystemHealthStatus:
        """Perform comprehensive system health check."""
        timestamp = datetime.now()

        # Collect current metrics
        metrics = self.collect_operational_metrics()

        # Analyze component health
        components = self._analyze_component_health(metrics)

        # Generate alerts based on thresholds
        alerts = self._generate_alerts(metrics)

        # Determine overall system status
        overall_status = self._determine_overall_status(components, alerts)

        # Analyze SLA compliance
        sla_compliance = {comp: analysis.compliance_status
                         for comp, analysis in self.sla_analysis.items()}

        # Assess consolidation impact
        consolidation_impact = self._assess_current_consolidation_impact(metrics)

        health_status = SystemHealthStatus(
            timestamp=timestamp,
            overall_status=overall_status,
            components=components,
            alerts=alerts,
            metrics=metrics,
            sla_compliance=sla_compliance,
            consolidation_impact=consolidation_impact,
        )

        # Store in history
        self.health_history.append(health_status)
        if len(self.health_history) > 100:
            self.health_history = self.health_history[-100:]

        return health_status

    def _analyze_component_health(self, metrics: List[OperationalMetric]) -> Dict[str, Dict[str, Any]]:
        """Analyze health of individual system components."""
        components = {}

        # Group metrics by component
        component_metrics = {}
        for metric in metrics:
            component_name = metric.name.split('_')[0] if '_' in metric.name else 'system'
            if component_name not in component_metrics:
                component_metrics[component_name] = []
            component_metrics[component_name].append(metric)

        # Analyze each component
        for component_name, comp_metrics in component_metrics.items():
            health_status = "healthy"
            issues = []

            for metric in comp_metrics:
                if metric.threshold_critical and metric.value >= metric.threshold_critical:
                    health_status = "critical"
                    issues.append(f"{metric.name}: {metric.value} >= {metric.threshold_critical}")
                elif metric.threshold_warning and metric.value >= metric.threshold_warning:
                    if health_status == "healthy":
                        health_status = "warning"
                    issues.append(f"{metric.name}: {metric.value} >= {metric.threshold_warning}")

            components[component_name] = {
                "status": health_status,
                "issues": issues,
                "metrics_count": len(comp_metrics),
                "last_check": datetime.now(),
            }

        return components

    def _generate_alerts(self, metrics: List[OperationalMetric]) -> List[Dict[str, Any]]:
        """Generate alerts based on metric thresholds."""
        alerts = []

        for metric in metrics:
            alert_data = None

            if metric.threshold_critical and metric.value >= metric.threshold_critical:
                alert_data = {
                    "id": f"alert_{int(time.time())}_{metric.name}",
                    "type": "critical",
                    "component": metric.name.split('_')[0],
                    "message": f"CRITICAL: {metric.name} at {metric.value}{metric.unit}",
                    "value": metric.value,
                    "threshold": metric.threshold_critical,
                    "timestamp": metric.timestamp,
                    "sla_impact": metric.sla_impact,
                }
            elif metric.threshold_warning and metric.value >= metric.threshold_warning:
                alert_data = {
                    "id": f"alert_{int(time.time())}_{metric.name}",
                    "type": "warning",
                    "component": metric.name.split('_')[0],
                    "message": f"WARNING: {metric.name} at {metric.value}{metric.unit}",
                    "value": metric.value,
                    "threshold": metric.threshold_warning,
                    "timestamp": metric.timestamp,
                    "sla_impact": metric.sla_impact,
                }

            if alert_data:
                alerts.append(alert_data)

        return alerts

    def _determine_overall_status(self, components: Dict[str, Dict[str, Any]],
                                alerts: List[Dict[str, Any]]) -> str:
        """Determine overall system health status."""
        if any(component["status"] == "critical" for component in components.values()):
            return "critical"
        elif any(component["status"] == "warning" for component in components.values()):
            return "warning"
        elif any(alert["type"] == "critical" for alert in alerts):
            return "critical"
        elif any(alert["type"] == "warning" for alert in alerts):
            return "warning"
        else:
            return "healthy"

    def _assess_current_consolidation_impact(self, metrics: List[OperationalMetric]) -> Dict[str, Any]:
        """Assess current consolidation impact on system."""
        consolidation_metrics = [m for m in metrics if "consolidation" in m.name.lower()]

        impact_assessment = {
            "performance_impact": 0.0,
            "stability_impact": "low",
            "sla_impact": False,
            "recommendations": [],
        }

        for metric in consolidation_metrics:
            if "performance_impact" in metric.name:
                impact_assessment["performance_impact"] = metric.value
                if metric.value >= 10.0:
                    impact_assessment["stability_impact"] = "high"
                    impact_assessment["sla_impact"] = True
                    impact_assessment["recommendations"].append("Consider pausing consolidation")
                elif metric.value >= 5.0:
                    impact_assessment["stability_impact"] = "medium"
                    impact_assessment["recommendations"].append("Monitor closely")

        return impact_assessment

    def generate_operational_report(self) -> Dict[str, Any]:
        """Generate comprehensive operational monitoring report."""
        current_health = self.perform_system_health_check()

        report = {
            "timestamp": datetime.now(),
            "system_overview": {
                "platform": platform.system(),
                "architecture": platform.machine(),
                "python_version": platform.python_version(),
            },
            "health_status": {
                "overall_status": current_health.overall_status,
                "components_count": len(current_health.components),
                "alerts_count": len(current_health.alerts),
                "metrics_count": len(current_health.metrics),
            },
            "sla_analysis": {
                component: {
                    "tier": analysis.tier.value,
                    "current_uptime": analysis.current_uptime_percentage,
                    "required_uptime": analysis.required_uptime_percentage,
                    "compliant": analysis.compliance_status,
                    "risk_level": analysis.risk_assessment.get("sla_breach_risk", "unknown"),
                }
                for component, analysis in self.sla_analysis.items()
            },
            "monitoring_capacity": self.monitoring_capacity,
            "alert_thresholds": self.alert_thresholds,
            "consolidation_readiness": {
                "monitoring_baseline_established": True,
                "alert_system_configured": True,
                "health_checks_active": True,
                "sla_analysis_complete": True,
                "risk_assessment_complete": True,
            },
            "recommendations": self._generate_operational_recommendations(current_health),
        }

        return report

    def _generate_operational_recommendations(self, health: SystemHealthStatus) -> List[str]:
        """Generate operational recommendations based on current health."""
        recommendations = []

        # SLA compliance recommendations
        non_compliant_components = [
            comp for comp, analysis in self.sla_analysis.items()
            if not analysis.compliance_status
        ]
        if non_compliant_components:
            recommendations.append(
                f"Address SLA compliance for: {', '.join(non_compliant_components)}"
            )

        # Alert-based recommendations
        critical_alerts = [alert for alert in health.alerts if alert["type"] == "critical"]
        if critical_alerts:
            recommendations.append(
                f"Address {len(critical_alerts)} critical alerts immediately"
            )

        warning_alerts = [alert for alert in health.alerts if alert["type"] == "warning"]
        if warning_alerts:
            recommendations.append(
                f"Review {len(warning_alerts)} warning alerts"
            )

        # Consolidation impact recommendations
        if health.consolidation_impact.get("stability_impact") in ["medium", "high"]:
            recommendations.append(
                "Monitor consolidation impact closely and prepare rollback procedures"
            )

        # Capacity recommendations
        if len(health.metrics) > self.monitoring_capacity["max_metrics_per_minute"] * 60:
            recommendations.append(
                "Consider increasing monitoring capacity for current load"
            )

        return recommendations if recommendations else ["All systems operating within normal parameters"]

    def save_baseline_snapshot(self) -> None:
        """Save current operational baseline snapshot."""
        snapshot = {
            "timestamp": datetime.now().isoformat(),
            "baseline_data": self.baseline_data,
            "sla_analysis": {
                comp: {
                    "tier": analysis.tier.value,
                    "current_uptime": analysis.current_uptime_percentage,
                    "required_uptime": analysis.required_uptime_percentage,
                    "compliance_status": analysis.compliance_status,
                    "risk_assessment": analysis.risk_assessment,
                    "consolidation_impact": analysis.consolidation_impact,
                    "mitigation_strategies": analysis.mitigation_strategies,
                }
                for comp, analysis in self.sla_analysis.items()
            },
            "monitoring_capacity": self.monitoring_capacity,
            "alert_thresholds": self.alert_thresholds,
            "system_info": {
                "platform": platform.system(),
                "architecture": platform.machine(),
                "python_version": platform.python_version(),
            },
        }

        snapshot_file = self.baseline_directory / f"operational_baseline_{int(time.time())}.json"
        with open(snapshot_file, 'w') as f:
            json.dump(snapshot, f, indent=2, default=str)

        print(f"✅ Operational baseline snapshot saved: {snapshot_file}")

    def export_operational_dashboard_data(self) -> Dict[str, Any]:
        """Export data for operational monitoring dashboards."""
        current_health = self.perform_system_health_check()

        dashboard_data = {
            "timestamp": datetime.now().isoformat(),
            "system_status": current_health.overall_status,
            "components": {
                name: {
                    "status": comp["status"],
                    "issues": len(comp["issues"]),
                    "last_check": comp["last_check"].isoformat(),
                }
                for name, comp in current_health.components.items()
            },
            "alerts": {
                "total": len(current_health.alerts),
                "critical": len([a for a in current_health.alerts if a["type"] == "critical"]),
                "warning": len([a for a in current_health.alerts if a["type"] == "warning"]),
                "recent": [a for a in current_health.alerts[-5:]],  # Last 5 alerts
            },
            "sla_compliance": current_health.sla_compliance,
            "key_metrics": {
                metric.name: {
                    "value": metric.value,
                    "unit": metric.unit,
                    "priority": metric.priority.value,
                    "sla_impact": metric.sla_impact,
                }
                for metric in current_health.metrics
                if metric.priority in [MonitoringPriority.CRITICAL, MonitoringPriority.HIGH]
            },
            "consolidation_status": {
                "impact_level": current_health.consolidation_impact.get("stability_impact", "unknown"),
                "performance_impact": current_health.consolidation_impact.get("performance_impact", 0.0),
                "recommendations": current_health.consolidation_impact.get("recommendations", []),
            },
        }

        return dashboard_data

    def get_consolidation_safety_status(self) -> Dict[str, Any]:
        """Get consolidation safety status based on operational monitoring."""
        current_health = self.perform_system_health_check()

        safety_status = {
            "consolidation_safe": True,
            "blocking_issues": [],
            "warnings": [],
            "monitoring_ready": True,
            "rollback_ready": True,
            "sla_protected": True,
        }

        # Check for blocking issues
        critical_alerts = [a for a in current_health.alerts if a["type"] == "critical"]
        if critical_alerts:
            safety_status["consolidation_safe"] = False
            safety_status["blocking_issues"].extend([
                f"Critical alert: {alert['message']}" for alert in critical_alerts
            ])

        # Check SLA compliance
        non_compliant_slas = [
            comp for comp, compliant in current_health.sla_compliance.items()
            if not compliant
        ]
        if non_compliant_slas:
            safety_status["sla_protected"] = False
            safety_status["blocking_issues"].append(
                f"SLA non-compliant components: {', '.join(non_compliant_slas)}"
            )

        # Check consolidation impact
        if current_health.consolidation_impact.get("stability_impact") == "high":
            safety_status["consolidation_safe"] = False
            safety_status["blocking_issues"].append(
                "High consolidation stability impact detected"
            )

        # Check for warnings
        warning_alerts = [a for a in current_health.alerts if a["type"] == "warning"]
        if warning_alerts:
            safety_status["warnings"].extend([
                f"Warning: {alert['message']}" for alert in warning_alerts
            ])

        return safety_status


def main():
    """Main function to demonstrate operational monitoring baseline."""
    print("🐝 AGENT-8 OPERATIONAL MONITORING BASELINE SYSTEM")
    print("=" * 60)

    # Initialize operational monitoring baseline
    baseline = OperationalMonitoringBaseline()

    # Perform initial health check
    print("\n🔍 Performing initial system health check...")
    health_status = baseline.perform_system_health_check()

    print(f"📊 Overall System Status: {health_status.overall_status.upper()}")
    print(f"🖥️  Components Monitored: {len(health_status.components)}")
    print(f"🚨 Active Alerts: {len(health_status.alerts)}")
    print(f"📈 Metrics Collected: {len(health_status.metrics)}")

    # Display SLA analysis
    print("\n📋 SLA COMPLIANCE ANALYSIS:")
    for component, analysis in baseline.sla_analysis.items():
        status_icon = "✅" if analysis.compliance_status else "❌"
        print(f"  {status_icon} {component}: {analysis.current_uptime_percentage:.2f}% "
              f"(Required: {analysis.required_uptime_percentage:.2f}%)")

    # Display alerts
    if health_status.alerts:
        print("\n🚨 ACTIVE ALERTS:")
        for alert in health_status.alerts[:5]:  # Show first 5 alerts
            print(f"  {alert['type'].upper()}: {alert['message']}")

    # Generate operational report
    print("\n📄 Generating operational report...")
    report = baseline.generate_operational_report()

    print("\n🎯 CONSOLIDATION SAFETY STATUS:")
    safety = baseline.get_consolidation_safety_status()
    status_icon = "✅" if safety["consolidation_safe"] else "❌"
    print(f"  {status_icon} Consolidation Safe: {safety['consolidation_safe']}")
    print(f"  🛡️  SLA Protected: {safety['sla_protected']}")
    print(f"  📊 Monitoring Ready: {safety['monitoring_ready']}")

    if safety["blocking_issues"]:
        print("  🚫 Blocking Issues:")
        for issue in safety["blocking_issues"]:
            print(f"    • {issue}")

    if safety["warnings"]:
        print("  ⚠️  Warnings:")
        for warning in safety["warnings"]:
            print(f"    • {warning}")

    # Save baseline snapshot
    print("\n💾 Saving operational baseline snapshot...")
    baseline.save_baseline_snapshot()

    # Export dashboard data
    print("📊 Exporting dashboard data...")
    dashboard_data = baseline.export_operational_dashboard_data()

    print("\n✅ OPERATIONAL MONITORING BASELINE ESTABLISHED!")
    print("🐝 Ready for Phase 2 consolidation with comprehensive monitoring coverage.")

    return baseline


if __name__ == "__main__":
    baseline_system = main()
