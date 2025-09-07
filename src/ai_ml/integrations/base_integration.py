"""
Base Integration Interface
Captain Agent-3: Unified Integration Pattern
"""

from abc import ABC, abstractmethod

class BaseIntegration(ABC):
    """Abstract base integration - no duplication allowed"""
    
    def __init__(self, name, provider):
        self.name = name
        self.provider = provider
        self.status = "initialized"
    
    @abstractmethod
    def connect(self):
        """Establish connection"""
        pass
    
    @abstractmethod
    def execute(self, operation):
        """Execute integration operation"""
        pass
    
    def get_info(self):
        """Get integration information"""
        return {"name": self.name, "provider": self.provider, "status": self.status}
