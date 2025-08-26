#!/usr/bin/env python3
"""
Unified Workspace System - Agent Cellphone V2

Main entry point for unified workspace system consolidation.
Integrates all workspace management, consolidation, optimization, and health monitoring.

Author: Agent-3 Integration & Testing Specialist
Task: TASK 3A - Workspace System Consolidation
V2 Standards: ≤400 LOC, SRP, OOP principles
"""

import logging
import time
import threading
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime

# Core infrastructure imports
from src.core.managers.performance_manager import PerformanceManager

# Workspace system components
from .workspace_manager import UnifiedWorkspaceManager
from .workspace_orchestrator import WorkspaceCoordinationOrchestrator
from .workspace_consolidation_orchestrator import WorkspaceConsolidationOrchestrator
from .workspace_resource_optimizer import WorkspaceResourceOptimizer
from .workspace_health_monitor import WorkspaceHealthMonitor


@dataclass
class UnifiedWorkspaceSystemConfig:
    """Configuration for unified workspace system"""
    enable_consolidation: bool = True
    enable_resource_optimization: bool = True
    enable_health_monitoring: bool = True
    enable_coordination: bool = True
    consolidation_interval: int = 300  # 5 minutes
    optimization_interval: int = 180   # 3 minutes
    health_check_interval: int = 120  # 2 minutes
    coordination_interval: int = 60   # 1 minute


@dataclass
class SystemStatus:
    """Overall system status"""
    system_active: bool
    consolidation_active: bool
    optimization_active: bool
    health_monitoring_active: bool
    coordination_active: bool
    total_workspaces: int
    consolidated_workspaces: int
    overall_health_score: float
    last_status_update: str


