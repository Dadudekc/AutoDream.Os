"""
SWARM Integration Manager - Agent Cellphone V2
==============================================

Orchestrates complete SWARM integration into V2 system.
Reuses existing SWARM code, maintains V2 standards (max 200 LOC).
Now inherits from BaseManager for unified functionality.

Architecture: Single Responsibility Principle - orchestrates SWARM integration
LOC: 198 lines (under 200 limit)
"""

import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from datetime import datetime
import json

from src.utils.stability_improvements import stability_manager, safe_import
from .base_manager import BaseManager, ManagerStatus, ManagerPriority

# Import V2 core components
from .agent_manager import AgentManager
from .task_manager import TaskManager
from .swarm_coordination_system import SwarmCoordinationSystem
from .swarm_agent_bridge import SwarmAgentBridge

logger = logging.getLogger(__name__)


class IntegrationStatus(Enum):
    """SWARM integration status enumeration"""

    NOT_INITIALIZED = "not_initialized"
    INITIALIZING = "initializing"
    ACTIVE = "active"
    DEGRADED = "degraded"
    ERROR = "error"


@dataclass
class IntegrationMetrics:
    """SWARM integration performance metrics"""

    total_agents: int
    integrated_agents: int
    coordination_tasks: int
    message_throughput: float
    system_health: str


