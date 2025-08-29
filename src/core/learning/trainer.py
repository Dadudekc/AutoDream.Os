"""Training orchestration utilities for the unified learning engine."""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Dict, Any, Optional, TYPE_CHECKING

from .models import LearningData, LearningMode
from .decision_models import (
    DecisionRequest,
    DecisionResult,
    DecisionContext,
    DecisionType,
    DecisionConfidence,
    DecisionAlgorithm,
)

if TYPE_CHECKING:  # pragma: no cover - for type checkers
    from .unified_learning_engine import UnifiedLearningEngine


def add_learning_data(
    engine: "UnifiedLearningEngine",
    session_id: str,
    context: str,
    input_data: Dict[str, Any],
    output_data: Dict[str, Any],
    performance_score: float,
    learning_mode: LearningMode = LearningMode.ADAPTIVE,
) -> bool:
    """Add learning data to an active session."""
    try:
        if session_id not in engine.learning_sessions:
            raise ValueError(f"Session {session_id} not found")
        session = engine.learning_sessions[session_id]
        learning_data = LearningData(
            data_id=str(uuid.uuid4()),
            agent_id=session.agent_id,
            context=context,
            input_data=input_data,
            output_data=output_data,
            performance_score=performance_score,
            learning_mode=learning_mode,
        )
        session.add_learning_data(learning_data)
        engine.logger.debug(f"Added learning data to session: {session_id}")
        engine.total_learning_operations += 1
        engine.successful_operations += 1
        return True
    except Exception as exc:  # pragma: no cover - log and return
        engine.logger.error(f"Failed to add learning data: {exc}")
        engine.total_learning_operations += 1
        engine.failed_operations += 1
        return False


def make_decision(
    engine: "UnifiedLearningEngine",
    decision_type: DecisionType,
    requester: str,
    parameters: Dict[str, Any],
    context: Optional[DecisionContext] = None,
    algorithm_id: Optional[str] = None,
) -> DecisionResult:
    """Make a decision using the unified decision system."""
    try:
        request = DecisionRequest(
            decision_type=decision_type,
            requester=requester,
            parameters=parameters,
        )
        if algorithm_id and algorithm_id in engine.decision_algorithms:
            algorithm = engine.decision_algorithms[algorithm_id]
        else:
            algorithm = _select_algorithm_for_decision_type(engine, decision_type)
        start_time = datetime.now()
        outcome = _execute_decision_algorithm(engine, algorithm, request, context)
        processing_time = (datetime.now() - start_time).total_seconds()
        confidence = _calculate_decision_confidence(engine, request, context)
        result = DecisionResult(
            decision_id=request.decision_id,
            outcome=outcome,
            confidence=confidence,
            reasoning=f"Decision made using {algorithm.name} algorithm",
        )
        _update_decision_metrics(
            engine, decision_type, True, processing_time, confidence
        )
        engine.logger.info(f"Decision made: {request.decision_id} - {outcome}")
        engine.total_learning_operations += 1
        engine.successful_operations += 1
        return result
    except Exception as exc:  # pragma: no cover - return failure result
        engine.logger.error(f"Failed to make decision: {exc}")
        engine.total_learning_operations += 1
        engine.failed_operations += 1
        return DecisionResult(
            decision_id=str(uuid.uuid4()),
            outcome="decision_failed",
            confidence=DecisionConfidence.VERY_LOW,
            reasoning=f"Decision failed: {str(exc)}",
        )


def _select_algorithm_for_decision_type(
    engine: "UnifiedLearningEngine", decision_type: DecisionType
) -> DecisionAlgorithm:
    """Select the best algorithm for a given decision type."""
    suitable_algorithms = [
        alg
        for alg in engine.decision_algorithms.values()
        if decision_type in alg.decision_types and alg.is_active
    ]
    if not suitable_algorithms:
        return list(engine.decision_algorithms.values())[0]
    return max(
        suitable_algorithms,
        key=lambda alg: alg.performance_metrics.get("success_rate", 0.0),
    )


def _execute_decision_algorithm(
    engine: "UnifiedLearningEngine",
    algorithm: DecisionAlgorithm,
    request: DecisionRequest,
    context: Optional[DecisionContext],
) -> str:
    """Execute a decision algorithm."""
    if algorithm.implementation:
        return algorithm.implementation(request, context)
    return _default_decision_logic(engine, request, context)


def _default_decision_logic(
    engine: "UnifiedLearningEngine",
    request: DecisionRequest,
    context: Optional[DecisionContext],
) -> str:
    """Default decision logic when no custom implementation is available."""
    decision_type = request.decision_type
    if decision_type == DecisionType.TASK_ASSIGNMENT:
        return "task_assigned_to_primary_agent"
    if decision_type == DecisionType.PRIORITY_DETERMINATION:
        return f"priority_set_to_{request.parameters.get('priority', 'medium')}"
    if decision_type == DecisionType.LEARNING_STRATEGY:
        return "adaptive_learning_strategy_selected"
    return "default_decision_outcome"


def _calculate_decision_confidence(
    engine: "UnifiedLearningEngine",
    request: DecisionRequest,
    context: Optional[DecisionContext],
) -> DecisionConfidence:
    """Calculate confidence level for a decision."""
    base_confidence = 0.7
    if request.parameters:
        base_confidence += 0.1
    if context:
        base_confidence += 0.1
    if request.decision_type in engine.decision_metrics:
        metrics = engine.decision_metrics[request.decision_type]
        success_rate = metrics.get("success_rate", 0.0) / 100.0
        base_confidence += success_rate * 0.1
    confidence_score = max(0.0, min(1.0, base_confidence))
    if confidence_score >= 0.9:
        return DecisionConfidence.CERTAIN
    if confidence_score >= 0.8:
        return DecisionConfidence.VERY_HIGH
    if confidence_score >= 0.7:
        return DecisionConfidence.HIGH
    if confidence_score >= 0.6:
        return DecisionConfidence.MEDIUM
    if confidence_score >= 0.5:
        return DecisionConfidence.LOW
    return DecisionConfidence.VERY_LOW


def _update_decision_metrics(
    engine: "UnifiedLearningEngine",
    decision_type: DecisionType,
    success: bool,
    processing_time: float,
    confidence: DecisionConfidence,
) -> None:
    """Update decision performance metrics."""
    if decision_type not in engine.decision_metrics:
        engine.decision_metrics[decision_type] = {
            "total_decisions": 0,
            "successful_decisions": 0,
            "failed_decisions": 0,
            "total_processing_time": 0.0,
            "average_processing_time": 0.0,
            "success_rate": 0.0,
        }
    metrics = engine.decision_metrics[decision_type]
    metrics["total_decisions"] += 1
    if success:
        metrics["successful_decisions"] += 1
    else:
        metrics["failed_decisions"] += 1
    metrics["total_processing_time"] += processing_time
    metrics["average_processing_time"] = (
        metrics["total_processing_time"] / metrics["total_decisions"]
    )
    metrics["success_rate"] = (
        metrics["successful_decisions"] / metrics["total_decisions"]
    ) * 100.0
