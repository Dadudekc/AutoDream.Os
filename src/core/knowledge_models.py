#!/usr/bin/env python3
"""
Knowledge Models - Agent Cellphone V2
=====================================

Data models and classes for the knowledge database system.
Extracted from monolithic knowledge_database.py for better modularity.

Follows V2 coding standards: ≤300 LOC, OOP design, SRP
"""

import json
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Any
from datetime import datetime


@dataclass
class KnowledgeEntry:
    """Represents a single knowledge entry"""
    
    id: str
    title: str
    content: str
    category: str
    tags: List[str]
    source: str
    confidence: float  # 0.0 to 1.0
    created_at: float
    updated_at: float
    agent_id: str
    related_entries: List[str]
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert entry to dictionary for storage"""
        return asdict(self)
    
    def to_json(self) -> str:
        """Convert entry to JSON string"""
        return json.dumps(self.to_dict())
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'KnowledgeEntry':
        """Create entry from dictionary"""
        # Handle JSON-serialized fields
        if isinstance(data.get('tags'), str):
            data['tags'] = json.loads(data['tags'])
        if isinstance(data.get('related_entries'), str):
            data['related_entries'] = json.loads(data['related_entries'])
        if isinstance(data.get('metadata'), str):
            data['metadata'] = json.loads(data['metadata'])
        
        return cls(**data)
    
    @classmethod
    def create(cls, title: str, content: str, category: str, 
               tags: List[str], source: str, agent_id: str, 
               confidence: float = 1.0, related_entries: Optional[List[str]] = None,
               metadata: Optional[Dict[str, Any]] = None) -> 'KnowledgeEntry':
        """Create a new knowledge entry with current timestamps"""
        now = datetime.now().timestamp()
        return cls(
            id=f"kb_{int(now)}_{hash(title) % 10000:04d}",
            title=title,
            content=content,
            category=category,
            tags=tags or [],
            source=source,
            confidence=max(0.0, min(1.0, confidence)),
            created_at=now,
            updated_at=now,
            agent_id=agent_id,
            related_entries=related_entries or [],
            metadata=metadata or {}
        )
    
    def update(self, **kwargs) -> None:
        """Update entry fields and timestamp"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now().timestamp()
    
    def add_tag(self, tag: str) -> None:
        """Add a tag to the entry"""
        if tag not in self.tags:
            self.tags.append(tag)
            self.updated_at = datetime.now().timestamp()
    
    def remove_tag(self, tag: str) -> None:
        """Remove a tag from the entry"""
        if tag in self.tags:
            self.tags.remove(tag)
            self.updated_at = datetime.now().timestamp()
    
    def add_related_entry(self, entry_id: str) -> None:
        """Add a related entry ID"""
        if entry_id not in self.related_entries:
            self.related_entries.append(entry_id)
            self.updated_at = datetime.now().timestamp()
    
    def remove_related_entry(self, entry_id: str) -> None:
        """Remove a related entry ID"""
        if entry_id in self.related_entries:
            self.related_entries.remove(entry_id)
            self.updated_at = datetime.now().timestamp()
    
    def get_age_days(self) -> float:
        """Get age of entry in days"""
        return (datetime.now().timestamp() - self.created_at) / (24 * 3600)
    
    def is_recent(self, days: int = 7) -> bool:
        """Check if entry was created within specified days"""
        return self.get_age_days() <= days
    
    def get_confidence_level(self) -> str:
        """Get human-readable confidence level"""
        if self.confidence >= 0.9:
            return "Very High"
        elif self.confidence >= 0.7:
            return "High"
        elif self.confidence >= 0.5:
            return "Medium"
        elif self.confidence >= 0.3:
            return "Low"
        else:
            return "Very Low"


