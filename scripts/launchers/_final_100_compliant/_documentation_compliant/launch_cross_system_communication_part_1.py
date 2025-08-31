"""
launch_cross_system_communication_part_1.py
Module: launch_cross_system_communication_part_1.py
Purpose: Automated documentation compliance
Created: 2025-08-31 00:36:58
"""

# Part 1 of launch_cross_system_communication.py
# Original file: .\scripts\launchers\launch_cross_system_communication.py


            # Initialize communication manager
            self.communication_manager = CrossSystemCommunicationManager()

            # Load system endpoints from config
            await self._load_system_endpoints()

            # Initialize integration coordinator
            self.integration_coordinator = IntegrationCoordinator()

            # Initialize test runner
            self.test_runner = TestExecutor()
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

                suite = TestOrchestrator(
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
                        ServiceIntegrationTester("test_system_connections")
                    )
                    suite.add_test(ServiceIntegrationTester("test_message_routing"))
                    suite.add_test(
                        ServiceIntegrationTester("test_protocol_handling")
                    )

                elif suite_name == "api_integration":
                    suite.add_test(ServiceIntegrationTester("test_endpoint_registration"))
                    suite.add_test(ServiceIntegrationTester("test_request_handling"))
                    suite.add_test(ServiceIntegrationTester("test_response_validation"))

                elif suite_name == "middleware_integration":
                    suite.add_test(ServiceIntegrationTester("test_middleware_chains"))
                    suite.add_test(
                        ServiceIntegrationTester("test_data_transformation")
                    )
                    suite.add_test(ServiceIntegrationTester("test_validation_rules"))

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


