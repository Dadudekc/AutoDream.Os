"""
run_unified_portal_part_4.py
Module: run_unified_portal_part_4.py
Purpose: Automated documentation compliance
Created: 2025-08-31 00:37:00
"""

# Part 4 of run_unified_portal.py
# Original file: .\scripts\launchers\run_unified_portal.py

            logger.error(f"Error creating portal: {e}")
            raise

    def launch_portal(
        """
        launch_portal
        
        Purpose: Automated function documentation
        """
        self,
        backend_type: str = "flask",
        host: str = None,
        port: int = None,
        reload: bool = None,
    ):
        """Launch the portal with specified settings"""
        try:
            # Create portal
            portal = self.create_portal(backend_type)

            # Get server configuration
            server_config = self.config.get("server", {})
            host = host or server_config.get("host", "0.0.0.0")
            port = port or server_config.get("port", 5000)
            reload = reload if reload is not None else server_config.get("reload", True)

            logger.info(f"Launching {backend_type.upper()} portal on {host}:{port}")
            logger.info(f"Portal URL: http://{host}:{port}")
            logger.info(f"Agent Dashboard: http://{host}:{port}/dashboard")
            logger.info(f"API Documentation: http://{host}:{port}/docs")

            # Launch portal
            if hasattr(portal, "run"):
                portal.run(host=host, port=port, reload=reload)
            else:
                logger.error(
                    f"Portal object does not have a 'run' method: {type(portal)}"
                )

        except Exception as e:
            logger.error(f"Error launching portal: {e}")
            raise

    def show_status(self):
        """Show portal and agent status"""
        if not self.portal:
            logger.info("Portal not created yet. Use 'launch' command first.")
            return

        try:
            # Get portal stats
            if hasattr(self.portal, "portal") and hasattr(
                self.portal.portal, "get_portal_stats"
            ):
                stats = self.portal.portal.get_portal_stats()

