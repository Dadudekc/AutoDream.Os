#!/usr/bin/env python3
"""
Emergency Response Core Module - Extracted from emergency_response_system.py
Agent-3: Monolithic File Modularization Contract

This module contains the main EmergencyResponseSystem class and core functionality.
"""

import logging
import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

from ..base_manager import BaseManager, ManagerStatus, ManagerPriority
from .emergency_types import EmergencyEvent, EmergencyType, EmergencyLevel
from .emergency_monitoring import EmergencyMonitoring
from .protocol_manager import ProtocolManager
from .emergency_coordination import EmergencyCoordination
from .recovery_manager import RecoveryManager
from .emergency_documentation import EmergencyDocumentation
from .health_integration import HealthIntegration

logger = logging.getLogger(__name__)


class EmergencyResponseSystem(BaseManager):
    """
    Emergency Response System - Single responsibility: Emergency response management
    
    This system implements:
    - Automated failure detection and monitoring
    - Emergency protocol activation and execution
    - Rapid recovery procedures
    - Emergency documentation and reporting
    - Integration with existing health monitoring
    """

    def __init__(self, config_path: str = "config/emergency_response.json"):
        """Initialize emergency response system"""
        super().__init__(
            manager_id="emergency_response_system",
            manager_name="Emergency Response System",
            manager_type="emergency_response",
            priority=ManagerPriority.CRITICAL,
            status=ManagerStatus.INITIALIZING
        )
        
        self.config_path = config_path
        self.config = self._load_emergency_config()
        
        # Initialize component managers
        self.monitoring = None
        self.protocol_manager = None
        self.coordination = None
        self.recovery_manager = None
        self.documentation = None
        self.health_integration = None
        
        # Emergency tracking
        self.active_emergencies: Dict[str, EmergencyEvent] = {}
        self.emergency_history: List[EmergencyEvent] = []
        self.emergency_counter = 0
        
        # Initialize system
        self._initialize_system()
    
    def _load_emergency_config(self) -> Dict[str, Any]:
        """Load emergency response configuration"""
        try:
            if Path(self.config_path).exists():
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                logger.info("Emergency response config loaded successfully")
                return config
            else:
                logger.warning(f"Emergency config not found: {self.config_path}")
                return self._get_default_config()
        except Exception as e:
            logger.error(f"Error loading emergency config: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default emergency response configuration"""
        return {
            "monitoring_interval": 30,
            "max_active_emergencies": 10,
            "auto_recovery_enabled": True,
            "documentation_required": True,
            "coordination_enabled": True,
            "health_integration_enabled": True,
            "default_protocols": ["system_failure", "workflow_stall"],
            "escalation_timeout": 1800,  # 30 minutes
            "recovery_timeout": 3600     # 1 hour
        }
    
    def _initialize_system(self):
        """Initialize emergency response system components"""
        try:
            logger.info("Initializing Emergency Response System")
            
            # Initialize component managers
            self._initialize_component_managers()
            
            # Setup default protocols
            self._setup_default_protocols()
            
            # Setup health integration
            self._setup_health_integration()
            
            # Update status
            self.status = ManagerStatus.ACTIVE
            logger.info("Emergency Response System initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing Emergency Response System: {e}")
            self.status = ManagerStatus.ERROR
    
    def _initialize_component_managers(self):
        """Initialize component managers"""
        try:
            # Initialize protocol manager
            self.protocol_manager = ProtocolManager()
            logger.info("Protocol Manager initialized")
            
            # Initialize coordination
            self.coordination = EmergencyCoordination()
            logger.info("Emergency Coordination initialized")
            
            # Initialize recovery manager
            self.recovery_manager = RecoveryManager()
            logger.info("Recovery Manager initialized")
            
            # Initialize documentation
            self.documentation = EmergencyDocumentation()
            logger.info("Emergency Documentation initialized")
            
        except Exception as e:
            logger.error(f"Error initializing component managers: {e}")
            raise
    
    def _setup_default_protocols(self):
        """Setup default emergency protocols"""
        try:
            # Default protocols are already set up in ProtocolManager
            logger.info("Default emergency protocols configured")
            
        except Exception as e:
            logger.error(f"Error setting up default protocols: {e}")
    
    def _setup_health_integration(self):
        """Setup health monitoring integration"""
        try:
            # This would typically initialize health monitoring components
            # For now, we'll create placeholder components
            logger.info("Health integration setup completed")
            
        except Exception as e:
            logger.error(f"Error setting up health integration: {e}")
    
    def trigger_emergency(self, emergency_type: EmergencyType, 
                         level: EmergencyLevel, 
                         description: str, 
                         source: str,
                         affected_components: Optional[List[str]] = None,
                         impact_assessment: Optional[Dict[str, Any]] = None) -> EmergencyEvent:
        """Trigger a new emergency"""
        try:
            # Generate emergency ID
            self.emergency_counter += 1
            emergency_id = f"EMERGENCY-{self.emergency_counter:04d}-{int(time.time())}"
            
            # Create emergency event
            emergency = EmergencyEvent(
                id=emergency_id,
                type=emergency_type,
                level=level,
                description=description,
                timestamp=datetime.now(),
                source=source,
                affected_components=affected_components or [],
                impact_assessment=impact_assessment or {}
            )
            
            # Add to active emergencies
            self.active_emergencies[emergency_id] = emergency
            
            # Record in history
            self.emergency_history.append(emergency)
            
            logger.warning(f"Emergency triggered: {emergency_id} - {emergency_type.value} ({level.value})")
            
            # Start emergency response
            self._start_emergency_response(emergency)
            
            return emergency
            
        except Exception as e:
            logger.error(f"Error triggering emergency: {e}")
            raise
    
    def _start_emergency_response(self, emergency: EmergencyEvent):
        """Start emergency response process"""
        try:
            logger.info(f"Starting emergency response for: {emergency.id}")
            
            # Activate emergency protocol
            if self.protocol_manager:
                protocol_activated = self.protocol_manager.activate_emergency_protocol(emergency)
                if protocol_activated:
                    logger.info(f"Emergency protocol activated for: {emergency.id}")
                else:
                    logger.error(f"Failed to activate emergency protocol for: {emergency.id}")
            
            # Activate emergency coordination
            if self.coordination:
                coordination_activated = self.coordination.activate_emergency_coordination(emergency)
                if coordination_activated:
                    logger.info(f"Emergency coordination activated for: {emergency.id}")
                else:
                    logger.error(f"Failed to activate emergency coordination for: {emergency.id}")
            
            # Start recovery process
            if self.recovery_manager:
                recovery_started = self.recovery_manager.start_recovery_process(emergency)
                if recovery_started:
                    logger.info(f"Recovery process started for: {emergency.id}")
                else:
                    logger.error(f"Failed to start recovery process for: {emergency.id}")
            
            # Generate documentation
            if self.documentation and self.config.get("documentation_required", True):
                self._generate_emergency_documentation(emergency)
            
            logger.info(f"Emergency response started for: {emergency.id}")
            
        except Exception as e:
            logger.error(f"Error starting emergency response: {e}")
    
    def _generate_emergency_documentation(self, emergency: EmergencyEvent):
        """Generate emergency documentation"""
        try:
            # Collect response data
            response_data = {
                "actions_taken": ["Emergency protocol activated", "Coordination initiated", "Recovery started"],
                "timestamp": datetime.now().isoformat()
            }
            
            # Get recovery data if available
            recovery_data = None
            if self.recovery_manager:
                recovery_data = self.recovery_manager.get_recovery_status(emergency.id)
            
            # Generate documentation
            if self.documentation:
                generated_files = self.documentation.generate_emergency_documentation(
                    emergency, response_data, recovery_data
                )
                logger.info(f"Emergency documentation generated: {len(generated_files)} files")
            
        except Exception as e:
            logger.error(f"Error generating emergency documentation: {e}")
    
    def resolve_emergency(self, emergency_id: str, resolution_notes: Optional[str] = None) -> bool:
        """Resolve an emergency"""
        try:
            if emergency_id not in self.active_emergencies:
                logger.warning(f"Emergency not found: {emergency_id}")
                return False
            
            emergency = self.active_emergencies[emergency_id]
            emergency.status = "resolved"
            emergency.resolution_time = datetime.now()
            
            if resolution_notes:
                emergency.lessons_learned.append(resolution_notes)
            
            # Remove from active emergencies
            del self.active_emergencies[emergency_id]
            
            # Stop coordination if active
            if self.coordination:
                self.coordination.stop_coordination()
            
            # Generate final documentation
            if self.documentation:
                self._generate_final_documentation(emergency)
            
            logger.info(f"Emergency resolved: {emergency_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error resolving emergency: {e}")
            return False
    
    def _generate_final_documentation(self, emergency: EmergencyEvent):
        """Generate final documentation for resolved emergency"""
        try:
            # Collect final response data
            response_data = {
                "actions_taken": ["Emergency resolved", "Coordination stopped", "Recovery completed"],
                "resolution_time": emergency.resolution_time.isoformat() if emergency.resolution_time else None,
                "timestamp": datetime.now().isoformat()
            }
            
            # Get final recovery data
            recovery_data = None
            if self.recovery_manager:
                recovery_data = self.recovery_manager.get_recovery_status(emergency.id)
            
            # Generate final documentation
            if self.documentation:
                generated_files = self.documentation.generate_emergency_documentation(
                    emergency, response_data, recovery_data
                )
                logger.info(f"Final documentation generated: {len(generated_files)} files")
            
        except Exception as e:
            logger.error(f"Error generating final documentation: {e}")
    
    def get_emergency_status(self, emergency_id: str) -> Optional[Dict[str, Any]]:
        """Get status of specific emergency"""
        try:
            if emergency_id not in self.active_emergencies:
                return None
            
            emergency = self.active_emergencies[emergency_id]
            
            status = {
                "emergency_id": emergency.id,
                "type": emergency.type.value,
                "level": emergency.level.value,
                "description": emergency.description,
                "timestamp": emergency.timestamp.isoformat(),
                "status": emergency.status,
                "source": emergency.source,
                "affected_components": emergency.affected_components,
                "impact_assessment": emergency.impact_assessment
            }
            
            # Add protocol status
            if self.protocol_manager:
                protocol_status = self.protocol_manager.get_protocol_status(emergency_id)
                if protocol_status:
                    status["protocol_status"] = protocol_status
            
            # Add coordination status
            if self.coordination:
                coordination_status = self.coordination.get_coordination_status()
                status["coordination_status"] = coordination_status
            
            # Add recovery status
            if self.recovery_manager:
                recovery_status = self.recovery_manager.get_recovery_status(emergency_id)
                if recovery_status:
                    status["recovery_status"] = recovery_status
            
            return status
            
        except Exception as e:
            logger.error(f"Error getting emergency status: {e}")
            return None
    
    def get_emergency_history(self) -> List[Dict[str, Any]]:
        """Get emergency history"""
        try:
            history = []
            
            for emergency in self.emergency_history:
                history.append({
                    "emergency_id": emergency.id,
                    "type": emergency.type.value,
                    "level": emergency.level.value,
                    "description": emergency.description,
                    "timestamp": emergency.timestamp.isoformat(),
                    "status": emergency.status,
                    "source": emergency.source,
                    "resolution_time": emergency.resolution_time.isoformat() if emergency.resolution_time else None
                })
            
            return history
            
        except Exception as e:
            logger.error(f"Error getting emergency history: {e}")
            return []
    
    def health_check(self) -> Dict[str, Any]:
        """Perform health check on emergency response system"""
        try:
            health_status = {
                "system_status": self.status.value,
                "active_emergencies": len(self.active_emergencies),
                "total_emergencies": len(self.emergency_history),
                "components": {}
            }
            
            # Check component health
            if self.protocol_manager:
                health_status["components"]["protocol_manager"] = "healthy"
            else:
                health_status["components"]["protocol_manager"] = "unavailable"
            
            if self.coordination:
                health_status["components"]["coordination"] = "healthy"
            else:
                health_status["components"]["coordination"] = "unavailable"
            
            if self.recovery_manager:
                health_status["components"]["recovery_manager"] = "healthy"
            else:
                health_status["components"]["recovery_manager"] = "unavailable"
            
            if self.documentation:
                health_status["components"]["documentation"] = "healthy"
            else:
                health_status["components"]["documentation"] = "unavailable"
            
            # Overall health
            if all(status == "healthy" for status in health_status["components"].values()):
                health_status["overall_health"] = "healthy"
            elif any(status == "unavailable" for status in health_status["components"].values()):
                health_status["overall_health"] = "degraded"
            else:
                health_status["overall_health"] = "unhealthy"
            
            return health_status
            
        except Exception as e:
            logger.error(f"Error performing health check: {e}")
            return {"error": str(e), "overall_health": "error"}
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get overall system status"""
        return {
            "manager_id": self.manager_id,
            "manager_name": self.manager_name,
            "status": self.status.value,
            "priority": self.priority.value,
            "active_emergencies": len(self.active_emergencies),
            "total_emergencies": len(self.emergency_history),
            "config": self.config,
            "health_status": self.health_check()
        }
    
    def shutdown(self):
        """Shutdown emergency response system"""
        try:
            logger.info("Shutting down Emergency Response System")
            
            # Stop all active emergencies
            for emergency_id in list(self.active_emergencies.keys()):
                self.resolve_emergency(emergency_id, "System shutdown")
            
            # Stop coordination
            if self.coordination:
                self.coordination.stop_coordination()
            
            # Update status
            self.status = ManagerStatus.SHUTDOWN
            
            logger.info("Emergency Response System shutdown completed")
            
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")
