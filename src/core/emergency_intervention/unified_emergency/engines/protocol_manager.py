"""
Protocol Manager - V2 Compliant Module
=====================================

Manages emergency intervention protocols.
Extracted from engine.py for V2 compliance.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

import time
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime

from ..models import (
    Emergency, EmergencySeverity, EmergencyType, EmergencyStatus,
    InterventionProtocol, InterventionResult, InterventionAction,
    EmergencyResponse, EmergencyContext, EmergencyInterventionModels
)


class ProtocolManager:
    """
    Manages emergency intervention protocols.
    
    Handles protocol registration, matching, and execution
    for emergency intervention operations.
    """
    
    def __init__(self):
        """Initialize protocol manager."""
        self.protocols: Dict[str, InterventionProtocol] = {}
    
    def register_protocol(self, protocol: InterventionProtocol) -> None:
        """Register intervention protocol."""
        self.protocols[protocol.protocol_id] = protocol
    
    def find_matching_protocols(self, emergency: Emergency) -> List[InterventionProtocol]:
        """Find protocols matching emergency type and severity."""
        matching_protocols = []
        
        for protocol in self.protocols.values():
            if (protocol.emergency_type == emergency.emergency_type and
                self._severity_matches(emergency.severity, protocol.severity_threshold)):
                matching_protocols.append(protocol)
        
        # Sort by priority
        return sorted(matching_protocols, key=lambda p: p.priority)
    
    def _severity_matches(self, emergency_severity: EmergencySeverity, threshold: EmergencySeverity) -> bool:
        """Check if emergency severity matches threshold."""
        severity_levels = {
            EmergencySeverity.LOW: 1,
            EmergencySeverity.MEDIUM: 2,
            EmergencySeverity.HIGH: 3,
            EmergencySeverity.CRITICAL: 4
        }
        
        return severity_levels[emergency_severity] >= severity_levels[threshold]
    
    def get_protocol(self, protocol_id: str) -> Optional[InterventionProtocol]:
        """Get protocol by ID."""
        return self.protocols.get(protocol_id)
    
    def get_all_protocols(self) -> List[InterventionProtocol]:
        """Get all registered protocols."""
        return list(self.protocols.values())
    
    def get_protocols_by_type(self, emergency_type: EmergencyType) -> List[InterventionProtocol]:
        """Get protocols for specific emergency type."""
        return [
            protocol for protocol in self.protocols.values()
            if protocol.emergency_type == emergency_type
        ]
    
    def get_protocols_by_severity(self, severity: EmergencySeverity) -> List[InterventionProtocol]:
        """Get protocols for specific severity level."""
        return [
            protocol for protocol in self.protocols.values()
            if self._severity_matches(severity, protocol.severity_threshold)
        ]
    
    def remove_protocol(self, protocol_id: str) -> bool:
        """Remove protocol by ID."""
        if protocol_id in self.protocols:
            del self.protocols[protocol_id]
            return True
        return False
    
    def update_protocol(self, protocol: InterventionProtocol) -> bool:
        """Update existing protocol."""
        if protocol.protocol_id in self.protocols:
            self.protocols[protocol.protocol_id] = protocol
            return True
        return False
    
    def get_protocol_count(self) -> int:
        """Get total number of registered protocols."""
        return len(self.protocols)
    
    def get_protocol_summary(self) -> Dict[str, Any]:
        """Get summary of all protocols."""
        summary = {
            'total_protocols': len(self.protocols),
            'protocols_by_type': {},
            'protocols_by_severity': {},
            'protocols_by_priority': {}
        }
        
        for protocol in self.protocols.values():
            # Count by type
            type_name = protocol.emergency_type.value
            summary['protocols_by_type'][type_name] = summary['protocols_by_type'].get(type_name, 0) + 1
            
            # Count by severity
            severity_name = protocol.severity_threshold.value
            summary['protocols_by_severity'][severity_name] = summary['protocols_by_severity'].get(severity_name, 0) + 1
            
            # Count by priority
            priority = protocol.priority
            summary['protocols_by_priority'][priority] = summary['protocols_by_priority'].get(priority, 0) + 1
        
        return summary
    
    def validate_protocol(self, protocol: InterventionProtocol) -> Dict[str, Any]:
        """Validate protocol configuration."""
        validation_result = {
            'is_valid': True,
            'errors': [],
            'warnings': []
        }
        
        # Check required fields
        if not protocol.protocol_id:
            validation_result['errors'].append("Protocol ID is required")
            validation_result['is_valid'] = False
        
        if not protocol.emergency_type:
            validation_result['errors'].append("Emergency type is required")
            validation_result['is_valid'] = False
        
        if not protocol.actions or len(protocol.actions) == 0:
            validation_result['errors'].append("At least one action is required")
            validation_result['is_valid'] = False
        
        # Check for duplicate protocol ID
        if protocol.protocol_id in self.protocols:
            validation_result['warnings'].append("Protocol ID already exists")
        
        # Check priority range
        if protocol.priority < 1 or protocol.priority > 10:
            validation_result['warnings'].append("Priority should be between 1 and 10")
        
        return validation_result
    
    def clear_protocols(self):
        """Clear all registered protocols."""
        self.protocols.clear()
    
    def export_protocols(self) -> Dict[str, Any]:
        """Export all protocols for backup/transfer."""
        return {
            'protocols': {
                protocol_id: {
                    'protocol_id': protocol.protocol_id,
                    'emergency_type': protocol.emergency_type.value,
                    'severity_threshold': protocol.severity_threshold.value,
                    'priority': protocol.priority,
                    'actions': [action.value for action in protocol.actions],
                    'description': protocol.description,
                    'created_at': protocol.created_at.isoformat() if protocol.created_at else None
                }
                for protocol_id, protocol in self.protocols.items()
            },
            'exported_at': datetime.now().isoformat(),
            'total_protocols': len(self.protocols)
        }
