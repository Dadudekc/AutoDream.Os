#!/usr/bin/env python3
"""
Unified Portal Data Models - V2 Core Web Integration

Portal configuration and data structures.
Follows V2 standards: ≤300 LOC, SRP, OOP principles.

Author: V2 SWARM CAPTAIN
License: MIT
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from .enums import PortalSection, AgentDashboard


@dataclass
class PortalConfig:
    """Portal configuration settings"""
    title: str = "Agent_Cellphone_V2 Unified Portal"
    version: str = "1.0.0"
    theme: str = "default"
    enable_real_time: bool = True
    enable_websockets: bool = True
    enable_agent_integration: bool = True
    max_agents: int = 8
    session_timeout: int = 3600
    debug_mode: bool = False
    api_endpoints: Dict[str, str] = field(default_factory=dict)
    security_settings: Dict[str, Any] = field(default_factory=dict)
    performance_settings: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary"""
        return {
            'title': self.title,
            'version': self.version,
            'theme': self.theme,
            'enable_real_time': self.enable_real_time,
            'enable_websockets': self.enable_websockets,
            'enable_agent_integration': self.enable_agent_integration,
            'max_agents': self.max_agents,
            'session_timeout': self.session_timeout,
            'debug_mode': self.debug_mode,
            'api_endpoints': self.api_endpoints,
            'security_settings': self.security_settings,
            'performance_settings': self.performance_settings
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PortalConfig':
        """Create config from dictionary"""
        return cls(**data)


@dataclass
class AgentPortalInfo:
    """Information about an agent's portal integration"""
    agent_id: str
    name: str
    description: str
    dashboard_type: AgentDashboard
    capabilities: List[str] = field(default_factory=list)
    status: str = "active"
    last_seen: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    permissions: List[str] = field(default_factory=list)
    
    def is_active(self) -> bool:
        """Check if agent is currently active"""
        return self.status == "active"
    
    def has_capability(self, capability: str) -> bool:
        """Check if agent has specific capability"""
        return capability in self.capabilities
    
    def has_permission(self, permission: str) -> bool:
        """Check if agent has specific permission"""
        return permission in self.permissions
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'agent_id': self.agent_id,
            'name': self.name,
            'description': self.description,
            'dashboard_type': self.dashboard_type.value,
            'capabilities': self.capabilities,
            'status': self.status,
            'last_seen': self.last_seen,
            'metadata': self.metadata,
            'permissions': self.permissions
        }


@dataclass
class PortalNavigation:
    """Portal navigation structure"""
    sections: List[PortalSection] = field(default_factory=list)
    current_section: Optional[PortalSection] = None
    breadcrumbs: List[str] = field(default_factory=list)
    navigation_tree: Dict[str, Any] = field(default_factory=dict)
    
    def add_section(self, section: PortalSection):
        """Add navigation section"""
        if section not in self.sections:
            self.sections.append(section)
    
    def set_current_section(self, section: PortalSection):
        """Set current navigation section"""
        self.current_section = section
        self._update_breadcrumbs(section)
    
    def _update_breadcrumbs(self, section: PortalSection):
        """Update breadcrumb navigation"""
        if section:
            section_name = section.value.replace('_', ' ').title()
            if section_name not in self.breadcrumbs:
                self.breadcrumbs.append(section_name)
    
    def get_navigation_path(self) -> List[str]:
        """Get current navigation path"""
        return self.breadcrumbs.copy()
    
    def clear_breadcrumbs(self):
        """Clear breadcrumb navigation"""
        self.breadcrumbs.clear()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'sections': [section.value for section in self.sections],
            'current_section': self.current_section.value if self.current_section else None,
            'breadcrumbs': self.breadcrumbs,
            'navigation_tree': self.navigation_tree
        }

