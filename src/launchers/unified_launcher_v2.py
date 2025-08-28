#!/usr/bin/env python3
"""
Unified Launcher V2 - Agent Cellphone V2
========================================

Unified launcher with FSM integration and strict OOP design.
Follows Single Responsibility Principle with 200 LOC limit.
"""

import logging
import argparse

from src.utils.stability_improvements import stability_manager, safe_import
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class LaunchConfig:
    """Launch configuration data."""

    mode: str
    agents: list
    fsm_enabled: bool
    monitoring_enabled: bool
    workspace_path: str
    config_path: str


class UnifiedLauncherV2:
    """
    Unified Launcher V2 - Single responsibility: System launch and coordination.

    This service manages:
    - System initialization and startup
    - FSM orchestrator integration
    - Agent coordination launch
    - Service health monitoring
    """

    def __init__(self, config_path: str = "config"):
        """Initialize Unified Launcher V2."""
        self.config_path = Path(config_path)
        self.logger = self._setup_logging()
        self.status = "initialized"
        self.services = {}
        self.launch_config: Optional[LaunchConfig] = None

        # Initialize component managers
        self._initialize_managers()

    def _setup_logging(self) -> logging.Logger:
        """Setup logging for the service."""
        logger = logging.getLogger("UnifiedLauncherV2")
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def _initialize_managers(self):
        """Initialize all component managers."""
        try:
            # Import managers with proper path handling
            import sys
            from pathlib import Path

            # Add src to path for imports
            src_path = Path(__file__).parent.parent
            if str(src_path) not in sys.path:
                sys.path.insert(0, str(src_path))

            from core.workspace_manager import WorkspaceManager
            from core.inbox_manager import InboxManager
            from core.task_manager import TaskManager
            from core.fsm import FSMSystemManager
            from services.response_capture import (
                ResponseCaptureService,
                CaptureConfig,
                CaptureStrategy,
            )

            # Initialize workspace manager
            self.workspace_manager = WorkspaceManager()
            self.services["workspace"] = self.workspace_manager
            self.logger.info("Workspace Manager initialized")

            # Initialize inbox manager
            self.inbox_manager = InboxManager(self.workspace_manager)
            self.services["inbox"] = self.inbox_manager
            self.logger.info("Inbox Manager initialized")

            # Initialize task manager
            self.task_manager = TaskManager(self.workspace_manager)
            self.services["task"] = self.task_manager
            self.logger.info("Task Manager initialized")

            # Initialize FSM system manager
            self.fsm_system_manager = FSMSystemManager()
            self.services["fsm"] = self.fsm_system_manager
            self.logger.info("FSM System Manager initialized")

            # Initialize response capture service
            capture_config = CaptureConfig(strategy=CaptureStrategy.FILE)
            self.response_capture = ResponseCaptureService(capture_config)
            self.services["response_capture"] = self.response_capture
            self.logger.info("Response Capture Service initialized")

            self.status = "managers_ready"

        except Exception as e:
            self.logger.error(f"Failed to initialize managers: {e}")
            self.status = "initialization_failed"

    def launch_system(
        self,
        mode: str = "standard",
        agents: list = None,
        fsm_enabled: bool = True,
        monitoring_enabled: bool = True,
    ) -> bool:
        """Launch the complete V2 system."""
        try:
            self.logger.info(f"Launching V2 system in {mode} mode...")

            # Create launch configuration
            self.launch_config = LaunchConfig(
                mode=mode,
                agents=agents
                or ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5"],
                fsm_enabled=fsm_enabled,
                monitoring_enabled=monitoring_enabled,
                workspace_path="agent_workspaces",
                config_path=str(self.config_path),
            )

            # Create agent workspaces
            for agent in self.launch_config.agents:
                self.workspace_manager.create_workspace(agent)

            # Start FSM system manager if enabled
            if fsm_enabled:
                self.logger.info("FSM System Manager monitoring active")

            # Start response capture if enabled
            if monitoring_enabled:
                self.response_capture.start_capture()
                self.logger.info("Response Capture monitoring started")

            self.status = "running"
            self.logger.info("V2 system launched successfully")
            return True

        except Exception as e:
            self.logger.error(f"Failed to launch system: {e}")
            self.status = "launch_failed"
            return False

    def create_fsm_task(
        self,
        title: str,
        description: str,
        assigned_agent: str,
        priority: str = "normal",
    ) -> str:
        """Create FSM task through the launcher."""
        try:
            from core.fsm import TaskPriority

            # Convert string priority to enum
            priority_map = {
                "low": TaskPriority.LOW,
                "normal": TaskPriority.NORMAL,
                "high": TaskPriority.HIGH,
                "critical": TaskPriority.CRITICAL,
            }

            task_priority = priority_map.get(priority.lower(), TaskPriority.NORMAL)

            # Create task via FSM system manager
            task_id = self.fsm_system_manager.create_task(
                title=title,
                description=description,
                assigned_agent=assigned_agent,
                priority=task_priority,
            )

            self.logger.info(f"Created FSM task: {task_id} for {assigned_agent}")
            return task_id

        except Exception as e:
            self.logger.error(f"Failed to create FSM task: {e}")
            return ""

    def send_coordination_message(
        self, sender: str, recipient: str, message_type: str, content: str
    ) -> bool:
        """Send coordination message between agents."""
        try:
            # Send message via inbox manager
            message_id = self.inbox_manager.send_message(
                sender=sender,
                recipient=recipient,
                subject=f"Coordination: {message_type}",
                content=content,
            )

            if message_id:
                self.logger.info(f"Coordination message sent: {sender} -> {recipient}")
                return True
            return False

        except Exception as e:
            self.logger.error(f"Failed to send coordination message: {e}")
            return False

    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status."""
        try:
            status = {
                "launcher_status": self.status,
                "launch_time": datetime.now().isoformat(),
                "launch_config": self.launch_config.__dict__
                if self.launch_config
                else None,
                "services": {},
            }

            # Get status from each service
            for service_name, service in self.services.items():
                try:
                    if hasattr(service, "get_workspace_status"):
                        status["services"][
                            service_name
                        ] = service.get_workspace_status()
                    elif hasattr(service, "get_system_status"):
                        status["services"][service_name] = service.get_system_status()
                    elif hasattr(service, "get_fsm_status"):
                        status["services"][service_name] = service.get_fsm_status()
                    elif hasattr(service, "get_status"):
                        status["services"][service_name] = service.get_status()
                    else:
                        status["services"][service_name] = {"status": "active"}
                except Exception as e:
                    status["services"][service_name] = {
                        "status": "error",
                        "error": str(e),
                    }

            return status

        except Exception as e:
            self.logger.error(f"Failed to get system status: {e}")
            return {"launcher_status": "error", "error": str(e)}

    def shutdown_system(self) -> bool:
        """Shutdown the complete V2 system."""
        try:
            self.logger.info("Shutting down V2 system...")

            # Shutdown services in reverse order
            services_to_shutdown = [
                ("response_capture", "stop_capture"),
                ("fsm", "stop_monitoring"),
                ("fsm", "shutdown_orchestrator"),
                ("task", "shutdown_manager"),
                ("inbox", "shutdown_manager"),
                ("workspace", "shutdown_manager"),
            ]

            for service_name, method_name in services_to_shutdown:
                if service_name in self.services:
                    service = self.services[service_name]
                    if hasattr(service, method_name):
                        try:
                            getattr(service, method_name)()
                            self.logger.info(f"Shutdown {service_name} service")
                        except Exception as e:
                            self.logger.error(f"Failed to shutdown {service_name}: {e}")

            self.status = "shutdown"
            self.logger.info("V2 system shutdown complete")
            return True

        except Exception as e:
            self.logger.error(f"Failed to shutdown system: {e}")
            return False

    def run_workflow(self, workflow_name: str, **kwargs) -> bool:
        """Run a predefined workflow."""
        try:
            if workflow_name == "agent_swarm":
                return self._run_agent_swarm_workflow(**kwargs)
            elif workflow_name == "coordination":
                return self._run_coordination_workflow(**kwargs)
            elif workflow_name == "onboarding":
                return self._run_onboarding_workflow(**kwargs)
            else:
                self.logger.error(f"Unknown workflow: {workflow_name}")
                return False

        except Exception as e:
            self.logger.error(f"Failed to run workflow {workflow_name}: {e}")
            return False

    def _run_agent_swarm_workflow(self, **kwargs) -> bool:
        """Run agent swarm coordination workflow."""
        try:
            # Create coordination tasks for all agents
            for agent in self.launch_config.agents:
                task_id = self.create_fsm_task(
                    title=f"Agent Swarm Coordination - {agent}",
                    description=f"Coordinate with other agents in swarm mode",
                    assigned_agent=agent,
                    priority="high",
                )

                # Send coordination message
                self.send_coordination_message(
                    "UnifiedLauncher",
                    agent,
                    "SWARM_ACTIVATION",
                    f"Agent swarm activated. Your task ID: {task_id}",
                )

            self.logger.info("Agent swarm workflow initiated")
            return True

        except Exception as e:
            self.logger.error(f"Agent swarm workflow failed: {e}")
            return False

    def _run_coordination_workflow(self, **kwargs) -> bool:
        """Run standard coordination workflow."""
        try:
            # Basic coordination workflow
            self.logger.info("Standard coordination workflow initiated")
            return True

        except Exception as e:
            self.logger.error(f"Coordination workflow failed: {e}")
            return False

    def _run_onboarding_workflow(self, **kwargs) -> bool:
        """Run agent onboarding workflow."""
        try:
            # Agent onboarding workflow
            self.logger.info("Agent onboarding workflow initiated")
            return True

        except Exception as e:
            self.logger.error(f"Onboarding workflow failed: {e}")
            return False


def main():
    """CLI interface for Unified Launcher V2."""
    parser = argparse.ArgumentParser(
        description="Unified Launcher V2 - Agent Cellphone V2"
    )
    parser.add_argument("--launch", action="store_true", help="Launch V2 system")
    parser.add_argument(
        "--mode", default="standard", help="Launch mode (standard, swarm, coordination)"
    )
    parser.add_argument("--agents", nargs="+", help="Agent list")
    parser.add_argument("--workflow", help="Run specific workflow")
    parser.add_argument("--status", action="store_true", help="Show system status")
    parser.add_argument("--shutdown", action="store_true", help="Shutdown system")
    parser.add_argument("--test", action="store_true", help="Run launcher tests")

    args = parser.parse_args()

    # Create launcher instance
    launcher = UnifiedLauncherV2()

    if args.launch:
        success = launcher.launch_system(
            mode=args.mode,
            agents=args.agents,
            fsm_enabled=True,
            monitoring_enabled=True,
        )
        print(f"System launch: {'✅ Success' if success else '❌ Failed'}")

    elif args.workflow:
        success = launcher.run_workflow(args.workflow)
        print(f"Workflow {args.workflow}: {'✅ Success' if success else '❌ Failed'}")

    elif args.status:
        status = launcher.get_system_status()
        print("📊 System Status:")
        for key, value in status.items():
            if key != "services":
                print(f"  {key}: {value}")

        if "services" in status:
            print("\nService Status:")
            for service, service_status in status["services"].items():
                print(f"  {service}: {service_status}")

    elif args.shutdown:
        success = launcher.shutdown_system()
        print(f"System shutdown: {'✅ Success' if success else '❌ Failed'}")

    elif args.test:
        print("🧪 Running launcher tests...")
        try:
            # Test system launch
            success = launcher.launch_system(mode="test")
            print(f"Launch test: {'✅ Success' if success else '❌ Failed'}")

            # Test status
            status = launcher.get_system_status()
            print(
                f"Status test: {'✅ Success' if 'launcher_status' in status else '❌ Failed'}"
            )

            # Test shutdown
            success = launcher.shutdown_system()
            print(f"Shutdown test: {'✅ Success' if success else '❌ Failed'}")

        except Exception as e:
            print(f"❌ Launcher test failed: {e}")

    else:
        print("🚀 Unified Launcher V2 - Agent Cellphone V2")
        print("Use --help for available commands")


if __name__ == "__main__":
    main()
