"""Video handling for webcam filter system."""
import logging
import threading
import time
from pathlib import Path
from typing import Dict, Any, Optional

import cv2

try:
    from .obs_integration import OBSVirtualCameraIntegration
    from .core import MultimediaCore

    logger = logging.getLogger(__name__)
except ImportError as e:
    print(f"⚠️ Warning: Some multimedia services could not be imported: {e}")

    class MockService:
        def __init__(self, name):
            self.name = name

        def __getattr__(self, name):
            return lambda *args, **kwargs: None

    OBSVirtualCameraIntegration = MockService("OBSVirtualCameraIntegration")
    MultimediaCore = MockService("MultimediaCore")
    logger = logging.getLogger(__name__)


class WebcamVideoHandler:
    """Handle webcam input, processing loop, and OBS integration."""

    def __init__(self, config: Dict[str, Any], filter_processor):
        self.config = config
        self.filter_processor = filter_processor
        self.is_running = False
        self.camera = None
        self.obs_integration = None
        self.processing_thread: Optional[threading.Thread] = None
        self.frame_buffer = []

        Path(self.config["save_directory"]).mkdir(parents=True, exist_ok=True)
        self._initialize_camera()
        self._connect_obs_integration()

    def _initialize_camera(self):
        try:
            self.camera = cv2.VideoCapture(self.config["camera_index"])
            if not self.camera.isOpened():
                raise Exception(
                    f"Could not open camera at index {self.config['camera_index']}"
                )
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.config["resolution"][0])
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config["resolution"][1])
            self.camera.set(cv2.CAP_PROP_FPS, self.config["frame_rate"])
            logger.info(
                f"✅ Camera initialized: {self.config['resolution']} @ {self.config['frame_rate']}fps"
            )
        except Exception as e:
            logger.error(f"❌ Failed to initialize camera: {e}")
            raise

    def _connect_obs_integration(self):
        try:
            if self.config["obs_integration"]["enabled"]:
                obs_config = {
                    "resolution": self.config["obs_integration"]["output_resolution"],
                    "frame_rate": self.config["obs_integration"]["frame_rate"],
                }
                self.obs_integration = OBSVirtualCameraIntegration(obs_config)
                logger.info("✅ Connected to OBS Integration Service")
            else:
                logger.info("⚠️ OBS integration disabled in configuration")
        except Exception as e:
            logger.warning(f"⚠️ Could not connect to OBS integration: {e}")

    # --- lifecycle ---
    def start(self) -> bool:
        if self.is_running:
            logger.warning("⚠️ Filter system already running")
            return False
        self.is_running = True
        self._start_processing_thread()
        logger.info("✅ Webcam filtering system started successfully")
        return True

    def stop(self) -> bool:
        if not self.is_running:
            logger.warning("⚠️ Filter system not running")
            return False
        try:
            if self.processing_thread and self.processing_thread.is_alive():
                self.is_running = False
                self.processing_thread.join(timeout=5.0)
                logger.info("✅ Processing thread stopped")
            if self.camera:
                self.camera.release()
                logger.info("✅ Camera released")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to stop filtering system: {e}")
            return False

    def _start_processing_thread(self):
        def process_video():
            while self.is_running:
                try:
                    ret, frame = self.camera.read()
                    if not ret:
                        logger.warning("⚠️ Failed to capture frame")
                        time.sleep(1.0 / self.config["frame_rate"])
                        continue
                    filtered_frame = self.filter_processor.apply_filter_pipeline(frame)
                    self.frame_buffer.append(filtered_frame)
                    if len(self.frame_buffer) > 10:
                        self.frame_buffer.pop(0)
                    if self.obs_integration:
                        self.obs_integration.push_frame_to_obs(filtered_frame)
                    time.sleep(1.0 / self.config["frame_rate"])
                except Exception as e:
                    logger.error(f"❌ Processing error: {e}")
                    time.sleep(1.0 / self.config["frame_rate"])

        self.processing_thread = threading.Thread(target=process_video, daemon=True)
        self.processing_thread.start()

    # --- frame utilities ---
    def save_filtered_frame(self, filename: Optional[str] = None) -> bool:
        if not self.frame_buffer:
            logger.warning("⚠️ No frames available to save")
            return False
        try:
            if filename is None:
                filename = f"filtered_frame_{int(time.time())}.jpg"
            filepath = Path(self.config["save_directory"]) / filename
            latest_frame = self.frame_buffer[-1]
            cv2.imwrite(str(filepath), latest_frame)
            logger.info(f"✅ Saved filtered frame: {filepath}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to save filtered frame: {e}")
            return False
