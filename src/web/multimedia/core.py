"""
Multimedia Core Service
Agent_Cellphone_V2_Repository TDD Integration Project

Core multimedia processing service that integrates with existing web infrastructure
"""

import os
import sys
import logging
import threading
import time

from src.utils.stability_improvements import stability_manager, safe_import
from typing import Dict, List, Any, Optional, Callable
from pathlib import Path
import cv2
import numpy as np
from PIL import Image

# Import existing web services
try:
    from ..health_monitor_web import HealthMonitorWeb
    from ..frontend.frontend_app import FrontendApp

    logger = logging.getLogger(__name__)
except ImportError as e:
    print(f"⚠️ Warning: Some web services could not be imported: {e}")

    # Create mock services for basic functionality
    class MockService:
        def __init__(self, name):
            self.name = name

        def __getattr__(self, name):
            return lambda *args, **kwargs: None

    HealthMonitorWeb = MockService("HealthMonitorWeb")
    FrontendApp = MockService("FrontendApp")
    logger = logging.getLogger(__name__)


class MultimediaCore:
    """
    Core multimedia processing service that integrates with existing web infrastructure
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or self._default_config()
        self.is_running = False
        self.processing_threads = {}
        self.active_filters = {}
        self.performance_metrics = {}

        # Initialize multimedia processing capabilities
        self._initialize_processing_capabilities()

        # Connect to existing web services
        self._connect_web_services()

        logger.info("🎬 Multimedia Core Service initialized successfully")

    def _default_config(self) -> Dict[str, Any]:
        """Default configuration for multimedia processing"""
        return {
            "max_threads": 4,
            "frame_rate": 30,
            "resolution": (640, 480),
            "quality": "high",
            "enable_gpu": False,
            "temp_directory": "/tmp/multimedia",
            "log_level": "INFO",
        }

    def _initialize_processing_capabilities(self):
        """Initialize multimedia processing capabilities"""
        try:
            # Check OpenCV availability
            cv2_version = cv2.__version__
            logger.info(f"✅ OpenCV {cv2_version} available")

            # Check PyQt5 availability
            try:
                import PyQt5

                logger.info("✅ PyQt5 available for GUI components")
            except ImportError:
                logger.warning("⚠️ PyQt5 not available - GUI features disabled")

            # Check FFmpeg availability
            try:
                import ffmpeg

                logger.info("✅ FFmpeg Python bindings available")
            except ImportError:
                logger.warning("⚠️ FFmpeg Python bindings not available")

            # Create temp directory
            temp_dir = Path(self.config["temp_directory"])
            temp_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"✅ Temporary directory created: {temp_dir}")

        except Exception as e:
            logger.error(f"❌ Failed to initialize processing capabilities: {e}")
            raise

    def _connect_web_services(self):
        """Connect to existing web services"""
        try:
            # Connect to health monitor
            self.health_monitor = HealthMonitorWeb()
            logger.info("✅ Connected to Health Monitor Web Service")

            # Connect to frontend app
            self.frontend_app = FrontendApp()
            logger.info("✅ Connected to Frontend App Service")

        except Exception as e:
            logger.warning(f"⚠️ Could not connect to all web services: {e}")

    def start_processing(self) -> bool:
        """Start multimedia processing service"""
        if self.is_running:
            logger.warning("⚠️ Multimedia processing already running")
            return False

        try:
            self.is_running = True
            logger.info("🎬 Starting multimedia processing service...")

            # Start performance monitoring thread
            self._start_performance_monitoring()

            logger.info("✅ Multimedia processing service started successfully")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to start multimedia processing: {e}")
            self.is_running = False
            return False

    def stop_processing(self) -> bool:
        """Stop multimedia processing service"""
        if not self.is_running:
            logger.warning("⚠️ Multimedia processing not running")
            return False

        try:
            logger.info("🛑 Stopping multimedia processing service...")

            # Stop all processing threads
            for thread_name, thread in self.processing_threads.items():
                if thread.is_alive():
                    thread.join(timeout=5.0)
                    logger.info(f"✅ Stopped thread: {thread_name}")

            # Stop performance monitoring
            self._stop_performance_monitoring()

            self.is_running = False
            logger.info("✅ Multimedia processing service stopped successfully")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to stop multimedia processing: {e}")
            return False

    def _start_performance_monitoring(self):
        """Start performance monitoring thread"""

        def monitor_performance():
            while self.is_running:
                try:
                    # Collect performance metrics
                    self.performance_metrics = {
                        "active_threads": len(
                            [
                                t
                                for t in self.processing_threads.values()
                                if t.is_alive()
                            ]
                        ),
                        "active_filters": len(self.active_filters),
                        "memory_usage": self._get_memory_usage(),
                        "cpu_usage": self._get_cpu_usage(),
                        "timestamp": time.time(),
                    }

                    # Report to health monitor if available
                    if hasattr(self, "health_monitor"):
                        try:
                            self.health_monitor.report_multimedia_health(
                                self.performance_metrics
                            )
                        except:
                            pass

                    time.sleep(5)  # Update every 5 seconds

                except Exception as e:
                    logger.error(f"❌ Performance monitoring error: {e}")
                    time.sleep(10)  # Wait longer on error

        monitor_thread = threading.Thread(target=monitor_performance, daemon=True)
        monitor_thread.start()
        self.processing_threads["performance_monitor"] = monitor_thread

    def _stop_performance_monitoring(self):
        """Stop performance monitoring"""
        if "performance_monitor" in self.processing_threads:
            thread = self.processing_threads["performance_monitor"]
            if thread.is_alive():
                thread.join(timeout=5.0)

    def _get_memory_usage(self) -> float:
        """Get current memory usage in MB"""
        try:
            import psutil

            process = psutil.Process()
            return process.memory_info().rss / 1024 / 1024  # Convert to MB
        except ImportError:
            return 0.0

    def _get_cpu_usage(self) -> float:
        """Get current CPU usage percentage"""
        try:
            import psutil

            return psutil.cpu_percent(interval=1)
        except ImportError:
            return 0.0

    def get_status(self) -> Dict[str, Any]:
        """Get current service status"""
        return {
            "is_running": self.is_running,
            "active_threads": len(
                [t for t in self.processing_threads.values() if t.is_alive()]
            ),
            "active_filters": len(self.active_filters),
            "performance_metrics": self.performance_metrics,
            "config": self.config,
        }

    def health_check(self) -> Dict[str, Any]:
        """Perform health check of multimedia services"""
        health_status = {"status": "healthy", "timestamp": time.time(), "checks": {}}

        try:
            # Check OpenCV
            cv2_version = cv2.__version__
            health_status["checks"]["opencv"] = {
                "status": "healthy",
                "version": cv2_version,
            }
        except Exception as e:
            health_status["checks"]["opencv"] = {"status": "unhealthy", "error": str(e)}
            health_status["status"] = "degraded"

        # Check PyQt5
        try:
            import PyQt5

            health_status["checks"]["pyqt5"] = {
                "status": "healthy",
                "version": PyQt5.QtCore.QT_VERSION_STR,
            }
        except Exception as e:
            health_status["checks"]["pyqt5"] = {"status": "unhealthy", "error": str(e)}
            health_status["status"] = "degraded"

        # Check FFmpeg
        try:
            import ffmpeg

            health_status["checks"]["ffmpeg"] = {"status": "healthy"}
        except Exception as e:
            health_status["checks"]["ffmpeg"] = {"status": "unhealthy", "error": str(e)}
            health_status["status"] = "degraded"

        return health_status
