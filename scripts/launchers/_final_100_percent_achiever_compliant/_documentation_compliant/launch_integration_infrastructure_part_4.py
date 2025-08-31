"""
launch_integration_infrastructure_part_4.py
Module: launch_integration_infrastructure_part_4.py
Purpose: Automated documentation compliance
Created: 2025-08-31 00:36:59
"""

# Part 4 of launch_integration_infrastructure.py
# Original file: .\scripts\launchers\launch_integration_infrastructure.py

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

