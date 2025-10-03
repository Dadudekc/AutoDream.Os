"""
Discord Commander Optimization - V2 Compliant Main Interface
============================================================

Main interface for Discord commander optimization system.
V2 Compliance: ≤400 lines, single responsibility, KISS principle
"""

from typing import Any

from .optimization_core import (
    DiscordCacheManager,
    DiscordOptimizationEngine,
    DiscordPerformanceMonitor,
)
from .optimization_models import DiscordPerformanceMetrics, OptimizationConfig


class DiscordOptimizationManager:
    """Main Discord optimization manager interface."""

    def __init__(self, config: OptimizationConfig = None):
        """Initialize Discord optimization manager."""
        self.config = config or OptimizationConfig()
        self.monitor = DiscordPerformanceMonitor(self.config)
        self.engine = DiscordOptimizationEngine(self.config)
        self.cache = DiscordCacheManager(self.config)

    def update_performance_metrics(self, metrics: DiscordPerformanceMetrics):
        """Update performance metrics."""
        self.monitor.update_metrics(metrics)

    def get_current_metrics(self) -> DiscordPerformanceMetrics:
        """Get current performance metrics."""
        return self.monitor.get_current_metrics()

    def analyze_performance(self) -> dict[str, Any]:
        """Analyze current performance and suggest optimizations."""
        current_metrics = self.monitor.get_current_metrics()
        return self.engine.analyze_performance(current_metrics)

    def apply_optimizations(self, recommendations: list[str]) -> dict[str, Any]:
        """Apply optimization recommendations."""
        return self.engine.apply_optimizations(recommendations)

    def manage_cache_operations(self, operation: str, key: str = None, value: Any = None) -> Any:
        """Manage cache operations."""
        if operation == "get" and key:
            return self.cache.get(key)
        elif operation == "set" and key and value is not None:
            return self.cache.set(key, value)
        elif operation == "clear":
            self.cache.clear()
            return True
        elif operation == "stats":
            return self.cache.get_cache_stats()
        else:
            return None

    def get_performance_summary(self) -> dict[str, Any]:
        """Get comprehensive performance summary."""
        current_metrics = self.monitor.get_current_metrics()
        analysis = self.engine.analyze_performance(current_metrics)
        cache_stats = self.cache.get_cache_stats()

        return {
            "current_metrics": current_metrics.to_dict(),
            "performance_analysis": analysis,
            "cache_stats": cache_stats,
            "optimization_config": {
                "cache_size": self.config.cache_size,
                "cache_ttl": self.config.cache_ttl,
                "rate_limit_per_minute": self.config.rate_limit_per_minute,
                "max_concurrent_operations": self.config.max_concurrent_operations,
                "enable_compression": self.config.enable_compression,
                "enable_caching": self.config.enable_caching,
            },
        }


# Global instance for backward compatibility
discord_optimization_manager = DiscordOptimizationManager()


def main():
    """Main function for testing."""
    manager = DiscordOptimizationManager()
    print("Discord Commander Optimization Manager initialized")
    print(f"Cache stats: {manager.get_cache_stats()}")


if __name__ == "__main__":
    main()
