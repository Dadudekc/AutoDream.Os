"""
ML Learning Coordinator Services
===============================

Service functionality for ML learning coordination operations.
V2 Compliance: < 300 lines, single responsibility, service logic.

Author: Agent-3 - Infrastructure & DevOps Specialist
Mission: V2 Compliance Refactoring
"""

import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from .models import (
    LearningPattern,
    MLPrediction,
    ModelState,
    MLOptimizationMetrics,
    FeatureAnalysis,
    LearningSession,
    LearningStatus,
    ModelType,
    FeatureType,
)
from ...ml_optimizer_models import MLConfiguration
from .coordinator_core import MLLearningCoordinatorCore


class MLLearningCoordinatorServices:
    """Service functionality for ML learning coordination operations."""

    def __init__(self, coordinator_core: MLLearningCoordinatorCore):
        """Initialize ML learning coordinator services."""
        self.coordinator_core = coordinator_core
        self.logger = logging.getLogger(__name__)
        self.is_initialized = False

    def initialize(self) -> bool:
        """Initialize the coordinator services."""
        try:
            if not self.coordinator_core.is_initialized:
                raise Exception("Coordinator core not initialized")

            self.is_initialized = True
            self.logger.info("ML Learning Coordinator Services initialized")
            return True
        except Exception as e:
            self.logger.error(
                f"Failed to initialize ML Learning Coordinator Services: {e}"
            )
            return False

    def analyze_learning_progress(self, session_id: str) -> Dict[str, Any]:
        """Analyze learning progress for a session."""
        try:
            if not self.is_initialized:
                raise RuntimeError("Coordinator services not initialized")

            session = self.coordinator_core.get_learning_session(session_id)
            if not session:
                return {"error": f"Session {session_id} not found"}

            # Get model states for this session
            model_states = self.coordinator_core.get_model_states_by_session(session_id)

            # Get optimization metrics for this session
            metrics = self.coordinator_core.get_optimization_metrics_by_session(
                session_id
            )

            # Calculate progress metrics
            total_states = len(model_states)
            recent_states = [
                state
                for state in model_states
                if state.created_at >= datetime.now() - timedelta(hours=1)
            ]

            avg_accuracy = 0
            if metrics:
                avg_accuracy = sum(m.accuracy for m in metrics) / len(metrics)

            return {
                "session_id": session_id,
                "total_model_states": total_states,
                "recent_states": len(recent_states),
                "average_accuracy": avg_accuracy,
                "learning_status": session.status.value,
                "created_at": session.created_at.isoformat(),
                "analysis_timestamp": datetime.now().isoformat(),
            }

        except Exception as e:
            self.logger.error(f"Error analyzing learning progress: {e}")
            return {"error": str(e)}

    def generate_learning_report(self, session_id: str = None) -> Dict[str, Any]:
        """Generate learning report."""
        try:
            if not self.is_initialized:
                raise RuntimeError("Coordinator services not initialized")

            if session_id:
                sessions = [self.coordinator_core.get_learning_session(session_id)]
                if not sessions[0]:
                    return {"error": f"Session {session_id} not found"}
            else:
                sessions = self.coordinator_core.get_active_sessions()

            if not sessions:
                return {"message": "No active sessions found"}

            # Generate report data
            report_data = {
                "report_type": "learning_analysis",
                "total_sessions": len(sessions),
                "generated_at": datetime.now().isoformat(),
                "sessions": [],
            }

            for session in sessions:
                session_data = {
                    "session_id": session.session_id,
                    "model_type": session.model_type.value,
                    "status": session.status.value,
                    "created_at": session.created_at.isoformat(),
                    "progress": self.analyze_learning_progress(session.session_id),
                }
                report_data["sessions"].append(session_data)

            self.logger.info(f"Generated learning report for {len(sessions)} sessions")
            return report_data

        except Exception as e:
            self.logger.error(f"Error generating learning report: {e}")
            return {"error": str(e)}

    def optimize_learning_parameters(self, session_id: str) -> Dict[str, Any]:
        """Optimize learning parameters for a session."""
        try:
            if not self.is_initialized:
                raise RuntimeError("Coordinator services not initialized")

            session = self.coordinator_core.get_learning_session(session_id)
            if not session:
                return {"error": f"Session {session_id} not found"}

            # Get recent optimization metrics
            metrics = self.coordinator_core.get_optimization_metrics_by_session(
                session_id
            )
            recent_metrics = [
                m
                for m in metrics
                if m.created_at >= datetime.now() - timedelta(hours=1)
            ]

            if not recent_metrics:
                return {"message": "No recent metrics available for optimization"}

            # Calculate optimization suggestions
            avg_accuracy = sum(m.accuracy for m in recent_metrics) / len(recent_metrics)
            avg_loss = sum(m.loss for m in recent_metrics) / len(recent_metrics)

            optimization_suggestions = []

            if avg_accuracy < 0.8:
                optimization_suggestions.append("Consider increasing learning rate")
                optimization_suggestions.append("Review feature selection")

            if avg_loss > 0.5:
                optimization_suggestions.append("Consider reducing learning rate")
                optimization_suggestions.append("Check for overfitting")

            return {
                "session_id": session_id,
                "average_accuracy": avg_accuracy,
                "average_loss": avg_loss,
                "optimization_suggestions": optimization_suggestions,
                "metrics_analyzed": len(recent_metrics),
                "generated_at": datetime.now().isoformat(),
            }

        except Exception as e:
            self.logger.error(f"Error optimizing learning parameters: {e}")
            return {"error": str(e)}

    def monitor_learning_health(self) -> Dict[str, Any]:
        """Monitor learning system health."""
        try:
            if not self.is_initialized:
                raise RuntimeError("Coordinator services not initialized")

            active_sessions = self.coordinator_core.get_active_sessions()

            # Calculate health metrics
            total_sessions = len(active_sessions)
            healthy_sessions = 0
            warning_sessions = 0
            critical_sessions = 0

            for session in active_sessions:
                progress = self.analyze_learning_progress(session.session_id)
                if "error" in progress:
                    critical_sessions += 1
                elif progress.get("average_accuracy", 0) < 0.6:
                    warning_sessions += 1
                else:
                    healthy_sessions += 1

            health_score = (
                (healthy_sessions / total_sessions) if total_sessions > 0 else 0
            )

            return {
                "total_sessions": total_sessions,
                "healthy_sessions": healthy_sessions,
                "warning_sessions": warning_sessions,
                "critical_sessions": critical_sessions,
                "health_score": health_score,
                "overall_status": (
                    "healthy"
                    if health_score > 0.8
                    else "warning" if health_score > 0.5 else "critical"
                ),
                "monitored_at": datetime.now().isoformat(),
            }

        except Exception as e:
            self.logger.error(f"Error monitoring learning health: {e}")
            return {"error": str(e)}

    def get_services_status(self) -> Dict[str, Any]:
        """Get services status."""
        if not self.is_initialized:
            return {"status": "not_initialized"}

        return {
            "status": "initialized",
            "coordinator_core_initialized": self.coordinator_core.is_initialized,
            "services_type": "ml_learning_coordination",
        }

    def shutdown(self):
        """Shutdown coordinator services."""
        if not self.is_initialized:
            return

        self.logger.info("Shutting down ML Learning Coordinator Services")
        self.is_initialized = False
