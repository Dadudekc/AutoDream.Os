#!/usr/bin/env python3
"""
Debate Coordinator - V2 Compliant
=================================

Core debate coordination logic.
V2 COMPLIANT: Under 300 lines, single responsibility.

Author: Agent-4 (Quality Assurance Specialist - CAPTAIN)
License: MIT
"""

import logging
import time
import uuid
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class DebateTopic:
    """Debate topic data structure."""
    topic_id: str
    title: str
    description: str
    participants: List[str]
    status: str
    created_at: datetime
    updated_at: datetime
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class DebateResponse:
    """Debate response data structure."""
    response_id: str
    topic_id: str
    agent_id: str
    content: str
    timestamp: datetime
    position: str  # for/against/neutral
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class DebateCoordinator:
    """Core debate coordination logic."""
    
    def __init__(self):
        self.active_topics: Dict[str, DebateTopic] = {}
        self.debate_responses: Dict[str, List[DebateResponse]] = {}
        self.logger = logging.getLogger(__name__)
        
        # Load existing debate data
        self._load_debate_data()
        
        self.logger.info("Debate Coordinator initialized")
    
    def _load_debate_data(self) -> None:
        """Load existing debate data from storage."""
        try:
            debate_file = Path(__file__).parent.parent.parent.parent.parent / "data" / "debates.json"
            if debate_file.exists():
                import json
                with open(debate_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                # Load topics
                for topic_data in data.get('topics', []):
                    topic = DebateTopic(
                        topic_id=topic_data['topic_id'],
                        title=topic_data['title'],
                        description=topic_data['description'],
                        participants=topic_data['participants'],
                        status=topic_data['status'],
                        created_at=datetime.fromisoformat(topic_data['created_at']),
                        updated_at=datetime.fromisoformat(topic_data['updated_at']),
                        metadata=topic_data.get('metadata', {})
                    )
                    self.active_topics[topic.topic_id] = topic
                
                # Load responses
                for response_data in data.get('responses', []):
                    response = DebateResponse(
                        response_id=response_data['response_id'],
                        topic_id=response_data['topic_id'],
                        agent_id=response_data['agent_id'],
                        content=response_data['content'],
                        timestamp=datetime.fromisoformat(response_data['timestamp']),
                        position=response_data['position'],
                        metadata=response_data.get('metadata', {})
                    )
                    
                    if response.topic_id not in self.debate_responses:
                        self.debate_responses[response.topic_id] = []
                    self.debate_responses[response.topic_id].append(response)
                    
        except Exception as e:
            self.logger.warning(f"Failed to load debate data: {e}")
    
    def create_debate_topic(self, title: str, description: str, 
                           participants: List[str], metadata: Dict[str, Any] = None) -> str:
        """Create a new debate topic."""
        topic_id = str(uuid.uuid4())
        current_time = datetime.now()
        
        topic = DebateTopic(
            topic_id=topic_id,
            title=title,
            description=description,
            participants=participants,
            status="active",
            created_at=current_time,
            updated_at=current_time,
            metadata=metadata or {}
        )
        
        self.active_topics[topic_id] = topic
        self.debate_responses[topic_id] = []
        
        self.logger.info(f"Created debate topic: {title}")
        self._save_debate_data()
        
        return topic_id
    
    def add_debate_response(self, topic_id: str, agent_id: str, content: str, 
                           position: str = "neutral", metadata: Dict[str, Any] = None) -> str:
        """Add a response to a debate topic."""
        if topic_id not in self.active_topics:
            raise ValueError(f"Debate topic {topic_id} not found")
        
        response_id = str(uuid.uuid4())
        current_time = datetime.now()
        
        response = DebateResponse(
            response_id=response_id,
            topic_id=topic_id,
            agent_id=agent_id,
            content=content,
            timestamp=current_time,
            position=position,
            metadata=metadata or {}
        )
        
        self.debate_responses[topic_id].append(response)
        
        # Update topic timestamp
        self.active_topics[topic_id].updated_at = current_time
        
        self.logger.info(f"Added response to topic {topic_id} from agent {agent_id}")
        self._save_debate_data()
        
        return response_id
    
    def get_debate_topic(self, topic_id: str) -> Optional[DebateTopic]:
        """Get a debate topic by ID."""
        return self.active_topics.get(topic_id)
    
    def get_debate_responses(self, topic_id: str) -> List[DebateResponse]:
        """Get all responses for a debate topic."""
        return self.debate_responses.get(topic_id, [])
    
    def list_active_topics(self) -> List[DebateTopic]:
        """List all active debate topics."""
        return [topic for topic in self.active_topics.values() if topic.status == "active"]
    
    def close_debate_topic(self, topic_id: str) -> bool:
        """Close a debate topic."""
        if topic_id in self.active_topics:
            self.active_topics[topic_id].status = "closed"
            self.active_topics[topic_id].updated_at = datetime.now()
            self._save_debate_data()
            self.logger.info(f"Closed debate topic: {topic_id}")
            return True
        return False
    
    def get_debate_summary(self, topic_id: str) -> Dict[str, Any]:
        """Get summary statistics for a debate topic."""
        if topic_id not in self.active_topics:
            return {}
        
        topic = self.active_topics[topic_id]
        responses = self.debate_responses.get(topic_id, [])
        
        # Count responses by position
        position_counts = {}
        for response in responses:
            position_counts[response.position] = position_counts.get(response.position, 0) + 1
        
        return {
            "topic_id": topic_id,
            "title": topic.title,
            "status": topic.status,
            "participants": topic.participants,
            "total_responses": len(responses),
            "position_counts": position_counts,
            "created_at": topic.created_at.isoformat(),
            "updated_at": topic.updated_at.isoformat(),
            "duration_hours": (topic.updated_at - topic.created_at).total_seconds() / 3600
        }
    
    def _save_debate_data(self) -> None:
        """Save debate data to storage."""
        try:
            debate_file = Path(__file__).parent.parent.parent.parent.parent / "data" / "debates.json"
            debate_file.parent.mkdir(parents=True, exist_ok=True)
            
            import json
            data = {
                "topics": [
                    {
                        "topic_id": topic.topic_id,
                        "title": topic.title,
                        "description": topic.description,
                        "participants": topic.participants,
                        "status": topic.status,
                        "created_at": topic.created_at.isoformat(),
                        "updated_at": topic.updated_at.isoformat(),
                        "metadata": topic.metadata
                    }
                    for topic in self.active_topics.values()
                ],
                "responses": [
                    {
                        "response_id": response.response_id,
                        "topic_id": response.topic_id,
                        "agent_id": response.agent_id,
                        "content": response.content,
                        "timestamp": response.timestamp.isoformat(),
                        "position": response.position,
                        "metadata": response.metadata
                    }
                    for responses in self.debate_responses.values()
                    for response in responses
                ]
            }
            
            with open(debate_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            self.logger.error(f"Failed to save debate data: {e}")

