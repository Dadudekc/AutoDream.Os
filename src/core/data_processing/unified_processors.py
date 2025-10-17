"""
Unified Data Processors - DUP-008 Consolidation
===============================================

Consolidates duplicate data processing patterns found across:
- process_batch() - 4 duplicate implementations
- process_data() - 3 duplicate implementations
- process_results() - 4 duplicate implementations

V2 Compliance: ≤400 lines, SOLID principles, comprehensive error handling.

Author: Agent-1 - Integration & Core Systems Specialist
Mission: DUP-008 Data Processing Patterns Consolidation
License: MIT
"""

import logging
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class ProcessingResult:
    """Standard result structure for all processors."""
    success: bool
    data: Any
    errors: List[str]
    metadata: Dict[str, Any]


class UnifiedBatchProcessor:
    """
    Unified batch processing.
    
    Consolidates process_batch from:
    - src/core/utilities/processing_utilities.py
    - src/core/message_queue.py
    - src/core/analytics/engines/batch_analytics_engine.py
    - src/infrastructure/browser_backup/thea_modules/content_scraper.py
    """
    
    def __init__(self, batch_size: int = 100, processor_func: Optional[Callable] = None):
        """
        Initialize batch processor.
        
        Args:
            batch_size: Size of each batch
            processor_func: Function to apply to each item
        """
        self.batch_size = batch_size
        self.processor_func = processor_func
        self.logger = logging.getLogger(__name__)
    
    async def process_batch(
        self,
        items: List[Any],
        processor: Optional[Callable] = None
    ) -> ProcessingResult:
        """
        Process items in batches.
        
        Args:
            items: List of items to process
            processor: Function to process each item (overrides init processor)
            
        Returns:
            ProcessingResult with success status, data, errors
        """
        processor_func = processor or self.processor_func
        
        total = len(items)
        processed = 0
        failed = 0
        errors = []
        results_data = []
        
        if not items:
            return ProcessingResult(
                success=True,
                data=[],
                errors=[],
                metadata={"total": 0, "processed": 0, "failed": 0, "batches": 0}
            )
        
        # Process in batches
        batch_count = 0
        for i in range(0, total, self.batch_size):
            batch = items[i:i + self.batch_size]
            batch_count += 1
            
            for item in batch:
                try:
                    if processor_func:
                        result = processor_func(item)
                        results_data.append(result)
                    else:
                        results_data.append(item)
                    processed += 1
                except Exception as e:
                    failed += 1
                    errors.append(f"Item {processed + failed}: {str(e)}")
                    self.logger.error(f"Batch processing error: {e}")
        
        success = failed == 0
        
        return ProcessingResult(
            success=success,
            data=results_data,
            errors=errors,
            metadata={
                "total": total,
                "processed": processed,
                "failed": failed,
                "batches": batch_count,
                "batch_size": self.batch_size
            }
        )


class UnifiedDataProcessor:
    """
    Unified data processing.
    
    Consolidates process_data from:
    - src/core/utilities/processing_utilities.py
    - src/core/analytics/coordinators/processing_coordinator.py
    - src/core/analytics/coordinators/analytics_coordinator.py
    """
    
    def __init__(self, transformers: Optional[List[Callable]] = None):
        """
        Initialize data processor.
        
        Args:
            transformers: List of transformation functions to apply
        """
        self.transformers = transformers or []
        self.logger = logging.getLogger(__name__)
    
    async def process_data(
        self,
        data: Dict[str, Any],
        transformer: Optional[Callable] = None
    ) -> ProcessingResult:
        """
        Process data through transformation pipeline.
        
        Args:
            data: Data dictionary to process
            transformer: Single transformer function (or uses self.transformers)
            
        Returns:
            ProcessingResult with transformed data
        """
        if not data:
            return ProcessingResult(
                success=True,
                data={},
                errors=[],
                metadata={"transformers_applied": 0}
            )
        
        try:
            processed_data = data.copy()
            transformers_list = [transformer] if transformer else self.transformers
            
            for idx, trans_func in enumerate(transformers_list):
                try:
                    processed_data = trans_func(processed_data)
                except Exception as e:
                    self.logger.error(f"Transformer {idx} failed: {e}")
                    return ProcessingResult(
                        success=False,
                        data=data,  # Return original on error
                        errors=[f"Transformer {idx}: {str(e)}"],
                        metadata={"transformers_applied": idx}
                    )
            
            return ProcessingResult(
                success=True,
                data=processed_data,
                errors=[],
                metadata={"transformers_applied": len(transformers_list)}
            )
            
        except Exception as e:
            self.logger.error(f"Data processing error: {e}")
            return ProcessingResult(
                success=False,
                data=data,
                errors=[str(e)],
                metadata={"transformers_applied": 0}
            )


