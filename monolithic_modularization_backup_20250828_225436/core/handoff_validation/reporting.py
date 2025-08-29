"""Reporting helpers for handoff validation."""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from .rules import ValidationSession, ValidationStatus

logger = logging.getLogger(__name__)


def update_validation_metrics(
    metrics: Dict[str, Any], session: ValidationSession
) -> None:
    """Update aggregate metrics using results from ``session``."""
    metrics["total_sessions"] += 1
    if session.overall_status == ValidationStatus.PASSED:
        metrics["successful_sessions"] += 1
    else:
        metrics["failed_sessions"] += 1

    if session.duration:
        metrics["total_duration"] += session.duration
        metrics["average_duration"] = (
            metrics["total_duration"] / metrics["total_sessions"]
        )

    for result in session.results:
        rule_id = result.rule_id
        rule_stats = metrics.setdefault("rule_success_rates", {}).setdefault(
            rule_id, {"total": 0, "passed": 0, "failed": 0}
        )
        rule_stats["total"] += 1
        if result.status == ValidationStatus.PASSED:
            rule_stats["passed"] += 1
        else:
            rule_stats["failed"] += 1

        severity = result.severity.value
        sev_stats = metrics.setdefault("severity_distribution", {}).setdefault(
            severity, {"total": 0, "passed": 0, "failed": 0}
        )
        sev_stats["total"] += 1
        if result.status == ValidationStatus.PASSED:
            sev_stats["passed"] += 1
        else:
            sev_stats["failed"] += 1


def validation_status(
    session_id: str,
    active_sessions: Dict[str, ValidationSession],
    history: List[ValidationSession],
) -> Optional[Dict[str, Any]]:
    """Return status information for ``session_id``."""
    session = active_sessions.get(session_id)
    if session:
        return {
            "session_id": session.session_id,
            "handoff_id": session.handoff_id,
            "procedure_id": session.procedure_id,
            "status": session.overall_status.value,
            "progress": len(session.results) / len(session.rules)
            if session.rules
            else 0.0,
            "start_time": session.start_time,
            "rules_total": len(session.rules),
            "rules_completed": len(session.results),
        }

    for past in history:
        if past.session_id == session_id:
            return {
                "session_id": past.session_id,
                "handoff_id": past.handoff_id,
                "procedure_id": past.procedure_id,
                "status": past.overall_status.value,
                "validation_score": past.validation_score,
                "start_time": past.start_time,
                "end_time": past.end_time,
                "duration": past.duration,
                "critical_failures": past.critical_failures,
                "high_failures": past.high_failures,
                "medium_failures": past.medium_failures,
                "low_failures": past.low_failures,
            }
    return None


def system_status(
    metrics: Dict[str, Any],
    active_sessions: Dict[str, ValidationSession],
    available_rules: List[str],
) -> Dict[str, Any]:
    """Return overall system status using the provided ``metrics``."""
    try:
        success_rate = (
            metrics["successful_sessions"] / metrics["total_sessions"]
            if metrics["total_sessions"]
            else 0.0
        )
        return {
            "system_status": "operational",
            "active_sessions": len(active_sessions),
            "total_sessions": metrics["total_sessions"],
            "success_rate": success_rate,
            "average_duration": metrics["average_duration"],
            "available_rules": available_rules,
            "rule_success_rates": metrics.get("rule_success_rates", {}),
            "severity_distribution": metrics.get("severity_distribution", {}),
        }
    except Exception as exc:  # pragma: no cover - defensive programming
        logger.error("Failed to compile system status: %s", exc)
        return {"error": str(exc)}
