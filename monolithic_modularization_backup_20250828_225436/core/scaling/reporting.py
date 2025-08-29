"""Scaling report generation utilities."""

import logging
from collections import defaultdict
from datetime import datetime
from typing import Any, Dict

from .patterns import analyze_scaling_patterns

logger = logging.getLogger(__name__)


def generate_scaling_report(manager: Any, report_type: str = "comprehensive") -> Dict[str, Any]:
    """Generate comprehensive scaling report."""
    try:
        report: Dict[str, Any] = {
            "report_id": f"scaling_report_{int(datetime.now().timestamp())}",
            "generated_at": datetime.now().isoformat(),
            "report_type": report_type,
            "summary": {},
            "detailed_metrics": {},
            "scaling_summary": {},
            "recommendations": [],
        }
        total_metrics = len(manager.metrics_history)
        total_decisions = len(manager.decision_history)
        active_alerts = len(manager.performance_alerts)
        report["summary"] = {
            "total_metrics_recorded": total_metrics,
            "total_scaling_decisions": total_decisions,
            "active_performance_alerts": active_alerts,
            "current_instances": manager.current_instances,
            "target_instances": manager.target_instances,
            "scaling_status": manager.scaling_status.value,
        }
        if manager.metrics_history:
            latest = manager.metrics_history[-1]
            report["detailed_metrics"] = {
                "current_instances": latest.current_instances,
                "target_instances": latest.target_instances,
                "cpu_utilization": latest.cpu_utilization,
                "memory_utilization": latest.memory_utilization,
                "response_time": latest.response_time,
                "throughput": latest.throughput,
                "error_rate": latest.error_rate,
            }
        if manager.decision_history:
            recent = manager.decision_history[-10:]
            counts = defaultdict(int)
            for decision in recent:
                counts[decision.action] += 1
            report["scaling_summary"] = {
                "recent_actions": dict(counts),
                "average_confidence": sum(d.confidence for d in recent) / len(recent),
                "scaling_frequency": len(recent),
            }
        if active_alerts > 0:
            report["recommendations"].append(
                f"Address {active_alerts} active performance alerts"
            )
        pattern_analysis = analyze_scaling_patterns(manager)
        if pattern_analysis.get("scaling_efficiency", 1.0) < 0.8:
            report["recommendations"].append(
                "Low scaling efficiency - review decision algorithms"
            )
        if manager.metrics_history:
            latest = manager.metrics_history[-1]
            if latest.cpu_utilization > 80 or latest.memory_utilization > 85:
                report["recommendations"].append(
                    "High resource utilization - consider scaling up"
                )
        logger.info("Scaling report generated: %s", report["report_id"])
        return report
    except Exception as exc:  # pragma: no cover - defensive
        logger.error("Failed to generate scaling report: %s", exc)
        return {"error": str(exc)}
