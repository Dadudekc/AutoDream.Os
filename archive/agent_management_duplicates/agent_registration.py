#!/usr/bin/env python3
"""
Agent Registration - V2 Core Agent Registration System

This module handles agent discovery, onboarding, capability assessment, and resource allocation.
Follows Single Responsibility Principle - only agent registration.
Architecture: Single Responsibility Principle - agent registration only
LOC: Target 200 lines (under 200 limit)
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any, Set
from pathlib import Path
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime, timedelta
import threading
import time
import uuid

from .agent_manager import AgentManager, AgentStatus, AgentCapability, AgentInfo
from .config_manager import ConfigManager

logger = logging.getLogger(__name__)


class RegistrationStatus(Enum):
    """Agent registration status"""

    DISCOVERED = "discovered"
    REGISTERING = "registering"
    REGISTERED = "registered"
    FAILED = "failed"
    EXPIRED = "expired"


class DiscoveryMethod(Enum):
    """Agent discovery methods"""

    DIRECTORY_SCAN = "directory_scan"
    HEARTBEAT_DETECTION = "heartbeat_detection"
    MANUAL_REGISTRATION = "manual_registration"
    AUTO_DISCOVERY = "auto_discovery"


@dataclass
class RegistrationRequest:
    """Agent registration request"""

    request_id: str
    agent_id: str
    agent_name: str
    capabilities: List[AgentCapability]
    discovery_method: DiscoveryMethod
    timestamp: str
    status: RegistrationStatus
    metadata: Dict[str, Any]


@dataclass
class CapabilityAssessment:
    """Agent capability assessment result"""

    agent_id: str
    capabilities: List[AgentCapability]
    skill_levels: Dict[AgentCapability, float]
    performance_history: Dict[str, float]
    reliability_score: float
    assessment_timestamp: str


class AgentRegistrationManager:
    """
    Manages agent registration, discovery, and capability assessment

    Responsibilities:
    - Agent discovery and detection
    - Registration workflow management
    - Capability assessment and classification
    - Resource allocation and placement
    """

    def __init__(self, agent_manager: AgentManager, config_manager: ConfigManager):
        self.agent_manager = agent_manager
        self.config_manager = config_manager
        self.registration_requests: Dict[str, RegistrationRequest] = {}
        self.capability_assessments: Dict[str, CapabilityAssessment] = {}
        self.discovery_thread = None
        self.running = False
        self.logger = logging.getLogger(f"{__name__}.AgentRegistrationManager")

        # Start discovery thread
        self._start_discovery_thread()

    def _start_discovery_thread(self):
        """Start the agent discovery thread"""
        self.running = True
        self.discovery_thread = threading.Thread(
            target=self._discovery_loop, daemon=True
        )
        self.discovery_thread.start()
        self.logger.info("Agent discovery thread started")

    def _discovery_loop(self):
        """Main discovery loop for detecting new agents"""
        while self.running:
            try:
                # Scan for new agents
                self._scan_for_new_agents()

                # Check for expired registrations
                self._cleanup_expired_registrations()

                # Wait before next scan
                time.sleep(30)  # Scan every 30 seconds

            except Exception as e:
                self.logger.error(f"Discovery loop error: {e}")
                time.sleep(60)  # Wait longer on error

    def _scan_for_new_agents(self):
        """Scan for new agents in the workspace"""
        try:
            workspace_dir = Path(
                self.config_manager.get_config(
                    "agents", "workspace_dir", "agent_workspaces"
                )
            )

            if not workspace_dir.exists():
                return

            # Scan for new agent directories
            for agent_dir in workspace_dir.iterdir():
                if agent_dir.is_dir() and agent_dir.name.startswith("Agent-"):
                    agent_id = agent_dir.name

                    # Check if agent is already registered
                    if not self.agent_manager.get_workspace_info(agent_id):
                        # New agent discovered
                        self._handle_new_agent_discovery(agent_id, agent_dir)

        except Exception as e:
            self.logger.error(f"Agent discovery scan failed: {e}")

    def _handle_new_agent_discovery(self, agent_id: str, agent_dir: Path):
        """Handle discovery of a new agent"""
        try:
            # Create registration request
            request = RegistrationRequest(
                request_id=str(uuid.uuid4()),
                agent_id=agent_id,
                agent_name=agent_id,
                capabilities=self._detect_agent_capabilities(agent_dir),
                discovery_method=DiscoveryMethod.DIRECTORY_SCAN,
                timestamp=datetime.now().isoformat(),
                status=RegistrationStatus.DISCOVERED,
                metadata={"discovery_path": str(agent_dir)},
            )

            # Store registration request
            self.registration_requests[request.request_id] = request

            # Attempt automatic registration
            if self._should_auto_register(request):
                self._process_registration_request(request.request_id)

            self.logger.info(f"New agent discovered: {agent_id}")

        except Exception as e:
            self.logger.error(
                f"Failed to handle new agent discovery for {agent_id}: {e}"
            )

    def _detect_agent_capabilities(self, agent_dir: Path) -> List[AgentCapability]:
        """Detect agent capabilities based on directory structure and files"""
        try:
            capabilities = []

            # Check for capability indicators in directory structure
            if (agent_dir / "refactoring").exists():
                capabilities.append(AgentCapability.REFACTORING)

            if (agent_dir / "testing").exists():
                capabilities.append(AgentCapability.TESTING)

            if (agent_dir / "integration").exists():
                capabilities.append(AgentCapability.INTEGRATION)

            if (agent_dir / "documentation").exists():
                capabilities.append(AgentCapability.DOCUMENTATION)

            if (agent_dir / "coordination").exists():
                capabilities.append(AgentCapability.COORDINATION)

            if (agent_dir / "security").exists():
                capabilities.append(AgentCapability.SECURITY)

            if (agent_dir / "performance").exists():
                capabilities.append(AgentCapability.PERFORMANCE)

            # If no specific capabilities detected, assign general ones
            if not capabilities:
                capabilities = [AgentCapability.TESTING, AgentCapability.DOCUMENTATION]

            return capabilities

        except Exception as e:
            self.logger.error(f"Failed to detect capabilities for {agent_dir}: {e}")
            return [AgentCapability.TESTING]  # Default capability

    def _should_auto_register(self, request: RegistrationRequest) -> bool:
        """Determine if agent should be automatically registered"""
        try:
            auto_register = self.config_manager.get_config(
                "agents", "auto_register", True
            )
            if not auto_register:
                return False

            # Check if agent has minimum required capabilities
            min_capabilities = self.config_manager.get_config(
                "agents", "min_capabilities", 1
            )
            if len(request.capabilities) < min_capabilities:
                return False

            return True

        except Exception as e:
            self.logger.error(
                f"Failed to determine auto-registration for {request.agent_id}: {e}"
            )
            return False

    def register_agent_manual(
        self, agent_id: str, agent_name: str, capabilities: List[AgentCapability]
    ) -> str:
        """Manually register an agent"""
        try:
            # Create registration request
            request = RegistrationRequest(
                request_id=str(uuid.uuid4()),
                agent_id=agent_id,
                agent_name=agent_name,
                capabilities=capabilities,
                discovery_method=DiscoveryMethod.MANUAL_REGISTRATION,
                timestamp=datetime.now().isoformat(),
                status=RegistrationStatus.REGISTERING,
                metadata={"manual_registration": True},
            )

            # Store registration request
            self.registration_requests[request.request_id] = request

            # Process registration
            success = self._process_registration_request(request.request_id)

            if success:
                return request.request_id
            else:
                return ""

        except Exception as e:
            self.logger.error(f"Failed to manually register agent {agent_id}: {e}")
            return ""

    def _process_registration_request(self, request_id: str) -> bool:
        """Process a registration request"""
        try:
            if request_id not in self.registration_requests:
                return False

            request = self.registration_requests[request_id]

            # Update status to registering
            request.status = RegistrationStatus.REGISTERING

            # Attempt to register with agent manager
            success = self.agent_manager.register_agent(
                request.agent_id, request.agent_name, request.capabilities
            )

            if success:
                # Update status to registered
                request.status = RegistrationStatus.REGISTERED

                # Perform capability assessment
                self._perform_capability_assessment(
                    request.agent_id, request.capabilities
                )

                self.logger.info(f"Agent {request.agent_id} registered successfully")
                return True
            else:
                # Update status to failed
                request.status = RegistrationStatus.FAILED
                self.logger.error(f"Failed to register agent {request.agent_id}")
                return False

        except Exception as e:
            self.logger.error(
                f"Failed to process registration request {request_id}: {e}"
            )
            return False

    def _perform_capability_assessment(
        self, agent_id: str, capabilities: List[AgentCapability]
    ):
        """Perform capability assessment for an agent"""
        try:
            # Initialize skill levels
            skill_levels = {}
            for capability in capabilities:
                skill_levels[capability] = 0.5  # Default skill level

            # Create capability assessment
            assessment = CapabilityAssessment(
                agent_id=agent_id,
                capabilities=capabilities,
                skill_levels=skill_levels,
                performance_history={},
                reliability_score=0.8,  # Default reliability
                assessment_timestamp=datetime.now().isoformat(),
            )

            # Store assessment
            self.capability_assessments[agent_id] = assessment

            self.logger.info(f"Capability assessment completed for {agent_id}")

        except Exception as e:
            self.logger.error(
                f"Failed to perform capability assessment for {agent_id}: {e}"
            )

    def get_registration_status(self, request_id: str) -> Optional[RegistrationStatus]:
        """Get registration status for a request"""
        if request_id in self.registration_requests:
            return self.registration_requests[request_id].status
        return None

    def get_pending_registrations(self) -> List[RegistrationRequest]:
        """Get all pending registration requests"""
        return [
            req
            for req in self.registration_requests.values()
            if req.status == RegistrationStatus.DISCOVERED
        ]

    def get_capability_assessment(
        self, agent_id: str
    ) -> Optional[CapabilityAssessment]:
        """Get capability assessment for an agent"""
        return self.capability_assessments.get(agent_id)

    def update_capability_assessment(
        self, agent_id: str, capability: AgentCapability, skill_level: float
    ):
        """Update capability assessment for an agent"""
        try:
            if agent_id in self.capability_assessments:
                assessment = self.capability_assessments[agent_id]
                assessment.skill_levels[capability] = max(0.0, min(1.0, skill_level))
                assessment.assessment_timestamp = datetime.now().isoformat()

                self.logger.info(
                    f"Updated capability assessment for {agent_id}: {capability.value} = {skill_level}"
                )

        except Exception as e:
            self.logger.error(
                f"Failed to update capability assessment for {agent_id}: {e}"
            )

    def _cleanup_expired_registrations(self):
        """Clean up expired registration requests"""
        try:
            current_time = datetime.now()
            expired_requests = []

            for request_id, request in self.registration_requests.items():
                request_time = datetime.fromisoformat(request.timestamp)

                # Expire requests older than 24 hours
                if current_time - request_time > timedelta(hours=24):
                    expired_requests.append(request_id)

            # Remove expired requests
            for request_id in expired_requests:
                del self.registration_requests[request_id]

            if expired_requests:
                self.logger.info(
                    f"Cleaned up {len(expired_requests)} expired registration requests"
                )

        except Exception as e:
            self.logger.error(f"Failed to cleanup expired registrations: {e}")

    def get_registration_summary(self) -> Dict[str, Any]:
        """Get summary of registration system"""
        try:
            total_requests = len(self.registration_requests)
            pending_requests = len(self.get_pending_registrations())
            registered_agents = len(self.capability_assessments)

            return {
                "total_requests": total_requests,
                "pending_requests": pending_requests,
                "registered_agents": registered_agents,
                "discovery_active": self.running,
                "auto_register_enabled": self.config_manager.get_config(
                    "agents", "auto_register", True
                ),
            }
        except Exception as e:
            self.logger.error(f"Failed to get registration summary: {e}")
            return {"error": str(e)}

    def run_smoke_test(self) -> bool:
        """Run basic functionality test for this instance"""
        try:
            # Test manual registration
            test_agent_id = "smoke_test_agent"
            request_id = self.register_agent_manual(
                test_agent_id, "Smoke Test Agent", [AgentCapability.TESTING]
            )

            if not request_id:
                return False

            # Test registration status
            status = self.get_registration_status(request_id)
            if status != RegistrationStatus.REGISTERED:
                return False

            # Test capability assessment
            assessment = self.get_capability_assessment(test_agent_id)
            if not assessment:
                return False

            # Test capability update
            self.update_capability_assessment(
                test_agent_id, AgentCapability.TESTING, 0.8
            )

            # Test registration summary
            summary = self.get_registration_summary()
            if "total_requests" not in summary:
                return False

            return True

        except Exception as e:
            self.logger.error(f"Smoke test failed: {e}")
            return False

    def shutdown(self):
        """Shutdown the registration manager"""
        self.running = False
        if self.discovery_thread:
            self.discovery_thread.join(timeout=5)


def run_smoke_test():
    """Run basic functionality test for AgentRegistrationManager"""
    print("🧪 Running AgentRegistrationManager Smoke Test...")

    try:
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            # Create temporary config and agent directories
            config_dir = Path(temp_dir) / "config"
            agent_dir = Path(temp_dir) / "agent_workspaces"
            config_dir.mkdir()
            agent_dir.mkdir()

            # Create mock config
            config_file = config_dir / "agents.json"
            with open(config_file, "w") as f:
                json.dump({"workspace_dir": str(agent_dir), "auto_register": True}, f)

            # Initialize managers
            config_manager = ConfigManager(config_dir)
            agent_manager = AgentManager(agent_dir)
            registration_manager = AgentRegistrationManager(
                agent_manager, config_manager
            )

            # Test manual registration
            test_agent_id = "smoke_test_agent"
            request_id = registration_manager.register_agent_manual(
                test_agent_id, "Smoke Test Agent", [AgentCapability.TESTING]
            )
            assert request_id

            # Test registration status
            status = registration_manager.get_registration_status(request_id)
            assert status == RegistrationStatus.REGISTERED

            # Test capability assessment
            assessment = registration_manager.get_capability_assessment(test_agent_id)
            assert assessment is not None

            # Test registration summary
            summary = registration_manager.get_registration_summary()
            assert "total_requests" in summary

            # Cleanup
            registration_manager.shutdown()
            agent_manager.shutdown()
            config_manager.shutdown()

        print("✅ AgentRegistrationManager Smoke Test PASSED")
        return True

    except Exception as e:
        print(f"❌ AgentRegistrationManager Smoke Test FAILED: {e}")
        return False


def main():
    """CLI interface for AgentRegistrationManager testing"""
    import argparse

    parser = argparse.ArgumentParser(description="Agent Registration Manager CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    parser.add_argument(
        "--register",
        nargs=3,
        metavar=("ID", "NAME", "CAPABILITIES"),
        help="Manually register agent",
    )
    parser.add_argument("--status", help="Get registration status by request ID")
    parser.add_argument(
        "--pending", action="store_true", help="Show pending registrations"
    )
    parser.add_argument("--assessment", help="Get capability assessment for agent")
    parser.add_argument(
        "--summary", action="store_true", help="Show registration summary"
    )

    args = parser.parse_args()

    if args.test:
        run_smoke_test()
        return

    # Initialize managers
    config_manager = ConfigManager()
    agent_manager = AgentManager()
    registration_manager = AgentRegistrationManager(agent_manager, config_manager)

    if args.register:
        agent_id, name, capabilities_str = args.register
        capabilities = [
            AgentCapability(cap.strip()) for cap in capabilities_str.split(",")
        ]
        request_id = registration_manager.register_agent_manual(
            agent_id, name, capabilities
        )
        print(f"Agent registration: {'✅ Success' if request_id else '❌ Failed'}")
        if request_id:
            print(f"Request ID: {request_id}")
    elif args.status:
        status = registration_manager.get_registration_status(args.status)
        if status:
            print(f"Registration status: {status.value}")
        else:
            print(f"Request '{args.status}' not found")
    elif args.pending:
        pending = registration_manager.get_pending_registrations()
        print("Pending Registrations:")
        for req in pending:
            print(f"  {req.agent_id}: {req.status.value}")
    elif args.assessment:
        assessment = registration_manager.get_capability_assessment(args.assessment)
        if assessment:
            print(f"Capability Assessment for {args.assessment}:")
            for cap, level in assessment.skill_levels.items():
                print(f"  {cap.value}: {level}")
        else:
            print(f"Assessment for '{args.assessment}' not found")
    elif args.summary:
        summary = registration_manager.get_registration_summary()
        print("Registration Summary:")
        for key, value in summary.items():
            print(f"  {key}: {value}")
    else:
        parser.print_help()

    # Cleanup
    registration_manager.shutdown()
    agent_manager.shutdown()
    config_manager.shutdown()


if __name__ == "__main__":
    main()
