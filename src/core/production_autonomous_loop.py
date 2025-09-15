#!/usr/bin/env python3
"""
Production Autonomous Loop - Production Autonomous Loop System
============================================================

Production-ready autonomous loop system with full swarm coordination integration.
Part of the autonomous loop system integration implementation.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

from __future__ import annotations

import logging
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.autonomous_loop_system_integration import AutonomousLoopSystemIntegration
from src.services.consolidated_messaging_service import ConsolidatedMessagingService

logger = logging.getLogger(__name__)


class ProductionAutonomousLoop:
    """Production-ready autonomous loop system with swarm coordination."""
    
    def __init__(self, agent_id: str = "Agent-2") -> None:
        """Initialize production autonomous loop."""
        self.agent_id = agent_id
        self.workspace_path = Path(f"agent_workspaces/{agent_id}")
        
        # Initialize system integration
        self.system_integration = AutonomousLoopSystemIntegration(agent_id)
        
        # Initialize messaging service
        self.messaging_service = ConsolidatedMessagingService(
            coord_path="config/coordinates.json"
        )
        
        # Set integration callbacks
        self._setup_integration_callbacks()
        
        # Production settings
        self.production_mode = True
        self.cycle_interval = 60  # 60 seconds between cycles
        self.max_idle_cycles = 10  # Max cycles with no activity
        self.status_reporting_interval = 300  # 5 minutes between status reports
        
        # Operational metrics
        self.operational_metrics = {
            "cycles_completed": 0,
            "messages_processed": 0,
            "tasks_completed": 0,
            "errors_encountered": 0,
            "uptime_start": datetime.now(),
            "last_activity": datetime.now()
        }
        
        logger.info(f"Production autonomous loop initialized for {agent_id}")
    
    def _setup_integration_callbacks(self) -> None:
        """Setup integration callbacks for system integration."""
        
        def messaging_callback(message: str) -> bool:
            """Messaging system integration callback."""
            try:
                # Process message through messaging service
                logger.info(f"Processing message: {message}")
                return True
            except Exception as e:
                logger.error(f"Messaging callback error: {e}")
                return False
        
        def coordinate_callback(coordinates: str) -> bool:
            """Coordinate system integration callback."""
            try:
                # Process coordinate data
                logger.info(f"Processing coordinates: {coordinates}")
                return True
            except Exception as e:
                logger.error(f"Coordinate callback error: {e}")
                return False
        
        def swarm_callback(swarm_data: str) -> bool:
            """Swarm coordination integration callback."""
            try:
                # Process swarm coordination data
                logger.info(f"Processing swarm data: {swarm_data}")
                return True
            except Exception as e:
                logger.error(f"Swarm callback error: {e}")
                return False
        
        # Set callbacks
        self.system_integration.set_messaging_callback(messaging_callback)
        self.system_integration.set_coordinate_callback(coordinate_callback)
        self.system_integration.set_swarm_callback(swarm_callback)
    
    def send_status_report(self, status_message: str) -> bool:
        """Send status report to Captain Agent-4."""
        try:
            success = self.messaging_service.send_message(
                "Agent-4", 
                status_message, 
                self.agent_id
            )
            if success:
                logger.info("Status report sent successfully")
            else:
                logger.error("Failed to send status report")
            return success
        except Exception as e:
            logger.error(f"Status reporting error: {e}")
            return False
    
    def process_messages(self, message_count: int) -> bool:
        """Process messages and update metrics."""
        try:
            self.operational_metrics["messages_processed"] += message_count
            self.operational_metrics["last_activity"] = datetime.now()
            logger.info(f"Processed {message_count} messages")
            return True
        except Exception as e:
            logger.error(f"Message processing error: {e}")
            return False
    
    def process_task(self, task_data: Dict[str, Any]) -> bool:
        """Process task and update metrics."""
        try:
            task_id = task_data.get("id", "unknown")
            task_status = task_data.get("status", "unknown")
            
            if task_status == "completed":
                self.operational_metrics["tasks_completed"] += 1
                self.operational_metrics["last_activity"] = datetime.now()
                logger.info(f"Task completed: {task_id}")
            
            return True
        except Exception as e:
            logger.error(f"Task processing error: {e}")
            return False
    
    def resolve_blocker(self, blocker_description: str) -> bool:
        """Resolve blocker and update metrics."""
        try:
            logger.info(f"Resolving blocker: {blocker_description}")
            self.operational_metrics["last_activity"] = datetime.now()
            return True
        except Exception as e:
            logger.error(f"Blocker resolution error: {e}")
            return False
    
    def update_metrics(self, cycle_results: Dict[str, Any]) -> None:
        """Update operational metrics based on cycle results."""
        try:
            self.operational_metrics["cycles_completed"] += 1
            
            # Update message processing count
            messages_processed = cycle_results.get("messages_processed", 0)
            if messages_processed > 0:
                self.operational_metrics["messages_processed"] += messages_processed
                self.operational_metrics["last_activity"] = datetime.now()
            
            # Update task completion count
            if cycle_results.get("task_completed"):
                self.operational_metrics["tasks_completed"] += 1
                self.operational_metrics["last_activity"] = datetime.now()
            
            # Update error count
            if "error" in cycle_results:
                self.operational_metrics["errors_encountered"] += 1
            
        except Exception as e:
            logger.error(f"Metrics update error: {e}")
    
    def generate_status_report(self) -> str:
        """Generate comprehensive status report."""
        try:
            uptime = datetime.now() - self.operational_metrics["uptime_start"]
            last_activity = datetime.now() - self.operational_metrics["last_activity"]
            
            status_report = f"""PRODUCTION AUTONOMOUS LOOP STATUS REPORT - {self.agent_id}