@dataclass
class KnowledgeRelationship:
    """Represents a relationship between knowledge entries"""
    
    id: Optional[int]
    entry_id: str
    related_id: str
    relationship_type: str
    strength: float  # 0.0 to 1.0
    created_at: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert relationship to dictionary"""
        return asdict(self)
    
    @classmethod
    def create(cls, entry_id: str, related_id: str, 
               relationship_type: str, strength: float = 1.0) -> 'KnowledgeRelationship':
        """Create a new relationship with current timestamp"""
        return cls(
            id=None,
            entry_id=entry_id,
            related_id=related_id,
            relationship_type=relationship_type,
            strength=max(0.0, min(1.0, strength)),
            created_at=datetime.now().timestamp()
        )


@dataclass
class SearchIndexEntry:
    """Represents a search index entry for full-text search"""
    
    id: Optional[int]
    entry_id: str
    search_text: str
    weight: float  # 0.0 to 1.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert search index entry to dictionary"""
        return asdict(self)
    
    @classmethod
    def create(cls, entry_id: str, search_text: str, weight: float = 1.0) -> 'SearchIndexEntry':
        """Create a new search index entry"""
        return cls(
            id=None,
            entry_id=entry_id,
            search_text=search_text,
            weight=max(0.0, min(1.0, weight))
        )


class KnowledgeEntryBuilder:
    """Builder pattern for creating knowledge entries with validation"""
    
    def __init__(self):
        self._entry_data = {}
    
    def with_title(self, title: str) -> 'KnowledgeEntryBuilder':
        """Set the entry title"""
        if not title or not title.strip():
            raise ValueError("Title cannot be empty")
        self._entry_data['title'] = title.strip()
        return self
    
    def with_content(self, content: str) -> 'KnowledgeEntryBuilder':
        """Set the entry content"""
        if not content or not content.strip():
            raise ValueError("Content cannot be empty")
        self._entry_data['content'] = content.strip()
        return self
    
    def with_category(self, category: str) -> 'KnowledgeEntryBuilder':
        """Set the entry category"""
        if not category or not category.strip():
            raise ValueError("Category cannot be empty")
        self._entry_data['category'] = category.strip()
        return self
    
    def with_tags(self, tags: List[str]) -> 'KnowledgeEntryBuilder':
        """Set the entry tags"""
        if not tags:
            tags = []
        self._entry_data['tags'] = [tag.strip() for tag in tags if tag.strip()]
        return self
    
    def with_source(self, source: str) -> 'KnowledgeEntryBuilder':
        """Set the entry source"""
        if not source or not source.strip():
            raise ValueError("Source cannot be empty")
        self._entry_data['source'] = source.strip()
        return self
    
    def with_agent_id(self, agent_id: str) -> 'KnowledgeEntryBuilder':
        """Set the agent ID"""
        if not agent_id or not agent_id.strip():
            raise ValueError("Agent ID cannot be empty")
        self._entry_data['agent_id'] = agent_id.strip()
        return self
    
    def with_confidence(self, confidence: float) -> 'KnowledgeEntryBuilder':
        """Set the confidence level"""
        if not 0.0 <= confidence <= 1.0:
            raise ValueError("Confidence must be between 0.0 and 1.0")
        self._entry_data['confidence'] = confidence
        return self
    
    def with_metadata(self, metadata: Dict[str, Any]) -> 'KnowledgeEntryBuilder':
        """Set additional metadata"""
        self._entry_data['metadata'] = metadata or {}
        return self
    
    def build(self) -> KnowledgeEntry:
        """Build and validate the knowledge entry"""
        required_fields = ['title', 'content', 'category', 'source', 'agent_id']
        for field in required_fields:
            if field not in self._entry_data:
                raise ValueError(f"Required field '{field}' is missing")
        
        return KnowledgeEntry.create(
            title=self._entry_data['title'],
            content=self._entry_data['content'],
            category=self._entry_data['category'],
            tags=self._entry_data.get('tags', []),
            source=self._entry_data['source'],
            agent_id=self._entry_data['agent_id'],
            confidence=self._entry_data.get('confidence', 1.0),
            metadata=self._entry_data.get('metadata', {})
        )


# Export main classes
__all__ = [
    'KnowledgeEntry',
    'KnowledgeRelationship', 
    'SearchIndexEntry',
    'KnowledgeEntryBuilder'
]
