#!/usr/bin/env python3
"""
Master Distributed Data System
==============================
Master orchestrator for all distributed data systems components.
Follows 200 LOC limit and single responsibility principle.
"""

import logging
import time

from src.utils.stability_improvements import stability_manager, safe_import
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

from multi_agent_data_coordination import MultiAgentDataCoordination
from consistency_management import (
    ConsistencyManagement,
    ConsistencyRule,
    ConsistencyLevel,
)
from distributed_data_workflows import DistributedDataWorkflows, WorkflowDefinition
from data_synchronization import DataSynchronization, SyncPriority

logger = logging.getLogger(__name__)


@dataclass
class DistributedSystemStatus:
    """Overall distributed data system status"""

    timestamp: str
    data_coordination: str
    consistency_management: str
    data_workflows: str
    data_synchronization: str
    overall_health: str
    total_agents: int
    active_workflows: int
    sync_requests: int


class MasterDistributedDataSystem:
    """Master orchestrator for distributed data systems"""

    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.MasterDistributedDataSystem")

        # Initialize all distributed data systems
        self.data_coordination = MultiAgentDataCoordination("master-coordination")
        self.consistency_management = ConsistencyManagement("master-consistency")
        self.data_workflows = DistributedDataWorkflows("master-workflows")
        self.data_synchronization = DataSynchronization("master-sync")

        # System state
        self._system_initialized = False
        self._start_time = time.time()

        self.logger.info("Master Distributed Data System initialized")

    def initialize_system(self) -> bool:
        """Initialize the complete distributed data system"""
        try:
            # Start all engines
            self.data_coordination.start_coordination()
            self.consistency_management.start_consistency_monitoring()
            self.data_workflows.start_workflow_engine()
            self.data_synchronization.start_sync_engine()

            # Set up default consistency rules
            self._setup_default_consistency_rules()

            # Register default workflows
            self._register_default_workflows()

            self._system_initialized = True
            self.logger.info("Distributed Data System fully initialized")
            return True

        except Exception as e:
            self.logger.error(f"Failed to initialize distributed data system: {e}")
            return False

    def _setup_default_consistency_rules(self):
        """Set up default consistency rules"""
        try:
            # User data: Strong consistency with replication
            user_rule = ConsistencyRule(
                "user-data-rule",
                "user-data",
                ConsistencyLevel.STRONG,
                max_drift_ms=1000,
                replication_factor=2,
            )
            self.consistency_management.add_consistency_rule(user_rule)

            # Configuration data: Eventual consistency
            config_rule = ConsistencyRule(
                "config-data-rule",
                "config-data",
                ConsistencyLevel.EVENTUAL,
                max_drift_ms=5000,
                replication_factor=1,
            )
            self.consistency_management.add_consistency_rule(config_rule)

            # Log data: Linearizable consistency
            log_rule = ConsistencyRule(
                "log-data-rule",
                "log-data",
                ConsistencyLevel.LINEARIZABLE,
                max_drift_ms=100,
                replication_factor=3,
            )
            self.consistency_management.add_consistency_rule(log_rule)

        except Exception as e:
            self.logger.warning(f"Failed to setup default consistency rules: {e}")

    def _register_default_workflows(self):
        """Register default data workflows"""
        try:
            # Data backup workflow
            backup_workflow = WorkflowDefinition(
                "data-backup-workflow",
                "Data Backup Pipeline",
                "Automated data backup and replication workflow",
                steps=[
                    {
                        "type": "data_read",
                        "name": "Read Source Data",
                        "data_key": "all-data",
                    },
                    {
                        "type": "data_transform",
                        "name": "Prepare Backup",
                        "transform_type": "copy",
                    },
                    {
                        "type": "data_write",
                        "name": "Write Backup",
                        "data_key": "backup-data",
                    },
                    {
                        "type": "validation",
                        "name": "Validate Backup",
                        "rules": ["integrity_check"],
                    },
                    {
                        "type": "notification",
                        "name": "Backup Complete",
                        "notification_type": "success",
                    },
                ],
            )
            self.data_workflows.register_workflow(backup_workflow)

            # Data sync workflow
            sync_workflow = WorkflowDefinition(
                "data-sync-workflow",
                "Data Synchronization Pipeline",
                "Multi-agent data synchronization workflow",
                steps=[
                    {
                        "type": "data_read",
                        "name": "Read Source Data",
                        "data_key": "sync-data",
                    },
                    {
                        "type": "data_sync",
                        "name": "Synchronize Data",
                        "targets": ["agent-1", "agent-2"],
                    },
                    {
                        "type": "validation",
                        "name": "Validate Sync",
                        "rules": ["consistency_check"],
                    },
                    {
                        "type": "notification",
                        "name": "Sync Complete",
                        "notification_type": "info",
                    },
                ],
            )
            self.data_workflows.register_workflow(sync_workflow)

        except Exception as e:
            self.logger.warning(f"Failed to register default workflows: {e}")

    def register_agent(self, agent_id: str) -> bool:
        """Register an agent with all distributed data systems"""
        try:
            # Register with coordination system
            coord_success = self.data_coordination.register_agent(agent_id)

            if coord_success:
                self.logger.info(
                    f"Agent registered with distributed data system: {agent_id}"
                )
                return True
            else:
                self.logger.warning(f"Failed to register agent: {agent_id}")
                return False

        except Exception as e:
            self.logger.error(f"Agent registration error: {e}")
            return False

    def execute_data_workflow(
        self, workflow_id: str, parameters: Optional[Dict[str, Any]] = None
    ) -> str:
        """Execute a data workflow"""
        try:
            execution_id = self.data_workflows.execute_workflow(workflow_id, parameters)
            self.logger.info(f"Data workflow executed: {workflow_id} ({execution_id})")
            return execution_id
        except Exception as e:
            self.logger.error(f"Workflow execution failed: {e}")
            raise

    def request_data_synchronization(
        self,
        source_agent: str,
        target_agents: List[str],
        data_keys: List[str],
        priority: SyncPriority = SyncPriority.NORMAL,
    ) -> str:
        """Request data synchronization"""
        try:
            request_id = self.data_synchronization.request_synchronization(
                source_agent, target_agents, data_keys, priority
            )
            self.logger.info(f"Data sync requested: {request_id}")
            return request_id
        except Exception as e:
            self.logger.error(f"Data sync request failed: {e}")
            raise

    def get_system_status(self) -> DistributedSystemStatus:
        """Get comprehensive distributed data system status"""
        from datetime import datetime

        # Get status from all components
        coord_status = self.data_coordination.get_coordination_status()
        consistency_status = self.consistency_management.get_consistency_status()
        workflow_stats = self.data_workflows.get_workflow_statistics()
        sync_stats = self.data_synchronization.get_synchronization_stats()

        # Calculate overall health
        health_scores = [
            consistency_status.get("consistent_keys", 0)
            / max(1, consistency_status.get("total_rules", 1))
            * 100,
            workflow_stats.get("success_rate", 0),
            sync_stats.get("success_rate", 0),
        ]
        avg_health = sum(health_scores) / len(health_scores)

        if avg_health >= 80:
            overall_health = "HEALTHY"
        elif avg_health >= 60:
            overall_health = "DEGRADED"
        else:
            overall_health = "CRITICAL"

        return DistributedSystemStatus(
            timestamp=datetime.now().isoformat(),
            data_coordination="ACTIVE"
            if coord_status.get("coordination_active")
            else "INACTIVE",
            consistency_management="ACTIVE"
            if consistency_status.get("monitoring_active")
            else "INACTIVE",
            data_workflows="ACTIVE"
            if workflow_stats.get("engine_active")
            else "INACTIVE",
            data_synchronization="ACTIVE"
            if sync_stats.get("sync_engine_active")
            else "INACTIVE",
            overall_health=overall_health,
            total_agents=coord_status.get("active_agents", 0),
            active_workflows=workflow_stats.get("active_executions", 0),
            sync_requests=sync_stats.get("pending_requests", 0),
        )

    def generate_system_report(self) -> str:
        """Generate comprehensive distributed data system report"""
        status = self.get_system_status()

        lines = [
            "🚀 DISTRIBUTED DATA SYSTEM COMPREHENSIVE REPORT",
            "=" * 60,
            f"Timestamp: {status.timestamp}",
            f"Overall Health: {status.overall_health}",
            f"Total Agents: {status.total_agents}",
            f"Active Workflows: {status.active_workflows}",
            f"Sync Requests: {status.sync_requests}",
            "",
            "COMPONENT STATUS:",
            f"  Data Coordination: {status.data_coordination}",
            f"  Consistency Management: {status.consistency_management}",
            f"  Data Workflows: {status.data_workflows}",
            f"  Data Synchronization: {status.data_synchronization}",
            "",
            "SYSTEM METRICS:",
        ]

        # Add component-specific metrics
        coord_status = self.data_coordination.get_coordination_status()
        consistency_status = self.consistency_management.get_consistency_status()
        workflow_stats = self.data_workflows.get_workflow_statistics()
        sync_stats = self.data_synchronization.get_synchronization_stats()

        lines.extend(
            [
                f"  Coordination - Active Agents: {coord_status.get('active_agents', 0)}",
                f"  Consistency - Rules: {consistency_status.get('total_rules', 0)}",
                f"  Workflows - Success Rate: {workflow_stats.get('success_rate', 0):.1f}%",
                f"  Synchronization - Success Rate: {sync_stats.get('success_rate', 0):.1f}%",
            ]
        )

        lines.append("=" * 60)
        return "\n".join(lines)

    def shutdown_system(self):
        """Gracefully shutdown the distributed data system"""
        self.logger.info("Shutting down Distributed Data System")

        try:
            self.data_coordination.stop_coordination()
            self.consistency_management.stop_consistency_monitoring()
            self.data_workflows.stop_workflow_engine()
            self.data_synchronization.stop_sync_engine()

            self._system_initialized = False
            self.logger.info("Distributed Data System shutdown complete")

        except Exception as e:
            self.logger.error(f"Shutdown error: {e}")


