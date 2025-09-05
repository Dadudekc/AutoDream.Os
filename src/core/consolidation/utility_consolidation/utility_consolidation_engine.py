#!/usr/bin/env python3
"""
Utility Consolidation Engine - KISS Compliant
=============================================

Simple utility consolidation engine.

Author: Agent-5 - Business Intelligence Specialist
License: MIT
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class UtilityConsolidationEngine:
    """Simple utility consolidation engine."""
    
    def __init__(self, config=None):
        """Initialize utility consolidation engine."""
        self.config = config or {}
        self.logger = logger
        self.consolidation_history = []
        self.utilities = {}
    
    def consolidate_utilities(self, utilities: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Consolidate utility functions."""
        try:
            if not utilities:
                return {"error": "No utilities provided"}
            
            # Simple consolidation logic
            consolidated = self._merge_utilities(utilities)
            duplicates = self._find_duplicates(utilities)
            optimized = self._optimize_utilities(consolidated)
            
            result = {
                "consolidated": consolidated,
                "duplicates_found": len(duplicates),
                "optimized": optimized,
                "original_count": len(utilities),
                "consolidated_count": len(consolidated),
                "timestamp": datetime.now().isoformat()
            }
            
            # Store in history
            self.consolidation_history.append(result)
            if len(self.consolidation_history) > 100:  # Keep only last 100
                self.consolidation_history.pop(0)
            
            self.logger.info(f"Utilities consolidated: {len(utilities)} -> {len(consolidated)}")
            return result
            
        except Exception as e:
            self.logger.error(f"Error consolidating utilities: {e}")
            return {"error": str(e)}
    
    def _merge_utilities(self, utilities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Merge similar utilities."""
        try:
            merged = []
            seen = set()
            
            for utility in utilities:
                if isinstance(utility, dict) and "name" in utility:
                    name = utility["name"]
                    if name not in seen:
                        merged.append(utility)
                        seen.add(name)
            
            return merged
        except Exception as e:
            self.logger.error(f"Error merging utilities: {e}")
            return []
    
    def _find_duplicates(self, utilities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Find duplicate utilities."""
        try:
            duplicates = []
            seen = set()
            
            for utility in utilities:
                if isinstance(utility, dict) and "name" in utility:
                    name = utility["name"]
                    if name in seen:
                        duplicates.append(utility)
                    else:
                        seen.add(name)
            
            return duplicates
        except Exception as e:
            self.logger.error(f"Error finding duplicates: {e}")
            return []
    
    def _optimize_utilities(self, utilities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Optimize utilities."""
        try:
            optimized = []
            
            for utility in utilities:
                if isinstance(utility, dict):
                    # Simple optimization
                    optimized_utility = utility.copy()
                    optimized_utility["optimized"] = True
                    optimized.append(optimized_utility)
            
            return optimized
        except Exception as e:
            self.logger.error(f"Error optimizing utilities: {e}")
            return []
    
    def get_consolidation_summary(self) -> Dict[str, Any]:
        """Get consolidation summary."""
        try:
            if not self.consolidation_history:
                return {"message": "No consolidation data available"}
            
            total_consolidations = len(self.consolidation_history)
            recent_consolidation = self.consolidation_history[-1] if self.consolidation_history else {}
            
            return {
                "total_consolidations": total_consolidations,
                "recent_consolidation": recent_consolidation,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Error getting consolidation summary: {e}")
            return {"error": str(e)}
    
    def clear_consolidation_history(self) -> None:
        """Clear consolidation history."""
        self.consolidation_history.clear()
        self.logger.info("Consolidation history cleared")
    
    def get_status(self) -> Dict[str, Any]:
        """Get engine status."""
        return {
            "active": True,
            "consolidation_count": len(self.consolidation_history),
            "timestamp": datetime.now().isoformat()
        }

# Simple factory function
def create_utility_consolidation_engine(config=None) -> UtilityConsolidationEngine:
    """Create utility consolidation engine."""
    return UtilityConsolidationEngine(config)

__all__ = ["UtilityConsolidationEngine", "create_utility_consolidation_engine"]