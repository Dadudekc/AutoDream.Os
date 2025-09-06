#!/usr/bin/env python3
"""
ML Pattern Learning Engine
==========================

Pattern learning engine for ML optimization system.
Handles pattern recognition, learning, and pattern management.
V2 COMPLIANT: Focused pattern learning under 300 lines.

@version 1.0.0 - V2 COMPLIANCE MODULAR PATTERN LEARNING
@license MIT
"""

import threading
from typing import Dict, List, Any, Optional
from datetime import datetime
from collections import deque

from ..ml_optimizer_models import (
    MLOptimizationConfig,
    LearningPattern,
    create_learning_pattern,
)


class PatternLearningEngine:
    """Pattern learning engine for ML optimization."""

    def __init__(self, config: MLOptimizationConfig):
        """Initialize pattern learning engine with configuration."""
        self.config = config
        self.learned_patterns: Dict[str, LearningPattern] = {}
        self.training_data: deque = deque(maxlen=10000)
        self.learning_lock = threading.Lock()

    def learn_pattern(
        self,
        pattern_type: str,
        features: Dict[str, Any],
        target_value: Any,
        pattern_id: Optional[str] = None,
    ) -> bool:
        """Learn a new pattern or update existing one."""
        try:
            if not pattern_id:
                pattern_id = self._generate_pattern_id(pattern_type, features)

            with self.learning_lock:
                if pattern_id in self.learned_patterns:
                    # Update existing pattern
                    pattern = self.learned_patterns[pattern_id]
                    pattern.update_frequency()
                    # Update target value if different
                    if pattern.target_value != target_value:
                        pattern.target_value = target_value
                else:
                    # Create new pattern
                    pattern = create_learning_pattern(
                        pattern_id=pattern_id,
                        pattern_type=pattern_type,
                        features=features,
                        target_value=target_value,
                    )
                    self.learned_patterns[pattern_id] = pattern

                # Add to training data
                self.training_data.append(
                    {
                        "pattern_id": pattern_id,
                        "pattern_type": pattern_type,
                        "features": features,
                        "target_value": target_value,
                        "timestamp": datetime.now(),
                    }
                )

                return True

        except Exception as e:
            return False

    def get_pattern(self, pattern_id: str) -> Optional[LearningPattern]:
        """Get a specific pattern by ID."""
        return self.learned_patterns.get(pattern_id)

    def get_patterns_by_type(self, pattern_type: str) -> List[LearningPattern]:
        """Get all patterns of a specific type."""
        return [
            pattern
            for pattern in self.learned_patterns.values()
            if pattern.pattern_type == pattern_type
        ]

    def update_pattern_accuracy(self, pattern_id: str, accuracy: float) -> bool:
        """Update pattern accuracy based on validation."""
        try:
            if pattern_id in self.learned_patterns:
                pattern = self.learned_patterns[pattern_id]
                pattern.update_accuracy(accuracy)
                return True
            return False
        except Exception:
            return False

    def remove_pattern(self, pattern_id: str) -> bool:
        """Remove a pattern from learning."""
        try:
            with self.learning_lock:
                if pattern_id in self.learned_patterns:
                    del self.learned_patterns[pattern_id]
                    return True
                return False
        except Exception:
            return False

    def get_pattern_statistics(self) -> Dict[str, Any]:
        """Get statistics about learned patterns."""
        if not self.learned_patterns:
            return {
                "total_patterns": 0,
                "pattern_types": {},
                "avg_frequency": 0.0,
                "avg_accuracy": 0.0,
            }

        pattern_types = {}
        total_frequency = 0
        total_accuracy = 0

        for pattern in self.learned_patterns.values():
            pattern_type = pattern.pattern_type
            pattern_types[pattern_type] = pattern_types.get(pattern_type, 0) + 1
            total_frequency += pattern.frequency
            total_accuracy += pattern.accuracy

        return {
            "total_patterns": len(self.learned_patterns),
            "pattern_types": pattern_types,
            "avg_frequency": total_frequency / len(self.learned_patterns),
            "avg_accuracy": total_accuracy / len(self.learned_patterns),
            "training_data_size": len(self.training_data),
        }

    def find_similar_patterns(
        self,
        pattern_type: str,
        features: Dict[str, Any],
        similarity_threshold: float = 0.7,
    ) -> List[LearningPattern]:
        """Find patterns similar to given features."""
        similar_patterns = []

        with self.learning_lock:
            for pattern in self.learned_patterns.values():
                if pattern.pattern_type == pattern_type:
                    similarity = self._calculate_feature_similarity(
                        pattern.features, features
                    )

                    if similarity >= similarity_threshold:
                        pattern.metadata["similarity"] = similarity
                        similar_patterns.append(pattern)

        # Sort by similarity and frequency
        similar_patterns.sort(
            key=lambda p: (p.metadata.get("similarity", 0), p.frequency, p.accuracy),
            reverse=True,
        )

        return similar_patterns[:10]  # Top 10 similar patterns

    def _generate_pattern_id(self, pattern_type: str, features: Dict[str, Any]) -> str:
        """Generate unique pattern ID."""
        # Create ID based on pattern type and key features
        feature_str = "_".join(f"{k}_{v}" for k, v in sorted(features.items())[:3])
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{pattern_type}_{hash(feature_str)}_{timestamp}"

    def _calculate_feature_similarity(
        self, pattern_features: Dict[str, Any], input_features: Dict[str, Any]
    ) -> float:
        """Calculate similarity between feature sets."""
        if not pattern_features or not input_features:
            return 0.0

        pattern_keys = set(pattern_features.keys())
        input_keys = set(input_features.keys())

        # Key overlap
        common_keys = pattern_keys.intersection(input_keys)
        total_keys = pattern_keys.union(input_keys)

        if not total_keys:
            return 0.0

        key_similarity = len(common_keys) / len(total_keys)

        # Value similarity for common keys
        value_similarities = []
        for key in common_keys:
            pattern_val = pattern_features[key]
            input_val = input_features[key]

            if pattern_val == input_val:
                value_similarities.append(1.0)
            elif isinstance(pattern_val, (int, float)) and isinstance(
                input_val, (int, float)
            ):
                # Numerical similarity
                max_val = max(abs(pattern_val), abs(input_val), 1.0)
                diff = abs(pattern_val - input_val)
                similarity = max(0.0, 1.0 - (diff / max_val))
                value_similarities.append(similarity)
            else:
                value_similarities.append(0.0)

        value_similarity = (
            sum(value_similarities) / len(value_similarities)
            if value_similarities
            else 0.0
        )

        # Combined similarity
        return (key_similarity + value_similarity) / 2.0

    def clear_patterns(self):
        """Clear all learned patterns."""
        with self.learning_lock:
            self.learned_patterns.clear()
            self.training_data.clear()

    def export_patterns(self) -> Dict[str, Any]:
        """Export patterns for persistence."""
        return {
            "patterns": {
                pid: pattern.to_dict() for pid, pattern in self.learned_patterns.items()
            },
            "training_data": list(self.training_data),
            "export_timestamp": datetime.now().isoformat(),
        }

    def import_patterns(self, data: Dict[str, Any]) -> bool:
        """Import patterns from persistence data."""
        try:
            with self.learning_lock:
                # Import patterns
                if "patterns" in data:
                    for pid, pattern_data in data["patterns"].items():
                        pattern = LearningPattern.from_dict(pattern_data)
                        self.learned_patterns[pid] = pattern

                # Import training data
                if "training_data" in data:
                    self.training_data.extend(data["training_data"])

                return True
        except Exception:
            return False


# Factory function for dependency injection
def create_pattern_learning_engine(
    config: MLOptimizationConfig,
) -> PatternLearningEngine:
    """Factory function to create pattern learning engine with configuration."""
    return PatternLearningEngine(config)


# Export for DI
__all__ = ["PatternLearningEngine", "create_pattern_learning_engine"]