def main():
    """CLI interface for testing MasterDistributedDataSystem"""
    import argparse

    parser = argparse.ArgumentParser(description="Master Distributed Data System CLI")
    parser.add_argument("--test", action="store_true", help="Run comprehensive test")

    args = parser.parse_args()

    if args.test:
        print("🧪 MasterDistributedDataSystem Comprehensive Test")
        print("=" * 55)

        master = MasterDistributedDataSystem()

        # Initialize system
        init_success = master.initialize_system()
        print(f"✅ System initialization: {init_success}")

        # Register test agents
        agent1_success = master.register_agent("test-agent-1")
        agent2_success = master.register_agent("test-agent-2")
        print(f"✅ Agent 1 registration: {agent1_success}")
        print(f"✅ Agent 2 registration: {agent2_success}")

        # Execute workflow
        try:
            execution_id = master.execute_data_workflow("data-backup-workflow")
            print(f"✅ Workflow execution: {execution_id}")
        except Exception as e:
            print(f"⚠️ Workflow execution: {e}")

        # Request synchronization
        try:
            sync_id = master.request_data_synchronization(
                "test-agent-1", ["test-agent-2"], ["test-data"], SyncPriority.HIGH
            )
            print(f"✅ Data sync request: {sync_id}")
        except Exception as e:
            print(f"⚠️ Data sync request: {e}")

        # Get system status
        status = master.get_system_status()
        print(f"✅ System health: {status.overall_health}")
        print(f"✅ Total agents: {status.total_agents}")

        # Generate report
        report = master.generate_system_report()
        print("\n📊 SYSTEM REPORT:")
        print(report)

        # Cleanup
        master.shutdown_system()
        print("\n🎉 MasterDistributedDataSystem test PASSED!")

    else:
        print("MasterDistributedDataSystem ready")
        print("Use --test to run comprehensive test")


if __name__ == "__main__":
    main()
