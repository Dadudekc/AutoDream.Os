"""
Screen Capture - V2 Compliant
============================

Screen capture functionality with coordinate-based region targeting.
Integrates with V2's coordinate system for agent-specific screen regions.

V2 Compliance: ≤200 lines, SOLID principles, comprehensive error handling.

Author: Agent-1 - Vision & Automation Specialist
Optimized: Agent-7 - Repository Cloning Specialist (V2 consolidation)
License: MIT
"""

import logging
import time
from collections.abc import Callable

# Optional dependencies for screen capture
try:
    import numpy as np
    from PIL import Image, ImageGrab

    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    logging.warning("PIL/Pillow not available - screen capture disabled")

# V2 Integration imports (uses fallbacks if unavailable)
from .utils import get_coordinate_loader, get_logger, get_unified_config


class ScreenCapture:
    """
    Screen capture with coordinate integration.

    Capabilities:
    - Full screen and region-based capture
    - Agent-specific region capture via coordinates
    - Continuous monitoring mode
    - Image format conversion
    """

    def __init__(self, config: dict | None = None):
        """Initialize screen capture system."""
        self.config = config or {}
        self.logger = get_logger(__name__)

        # V2 Integration
        self.coordinate_loader = get_coordinate_loader()
        self.unified_config = get_unified_config()

        # Capture settings
        capture_config = self.config.get("capture", {})
        self.capture_frequency = capture_config.get("frequency", 1.0)
        self.capture_format = capture_config.get("format", "RGB")

        # State
        self.is_monitoring = False

        if not PIL_AVAILABLE:
            self.logger.error("PIL/Pillow not available - screen capture disabled")

    def capture_screen(self, region: tuple[int, int, int, int] | None = None) -> np.ndarray | None:
        """
        Capture screenshot of specified region or full screen.

        Args:
            region: (x, y, width, height) tuple for region capture

        Returns:
            numpy array of captured image, or None if failed
        """
        if not PIL_AVAILABLE:
            self.logger.error("Screen capture failed: PIL not available")
            return None

        try:
            # Capture region or full screen
            if region:
                x, y, width, height = region
                bbox = (x, y, x + width, y + height)
                screenshot = ImageGrab.grab(bbox=bbox)
            else:
                screenshot = ImageGrab.grab()

            # Convert to numpy array
            img_array = np.array(screenshot)

            # Apply format conversion
            img_array = self._convert_format(img_array)

            self.logger.info(f"Screenshot captured: {img_array.shape}")
            return img_array

        except Exception as e:
            self.logger.error(f"Screen capture failed: {e}")
            return None

    def capture_agent_region(self, agent_id: str) -> np.ndarray | None:
        """
        Capture screen region for specific agent using coordinates.

        Args:
            agent_id: Agent identifier (e.g., "Agent-1")

        Returns:
            numpy array of captured image, or None if failed
        """
        if not self.coordinate_loader:
            self.logger.warning("Coordinate loader not available - using fallback")
            return self._capture_fallback_region(agent_id)

        try:
            # Get agent coordinates
            coordinates = self.coordinate_loader.get_coordinates(agent_id)
            if not coordinates:
                self.logger.warning(f"No coordinates found for {agent_id}")
                return self._capture_fallback_region(agent_id)

            # Create region around coordinates
            x, y = coordinates
            region = (
                max(0, x - 200),  # 400x300 region centered on coordinates
                max(0, y - 150),
                400,
                300,
            )

            return self.capture_screen(region)

        except Exception as e:
            self.logger.error(f"Agent region capture failed for {agent_id}: {e}")
            return self._capture_fallback_region(agent_id)

    def continuous_capture(
        self, callback_func: Callable, duration: int | None = None, agent_id: str | None = None
    ) -> None:
        """
        Continuously capture screen and call callback with image.

        Args:
            callback_func: Function to call with captured image
            duration: Duration in seconds (None for indefinite)
            agent_id: Agent ID for region capture (None for full screen)
        """
        start_time = time.time()
        self.is_monitoring = True

        self.logger.info(f"Starting continuous capture for {duration or 'indefinite'} seconds")

        try:
            while self.is_monitoring:
                # Check duration
                if duration and (time.time() - start_time) >= duration:
                    break

                # Capture image
                if agent_id:
                    image = self.capture_agent_region(agent_id)
                else:
                    image = self.capture_screen()

                # Call callback
                if image is not None and callback_func:
                    try:
                        callback_func(image)
                    except Exception as e:
                        self.logger.error(f"Callback failed: {e}")

                # Wait for next capture
                time.sleep(1.0 / self.capture_frequency)

        except Exception as e:
            self.logger.error(f"Continuous capture failed: {e}")
        finally:
            self.is_monitoring = False
            self.logger.info("Continuous capture stopped")

    def stop_monitoring(self) -> None:
        """Stop continuous monitoring."""
        self.is_monitoring = False

    def save_image(self, image: np.ndarray, filename: str, format: str = "PNG") -> bool:
        """
        Save image to file.

        Args:
            image: Image array to save
            filename: Output filename
            format: Image format (PNG, JPEG, etc.)

        Returns:
            True if successful, False otherwise
        """
        try:
            # Convert numpy array to PIL Image
            pil_image = Image.fromarray(image)

            # Save to file
            pil_image.save(filename, format=format)

            self.logger.info(f"Image saved to {filename}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to save image: {e}")
            return False

    def _convert_format(self, img_array: np.ndarray) -> np.ndarray:
        """Convert image array to configured format."""
        if self.capture_format == "L":  # Grayscale
            if len(img_array.shape) == 3:
                return np.mean(img_array, axis=2).astype(np.uint8)
        elif self.capture_format == "RGB":
            if len(img_array.shape) == 4:  # RGBA
                return img_array[:, :, :3]  # Remove alpha channel
        return img_array

    def _capture_fallback_region(self, agent_id: str) -> np.ndarray | None:
        """Capture fallback region when coordinates unavailable."""
        fallback_regions = self.config.get("coordinates", {}).get("fallback_regions", {})

        if agent_id in fallback_regions:
            return self.capture_screen(fallback_regions[agent_id])
        else:
            self.logger.warning(f"No fallback region for {agent_id} - using full screen")
            return self.capture_screen()

    def get_capture_info(self) -> dict:
        """Get information about capture capabilities."""
        return {
            "pil_available": PIL_AVAILABLE,
            "coordinate_loader_available": self.coordinate_loader is not None,
            "capture_frequency": self.capture_frequency,
            "capture_format": self.capture_format,
            "is_monitoring": self.is_monitoring,
        }
