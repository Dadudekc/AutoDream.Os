#!/usr/bin/env python3
"""
Deployment Coordinator - V2 Compliance Module
=============================================

Main coordination system for deployment operations.
Refactored from monolithic 393-line file into modular architecture.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

import logging
from typing import Dict, Any, Optional, List, Set
from datetime import datetime

from ..deployment_models import (
    MassDeploymentTarget, MaximumEfficiencyDeploymentStatus, DeploymentConfig,
    DeploymentMetrics, DeploymentStatus, create_deployment_metrics, create_default_config
)
from ..engines.deployment_discovery_engine import DeploymentDiscoveryEngine
from ..engines.deployment_execution_engine import DeploymentExecutionEngine
from ..engines.deployment_metrics_engine import DeploymentMetricsEngine


class DeploymentCoordinator:
    """
    Main deployment coordination system for maximum efficiency mass deployment.
    
    Manages deployment targets, coordinates concurrent execution,
    and tracks progress across the entire deployment process.
    """
    
    def __init__(self, config: Optional[DeploymentConfig] = None):
        """Initialize deployment coordinator."""
        self.logger = logging.getLogger(__name__)
        self.config = config or create_default_config()
        
        # Validate configuration
        try:
            self.config.validate()
        except Exception as e:
            self.logger.error(f"Invalid deployment configuration: {e}")
            raise
        
        # Initialize engines
        self.discovery_engine = DeploymentDiscoveryEngine(self.config)
        self.execution_engine = DeploymentExecutionEngine(self.config)
        self.metrics_engine = DeploymentMetricsEngine()
        
        # Set logger references
        self.discovery_engine.logger = self.logger
        self.execution_engine.logger = self.logger
        self.metrics_engine.logger = self.logger
        
        # Deployment state
        self.deployment_targets: List[MassDeploymentTarget] = []
        self.agent_statuses: Dict[str, MaximumEfficiencyDeploymentStatus] = {}
        self.deployment_metrics = create_deployment_metrics()
        
        # Execution state
        self.is_running = False
        self.active_deployments = 0
        
        self.logger.info("Deployment Coordinator initialized")

    def discover_deployment_targets(self, base_path: str = "src") -> List[MassDeploymentTarget]:
        """Discover deployment targets based on file patterns."""
        targets = self.discovery_engine.discover_deployment_targets(base_path)
        self.deployment_targets = targets
        self.deployment_metrics.total_targets = len(targets)
        
        self.logger.info(f"Discovered {len(targets)} deployment targets")
        return targets

    def execute_deployment_batch(self, agent_filter: Optional[Set[str]] = None) -> Dict[str, Any]:
        """Execute deployment batch for discovered targets."""
        if self.is_running:
            return {"success": False, "error": "Deployment already in progress"}
        
        try:
            self.is_running = True
            self.logger.info("Starting deployment batch execution")
            
            # Filter targets if agent filter provided
            targets = self.deployment_targets
            if agent_filter:
                targets = self.discovery_engine.filter_targets_by_agent(targets, agent_filter)
            
            # Sort targets by priority
            targets = self.discovery_engine.sort_targets_by_priority(targets)
            
            # Execute deployments
            results = self.execution_engine.execute_concurrent_deployments(targets, self.deployment_metrics)
            
            # Update metrics
            self.deployment_metrics.total_deployments = len(results)
            
            return {
                "success": True,
                "results": results,
                "metrics": self.deployment_metrics.to_dict()
            }
            
        except Exception as e:
            self.logger.error(f"Error executing deployment batch: {e}")
            return {"success": False, "error": str(e)}
        finally:
            self.is_running = False

    def get_deployment_summary(self) -> Dict[str, Any]:
        """Get comprehensive deployment summary."""
        return self.metrics_engine.get_deployment_summary(
            self.deployment_targets,
            self.deployment_metrics,
            self.agent_statuses,
            self.is_running,
            self.active_deployments,
            self.config
        )

    def get_performance_report(self) -> Dict[str, Any]:
        """Get detailed performance report."""
        return self.metrics_engine.generate_performance_report(self.deployment_metrics)

    def shutdown(self):
        """Shutdown deployment coordinator."""
        self.logger.info("Shutting down deployment coordinator...")
        self.execution_engine.shutdown()
        self.is_running = False
        self.logger.info("Deployment coordinator shutdown complete")
