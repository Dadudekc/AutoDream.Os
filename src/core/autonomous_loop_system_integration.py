#!/usr/bin/env python3
"""
Autonomous Loop System Integration - System Integration Module
============================================================

System integration module for autonomous loop with existing swarm infrastructure.
Part of the autonomous loop system integration implementation.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

from __future__ import annotations

import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.autonomous_loop_integration import AutonomousLoopIntegration
from src.core.continuous_autonomy_behavior import ContinuousAutonomyBehavior
from src.core.autonomous_loop_validator import AutonomousLoopValidator

logger = logging.getLogger(__name__)


class AutonomousLoopSystemIntegration:
    """System integration for autonomous loop with existing swarm infrastructure."""
    
    def __init__(self, agent_id: str = "Agent-2") -> None:
        """Initialize autonomous loop system integration."""
        self.agent_id = agent_id
        self.workspace_path = Path(f"agent_workspaces/{agent_id}")
        
        # Initialize core components
        self.autonomous_loop = AutonomousLoopIntegration(agent_id)
        self.continuous_autonomy = ContinuousAutonomyBehavior(agent_id)
        self.validator = AutonomousLoopValidator(agent_id)
        
        # Integration status
        self.integration_status: Dict[str, Any] = {
            "autonomous_loop": False,
            "continuous_autonomy": False,
            "validator": False,
            "messaging_system": False,
            "coordinate_system": False,
            "swarm_coordination": False
        }
        
        # Integration callbacks
        self.messaging_callback: Optional[callable] = None
        self.coordinate_callback: Optional[callable] = None
        self.swarm_callback: Optional[callable] = None
        
        logger.info(f"Autonomous loop system integration initialized for {agent_id}")
    
    def set_messaging_callback(self, callback: callable) -> None:
        """Set messaging system integration callback."""
        self.messaging_callback = callback
        self.integration_status["messaging_system"] = True
        logger.info("Messaging system callback set")
    
    def set_coordinate_callback(self, callback: callable) -> None:
        """Set coordinate system integration callback."""
        self.coordinate_callback = callback
        self.integration_status["coordinate_system"] = True
        logger.info("Coordinate system callback set")
    
    def set_swarm_callback(self, callback: callable) -> None:
        """Set swarm coordination integration callback."""
        self.swarm_callback = callback
        self.integration_status["swarm_coordination"] = True
        logger.info("Swarm coordination callback set")
    
    def integrate_autonomous_loop(self) -> bool:
        """Integrate autonomous loop with existing systems."""
        try:
            # Test autonomous loop functionality
            cycle_results = self.autonomous_loop.autonomous_loop_cycle()
            
            # Verify integration
            if cycle_results and "error" not in cycle_results:
                self.integration_status["autonomous_loop"] = True
                logger.info("Autonomous loop integration successful")
                return True
            else:
                logger.error(f"Autonomous loop integration failed: {cycle_results}")
                return False
                
        except Exception as e:
            logger.error(f"Autonomous loop integration error: {e}")
            return False
    
    def integrate_continuous_autonomy(self) -> bool:
        """Integrate continuous autonomy behavior with existing systems."""
        try:
            # Test continuous autonomy functionality
            status = self.continuous_autonomy.get_status()
            
            # Verify integration
            if status and "is_running" in status:
                self.integration_status["continuous_autonomy"] = True
                logger.info("Continuous autonomy integration successful")
                return True
            else:
                logger.error(f"Continuous autonomy integration failed: {status}")
                return False
                
        except Exception as e:
            logger.error(f"Continuous autonomy integration error: {e}")
            return False
    
    def integrate_validator(self) -> bool:
        """Integrate validator with existing systems."""
        try:
            # Test validator functionality
            validation_results = self.validator.validate_integration()
            
            # Verify integration
            if validation_results and validation_results.get("integration_valid"):
                self.integration_status["validator"] = True
                logger.info("Validator integration successful")
                return True
            else:
                logger.error(f"Validator integration failed: {validation_results}")
                return False
                
        except Exception as e:
            logger.error(f"Validator integration error: {e}")
            return False
    
    def integrate_messaging_system(self) -> bool:
        """Integrate with messaging system."""
        try:
            if self.messaging_callback:
                # Test messaging integration
                result = self.messaging_callback("System integration test message")
                if result:
                    logger.info("Messaging system integration successful")
                    return True
                else:
                    logger.error("Messaging system integration failed")
                    return False
            else:
                logger.warning("No messaging callback set, skipping integration")
                return True
                
        except Exception as e:
            logger.error(f"Messaging system integration error: {e}")
            return False
    
    def integrate_coordinate_system(self) -> bool:
        """Integrate with coordinate system."""
        try:
            if self.coordinate_callback:
                # Test coordinate integration
                result = self.coordinate_callback("System integration test coordinates")
                if result:
                    logger.info("Coordinate system integration successful")
                    return True
                else:
                    logger.error("Coordinate system integration failed")
                    return False
            else:
                logger.warning("No coordinate callback set, skipping integration")
                return True
                
        except Exception as e:
            logger.error(f"Coordinate system integration error: {e}")
            return False
    
    def integrate_swarm_coordination(self) -> bool:
        """Integrate with swarm coordination system."""
        try:
            if self.swarm_callback:
                # Test swarm coordination integration
                result = self.swarm_callback("System integration test swarm coordination")
                if result:
                    logger.info("Swarm coordination integration successful")
                    return True
                else:
                    logger.error("Swarm coordination integration failed")
                    return False
            else:
                logger.warning("No swarm callback set, skipping integration")
                return True
                
        except Exception as e:
            logger.error(f"Swarm coordination integration error: {e}")
            return False
    
    def execute_full_integration(self) -> Dict[str, Any]:
        """Execute full system integration."""
        integration_start = datetime.now()
        results = {
            "overall_success": False,
            "component_results": {},
            "integration_status": {},
            "errors": [],
            "warnings": [],
            "integration_duration": 0
        }
        
        try:
            # Integrate core components
            results["component_results"]["autonomous_loop"] = self.integrate_autonomous_loop()
            results["component_results"]["continuous_autonomy"] = self.integrate_continuous_autonomy()
            results["component_results"]["validator"] = self.integrate_validator()
            
            # Integrate external systems
            results["component_results"]["messaging_system"] = self.integrate_messaging_system()
            results["component_results"]["coordinate_system"] = self.integrate_coordinate_system()
            results["component_results"]["swarm_coordination"] = self.integrate_swarm_coordination()
            
            # Update integration status
            results["integration_status"] = self.integration_status.copy()
            
            # Calculate overall success
            core_components_success = all([
                results["component_results"]["autonomous_loop"],
                results["component_results"]["continuous_autonomy"],
                results["component_results"]["validator"]
            ])
            
            external_systems_success = all([
                results["component_results"]["messaging_system"],
                results["component_results"]["coordinate_system"],
                results["component_results"]["swarm_coordination"]
            ])
            
            results["overall_success"] = core_components_success and external_systems_success
            
            # Calculate duration
            integration_end = datetime.now()
            results["integration_duration"] = (integration_end - integration_start).total_seconds()
            
            logger.info(f"Full system integration completed: {results['overall_success']}")
            return results
            
        except Exception as e:
            logger.error(f"Full system integration failed: {e}")
            results["errors"].append(str(e))
            return results
    
    def get_integration_status(self) -> Dict[str, Any]:
        """Get current integration status."""
        return {
            "agent_id": self.agent_id,
            "integration_status": self.integration_status.copy(),
            "component_status": {
                "autonomous_loop_operational": self.integration_status["autonomous_loop"],
                "continuous_autonomy_operational": self.integration_status["continuous_autonomy"],
                "validator_operational": self.integration_status["validator"],
                "messaging_system_connected": self.integration_status["messaging_system"],
                "coordinate_system_connected": self.integration_status["coordinate_system"],
                "swarm_coordination_connected": self.integration_status["swarm_coordination"]
            },
            "overall_operational": all(self.integration_status.values())
        }
    
    def start_autonomous_operation(self) -> bool:
        """Start autonomous operation with full system integration."""
        try:
            # Execute full integration first
            integration_results = self.execute_full_integration()
            
            if not integration_results["overall_success"]:
                logger.error("System integration failed, cannot start autonomous operation")
                return False
            
            # Start continuous autonomy
            start_success = self.continuous_autonomy.start()
            
            if start_success:
                logger.info("Autonomous operation started successfully")
                return True
            else:
                logger.error("Failed to start autonomous operation")
                return False
                
        except Exception as e:
            logger.error(f"Failed to start autonomous operation: {e}")
            return False
    
    def stop_autonomous_operation(self) -> bool:
        """Stop autonomous operation."""
        try:
            stop_success = self.continuous_autonomy.stop()
            
            if stop_success:
                logger.info("Autonomous operation stopped successfully")
                return True
            else:
                logger.error("Failed to stop autonomous operation")
                return False
                
        except Exception as e:
            logger.error(f"Failed to stop autonomous operation: {e}")
            return False
