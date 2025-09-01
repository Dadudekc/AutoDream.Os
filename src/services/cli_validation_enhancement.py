#!/usr/bin/env python3
"""
CLI Validation Enhancement Module - Agent Cellphone V2
====================================================

Enhanced CLI validation framework with advanced modular architecture patterns.
Provides comprehensive validation capabilities with improved performance and extensibility.

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

import time
from datetime import datetime
from typing import Dict, Any, List, Optional, Callable

from .validation_models import ValidationError, ValidationResult, ValidationExitCodes
from .cli_validator_core import CLIValidatorCore
from .models.validation_enhancement_models import (
    ValidationStrategy, ValidationPriority, ValidationMetrics, ValidationContext
)
from .utils.validation_strategies import ValidationStrategies
from .utils.validation_utils import ValidationUtils


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
            ValidationStrategy.SEQUENTIAL: ValidationStrategies.validate_sequential,
            ValidationStrategy.PARALLEL: ValidationStrategies.validate_parallel,
            ValidationStrategy.PIPELINE: ValidationStrategies.validate_pipeline,
            ValidationStrategy.CACHED: ValidationStrategies.validate_cached
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
        start_memory = ValidationUtils.get_memory_usage()
        
        try:
            # Execute validation based on strategy
            validator_func = self.validation_strategies.get(
                context.strategy, 
                ValidationStrategies.validate_sequential
            )
            
            if context.strategy == ValidationStrategy.PARALLEL:
                result = await validator_func(
                    self.core_validator, self.custom_validators, args, context
                )
            elif context.strategy == ValidationStrategy.PIPELINE:
                result = await validator_func(
                    self.core_validator, self.custom_validators, args, context
                )
            elif context.strategy == ValidationStrategy.CACHED:
                result = await validator_func(
                    self.core_validator, self.validation_cache, args, context
                )
            else:
                result = await validator_func(self.core_validator, args, context)
            
            # Collect metrics
            end_time = time.time()
            end_memory = ValidationUtils.get_memory_usage()
            
            metrics = ValidationMetrics(
                validation_time_ms=(end_time - start_time) * 1000,
                memory_usage_mb=(end_memory - start_memory) / (1024 * 1024),
                cache_hit_rate=ValidationUtils.calculate_cache_hit_rate(self.validation_metrics),
                error_count=1 if not result.is_valid else 0,
                success_count=1 if result.is_valid else 0,
                timestamp=datetime.now()
            )
            
            self.validation_metrics.append(metrics)
            ValidationUtils.cleanup_old_metrics(self.validation_metrics)
            
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



    def get_validation_performance_report(self) -> Dict[str, Any]:
        """Generate validation performance report."""
        return ValidationUtils.generate_performance_report(
            self.validation_metrics, self.validation_cache, self.custom_validators
        )

    def get_enhancement_summary(self) -> str:
        """Get human-readable enhancement summary."""
        return ValidationUtils.generate_enhancement_summary(
            self.validation_metrics, self.validation_cache, self.custom_validators
        )
