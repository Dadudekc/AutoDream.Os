#!/usr/bin/env python3
"""
Insight Processor - KISS Compliant
==================================

Simple analytics insight processing.

Author: Agent-5 - Business Intelligence Specialist
License: MIT
"""

import logging
from typing import Any, Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class InsightProcessor:
    """Simple analytics insight processor."""
    
    def __init__(self, config=None):
        """Initialize insight processor."""
        self.config = config or {}
        self.logger = logger
        
        # Simple processing state
        self.stats = {
            'insights_processed': 0,
            'validation_errors': 0,
            'processing_errors': 0
        }
    
    def process_insight(self, insight_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process analytics insight."""
        try:
            self.stats['insights_processed'] += 1
            
            # Simple insight processing
            processed_insight = {
                'insight_id': insight_data.get('insight_id', f"insight_{datetime.now().timestamp()}"),
                'type': insight_data.get('type', 'unknown'),
                'message': insight_data.get('message', ''),
                'confidence': insight_data.get('confidence', 0.5),
                'timestamp': datetime.now().isoformat(),
                'metadata': insight_data.get('metadata', {})
            }
            
            # Validate insight
            if self._validate_insight(processed_insight):
                self.logger.info(f"Processed insight: {processed_insight['insight_id']}")
                return processed_insight
            else:
                self.stats['validation_errors'] += 1
                return {"error": "validation_failed", "insight_id": processed_insight['insight_id']}
                
        except Exception as e:
            self.stats['processing_errors'] += 1
            self.logger.error(f"Error processing insight: {e}")
            return {"error": str(e)}
    
    def _validate_insight(self, insight: Dict[str, Any]) -> bool:
        """Validate insight data."""
        try:
            # Simple validation
            required_fields = ['insight_id', 'type', 'message']
            for field in required_fields:
                if field not in insight or not insight[field]:
                    return False
            
            # Validate confidence
            confidence = insight.get('confidence', 0)
            if not isinstance(confidence, (int, float)) or confidence < 0 or confidence > 1:
                return False
            
            return True
        except Exception as e:
            self.logger.error(f"Error validating insight: {e}")
            return False
    
    def batch_process_insights(self, insights: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process multiple insights in batch."""
        try:
            results = []
            for insight in insights:
                result = self.process_insight(insight)
                results.append(result)
            
            self.logger.info(f"Batch processed {len(insights)} insights")
            return results
        except Exception as e:
            self.logger.error(f"Error in batch processing: {e}")
            return []
    
    def get_processing_stats(self) -> Dict[str, Any]:
        """Get processing statistics."""
        total = self.stats['insights_processed']
        success_rate = ((total - self.stats['validation_errors'] - self.stats['processing_errors']) / total * 100) if total > 0 else 0
        
        return {
            "insights_processed": total,
            "validation_errors": self.stats['validation_errors'],
            "processing_errors": self.stats['processing_errors'],
            "success_rate": success_rate,
            "timestamp": datetime.now().isoformat()
        }
    
    def reset_stats(self) -> None:
        """Reset processing statistics."""
        self.stats = {
            'insights_processed': 0,
            'validation_errors': 0,
            'processing_errors': 0
        }
        self.logger.info("Processing statistics reset")
    
    def get_status(self) -> Dict[str, Any]:
        """Get processor status."""
        return {
            "active": True,
            "stats": self.get_processing_stats(),
            "timestamp": datetime.now().isoformat()
        }

__all__ = ["InsightProcessor"]