"""
Manager Interface - Abstract Manager Interface
Captain Agent-3: MODULAR-001 Implementation
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class IManager(ABC):
    """Abstract interface for managers"""
    
    @abstractmethod
    def initialize_manager(self, config: Dict[str, Any]) -> bool:
        """Initialize manager"""
        pass
    
    @abstractmethod
    def register_resource(self, resource_id: str, resource_data: Dict[str, Any]) -> bool:
        """Register resource"""
        pass
    
    @abstractmethod
    def get_resource(self, resource_id: str) -> Optional[Dict[str, Any]]:
        """Get resource"""
        pass
    
    @abstractmethod
    def get_manager_status(self) -> Dict[str, Any]:
        """Get manager status"""
        pass
