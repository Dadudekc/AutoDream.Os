#!/usr/bin/env python3
"""
Data Optimization Engine - KISS Compliant
=========================================

Simple data optimization engine.

Author: Agent-5 - Business Intelligence Specialist
License: MIT
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class DataOptimizationEngine:
    """Simple data optimization engine."""

    def __init__(self, config=None):
        """Initialize data optimization engine."""
        self.config = config or {}
        self.logger = logger
        self.optimization_history = []
        self.cache = {}

    def optimize_data(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Optimize data processing."""
        try:
            if not data:
                return {"error": "No data provided"}

            # Simple optimization logic
            optimized = self._compress_data(data)
            cached = self._cache_data(optimized)
            metrics = self._calculate_metrics(data, optimized)

            result = {
                "optimized_data": optimized,
                "cached": cached,
                "metrics": metrics,
                "original_size": len(data),
                "optimized_size": len(optimized),
                "timestamp": datetime.now().isoformat(),
            }

            # Store in history
            self.optimization_history.append(result)
            if len(self.optimization_history) > 100:  # Keep only last 100
                self.optimization_history.pop(0)

            self.logger.info(f"Data optimized: {len(data)} -> {len(optimized)}")
            return result

        except Exception as e:
            self.logger.error(f"Error optimizing data: {e}")
            return {"error": str(e)}

    def _compress_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compress data."""
        try:
            compressed = []

            for item in data:
                if isinstance(item, dict):
                    # Simple compression
                    compressed_item = {k: v for k, v in item.items() if v is not None}
                    compressed.append(compressed_item)

            return compressed
        except Exception as e:
            self.logger.error(f"Error compressing data: {e}")
            return []

    def _cache_data(self, data: List[Dict[str, Any]]) -> bool:
        """Cache data."""
        try:
            # Simple caching
            cache_key = f"data_{len(data)}_{datetime.now().timestamp()}"
            self.cache[cache_key] = data

            # Keep only last 50 cache entries
            if len(self.cache) > 50:
                oldest_key = next(iter(self.cache))
                del self.cache[oldest_key]

            return True
        except Exception as e:
            self.logger.error(f"Error caching data: {e}")
            return False

    def _calculate_metrics(
        self, original: List[Dict[str, Any]], optimized: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Calculate optimization metrics."""
        try:
            original_size = len(original)
            optimized_size = len(optimized)

            compression_ratio = (
                (original_size - optimized_size) / original_size
                if original_size > 0
                else 0
            )

            return {
                "original_size": original_size,
                "optimized_size": optimized_size,
                "compression_ratio": compression_ratio,
                "space_saved": original_size - optimized_size,
            }
        except Exception as e:
            self.logger.error(f"Error calculating metrics: {e}")
            return {}

    def get_optimization_summary(self) -> Dict[str, Any]:
        """Get optimization summary."""
        try:
            if not self.optimization_history:
                return {"message": "No optimization data available"}

            total_optimizations = len(self.optimization_history)
            recent_optimization = (
                self.optimization_history[-1] if self.optimization_history else {}
            )

            return {
                "total_optimizations": total_optimizations,
                "recent_optimization": recent_optimization,
                "cache_size": len(self.cache),
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            self.logger.error(f"Error getting optimization summary: {e}")
            return {"error": str(e)}

    def clear_optimization_history(self) -> None:
        """Clear optimization history."""
        self.optimization_history.clear()
        self.cache.clear()
        self.logger.info("Optimization history and cache cleared")

    def get_status(self) -> Dict[str, Any]:
        """Get engine status."""
        return {
            "active": True,
            "optimization_count": len(self.optimization_history),
            "cache_size": len(self.cache),
            "timestamp": datetime.now().isoformat(),
        }


# Simple factory function
def create_data_optimization_engine(config=None) -> DataOptimizationEngine:
    """Create data optimization engine."""
    return DataOptimizationEngine(config)


__all__ = ["DataOptimizationEngine", "create_data_optimization_engine"]
