"""
Base Validator - Abstract Validator Interface
Captain Agent-3: MODULAR-001 Implementation
"""

from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseValidator(ABC):
    """Abstract base validator"""
    
    def __init__(self, name: str):
        self.name = name
    
    @abstractmethod
    def validate(self, data: Any) -> Dict[str, Any]:
        """Validate data"""
        pass
    
    def get_validator_info(self) -> Dict[str, Any]:
        """Get validator information"""
        return {
            "name": self.name,
            "type": self.__class__.__name__
        }
