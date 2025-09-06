"""
Pattern Extractor - V2 Compliance Module
=======================================

Pattern extraction functionality for analytics.

V2 Compliance: < 300 lines, single responsibility, pattern extraction.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

import statistics
import logging
from typing import Dict, List, Any
from collections import Counter

logger = logging.getLogger(__name__)


class PatternExtractor:
    """Pattern extraction functionality."""

    def __init__(self):
        """Initialize pattern extractor."""
        self.logger = logger

    def extract_patterns(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract patterns from data."""
        try:
            if not data:
                return {"error": "No data provided"}

            patterns = {
                "frequency_patterns": self._extract_frequency_patterns(data),
                "value_patterns": self._extract_value_patterns(data),
                "temporal_patterns": self._extract_temporal_patterns(data),
            }

            return patterns
        except Exception as e:
            self.logger.error(f"Error extracting patterns: {e}")
            return {"error": str(e)}

    def _extract_frequency_patterns(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract frequency patterns."""
        try:
            # Count occurrences of each key
            key_counts = Counter()
            for item in data:
                for key in item.keys():
                    key_counts[key] += 1

            # Find most common keys
            most_common = key_counts.most_common(5)

            return {
                "most_common_keys": most_common,
                "total_keys": len(key_counts),
                "unique_keys": list(key_counts.keys()),
            }
        except Exception as e:
            self.logger.error(f"Error extracting frequency patterns: {e}")
            return {}

    def _extract_value_patterns(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract value patterns."""
        try:
            # Extract numeric values
            numeric_values = []
            for item in data:
                for value in item.values():
                    if isinstance(value, (int, float)):
                        numeric_values.append(value)

            if not numeric_values:
                return {"message": "No numeric values found"}

            # Calculate statistics
            mean_val = statistics.mean(numeric_values)
            median_val = statistics.median(numeric_values)
            stdev_val = (
                statistics.stdev(numeric_values) if len(numeric_values) > 1 else 0
            )

            return {
                "mean": round(mean_val, 3),
                "median": round(median_val, 3),
                "stdev": round(stdev_val, 3),
                "min": min(numeric_values),
                "max": max(numeric_values),
                "count": len(numeric_values),
            }
        except Exception as e:
            self.logger.error(f"Error extracting value patterns: {e}")
            return {}

    def _extract_temporal_patterns(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract temporal patterns."""
        try:
            # Look for timestamp fields
            timestamp_fields = []
            for item in data:
                for key, value in item.items():
                    if "time" in key.lower() or "date" in key.lower():
                        timestamp_fields.append(key)
                        break

            return {
                "timestamp_fields": list(set(timestamp_fields)),
                "has_temporal_data": len(timestamp_fields) > 0,
            }
        except Exception as e:
            self.logger.error(f"Error extracting temporal patterns: {e}")
            return {}
