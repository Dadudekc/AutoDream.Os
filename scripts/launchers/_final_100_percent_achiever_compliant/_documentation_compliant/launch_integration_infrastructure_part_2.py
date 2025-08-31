"""
launch_integration_infrastructure_part_2.py
Module: launch_integration_infrastructure_part_2.py
Purpose: Automated documentation compliance
Created: 2025-08-31 00:36:59
"""

# Part 2 of launch_integration_infrastructure.py
# Original file: .\scripts\launchers\launch_integration_infrastructure.py

            "retry_enabled": True,
            "max_workers": 10,
            "health_check_interval": 30,
            "log_level": "INFO",
        }

    def _create_integration_config(self) -> Dict[str, Any]:
        """Create configuration dictionary from loaded configuration."""
        config = self.config

        return {
            "api_enabled": config.get("api_management", {}).get("enabled", True),
            "message_queue_enabled": config.get("message_queue", {}).get(
                "enabled", True
            ),
            "caching_enabled": config.get("caching", {}).get("enabled", True),
            "circuit_breaker_enabled": config.get("circuit_breaker", {}).get(
                "enabled", True
            ),
            "retry_enabled": config.get("retry_middleware", {}).get("enabled", True),
            "max_workers": config.get("performance", {}).get("max_workers", 10),
            "health_check_interval": config.get("service_registry", {}).get(
                "health_check_interval", 30
            ),
            "log_level": config.get("logging_config", {}).get("level", "INFO"),
        }

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        logger.info(f"Received signal {signum}, initiating shutdown...")
        self.shutdown_event.set()

    async def start(self):
        """Start the integration infrastructure."""
        if self.running:
            logger.warning("Integration infrastructure is already running")
            return

        try:
            logger.info("Starting integration infrastructure...")

            # Create and start coordinator
            integration_config = self._create_integration_config()
            self.coordinator = IntegrationCoordinator()

            # Start the coordinator
            self.coordinator.start()
            self.running = True

            logger.info("Integration infrastructure started successfully")

