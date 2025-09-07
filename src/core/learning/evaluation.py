#!/usr/bin/env python3
"""Evaluation utilities for UnifiedLearningEngine."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional

from .models import LearningPattern, LearningStatus
from .decision_models import DecisionType
from . import models as learning_models
from .trainer import add_learning_data, make_decision


def identify_learning_patterns(
    engine: "UnifiedLearningEngine", agent_id: str, session_id: str
) -> List[LearningPattern]:
    """Identify learning patterns from session data."""
    try:
        if session_id not in engine.learning_sessions:
            return []
        session = engine.learning_sessions[session_id]
        patterns: List[LearningPattern] = []
        if not session.session_data:
            return patterns
        performance_scores = [data.performance_score for data in session.session_data]
        if len(performance_scores) >= 3:
            if performance_scores[-1] > performance_scores[0]:
                improvement_pattern = LearningPattern(
                    pattern_type="performance_improvement",
                    confidence_score=0.8,
                    supporting_data=[
                        f"Score improved from {performance_scores[0]} to {performance_scores[-1]}"
                    ],
                    frequency=1,
                )
                patterns.append(improvement_pattern)
            if max(performance_scores) - min(performance_scores) < 10:
                consistency_pattern = LearningPattern(
                    pattern_type="performance_consistency",
                    confidence_score=0.7,
                    supporting_data=["Performance scores show low variance"],
                    frequency=1,
                )
                patterns.append(consistency_pattern)
        for pattern in patterns:
            pattern_id = str(uuid.uuid4())
            pattern.pattern_id = pattern_id
            engine.learning_patterns[pattern_id] = pattern
        engine.logger.info(
            f"Identified {len(patterns)} learning patterns for session {session_id}"
        )
        return patterns
    except Exception as exc:  # pragma: no cover - log and return
        engine.logger.error(f"Failed to identify learning patterns: {exc}")
        return []


def get_learning_performance_summary(
    engine: "UnifiedLearningEngine", agent_id: str
) -> Dict[str, Any]:
    """Get comprehensive learning performance summary for an agent."""
    try:
        summary = {
            "agent_id": agent_id,
            "total_sessions": 0,
            "active_sessions": 0,
            "total_learning_goals": 0,
            "completed_goals": 0,
            "average_performance": 0.0,
            "learning_patterns": [],
            "recent_metrics": {},
        }
        agent_sessions = [
            s for s in engine.learning_sessions.values() if s.agent_id == agent_id
        ]
        summary["total_sessions"] = len(agent_sessions)
        summary["active_sessions"] = len(
            [s for s in agent_sessions if s.session_id in engine.active_sessions]
        )
        agent_goals = [
            g for g in engine.learning_goals.values() if g.agent_id == agent_id
        ]
        summary["total_learning_goals"] = len(agent_goals)
        summary["completed_goals"] = len(
            [g for g in agent_goals if g.status == LearningStatus.COMPLETED]
        )
        all_scores: List[float] = []
        for session in agent_sessions:
            for data in session.session_data:
                all_scores.append(data.performance_score)
        if all_scores:
            summary["average_performance"] = sum(all_scores) / len(all_scores)
        agent_patterns = [
            p
            for p in engine.learning_patterns.values()
            if p.pattern_id.startswith(agent_id)
        ]
        summary["learning_patterns"] = [p.pattern_type for p in agent_patterns]
        agent_metrics = [
            m for m in engine.learning_metrics.values() if m.agent_id == agent_id
        ]
        if agent_metrics:
            latest_metric = max(agent_metrics, key=lambda m: m.last_updated)
            summary["recent_metrics"] = {
                "metric_name": latest_metric.metric_name,
                "average_value": latest_metric.average_value,
                "trend": latest_metric.trend,
                "last_updated": latest_metric.last_updated.isoformat(),
            }
        return summary
    except Exception as exc:  # pragma: no cover - log and return
        engine.logger.error(f"Failed to get learning performance summary: {exc}")
        return {"error": str(exc)}


def get_engine_status(engine: "UnifiedLearningEngine") -> Dict[str, Any]:
    """Get comprehensive engine status and performance metrics."""
    uptime = (datetime.now() - engine.startup_time).total_seconds()
    return {
        "engine_id": engine.config.engine_id,
        "status": "active",
        "uptime_seconds": uptime,
        "total_operations": engine.total_learning_operations,
        "success_rate": (
            engine.successful_operations / max(1, engine.total_learning_operations)
        )
        * 100.0,
        "active_sessions": len(engine.active_sessions),
        "total_sessions": len(engine.learning_sessions),
        "learning_goals": len(engine.learning_goals),
        "decision_algorithms": len(engine.decision_algorithms),
        "learning_strategies": len(engine.learning_strategies),
        "startup_time": engine.startup_time.isoformat(),
        "last_updated": datetime.now().isoformat(),
    }


def run_smoke_test(engine: "UnifiedLearningEngine") -> bool:
    """Run basic functionality test for the learning engine."""
    try:
        test_session_id = learning_models.create_learning_session(
            engine, "test_agent", "test"
        )
        if not test_session_id:
            return False
        success = add_learning_data(
            engine,
            test_session_id,
            "test_context",
            {"input": "test"},
            {"output": "test"},
            0.8,
        )
        if not success:
            return False
        goal_id = learning_models.create_learning_goal(
            engine, "Test Goal", "Test learning goal", {"accuracy": 0.9}
        )
        if not goal_id:
            return False
        decision_result = make_decision(
            engine,
            DecisionType.TASK_ASSIGNMENT,
            "test_requester",
            {"task_id": "test_task"},
        )
        if not decision_result:
            return False
        learning_models.end_learning_session(engine, test_session_id)
        engine.learning_goals.pop(goal_id, None)
        engine.logger.info("\u2705 Learning engine smoke test passed")
        return True
    except Exception as exc:  # pragma: no cover - log and return
        engine.logger.error(f"\u274c Learning engine smoke test failed: {exc}")
        return False