class UnifiedResultsProcessor:
    """
    Unified results processing.
    
    Consolidates process_results from:
    - src/core/utilities/processing_utilities.py
    - src/core/managers/results/base_results_manager.py
    - src/core/managers/contracts.py
    - src/core/managers/core_results_manager.py
    """
    
    def __init__(self, validators: Optional[List[Callable]] = None):
        """
        Initialize results processor.
        
        Args:
            validators: List of validation functions
        """
        self.validators = validators or []
        self.logger = logging.getLogger(__name__)
    
    def process_results(
        self,
        results: Any,
        context: Optional[Dict[str, Any]] = None,
        result_type: Optional[str] = None
    ) -> ProcessingResult:
        """
        Process and validate results.
        
        Args:
            results: Results data to process
            context: Processing context
            result_type: Type of results for specialized processing
            
        Returns:
            ProcessingResult with validated results
        """
        context = context or {}
        
        try:
            # Validate results
            validation_errors = []
            for validator in self.validators:
                try:
                    is_valid = validator(results)
                    if not is_valid:
                        validation_errors.append(f"Validator {validator.__name__} failed")
                except Exception as e:
                    validation_errors.append(f"Validator error: {str(e)}")
            
            # Process by type if specified
            if result_type:
                results = self._process_by_type(results, result_type)
            
            success = len(validation_errors) == 0
            
            return ProcessingResult(
                success=success,
                data=results,
                errors=validation_errors,
                metadata={
                    "context": context,
                    "result_type": result_type,
                    "validators_run": len(self.validators)
                }
            )
            
        except Exception as e:
            self.logger.error(f"Results processing error: {e}")
            return ProcessingResult(
                success=False,
                data=results,
                errors=[str(e)],
                metadata={"context": context}
            )
    
    def _process_by_type(self, results: Any, result_type: str) -> Any:
        """Process results based on type."""
        # Type-specific processing logic
        if result_type == "validation":
            return {"type": "validation", "data": results}
        elif result_type == "performance":
            return {"type": "performance", "data": results}
        elif result_type == "integration":
            return {"type": "integration", "data": results}
        else:
            return results


# Singleton instances for convenience
_batch_processor = UnifiedBatchProcessor()
_data_processor = UnifiedDataProcessor()
_results_processor = UnifiedResultsProcessor()


# Convenience functions (backward compatibility)
async def process_batch(items: List[Any], processor_func: Optional[Callable] = None) -> Dict[str, Any]:
    """Process items in batches (convenience wrapper)."""
    result = await _batch_processor.process_batch(items, processor_func)
    return {
        "total": result.metadata["total"],
        "processed": result.metadata["processed"],
        "failed": result.metadata["failed"],
        "batches": result.metadata["batches"],
        "errors": result.errors
    }


async def process_data(data: Dict[str, Any], transformer: Optional[Callable] = None) -> Dict[str, Any]:
    """Process data through transformations (convenience wrapper)."""
    processor = UnifiedDataProcessor([transformer] if transformer else [])
    result = await processor.process_data(data)
    return result.data if result.success else data


def process_results(results: Any, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Process and validate results (convenience wrapper)."""
    result = _results_processor.process_results(results, context)
    return {
        "success": result.success,
        "data": result.data,
        "errors": result.errors,
        **result.metadata
    }

