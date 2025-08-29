"""
Contract status enumeration for the contract claiming system.
"""

from enum import Enum


class ContractStatus(Enum):
    """Enumeration of possible contract statuses."""
    
    AVAILABLE = "AVAILABLE"
    CLAIMED = "CLAIMED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"
    
    @classmethod
    def from_string(cls, status_str: str) -> 'ContractStatus':
        """Create ContractStatus from string, with fallback to AVAILABLE."""
        try:
            return cls(status_str.upper())
        except ValueError:
            return cls.AVAILABLE
    
    def __str__(self) -> str:
        """Return string representation of status."""
        return self.value
    
    def is_active(self) -> bool:
        """Check if status represents an active contract."""
        return self in [self.AVAILABLE, self.CLAIMED, self.IN_PROGRESS]
    
    def can_be_claimed(self) -> bool:
        """Check if contract can be claimed in current status."""
        return self == self.AVAILABLE
    
    def can_be_updated(self) -> bool:
        """Check if contract can be updated in current status."""
        return self in [self.CLAIMED, self.IN_PROGRESS]
    
    def can_be_completed(self) -> bool:
        """Check if contract can be completed in current status."""
        return self in [self.CLAIMED, self.IN_PROGRESS]
