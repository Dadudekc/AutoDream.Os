"""
launch_performance_core.py
Module: launch_performance_core.py
Purpose: Automated documentation compliance
Created: 2025-08-31 00:37:02
"""

# Performance optimized version of launch_performance_core.py
# Original file: .\scripts\launchers\launch_performance_core.py

import asyncio, logging, signal, time
from typing import Optional
from launch_performance_config import load_config


    setup_performance_monitor,
    setup_alerting_system,
    setup_dashboard,
)
    print_startup_summary,
    get_system_status as validator_get_system_status,
    get_health_status as validator_get_health_status,
)

logger = logging.getLogger(__name__)


class PerformanceMonitoringLauncher:
    """Main launcher for the performance monitoring system."""

    def __init__(self, config_file: str = "config/system/performance.json"):
        """
        __init__
        
        Purpose: Automated function documentation
        """
        self.config_file = config_file
        self.config = {}
        self.performance_monitor: Optional[PerformanceMonitor] = None
        self.dashboard_backend: Optional[DashboardBackend] = None
        self.dashboard_frontend: Optional[DashboardFrontend] = None
        self.alerting_system: Optional[AlertingSystem] = None
        self.running = False
        self.startup_time = time.time()
        self.shutdown_event = asyncio.Event()
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        logger.info("Performance monitoring launcher initialized")

    def _signal_handler(self, signum, frame):
        """
        _signal_handler
        
        Purpose: Automated function documentation
        """
        logger.info("Received signal %s, initiating graceful shutdown", signum)
        self.shutdown_event.set()

    def load_config(self) -> bool:
        """
        load_config
        
        Purpose: Automated function documentation
        """
        config = load_config(self.config_file)
        if config is None:
            return False
        self.config = config
        return True

    def setup_performance_monitor(self) -> bool:
        """
        setup_performance_monitor
        
        Purpose: Automated function documentation
        """
        self.performance_monitor = setup_performance_monitor(self.config, self.config_file)
        return self.performance_monitor is not None

    def setup_alerting_system(self) -> bool:
        """
        setup_alerting_system
        
        Purpose: Automated function documentation
        """
        self.alerting_system = setup_alerting_system(self.performance_monitor, self.config)
        return True if self.alerting_system or not self.config.get("performance_monitoring", {}).get("alerting", {}).get("enabled", True) else False

    def setup_dashboard(self) -> bool:
        """
        setup_dashboard
        
        Purpose: Automated function documentation
        """
        self.dashboard_backend, self.dashboard_frontend = setup_dashboard(
            self.performance_monitor, self.config
        )
        return True if (self.dashboard_backend or self.dashboard_frontend or not self.config.get("performance_monitoring", {}).get("dashboard", {}).get("enabled", True)) else False

    async def start_system(self) -> bool:
        try:
            if self.performance_monitor:
                await self.performance_monitor.start()
                logger.info("Performance monitor started")
            if self.dashboard_backend:
                await self.dashboard_backend.start()
                logger.info("Dashboard backend started")
            self.running = True
            print_startup_summary(self)
            return True
        except Exception as e:
            logger.error("Failed to start system: %s", e)
            return False

    async def stop_system(self):
        try:
            self.running = False
            if self.performance_monitor:
                await self.performance_monitor.stop()
                logger.info("Performance monitor stopped")
            if self.dashboard_backend:
                await self.dashboard_backend.stop()
                logger.info("Dashboard backend stopped")
        except Exception as e:
            logger.error("Error stopping system: %s", e)

    def get_system_status(self) -> dict:
        """
        get_system_status
        
        Purpose: Automated function documentation
        """
        return validator_get_system_status(self)

    def get_health_status(self) -> dict:
        """
        get_health_status
        
        Purpose: Automated function documentation
        """
        return validator_get_health_status(self)

    async def run_main_loop(self):
        try:
            await self.shutdown_event.wait()
        finally:
            await self.stop_system()


