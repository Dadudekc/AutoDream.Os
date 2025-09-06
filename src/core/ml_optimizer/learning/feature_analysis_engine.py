"""
ML Feature Analysis Engine - KISS Simplified
============================================

Simplified feature analysis engine for ML optimization.
KISS PRINCIPLE: Keep It Simple, Stupid - removed overengineering.

Author: Agent-8 (SSOT & System Integration Specialist) - KISS Simplification
License: MIT
"""

import statistics
from typing import Dict, List, Any, Optional
from datetime import datetime
from collections import Counter


class FeatureAnalysisEngine:
    """KISS Simplified Feature Analysis Engine.

    Removed overengineering - focuses on essential feature analysis only.
    """

    def __init__(self):
        """Initialize simplified feature analysis engine."""
        self.feature_cache: Dict[str, Any] = {}
        self.analysis_count = 0

    def extract_features(
        self, data: Any, feature_types: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Extract features from raw data - simplified."""
        try:
            if feature_types is None:
                feature_types = ["basic", "statistical"]

            features = {}

            # Basic features
            if "basic" in feature_types:
                features.update(self._extract_basic_features(data))

            # Statistical features
            if "statistical" in feature_types:
                features.update(self._extract_statistical_features(data))

            # Cache features
            cache_key = f"{type(data).__name__}_{len(str(data))}"
            self.feature_cache[cache_key] = features

            return features

        except Exception as e:
            return {"error": str(e)}

    def _extract_basic_features(self, data: Any) -> Dict[str, Any]:
        """Extract basic features."""
        try:
            features = {}

            if isinstance(data, (list, tuple)):
                features["length"] = len(data)
                features["type"] = "sequence"
            elif isinstance(data, dict):
                features["length"] = len(data)
                features["type"] = "mapping"
            elif isinstance(data, str):
                features["length"] = len(data)
                features["type"] = "string"
            else:
                features["type"] = type(data).__name__
                features["length"] = 1

            return features

        except Exception:
            return {}

    def _extract_statistical_features(self, data: Any) -> Dict[str, Any]:
        """Extract statistical features."""
        try:
            features = {}

            if isinstance(data, (list, tuple)) and data:
                # Convert to numbers if possible
                numeric_data = []
                for item in data:
                    try:
                        numeric_data.append(float(item))
                    except (ValueError, TypeError):
                        continue

                if numeric_data:
                    features["mean"] = statistics.mean(numeric_data)
                    features["median"] = statistics.median(numeric_data)
                    features["std_dev"] = (
                        statistics.stdev(numeric_data) if len(numeric_data) > 1 else 0
                    )
                    features["min"] = min(numeric_data)
                    features["max"] = max(numeric_data)
                    features["count"] = len(numeric_data)

            return features

        except Exception:
            return {}

    def calculate_similarity(
        self, features1: Dict[str, Any], features2: Dict[str, Any]
    ) -> float:
        """Calculate similarity between features - simplified."""
        try:
            if not features1 or not features2:
                return 0.0

            # Simple similarity calculation
            common_keys = set(features1.keys()) & set(features2.keys())
            if not common_keys:
                return 0.0

            similarities = []
            for key in common_keys:
                val1 = features1[key]
                val2 = features2[key]

                if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
                    # Numeric similarity
                    if val1 == 0 and val2 == 0:
                        similarity = 1.0
                    else:
                        similarity = 1.0 - abs(val1 - val2) / max(
                            abs(val1), abs(val2), 1
                        )
                    similarities.append(similarity)
                elif val1 == val2:
                    # Exact match
                    similarities.append(1.0)
                else:
                    # No match
                    similarities.append(0.0)

            return sum(similarities) / len(similarities) if similarities else 0.0

        except Exception:
            return 0.0

    def analyze_feature_importance(self, features: Dict[str, Any]) -> Dict[str, float]:
        """Analyze feature importance - simplified."""
        try:
            importance = {}

            for key, value in features.items():
                if isinstance(value, (int, float)):
                    # Numeric importance based on magnitude
                    importance[key] = abs(value) / 100.0  # Simple normalization
                elif isinstance(value, str):
                    # String importance based on length
                    importance[key] = min(len(value) / 100.0, 1.0)
                else:
                    # Default importance
                    importance[key] = 0.5

            return importance

        except Exception:
            return {}

    def get_analysis_summary(self) -> Dict[str, Any]:
        """Get analysis summary."""
        try:
            return {
                "total_analyses": self.analysis_count,
                "cached_features": len(self.feature_cache),
                "status": "active",
            }
        except Exception:
            return {"status": "error"}

    def cleanup(self) -> None:
        """Cleanup analysis resources."""
        try:
            self.feature_cache.clear()
            self.analysis_count = 0
        except Exception:
            pass


# Factory function for backward compatibility
def create_feature_analysis_engine() -> FeatureAnalysisEngine:
    """Create a feature analysis engine instance."""
    return FeatureAnalysisEngine()
