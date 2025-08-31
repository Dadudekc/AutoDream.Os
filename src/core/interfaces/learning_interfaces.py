"""
🎯 LEARNING INTERFACES - CONSOLIDATED
Agent-7 - Interface Systems Consolidation Specialist

Consolidated learning interface definitions.
Source: src/core/learning/interfaces/

Agent: Agent-7 (Interface Systems Consolidation Specialist)
Mission: CRITICAL SSOT Consolidation - 50%+ reduction in duplicate folders
Priority: CRITICAL - Above all other work
Status: IMPLEMENTATION PHASE 1 - Unified Interface System

Author: Agent-7 - Quality Completion Optimization Manager
License: MIT
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime


class LearningInterface(ABC):
    """
    Unified learning interface for all learning systems.
    
    Consolidates learning functionality from scattered implementations
    into a single source of truth.
    """
    
    @abstractmethod
    def learn(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Learn from provided data."""
        pass
    
    @abstractmethod
    def predict(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Make predictions based on learned patterns."""
        pass
    
    @abstractmethod
    def update_model(self, new_data: Dict[str, Any]) -> bool:
        """Update the learning model with new data."""
        pass
    
    @abstractmethod
    def get_performance_metrics(self) -> Dict[str, float]:
        """Get current performance metrics."""
        pass
    
    @abstractmethod
    def save_model(self, path: str) -> bool:
        """Save the current model to specified path."""
        pass
    
    @abstractmethod
    def load_model(self, path: str) -> bool:
        """Load a model from specified path."""
        pass
