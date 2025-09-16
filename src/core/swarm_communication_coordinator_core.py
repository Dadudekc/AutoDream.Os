#!/usr/bin/env python3
"""Swarm Communication Coordinator Core System"""

import asyncio
import logging
import time
from concurrent.futures import ThreadPoolExecutor

from .swarm_agent_manager import SwarmAgentManager
from .swarm_decision_manager import SwarmDecisionManager
from .swarm_quality_manager import SwarmQualityManager
from .unified_core_interfaces import CoreSystemMetadata, IUnifiedCoreSystem

logger = logging.getLogger(__name__)


class SwarmCommunicationCoordinatorCore(IUnifiedCoreSystem):
    """Core swarm communication coordinator with modular components"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._metadata = CoreSystemMetadata(
            name="SwarmCommunicationCoordinatorCore",
            version="3.0.0",
            description="Core coordinator for swarm communication and democratic decision making",
            author="Agent-2",
            dependencies=["swarm_agent_manager", "swarm_decision_manager", "swarm_quality_manager"],
            capabilities=[
                "swarm_coordination",
                "democratic_decision_making",
                "communication_routing",
            ],
        )

        # Initialize modular components
        self.agent_manager = SwarmAgentManager()
        self.decision_manager = SwarmDecisionManager()
        self.quality_manager = SwarmQualityManager()

        # Coordination settings
        self.coordination_broadcast_interval = 60  # 1 minute

        # Initialize coordination state
        self._running = False
        self.executor = None

        # Initialize swarm
        self.agent_manager.initialize_swarm_agents()

        logger.info("Swarm Communication Coordinator Core initialized")

    def start(self) -> None:
        """Start the coordination system"""
        if self._running:
            logger.warning("Swarm Communication Coordinator is already running")
            return

        self._running = True
        self.executor = ThreadPoolExecutor(max_workers=4)

        try:
            loop = asyncio.get_running_loop()
            asyncio.create_task(self._coordination_broadcast_loop())
            asyncio.create_task(self._quality_monitoring_loop())
            asyncio.create_task(self._decision_monitoring_loop())
            logger.info("Swarm Communication Coordinator background tasks started")
        except RuntimeError:
            logger.info("Swarm Communication Coordinator initialized")

    def stop(self) -> None:
        """Stop the coordination system"""
        self._running = False
        if self.executor:
            self.executor.shutdown(wait=True)
        logger.info("Swarm Communication Coordinator stopped")

    @property
    def metadata(self) -> CoreSystemMetadata:
        """Get system metadata"""
        return self._metadata

    def get_capabilities(self) -> list[str]:
        """Get system capabilities"""
        return self._metadata.capabilities

    def get_dependencies(self) -> list[str]:
        """Get system dependencies"""
        return self._metadata.dependencies

    async def _coordination_broadcast_loop(self) -> None:
        """Background loop for coordination broadcasts"""
        while self._running:
            try:
                await self._broadcast_coordination_status()
                await asyncio.sleep(self.coordination_broadcast_interval)
            except Exception as e:
                logger.error(f"Error in coordination broadcast loop: {e}")
                await asyncio.sleep(10)

    async def _quality_monitoring_loop(self) -> None:
        """Background loop for quality monitoring"""
        while self._running:
            try:
                await self._perform_quality_checks()
                await asyncio.sleep(self.quality_manager.qc_check_interval_seconds)
            except Exception as e:
                logger.error(f"Error in quality monitoring loop: {e}")
                await asyncio.sleep(30)

    async def _decision_monitoring_loop(self) -> None:
        """Background loop for decision monitoring"""
        while self._running:
            try:
                await self._monitor_decisions()
                await asyncio.sleep(60)  # Check every minute
            except Exception as e:
                logger.error(f"Error in decision monitoring loop: {e}")
                await asyncio.sleep(30)

    async def _broadcast_coordination_status(self) -> None:
        """Broadcast current coordination status to all agents"""
        try:
            status = self.get_coordination_status()
            # This would integrate with actual messaging system
            logger.debug(f"Broadcasting coordination status: {status}")
        except Exception as e:
            logger.error(f"Error broadcasting coordination status: {e}")

    async def _perform_quality_checks(self) -> None:
        """Perform periodic quality checks"""
        try:
            from .swarm_communication_enums import QCStandard

            for standard in QCStandard:
                self.quality_manager.perform_qc_check(standard, "system")

            logger.debug("Performed periodic quality checks")
        except Exception as e:
            logger.error(f"Error performing quality checks: {e}")

    async def _monitor_decisions(self) -> None:
        """Monitor pending decisions and handle timeouts"""
        try:
            pending_decisions = self.decision_manager.get_pending_decisions()
            voting_decisions = self.decision_manager.get_voting_decisions()

            # Check for timeouts and finalize decisions
            for decision in pending_decisions + voting_decisions:
                if decision.deadline and time.time() > decision.deadline.timestamp():
                    self.decision_manager._finalize_decision(decision.decision_id, timeout=True)

            logger.debug(f"Monitored {len(pending_decisions + voting_decisions)} decisions")
        except Exception as e:
            logger.error(f"Error monitoring decisions: {e}")

    def get_coordination_status(self) -> dict[str, any]:
        """Get current coordination status"""
        return {
            "system_status": "running" if self._running else "stopped",
            "agent_summary": self.agent_manager.get_agent_summary(),
            "decision_summary": self.decision_manager.get_decision_summary(),
            "quality_summary": self.quality_manager.get_qc_summary(),
            "timestamp": time.time(),
        }

    def create_mission_assignment_decision(self, mission_description: str, proposer: str) -> str:
        """Create a mission assignment decision"""
        from .swarm_communication_enums import SwarmDecisionType

        decision = self.decision_manager.create_decision(
            decision_type=SwarmDecisionType.MISSION_ASSIGNMENT,
            description=mission_description,
            proposer=proposer,
            deadline_hours=24,
        )

        logger.info(f"Created mission assignment decision: {decision.decision_id}")
        return decision.decision_id

    def vote_on_decision(self, decision_id: str, agent_id: str, vote: bool) -> bool:
        """Vote on a decision"""
        return self.decision_manager.vote_on_decision(decision_id, agent_id, vote)

    def get_system_metrics(self) -> dict[str, any]:
        """Get comprehensive system metrics"""
        return {
            "agent_metrics": self.agent_manager.get_metrics(),
            "decision_metrics": self.decision_manager.get_metrics(),
            "quality_metrics": self.quality_manager.get_metrics(),
            "system_uptime": time.time() - getattr(self, "_start_time", time.time()),
        }

    def get_status_report(self) -> str:
        """Get a human-readable status report"""
        status = self.get_coordination_status()

        report = f"""
=== SWARM COMMUNICATION COORDINATOR STATUS ===
System Status: {status["system_status"].upper()}
Active Agents: {status["agent_summary"]["active_agents"]}/{status["agent_summary"]["total_agents"]}
Pending Decisions: {status["decision_summary"]["pending_decisions"]}
Voting Decisions: {status["decision_summary"]["voting_decisions"]}
QC Pass Rate: {status["quality_summary"]["overall_pass_rate"]:.1f}%
Last Updated: {time.strftime("%Y-%m-%d %H:%M:%S")}
===============================================
        """

        return report.strip()


def get_swarm_communication_coordinator_core() -> SwarmCommunicationCoordinatorCore:
    """Get the singleton instance of the swarm communication coordinator core"""
    if not hasattr(get_swarm_communication_coordinator_core, "_instance"):
        get_swarm_communication_coordinator_core._instance = SwarmCommunicationCoordinatorCore()
    return get_swarm_communication_coordinator_core._instance