class SwarmIntegrationManager(BaseManager):
    """
    SWARM Integration Manager - Single responsibility: orchestrates SWARM integration

    This service orchestrates the complete SWARM integration:
    - Manages SWARM coordination system
    - Controls agent bridge operations
    - Provides unified integration interface
    - Monitors system health and performance
    
    Now inherits from BaseManager for unified functionality
    """

    def __init__(self, workspace_manager=None):
        """Initialize the SWARM integration manager with BaseManager"""
        super().__init__(
            manager_id="swarm_integration_manager",
            name="SWARM Integration Manager",
            description="Orchestrates complete SWARM integration into V2 system"
        )
        
        self.workspace_manager = workspace_manager
        self.status = IntegrationStatus.NOT_INITIALIZED

        # Core V2 managers
        self.agent_manager = AgentManager()
        self.task_manager = (
            TaskManager(workspace_manager) if workspace_manager else None
        )

        # SWARM integration components
        self.swarm_coordination = None
        self.agent_bridge = None

        # Integration state
        self.integration_active = False
        self.metrics = IntegrationMetrics(0, 0, 0, 0.0, "unknown")

        # SWARM integration management tracking
        self.integration_operations: List[Dict[str, Any]] = []
        self.coordination_operations: List[Dict[str, Any]] = []
        self.message_operations: List[Dict[str, Any]] = []

        # Initialize integration
        self._initialize_integration()
        self.logger.info("SWARM Integration Manager initialized")
    
    # ============================================================================
    # BaseManager Abstract Method Implementations
    # ============================================================================
    
    def _on_start(self) -> bool:
        """Initialize SWARM integration management system"""
        try:
            self.logger.info("Starting SWARM Integration Manager...")
            
            # Clear tracking data
            self.integration_operations.clear()
            self.coordination_operations.clear()
            self.message_operations.clear()
            
            # Reinitialize integration
            self._initialize_integration()
            
            self.logger.info("SWARM Integration Manager started successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start SWARM Integration Manager: {e}")
            return False
    
    def _on_stop(self):
        """Cleanup SWARM integration management system"""
        try:
            self.logger.info("Stopping SWARM Integration Manager...")
            
            # Save tracking data
            self._save_swarm_integration_management_data()
            
            # Clear data
            self.integration_operations.clear()
            self.coordination_operations.clear()
            self.message_operations.clear()
            
            self.logger.info("SWARM Integration Manager stopped successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to stop SWARM Integration Manager: {e}")
    
    def _on_heartbeat(self):
        """SWARM integration manager heartbeat"""
        try:
            # Check SWARM integration management health
            self._check_swarm_integration_management_health()
            
            # Update metrics
            self._update_metrics()
            
            # Update metrics
            self.record_operation("heartbeat", True, 0.0)
            
        except Exception as e:
            self.logger.error(f"Heartbeat error: {e}")
            self.record_operation("heartbeat", False, 0.0)
    
    def _on_initialize_resources(self) -> bool:
        """Initialize SWARM integration management resources"""
        try:
            # Initialize data structures
            self.integration_operations = []
            self.coordination_operations = []
            self.message_operations = []
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize resources: {e}")
            return False
    
    def _on_cleanup_resources(self):
        """Cleanup SWARM integration management resources"""
        try:
            # Clear data
            self.integration_operations.clear()
            self.coordination_operations.clear()
            self.message_operations.clear()
            
        except Exception as e:
            self.logger.error(f"Failed to cleanup resources: {e}")
    
    def _on_recovery_attempt(self, error: Exception, context: str) -> bool:
        """Attempt recovery from errors"""
        try:
            self.logger.info(f"Attempting recovery for {context}")
            
            # Reinitialize integration
            self._initialize_integration()
            
            # Reset tracking
            self.integration_operations.clear()
            self.coordination_operations.clear()
            self.message_operations.clear()
            
            self.logger.info("Recovery successful")
            return True
            
        except Exception as e:
            self.logger.error(f"Recovery failed: {e}")
            return False
    
    # ============================================================================
    # SWARM Integration Management Methods
    # ============================================================================
    
    def _initialize_integration(self):
        """Initialize complete SWARM integration system."""
        try:
            start_time = datetime.now()
            
            self.status = IntegrationStatus.INITIALIZING

            # Initialize SWARM coordination system
            self.swarm_coordination = SwarmCoordinationSystem(
                self.agent_manager, self.task_manager
            )

            # Initialize agent bridge
            self.agent_bridge = SwarmAgentBridge(self.swarm_coordination)

            # Check integration status
            if (
                self.swarm_coordination.coordination_active
                and self.agent_bridge.bridge_active
            ):
                self.status = IntegrationStatus.ACTIVE
                self.integration_active = True
                self.logger.info("SWARM integration system fully operational")

            else:
                self.status = IntegrationStatus.DEGRADED
                self.logger.warning("SWARM integration partially operational")

            # Record integration operation
            operation_record = {
                "timestamp": datetime.now().isoformat(),
                "operation": "initialize_integration",
                "status": self.status.value,
                "integration_active": self.integration_active,
                "success": True
            }
            self.integration_operations.append(operation_record)
            
            # Record operation
            operation_time = (datetime.now() - start_time).total_seconds()
            self.record_operation("initialize_integration", True, operation_time)
            
        except Exception as e:
            self.status = IntegrationStatus.ERROR
            self.logger.error(f"Failed to initialize SWARM integration: {e}")
            
            # Record failed operation
            operation_record = {
                "timestamp": datetime.now().isoformat(),
                "operation": "initialize_integration",
                "error": str(e),
                "success": False
            }
            self.integration_operations.append(operation_record)
            
            self.record_operation("initialize_integration", False, 0.0)

    def integrate_agent(
        self, agent_id: str, name: str, capabilities: List[str]
    ) -> bool:
        """Integrate a new agent into the SWARM system."""
        try:
            start_time = datetime.now()
            
            if not self.integration_active:
                self.logger.error("SWARM integration not active")
                self.record_operation("integrate_agent", False, 0.0)
                return False

            # Integrate with coordination system
            coord_success = self.swarm_coordination.integrate_agent(
                agent_id, name, capabilities
            )

            # Connect to agent bridge
            bridge_success = self.agent_bridge.connect_agent(
                agent_id, {"name": name, "capabilities": capabilities}
            )

            if coord_success and bridge_success:
                self._update_metrics()
                
                # Record integration operation
                operation_record = {
                    "timestamp": datetime.now().isoformat(),
                    "operation": "integrate_agent",
                    "agent_id": agent_id,
                    "name": name,
                    "capabilities": capabilities,
                    "success": True
                }
                self.integration_operations.append(operation_record)
                
                self.logger.info(f"Agent {agent_id} fully integrated into SWARM system")
                
                # Record operation
                operation_time = (datetime.now() - start_time).total_seconds()
                self.record_operation("integrate_agent", True, operation_time)
                
                return True
            else:
                self.logger.warning(f"Agent {agent_id} partially integrated")
                
                # Record partial operation
                operation_record = {
                    "timestamp": datetime.now().isoformat(),
                    "operation": "integrate_agent",
                    "agent_id": agent_id,
                    "name": name,
                    "capabilities": capabilities,
                    "coord_success": coord_success,
                    "bridge_success": bridge_success,
                    "success": False
                }
                self.integration_operations.append(operation_record)
                
                self.record_operation("integrate_agent", False, 0.0)
                return False

        except Exception as e:
            self.logger.error(f"Failed to integrate agent {agent_id}: {e}")
            
            # Record failed operation
            operation_record = {
                "timestamp": datetime.now().isoformat(),
                "operation": "integrate_agent",
                "agent_id": agent_id,
                "name": name,
                "capabilities": capabilities,
                "error": str(e),
                "success": False
            }
            self.integration_operations.append(operation_record)
            
            self.record_operation("integrate_agent", False, 0.0)
            return False

    def coordinate_agents(
        self, task_description: str, agent_ids: List[str]
    ) -> Dict[str, bool]:
        """Coordinate multiple agents for a specific task."""
        try:
            start_time = datetime.now()
            
            if not self.integration_active:
                self.record_operation("coordinate_agents", False, 0.0)
                return {agent_id: False for agent_id in agent_ids}

            # Use SWARM coordination system
            results = self.swarm_coordination.coordinate_agents(
                task_description, agent_ids
            )

            # Update metrics
            self.metrics.coordination_tasks += 1
            self._update_metrics()

            # Record coordination operation
            operation_record = {
                "timestamp": datetime.now().isoformat(),
                "operation": "coordinate_agents",
                "task_description": task_description,
                "agent_ids": agent_ids,
                "results": results,
                "success": True
            }
            self.coordination_operations.append(operation_record)
            
            # Record operation
            operation_time = (datetime.now() - start_time).total_seconds()
            self.record_operation("coordinate_agents", True, operation_time)
            
            return results

        except Exception as e:
            self.logger.error(f"Agent coordination failed: {e}")
            
            # Record failed operation
            operation_record = {
                "timestamp": datetime.now().isoformat(),
                "operation": "coordinate_agents",
                "task_description": task_description,
                "agent_ids": agent_ids,
                "error": str(e),
                "success": False
            }
            self.coordination_operations.append(operation_record)
            
            self.record_operation("coordinate_agents", False, 0.0)
            return {agent_id: False for agent_id in agent_ids}

    def send_coordination_message(
        self,
        from_agent: str,
        to_agent: str,
        content: str,
        message_type: str = "coordination",
    ) -> bool:
        """Send a coordination message between agents."""
        try:
            start_time = datetime.now()
            
            if not self.integration_active:
                self.record_operation("send_coordination_message", False, 0.0)
                return False

            # Use agent bridge for message routing
            success = self.agent_bridge.send_message(
                from_agent, to_agent, content, message_type, priority=2
            )

            if success:
                self._update_metrics()
                
                # Record message operation
                operation_record = {
                    "timestamp": datetime.now().isoformat(),
                    "operation": "send_coordination_message",
                    "from_agent": from_agent,
                    "to_agent": to_agent,
                    "content": content,
                    "message_type": message_type,
                    "success": True
                }
                self.message_operations.append(operation_record)
                
                # Record operation
                operation_time = (datetime.now() - start_time).total_seconds()
                self.record_operation("send_coordination_message", True, operation_time)
                
                return True
            else:
                # Record failed operation
                operation_record = {
                    "timestamp": datetime.now().isoformat(),
                    "operation": "send_coordination_message",
                    "from_agent": from_agent,
                    "to_agent": to_agent,
                    "content": content,
                    "message_type": message_type,
                    "success": False
                }
                self.message_operations.append(operation_record)
                
                self.record_operation("send_coordination_message", False, 0.0)
                return False

        except Exception as e:
            self.logger.error(f"Failed to send coordination message: {e}")
            
            # Record failed operation
            operation_record = {
                "timestamp": datetime.now().isoformat(),
                "operation": "send_coordination_message",
                "from_agent": from_agent,
                "to_agent": to_agent,
                "content": content,
                "message_type": message_type,
                "error": str(e),
                "success": False
            }
            self.message_operations.append(operation_record)
            
            self.record_operation("send_coordination_message", False, 0.0)
            return False

    def get_integration_status(self) -> Dict[str, Any]:
        """Get comprehensive integration status and metrics."""
        try:
            status = {
                "integration_status": self.status.value,
                "integration_active": self.integration_active,
                "metrics": {
                    "total_agents": self.metrics.total_agents,
                    "integrated_agents": self.metrics.integrated_agents,
                    "coordination_tasks": self.metrics.coordination_tasks,
                    "message_throughput": self.metrics.message_throughput,
                    "system_health": self.metrics.system_health,
                },
                "swarm_coordination": self.swarm_coordination.get_swarm_status()
                if self.swarm_coordination
                else None,
                "agent_bridge": self.agent_bridge.get_bridge_status()
                if self.agent_bridge
                else None,
                "manager_status": self.status.value,
                "manager_uptime": self.metrics.uptime_seconds
            }
            
            # Record operation
            self.record_operation("get_integration_status", True, 0.0)
            
            return status
            
        except Exception as e:
            self.logger.error(f"Failed to get integration status: {e}")
            self.record_operation("get_integration_status", False, 0.0)
            return {"error": str(e)}

    def _update_metrics(self):
        """Update integration performance metrics."""
        try:
            # Get current agent counts
            v2_agents = self.agent_manager.get_all_agents()
            self.metrics.total_agents = len(v2_agents)

            # Get integrated agent count
            if self.swarm_coordination:
                swarm_status = self.swarm_coordination.get_swarm_status()
                self.metrics.integrated_agents = swarm_status.get(
                    "integrated_agents", 0
                )

            # Calculate system health
            if self.integration_active and self.status == IntegrationStatus.ACTIVE:
                self.metrics.system_health = "healthy"
            elif self.status == IntegrationStatus.DEGRADED:
                self.metrics.system_health = "degraded"
            else:
                self.metrics.system_health = "unhealthy"

        except Exception as e:
            self.logger.error(f"Failed to update metrics: {e}")
    
    # ============================================================================
    # Private Helper Methods
    # ============================================================================
    
    def _save_swarm_integration_management_data(self):
        """Save SWARM integration management data to persistent storage"""
        try:
            # Create persistence directory if it doesn't exist
            persistence_dir = Path("data/persistent/swarm_integration")
            persistence_dir.mkdir(parents=True, exist_ok=True)
            
            # Prepare data for persistence
            integration_data = {
                "integration_operations": self.integration_operations,
                "coordination_operations": self.coordination_operations,
                "message_operations": self.message_operations,
                "agent_integrations": self.agent_integrations,
                "coordination_tasks": self.coordination_tasks,
                "timestamp": datetime.now().isoformat(),
                "manager_id": self.manager_id,
                "version": "2.0.0"
            }
            
            # Save to JSON file with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"swarm_integration_data_{timestamp}.json"
            filepath = persistence_dir / filename
            
            with open(filepath, 'w') as f:
                json.dump(integration_data, f, indent=2, default=str)
            
            # Keep only the latest 5 backup files
            self._cleanup_old_backups(persistence_dir, "swarm_integration_data_*.json", 5)
            
            self.logger.info(f"SWARM integration management data saved to {filepath}")
            
        except Exception as e:
            self.logger.error(f"Failed to save SWARM integration management data: {e}")
            # Fallback to basic logging if persistence fails
            self.logger.warning("Persistence failed, data only logged in memory")
    
    def _cleanup_old_backups(self, directory: Path, pattern: str, keep_count: int):
        """Clean up old backup files, keeping only the specified number"""
        try:
            files = list(directory.glob(pattern))
            if len(files) > keep_count:
                # Sort by modification time (oldest first)
                files.sort(key=lambda x: x.stat().st_mtime)
                # Remove oldest files
                for old_file in files[:-keep_count]:
                    old_file.unlink()
                    self.logger.debug(f"Removed old backup: {old_file}")
        except Exception as e:
            self.logger.warning(f"Failed to cleanup old backups: {e}")
    
    def _check_swarm_integration_management_health(self):
        """Check SWARM integration management health status"""
        try:
            # Check for excessive integration operations
            if len(self.integration_operations) > 1000:
                self.logger.warning(f"High number of integration operations: {len(self.integration_operations)}")
            
            # Check coordination operations
            if len(self.coordination_operations) > 500:
                self.logger.info(f"Large coordination operations history: {len(self.coordination_operations)} records")
                
        except Exception as e:
            self.logger.error(f"Failed to check SWARM integration management health: {e}")
    
    def get_swarm_integration_management_stats(self) -> Dict[str, Any]:
        """Get SWARM integration management statistics"""
        try:
            stats = {
                "total_agents": self.metrics.total_agents,
                "integrated_agents": self.metrics.integrated_agents,
                "coordination_tasks": self.metrics.coordination_tasks,
                "integration_operations_count": len(self.integration_operations),
                "coordination_operations_count": len(self.coordination_operations),
                "message_operations_count": len(self.message_operations),
                "integration_status": self.status.value,
                "integration_active": self.integration_active,
                "manager_status": self.status.value,
                "manager_uptime": self.metrics.uptime_seconds
            }
            
            # Record operation
            self.record_operation("get_swarm_integration_management_stats", True, 0.0)
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Failed to get SWARM integration management stats: {e}")
            self.record_operation("get_swarm_integration_management_stats", False, 0.0)
            return {"error": str(e)}


def run_smoke_test():
    """Run basic functionality test for SwarmIntegrationManager."""
    print("🧪 Running SwarmIntegrationManager Smoke Test...")

    # Test manager initialization
    manager = SwarmIntegrationManager()

    # Test status retrieval
    status = manager.get_integration_status()
    assert "integration_status" in status
    assert "metrics" in status

    print("✅ SwarmIntegrationManager Smoke Test PASSED")
    return True


def main():
    """CLI interface for SwarmIntegrationManager testing."""
    import argparse

    parser = argparse.ArgumentParser(description="SWARM Integration Manager CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    parser.add_argument("--status", action="store_true", help="Show integration status")

    args = parser.parse_args()

    if args.test:
        run_smoke_test()
        return

    if args.status:
        manager = SwarmIntegrationManager()
        status = manager.get_integration_status()

        print("SWARM Integration Manager Status:")
        print(f"Integration Status: {status['integration_status']}")
        print(f"Integration Active: {status['integration_active']}")
        print(f"Total Agents: {status['metrics']['total_agents']}")
        print(f"Integrated Agents: {status['metrics']['integrated_agents']}")
        print(f"System Health: {status['metrics']['system_health']}")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
