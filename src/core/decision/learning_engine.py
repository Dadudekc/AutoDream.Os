#!/usr/bin/env python3
"""
Learning Engine - Agent Cellphone V2 Decision System
===================================================

Implements learning and adaptation capabilities for the autonomous decision engine.
Follows V2 coding standards: ≤300 LOC, OOP design, SRP.

**Responsibilities:**
- Learning data management
- Performance metrics tracking
- Pattern recognition
- Continuous improvement

**Author:** Agent-1
**Created:** Current Sprint
**Status:** ACTIVE - V2 STANDARDS COMPLIANT
"""

import json
import time
import threading
from typing import Dict, List, Any, Optional
from dataclasses import asdict
from datetime import datetime

from .decision_types import LearningData, LearningMode, DataIntegrityLevel
from ..persistent_data_storage import PersistentDataStorage


class LearningEngine:
    """
    Learning and adaptation engine for autonomous decision making

    Responsibilities:
    - Manage learning data collection and storage
    - Track performance metrics
    - Identify patterns and trends
    - Enable continuous system improvement
    """

    def __init__(self, storage: PersistentDataStorage):
        self.storage = storage
        self.learning_data: List[LearningData] = []
        self.performance_metrics: Dict[str, List[float]] = {}
        self.learning_lock = threading.Lock()
        self.learning_mode = LearningMode.ADAPTIVE

    def add_learning_data(self, learning_data: LearningData) -> bool:
        """Add new learning data for continuous improvement"""
        try:
            with self.learning_lock:
                self.learning_data.append(learning_data)

                # Store learning data
                self.storage.store_data(
                    f"learning_data_{int(time.time())}",
                    asdict(learning_data),
                    "autonomous/learning",
                    DataIntegrityLevel.BASIC,
                )
            return True
        except Exception as e:
            print(f"Error adding learning data: {e}")
            return False

    def update_agent_capability(self, agent_id: str, capability: Any) -> bool:
        """Update agent capability information"""
        try:
            # Store updated capability
            self.storage.store_data(
                f"agent_capability_{agent_id}",
                asdict(capability),
                "autonomous/agents",
                DataIntegrityLevel.BASIC,
            )
            return True
        except Exception as e:
            print(f"Error updating agent capability: {e}")
            return False

    def record_performance_metric(self, metric_name: str, value: float) -> bool:
        """Record a performance metric for learning"""
        try:
            with self.learning_lock:
                if metric_name not in self.performance_metrics:
                    self.performance_metrics[metric_name] = []
                self.performance_metrics[metric_name].append(value)
            return True
        except Exception as e:
            print(f"Error recording performance metric: {e}")
            return False

    def get_learning_status(self) -> Dict[str, Any]:
        """Get current learning system status"""
        with self.learning_lock:
            return {
                "learning_mode": self.learning_mode.value,
                "total_learning_data": len(self.learning_data),
                "performance_metrics": {
                    name: len(values)
                    for name, values in self.performance_metrics.items()
                },
                "last_learning_update": self.learning_data[-1].timestamp
                if self.learning_data
                else None,
            }

    def analyze_patterns(self) -> Dict[str, Any]:
        """Analyze learning data for patterns"""
        with self.learning_lock:
            patterns = {}

            # Analyze performance trends
            for metric_name, values in self.performance_metrics.items():
                if len(values) > 1:
                    patterns[metric_name] = {
                        "trend": "improving" if values[-1] > values[0] else "declining",
                        "average": sum(values) / len(values),
                        "volatility": max(values) - min(values),
                    }

            # Analyze learning data patterns
            if self.learning_data:
                context_patterns = {}
                for data in self.learning_data:
                    context = data.context
                    if context not in context_patterns:
                        context_patterns[context] = []
                    context_patterns[context].append(data.feedback_score)

                patterns["context_performance"] = {
                    context: sum(scores) / len(scores)
                    for context, scores in context_patterns.items()
                }

            return patterns

    def get_learning_recommendations(self) -> List[str]:
        """Get recommendations based on learning analysis"""
        recommendations = []
        patterns = self.analyze_patterns()

        # Performance-based recommendations
        for metric_name, pattern in patterns.items():
            if isinstance(pattern, dict) and "trend" in pattern:
                if pattern["trend"] == "declining":
                    recommendations.append(
                        f"Investigate declining {metric_name} performance"
                    )
                elif pattern["volatility"] > 0.5:
                    recommendations.append(f"Reduce volatility in {metric_name}")

        # Learning data recommendations
        if len(self.learning_data) < 10:
            recommendations.append("Collect more learning data for better patterns")

        if not recommendations:
            recommendations.append("System performing well - continue current approach")

        return recommendations

    def run_smoke_test(self) -> bool:
        """Run basic functionality test"""
        try:
            # Test learning data addition
            test_data = LearningData(
                input_features=[0.1, 0.2, 0.3],
                output_target="test",
                context="smoke_test",
                timestamp=datetime.now().isoformat(),
                performance_metric=0.8,
                feedback_score=0.8,
            )

            success = self.add_learning_data(test_data)
            if not success:
                return False

            # Test performance metric recording
            success = self.record_performance_metric("test_metric", 0.9)
            if not success:
                return False

            # Test status retrieval
            status = self.get_learning_status()
            if not status:
                return False

            # Test pattern analysis
            patterns = self.analyze_patterns()
            if patterns is None:
                return False

            # Test recommendations
            recommendations = self.get_learning_recommendations()
            if not recommendations:
                return False

            return True

        except Exception as e:
            print(f"Learning engine smoke test failed: {e}")
            return False
