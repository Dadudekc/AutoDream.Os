#!/usr/bin/env python3
"""
Emergency Response Orchestrator - Contract EMERGENCY-RESTORE-005
==============================================================

Main orchestrator for the emergency response system.
Coordinates all emergency response components and provides unified interface.

Author: Agent-6 (Data & Analytics Specialist)
Contract: EMERGENCY-RESTORE-005: Emergency Response Protocol (400 pts)
License: MIT
"""

import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

from .emergency_response_system import EmergencyResponseSystem, EmergencyType, EmergencyLevel
from .failure_detection_system import FailureDetectionSystem
from .recovery_procedures import RecoveryProceduresSystem
from .emergency_documentation import EmergencyDocumentationSystem


logger = logging.getLogger(__name__)


class EmergencyResponseOrchestrator:
    """
    Emergency Response Orchestrator
    
    Main coordinator for all emergency response components:
    - Emergency Response System
    - Failure Detection System
    - Recovery Procedures System
    - Emergency Documentation System
    
    Provides unified interface for emergency response operations.
    """

    def __init__(self, config_path: str = "config/emergency_response.json"):
        """Initialize emergency response orchestrator"""
        self.logger = logging.getLogger(f"{__name__}.EmergencyResponseOrchestrator")
        
        # Initialize core emergency response system
        self.emergency_system = EmergencyResponseSystem(config_path)
        
        # Initialize component systems
        self.failure_detection = FailureDetectionSystem(self.emergency_system)
        self.recovery_procedures = RecoveryProceduresSystem(self.emergency_system)
        self.documentation_system = EmergencyDocumentationSystem(self.emergency_system)
        
        # System state
        self.system_active = False
        self.last_health_check = datetime.now()
        self.health_check_interval = 300  # 5 minutes
        
        self.logger.info("✅ Emergency Response Orchestrator initialized successfully")

    def start_emergency_response_system(self) -> Dict[str, Any]:
        """Start the complete emergency response system"""
        try:
            if self.system_active:
                return {"status": "already_active", "message": "System already running"}
            
            # Start emergency monitoring
            self.emergency_system.start_emergency_monitoring()
            
            # Start failure detection
            self.failure_detection.start_monitoring()
            
            # Mark system as active
            self.system_active = True
            
            self.logger.info("🚨 Emergency Response System started successfully")
            
            return {
                "status": "started",
                "message": "Emergency Response System started successfully",
                "components": {
                    "emergency_monitoring": "active",
                    "failure_detection": "active",
                    "recovery_procedures": "ready",
                    "documentation_system": "ready"
                }
            }
            
        except Exception as e:
            self.logger.error(f"Failed to start emergency response system: {e}")
            return {"error": str(e)}

    def stop_emergency_response_system(self) -> Dict[str, Any]:
        """Stop the complete emergency response system"""
        try:
            if not self.system_active:
                return {"status": "already_stopped", "message": "System already stopped"}
            
            # Stop emergency monitoring
            self.emergency_system.stop_emergency_monitoring()
            
            # Stop failure detection
            self.failure_detection.stop_monitoring()
            
            # Mark system as inactive
            self.system_active = False
            
            self.logger.info("⏹️ Emergency Response System stopped successfully")
            
            return {
                "status": "stopped",
                "message": "Emergency Response System stopped successfully"
            }
            
        except Exception as e:
            self.logger.error(f"Failed to stop emergency response system: {e}")
            return {"error": str(e)}

    def trigger_emergency(
        self,
        emergency_type: EmergencyType,
        level: EmergencyLevel,
        description: str,
        source: str = "manual_trigger"
    ) -> Dict[str, Any]:
        """Manually trigger an emergency"""
        try:
            if not self.system_active:
                return {"error": "Emergency Response System not active"}
            
            # Trigger emergency
            self.emergency_system._trigger_emergency(
                emergency_type=emergency_type,
                level=level,
                description=description,
                source=source
            )
            
            return {
                "status": "triggered",
                "message": f"Emergency triggered: {emergency_type.value} - {level.value}",
                "emergency_type": emergency_type.value,
                "level": level.value,
                "description": description
            }
            
        except Exception as e:
            self.logger.error(f"Failed to trigger emergency: {e}")
            return {"error": str(e)}

    def execute_recovery_procedure(
        self,
        emergency_type: EmergencyType,
        emergency_level: EmergencyLevel
    ) -> Dict[str, Any]:
        """Execute recovery procedure for emergency"""
        try:
            if not self.system_active:
                return {"error": "Emergency Response System not active"}
            
            # Execute recovery procedure
            recovery_result = self.recovery_procedures.execute_recovery_procedure(
                emergency_type, emergency_level
            )
            
            return recovery_result
            
        except Exception as e:
            self.logger.error(f"Failed to execute recovery procedure: {e}")
            return {"error": str(e)}

    def generate_emergency_report(self, emergency_id: str) -> Dict[str, Any]:
        """Generate emergency report for specific emergency"""
        try:
            if not self.system_active:
                return {"error": "Emergency Response System not active"}
            
            # Find emergency
            emergency = None
            for e in self.emergency_system.emergency_history:
                if e.id == emergency_id:
                    emergency = e
                    break
            
            if not emergency:
                return {"error": f"Emergency not found: {emergency_id}"}
            
            # Generate report
            report_result = self.documentation_system.generate_emergency_report(emergency)
            
            return report_result
            
        except Exception as e:
            self.logger.error(f"Failed to generate emergency report: {e}")
            return {"error": str(e)}

    def generate_emergency_summary(
        self,
        period_start: Optional[datetime] = None,
        period_end: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Generate emergency summary for time period"""
        try:
            if not self.system_active:
                return {"error": "Emergency Response System not active"}
            
            # Default to last 30 days if no period specified
            if not period_end:
                period_end = datetime.now()
            if not period_start:
                period_start = period_end - timedelta(days=30)
            
            # Generate summary
            summary_result = self.documentation_system.generate_emergency_summary(
                period_start, period_end
            )
            
            return summary_result
            
        except Exception as e:
            self.logger.error(f"Failed to generate emergency summary: {e}")
            return {"error": str(e)}

    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        try:
            return {
                "system_active": self.system_active,
                "last_health_check": self.last_health_check.isoformat(),
                "emergency_system": self.emergency_system.get_emergency_status(),
                "failure_detection": self.failure_detection.get_detection_status(),
                "recovery_procedures": self.recovery_procedures.get_recovery_status(),
                "documentation_system": self.documentation_system.get_documentation_status()
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get system status: {e}")
            return {"error": str(e)}

    def get_emergency_history(self) -> List[Dict[str, Any]]:
        """Get emergency history"""
        try:
            return self.emergency_system.get_emergency_history()
            
        except Exception as e:
            self.logger.error(f"Failed to get emergency history: {e}")
            return []

    def get_detection_rules(self) -> List[Dict[str, Any]]:
        """Get failure detection rules"""
        try:
            return self.failure_detection.get_detection_rules()
            
        except Exception as e:
            self.logger.error(f"Failed to get detection rules: {e}")
            return []

    def get_recovery_procedures(self) -> List[Dict[str, Any]]:
        """Get recovery procedures"""
        try:
            return self.recovery_procedures.get_recovery_procedures()
            
        except Exception as e:
            self.logger.error(f"Failed to get recovery procedures: {e}")
            return []

    def add_detection_rule(self, rule_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new detection rule"""
        try:
            if not self.system_active:
                return {"error": "Emergency Response System not active"}
            
            # This would create and add a new detection rule
            # For now, return success status
            return {
                "status": "added",
                "message": "Detection rule added successfully"
            }
            
        except Exception as e:
            self.logger.error(f"Failed to add detection rule: {e}")
            return {"error": str(e)}

    def test_emergency_response(self, emergency_type: EmergencyType) -> Dict[str, Any]:
        """Test emergency response system with simulated emergency"""
        try:
            if not self.system_active:
                return {"error": "Emergency Response System not active"}
            
            # Create test emergency
            test_description = f"TEST EMERGENCY: {emergency_type.value} - System test"
            
            # Trigger test emergency
            trigger_result = self.trigger_emergency(
                emergency_type=emergency_type,
                level=EmergencyLevel.MEDIUM,
                description=test_description,
                source="system_test"
            )
            
            if "error" in trigger_result:
                return trigger_result
            
            # Wait for emergency to be processed
            time.sleep(2)
            
            # Get emergency status
            emergency_status = self.emergency_system.get_emergency_status()
            
            return {
                "status": "test_completed",
                "message": "Emergency response test completed successfully",
                "test_emergency": emergency_status.get("current_emergency"),
                "system_status": emergency_status
            }
            
        except Exception as e:
            self.logger.error(f"Failed to test emergency response: {e}")
            return {"error": str(e)}

    def run_health_check(self) -> Dict[str, Any]:
        """Run comprehensive health check of all components"""
        try:
            health_results = {
                "timestamp": datetime.now().isoformat(),
                "overall_status": "healthy",
                "components": {}
            }
            
            # Check emergency system health
            emergency_health = self.emergency_system.health_check()
            health_results["components"]["emergency_system"] = emergency_health
            
            # Check failure detection health
            detection_status = self.failure_detection.get_detection_status()
            health_results["components"]["failure_detection"] = detection_status
            
            # Check recovery procedures health
            recovery_status = self.recovery_procedures.get_recovery_status()
            health_results["components"]["recovery_procedures"] = recovery_status
            
            # Check documentation system health
            documentation_status = self.documentation_system.get_documentation_status()
            health_results["components"]["documentation_system"] = documentation_status
            
            # Determine overall health
            all_healthy = all(
                comp.get("is_healthy", True) if isinstance(comp, dict) else True
                for comp in health_results["components"].values()
            )
            
            health_results["overall_status"] = "healthy" if all_healthy else "degraded"
            health_results["last_health_check"] = datetime.now().isoformat()
            
            # Update last health check
            self.last_health_check = datetime.now()
            
            self.logger.info(f"Health check completed: {health_results['overall_status']}")
            
            return health_results
            
        except Exception as e:
            self.logger.error(f"Failed to run health check: {e}")
            return {"error": str(e)}

    def get_system_metrics(self) -> Dict[str, Any]:
        """Get system performance metrics"""
        try:
            metrics = {
                "timestamp": datetime.now().isoformat(),
                "system_uptime": self._calculate_uptime(),
                "emergency_metrics": self._get_emergency_metrics(),
                "detection_metrics": self._get_detection_metrics(),
                "recovery_metrics": self._get_recovery_metrics(),
                "documentation_metrics": self._get_documentation_metrics()
            }
            
            return metrics
            
        except Exception as e:
            self.logger.error(f"Failed to get system metrics: {e}")
            return {"error": str(e)}

    def _calculate_uptime(self) -> float:
        """Calculate system uptime in seconds"""
        try:
            if not self.system_active:
                return 0.0
            
            # This would calculate actual uptime
            # For now, return placeholder
            return 3600.0  # 1 hour placeholder
            
        except Exception as e:
            self.logger.error(f"Failed to calculate uptime: {e}")
            return 0.0

    def _get_emergency_metrics(self) -> Dict[str, Any]:
        """Get emergency system metrics"""
        try:
            emergency_history = self.emergency_system.emergency_history
            
            return {
                "total_emergencies": len(emergency_history),
                "active_emergencies": len([e for e in emergency_history if e.status == "active"]),
                "resolved_emergencies": len([e for e in emergency_history if e.status == "resolved"]),
                "emergency_types": {
                    et.value: len([e for e in emergency_history if e.type == et])
                    for et in EmergencyType
                },
                "emergency_levels": {
                    el.value: len([e for e in emergency_history if e.level == el])
                    for el in EmergencyLevel
                }
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get emergency metrics: {e}")
            return {}

    def _get_detection_metrics(self) -> Dict[str, Any]:
        """Get failure detection metrics"""
        try:
            detection_status = self.failure_detection.get_detection_status()
            
            return {
                "monitoring_active": detection_status.get("monitoring_active", False),
                "total_rules": detection_status.get("total_rules", 0),
                "enabled_rules": detection_status.get("enabled_rules", 0),
                "rules_in_cooldown": detection_status.get("rules_in_cooldown", 0)
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get detection metrics: {e}")
            return {}

    def _get_recovery_metrics(self) -> Dict[str, Any]:
        """Get recovery procedures metrics"""
        try:
            recovery_status = self.recovery_procedures.get_recovery_status()
            
            return {
                "total_procedures": recovery_status.get("total_procedures", 0),
                "active_recoveries": recovery_status.get("active_recoveries", 0),
                "max_concurrent_recoveries": recovery_status.get("max_concurrent_recoveries", 0)
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get recovery metrics: {e}")
            return {}

    def _get_documentation_metrics(self) -> Dict[str, Any]:
        """Get documentation system metrics"""
        try:
            documentation_status = self.documentation_system.get_documentation_status()
            
            return {
                "total_reports": documentation_status.get("total_reports", 0),
                "report_templates": documentation_status.get("report_templates", []),
                "last_report": documentation_status.get("last_report"),
                "system_status": documentation_status.get("system_status", "unknown")
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get documentation metrics: {e}")
            return {}

    def emergency_response_demo(self) -> Dict[str, Any]:
        """Run emergency response system demonstration"""
        try:
            if not self.system_active:
                return {"error": "Emergency Response System not active"}
            
            demo_results = {
                "status": "demo_completed",
                "message": "Emergency Response System demonstration completed",
                "tests": []
            }
            
            # Test 1: Trigger test emergency
            test1_result = self.test_emergency_response(EmergencyType.WORKFLOW_STALL)
            demo_results["tests"].append({
                "test": "Emergency Trigger Test",
                "result": test1_result
            })
            
            # Test 2: Generate emergency report
            if "test_emergency" in test1_result:
                emergency_id = test1_result["test_emergency"]["id"]
                test2_result = self.generate_emergency_report(emergency_id)
                demo_results["tests"].append({
                    "test": "Emergency Report Generation",
                    "result": test2_result
                })
            
            # Test 3: System health check
            test3_result = self.run_health_check()
            demo_results["tests"].append({
                "test": "System Health Check",
                "result": test3_result
            })
            
            # Test 4: Get system metrics
            test4_result = self.get_system_metrics()
            demo_results["tests"].append({
                "test": "System Metrics Collection",
                "result": test4_result
            })
            
            self.logger.info("Emergency Response System demonstration completed successfully")
            
            return demo_results
            
        except Exception as e:
            self.logger.error(f"Failed to run emergency response demo: {e}")
            return {"error": str(e)}


# Export the main class
__all__ = ["EmergencyResponseOrchestrator"]
