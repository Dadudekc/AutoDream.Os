#!/usr/bin/env python3
"""
Communication Bridge - V2 Modular Architecture
=============================================

Communication functionality for the FSM system.
Follows V2 standards: OOP design, SRP, no strict LOC limits.

Author: Agent-4 (Captain)
Task: TASK 4I - FSM System Modularization
License: MIT
"""

import logging
import json
import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime

from .models import FSMCommunicationEvent, BridgeState
from .types import FSMConfig


logger = logging.getLogger(__name__)


class CommunicationBridge:
    """
    Communication Bridge - Inter-Agent Communication
    
    Single responsibility: Manage communication events, bridge states,
    and inter-agent messaging following V2 architecture standards.
    """
    
    def __init__(self, config: Optional[FSMConfig] = None):
        """Initialize communication bridge."""
        self.logger = logging.getLogger(f"{__name__}.CommunicationBridge")
        
        # Configuration
        self.config = config or FSMConfig()
        
        # Communication state
        self._communication_events: List[FSMCommunicationEvent] = []
        self._bridge_states: Dict[str, BridgeState] = {}
        
        # Communication history
        self._communication_history: List[Dict[str, Any]] = []
        
        self.logger.info("✅ Communication Bridge initialized successfully")
    
    # ============================================================================
    # COMMUNICATION EVENTS
    # ============================================================================
    
    def send_communication_event(
        self,
        event_type: str,
        source_agent: str,
        target_agent: str,
        message: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Send a communication event."""
        try:
            event_id = str(uuid.uuid4())
            now = datetime.now().isoformat()

            event = FSMCommunicationEvent(
                event_id=event_id,
                event_type=event_type,
                source_agent=source_agent,
                target_agent=target_agent,
                message=message,
                timestamp=now,
                metadata=metadata or {},
            )

            self._communication_events.append(event)
            self._save_communication_event(event)
            
            # Record in history
            self._communication_history.append({
                "timestamp": time.time(),
                "event_id": event_id,
                "event_type": event_type,
                "source_agent": source_agent,
                "target_agent": target_agent,
                "message": message
            })

            self.logger.info(f"Sent communication event: {event_id}")
            return event_id

        except Exception as e:
            self.logger.error(f"Failed to send communication event: {e}")
            return ""
    
    def get_communication_events(
        self,
        source_agent: Optional[str] = None,
        target_agent: Optional[str] = None,
        event_type: Optional[str] = None,
    ) -> List[FSMCommunicationEvent]:
        """Get communication events with optional filtering."""
        events = self._communication_events

        if source_agent:
            events = [e for e in events if e.source_agent == source_agent]
        if target_agent:
            events = [e for e in events if e.target_agent == target_agent]
        if event_type:
            events = [e for e in events if e.event_type == event_type]

        return events
    
    def get_communication_history(
        self,
        source_agent: Optional[str] = None,
        target_agent: Optional[str] = None,
        event_type: Optional[str] = None,
        time_range_hours: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get communication history with optional filtering."""
        history = self._communication_history

        if source_agent:
            history = [h for h in history if h.get("source_agent") == source_agent]
        if target_agent:
            history = [h for h in history if h.get("target_agent") == target_agent]
        if event_type:
            history = [h for h in history if h.get("event_type") == event_type]
        if time_range_hours:
            cutoff_time = time.time() - (time_range_hours * 3600)
            history = [h for h in history if h.get("timestamp", 0) > cutoff_time]

        return history
    
    # ============================================================================
    # BRIDGE MANAGEMENT
    # ============================================================================
    
    def update_bridge_state(self, bridge_id: str, new_state: BridgeState) -> bool:
        """Update bridge state."""
        try:
            self._bridge_states[bridge_id] = new_state
            self.logger.info(f"Updated bridge {bridge_id} state: {new_state.value}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to update bridge state: {e}")
            return False
    
    def get_bridge_state(self, bridge_id: str) -> Optional[BridgeState]:
        """Get bridge state."""
        return self._bridge_states.get(bridge_id)
    
    def get_all_bridge_states(self) -> Dict[str, BridgeState]:
        """Get all bridge states."""
        return dict(self._bridge_states)
    
    def create_bridge(self, bridge_id: str, initial_state: BridgeState = BridgeState.IDLE) -> bool:
        """Create a new communication bridge."""
        try:
            if bridge_id in self._bridge_states:
                self.logger.warning(f"Bridge {bridge_id} already exists")
                return False
            
            self._bridge_states[bridge_id] = initial_state
            self.logger.info(f"✅ Created bridge: {bridge_id} with state: {initial_state.value}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to create bridge {bridge_id}: {e}")
            return False
    
    def remove_bridge(self, bridge_id: str) -> bool:
        """Remove a communication bridge."""
        try:
            if bridge_id not in self._bridge_states:
                self.logger.warning(f"Bridge {bridge_id} not found")
                return False
            
            del self._bridge_states[bridge_id]
            self.logger.info(f"✅ Removed bridge: {bridge_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to remove bridge {bridge_id}: {e}")
            return False
    
    # ============================================================================
    # COMMUNICATION ANALYSIS
    # ============================================================================
    
    def analyze_communication_patterns(self, time_range_hours: int = 24) -> Dict[str, Any]:
        """Analyze communication patterns for insights."""
        try:
            # Get recent communication data
            recent_time = time.time() - (time_range_hours * 3600)
            recent_events = [e for e in self._communication_history if e.get("timestamp", 0) > recent_time]
            
            analysis = {
                "total_events": len(recent_events),
                "event_type_distribution": {},
                "agent_communication_matrix": {},
                "communication_frequency": {},
                "patterns": []
            }
            
            # Analyze event types
            for event in recent_events:
                event_type = event.get("event_type", "unknown")
                analysis["event_type_distribution"][event_type] = analysis["event_type_distribution"].get(event_type, 0) + 1
            
            # Analyze agent communication
            for event in recent_events:
                source = event.get("source_agent", "unknown")
                target = event.get("target_agent", "unknown")
                
                if source not in analysis["agent_communication_matrix"]:
                    analysis["agent_communication_matrix"][source] = {}
                if target not in analysis["agent_communication_matrix"][source]:
                    analysis["agent_communication_matrix"][source][target] = 0
                
                analysis["agent_communication_matrix"][source][target] += 1
            
            # Analyze communication frequency
            for event in recent_events:
                source = event.get("source_agent", "unknown")
                analysis["communication_frequency"][source] = analysis["communication_frequency"].get(source, 0) + 1
            
            # Identify patterns
            if analysis["total_events"] > 0:
                if analysis["total_events"] > 100:
                    analysis["patterns"].append("High communication volume - consider optimization")
                
                # Check for communication bottlenecks
                high_frequency_agents = [agent for agent, count in analysis["communication_frequency"].items() if count > 20]
                if high_frequency_agents:
                    analysis["patterns"].append(f"High communication frequency agents: {', '.join(high_frequency_agents)}")
            
            self.logger.info(f"Communication pattern analysis completed")
            return analysis
            
        except Exception as e:
            self.logger.error(f"Failed to analyze communication patterns: {e}")
            return {"error": str(e)}
    
    def get_communication_statistics(self) -> Dict[str, Any]:
        """Get communication system statistics."""
        try:
            total_events = len(self._communication_events)
            total_bridges = len(self._bridge_states)
            
            # Calculate bridge state distribution
            bridge_state_distribution = {}
            for state in self._bridge_states.values():
                bridge_state_distribution[state.value] = bridge_state_distribution.get(state.value, 0) + 1
            
            # Calculate event type distribution
            event_type_distribution = {}
            for event in self._communication_events:
                event_type = event.event_type
                event_type_distribution[event_type] = event_type_distribution.get(event_type, 0) + 1
            
            return {
                "total_communication_events": total_events,
                "total_bridges": total_bridges,
                "bridge_state_distribution": bridge_state_distribution,
                "event_type_distribution": event_type_distribution,
                "active_bridges": len([b for b in self._bridge_states.values() if b == BridgeState.CONNECTED]),
                "last_updated": time.time()
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get communication statistics: {e}")
            return {"error": str(e)}
    
    # ============================================================================
    # STORAGE AND PERSISTENCE
    # ============================================================================
    
    def _save_communication_event(self, event: FSMCommunicationEvent) -> None:
        """Save communication event to storage."""
        try:
            # This would implement actual storage logic
            # For now, just log the event
            self.logger.debug(f"Communication event saved: {event.event_id}")
        except Exception as e:
            self.logger.error(f"Failed to save communication event {event.event_id}: {e}")
    
    # ============================================================================
    # CLEANUP AND MAINTENANCE
    # ============================================================================
    
    def cleanup_old_events(self, retention_hours: int = 24) -> int:
        """Clean up old communication events."""
        try:
            cutoff_time = time.time() - (retention_hours * 3600)
            old_events = [e for e in self._communication_events if e.timestamp < datetime.fromtimestamp(cutoff_time).isoformat()]
            
            cleaned_count = 0
            for event in old_events:
                try:
                    self._communication_events.remove(event)
                    cleaned_count += 1
                except Exception as e:
                    self.logger.warning(f"Failed to cleanup event {event.event_id}: {e}")
            
            if cleaned_count > 0:
                self.logger.info(f"Cleaned up {cleaned_count} old communication events")
            
            return cleaned_count
            
        except Exception as e:
            self.logger.error(f"Failed to cleanup old events: {e}")
            return 0
    
    def cleanup(self):
        """Cleanup communication bridge resources."""
        try:
            # Clean up old events
            self.cleanup_old_events()
            
            self.logger.info("CommunicationBridge cleanup completed")
        except Exception as e:
            self.logger.error(f"CommunicationBridge cleanup failed: {e}")


# Import time module for timestamp operations
import time

