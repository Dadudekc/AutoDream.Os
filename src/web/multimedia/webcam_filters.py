"""
Webcam Filter System with OBS Integration
Agent_Cellphone_V2_Repository TDD Integration Project

Comprehensive real-time webcam filtering with OBS Virtual Camera output
"""

import os
import sys
import logging
import threading
import time
import json

from src.utils.stability_improvements import stability_manager, safe_import
from typing import Dict, List, Any, Optional, Callable, Tuple
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance

# Import existing services
try:
    from .obs_integration import OBSVirtualCameraIntegration
    from .core import MultimediaCore

    logger = logging.getLogger(__name__)
except ImportError as e:
    print(f"⚠️ Warning: Some multimedia services could not be imported: {e}")

    # Create mock services for basic functionality
    class MockService:
        def __init__(self, name):
            self.name = name

        def __getattr__(self, name):
            return lambda *args, **kwargs: None

    OBSVirtualCameraIntegration = MockService("OBSVirtualCameraIntegration")
    MultimediaCore = MockService("MultimediaCore")
    logger = logging.getLogger(__name__)


class WebcamFilterSystem:
    """
    Comprehensive Webcam Filter System with OBS Integration
    Provides real-time video effects and processing
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or self._default_config()
        self.is_running = False
        self.camera = None
        self.active_filters = {}
        self.filter_pipeline = []
        self.obs_integration = None
        self.processing_thread = None
        self.frame_buffer = []

        # Initialize filter system
        self._initialize_filter_system()

        # Connect to OBS integration
        self._connect_obs_integration()

        logger.info("🎨 Webcam Filter System initialized successfully")

    def _default_config(self) -> Dict[str, Any]:
        """Default configuration for webcam filter system"""
        return {
            "camera_index": 0,
            "frame_rate": 30,
            "resolution": (1280, 720),
            "quality": "high",
            "enable_preview": True,
            "preview_window_size": (640, 480),
            "filter_chain_max": 10,
            "auto_save_filtered": True,
            "save_directory": "/tmp/filtered_frames",
            "obs_integration": {
                "enabled": True,
                "output_resolution": (1920, 1080),
                "frame_rate": 30,
            },
        }

    def _initialize_filter_system(self):
        """Initialize the webcam filter system"""
        try:
            # Create save directory
            save_dir = Path(self.config["save_directory"])
            save_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"✅ Filter save directory created: {save_dir}")

            # Initialize camera
            self._initialize_camera()

            # Load available filters
            self._load_available_filters()

        except Exception as e:
            logger.error(f"❌ Failed to initialize filter system: {e}")
            raise

    def _initialize_camera(self):
        """Initialize webcam camera"""
        try:
            self.camera = cv2.VideoCapture(self.config["camera_index"])

            if not self.camera.isOpened():
                raise Exception(
                    f"Could not open camera at index {self.config['camera_index']}"
                )

            # Set camera properties
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.config["resolution"][0])
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config["resolution"][1])
            self.camera.set(cv2.CAP_PROP_FPS, self.config["frame_rate"])

            logger.info(
                f"✅ Camera initialized: {self.config['resolution']} @ {self.config['frame_rate']}fps"
            )

        except Exception as e:
            logger.error(f"❌ Failed to initialize camera: {e}")
            raise

    def _load_available_filters(self):
        """Load all available video filters"""
        self.available_filters = {
            # Basic Image Filters
            "blur": self._apply_blur_filter,
            "sharpen": self._apply_sharpen_filter,
            "smooth": self._apply_smooth_filter,
            "emboss": self._apply_emboss_filter,
            "edge_enhance": self._apply_edge_enhance_filter,
            # Color Filters
            "grayscale": self._apply_grayscale_filter,
            "sepia": self._apply_sepia_filter,
            "invert": self._apply_invert_filter,
            "posterize": self._apply_posterize_filter,
            "solarize": self._apply_solarize_filter,
            # Artistic Filters
            "cartoon": self._apply_cartoon_filter,
            "sketch": self._apply_sketch_filter,
            "oil_painting": self._apply_oil_painting_filter,
            "watercolor": self._apply_watercolor_filter,
            "pixelate": self._apply_pixelate_filter,
            # Special Effects
            "glitch": self._apply_glitch_filter,
            "vintage": self._apply_vintage_filter,
            "neon": self._apply_neon_filter,
            "hologram": self._apply_hologram_filter,
            "matrix": self._apply_matrix_filter,
            # Face Filters
            "face_detection": self._apply_face_detection_filter,
            "face_swap": self._apply_face_swap_filter,
            "age_progression": self._apply_age_progression_filter,
            "emotion_detection": self._apply_emotion_detection_filter,
            # Background Effects
            "background_blur": self._apply_background_blur_filter,
            "background_replacement": self._apply_background_replacement_filter,
            "green_screen": self._apply_green_screen_filter,
            "virtual_background": self._apply_virtual_background_filter,
        }

        logger.info(f"✅ Loaded {len(self.available_filters)} available filters")

    def _connect_obs_integration(self):
        """Connect to OBS integration service"""
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

    def add_filter(
        self, filter_name: str, parameters: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Add a filter to the processing pipeline"""
        if filter_name not in self.available_filters:
            logger.error(f"❌ Filter '{filter_name}' not found")
            return False

        if len(self.filter_pipeline) >= self.config["filter_chain_max"]:
            logger.warning(
                f"⚠️ Filter pipeline full ({self.config['filter_chain_max']} max)"
            )
            return False

        filter_config = {
            "name": filter_name,
            "function": self.available_filters[filter_name],
            "parameters": parameters or {},
            "enabled": True,
        }

        self.filter_pipeline.append(filter_config)
        self.active_filters[filter_name] = filter_config

        logger.info(f"✅ Added filter: {filter_name}")
        return True

    def remove_filter(self, filter_name: str) -> bool:
        """Remove a filter from the processing pipeline"""
        for i, filter_config in enumerate(self.filter_pipeline):
            if filter_config["name"] == filter_name:
                del self.filter_pipeline[i]
                if filter_name in self.active_filters:
                    del self.active_filters[filter_name]
                logger.info(f"✅ Removed filter: {filter_name}")
                return True

        logger.warning(f"⚠️ Filter '{filter_name}' not found in pipeline")
        return False

    def clear_filters(self) -> bool:
        """Clear all filters from the processing pipeline"""
        self.filter_pipeline.clear()
        self.active_filters.clear()
        logger.info("✅ Cleared all filters")
        return True

    def start_filtering(self) -> bool:
        """Start the webcam filtering system"""
        if self.is_running:
            logger.warning("⚠️ Filter system already running")
            return False

        try:
            self.is_running = True
            logger.info("🎬 Starting webcam filtering system...")

            # Start processing thread
            self._start_processing_thread()

            logger.info("✅ Webcam filtering system started successfully")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to start filtering system: {e}")
            self.is_running = False
            return False

    def stop_filtering(self) -> bool:
        """Stop the webcam filtering system"""
        if not self.is_running:
            logger.warning("⚠️ Filter system not running")
            return False

        try:
            logger.info("🛑 Stopping webcam filtering system...")

            # Stop processing thread
            if self.processing_thread and self.processing_thread.is_alive():
                self.is_running = False
                self.processing_thread.join(timeout=5.0)
                logger.info("✅ Processing thread stopped")

            # Release camera
            if self.camera:
                self.camera.release()
                logger.info("✅ Camera released")

            logger.info("✅ Webcam filtering system stopped successfully")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to stop filtering system: {e}")
            return False

    def _start_processing_thread(self):
        """Start the video processing thread"""

        def process_video():
            while self.is_running:
                try:
                    # Capture frame from camera
                    ret, frame = self.camera.read()
                    if not ret:
                        logger.warning("⚠️ Failed to capture frame")
                        time.sleep(1.0 / self.config["frame_rate"])
                        continue

                    # Apply filter pipeline
                    filtered_frame = self._apply_filter_pipeline(frame)

                    # Add to frame buffer
                    self.frame_buffer.append(filtered_frame)
                    if len(self.frame_buffer) > 10:  # Keep last 10 frames
                        self.frame_buffer.pop(0)

                    # Send to OBS if connected
                    if self.obs_integration:
                        self.obs_integration.push_frame_to_obs(filtered_frame)

                    # Control frame rate
                    time.sleep(1.0 / self.config["frame_rate"])

                except Exception as e:
                    logger.error(f"❌ Processing error: {e}")
                    time.sleep(1.0 / self.config["frame_rate"])

        self.processing_thread = threading.Thread(target=process_video, daemon=True)
        self.processing_thread.start()

    def _apply_filter_pipeline(self, frame: np.ndarray) -> np.ndarray:
        """Apply all active filters to the frame"""
        processed_frame = frame.copy()

        for filter_config in self.filter_pipeline:
            if filter_config["enabled"]:
                try:
                    filter_func = filter_config["function"]
                    parameters = filter_config["parameters"]

                    # Apply filter with parameters
                    processed_frame = filter_func(processed_frame, **parameters)

                except Exception as e:
                    logger.error(f"❌ Filter '{filter_config['name']}' failed: {e}")
                    continue

        return processed_frame

    # ===== FILTER IMPLEMENTATIONS =====

    def _apply_blur_filter(
        self, frame: np.ndarray, intensity: float = 0.5
    ) -> np.ndarray:
        """Apply blur filter to frame"""
        kernel_size = int(15 * intensity) + 1
        if kernel_size % 2 == 0:
            kernel_size += 1
        return cv2.GaussianBlur(frame, (kernel_size, kernel_size), 0)

    def _apply_sharpen_filter(
        self, frame: np.ndarray, intensity: float = 0.5
    ) -> np.ndarray:
        """Apply sharpen filter to frame"""
        kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]]) * intensity
        return cv2.filter2D(frame, -1, kernel)

    def _apply_smooth_filter(
        self, frame: np.ndarray, intensity: float = 0.5
    ) -> np.ndarray:
        """Apply smooth filter to frame"""
        kernel_size = int(10 * intensity) + 1
        if kernel_size % 2 == 0:
            kernel_size += 1
        return cv2.medianBlur(frame, kernel_size)

    def _apply_emboss_filter(
        self, frame: np.ndarray, intensity: float = 0.5
    ) -> np.ndarray:
        """Apply emboss filter to frame"""
        kernel = np.array([[0, -1, -1], [1, 0, -1], [1, 1, 0]]) * intensity
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        embossed = cv2.filter2D(gray, -1, kernel) + 128
        return cv2.cvtColor(embossed.astype(np.uint8), cv2.COLOR_GRAY2BGR)

    def _apply_edge_enhance_filter(
        self, frame: np.ndarray, intensity: float = 0.5
    ) -> np.ndarray:
        """Apply edge enhancement filter to frame"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        enhanced = cv2.addWeighted(gray, 1 - intensity, edges, intensity, 0)
        return cv2.cvtColor(enhanced.astype(np.uint8), cv2.COLOR_GRAY2BGR)

    def _apply_grayscale_filter(self, frame: np.ndarray) -> np.ndarray:
        """Apply grayscale filter to frame"""
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    def _apply_sepia_filter(
        self, frame: np.ndarray, intensity: float = 0.8
    ) -> np.ndarray:
        """Apply sepia filter to frame"""
        sepia_matrix = np.array(
            [[0.393, 0.769, 0.189], [0.349, 0.686, 0.168], [0.272, 0.534, 0.131]]
        )
        sepia_frame = cv2.transform(frame, sepia_matrix)
        return cv2.addWeighted(frame, 1 - intensity, sepia_frame, intensity, 0)

    def _apply_invert_filter(self, frame: np.ndarray) -> np.ndarray:
        """Apply invert filter to frame"""
        return cv2.bitwise_not(frame)

    def _apply_posterize_filter(self, frame: np.ndarray, levels: int = 4) -> np.ndarray:
        """Apply posterize filter to frame"""
        factor = 256 // levels
        return (frame // factor) * factor

    def _apply_solarize_filter(
        self, frame: np.ndarray, threshold: int = 128
    ) -> np.ndarray:
        """Apply solarize filter to frame"""
        solarized = frame.copy()
        solarized[frame > threshold] = 255 - frame[frame > threshold]
        return solarized

    def _apply_cartoon_filter(
        self, frame: np.ndarray, intensity: float = 0.5
    ) -> np.ndarray:
        """Apply cartoon filter to frame"""
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Apply median blur
        gray = cv2.medianBlur(gray, 5)

        # Detect edges
        edges = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9
        )

        # Apply bilateral filter for cartoon effect
        color = cv2.bilateralFilter(frame, 9, 300, 300)

        # Combine edges with color
        cartoon = cv2.bitwise_and(color, cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR))

        return cv2.addWeighted(frame, 1 - intensity, cartoon, intensity, 0)

    def _apply_sketch_filter(
        self, frame: np.ndarray, intensity: float = 0.5
    ) -> np.ndarray:
        """Apply sketch filter to frame"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        inverted = cv2.bitwise_not(gray)
        blurred = cv2.GaussianBlur(inverted, (21, 21), 0)
        sketch = cv2.divide(gray, 255 - blurred, scale=256)
        return cv2.addWeighted(
            frame, 1 - intensity, cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR), intensity, 0
        )

    def _apply_oil_painting_filter(
        self, frame: np.ndarray, intensity: float = 0.5
    ) -> np.ndarray:
        """Apply oil painting filter to frame"""
        # This is a simplified oil painting effect
        kernel_size = int(5 * intensity) + 1
        if kernel_size % 2 == 0:
            kernel_size += 1

        # Apply bilateral filter for oil painting effect
        oil_painted = cv2.bilateralFilter(frame, kernel_size, 75, 75)

        return cv2.addWeighted(frame, 1 - intensity, oil_painted, intensity, 0)

    def _apply_watercolor_filter(
        self, frame: np.ndarray, intensity: float = 0.5
    ) -> np.ndarray:
        """Apply watercolor filter to frame"""
        # Apply bilateral filter for watercolor effect
        watercolor = cv2.bilateralFilter(frame, 9, 75, 75)

        # Add slight blur for watercolor texture
        watercolor = cv2.GaussianBlur(watercolor, (3, 3), 0)

        return cv2.addWeighted(frame, 1 - intensity, watercolor, intensity, 0)

    def _apply_pixelate_filter(
        self, frame: np.ndarray, pixel_size: int = 10
    ) -> np.ndarray:
        """Apply pixelate filter to frame"""
        height, width = frame.shape[:2]

        # Resize down
        small = cv2.resize(frame, (width // pixel_size, height // pixel_size))

        # Resize up
        pixelated = cv2.resize(small, (width, height), interpolation=cv2.INTER_NEAREST)

        return pixelated

    def _apply_glitch_filter(
        self, frame: np.ndarray, intensity: float = 0.3
    ) -> np.ndarray:
        """Apply glitch filter to frame"""
        glitched = frame.copy()

        # Random horizontal shifts
        if np.random.random() < intensity:
            shift = np.random.randint(-20, 20)
            glitched = np.roll(glitched, shift, axis=1)

        # Random color channel shifts
        if np.random.random() < intensity:
            channel = np.random.randint(0, 3)
            shift = np.random.randint(-10, 10)
            glitched[:, :, channel] = np.roll(glitched[:, :, channel], shift, axis=1)

        return glitched

    def _apply_vintage_filter(
        self, frame: np.ndarray, intensity: float = 0.6
    ) -> np.ndarray:
        """Apply vintage filter to frame"""
        # Convert to float for processing
        vintage = frame.astype(np.float32) / 255.0

        # Apply vintage color adjustments
        vintage[:, :, 0] *= 1.2  # Increase red
        vintage[:, :, 1] *= 0.8  # Decrease green
        vintage[:, :, 2] *= 0.9  # Decrease blue

        # Add slight sepia tone
        vintage = np.clip(vintage, 0, 1)

        # Convert back to uint8
        vintage = (vintage * 255).astype(np.uint8)

        return cv2.addWeighted(frame, 1 - intensity, vintage, intensity, 0)

    def _apply_neon_filter(
        self, frame: np.ndarray, intensity: float = 0.5
    ) -> np.ndarray:
        """Apply neon filter to frame"""
        # Detect edges
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)

        # Create neon effect
        neon = np.zeros_like(frame)
        neon[edges > 0] = [0, 255, 255]  # Cyan neon

        return cv2.addWeighted(frame, 1 - intensity, neon, intensity, 0)

    def _apply_hologram_filter(
        self, frame: np.ndarray, intensity: float = 0.4
    ) -> np.ndarray:
        """Apply hologram filter to frame"""
        # Create hologram effect with color shifts
        hologram = frame.copy()

        # Shift color channels
        hologram[:, :, 0] = np.roll(hologram[:, :, 0], 5, axis=1)  # Red shift
        hologram[:, :, 2] = np.roll(hologram[:, :, 2], -5, axis=1)  # Blue shift

        # Add transparency effect
        hologram = cv2.addWeighted(frame, 0.7, hologram, 0.3, 0)

        return cv2.addWeighted(frame, 1 - intensity, hologram, intensity, 0)

    def _apply_matrix_filter(
        self, frame: np.ndarray, intensity: float = 0.6
    ) -> np.ndarray:
        """Apply matrix-style filter to frame"""
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Apply threshold for matrix effect
        _, matrix = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

        # Convert to green matrix style
        matrix_green = np.zeros_like(frame)
        matrix_green[matrix > 0] = [0, 255, 0]  # Green matrix

        return cv2.addWeighted(frame, 1 - intensity, matrix_green, intensity, 0)

    def _apply_face_detection_filter(
        self, frame: np.ndarray, intensity: float = 0.5
    ) -> np.ndarray:
        """Apply face detection filter to frame"""
        # Load face cascade classifier
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

        # Detect faces
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        # Draw face rectangles
        face_frame = frame.copy()
        for x, y, w, h in faces:
            cv2.rectangle(face_frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        return cv2.addWeighted(frame, 1 - intensity, face_frame, intensity, 0)

    def _apply_face_swap_filter(
        self, frame: np.ndarray, intensity: float = 0.5
    ) -> np.ndarray:
        """Apply face swap filter to frame (simplified)"""
        # This is a simplified face swap effect
        # In a real implementation, you'd use more sophisticated face detection and swapping

        # Apply slight distortion to simulate face swap
        height, width = frame.shape[:2]
        map_x = np.zeros((height, width), np.float32)
        map_y = np.zeros((height, width), np.float32)

        for y in range(height):
            for x in range(width):
                map_x[y, x] = x + np.sin(y / 30.0) * 10 * intensity
                map_y[y, x] = y + np.cos(x / 30.0) * 10 * intensity

        face_swapped = cv2.remap(frame, map_x, map_y, cv2.INTER_LINEAR)

        return cv2.addWeighted(frame, 1 - intensity, face_swapped, intensity, 0)

    def _apply_age_progression_filter(
        self, frame: np.ndarray, intensity: float = 0.5
    ) -> np.ndarray:
        """Apply age progression filter to frame (simplified)"""
        # This is a simplified age progression effect
        # In a real implementation, you'd use AI models for age progression

        # Apply slight blur and color adjustments to simulate aging
        aged = cv2.GaussianBlur(frame, (5, 5), 0)
        aged = cv2.addWeighted(aged, 0.9, frame, 0.1, 0)

        return cv2.addWeighted(frame, 1 - intensity, aged, intensity, 0)

    def _apply_emotion_detection_filter(
        self, frame: np.ndarray, intensity: float = 0.5
    ) -> np.ndarray:
        """Apply emotion detection filter to frame (simplified)"""
        # This is a simplified emotion detection effect
        # In a real implementation, you'd use AI models for emotion detection

        # Apply color overlay to simulate emotion detection
        emotion_frame = frame.copy()
        emotion_frame[:, :, 1] = cv2.add(emotion_frame[:, :, 1], 50)  # Increase green

        return cv2.addWeighted(frame, 1 - intensity, emotion_frame, intensity, 0)

    def _apply_background_blur_filter(
        self, frame: np.ndarray, intensity: float = 0.7
    ) -> np.ndarray:
        """Apply background blur filter to frame"""
        # This is a simplified background blur effect
        # In a real implementation, you'd use segmentation models

        # Apply blur to entire frame
        blurred = cv2.GaussianBlur(frame, (21, 21), 0)

        # Keep center region sharp (simulating subject focus)
        height, width = frame.shape[:2]
        center_y, center_x = height // 2, width // 2
        region_size = min(height, width) // 4

        y1, y2 = max(0, center_y - region_size), min(height, center_y + region_size)
        x1, x2 = max(0, center_x - region_size), min(width, center_x + region_size)

        blurred[y1:y2, x1:x2] = frame[y1:y2, x1:x2]

        return cv2.addWeighted(frame, 1 - intensity, blurred, intensity, 0)

    def _apply_background_replacement_filter(
        self, frame: np.ndarray, intensity: float = 0.6
    ) -> np.ndarray:
        """Apply background replacement filter to frame (simplified)"""
        # This is a simplified background replacement effect
        # In a real implementation, you'd use segmentation models

        # Create a simple background
        height, width = frame.shape[:2]
        background = np.full((height, width, 3), [100, 150, 200], dtype=np.uint8)

        # Blend with original frame
        return cv2.addWeighted(frame, 1 - intensity, background, intensity, 0)

    def _apply_green_screen_filter(
        self, frame: np.ndarray, intensity: float = 0.8
    ) -> np.ndarray:
        """Apply green screen filter to frame (simplified)"""
        # This is a simplified green screen effect
        # In a real implementation, you'd use color-based segmentation

        # Convert to HSV for better green detection
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Define green range
        lower_green = np.array([40, 40, 40])
        upper_green = np.array([80, 255, 255])

        # Create mask
        mask = cv2.inRange(hsv, lower_green, upper_green)

        # Create background
        background = np.full_like(frame, [0, 0, 255])  # Red background

        # Apply mask
        green_screened = np.where(mask[:, :, np.newaxis] == 255, background, frame)

        return cv2.addWeighted(frame, 1 - intensity, green_screened, intensity, 0)

    def _apply_virtual_background_filter(
        self, frame: np.ndarray, intensity: float = 0.7
    ) -> np.ndarray:
        """Apply virtual background filter to frame (simplified)"""
        # This is a simplified virtual background effect
        # In a real implementation, you'd use segmentation models

        # Create a virtual background
        height, width = frame.shape[:2]
        virtual_bg = np.zeros((height, width, 3), dtype=np.uint8)

        # Add some pattern to virtual background
        for i in range(0, height, 20):
            for j in range(0, width, 20):
                color = np.random.randint(0, 255, 3)
                virtual_bg[i : i + 20, j : j + 20] = color

        # Blend with original frame
        return cv2.addWeighted(frame, 1 - intensity, virtual_bg, intensity, 0)

    def get_filter_status(self) -> Dict[str, Any]:
        """Get current filter system status"""
        return {
            "is_running": self.is_running,
            "active_filters": len(self.active_filters),
            "filter_pipeline": [f["name"] for f in self.filter_pipeline],
            "camera_connected": self.camera is not None and self.camera.isOpened(),
            "obs_connected": self.obs_integration is not None,
            "frame_buffer_size": len(self.frame_buffer),
            "config": self.config,
        }

    def save_filtered_frame(self, filename: Optional[str] = None) -> bool:
        """Save the current filtered frame"""
        if not self.frame_buffer:
            logger.warning("⚠️ No frames available to save")
            return False

        try:
            if filename is None:
                timestamp = int(time.time())
                filename = f"filtered_frame_{timestamp}.jpg"

            filepath = Path(self.config["save_directory"]) / filename

            # Save the most recent filtered frame
            latest_frame = self.frame_buffer[-1]
            cv2.imwrite(str(filepath), latest_frame)

            logger.info(f"✅ Saved filtered frame: {filepath}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to save filtered frame: {e}")
            return False

    def get_available_filters(self) -> List[str]:
        """Get list of available filter names"""
        return list(self.available_filters.keys())

    def get_filter_parameters(self, filter_name: str) -> Optional[Dict[str, Any]]:
        """Get default parameters for a specific filter"""
        if filter_name not in self.available_filters:
            return None

        # Return default parameters for each filter
        default_params = {
            "blur": {"intensity": 0.5},
            "sharpen": {"intensity": 0.5},
            "smooth": {"intensity": 0.5},
            "emboss": {"intensity": 0.5},
            "edge_enhance": {"intensity": 0.5},
            "sepia": {"intensity": 0.8},
            "posterize": {"levels": 4},
            "solarize": {"threshold": 128},
            "cartoon": {"intensity": 0.5},
            "sketch": {"intensity": 0.5},
            "oil_painting": {"intensity": 0.5},
            "watercolor": {"intensity": 0.5},
            "pixelate": {"pixel_size": 10},
            "glitch": {"intensity": 0.3},
            "vintage": {"intensity": 0.6},
            "neon": {"intensity": 0.5},
            "hologram": {"intensity": 0.4},
            "matrix": {"intensity": 0.6},
            "face_detection": {"intensity": 0.5},
            "face_swap": {"intensity": 0.5},
            "age_progression": {"intensity": 0.5},
            "emotion_detection": {"intensity": 0.5},
            "background_blur": {"intensity": 0.7},
            "background_replacement": {"intensity": 0.6},
            "green_screen": {"intensity": 0.8},
            "virtual_background": {"intensity": 0.7},
        }

        return default_params.get(filter_name, {})
