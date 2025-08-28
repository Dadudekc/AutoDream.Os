from __future__ import annotations

from typing import Any, Dict, List, Optional

from .metrics import TestConfiguration, TestSession
from .utils import safe_divide


def generate_test_status(
    session_id: str,
    active_sessions: Dict[str, TestSession],
    test_history: List[TestSession],
) -> Optional[Dict[str, Any]]:
    """Generate status information for a test session."""

    if session_id in active_sessions:
        session = active_sessions[session_id]
        return {
            "session_id": session.session_id,
            "test_config_id": session.test_config.test_id,
            "test_type": session.test_config.test_type.value,
            "status": session.status.value,
            "progress": safe_divide(session.current_iteration, session.test_config.iterations)
            if session.test_config.iterations > 0
            else 0.0,
            "start_time": session.start_time,
            "iterations_total": session.test_config.iterations,
            "iterations_completed": session.current_iteration,
        }

    for test_session in test_history:
        if test_session.session_id == session_id:
            return {
                "session_id": test_session.session_id,
                "test_config_id": test_session.test_config.test_id,
                "test_type": test_session.test_config.test_type.value,
                "status": test_session.status.value,
                "start_time": test_session.start_time,
                "end_time": test_session.end_time,
                "duration": (test_session.end_time - test_session.start_time)
                if test_session.end_time
                else None,
                "error_details": test_session.error_details,
                "results_count": len(test_session.results),
            }

    return None


def generate_system_status(
    reliability_metrics: Dict[str, Any],
    active_sessions: Dict[str, TestSession],
    test_configurations: Dict[str, TestConfiguration],
) -> Dict[str, Any]:
    """Generate an overall system status report."""

    return {
        "system_status": "operational",
        "active_sessions": len(active_sessions),
        "total_tests": reliability_metrics["total_tests"],
        "success_rate": safe_divide(
            reliability_metrics["successful_tests"], reliability_metrics["total_tests"]
        ),
        "total_iterations": reliability_metrics["total_iterations"],
        "iteration_success_rate": safe_divide(
            reliability_metrics["successful_iterations"],
            reliability_metrics["total_iterations"],
        ),
        "average_success_rate": reliability_metrics["average_success_rate"],
        "average_duration": reliability_metrics["average_duration"],
        "available_configurations": list(test_configurations.keys()),
        "test_type_performance": reliability_metrics["test_type_performance"],
    }
