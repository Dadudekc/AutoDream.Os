#!/usr/bin/env python3
"""
Integration Infrastructure Launcher
Launches and manages the integration infrastructure for Agent_Cellphone_V2_Repository.
"""

import argparse
import asyncio
import json
import logging
import os
import signal
import sys
import time

from src.utils.stability_improvements import stability_manager, safe_import
from pathlib import Path
from typing import Dict, Any, Optional

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from services.integration_coordinator import IntegrationCoordinator
from services.api_manager import APIManager
from services.middleware_tools import MessageQueue, CacheManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("logs/integration_launcher.log"),
    ],
)
logger = logging.getLogger(__name__)


class IntegrationInfrastructureLauncher:
    """Launcher for the integration infrastructure."""

    def __init__(self, config_path: str = "config/system/integration.json"):
        self.config_path = config_path
        self.config = self._load_config()
        self.coordinator: Optional[IntegrationCoordinator] = None
        self.running = False
        self.shutdown_event = asyncio.Event()

        # Setup signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file."""
        try:
            config_file = Path(self.config_path)
            if not config_file.exists():
                logger.warning(
                    f"Config file {self.config_path} not found, using defaults"
                )
                return self._get_default_config()

            with open(config_file, "r") as f:
                config = json.load(f)

            logger.info(f"Configuration loaded from {self.config_path}")
            return config.get("integration_infrastructure", {})

        except Exception as e:
            logger.error(f"Failed to load configuration: {str(e)}")
            logger.info("Using default configuration")
            return self._get_default_config()

    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration."""
        return {
            "api_management": {"enabled": True},
            "message_queue": {"enabled": True},
            "caching": {"enabled": True},
            "circuit_breaker": {"enabled": True},
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

            # Register additional services if configured
            await self._register_additional_services()

            # Start monitoring loop
            await self._monitoring_loop()

        except Exception as e:
            logger.error(f"Failed to start integration infrastructure: {str(e)}")
            self.running = False
            raise

    async def _register_additional_services(self):
        """Register additional services based on configuration."""
        try:
            # Register external API services if configured
            external_apis = self.config.get("integration_points", {}).get(
                "external_apis", {}
            )
            if external_apis.get("enabled", False):
                for endpoint in external_apis.get("endpoints", []):
                    self.coordinator.register_service(
                        f"external_api_{endpoint['name']}",
                        {
                            "type": "external_api",
                            "endpoint": endpoint["url"],
                            "authentication": endpoint.get("authentication", {}),
                            "rate_limiting": endpoint.get("rate_limiting", {}),
                        },
                    )
                    logger.info(f"Registered external API service: {endpoint['name']}")

            # Register database services if configured
            databases = self.config.get("integration_points", {}).get("databases", {})
            if databases.get("enabled", False):
                for db in databases.get("connections", []):
                    self.coordinator.register_service(
                        f"database_{db['name']}",
                        {
                            "type": "database",
                            "connection_string": db["connection_string"],
                            "pool_size": db.get("pool_size", 10),
                        },
                    )
                    logger.info(f"Registered database service: {db['name']}")

            # Register message broker services if configured
            message_brokers = self.config.get("integration_points", {}).get(
                "message_brokers", {}
            )
            if message_brokers.get("enabled", False):
                for broker in message_brokers.get("brokers", []):
                    self.coordinator.register_service(
                        f"message_broker_{broker['name']}",
                        {
                            "type": "message_broker",
                            "broker_url": broker["url"],
                            "topics": broker.get("topics", []),
                            "consumer_groups": broker.get("consumer_groups", []),
                        },
                    )
                    logger.info(f"Registered message broker service: {broker['name']}")

        except Exception as e:
            logger.error(f"Failed to register additional services: {str(e)}")

    async def _monitoring_loop(self):
        """Main monitoring loop."""
        logger.info("Starting monitoring loop...")

        while not self.shutdown_event.is_set():
            try:
                if self.coordinator and self.coordinator.running:
                    # Get system status
                    status = self.coordinator.get_integration_status()

                    # Log status periodically
                    if int(time.time()) % 60 == 0:  # Every minute
                        logger.info(f"System status: {status['running']}")

                        # Check for any unhealthy services
                        health = await self.coordinator.get_system_health()
                        unhealthy_services = [
                            name
                            for name, service_health in health.items()
                            if service_health.status != "healthy"
                        ]

                        if unhealthy_services:
                            logger.warning(
                                f"Unhealthy services detected: {unhealthy_services}"
                            )

                    # Wait before next check
                    await asyncio.sleep(10)
                else:
                    logger.error("Coordinator is not running, exiting monitoring loop")
                    break

            except Exception as e:
                logger.error(f"Error in monitoring loop: {str(e)}")
                await asyncio.sleep(5)

        logger.info("Monitoring loop stopped")

    async def stop(self):
        """Stop the integration infrastructure."""
        if not self.running:
            logger.warning("Integration infrastructure is not running")
            return

        try:
            logger.info("Stopping integration infrastructure...")

            # Set shutdown event
            self.shutdown_event.set()

            # Stop coordinator
            if self.coordinator:
                self.coordinator.stop()
                self.coordinator = None

            self.running = False
            logger.info("Integration infrastructure stopped successfully")

        except Exception as e:
            logger.error(f"Failed to stop integration infrastructure: {str(e)}")
            raise

    async def restart(self):
        """Restart the integration infrastructure."""
        logger.info("Restarting integration infrastructure...")
        await self.stop()
        await asyncio.sleep(2)  # Wait a bit before restarting
        await self.start()

    def get_status(self) -> Dict[str, Any]:
        """Get current status of the integration infrastructure."""
        if not self.coordinator:
            return {
                "running": False,
                "coordinator": None,
                "config_loaded": bool(self.config),
            }

        return {
            "running": self.running,
            "coordinator_status": self.coordinator.get_integration_status(),
            "config_loaded": bool(self.config),
            "config_path": self.config_path,
        }

    async def health_check(self) -> bool:
        """Perform health check on the integration infrastructure."""
        if not self.coordinator or not self.coordinator.running:
            return False

        try:
            health = await self.coordinator.get_system_health()
            all_healthy = all(
                service_health.status == "healthy" for service_health in health.values()
            )
            return all_healthy
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return False


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Integration Infrastructure Launcher")
    parser.add_argument(
        "--config",
        "-c",
        default="config/system/integration.json",
        help="Path to configuration file",
    )
    parser.add_argument(
        "--action",
        "-a",
        choices=["start", "stop", "restart", "status", "health"],
        default="start",
        help="Action to perform",
    )
    parser.add_argument(
        "--daemon", "-d", action="store_true", help="Run in daemon mode"
    )
    parser.add_argument(
        "--log-level",
        "-l",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Log level",
    )

    args = parser.parse_args()

    # Set log level
    logging.getLogger().setLevel(getattr(logging, args.log_level.upper()))

    # Create launcher
    launcher = IntegrationInfrastructureLauncher(args.config)

    try:
        if args.action == "start":
            if args.daemon:
                logger.info("Starting integration infrastructure in daemon mode...")
                # In a real implementation, you would daemonize here
                await launcher.start()

                # Keep running until shutdown signal
                await launcher.shutdown_event.wait()
            else:
                await launcher.start()
                logger.info("Integration infrastructure started. Press Ctrl+C to stop.")

                # Keep running until shutdown signal
                await launcher.shutdown_event.wait()

        elif args.action == "stop":
            await launcher.stop()

        elif args.action == "restart":
            await launcher.restart()

        elif args.action == "status":
            status = launcher.get_status()
            print(json.dumps(status, indent=2, default=str))

        elif args.action == "health":
            is_healthy = await launcher.health_check()
            print(f"Health check result: {'HEALTHY' if is_healthy else 'UNHEALTHY'}")
            sys.exit(0 if is_healthy else 1)

    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt, shutting down...")
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        sys.exit(1)
    finally:
        if launcher.running:
            await launcher.stop()


if __name__ == "__main__":
    # Ensure logs directory exists
    os.makedirs("logs", exist_ok=True)

    # Run the launcher
    asyncio.run(main())
