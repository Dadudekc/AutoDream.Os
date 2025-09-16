#!/usr/bin/env python3
"""
Swarm Data Optimizer - Agent-5 Specialized Module
================================================

Data optimization strategies for swarm efficiency, including caching,
compression, indexing, and performance optimization.

V2 Compliance: < 400 lines, single responsibility for swarm data optimization.
Author: Agent-5 (Business Intelligence Specialist)
Mission: Phase 1 Consolidation - Data Optimization Support
License: MIT
"""

import json
import logging
import time
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

from .unified_analytics_engine import UnifiedAnalyticsEngine, AnalyticsStrategy

logger = logging.getLogger(__name__)


class OptimizationStrategy(Enum):
    """Data optimization strategies."""
    CACHING = "caching"
    COMPRESSION = "compression"
    INDEXING = "indexing"
    DEDUPLICATION = "deduplication"
    BATCH_PROCESSING = "batch_processing"
    LAZY_LOADING = "lazy_loading"


class DataType(Enum):
    """Data types for optimization."""
    METRICS = "metrics"
    CONFIGURATION = "configuration"
    MESSAGES = "messages"
    REPORTS = "reports"
    COORDINATES = "coordinates"
    PROGRESS = "progress"


@dataclass
class OptimizationResult:
    """Result of data optimization operation."""
    strategy: OptimizationStrategy
    data_type: DataType
    original_size: int
    optimized_size: int
    compression_ratio: float
    processing_time: float
    success: bool
    metadata: Dict[str, Any]

    def __post_init__(self):
        if self.compression_ratio == 0 and self.original_size > 0:
            self.compression_ratio = (self.original_size - self.optimized_size) / self.original_size


@dataclass
class CacheEntry:
    """Cache entry for optimized data."""
    key: str
    data: Any
    timestamp: float
    access_count: int
    size: int
    ttl: float  # Time to live in seconds

    def __post_init__(self):
        if self.timestamp == 0:
            self.timestamp = time.time()
        if self.access_count == 0:
            self.access_count = 0


