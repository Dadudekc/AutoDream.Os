#!/usr/bin/env python3
"""
Cross-System Communication and Integration Testing Launcher
Launches and manages the cross-system communication infrastructure and integration testing.
"""

import argparse
import asyncio
import json
import logging
import signal
import sys
import time
from pathlib import Path
from typing import Dict, Any, Optional

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from services.cross_system_communication import (
    CrossSystemCommunicationManager,
    SystemEndpoint,
    CommunicationProtocol,
)
from services.integration_testing_framework import (
    IntegrationTestRunner,
    IntegrationTestSuite,
    CrossSystemCommunicationTest,
    APIIntegrationTest,
    MiddlewareIntegrationTest,
)
from services.integration_coordinator import IntegrationCoordinator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/cross_system_communication.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)


class CrossSystemCommunicationLauncher:
    """Launcher for cross-system communication and integration testing."""

    def __init__(
        self, config_path: str = "config/cross_system_communication_config.json"
    ):
        self.config_path = config_path
        self.config = self._load_config()
        self.communication_manager: Optional[CrossSystemCommunicationManager] = None
        self.test_runner: Optional[IntegrationTestRunner] = None
        self.integration_coordinator: Optional[IntegrationCoordinator] = None
        self.running = False

        # Setup signal handlers
        self._setup_signal_handlers()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file."""
        try:
            config_file = Path(self.config_path)
            if not config_file.exists():
                logger.error(f"Configuration file not found: {self.config_path}")
                sys.exit(1)

            with open(config_file, "r") as f:
                config = json.load(f)

            logger.info(f"Configuration loaded from: {self.config_path}")
            return config

        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            sys.exit(1)

    def _setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown."""

        def signal_handler(signum, frame):
            logger.info(f"Received signal {signum}, initiating graceful shutdown")
            asyncio.create_task(self.stop())

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

    async def start(self) -> bool:
        """Start the cross-system communication system."""
        if self.running:
            logger.warning("System is already running")
            return True

        try:
            logger.info("Starting cross-system communication system...")

            # Initialize communication manager
            self.communication_manager = CrossSystemCommunicationManager()

            # Load system endpoints from config
            await self._load_system_endpoints()

            # Initialize integration coordinator
            self.integration_coordinator = IntegrationCoordinator()

            # Initialize test runner
            self.test_runner = IntegrationTestRunner()
            await self._setup_test_suites()

            # Start communication manager
            await self.communication_manager.start()

            # Start integration coordinator
            await self.integration_coordinator.start()

            self.running = True
            logger.info("Cross-system communication system started successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to start system: {e}")
            return False

    async def _load_system_endpoints(self):
        """Load system endpoints from configuration."""
        try:
            systems_config = self.config.get("systems", {})

            for system_id, system_config in systems_config.items():
                # Convert protocol string to enum
                protocol_str = system_config.get("protocol", "http")
                try:
                    protocol = CommunicationProtocol(protocol_str)
                except ValueError:
                    logger.warning(
                        f"Invalid protocol '{protocol_str}' for system {system_id}, using HTTP"
                    )
                    protocol = CommunicationProtocol.HTTP

                # Create system endpoint
                endpoint = SystemEndpoint(
                    system_id=system_id,
                    name=system_config.get("name", system_id),
                    protocol=protocol,
                    host=system_config.get("host", "localhost"),
                    port=system_config.get("port", 80),
                    path=system_config.get("path", ""),
                    timeout=system_config.get("timeout", 30.0),
                    retry_attempts=system_config.get("retry_attempts", 3),
                    health_check_interval=system_config.get(
                        "health_check_interval", 60.0
                    ),
                    credentials=system_config.get("credentials"),
                    metadata=system_config.get("metadata", {}),
                )

                self.communication_manager.add_endpoint(endpoint)
                logger.info(
                    f"Added system endpoint: {system_id} ({protocol.value}://{endpoint.host}:{endpoint.port})"
                )

            logger.info(f"Loaded {len(systems_config)} system endpoints")

        except Exception as e:
            logger.error(f"Failed to load system endpoints: {e}")
            raise

    async def _setup_test_suites(self):
        """Setup integration test suites."""
        try:
            testing_config = self.config.get("integration_testing", {})
            test_suites_config = testing_config.get("test_suites", {})

            # Create test suites based on configuration
            for suite_name, suite_config in test_suites_config.items():
                if not suite_config.get("enabled", True):
                    continue

                suite = IntegrationTestSuite(
                    name=suite_name,
                    description=suite_config.get(
                        "description", f"Test suite for {suite_name}"
                    ),
                )

                # Configure suite options
                suite.parallel_execution = testing_config.get(
                    "parallel_execution", False
                )
                suite.max_parallel_tests = testing_config.get("max_parallel_tests", 5)
                suite.stop_on_failure = testing_config.get("stop_on_failure", False)
                suite.retry_failed_tests = testing_config.get(
                    "retry_failed_tests", False
                )
                suite.max_retries = testing_config.get("max_retries", 3)

                # Add tests based on suite type
                if suite_name == "cross_system_communication":
                    suite.add_test(
                        CrossSystemCommunicationTest("test_system_connections")
                    )
                    suite.add_test(CrossSystemCommunicationTest("test_message_routing"))
                    suite.add_test(
                        CrossSystemCommunicationTest("test_protocol_handling")
                    )

                elif suite_name == "api_integration":
                    suite.add_test(APIIntegrationTest("test_endpoint_registration"))
                    suite.add_test(APIIntegrationTest("test_request_handling"))
                    suite.add_test(APIIntegrationTest("test_response_validation"))

                elif suite_name == "middleware_integration":
                    suite.add_test(MiddlewareIntegrationTest("test_middleware_chains"))
                    suite.add_test(
                        MiddlewareIntegrationTest("test_data_transformation")
                    )
                    suite.add_test(MiddlewareIntegrationTest("test_validation_rules"))

                # Add suite to test runner
                self.test_runner.add_test_suite(suite)
                logger.info(f"Added test suite: {suite_name}")

            logger.info(f"Setup {len(test_suites_config)} test suites")

        except Exception as e:
            logger.error(f"Failed to setup test suites: {e}")
            raise

    async def stop(self) -> bool:
        """Stop the cross-system communication system."""
        if not self.running:
            return True

        try:
            logger.info("Stopping cross-system communication system...")

            # Stop test runner
            if self.test_runner:
                # Test runner doesn't have a stop method, just clear suites
                self.test_runner.test_suites.clear()

            # Stop integration coordinator
            if self.integration_coordinator:
                await self.integration_coordinator.stop()

            # Stop communication manager
            if self.communication_manager:
                await self.communication_manager.stop()

            self.running = False
            logger.info("Cross-system communication system stopped successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to stop system: {e}")
            return False

    async def get_status(self) -> Dict[str, Any]:
        """Get system status."""
        status = {"running": self.running, "timestamp": time.time()}

        if self.communication_manager:
            status["communication_manager"] = {
                "endpoints": len(self.communication_manager.endpoints),
                "connected_systems": len(self.communication_manager.handlers),
                "system_status": self.communication_manager.get_system_status(),
                "metrics": self.communication_manager.get_metrics().__dict__,
            }

        if self.test_runner:
            status["test_runner"] = self.test_runner.get_global_summary()

        if self.integration_coordinator:
            status["integration_coordinator"] = {
                "status": self.integration_coordinator.status.value,
                "metrics": self.integration_coordinator.metrics.__dict__,
            }

        return status

    async def run_tests(self, suite_name: Optional[str] = None) -> Dict[str, Any]:
        """Run integration tests."""
        if not self.test_runner:
            return {"error": "Test runner not initialized"}

        try:
            if suite_name:
                logger.info(f"Running test suite: {suite_name}")
                results = await self.test_runner.run_specific_suite(suite_name)
                return {
                    "suite_name": suite_name,
                    "results": results if results else [],
                    "success": results is not None,
                }
            else:
                logger.info("Running all test suites")
                results = await self.test_runner.run_all_suites()
                return {"all_suites": True, "results": results, "success": True}

        except Exception as e:
            logger.error(f"Failed to run tests: {e}")
            return {"error": str(e), "success": False}

    async def connect_system(self, system_id: str) -> bool:
        """Connect to a specific system."""
        if not self.communication_manager:
            return False

        try:
            logger.info(f"Connecting to system: {system_id}")
            return await self.communication_manager.connect_system(system_id)
        except Exception as e:
            logger.error(f"Failed to connect to system {system_id}: {e}")
            return False

    async def disconnect_system(self, system_id: str) -> bool:
        """Disconnect from a specific system."""
        if not self.communication_manager:
            return False

        try:
            logger.info(f"Disconnecting from system: {system_id}")
            return await self.communication_manager.disconnect_system(system_id)
        except Exception as e:
            logger.error(f"Failed to disconnect from system {system_id}: {e}")
            return False

    async def send_test_message(
        self, target_system: str, message_type: str = "request"
    ) -> bool:
        """Send a test message to a system."""
        if not self.communication_manager:
            return False

        try:
            from services.cross_system_communication import (
                CrossSystemMessage,
                MessageType,
                MessagePriority,
            )

            test_message = CrossSystemMessage(
                message_id=f"test_msg_{int(time.time())}",
                source_system="launcher",
                target_system=target_system,
                message_type=MessageType(message_type),
                priority=MessagePriority.NORMAL,
                timestamp=time.time(),
                payload={"test": True, "timestamp": time.time(), "source": "launcher"},
            )

            logger.info(f"Sending test message to {target_system}")
            return await self.communication_manager.send_message(test_message)

        except Exception as e:
            logger.error(f"Failed to send test message: {e}")
            return False


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Cross-System Communication and Integration Testing Launcher"
    )

    parser.add_argument(
        "action",
        choices=[
            "start",
            "stop",
            "restart",
            "status",
            "test",
            "connect",
            "disconnect",
            "send-message",
        ],
        help="Action to perform",
    )

    parser.add_argument(
        "--config",
        "-c",
        default="config/cross_system_communication_config.json",
        help="Configuration file path",
    )

    parser.add_argument("--suite", "-s", help="Test suite name (for test action)")

    parser.add_argument(
        "--system",
        "-sys",
        help="System ID (for connect/disconnect/send-message actions)",
    )

    parser.add_argument(
        "--message-type",
        "-mt",
        default="request",
        choices=[
            "request",
            "response",
            "event",
            "command",
            "query",
            "notification",
            "heartbeat",
        ],
        help="Message type for send-message action",
    )

    parser.add_argument(
        "--timeout",
        "-t",
        type=int,
        default=300,
        help="Timeout in seconds for test execution",
    )

    args = parser.parse_args()

    # Create launcher
    launcher = CrossSystemCommunicationLauncher(args.config)

    try:
        if args.action == "start":
            success = await launcher.start()
            if success:
                logger.info("System started successfully")
                # Keep running until interrupted
                while launcher.running:
                    await asyncio.sleep(1)
            else:
                logger.error("Failed to start system")
                sys.exit(1)

        elif args.action == "stop":
            success = await launcher.stop()
            if success:
                logger.info("System stopped successfully")
            else:
                logger.error("Failed to stop system")
                sys.exit(1)

        elif args.action == "restart":
            await launcher.stop()
            await asyncio.sleep(2)
            success = await launcher.start()
            if success:
                logger.info("System restarted successfully")
            else:
                logger.error("Failed to restart system")
                sys.exit(1)

        elif args.action == "status":
            status = await launcher.get_status()
            print(json.dumps(status, indent=2, default=str))

        elif args.action == "test":
            if args.suite:
                results = await launcher.run_tests(args.suite)
            else:
                results = await launcher.run_tests()
            print(json.dumps(results, indent=2, default=str))

        elif args.action == "connect":
            if not args.system:
                logger.error("System ID required for connect action")
                sys.exit(1)
            success = await launcher.connect_system(args.system)
            if success:
                logger.info(f"Connected to system: {args.system}")
            else:
                logger.error(f"Failed to connect to system: {args.system}")
                sys.exit(1)

        elif args.action == "disconnect":
            if not args.system:
                logger.error("System ID required for disconnect action")
                sys.exit(1)
            success = await launcher.disconnect_system(args.system)
            if success:
                logger.info(f"Disconnected from system: {args.system}")
            else:
                logger.error(f"Failed to disconnect from system: {args.system}")
                sys.exit(1)

        elif args.action == "send-message":
            if not args.system:
                logger.error("System ID required for send-message action")
                sys.exit(1)
            success = await launcher.send_test_message(args.system, args.message_type)
            if success:
                logger.info(f"Test message sent to system: {args.system}")
            else:
                logger.error(f"Failed to send test message to system: {args.system}")
                sys.exit(1)

    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt, shutting down...")
        await launcher.stop()
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        await launcher.stop()
        sys.exit(1)


if __name__ == "__main__":
    # Ensure logs directory exists
    Path("logs").mkdir(exist_ok=True)

    # Run the launcher
    asyncio.run(main())