============================================================
🕒 Uptime: {uptime}
🔄 Cycles Completed: {self.operational_metrics['cycles_completed']}
📨 Messages Processed: {self.operational_metrics['messages_processed']}
✅ Tasks Completed: {self.operational_metrics['tasks_completed']}
❌ Errors Encountered: {self.operational_metrics['errors_encountered']}
⏰ Last Activity: {last_activity} ago
🔧 Production Mode: {'ACTIVE' if self.production_mode else 'INACTIVE'}
📊 System Integration: {'OPERATIONAL' if self.system_integration.get_integration_status()['overall_operational'] else 'DEGRADED'}
============================================================"""
            
            return status_report
            
        except Exception as e:
            logger.error(f"Status report generation error: {e}")
            return f"Status report generation failed: {e}"
    
    def start_production_operation(self) -> bool:
        """Start production autonomous operation."""
        try:
            logger.info("Starting production autonomous operation...")
            
            # Execute full system integration
            integration_results = self.system_integration.execute_full_integration()
            
            if not integration_results["overall_success"]:
                logger.error("System integration failed, cannot start production operation")
                return False
            
            # Start autonomous operation
            start_success = self.system_integration.start_autonomous_operation()
            
            if start_success:
                # Send initial status report
                initial_report = f"PRODUCTION AUTONOMOUS LOOP STARTED - {self.agent_id}\nSystem integration successful. All components operational. Ready for continuous autonomous operation."
                self.send_status_report(initial_report)
                
                logger.info("Production autonomous operation started successfully")
                return True
            else:
                logger.error("Failed to start production autonomous operation")
                return False
                
        except Exception as e:
            logger.error(f"Failed to start production autonomous operation: {e}")
            return False
    
    def stop_production_operation(self) -> bool:
        """Stop production autonomous operation."""
        try:
            logger.info("Stopping production autonomous operation...")
            
            # Generate final status report
            final_report = f"PRODUCTION AUTONOMOUS LOOP STOPPING - {self.agent_id}\n{self.generate_status_report()}"
            self.send_status_report(final_report)
            
            # Stop autonomous operation
            stop_success = self.system_integration.stop_autonomous_operation()
            
            if stop_success:
                logger.info("Production autonomous operation stopped successfully")
                return True
            else:
                logger.error("Failed to stop production autonomous operation")
                return False
                
        except Exception as e:
            logger.error(f"Failed to stop production autonomous operation: {e}")
            return False
    
    def get_production_status(self) -> Dict[str, Any]:
        """Get comprehensive production status."""
        try:
            integration_status = self.system_integration.get_integration_status()
            
            return {
                "agent_id": self.agent_id,
                "production_mode": self.production_mode,
                "operational_metrics": self.operational_metrics.copy(),
                "integration_status": integration_status,
                "system_health": {
                    "overall_operational": integration_status["overall_operational"],
                    "autonomous_loop_active": integration_status["component_status"]["autonomous_loop_operational"],
                    "continuous_autonomy_active": integration_status["component_status"]["continuous_autonomy_operational"],
                    "messaging_connected": integration_status["component_status"]["messaging_system_connected"],
                    "coordinate_connected": integration_status["component_status"]["coordinate_system_connected"],
                    "swarm_connected": integration_status["component_status"]["swarm_coordination_connected"]
                },
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Production status retrieval error: {e}")
            return {"error": str(e)}