class SwarmDataOptimizer:
    """Data optimization system for swarm efficiency."""

    def __init__(self, cache_size_limit: int = 1000, default_ttl: float = 3600):
        """Initialize swarm data optimizer."""
        self.cache_size_limit = cache_size_limit
        self.default_ttl = default_ttl
        
        # Initialize analytics engine
        self.analytics_engine = UnifiedAnalyticsEngine()
        
        # Cache system
        self.cache: Dict[str, CacheEntry] = {}
        self.cache_hits = 0
        self.cache_misses = 0
        
        # Optimization tracking
        self.optimization_results: List[OptimizationResult] = []
        self.optimization_stats = {
            "total_optimizations": 0,
            "total_savings": 0,
            "average_compression": 0.0,
            "cache_hit_rate": 0.0
        }
        
        self.logger = logging.getLogger(__name__)
        self.logger.info("SwarmDataOptimizer initialized")

    def optimize_data(
        self,
        data: Any,
        data_type: DataType,
        strategies: Optional[List[OptimizationStrategy]] = None
    ) -> OptimizationResult:
        """Optimize data using specified strategies."""
        try:
            start_time = time.time()
            
            # Default strategies based on data type
            if strategies is None:
                strategies = self._get_default_strategies(data_type)
            
            # Serialize data to get original size
            original_data = json.dumps(data, default=str)
            original_size = len(original_data.encode('utf-8'))
            
            optimized_data = data
            total_compression = 0
            
            # Apply optimization strategies
            for strategy in strategies:
                optimized_data = self._apply_strategy(optimized_data, strategy, data_type)
            
            # Calculate final size
            final_data = json.dumps(optimized_data, default=str)
            optimized_size = len(final_data.encode('utf-8'))
            
            processing_time = time.time() - start_time
            compression_ratio = (original_size - optimized_size) / original_size if original_size > 0 else 0
            
            result = OptimizationResult(
                strategy=strategies[0] if strategies else OptimizationStrategy.CACHING,
                data_type=data_type,
                original_size=original_size,
                optimized_size=optimized_size,
                compression_ratio=compression_ratio,
                processing_time=processing_time,
                success=True,
                metadata={
                    "strategies_applied": [s.value for s in strategies],
                    "optimization_timestamp": time.time()
                }
            )
            
            # Track optimization
            self.optimization_results.append(result)
            self._update_optimization_stats(result)
            
            self.logger.info(f"Optimized {data_type.value} data: {compression_ratio:.1%} reduction")
            return result
            
        except Exception as e:
            self.logger.error(f"Error optimizing data: {e}")
            return OptimizationResult(
                strategy=OptimizationStrategy.CACHING,
                data_type=data_type,
                original_size=0,
                optimized_size=0,
                compression_ratio=0,
                processing_time=0,
                success=False,
                metadata={"error": str(e)}
            )

    def _get_default_strategies(self, data_type: DataType) -> List[OptimizationStrategy]:
        """Get default optimization strategies for data type."""
        strategy_map = {
            DataType.METRICS: [OptimizationStrategy.CACHING, OptimizationStrategy.COMPRESSION],
            DataType.CONFIGURATION: [OptimizationStrategy.CACHING, OptimizationStrategy.INDEXING],
            DataType.MESSAGES: [OptimizationStrategy.COMPRESSION, OptimizationStrategy.DEDUPLICATION],
            DataType.REPORTS: [OptimizationStrategy.COMPRESSION, OptimizationStrategy.INDEXING],
            DataType.COORDINATES: [OptimizationStrategy.CACHING],
            DataType.PROGRESS: [OptimizationStrategy.CACHING, OptimizationStrategy.BATCH_PROCESSING]
        }
        return strategy_map.get(data_type, [OptimizationStrategy.CACHING])

    def _apply_strategy(self, data: Any, strategy: OptimizationStrategy, data_type: DataType) -> Any:
        """Apply specific optimization strategy to data."""
        try:
            if strategy == OptimizationStrategy.CACHING:
                return self._apply_caching(data, data_type)
            elif strategy == OptimizationStrategy.COMPRESSION:
                return self._apply_compression(data)
            elif strategy == OptimizationStrategy.INDEXING:
                return self._apply_indexing(data)
            elif strategy == OptimizationStrategy.DEDUPLICATION:
                return self._apply_deduplication(data)
            elif strategy == OptimizationStrategy.BATCH_PROCESSING:
                return self._apply_batch_processing(data)
            elif strategy == OptimizationStrategy.LAZY_LOADING:
                return self._apply_lazy_loading(data)
            else:
                return data
                
        except Exception as e:
            self.logger.error(f"Error applying strategy {strategy.value}: {e}")
            return data

    def _apply_caching(self, data: Any, data_type: DataType) -> Any:
        """Apply caching strategy."""
        try:
            # Create cache key
            cache_key = f"{data_type.value}_{hash(str(data))}"
            
            # Check if data is already cached
            if cache_key in self.cache:
                entry = self.cache[cache_key]
                if time.time() - entry.timestamp < entry.ttl:
                    entry.access_count += 1
                    self.cache_hits += 1
                    return entry.data
                else:
                    # Remove expired entry
                    del self.cache[cache_key]
            
            # Cache miss
            self.cache_misses += 1
            
            # Add to cache
            data_size = len(json.dumps(data, default=str).encode('utf-8'))
            entry = CacheEntry(
                key=cache_key,
                data=data,
                timestamp=time.time(),
                access_count=1,
                size=data_size,
                ttl=self.default_ttl
            )
            
            # Manage cache size
            self._manage_cache_size()
            self.cache[cache_key] = entry
            
            return data
            
        except Exception as e:
            self.logger.error(f"Error applying caching: {e}")
            return data

    def _apply_compression(self, data: Any) -> Any:
        """Apply compression strategy."""
        try:
            # Simple compression simulation (remove whitespace, optimize structure)
            if isinstance(data, dict):
                # Remove empty values and optimize structure
                compressed = {k: v for k, v in data.items() if v is not None and v != ""}
                return compressed
            elif isinstance(data, list):
                # Remove duplicates and empty items
                compressed = list(set(item for item in data if item is not None and item != ""))
                return compressed
            else:
                return data
                
        except Exception as e:
            self.logger.error(f"Error applying compression: {e}")
            return data

    def _apply_indexing(self, data: Any) -> Any:
        """Apply indexing strategy."""
        try:
            # Create index for faster access
            if isinstance(data, dict):
                # Add index metadata
                indexed_data = {
                    "_index": {
                        "keys": list(data.keys()),
                        "count": len(data),
                        "created_at": time.time()
                    },
                    "_data": data
                }
                return indexed_data
            else:
                return data
                
        except Exception as e:
            self.logger.error(f"Error applying indexing: {e}")
            return data

    def _apply_deduplication(self, data: Any) -> Any:
        """Apply deduplication strategy."""
        try:
            if isinstance(data, list):
                # Remove duplicates while preserving order
                seen = set()
                deduplicated = []
                for item in data:
                    item_key = str(item)
                    if item_key not in seen:
                        seen.add(item_key)
                        deduplicated.append(item)
                return deduplicated
            elif isinstance(data, dict):
                # Remove duplicate values
                seen_values = set()
                deduplicated = {}
                for key, value in data.items():
                    value_key = str(value)
                    if value_key not in seen_values:
                        seen_values.add(value_key)
                        deduplicated[key] = value
                return deduplicated
            else:
                return data
                
        except Exception as e:
            self.logger.error(f"Error applying deduplication: {e}")
            return data

    def _apply_batch_processing(self, data: Any) -> Any:
        """Apply batch processing strategy."""
        try:
            if isinstance(data, list) and len(data) > 10:
                # Process in batches for better performance
                batch_size = 10
                batches = [data[i:i + batch_size] for i in range(0, len(data), batch_size)]
                return {
                    "_batched": True,
                    "_batch_count": len(batches),
                    "_batch_size": batch_size,
                    "_data": batches
                }
            else:
                return data
                
        except Exception as e:
            self.logger.error(f"Error applying batch processing: {e}")
            return data

    def _apply_lazy_loading(self, data: Any) -> Any:
        """Apply lazy loading strategy."""
        try:
            if isinstance(data, dict) and len(data) > 5:
                # Create lazy loading structure
                return {
                    "_lazy_loaded": True,
                    "_keys": list(data.keys()),
                    "_load_function": "load_data_on_demand",
                    "_metadata": {
                        "total_items": len(data),
                        "created_at": time.time()
                    }
                }
            else:
                return data
                
        except Exception as e:
            self.logger.error(f"Error applying lazy loading: {e}")
            return data

    def _manage_cache_size(self) -> None:
        """Manage cache size to stay within limits."""
        try:
            if len(self.cache) >= self.cache_size_limit:
                # Remove least recently used entries
                sorted_entries = sorted(
                    self.cache.items(),
                    key=lambda x: (x[1].access_count, x[1].timestamp)
                )
                
                # Remove 20% of cache entries
                remove_count = max(1, len(sorted_entries) // 5)
                for i in range(remove_count):
                    key, _ = sorted_entries[i]
                    del self.cache[key]
                    
        except Exception as e:
            self.logger.error(f"Error managing cache size: {e}")

    def _update_optimization_stats(self, result: OptimizationResult) -> None:
        """Update optimization statistics."""
        try:
            self.optimization_stats["total_optimizations"] += 1
            self.optimization_stats["total_savings"] += result.original_size - result.optimized_size
            
            # Update average compression
            total_compression = sum(r.compression_ratio for r in self.optimization_results)
            self.optimization_stats["average_compression"] = (
                total_compression / len(self.optimization_results)
            )
            
            # Update cache hit rate
            total_requests = self.cache_hits + self.cache_misses
            if total_requests > 0:
                self.optimization_stats["cache_hit_rate"] = (
                    self.cache_hits / total_requests * 100
                )
                
        except Exception as e:
            self.logger.error(f"Error updating optimization stats: {e}")

    def get_cache_statistics(self) -> Dict[str, Any]:
        """Get cache statistics."""
        try:
            total_size = sum(entry.size for entry in self.cache.values())
            total_requests = self.cache_hits + self.cache_misses
            
            return {
                "cache_entries": len(self.cache),
                "cache_size_bytes": total_size,
                "cache_hits": self.cache_hits,
                "cache_misses": self.cache_misses,
                "cache_hit_rate": (self.cache_hits / total_requests * 100) if total_requests > 0 else 0,
                "average_entry_size": total_size / len(self.cache) if self.cache else 0,
                "cache_limit": self.cache_size_limit
            }
            
        except Exception as e:
            self.logger.error(f"Error getting cache statistics: {e}")
            return {"error": str(e)}

    def get_optimization_report(self) -> Dict[str, Any]:
        """Get comprehensive optimization report."""
        try:
            return {
                "optimization_stats": self.optimization_stats,
                "cache_stats": self.get_cache_statistics(),
                "recent_optimizations": [
                    asdict(result) for result in self.optimization_results[-10:]
                ],
                "analytics_engine_stats": self.analytics_engine.get_analytics_statistics(),
                "generated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error getting optimization report: {e}")
            return {"error": str(e)}

    def clear_cache(self) -> None:
        """Clear all cached data."""
        try:
            self.cache.clear()
            self.cache_hits = 0
            self.cache_misses = 0
            self.logger.info("Cache cleared")
            
        except Exception as e:
            self.logger.error(f"Error clearing cache: {e}")

    def save_optimization_data(self, data_path: str = "data/optimization") -> None:
        """Save optimization data to persistent storage."""
        try:
            data_dir = Path(data_path)
            data_dir.mkdir(parents=True, exist_ok=True)
            
            # Save optimization results
            results_file = data_dir / "optimization_results.json"
            with open(results_file, "w") as f:
                json.dump([asdict(result) for result in self.optimization_results], f, indent=2)
            
            # Save cache data
            cache_file = data_dir / "cache_data.json"
            with open(cache_file, "w") as f:
                json.dump({
                    key: {
                        "data": entry.data,
                        "timestamp": entry.timestamp,
                        "access_count": entry.access_count,
                        "size": entry.size,
                        "ttl": entry.ttl
                    }
                    for key, entry in self.cache.items()
                }, f, indent=2)
            
            self.logger.info("Optimization data saved to persistent storage")
            
        except Exception as e:
            self.logger.error(f"Error saving optimization data: {e}")


# Export main classes
__all__ = [
    "SwarmDataOptimizer",
    "OptimizationResult",
    "OptimizationStrategy",
    "DataType",
    "CacheEntry",
]



