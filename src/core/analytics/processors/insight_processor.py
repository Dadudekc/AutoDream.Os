#!/usr/bin/env python3
"""
Insight Processor - V2 Compliance Module
======================================

Handles analytics insight processing and validation.
Extracted from vector_analytics_processor.py for V2 compliance.

Responsibilities:
- Insight data processing
- Insight validation
- Insight transformation
- Insight storage

V2 Compliance: < 300 lines, single responsibility, modular design.

Author: Agent-7 - Web Development
License: MIT
"""

import time
import logging
from typing import Any, Dict, Optional
from datetime import datetime

from ..vector_analytics_models import (
    AnalyticsInsight, create_insight, validate_insight
)


class InsightProcessor:
    """
    Analytics insight processing engine.
    
    Handles processing, validation, and transformation of analytics insights
    with comprehensive error handling and performance optimization.
    """
    
    def __init__(self, config):
        """Initialize insight processor."""
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Processing statistics
        self.processing_stats = {
            'insights_processed': 0,
            'validation_errors': 0,
            'processing_errors': 0,
            'average_processing_time': 0.0
        }
    
    def process_insight(self, data: Dict[str, Any]) -> Optional[AnalyticsInsight]:
        """Process analytics insight data."""
        start_time = time.time()
        
        try:
            # Validate input data
            if not self._validate_input_data(data):
                self._record_validation_error("Invalid input data")
                return None
            
            # Extract insight parameters
            insight_id = self._generate_insight_id()
            insight_type = data.get('type', 'general')
            confidence = self._calculate_confidence(data)
            priority = self._determine_priority(data)
            
            # Create insight
            insight = create_insight(
                insight_id=insight_id,
                insight_type=insight_type,
                confidence=confidence,
                data=data,
                priority=priority
            )
            
            # Validate created insight
            if not validate_insight(insight):
                self._record_validation_error("Created insight failed validation")
                return None
            
            # Apply post-processing
            insight = self._apply_post_processing(insight)
            
            # Update statistics
            processing_time = time.time() - start_time
            self._update_processing_stats(processing_time, True)
            
            return insight
            
        except Exception as e:
            self.logger.error(f"Error processing insight: {e}")
            self._record_processing_error(str(e))
            processing_time = time.time() - start_time
            self._update_processing_stats(processing_time, False)
            return None
    
    def _validate_input_data(self, data: Dict[str, Any]) -> bool:
        """Validate input data for insight processing."""
        try:
            # Check required fields
            if not isinstance(data, dict):
                return False
            
            # Check data structure
            if not data:
                return False
            
            # Validate confidence if present
            if 'confidence' in data:
                confidence = data['confidence']
                if not isinstance(confidence, (int, float)) or not 0.0 <= confidence <= 1.0:
                    return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error validating input data: {e}")
            return False
    
    def _generate_insight_id(self) -> str:
        """Generate unique insight ID."""
        timestamp = int(time.time() * 1000)
        return f"insight_{timestamp}"
    
    def _calculate_confidence(self, data: Dict[str, Any]) -> float:
        """Calculate confidence score for insight."""
        try:
            # Use provided confidence if available
            if 'confidence' in data:
                return float(data['confidence'])
            
            # Calculate based on data quality indicators
            confidence = 0.8  # Base confidence
            
            # Adjust based on data completeness
            required_fields = ['type', 'data']
            present_fields = sum(1 for field in required_fields if field in data and data[field])
            completeness = present_fields / len(required_fields)
            confidence *= completeness
            
            # Adjust based on data size
            data_size = len(str(data))
            if data_size > 1000:
                confidence *= 1.1  # Bonus for rich data
            elif data_size < 100:
                confidence *= 0.9  # Penalty for sparse data
            
            return min(max(confidence, 0.0), 1.0)
            
        except Exception as e:
            self.logger.error(f"Error calculating confidence: {e}")
            return 0.5  # Default confidence
    
    def _determine_priority(self, data: Dict[str, Any]) -> str:
        """Determine priority level for insight."""
        try:
            # Use provided priority if available
            if 'priority' in data and data['priority'] in ['low', 'normal', 'high', 'critical']:
                return data['priority']
            
            # Determine based on confidence
            confidence = self._calculate_confidence(data)
            if confidence >= 0.9:
                return 'high'
            elif confidence >= 0.7:
                return 'normal'
            else:
                return 'low'
                
        except Exception as e:
            self.logger.error(f"Error determining priority: {e}")
            return 'normal'
    
    def _apply_post_processing(self, insight: AnalyticsInsight) -> AnalyticsInsight:
        """Apply post-processing to insight."""
        try:
            # Add tags based on insight type
            if insight.insight_type not in insight.tags:
                insight.tags.append(insight.insight_type)
            
            # Add confidence-based tags
            if insight.confidence >= 0.9:
                insight.tags.append('high_confidence')
            elif insight.confidence >= 0.7:
                insight.tags.append('medium_confidence')
            else:
                insight.tags.append('low_confidence')
            
            # Add priority-based tags
            if insight.priority == 'critical':
                insight.tags.append('critical')
            elif insight.priority == 'high':
                insight.tags.append('important')
            
            return insight
            
        except Exception as e:
            self.logger.error(f"Error in post-processing: {e}")
            return insight
    
    def _record_validation_error(self, error_message: str):
        """Record validation error."""
        self.processing_stats['validation_errors'] += 1
        self.logger.warning(f"Validation error: {error_message}")
    
    def _record_processing_error(self, error_message: str):
        """Record processing error."""
        self.processing_stats['processing_errors'] += 1
        self.logger.error(f"Processing error: {error_message}")
    
    def _update_processing_stats(self, processing_time: float, success: bool):
        """Update processing statistics."""
        if success:
            self.processing_stats['insights_processed'] += 1
            
            # Update average processing time
            if self.processing_stats['average_processing_time'] == 0:
                self.processing_stats['average_processing_time'] = processing_time
            else:
                # Exponential moving average
                alpha = 0.1
                self.processing_stats['average_processing_time'] = (
                    alpha * processing_time + 
                    (1 - alpha) * self.processing_stats['average_processing_time']
                )
        else:
            self.processing_stats['processing_errors'] += 1
    
    def get_processing_stats(self) -> Dict[str, Any]:
        """Get processing statistics."""
        return self.processing_stats.copy()
    
    def reset_stats(self):
        """Reset processing statistics."""
        self.processing_stats = {
            'insights_processed': 0,
            'validation_errors': 0,
            'processing_errors': 0,
            'average_processing_time': 0.0
        }
        self.logger.info("Insight processor statistics reset")
    
    def validate_insight_data(self, data: Dict[str, Any]) -> bool:
        """Validate insight data without processing."""
        return self._validate_input_data(data)
    
    def get_insight_summary(self, insight: AnalyticsInsight) -> Dict[str, Any]:
        """Get summary information for an insight."""
        try:
            return {
                'insight_id': insight.insight_id,
                'insight_type': insight.insight_type,
                'confidence': insight.confidence,
                'priority': insight.priority,
                'tags': insight.tags,
                'timestamp': insight.timestamp.isoformat(),
                'data_size': len(str(insight.data))
            }
        except Exception as e:
            self.logger.error(f"Error getting insight summary: {e}")
            return {'error': str(e)}
