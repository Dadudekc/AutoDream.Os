"""
Contract data model for the contract claiming system.
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional, List
from datetime import datetime
from .contract_status import ContractStatus


@dataclass
class Contract:
    """Contract data model representing a single contract."""
    
    contract_id: str
    title: str
    description: str
    category: str
    points: int
    status: ContractStatus
    agent_id: Optional[str] = None
    claimed_at: Optional[datetime] = None
    progress: str = "0%"
    deliverables: Optional[List[str]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        """Initialize default values after object creation."""
        if self.deliverables is None:
            self.deliverables = []
        if self.metadata is None:
            self.metadata = {}
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert contract to dictionary representation."""
        return {
            'contract_id': self.contract_id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'points': self.points,
            'status': self.status.value,
            'agent_id': self.agent_id,
            'claimed_at': self.claimed_at.isoformat() if self.claimed_at else None,
            'progress': self.progress,
            'deliverables': self.deliverables,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Contract':
        """Create contract from dictionary representation."""
        # Handle datetime fields
        claimed_at = None
        if data.get('claimed_at'):
            try:
                claimed_at = datetime.fromisoformat(data['claimed_at'])
            except ValueError:
                pass
        
        created_at = None
        if data.get('created_at'):
            try:
                created_at = datetime.fromisoformat(data['created_at'])
            except ValueError:
                pass
        
        updated_at = None
        if data.get('updated_at'):
            try:
                updated_at = datetime.fromisoformat(data['updated_at'])
            except ValueError:
                pass
        
        return cls(
            contract_id=data['contract_id'],
            title=data['title'],
            description=data['description'],
            category=data['category'],
            points=data['points'],
            status=ContractStatus(data['status']),
            agent_id=data.get('agent_id'),
            claimed_at=claimed_at,
            progress=data.get('progress', '0%'),
            deliverables=data.get('deliverables', []),
            created_at=created_at,
            updated_at=updated_at,
            metadata=data.get('metadata', {})
        )
    
    def update_progress(self, progress: str) -> None:
        """Update contract progress."""
        self.progress = progress
        self.updated_at = datetime.now()
    
    def add_deliverable(self, deliverable: str) -> None:
        """Add a deliverable to the contract."""
        if deliverable not in self.deliverables:
            self.deliverables.append(deliverable)
            self.updated_at = datetime.now()
    
    def is_available(self) -> bool:
        """Check if contract is available for claiming."""
        return self.status == ContractStatus.AVAILABLE
    
    def is_claimed(self) -> bool:
        """Check if contract is claimed by an agent."""
        return self.status == ContractStatus.CLAIMED
    
    def is_completed(self) -> bool:
        """Check if contract is completed."""
        return self.status == ContractStatus.COMPLETED
