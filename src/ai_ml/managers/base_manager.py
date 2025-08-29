"""
Base Manager Interface
Captain Agent-3: Unified Management Pattern
"""

from abc import ABC, abstractmethod

class BaseManager(ABC):
    """Abstract base manager - no duplication allowed"""
    
    def __init__(self, name):
        self.name = name
        self.status = "initialized"
    
    @abstractmethod
    def initialize(self):
        """Initialize manager"""
        pass
    
    @abstractmethod
    def execute(self, operation):
        """Execute manager operation"""
        pass
    
    def get_status(self):
        """Get manager status"""
        return {"name": self.name, "status": self.status}
