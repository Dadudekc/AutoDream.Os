"""
launch_cross_system_communication_part_2.py
Module: launch_cross_system_communication_part_2.py
Purpose: Automated documentation compliance
Created: 2025-08-31 00:36:58
"""

# Part 2 of launch_cross_system_communication.py
# Original file: .\scripts\launchers\launch_cross_system_communication.py

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
                CrossSystemMessage,
                MessageType,
                UnifiedMessagePriority,
            )

            test_message = CrossSystemMessage(
                message_id=f"test_msg_{int(time.time())}",
                source_system="launcher",
                target_system=target_system,
                message_type=MessageType(message_type),
                priority=UnifiedMessagePriority.NORMAL,
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
        default="config/system/communication.json",
        help="Configuration file path",
    )

    parser.add_argument("--suite", "-s", help="Test suite name (for test action)")

    parser.add_argument(
        "--system",
        "-sys",
        help="System ID (for connect/disconnect/send-message actions)",
    )

    parser.add_argument(

