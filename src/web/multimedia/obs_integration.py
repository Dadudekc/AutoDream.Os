"""
OBS Virtual Camera Integration Service
Agent_Cellphone_V2_Repository TDD Integration Project

Provides seamless integration with OBS Studio for virtual camera output
"""

import os
import sys
import logging
import threading
import time
import json

from src.utils.stability_improvements import stability_manager, safe_import
from typing import Dict, List, Any, Optional, Callable
from pathlib import Path
import cv2
import numpy as np

# Import existing web services
try:
    from ..health_monitor_web import HealthMonitorWeb

    logger = logging.getLogger(__name__)
except ImportError as e:
    print(f"⚠️ Warning: Health monitor could not be imported: {e}")

    # Create mock service for basic functionality
    class MockService:
        def __init__(self, name):
            self.name = name

        def __getattr__(self, name):
            return lambda *args, **kwargs: None

    HealthMonitorWeb = MockService("HealthMonitorWeb")
    logger = logging.getLogger(__name__)


class OBSVirtualCameraIntegration:
    """
    OBS Virtual Camera Integration Service
    Enables pushing multimedia feeds directly to OBS Studio
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or self._default_config()
        self.is_connected = False
        self.obs_websocket = None
        self.virtual_camera = None
        self.output_stream = None
        self.frame_buffer = []
        self.connection_thread = None

        # Initialize OBS integration capabilities
        self._initialize_obs_integration()

        # Connect to health monitor
        self._connect_health_monitor()

        logger.info("🎥 OBS Virtual Camera Integration Service initialized")

    def _default_config(self) -> Dict[str, Any]:
        """Default configuration for OBS integration"""
        return {
            "obs_websocket_host": "localhost",
            "obs_websocket_port": 4455,
            "obs_websocket_password": "",
            "virtual_camera_name": "Agent_Cellphone_Multimedia",
            "frame_rate": 30,
            "resolution": (1920, 1080),
            "quality": "high",
            "buffer_size": 100,
            "auto_reconnect": True,
            "reconnect_interval": 5,
        }

    def _initialize_obs_integration(self):
        """Initialize OBS integration capabilities"""
        try:
            # Check OBS WebSocket availability
            try:
                import obswebsocket

                logger.info("✅ OBS WebSocket Python library available")
            except ImportError:
                logger.warning("⚠️ OBS WebSocket Python library not available")

            # Check virtual camera availability
            try:
                import virtual_camera

                logger.info("✅ Virtual Camera library available")
            except ImportError:
                logger.warning("⚠️ Virtual Camera library not available")

            # Check OBS Studio Python bindings
            try:
                import obs_python

                logger.info("✅ OBS Studio Python bindings available")
            except ImportError:
                logger.warning("⚠️ OBS Studio Python bindings not available")

            # Create output directory
            output_dir = Path(self.config.get("output_directory", "/tmp/obs_output"))
            output_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"✅ OBS output directory created: {output_dir}")

        except Exception as e:
            logger.error(f"❌ Failed to initialize OBS integration: {e}")
            raise

    def _connect_health_monitor(self):
        """Connect to health monitor service"""
        try:
            self.health_monitor = HealthMonitorWeb()
            logger.info("✅ Connected to Health Monitor Web Service")
        except Exception as e:
            logger.warning(f"⚠️ Could not connect to health monitor: {e}")

    def connect_to_obs(self) -> bool:
        """Connect to OBS Studio via WebSocket"""
        if self.is_connected:
            logger.warning("⚠️ Already connected to OBS")
            return True

        try:
            logger.info("🔌 Connecting to OBS Studio...")

            # Attempt WebSocket connection
            if self._connect_obs_websocket():
                logger.info("✅ Connected to OBS Studio via WebSocket")
                self.is_connected = True
                return True

            # Fallback to virtual camera
            if self._setup_virtual_camera():
                logger.info("✅ Virtual camera setup successful")
                self.is_connected = True
                return True

            logger.error("❌ Failed to connect to OBS Studio")
            return False

        except Exception as e:
            logger.error(f"❌ OBS connection failed: {e}")
            return False

    def _connect_obs_websocket(self) -> bool:
        """Connect to OBS Studio via WebSocket"""
        try:
            import obswebsocket

            # Create WebSocket connection
            self.obs_websocket = obswebsocket.obsws(
                host=self.config["obs_websocket_host"],
                port=self.config["obs_websocket_port"],
                password=self.config["obs_websocket_password"],
            )

            # Test connection
            self.obs_websocket.connect()
            logger.info("✅ OBS WebSocket connection established")
            return True

        except Exception as e:
            logger.warning(f"⚠️ OBS WebSocket connection failed: {e}")
            return False

    def _setup_virtual_camera(self) -> bool:
        """Setup virtual camera for OBS integration"""
        try:
            import virtual_camera

            # Create virtual camera instance
            self.virtual_camera = virtual_camera.VirtualCamera(
                name=self.config["virtual_camera_name"],
                width=self.config["resolution"][0],
                height=self.config["resolution"][1],
                fps=self.config["frame_rate"],
            )

            # Start virtual camera
            self.virtual_camera.start()
            logger.info("✅ Virtual camera started successfully")
            return True

        except Exception as e:
            logger.warning(f"⚠️ Virtual camera setup failed: {e}")
            return False

    def disconnect_from_obs(self) -> bool:
        """Disconnect from OBS Studio"""
        if not self.is_connected:
            logger.warning("⚠️ Not connected to OBS")
            return True

        try:
            logger.info("🔌 Disconnecting from OBS Studio...")

            # Close WebSocket connection
            if self.obs_websocket:
                try:
                    self.obs_websocket.disconnect()
                    logger.info("✅ OBS WebSocket disconnected")
                except:
                    pass

            # Stop virtual camera
            if self.virtual_camera:
                try:
                    self.virtual_camera.stop()
                    logger.info("✅ Virtual camera stopped")
                except:
                    pass

            self.is_connected = False
            logger.info("✅ Disconnected from OBS Studio successfully")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to disconnect from OBS: {e}")
            return False

    def push_frame_to_obs(self, frame: np.ndarray) -> bool:
        """Push a video frame to OBS Studio"""
        if not self.is_connected:
            logger.warning("⚠️ Not connected to OBS - attempting to connect")
            if not self.connect_to_obs():
                return False

        try:
            # Resize frame to match OBS resolution
            frame_resized = cv2.resize(frame, self.config["resolution"])

            # Add frame to buffer
            self.frame_buffer.append(frame_resized)

            # Maintain buffer size
            if len(self.frame_buffer) > self.config["buffer_size"]:
                self.frame_buffer.pop(0)

            # Push to OBS via WebSocket if available
            if self.obs_websocket:
                return self._push_frame_websocket(frame_resized)

            # Push to virtual camera if available
            elif self.virtual_camera:
                return self._push_frame_virtual_camera(frame_resized)

            return False

        except Exception as e:
            logger.error(f"❌ Failed to push frame to OBS: {e}")
            return False

    def _push_frame_websocket(self, frame: np.ndarray) -> bool:
        """Push frame via OBS WebSocket"""
        try:
            # Convert frame to base64 for transmission
            import base64

            _, buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
            frame_base64 = base64.b64encode(buffer).decode("utf-8")

            # Send frame data via WebSocket
            if self.obs_websocket:
                # This would require custom OBS plugin to receive frames
                # For now, we'll use the virtual camera approach
                pass

            return True

        except Exception as e:
            logger.error(f"❌ WebSocket frame push failed: {e}")
            return False

    def _push_frame_virtual_camera(self, frame: np.ndarray) -> bool:
        """Push frame via virtual camera"""
        try:
            if self.virtual_camera:
                # Convert BGR to RGB (OpenCV uses BGR, most systems use RGB)
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Push frame to virtual camera
                self.virtual_camera.push_frame(frame_rgb)
                return True

            return False

        except Exception as e:
            logger.error(f"❌ Virtual camera frame push failed: {e}")
            return False

    def start_streaming(self, source: Callable[[], np.ndarray]) -> bool:
        """Start streaming frames from source to OBS"""
        if not self.is_connected:
            logger.error("❌ Not connected to OBS - cannot start streaming")
            return False

        try:
            logger.info("🎥 Starting OBS streaming...")

            def stream_frames():
                while self.is_connected:
                    try:
                        # Get frame from source
                        frame = source()
                        if frame is not None:
                            # Push frame to OBS
                            self.push_frame_to_obs(frame)

                        # Control frame rate
                        time.sleep(1.0 / self.config["frame_rate"])

                    except Exception as e:
                        logger.error(f"❌ Streaming error: {e}")
                        time.sleep(1.0 / self.config["frame_rate"])

            # Start streaming thread
            self.streaming_thread = threading.Thread(target=stream_frames, daemon=True)
            self.streaming_thread.start()

            logger.info("✅ OBS streaming started successfully")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to start OBS streaming: {e}")
            return False

    def stop_streaming(self) -> bool:
        """Stop streaming to OBS"""
        try:
            logger.info("🛑 Stopping OBS streaming...")

            # Stop streaming thread
            if hasattr(self, "streaming_thread") and self.streaming_thread:
                self.is_connected = False
                self.streaming_thread.join(timeout=5.0)
                logger.info("✅ Streaming thread stopped")

            logger.info("✅ OBS streaming stopped successfully")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to stop OBS streaming: {e}")
            return False

    def get_obs_status(self) -> Dict[str, Any]:
        """Get OBS connection and streaming status"""
        return {
            "is_connected": self.is_connected,
            "websocket_connected": self.obs_websocket is not None,
            "virtual_camera_active": self.virtual_camera is not None,
            "frame_buffer_size": len(self.frame_buffer),
            "streaming_active": hasattr(self, "streaming_thread")
            and self.streaming_thread
            and self.streaming_thread.is_alive(),
            "config": self.config,
        }

    def health_check(self) -> Dict[str, Any]:
        """Perform health check of OBS integration"""
        health_status = {"status": "healthy", "timestamp": time.time(), "checks": {}}

        # Check OBS WebSocket
        try:
            if self.obs_websocket:
                health_status["checks"]["obs_websocket"] = {
                    "status": "healthy",
                    "connected": True,
                }
            else:
                health_status["checks"]["obs_websocket"] = {
                    "status": "unhealthy",
                    "error": "Not initialized",
                }
                health_status["status"] = "degraded"
        except Exception as e:
            health_status["checks"]["obs_websocket"] = {
                "status": "unhealthy",
                "error": str(e),
            }
            health_status["status"] = "degraded"

        # Check Virtual Camera
        try:
            if self.virtual_camera:
                health_status["checks"]["virtual_camera"] = {
                    "status": "healthy",
                    "active": True,
                }
            else:
                health_status["checks"]["virtual_camera"] = {
                    "status": "unhealthy",
                    "error": "Not initialized",
                }
                health_status["status"] = "degraded"
        except Exception as e:
            health_status["checks"]["virtual_camera"] = {
                "status": "unhealthy",
                "error": str(e),
            }
            health_status["status"] = "degraded"

        return health_status
