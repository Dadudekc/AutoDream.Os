#!/usr/bin/env python3
"""
Data Processing Module - Agent Cellphone V2
==========================================

Extracted from unified_learning_engine.py to provide focused data processing functionality.
Follows V2 standards: modular design, SRP, clean interfaces.

**Author:** Captain Agent-3 (MODULAR-007 Contract)
**Created:** Current Sprint
**Status:** ACTIVE - MODULARIZATION IN PROGRESS
"""

import logging
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass

from ..models import (
    LearningData, LearningMetrics, LearningSession, LearningGoal
)


@dataclass
class DataProcessingResult:
    """Result of data processing operation"""
    success: bool
    processed_data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    processing_time_ms: float = 0.0
    data_quality_score: float = 0.0


class DataProcessingModule:
    """
    Focused module for learning data processing and management
    
    This module handles:
    - Data validation and preprocessing
    - Data quality assessment
    - Data transformation and normalization
    - Data storage and retrieval optimization
    """
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.data_cache: Dict[str, Any] = {}
        self.processing_stats: Dict[str, int] = {
            "total_processed": 0,
            "successful_processing": 0,
            "failed_processing": 0,
            "data_validation_passed": 0,
            "data_validation_failed": 0
        }
        self.quality_thresholds: Dict[str, float] = {
            "minimum_quality": 0.6,
            "acceptable_quality": 0.8,
            "excellent_quality": 0.9
        }
        
        self.logger.info("DataProcessingModule initialized")
    
    def process_learning_data(
        self,
        raw_data: Dict[str, Any],
        context: str = "general",
        validation_level: str = "standard"
    ) -> DataProcessingResult:
        """Process raw learning data with validation and preprocessing"""
        start_time = datetime.now()
        
        try:
            self.logger.info(f"Processing learning data for context: {context}")
            
            # Validate input data
            validation_result = self._validate_input_data(raw_data, validation_level)
            if not validation_result["valid"]:
                self.processing_stats["data_validation_failed"] += 1
                return DataProcessingResult(
                    success=False,
                    error_message=f"Data validation failed: {validation_result['errors']}",
                    processing_time_ms=0.0,
                    data_quality_score=0.0
                )
            
            self.processing_stats["data_validation_passed"] += 1
            
            # Preprocess data
            preprocessed_data = self._preprocess_data(raw_data, context)
            
            # Calculate data quality score
            quality_score = self._calculate_data_quality(preprocessed_data, context)
            
            # Transform data for learning engine
            transformed_data = self._transform_data(preprocessed_data, context)
            
            # Cache processed data
            cache_key = f"{context}_{uuid.uuid4().hex[:8]}"
            self.data_cache[cache_key] = {
                "original_data": raw_data,
                "processed_data": transformed_data,
                "quality_score": quality_score,
                "processing_timestamp": datetime.now().isoformat(),
                "context": context
            }
            
            # Update statistics
            self.processing_stats["total_processed"] += 1
            self.processing_stats["successful_processing"] += 1
            
            processing_time = (datetime.now() - start_time).total_seconds() * 1000
            
            self.logger.info(f"Successfully processed data with quality score: {quality_score:.2f}")
            
            return DataProcessingResult(
                success=True,
                processed_data=transformed_data,
                processing_time_ms=processing_time,
                data_quality_score=quality_score
            )
            
        except Exception as e:
            self.logger.error(f"Failed to process learning data: {e}")
            self.processing_stats["total_processed"] += 1
            self.processing_stats["failed_processing"] += 1
            
            processing_time = (datetime.now() - start_time).total_seconds() * 1000
            
            return DataProcessingResult(
                success=False,
                error_message=str(e),
                processing_time_ms=processing_time,
                data_quality_score=0.0
            )
    
    def _validate_input_data(
        self,
        raw_data: Dict[str, Any],
        validation_level: str
    ) -> Dict[str, Any]:
        """Validate input data based on validation level"""
        errors = []
        warnings = []
        
        # Basic validation - required fields
        required_fields = ["input_data", "output_data"]
        for field in required_fields:
            if field not in raw_data:
                errors.append(f"Missing required field: {field}")
        
        # Standard validation
        if validation_level in ["standard", "strict"]:
            if "performance_score" in raw_data:
                score = raw_data["performance_score"]
                if not isinstance(score, (int, float)) or score < 0 or score > 1:
                    errors.append("Performance score must be a number between 0 and 1")
            
            if "context" in raw_data and not isinstance(raw_data["context"], str):
                errors.append("Context must be a string")
        
        # Strict validation
        if validation_level == "strict":
            if "input_data" in raw_data and not isinstance(raw_data["input_data"], dict):
                errors.append("Input data must be a dictionary")
            
            if "output_data" in raw_data and not isinstance(raw_data["output_data"], dict):
                errors.append("Output data must be a dictionary")
            
            # Check for empty data
            if "input_data" in raw_data and not raw_data["input_data"]:
                warnings.append("Input data is empty")
            
            if "output_data" in raw_data and not raw_data["output_data"]:
                warnings.append("Output data is empty")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }
    
    def _preprocess_data(
        self,
        raw_data: Dict[str, Any],
        context: str
    ) -> Dict[str, Any]:
        """Preprocess raw data for learning engine consumption"""
        preprocessed = raw_data.copy()
        
        # Normalize performance scores
        if "performance_score" in preprocessed:
            score = preprocessed["performance_score"]
            if isinstance(score, (int, float)):
                # Ensure score is between 0 and 1
                preprocessed["performance_score"] = max(0.0, min(1.0, float(score)))
        
        # Add metadata
        preprocessed["_metadata"] = {
            "preprocessing_timestamp": datetime.now().isoformat(),
            "context": context,
            "data_version": "1.0",
            "processing_module": "DataProcessingModule"
        }
        
        # Context-specific preprocessing
        if context == "collaborative":
            preprocessed = self._preprocess_collaborative_data(preprocessed)
        elif context == "adaptive":
            preprocessed = self._preprocess_adaptive_data(preprocessed)
        elif context == "reinforcement":
            preprocessed = self._preprocess_reinforcement_data(preprocessed)
        
        return preprocessed
    
    def _preprocess_collaborative_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Preprocess data for collaborative learning context"""
        # Add collaboration metrics
        if "collaborators" in data:
            data["_collaboration_metrics"] = {
                "collaborator_count": len(data["collaborators"]),
                "collaboration_diversity": self._calculate_diversity_score(data["collaborators"]),
                "collaboration_strength": self._calculate_collaboration_strength(data)
            }
        
        return data
    
    def _preprocess_adaptive_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Preprocess data for adaptive learning context"""
        # Add adaptation metrics
        if "performance_score" in data:
            data["_adaptation_metrics"] = {
                "performance_trend": "stable",  # Would be calculated from history
                "adaptation_opportunity": max(0.0, 1.0 - data["performance_score"]),
                "learning_rate_suggestion": self._suggest_learning_rate(data["performance_score"])
            }
        
        return data
    
    def _preprocess_reinforcement_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Preprocess data for reinforcement learning context"""
        # Add reinforcement metrics
        if "performance_score" in data:
            data["_reinforcement_metrics"] = {
                "reward_signal": data["performance_score"],
                "exploration_value": 1.0 - data["performance_score"],
                "policy_update_priority": "high" if data["performance_score"] < 0.5 else "medium"
            }
        
        return data
    
    def _calculate_diversity_score(self, collaborators: List[Any]) -> float:
        """Calculate diversity score for collaborators"""
        if not collaborators:
            return 0.0
        
        # Simple diversity calculation based on unique types
        unique_types = set(type(collab).__name__ for collab in collaborators)
        return min(1.0, len(unique_types) / max(1, len(collaborators)))
    
    def _calculate_collaboration_strength(self, data: Dict[str, Any]) -> float:
        """Calculate collaboration strength score"""
        # Simple collaboration strength calculation
        base_score = 0.5
        
        if "performance_score" in data:
            base_score += data["performance_score"] * 0.3
        
        if "collaborators" in data and len(data["collaborators"]) > 1:
            base_score += min(0.2, len(data["collaborators"]) * 0.05)
        
        return min(1.0, base_score)
    
    def _suggest_learning_rate(self, performance_score: float) -> float:
        """Suggest learning rate based on performance"""
        if performance_score < 0.3:
            return 0.2  # High learning rate for poor performance
        elif performance_score < 0.7:
            return 0.1  # Medium learning rate for moderate performance
        else:
            return 0.05  # Low learning rate for good performance
    
    def _transform_data(
        self,
        preprocessed_data: Dict[str, Any],
        context: str
    ) -> Dict[str, Any]:
        """Transform preprocessed data for learning engine consumption"""
        transformed = preprocessed_data.copy()
        
        # Convert to LearningData format if possible
        if all(key in transformed for key in ["input_data", "output_data", "performance_score"]):
            transformed["_learning_data_ready"] = True
            transformed["_learning_data_id"] = str(uuid.uuid4())
        
        # Add context-specific transformations
        if context == "collaborative":
            transformed["_transformed_for"] = "collaborative_learning"
        elif context == "adaptive":
            transformed["_transformed_for"] = "adaptive_learning"
        elif context == "reinforcement":
            transformed["_transformed_for"] = "reinforcement_learning"
        else:
            transformed["_transformed_for"] = "general_learning"
        
        return transformed
    
    def _calculate_data_quality(
        self,
        processed_data: Dict[str, Any],
        context: str
    ) -> float:
        """Calculate data quality score"""
        quality_score = 0.0
        
        # Base quality from required fields
        required_fields = ["input_data", "output_data"]
        field_score = sum(1 for field in required_fields if field in processed_data) / len(required_fields)
        quality_score += field_score * 0.3
        
        # Data completeness
        if "performance_score" in processed_data:
            quality_score += 0.2
        
        if "context" in processed_data:
            quality_score += 0.1
        
        # Metadata quality
        if "_metadata" in processed_data:
            quality_score += 0.1
        
        # Context-specific quality
        if context == "collaborative" and "_collaboration_metrics" in processed_data:
            quality_score += 0.1
        
        if context == "adaptive" and "_adaptation_metrics" in processed_data:
            quality_score += 0.1
        
        if context == "reinforcement" and "_reinforcement_metrics" in processed_data:
            quality_score += 0.1
        
        # Data transformation quality
        if "_learning_data_ready" in processed_data:
            quality_score += 0.1
        
        return min(1.0, quality_score)
    
    def get_processing_statistics(self) -> Dict[str, Any]:
        """Get comprehensive processing statistics"""
        total = self.processing_stats["total_processed"]
        success_rate = (self.processing_stats["successful_processing"] / max(1, total)) * 100.0
        validation_rate = (self.processing_stats["data_validation_passed"] / max(1, total)) * 100.0
        
        return {
            "total_processed": total,
            "successful_processing": self.processing_stats["successful_processing"],
            "failed_processing": self.processing_stats["failed_processing"],
            "success_rate_percent": round(success_rate, 2),
            "validation_passed": self.processing_stats["data_validation_passed"],
            "validation_failed": self.processing_stats["data_validation_failed"],
            "validation_rate_percent": round(validation_rate, 2),
            "cache_size": len(self.data_cache),
            "quality_thresholds": self.quality_thresholds.copy()
        }
    
    def get_cached_data(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """Retrieve cached processed data"""
        return self.data_cache.get(cache_key)
    
    def clear_cache(self, older_than_hours: int = 24) -> int:
        """Clear old cached data"""
        try:
            cutoff_time = datetime.now().timestamp() - (older_than_hours * 3600)
            cleared_count = 0
            
            keys_to_remove = []
            for key, data in self.data_cache.items():
                if "_metadata" in data and "processing_timestamp" in data["_metadata"]:
                    try:
                        timestamp = datetime.fromisoformat(data["_metadata"]["processing_timestamp"])
                        if timestamp.timestamp() < cutoff_time:
                            keys_to_remove.append(key)
                    except:
                        # If timestamp parsing fails, remove the entry
                        keys_to_remove.append(key)
            
            for key in keys_to_remove:
                self.data_cache.pop(key, None)
                cleared_count += 1
            
            self.logger.info(f"Cleared {cleared_count} old cache entries")
            return cleared_count
            
        except Exception as e:
            self.logger.error(f"Failed to clear cache: {e}")
            return 0
    
    def run_module_test(self) -> bool:
        """Run basic functionality test for the data processing module"""
        try:
            # Test data processing
            test_data = {
                "input_data": {"test_input": "value"},
                "output_data": {"test_output": "result"},
                "performance_score": 0.85,
                "context": "test"
            }
            
            result = self.process_learning_data(test_data, "test", "standard")
            if not result.success:
                return False
            
            if result.data_quality_score < 0.5:
                return False
            
            # Test validation
            invalid_data = {"input_data": "not_a_dict"}
            invalid_result = self.process_learning_data(invalid_data, "test", "strict")
            if invalid_result.success:
                return False
            
            # Test statistics
            stats = self.get_processing_statistics()
            if stats["total_processed"] < 2:
                return False
            
            # Test cache operations
            cache_key = list(self.data_cache.keys())[0] if self.data_cache else None
            if cache_key:
                cached_data = self.get_cached_data(cache_key)
                if not cached_data:
                    return False
            
            # Test cache clearing
            cleared_count = self.clear_cache(older_than_hours=0)
            if cleared_count < 1:
                return False
            
            self.logger.info("✅ Data processing module test passed")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Data processing module test failed: {e}")
            return False
