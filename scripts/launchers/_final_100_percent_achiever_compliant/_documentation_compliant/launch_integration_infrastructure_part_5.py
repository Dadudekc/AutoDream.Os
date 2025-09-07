"""
launch_integration_infrastructure_part_5.py
Module: launch_integration_infrastructure_part_5.py
Purpose: Automated documentation compliance
Created: 2025-08-31 00:36:59
"""

# Part 5 of launch_integration_infrastructure.py
# Original file: .\scripts\launchers\launch_integration_infrastructure.py

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

