#!/usr/bin/env python3
"""
CLI Validation Enhancement Module - Agent Cellphone V2
====================================================

Enhanced CLI validation framework with advanced modular architecture patterns.
Provides comprehensive validation capabilities with improved performance and extensibility.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

import asyncio
import time
from datetime import datetime
from typing import Dict, Any, List, Optional, Callable, Union
from dataclasses import dataclass, field
from enum import Enum

from .validation_models import ValidationError, ValidationResult, ValidationExitCodes
from .cli_validator_core import CLIValidatorCore


class ValidationStrategy(Enum):
    """Validation strategy types."""
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    PIPELINE = "pipeline"
    CACHED = "cached"


class ValidationPriority(Enum):
    """Validation priority levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class ValidationMetrics:
    """Validation performance metrics."""
    validation_time_ms: float
    memory_usage_mb: float
    cache_hit_rate: float
    error_count: int
    success_count: int
    timestamp: datetime


@dataclass
class ValidationContext:
    """Context for validation operations."""
    request_id: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    priority: ValidationPriority = ValidationPriority.MEDIUM
    strategy: ValidationStrategy = ValidationStrategy.SEQUENTIAL
    timeout_seconds: float = 30.0
    metadata: Dict[str, Any] = field(default_factory=dict)


class EnhancedCLIValidator:
    """
    Enhanced CLI validation framework with advanced modular architecture.
    
    Provides comprehensive validation capabilities with:
    - Advanced validation strategies
    - Performance optimization
    - Caching mechanisms
    - Parallel processing
    - Metrics collection
    - Extensible architecture
    """

    def __init__(self):
        """Initialize the enhanced CLI validator."""
        self.core_validator = CLIValidatorCore()
        self.validation_cache: Dict[str, ValidationResult] = {}
        self.validation_metrics: List[ValidationMetrics] = []
        self.custom_validators: Dict[str, Callable] = {}
        self.validation_strategies = {
            ValidationStrategy.SEQUENTIAL: self._validate_sequential,
            ValidationStrategy.PARALLEL: self._validate_parallel,
            ValidationStrategy.PIPELINE: self._validate_pipeline,
            ValidationStrategy.CACHED: self._validate_cached
        }

    async def validate_with_enhancement(
        self,
        args: Any,
        context: Optional[ValidationContext] = None
    ) -> ValidationResult:
        """
        Enhanced validation with advanced features.
        
        Args:
            args: Arguments to validate
            context: Validation context with strategy and options
            
        Returns:
            Enhanced validation result
        """
        if context is None:
            context = ValidationContext(
                request_id=f"req_{int(time.time())}",
                priority=ValidationPriority.MEDIUM
            )
        
        start_time = time.time()
        start_memory = self._get_memory_usage()
        
        try:
            # Execute validation based on strategy
            validator_func = self.validation_strategies.get(
                context.strategy, 
                self._validate_sequential
            )
            
            result = await validator_func(args, context)
            
            # Collect metrics
            end_time = time.time()
            end_memory = self._get_memory_usage()
            
            metrics = ValidationMetrics(
                validation_time_ms=(end_time - start_time) * 1000,
                memory_usage_mb=(end_memory - start_memory) / (1024 * 1024),
                cache_hit_rate=self._calculate_cache_hit_rate(),
                error_count=1 if not result.is_valid else 0,
                success_count=1 if result.is_valid else 0,
                timestamp=datetime.now()
            )
            
            self.validation_metrics.append(metrics)
            self._cleanup_old_metrics()
            
            return result
            
        except Exception as e:
            # Handle validation errors
            error_result = ValidationResult(
                is_valid=False,
                error=ValidationError(
                    code=ValidationExitCodes.INTERNAL_ERROR,
                    message=f"Enhanced validation failed: {str(e)}",
                    hint="Check validation context and arguments",
                    timestamp=datetime.now(),
                    details={"exception": str(e), "context": context.__dict__ if context else None}
                )
            )
            
            return error_result

    async def _validate_sequential(
        self,
        args: Any,
        context: ValidationContext
    ) -> ValidationResult:
        """Sequential validation strategy."""
        return self.core_validator.validate_args(args)

    async def _validate_parallel(
        self,
        args: Any,
        context: ValidationContext
    ) -> ValidationResult:
        """Parallel validation strategy."""
        # Create validation tasks for parallel execution
        tasks = []
        
        # Core validation task
        tasks.append(asyncio.create_task(
            self._run_core_validation(args)
        ))
        
        # Custom validators
        for validator_name, validator_func in self.custom_validators.items():
            tasks.append(asyncio.create_task(
                self._run_custom_validation(validator_name, validator_func, args)
            ))
        
        # Execute all validations in parallel
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        for result in results:
            if isinstance(result, Exception):
                return ValidationResult(
                    is_valid=False,
                    error=ValidationError(
                        code=ValidationExitCodes.INTERNAL_ERROR,
                        message=f"Parallel validation error: {str(result)}",
                        timestamp=datetime.now()
                    )
                )
            elif not result.is_valid:
                return result
        
        return ValidationResult(is_valid=True)

    async def _validate_pipeline(
        self,
        args: Any,
        context: ValidationContext
    ) -> ValidationResult:
        """Pipeline validation strategy with early termination."""
        # Stage 1: Core validation
        core_result = await self._run_core_validation(args)
        if not core_result.is_valid:
            return core_result
        
        # Stage 2: Custom validations
        for validator_name, validator_func in self.custom_validators.items():
            custom_result = await self._run_custom_validation(
                validator_name, validator_func, args
            )
            if not custom_result.is_valid:
                return custom_result
        
        return ValidationResult(is_valid=True)

    async def _validate_cached(
        self,
        args: Any,
        context: ValidationContext
    ) -> ValidationResult:
        """Cached validation strategy."""
        # Generate cache key
        cache_key = self._generate_cache_key(args, context)
        
        # Check cache
        if cache_key in self.validation_cache:
            cached_result = self.validation_cache[cache_key]
            # Check if cache is still valid (e.g., not expired)
            if self._is_cache_valid(cached_result, context):
                return cached_result
        
        # Perform validation
        result = await self._validate_sequential(args, context)
        
        # Cache result
        self.validation_cache[cache_key] = result
        self._cleanup_cache()
        
        return result

    async def _run_core_validation(self, args: Any) -> ValidationResult:
        """Run core validation in async context."""
        try:
            is_valid, error = self.core_validator.validate_args(args)
            return ValidationResult(is_valid=is_valid, error=error)
        except Exception as e:
            return ValidationResult(
                is_valid=False,
                error=ValidationError(
                    code=ValidationExitCodes.INTERNAL_ERROR,
                    message=f"Core validation error: {str(e)}",
                    timestamp=datetime.now()
                )
            )

    async def _run_custom_validation(
        self,
        validator_name: str,
        validator_func: Callable,
        args: Any
    ) -> ValidationResult:
        """Run custom validation in async context."""
        try:
            if asyncio.iscoroutinefunction(validator_func):
                result = await validator_func(args)
            else:
                result = validator_func(args)
            
            if isinstance(result, ValidationResult):
                return result
            elif isinstance(result, bool):
                return ValidationResult(is_valid=result)
            else:
                return ValidationResult(is_valid=True)
                
        except Exception as e:
            return ValidationResult(
                is_valid=False,
                error=ValidationError(
                    code=ValidationExitCodes.INTERNAL_ERROR,
                    message=f"Custom validation '{validator_name}' error: {str(e)}",
                    timestamp=datetime.now()
                )
            )

    def register_custom_validator(
        self,
        name: str,
        validator_func: Callable,
        priority: ValidationPriority = ValidationPriority.MEDIUM
    ) -> None:
        """Register a custom validator."""
        self.custom_validators[name] = validator_func

    def unregister_custom_validator(self, name: str) -> None:
        """Unregister a custom validator."""
        if name in self.custom_validators:
            del self.custom_validators[name]

    def _generate_cache_key(self, args: Any, context: ValidationContext) -> str:
        """Generate cache key for validation results."""
        import hashlib
        import json
        
        # Create hashable representation of args
        try:
            args_str = json.dumps(args.__dict__ if hasattr(args, '__dict__') else str(args))
        except:
            args_str = str(args)
        
        # Create cache key
        key_data = f"{args_str}_{context.request_id}_{context.strategy.value}"
        return hashlib.md5(key_data.encode()).hexdigest()

    def _is_cache_valid(
        self,
        cached_result: ValidationResult,
        context: ValidationContext
    ) -> bool:
        """Check if cached result is still valid."""
        # Simple time-based cache validation (5 minutes)
        if cached_result.timestamp:
            age_seconds = (datetime.now() - cached_result.timestamp).total_seconds()
            return age_seconds < 300  # 5 minutes
        
        return True

    def _cleanup_cache(self) -> None:
        """Clean up old cache entries."""
        if len(self.validation_cache) > 1000:  # Limit cache size
            # Remove oldest entries
            sorted_items = sorted(
                self.validation_cache.items(),
                key=lambda x: x[1].timestamp or datetime.min
            )
            
            # Keep only newest 500 entries
            self.validation_cache = dict(sorted_items[-500:])

    def _cleanup_old_metrics(self) -> None:
        """Clean up old metrics data."""
        if len(self.validation_metrics) > 1000:  # Limit metrics history
            self.validation_metrics = self.validation_metrics[-500:]

    def _calculate_cache_hit_rate(self) -> float:
        """Calculate cache hit rate."""
        if not self.validation_metrics:
            return 0.0
        
        total_validations = len(self.validation_metrics)
        cache_hits = sum(1 for m in self.validation_metrics if m.cache_hit_rate > 0)
        
        return (cache_hits / total_validations) * 100 if total_validations > 0 else 0.0

    def _get_memory_usage(self) -> float:
        """Get current memory usage in bytes."""
        try:
            import psutil
            process = psutil.Process()
            return process.memory_info().rss
        except ImportError:
            return 0

    def get_validation_performance_report(self) -> Dict[str, Any]:
        """Generate validation performance report."""
        if not self.validation_metrics:
            return {"message": "No validation metrics available"}
        
        # Calculate performance statistics
        total_validations = len(self.validation_metrics)
        avg_validation_time = sum(m.validation_time_ms for m in self.validation_metrics) / total_validations
        avg_memory_usage = sum(m.memory_usage_mb for m in self.validation_metrics) / total_validations
        total_errors = sum(m.error_count for m in self.validation_metrics)
        total_successes = sum(m.success_count for m in self.validation_metrics)
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
                "cache_size": len(self.validation_cache),
                "cache_hit_rate_percent": round(self._calculate_cache_hit_rate(), 2)
            },
            "custom_validators": {
                "registered_count": len(self.custom_validators),
                "validator_names": list(self.custom_validators.keys())
            },
            "recent_metrics": [
                {
                    "timestamp": m.timestamp.isoformat(),
                    "validation_time_ms": round(m.validation_time_ms, 2),
                    "memory_usage_mb": round(m.memory_usage_mb, 2),
                    "success": m.success_count > 0
                }
                for m in self.validation_metrics[-10:]  # Last 10 metrics
            ]
        }

    def get_enhancement_summary(self) -> str:
        """Get human-readable enhancement summary."""
        report = self.get_validation_performance_report()
        
        if "message" in report:
            return report["message"]
        
        summary = f"Enhanced CLI Validation Summary:\n"
        summary += f"Total Validations: {report['performance_summary']['total_validations']}\n"
        summary += f"Average Time: {report['performance_summary']['average_validation_time_ms']}ms\n"
        summary += f"Success Rate: {report['performance_summary']['success_rate_percent']}%\n"
        summary += f"Cache Hit Rate: {report['cache_performance']['cache_hit_rate_percent']}%\n"
        summary += f"Custom Validators: {report['custom_validators']['registered_count']}\n"
        
        return summary
