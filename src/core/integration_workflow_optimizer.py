"""
Integration Workflow Optimizer - V2 Compliant
=============================================

Main integration workflow optimization system.
V2 Compliance: ≤400 lines, ≤10 functions, orchestrates components
"""

import time
from pathlib import Path

from .data_synchronizer import DataSynchronizer
from .integration_workflow_core import IntegrationWorkflowCore
from .integration_workflow_models import IntegrationPattern
from .service_connector import ServiceConnector


class IntegrationWorkflowOptimizer:
    """Main integration workflow optimization system."""

    def __init__(self):
        """Initialize the optimizer."""
        self.core = IntegrationWorkflowCore()
        self.connector = ServiceConnector()
        self.synchronizer = DataSynchronizer()
        self.optimization_results = []

    def optimize_workflow(
        self, workflow_id: str, pattern: IntegrationPattern, source: str, target: str
    ) -> dict:
        """Optimize a complete integration workflow."""
        # Create workflow
        workflow = self.core.create_workflow(workflow_id, pattern, source, target)

        # Establish connection
        connection_success = self.connector.establish_connection(workflow)

        # Optimize based on pattern
        if pattern == IntegrationPattern.SERVICE_TO_SERVICE:
            optimization = self.core.optimize_service_connections(workflow)
        elif pattern == IntegrationPattern.DATA_PIPELINE:
            optimization = self.core.optimize_data_pipeline(workflow)
        elif pattern == IntegrationPattern.EVENT_DRIVEN:
            optimization = self.core.optimize_event_driven_workflow(workflow)
        else:
            optimization = self.core.optimize_service_connections(workflow)

        # Create sync job if needed
        sync_job_id = None
        if pattern in [IntegrationPattern.DATA_PIPELINE, IntegrationPattern.EVENT_DRIVEN]:
            source_config = {"type": "database", "connection": source}
            target_config = {"type": "api", "connection": target}
            sync_job_id = self.synchronizer.create_sync_job(workflow, source_config, target_config)

        result = {
            "workflow_id": workflow_id,
            "pattern": pattern.value,
            "connection_established": connection_success,
            "optimization": optimization,
            "sync_job_id": sync_job_id,
            "success": True,
        }

        self.optimization_results.append(result)
        return result

    def get_system_metrics(self) -> dict:
        """Get comprehensive system metrics."""
        core_summary = self.core.get_optimization_summary()
        connector_metrics = self.connector.get_connection_metrics()
        sync_metrics = self.synchronizer.get_sync_metrics()

        return {
            "core": core_summary,
            "connections": connector_metrics,
            "synchronization": sync_metrics,
            "total_optimizations": len(self.optimization_results),
        }

    def optimize_system_performance(self) -> dict:
        """Optimize overall system performance."""
        start_time = time.time()

        # Optimize connections
        conn_optimization = self.connector.optimize_connection_pool()

        # Optimize synchronization
        sync_optimization = self.synchronizer.optimize_sync_performance()

        optimization_time = time.time() - start_time

        return {
            "connection_optimization": conn_optimization,
            "sync_optimization": sync_optimization,
            "total_optimization_time": optimization_time,
            "success": True,
        }

    def cleanup_system(self) -> dict:
        """Clean up system resources."""
        # Clean up old sync jobs
        cleaned_jobs = self.synchronizer.cleanup_old_jobs()

        # Get active connections count
        active_connections = len(self.connector.list_active_connections())

        return {
            "cleaned_jobs": cleaned_jobs,
            "active_connections": active_connections,
            "success": True,
        }

    def save_system_state(self, base_path: str) -> bool:
        """Save complete system state."""
        try:
            base_path = Path(base_path)
            base_path.mkdir(exist_ok=True)

            # Save core configuration
            core_success = self.core.save_configuration(str(base_path / "core_config.json"))

            # Save connection state
            conn_success = self.connector.save_connection_state(str(base_path / "connections.json"))

            # Save sync state
            sync_success = self.synchronizer.save_sync_state(str(base_path / "sync_state.json"))

            return core_success and conn_success and sync_success
        except Exception:
            return False

    def load_system_state(self, base_path: str) -> bool:
        """Load complete system state."""
        try:
            base_path = Path(base_path)

            # Load core configuration
            core_success = self.core.load_configuration(str(base_path / "core_config.json"))

            # Load connection state
            conn_success = self.connector.load_connection_state(str(base_path / "connections.json"))

            # Load sync state
            sync_success = self.synchronizer.load_sync_state(str(base_path / "sync_state.json"))

            return core_success and conn_success and sync_success
        except Exception:
            return False

    def get_optimization_report(self) -> dict:
        """Generate comprehensive optimization report."""
        metrics = self.get_system_metrics()

        return {
            "timestamp": time.time(),
            "metrics": metrics,
            "optimization_results": self.optimization_results,
            "system_health": "good" if metrics["total_optimizations"] > 0 else "no_optimizations",
        }
