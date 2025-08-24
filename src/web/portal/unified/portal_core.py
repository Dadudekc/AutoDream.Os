#!/usr/bin/env python3
"""
Unified Portal Core - V2 Core Web Integration

Core portal functionality and management.
Follows V2 standards: ≤300 LOC, SRP, OOP principles.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import logging
import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime

from .enums import PortalSection, AgentDashboard
from .data_models import PortalConfig, AgentPortalInfo, PortalNavigation


class UnifiedPortal:
    """
    Core unified portal system
    
    Single responsibility: Portal management and coordination.
    Follows V2 standards: OOP, SRP, clean production-grade code.
    """

    def __init__(self, config: Optional[PortalConfig] = None):
        """Initialize unified portal"""
        self.config = config or PortalConfig()
        self.navigation = PortalNavigation()
        self.agents: Dict[str, AgentPortalInfo] = {}
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.active_connections: List[str] = []
        
        self.logger = logging.getLogger(f"{__name__}.UnifiedPortal")
        self.logger.info("Unified portal initialized")

    def register_agent(self, agent_info: AgentPortalInfo) -> bool:
        """Register an agent with the portal"""
        try:
            if len(self.agents) >= self.config.max_agents:
                self.logger.warning(f"Maximum agents ({self.config.max_agents}) reached")
                return False
            
            self.agents[agent_info.agent_id] = agent_info
            self.logger.info(f"Agent registered: {agent_info.name} ({agent_info.agent_id})")
            return True
            
        except Exception as e:
            self.logger.error(f"Agent registration failed: {e}")
            return False

    def unregister_agent(self, agent_id: str) -> bool:
        """Unregister an agent from the portal"""
        try:
            if agent_id in self.agents:
                agent_name = self.agents[agent_id].name
                del self.agents[agent_id]
                self.logger.info(f"Agent unregistered: {agent_name} ({agent_id})")
                return True
            return False
            
        except Exception as e:
            self.logger.error(f"Agent unregistration failed: {e}")
            return False

    def get_agent_info(self, agent_id: str) -> Optional[AgentPortalInfo]:
        """Get information about a specific agent"""
        return self.agents.get(agent_id)

    def get_active_agents(self) -> List[AgentPortalInfo]:
        """Get list of currently active agents"""
        return [agent for agent in self.agents.values() if agent.is_active()]

    def get_agents_by_dashboard_type(self, dashboard_type: AgentDashboard) -> List[AgentPortalInfo]:
        """Get agents by dashboard type"""
        return [agent for agent in self.agents.values() if agent.dashboard_type == dashboard_type]

    def create_session(self, user_id: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """Create a new user session"""
        try:
            session_id = str(uuid.uuid4())
            session_data = {
                'user_id': user_id,
                'created_at': datetime.now().isoformat(),
                'last_activity': datetime.now().isoformat(),
                'metadata': metadata or {},
                'active': True
            }
            
            self.sessions[session_id] = session_data
            self.logger.info(f"Session created: {session_id} for user {user_id}")
            return session_id
            
        except Exception as e:
            self.logger.error(f"Session creation failed: {e}")
            raise

    def validate_session(self, session_id: str) -> bool:
        """Validate if a session is still active"""
        if session_id not in self.sessions:
            return False
        
        session = self.sessions[session_id]
        if not session.get('active', False):
            return False
        
        # Check session timeout
        last_activity = datetime.fromisoformat(session['last_activity'])
        timeout_delta = datetime.now() - last_activity
        if timeout_delta.total_seconds() > self.config.session_timeout:
            session['active'] = False
            return False
        
        return True

    def update_session_activity(self, session_id: str):
        """Update session last activity timestamp"""
        if session_id in self.sessions:
            self.sessions[session_id]['last_activity'] = datetime.now().isoformat()

    def terminate_session(self, session_id: str) -> bool:
        """Terminate a user session"""
        try:
            if session_id in self.sessions:
                self.sessions[session_id]['active'] = False
                self.logger.info(f"Session terminated: {session_id}")
                return True
            return False
            
        except Exception as e:
            self.logger.error(f"Session termination failed: {e}")
            return False

    def navigate_to_section(self, section: PortalSection, session_id: Optional[str] = None):
        """Navigate to a specific portal section"""
        try:
            self.navigation.set_current_section(section)
            
            if session_id and self.validate_session(session_id):
                self.update_session_activity(session_id)
            
            self.logger.info(f"Navigation to section: {section.value}")
            
        except Exception as e:
            self.logger.error(f"Navigation failed: {e}")

    def get_navigation_state(self) -> Dict[str, Any]:
        """Get current navigation state"""
        return self.navigation.to_dict()

    def get_portal_status(self) -> Dict[str, Any]:
        """Get overall portal status"""
        return {
            'title': self.config.title,
            'version': self.config.version,
            'active_agents': len(self.get_active_agents()),
            'total_agents': len(self.agents),
            'active_sessions': len([s for s in self.sessions.values() if s.get('active', False)]),
            'total_sessions': len(self.sessions),
            'current_section': self.navigation.current_section.value if self.navigation.current_section else None,
            'features': {
                'real_time': self.config.enable_real_time,
                'websockets': self.config.enable_websockets,
                'agent_integration': self.config.enable_agent_integration
            }
        }

    def add_connection(self, connection_id: str):
        """Add an active connection"""
        if connection_id not in self.active_connections:
            self.active_connections.append(connection_id)

    def remove_connection(self, connection_id: str):
        """Remove an active connection"""
        if connection_id in self.active_connections:
            self.active_connections.remove(connection_id)

    def get_connection_count(self) -> int:
        """Get count of active connections"""
        return len(self.active_connections)

    def cleanup_inactive_sessions(self):
        """Clean up inactive sessions"""
        try:
            current_time = datetime.now()
            sessions_to_terminate = []
            
            for session_id, session in self.sessions.items():
                if not session.get('active', False):
                    continue
                
                last_activity = datetime.fromisoformat(session['last_activity'])
                if (current_time - last_activity).total_seconds() > self.config.session_timeout:
                    sessions_to_terminate.append(session_id)
            
            for session_id in sessions_to_terminate:
                self.terminate_session(session_id)
            
            if sessions_to_terminate:
                self.logger.info(f"Cleaned up {len(sessions_to_terminate)} inactive sessions")
                
        except Exception as e:
            self.logger.error(f"Session cleanup failed: {e}")

    def get_agent_statistics(self) -> Dict[str, Any]:
        """Get agent statistics"""
        total_agents = len(self.agents)
        active_agents = len(self.get_active_agents())
        
        dashboard_counts = {}
        for agent in self.agents.values():
            dashboard_type = agent.dashboard_type.value
            dashboard_counts[dashboard_type] = dashboard_counts.get(dashboard_type, 0) + 1
        
        return {
            'total_agents': total_agents,
            'active_agents': active_agents,
            'inactive_agents': total_agents - active_agents,
            'dashboard_distribution': dashboard_counts,
            'capacity_utilization': (total_agents / self.config.max_agents) * 100
        }
