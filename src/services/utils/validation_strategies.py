"""
Validation Strategies

Validation strategy implementations for CLI validation enhancement system.

Author: Agent-3 - Infrastructure & DevOps Specialist
"""

import asyncio
from datetime import datetime
from typing import Any, Callable, Dict

from ..models.validation_enhancement_models import (
    ValidationContext, ValidationResult, ValidationStrategy
)
from ..validation_models import ValidationError, ValidationExitCodes


class ValidationStrategies:
    """Collection of validation strategy implementations."""

    @staticmethod
    async def validate_sequential(
        core_validator,
        args: Any,
        context: ValidationContext
    ) -> ValidationResult:
        """Sequential validation strategy."""
        return core_validator.validate_args(args)

    @staticmethod
    async def validate_parallel(
        core_validator,
        custom_validators: Dict[str, Callable],
        args: Any,
        context: ValidationContext
    ) -> ValidationResult:
        """Parallel validation strategy."""
        # Create validation tasks for parallel execution
        tasks = []
        
        # Core validation task
        tasks.append(asyncio.create_task(
            ValidationStrategies._run_core_validation(core_validator, args)
        ))
        
        # Custom validators
        for validator_name, validator_func in custom_validators.items():
            tasks.append(asyncio.create_task(
                ValidationStrategies._run_custom_validation(
                    validator_name, validator_func, args
                )
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

    @staticmethod
    async def validate_pipeline(
        core_validator,
        custom_validators: Dict[str, Callable],
        args: Any,
        context: ValidationContext
    ) -> ValidationResult:
        """Pipeline validation strategy with early termination."""
        # Stage 1: Core validation
        core_result = await ValidationStrategies._run_core_validation(core_validator, args)
        if not core_result.is_valid:
            return core_result
        
        # Stage 2: Custom validations
        for validator_name, validator_func in custom_validators.items():
            custom_result = await ValidationStrategies._run_custom_validation(
                validator_name, validator_func, args
            )
            if not custom_result.is_valid:
                return custom_result
        
        return ValidationResult(is_valid=True)

    @staticmethod
    async def validate_cached(
        core_validator,
        validation_cache: Dict[str, ValidationResult],
        args: Any,
        context: ValidationContext
    ) -> ValidationResult:
        """Cached validation strategy."""
        # Generate cache key
        cache_key = ValidationStrategies._generate_cache_key(args, context)
        
        # Check cache
        if cache_key in validation_cache:
            cached_result = validation_cache[cache_key]
            # Check if cache is still valid (e.g., not expired)
            if ValidationStrategies._is_cache_valid(cached_result, context):
                return cached_result
        
        # Perform validation
        result = await ValidationStrategies.validate_sequential(core_validator, args, context)
        
        # Cache result
        validation_cache[cache_key] = result
        
        return result

    @staticmethod
    async def _run_core_validation(core_validator, args: Any) -> ValidationResult:
        """Run core validation in async context."""
        try:
            is_valid, error = core_validator.validate_args(args)
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

    @staticmethod
    async def _run_custom_validation(
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

    @staticmethod
    def _generate_cache_key(args: Any, context: ValidationContext) -> str:
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

    @staticmethod
    def _is_cache_valid(
        cached_result: ValidationResult,
        context: ValidationContext
    ) -> bool:
        """Check if cached result is still valid."""
        # Simple time-based cache validation (5 minutes)
        if cached_result.timestamp:
            age_seconds = (datetime.now() - cached_result.timestamp).total_seconds()
            return age_seconds < 300  # 5 minutes
        
        return True
