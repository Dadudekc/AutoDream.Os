"""
Change Detector
==============

Detects changes between two images and identifies change regions.
Uses frame differencing and thresholding to find significant changes.

V2 Compliance: ≤200 lines, single responsibility, comprehensive error handling.

Author: Agent-7 - Repository Cloning Specialist (extracted from vision/analysis.py)
License: MIT
"""

import logging
import time

import numpy as np

try:
    import cv2

    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False
    logging.warning("OpenCV not available - change detection disabled")


class ChangeDetector:
    """
    Detects visual changes between two images.

    Capabilities:
    - Frame differencing
    - Change region detection
    - Change percentage calculation
    - Configurable sensitivity
    """

    def __init__(self, config: dict = None):
        """
        Initialize change detector.

        Args:
            config: Configuration dictionary with detection settings
        """
        self.config = config or {}
        self.logger = logging.getLogger(__name__)

        # Detection settings
        self.default_threshold = self.config.get("default_threshold", 0.1)
        self.diff_threshold = self.config.get("diff_threshold", 30)
        self.min_region_size = self.config.get("min_region_size", 10)

        if not OPENCV_AVAILABLE:
            self.logger.warning("Change detection disabled - OpenCV not available")

    def detect_changes(
        self, image1: np.ndarray, image2: np.ndarray, threshold: float = None
    ) -> dict:
        """
        Detect changes between two images.

        Args:
            image1: First image
            image2: Second image
            threshold: Change detection threshold (0.0 to 1.0)
                      If None, uses default_threshold from config

        Returns:
            Dictionary with change detection results:
            - changes_detected: Boolean indicating if changes found
            - change_percentage: Percentage of pixels that changed
            - change_regions: List of change region bounding boxes
            - threshold_used: Threshold value used
            - timestamp: Detection timestamp
        """
        if not OPENCV_AVAILABLE:
            return {"changes_detected": False, "reason": "OpenCV not available"}

        threshold = threshold if threshold is not None else self.default_threshold

        try:
            # Resize if needed
            if image1.shape != image2.shape:
                image2 = cv2.resize(image2, (image1.shape[1], image1.shape[0]))

            # Convert to grayscale
            gray1 = self._convert_to_grayscale(image1)
            gray2 = self._convert_to_grayscale(image2)

            # Calculate difference
            diff = cv2.absdiff(gray1, gray2)

            # Apply threshold
            _, thresh = cv2.threshold(diff, self.diff_threshold, 255, cv2.THRESH_BINARY)

            # Calculate change percentage
            total_pixels = thresh.size
            changed_pixels = np.count_nonzero(thresh)
            change_percentage = changed_pixels / total_pixels if total_pixels > 0 else 0.0

            # Determine if significant changes occurred
            changes_detected = change_percentage > threshold

            # Find change regions
            change_regions = []
            if changes_detected:
                change_regions = self._find_change_regions(thresh)

            return {
                "changes_detected": changes_detected,
                "change_percentage": change_percentage,
                "change_regions": change_regions,
                "threshold_used": threshold,
                "timestamp": time.time(),
            }

        except Exception as e:
            self.logger.error(f"Change detection failed: {e}")
            return {"changes_detected": False, "error": str(e)}

    def _convert_to_grayscale(self, image: np.ndarray) -> np.ndarray:
        """Convert image to grayscale if needed."""
        if len(image.shape) == 3:
            return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        return image.copy()

    def _find_change_regions(self, thresh: np.ndarray) -> list[dict]:
        """
        Find regions where changes occurred.

        Args:
            thresh: Thresholded difference image

        Returns:
            List of change region dictionaries
        """
        change_regions = []

        # Find contours of changed regions
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Process each contour
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)

            # Filter by minimum region size
            if w > self.min_region_size and h > self.min_region_size:
                change_regions.append(
                    {"position": (x, y), "size": (w, h), "bbox": (x, y, x + w, y + h)}
                )

        return change_regions

    def get_detector_info(self) -> dict:
        """
        Get detector configuration and capabilities.

        Returns:
            Dictionary with detector information
        """
        return {
            "opencv_available": OPENCV_AVAILABLE,
            "default_threshold": self.default_threshold,
            "diff_threshold": self.diff_threshold,
            "min_region_size": self.min_region_size,
        }
