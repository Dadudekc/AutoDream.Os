"""
Validation Utilities

Utility functions for CLI validation enhancement system.

Author: Agent-3 - Infrastructure & DevOps Specialist
"""

from datetime import datetime
from typing import Dict, Any, List

from ..models.validation_enhancement_models import ValidationMetrics, ValidationResult


class ValidationUtils:
    """Collection of validation utility functions."""

    @staticmethod
    def cleanup_cache(validation_cache: Dict[str, ValidationResult]) -> None:
        """Clean up old cache entries."""
        if len(validation_cache) > 1000:  # Limit cache size
            # Remove oldest entries
            sorted_items = sorted(
                validation_cache.items(),
                key=lambda x: x[1].timestamp or datetime.min
            )
            
            # Keep only newest 500 entries
            validation_cache.clear()
            validation_cache.update(dict(sorted_items[-500:]))

    @staticmethod
    def cleanup_old_metrics(validation_metrics: List[ValidationMetrics]) -> None:
        """Clean up old metrics data."""
        if len(validation_metrics) > 1000:  # Limit metrics history
            validation_metrics[:] = validation_metrics[-500:]

    @staticmethod
    def calculate_cache_hit_rate(validation_metrics: List[ValidationMetrics]) -> float:
        """Calculate cache hit rate."""
        if not validation_metrics:
            return 0.0
        
        total_validations = len(validation_metrics)
        cache_hits = sum(1 for m in validation_metrics if m.cache_hit_rate > 0)
        
        return (cache_hits / total_validations) * 100 if total_validations > 0 else 0.0

    @staticmethod
    def get_memory_usage() -> float:
        """Get current memory usage in bytes."""
        try:
            import psutil
            process = psutil.Process()
            return process.memory_info().rss
        except ImportError:
            return 0

    @staticmethod
    def generate_performance_report(
        validation_metrics: List[ValidationMetrics],
        validation_cache: Dict[str, ValidationResult],
        custom_validators: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate validation performance report."""
        if not validation_metrics:
            return {"message": "No validation metrics available"}
        
        # Calculate performance statistics
        total_validations = len(validation_metrics)
        avg_validation_time = sum(m.validation_time_ms for m in validation_metrics) / total_validations
        avg_memory_usage = sum(m.memory_usage_mb for m in validation_metrics) / total_validations
        total_errors = sum(m.error_count for m in validation_metrics)
        total_successes = sum(m.success_count for m in validation_metrics)
        success_rate = (total_successes / total_validations) * 100 if total_validations > 0 else 0
        
        return {
            "report_timestamp": datetime.now().isoformat(),
            "performance_summary": {
                "total_validations": total_validations,
                "average_validation_time_ms": round(avg_validation_time, 2),
                "average_memory_usage_mb": round(avg_memory_usage, 2),
                "success_rate_percent": round(success_rate, 2),
                "total_errors": total_errors,
                "total_successes": total_successes
            },
            "cache_performance": {
                "cache_size": len(validation_cache),
                "cache_hit_rate_percent": round(ValidationUtils.calculate_cache_hit_rate(validation_metrics), 2)
            },
            "custom_validators": {
                "registered_count": len(custom_validators),
                "validator_names": list(custom_validators.keys())
            },
            "recent_metrics": [
                {
                    "timestamp": m.timestamp.isoformat(),
                    "validation_time_ms": round(m.validation_time_ms, 2),
                    "memory_usage_mb": round(m.memory_usage_mb, 2),
                    "success": m.success_count > 0
                }
                for m in validation_metrics[-10:]  # Last 10 metrics
            ]
        }

    @staticmethod
    def generate_enhancement_summary(
        validation_metrics: List[ValidationMetrics],
        validation_cache: Dict[str, ValidationResult],
        custom_validators: Dict[str, Any]
    ) -> str:
        """Get human-readable enhancement summary."""
        report = ValidationUtils.generate_performance_report(
            validation_metrics, validation_cache, custom_validators
        )
        
        if "message" in report:
            return report["message"]
        
        summary = f"Enhanced CLI Validation Summary:\n"
        summary += f"Total Validations: {report['performance_summary']['total_validations']}\n"
        summary += f"Average Time: {report['performance_summary']['average_validation_time_ms']}ms\n"
        summary += f"Success Rate: {report['performance_summary']['success_rate_percent']}%\n"
        summary += f"Cache Hit Rate: {report['cache_performance']['cache_hit_rate_percent']}%\n"
        summary += f"Custom Validators: {report['custom_validators']['registered_count']}\n"
        
        return summary