class UnifiedWorkspaceSystem:
    """
    Unified Workspace System - TASK 3A

    Main entry point for workspace system consolidation.
    Integrates and coordinates all workspace management components.
    """

    def __init__(self, performance_manager: PerformanceManager, config: Optional[UnifiedWorkspaceSystemConfig] = None):
        self.performance_manager = performance_manager
        self.config = config or UnifiedWorkspaceSystemConfig()
        self.logger = logging.getLogger(f"{__name__}.UnifiedWorkspaceSystem")

        # Core components
        self.workspace_manager = UnifiedWorkspaceManager(performance_manager)
        self.coordination_orchestrator = WorkspaceCoordinationOrchestrator(
            self.workspace_manager, performance_manager
        )
        self.consolidation_orchestrator = WorkspaceConsolidationOrchestrator(performance_manager)
        self.resource_optimizer = WorkspaceResourceOptimizer(performance_manager)
        self.health_monitor = WorkspaceHealthMonitor(performance_manager)

        # System state
        self.system_active = False
        self.system_thread = None
        self.system_lock = threading.Lock()

        # Status tracking
        self.last_status_update = datetime.now()
        self.system_start_time = None

        self.logger.info("Unified Workspace System initialized for TASK 3A")

    def start_system(self) -> bool:
        """Start the unified workspace system"""
        try:
            with self.system_lock:
                if self.system_active:
                    self.logger.warning("Unified workspace system already active")
                    return False

                self.system_active = True
                self.system_start_time = datetime.now()
                self.last_status_update = datetime.now()

                # Start core components
                self._start_core_components()

                # Start system management thread
                self.system_thread = threading.Thread(
                    target=self._system_management_worker,
                    daemon=True
                )
                self.system_thread.start()

                # Setup system monitoring
                self._setup_system_monitoring()

                self.logger.info("Unified workspace system started successfully")
                return True

        except Exception as e:
            self.logger.error(f"Failed to start unified workspace system: {e}")
            self.system_active = False
            return False

    def stop_system(self) -> bool:
        """Stop the unified workspace system"""
        try:
            with self.system_lock:
                if not self.system_active:
                    self.logger.warning("Unified workspace system not active")
                    return False

                self.system_active = False

                # Stop core components
                self._stop_core_components()

                # Wait for system thread
                if self.system_thread and self.system_thread.is_alive():
                    self.system_thread.join(timeout=10.0)

                self.logger.info("Unified workspace system stopped")
                return True

        except Exception as e:
            self.logger.error(f"Failed to stop unified workspace system: {e}")
            return False

    def _start_core_components(self):
        """Start all core workspace system components"""
        try:
            # Start workspace management
            self.workspace_manager.start_workspace_management()

            # Start coordination if enabled
            if self.config.enable_coordination:
                self.coordination_orchestrator.start_coordination()

            # Start consolidation if enabled
            if self.config.enable_consolidation:
                self.consolidation_orchestrator.start_consolidation()

            # Start resource optimization if enabled
            if self.config.enable_resource_optimization:
                self.resource_optimizer.start_optimization()

            # Start health monitoring if enabled
            if self.config.enable_health_monitoring:
                self.health_monitor.start_health_monitoring()

            self.logger.info("All core components started successfully")

        except Exception as e:
            self.logger.error(f"Failed to start core components: {e}")
            raise

    def _stop_core_components(self):
        """Stop all core workspace system components"""
        try:
            # Stop all components
            self.workspace_manager.stop_workspace_management()
            self.coordination_orchestrator.stop_coordination()
            self.consolidation_orchestrator.stop_consolidation()
            self.resource_optimizer.stop_optimization()
            self.health_monitor.stop_health_monitoring()

            self.logger.info("All core components stopped successfully")

        except Exception as e:
            self.logger.error(f"Failed to stop core components: {e}")

    def _setup_system_monitoring(self):
        """Setup system monitoring with performance manager"""
        try:
            # Add system-level metrics
            self.performance_manager.add_metric("unified_workspace_system_active", 1, "boolean", "system")
            self.performance_manager.add_metric("workspace_system_components", 5, "count", "system")
            self.performance_manager.add_metric("workspace_system_uptime", 0, "seconds", "system")

            self.logger.info("System monitoring setup completed")

        except Exception as e:
            self.logger.error(f"Failed to setup system monitoring: {e}")

    def _system_management_worker(self):
        """Main system management worker thread"""
        try:
            self.logger.info("System management worker started")

            while self.system_active:
                try:
                    # Update system status
                    self._update_system_status()

                    # Perform system maintenance
                    self._perform_system_maintenance()

                    # Sleep between cycles
                    time.sleep(30)  # 30 second cycles

                except Exception as e:
                    self.logger.error(f"Error in system management worker: {e}")
                    time.sleep(60)  # Longer sleep on error

            self.logger.info("System management worker stopped")

        except Exception as e:
            self.logger.error(f"Fatal error in system management worker: {e}")

    def _update_system_status(self):
        """Update overall system status"""
        try:
            self.last_status_update = datetime.now()

            # Update uptime metric
            if self.system_start_time:
                uptime = (datetime.now() - self.system_start_time).total_seconds()
                self.performance_manager.add_metric("workspace_system_uptime", uptime, "seconds", "system")

        except Exception as e:
            self.logger.error(f"Failed to update system status: {e}")

    def _perform_system_maintenance(self):
        """Perform system maintenance tasks"""
        try:
            # Check component health
            self._check_component_health()

            # Update workspace registrations
            self._update_workspace_registrations()

            # Perform cleanup if needed
            self._perform_system_cleanup()

        except Exception as e:
            self.logger.error(f"Failed to perform system maintenance: {e}")

    def _check_component_health(self):
        """Check health of all system components"""
        try:
            # Check workspace manager
            workspace_status = self.workspace_manager.get_workspace_status()
            if workspace_status.get("error"):
                self.logger.warning(f"Workspace manager health issue: {workspace_status.get('error')}")

            # Check consolidation orchestrator
            consolidation_status = self.consolidation_orchestrator.get_consolidation_status()
            if consolidation_status.consolidation_active:
                self.logger.debug(f"Consolidation progress: {consolidation_status.overall_progress:.1f}%")

            # Check resource optimizer
            optimization_status = self.resource_optimizer.get_optimization_status()
            if optimization_status.get("error"):
                self.logger.warning(f"Resource optimizer health issue: {optimization_status.get('error')}")

            # Check health monitor
            health_status = self.health_monitor.get_overall_health_status()
            if health_status.get("error"):
                self.logger.warning(f"Health monitor health issue: {health_status.get('error')}")

        except Exception as e:
            self.logger.error(f"Failed to check component health: {e}")

    def _update_workspace_registrations(self):
        """Update workspace registrations across all components"""
        try:
            # Get current workspaces from workspace manager
            workspace_status = self.workspace_manager.get_workspace_status()
            workspaces = workspace_status.get("workspaces", {})

            # Register workspaces with health monitor and resource optimizer
            for workspace_id, workspace_info in workspaces.items():
                # Register with health monitor
                self.health_monitor.register_workspace(workspace_id)

                # Register with resource optimizer
                resource_info = {
                    "memory_mb": workspace_info.get("resource_usage", {}).get("memory_mb", 0),
                    "cpu_percent": workspace_info.get("resource_usage", {}).get("cpu_percent", 0),
                    "agent_count": workspace_info.get("agent_count", 0)
                }
                self.resource_optimizer.register_workspace_resources(workspace_id, resource_info)

        except Exception as e:
            self.logger.error(f"Failed to update workspace registrations: {e}")

    def _perform_system_cleanup(self):
        """Perform system cleanup tasks"""
        try:
            # Clean up old metrics if needed
            # This could include removing old performance data, logs, etc.
            pass

        except Exception as e:
            self.logger.error(f"Failed to perform system cleanup: {e}")

    def get_system_status(self) -> SystemStatus:
        """Get overall system status"""
        try:
            with self.system_lock:
                # Get component statuses
                workspace_status = self.workspace_manager.get_workspace_status()
                consolidation_status = self.consolidation_orchestrator.get_consolidation_status()
                optimization_status = self.resource_optimizer.get_optimization_status()
                health_status = self.health_monitor.get_overall_health_status()

                # Calculate overall metrics
                total_workspaces = workspace_status.get("total_workspaces", 0)
                consolidated_workspaces = consolidation_status.consolidated_workspaces
                overall_health_score = health_status.get("average_health_score", 0.0)

                return SystemStatus(
                    system_active=self.system_active,
                    consolidation_active=consolidation_status.consolidation_active,
                    optimization_active=optimization_status.get("optimization_active", False),
                    health_monitoring_active=self.health_monitor.health_monitoring_active,
                    coordination_active=self.coordination_orchestrator.coordination_active,
                    total_workspaces=total_workspaces,
                    consolidated_workspaces=consolidated_workspaces,
                    overall_health_score=overall_health_score,
                    last_status_update=self.last_status_update.isoformat()
                )

        except Exception as e:
            self.logger.error(f"Failed to get system status: {e}")
            return SystemStatus(
                system_active=False,
                consolidation_active=False,
                optimization_active=False,
                health_monitoring_active=False,
                coordination_active=False,
                total_workspaces=0,
                consolidated_workspaces=0,
                overall_health_score=0.0,
                last_status_update=datetime.now().isoformat()
            )

    def get_consolidation_plan(self) -> Dict[str, Any]:
        """Get workspace consolidation plan"""
        try:
            return self.consolidation_orchestrator.get_workspace_consolidation_plan()
        except Exception as e:
            self.logger.error(f"Failed to get consolidation plan: {e}")
            return {"error": str(e)}

    def add_consolidation_task(self, task_type: str, workspace_id: str, priority: int = 1) -> str:
        """Add a consolidation task"""
        try:
            return self.consolidation_orchestrator.add_consolidation_task(task_type, workspace_id, priority)
        except Exception as e:
            self.logger.error(f"Failed to add consolidation task: {e}")
            return ""

    def get_workspace_health(self, workspace_id: str) -> Optional[Dict[str, Any]]:
        """Get health information for a specific workspace"""
        try:
            health_info = self.health_monitor.get_workspace_health(workspace_id)
            if health_info:
                return {
                    "workspace_id": health_info.workspace_id,
                    "overall_status": health_info.overall_status.value,
                    "overall_score": health_info.overall_score,
                    "last_health_check": health_info.last_health_check,
                    "critical_issues": health_info.critical_issues,
                    "performance_alerts": health_info.performance_alerts
                }
            return None
        except Exception as e:
            self.logger.error(f"Failed to get workspace health for {workspace_id}: {e}")
            return None

    def run_workspace_optimization(self) -> Dict[str, Any]:
        """Run workspace optimization"""
        try:
            return self.workspace_manager.run_workspace_optimization()
        except Exception as e:
            self.logger.error(f"Failed to run workspace optimization: {e}")
            return {"error": str(e)}

    def set_optimization_strategy(self, strategy: str):
        """Set resource optimization strategy"""
        try:
            from .workspace_resource_optimizer import OptimizationStrategy
            strategy_enum = OptimizationStrategy(strategy)
            self.resource_optimizer.set_optimization_strategy(strategy_enum)
        except Exception as e:
            self.logger.error(f"Failed to set optimization strategy: {e}")

    def set_health_check_interval(self, interval_seconds: int):
        """Set health check interval"""
        try:
            self.health_monitor.set_health_check_interval(interval_seconds)
        except Exception as e:
            self.logger.error(f"Failed to set health check interval: {e}")

    def get_performance_summary(self) -> Dict[str, Any]:
        """Get comprehensive performance summary"""
        try:
            # Get status from all components
            system_status = self.get_system_status()
            workspace_status = self.workspace_manager.get_workspace_status()
            consolidation_status = self.consolidation_orchestrator.get_consolidation_status()
            optimization_status = self.resource_optimizer.get_optimization_status()
            health_status = self.health_monitor.get_overall_health_status()

            return {
                "system_status": {
                    "active": system_status.system_active,
                    "uptime_seconds": (datetime.now() - self.system_start_time).total_seconds() if self.system_start_time else 0,
                    "last_update": system_status.last_status_update
                },
                "workspace_status": workspace_status,
                "consolidation_status": {
                    "active": consolidation_status.consolidation_active,
                    "progress": consolidation_status.overall_progress,
                    "total_workspaces": consolidation_status.total_workspaces,
                    "consolidated_workspaces": consolidation_status.consolidated_workspaces
                },
                "optimization_status": optimization_status,
                "health_status": health_status,
                "summary_timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            self.logger.error(f"Failed to get performance summary: {e}")
            return {"error": str(e)}

