"""
Screen Capture - V2 Compliant
============================

Screen capture functionality with coordinate-based region targeting.
Integrates with V2's coordinate system for agent-specific screen regions.

V2 Compliance: ≤400 lines, SOLID principles, comprehensive error handling.

Author: Agent-1 - Vision & Automation Specialist
License: MIT
"""

import logging
import time
from pathlib import Path

# Optional dependencies for screen capture
try:
    import numpy as np
    from PIL import Image, ImageGrab

    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    logging.warning("PIL/Pillow not available - screen capture disabled")

# V2 Integration imports
try:
    from ..core.coordinate_loader import get_coordinate_loader
    from ..core.unified_config import get_unified_config
    from ..core.unified_logging_system import get_logger
except ImportError as e:
    logging.warning(f"V2 integration imports failed: {e}")

    # Fallback implementations
    def get_coordinate_loader():
        return None

    def get_unified_config():
        return type("MockConfig", (), {"get_env": lambda x, y=None: y})()

    def get_logger(name):
        return logging.getLogger(name)


class ScreenCapture:
    """
    Screen capture functionality with coordinate integration.

    Provides screen capture capabilities with support for:
    - Full screen capture
    - Region-based capture using coordinates
    - Agent-specific region capture
    - Continuous monitoring mode
    """

    def __init__(self, config: dict | None = None):
        """
        Initialize screen capture system.

        Args:
            config: Configuration dictionary (uses config/vision.yml if None)
        """
        self.config = config or {}
        self.logger = get_logger(__name__)

        # V2 Integration
        self.coordinate_loader = get_coordinate_loader()
        self.unified_config = get_unified_config()

        # Capture settings
        self.capture_region = self.config.get("capture", {}).get("region")
        self.capture_frequency = self.config.get("capture", {}).get("frequency", 1.0)
        self.capture_format = self.config.get("capture", {}).get("format", "RGB")
        self.capture_quality = self.config.get("capture", {}).get("quality", 95)

        # Performance settings
        self.max_concurrent_captures = self.config.get("performance", {}).get(
            "max_concurrent_captures", 3
        )
        self.capture_queue_size = self.config.get("performance", {}).get("capture_queue_size", 10)

        # State
        self.capture_queue = []
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
            if region:
                # Region capture
                x, y, width, height = region
                bbox = (x, y, x + width, y + height)
                screenshot = ImageGrab.grab(bbox=bbox)
            else:
                # Full screen capture
                screenshot = ImageGrab.grab()

            # Convert to numpy array
            img_array = np.array(screenshot)

            # Convert color format if needed
            if self.capture_format == "L":  # Grayscale
                if len(img_array.shape) == 3:
                    img_array = np.mean(img_array, axis=2).astype(np.uint8)
            elif self.capture_format == "RGB":
                if len(img_array.shape) == 4:  # RGBA
                    img_array = img_array[:, :, :3]  # Remove alpha channel

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
            self.logger.warning("Coordinate loader not available - using fallback region")
            return self._capture_fallback_region(agent_id)

        try:
            # Get agent coordinates
            coordinates = self.coordinate_loader.get_coordinates(agent_id)
            if not coordinates:
                self.logger.warning(f"No coordinates found for {agent_id} - using fallback")
                return self._capture_fallback_region(agent_id)

            # Create region around coordinates
            x, y = coordinates
            region_width = 400  # Default region size
            region_height = 300

            # Adjust region to stay within screen bounds
            region = (
                max(0, x - region_width // 2),
                max(0, y - region_height // 2),
                region_width,
                region_height,
            )

            return self.capture_screen(region)

        except Exception as e:
            self.logger.error(f"Agent region capture failed for {agent_id}: {e}")
            return self._capture_fallback_region(agent_id)

    def _capture_fallback_region(self, agent_id: str) -> np.ndarray | None:
        """Capture fallback region when coordinates are not available."""
        fallback_regions = self.config.get("coordinates", {}).get("fallback_regions", {})

        if agent_id in fallback_regions:
            region = fallback_regions[agent_id]
            return self.capture_screen(region)
        else:
            self.logger.warning(f"No fallback region for {agent_id} - using full screen")
            return self.capture_screen()

    def continuous_capture(
        self, callback_func, duration: int | None = None, agent_id: str | None = None
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
                if duration and (time.time() - start_time) > duration:
                    break

                # Capture screen
                if agent_id:
                    image = self.capture_agent_region(agent_id)
                else:
                    image = self.capture_screen()

                if image is not None:
                    # Call callback with image
                    try:
                        callback_func(image)
                    except Exception as e:
                        self.logger.error(f"Callback function failed: {e}")

                # Wait before next capture
                time.sleep(self.capture_frequency)

        except KeyboardInterrupt:
            self.logger.info("Continuous capture interrupted by user")
        except Exception as e:
            self.logger.error(f"Continuous capture failed: {e}")
        finally:
            self.is_monitoring = False
            self.logger.info("Continuous capture stopped")

    def stop_monitoring(self) -> None:
        """Stop continuous monitoring."""
        self.is_monitoring = False
        self.logger.info("Monitoring stopped")

    def save_image(self, image: np.ndarray, filename: str | Path, format: str = "PNG") -> bool:
        """
        Save captured image to file.

        Args:
            image: Image array to save
            filename: Output filename
            format: Image format (PNG, JPEG, etc.)

        Returns:
            True if successful, False otherwise
        """
        if not PIL_AVAILABLE:
            self.logger.error("Cannot save image: PIL not available")
            return False

        try:
            # Convert numpy array to PIL Image
            if len(image.shape) == 3:
                pil_image = Image.fromarray(image)
            else:
                pil_image = Image.fromarray(image, mode="L")

            # Save image
            pil_image.save(filename, format=format, quality=self.capture_quality)
            self.logger.info(f"Image saved: {filename}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to save image {filename}: {e}")
            return False

    def get_capture_info(self) -> dict[str, any]:
        """Get information about capture capabilities."""
        return {
            "pil_available": PIL_AVAILABLE,
            "coordinate_loader_available": self.coordinate_loader is not None,
            "capture_frequency": self.capture_frequency,
            "capture_format": self.capture_format,
            "capture_quality": self.capture_quality,
            "max_concurrent_captures": self.max_concurrent_captures,
            "is_monitoring": self.is_monitoring,
        }
