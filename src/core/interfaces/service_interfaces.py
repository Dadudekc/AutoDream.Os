"""
🎯 SERVICE INTERFACES - CONSOLIDATED
Agent-7 - Interface Systems Consolidation Specialist

Consolidated service interface definitions.
Source: src/services/interfaces/

Agent: Agent-7 (Interface Systems Consolidation Specialist)
Mission: CRITICAL SSOT Consolidation - 50%+ reduction in duplicate folders
Priority: CRITICAL - Above all other work
Status: IMPLEMENTATION PHASE 1 - Unified Interface System

Author: Agent-7 - Quality Completion Optimization Manager
License: MIT
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
from enum import Enum


class MessageType(Enum):
    """Message types for unified messaging system."""
    BULK = "bulk"
    CAMPAIGN = "campaign"
    COORDINATE = "coordinate"
    CROSS_SYSTEM = "cross_system"
    FSM = "fsm"
    ONBOARDING = "onboarding"
    YOLO = "yolo"


class BulkMessagingInterface(ABC):
    """Interface for bulk messaging operations."""
    
    @abstractmethod
    def send_bulk_message(self, recipients: List[str], message: str) -> Dict[str, Any]:
        """Send message to multiple recipients."""
        pass
    
    @abstractmethod
    def get_bulk_status(self, message_id: str) -> Dict[str, Any]:
        """Get status of bulk message."""
        pass


class CampaignMessagingInterface(ABC):
    """Interface for campaign messaging operations."""
    
    @abstractmethod
    def create_campaign(self, campaign_data: Dict[str, Any]) -> str:
        """Create a new messaging campaign."""
        pass
    
    @abstractmethod
    def send_campaign_message(self, campaign_id: str, message: str) -> Dict[str, Any]:
        """Send message as part of a campaign."""
        pass


class CoordinateDataInterface(ABC):
    """Interface for data coordination operations."""
    
    @abstractmethod
    def coordinate_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinate data across systems."""
        pass
    
    @abstractmethod
    def get_coordination_status(self, coordination_id: str) -> Dict[str, Any]:
        """Get status of data coordination."""
        pass


class CoordinateManagerInterface(ABC):
    """Interface for coordination management operations."""
    
    @abstractmethod
    def manage_coordination(self, coordination_data: Dict[str, Any]) -> Dict[str, Any]:
        """Manage coordination between systems."""
        pass
    
    @abstractmethod
    def get_coordination_metrics(self) -> Dict[str, float]:
        """Get coordination performance metrics."""
        pass


class CrossSystemMessagingInterface(ABC):
    """Interface for cross-system messaging operations."""
    
    @abstractmethod
    def send_cross_system_message(self, system: str, message: Dict[str, Any]) -> Dict[str, Any]:
        """Send message to another system."""
        pass
    
    @abstractmethod
    def receive_cross_system_message(self, system: str) -> Dict[str, Any]:
        """Receive message from another system."""
        pass


class FSMMessagingInterface(ABC):
    """Interface for FSM messaging operations."""
    
    @abstractmethod
    def send_fsm_message(self, state: str, message: Dict[str, Any]) -> Dict[str, Any]:
        """Send message to FSM state."""
        pass
    
    @abstractmethod
    def receive_fsm_message(self, state: str) -> Dict[str, Any]:
        """Receive message from FSM state."""
        pass


class MessageSenderInterface(ABC):
    """Interface for message sending operations."""
    
    @abstractmethod
    def send_message(self, recipient: str, message: str, message_type: MessageType) -> Dict[str, Any]:
        """Send message to recipient."""
        pass
    
    @abstractmethod
    def get_message_status(self, message_id: str) -> Dict[str, Any]:
        """Get status of sent message."""
        pass


class OnboardingMessagingInterface(ABC):
    """Interface for onboarding messaging operations."""
    
    @abstractmethod
    def send_onboarding_message(self, user_id: str, step: str) -> Dict[str, Any]:
        """Send onboarding message to user."""
        pass
    
    @abstractmethod
    def get_onboarding_progress(self, user_id: str) -> Dict[str, Any]:
        """Get user onboarding progress."""
        pass


class YOLOMessagingInterface(ABC):
    """Interface for YOLO messaging operations."""
    
    @abstractmethod
    def send_yolo_message(self, message: str) -> Dict[str, Any]:
        """Send YOLO message."""
        pass
    
    @abstractmethod
    def get_yolo_status(self, message_id: str) -> Dict[str, Any]:
        """Get YOLO message status."""
        pass
