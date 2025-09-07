"""
Learning Interface - Abstract Learning Engine
Captain Agent-3: MODULAR-001 Implementation
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class ILearningEngine(ABC):
    """Abstract interface for learning engines"""
    
    @abstractmethod
    def initialize_learning_module(self, module_name: str, config: Dict[str, Any]) -> bool:
        """Initialize learning module"""
        pass
    
    @abstractmethod
    def start_learning_session(self, session_id: str, module_name: str) -> bool:
        """Start learning session"""
        pass
    
    @abstractmethod
    def get_learning_status(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get learning status"""
        pass
