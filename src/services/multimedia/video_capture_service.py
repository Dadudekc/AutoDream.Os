#!/usr/bin/env python3
"""
Video Capture Service
Real-time video capture with threading support and OpenCV integration
"""

import cv2
import threading
import time
import logging
from typing import Optional, Callable, Dict, Any
from pathlib import Path
import numpy as np

logger = logging.getLogger(__name__)


class VideoCaptureService:
    """
    High-performance video capture service with threading support
    Supports webcam, screen capture, and file-based video processing
    """

    def __init__(self):
        self.capture_threads = {}
        self.is_capturing = False
        self.frame_callbacks = {}
        self.capture_config = {
            "fps": 30,
            "resolution": (640, 480),
            "codec": "XVID",
            "buffer_size": 100,
        }

    def start_webcam_capture(
        self, device_id: int = 0, callback: Optional[Callable] = None
    ) -> bool:
        """
        Start webcam capture with threading support

        Args:
            device_id: Camera device ID (default: 0)
            callback: Frame processing callback function

        Returns:
            bool: True if capture started successfully
        """
        try:
            if device_id in self.capture_threads:
                logger.warning(f"Webcam capture already running on device {device_id}")
                return False

            # Initialize capture
            cap = cv2.VideoCapture(device_id)
            if not cap.isOpened():
                logger.error(f"Failed to open webcam device {device_id}")
                return False

            # Configure capture settings
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.capture_config["resolution"][0])
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.capture_config["resolution"][1])
            cap.set(cv2.CAP_PROP_FPS, self.capture_config["fps"])

            # Start capture thread
            self.is_capturing = True
            capture_thread = threading.Thread(
                target=self._webcam_capture_loop,
                args=(cap, device_id, callback),
                daemon=True,
            )
            capture_thread.start()

            self.capture_threads[device_id] = {
                "thread": capture_thread,
                "capture": cap,
                "active": True,
            }

            logger.info(f"Webcam capture started on device {device_id}")
            return True

        except Exception as e:
            logger.error(f"Error starting webcam capture: {e}")
            return False

    def _webcam_capture_loop(
        self, cap: cv2.VideoCapture, device_id: int, callback: Optional[Callable]
    ):
        """Internal webcam capture loop with threading"""
        try:
            while self.is_capturing and self.capture_threads[device_id]["active"]:
                ret, frame = cap.read()
                if ret:
                    # Process frame if callback provided
                    if callback:
                        try:
                            processed_frame = callback(frame)
                            if processed_frame is not None:
                                frame = processed_frame
                        except Exception as e:
                            logger.error(f"Frame callback error: {e}")

                    # Store frame for access by other services
                    self.frame_callbacks[device_id] = frame

                    # Maintain frame rate
                    time.sleep(1.0 / self.capture_config["fps"])
                else:
                    logger.warning(f"Failed to read frame from device {device_id}")
                    break

        except Exception as e:
            logger.error(f"Webcam capture loop error: {e}")
        finally:
            cap.release()
            if device_id in self.capture_threads:
                self.capture_threads[device_id]["active"] = False

    def start_screen_capture(
        self, region: Optional[tuple] = None, callback: Optional[Callable] = None
    ) -> bool:
        """
        Start screen capture with threading support

        Args:
            region: Screen region to capture (x, y, width, height)
            callback: Frame processing callback function

        Returns:
            bool: True if capture started successfully
        """
        try:
            # Import screen capture library
            try:
                import pyautogui
                import PIL.ImageGrab
            except ImportError:
                logger.error("Screen capture requires pyautogui and PIL")
                return False

            # Start screen capture thread
            self.is_capturing = True
            screen_thread = threading.Thread(
                target=self._screen_capture_loop, args=(region, callback), daemon=True
            )
            screen_thread.start()

            self.capture_threads["screen"] = {
                "thread": screen_thread,
                "capture": None,
                "active": True,
                "region": region,
            }

            logger.info("Screen capture started")
            return True

        except Exception as e:
            logger.error(f"Error starting screen capture: {e}")
            return False

    def _screen_capture_loop(
        self, region: Optional[tuple], callback: Optional[Callable]
    ):
        """Internal screen capture loop with threading"""
        try:
            import PIL.ImageGrab
            import numpy as np

            while self.is_capturing and self.capture_threads["screen"]["active"]:
                # Capture screen region
                if region:
                    screenshot = PIL.ImageGrab.grab(bbox=region)
                else:
                    screenshot = PIL.ImageGrab.grab()

                # Convert to OpenCV format
                frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

                # Process frame if callback provided
                if callback:
                    try:
                        processed_frame = callback(frame)
                        if processed_frame is not None:
                            frame = processed_frame
                    except Exception as e:
                        logger.error(f"Screen capture callback error: {e}")

                # Store frame
                self.frame_callbacks["screen"] = frame

                # Maintain frame rate
                time.sleep(1.0 / self.capture_config["fps"])

        except Exception as e:
            logger.error(f"Screen capture loop error: {e}")

    def stop_capture(self, device_id: Optional[int] = None) -> bool:
        """
        Stop video capture

        Args:
            device_id: Specific device to stop, or None for all

        Returns:
            bool: True if capture stopped successfully
        """
        try:
            if device_id is not None:
                if device_id in self.capture_threads:
                    self.capture_threads[device_id]["active"] = False
                    self.capture_threads[device_id]["capture"].release()
                    del self.capture_threads[device_id]
                    logger.info(f"Capture stopped on device {device_id}")
                    return True
                return False
            else:
                # Stop all captures
                self.is_capturing = False
                for dev_id, capture_info in list(self.capture_threads.items()):
                    capture_info["active"] = False
                    if capture_info["capture"]:
                        capture_info["capture"].release()
                    del self.capture_threads[dev_id]

                logger.info("All captures stopped")
                return True

        except Exception as e:
            logger.error(f"Error stopping capture: {e}")
            return False

    def get_frame(self, device_id: int = 0) -> Optional[np.ndarray]:
        """
        Get current frame from specified device

        Args:
            device_id: Camera device ID or 'screen' for screen capture

        Returns:
            np.ndarray: Current frame or None if not available
        """
        return self.frame_callbacks.get(device_id)

    def apply_filter(self, frame: np.ndarray, filter_type: str, **kwargs) -> np.ndarray:
        """
        Apply real-time video filter

        Args:
            frame: Input frame
            filter_type: Type of filter to apply
            **kwargs: Filter-specific parameters

        Returns:
            np.ndarray: Filtered frame
        """
        try:
            if filter_type == "grayscale":
                return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            elif filter_type == "blur":
                kernel_size = kwargs.get("kernel_size", 15)
                return cv2.GaussianBlur(frame, (kernel_size, kernel_size), 0)
            elif filter_type == "edge_detection":
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                return cv2.Canny(gray, 100, 200)
            elif filter_type == "color_inversion":
                return cv2.bitwise_not(frame)
            else:
                logger.warning(f"Unknown filter type: {filter_type}")
                return frame

        except Exception as e:
            logger.error(f"Filter application error: {e}")
            return frame

    def save_frame(self, frame: np.ndarray, filepath: str) -> bool:
        """
        Save frame to file

        Args:
            frame: Frame to save
            filepath: Output file path

        Returns:
            bool: True if saved successfully
        """
        try:
            Path(filepath).parent.mkdir(parents=True, exist_ok=True)
            return cv2.imwrite(filepath, frame)
        except Exception as e:
            logger.error(f"Error saving frame: {e}")
            return False

    def get_capture_status(self) -> Dict[str, Any]:
        """
        Get current capture status

        Returns:
            Dict containing capture status information
        """
        return {
            "is_capturing": self.is_capturing,
            "active_captures": len(self.capture_threads),
            "devices": list(self.capture_threads.keys()),
            "frame_callbacks": list(self.frame_callbacks.keys()),
            "config": self.capture_config.copy(),
        }
