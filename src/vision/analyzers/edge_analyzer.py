"""
Edge Analyzer
============

Analyzes edge content in images using Canny edge detection and provides
edge density and distribution metrics.

V2 Compliance: ≤200 lines, single responsibility, comprehensive error handling.

Author: Agent-7 - Repository Cloning Specialist (extracted from vision/analysis.py)
License: MIT
"""

import logging

import numpy as np

try:
    import cv2

    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False
    logging.warning("OpenCV not available - edge analysis disabled")


class EdgeAnalyzer:
    """
    Analyzes edge content and distribution in images.

    Capabilities:
    - Canny edge detection
    - Edge density calculation
    - Edge distribution analysis
    """

    def __init__(self, config: dict = None):
        """
        Initialize edge analyzer.

        Args:
            config: Configuration dictionary with analysis settings
        """
        self.config = config or {}
        self.logger = logging.getLogger(__name__)

        # Edge detection thresholds
        self.low_threshold = self.config.get("low_threshold", 50)
        self.high_threshold = self.config.get("high_threshold", 150)

        if not OPENCV_AVAILABLE:
            self.logger.warning("Edge analysis disabled - OpenCV not available")

    def analyze_edges(self, image: np.ndarray) -> dict:
        """
        Analyze edge content in the image.

        Args:
            image: Input image array (RGB or grayscale)

        Returns:
            Dictionary with edge analysis results:
            - edge_density: Ratio of edge pixels to total pixels
            - edge_pixels: Number of edge pixels
            - total_pixels: Total number of pixels
        """
        if not OPENCV_AVAILABLE:
            return {}

        try:
            # Convert to grayscale
            gray = self._convert_to_grayscale(image)

            # Detect edges
            edges = cv2.Canny(gray, self.low_threshold, self.high_threshold)

            # Calculate metrics
            total_pixels = edges.size
            edge_pixels = np.count_nonzero(edges)
            edge_density = edge_pixels / total_pixels if total_pixels > 0 else 0.0

            return {
                "edge_density": edge_density,
                "edge_pixels": edge_pixels,
                "total_pixels": total_pixels,
            }
        except Exception as e:
            self.logger.error(f"Edge analysis failed: {e}")
            return {}

    def _convert_to_grayscale(self, image: np.ndarray) -> np.ndarray:
        """Convert image to grayscale if needed."""
        if len(image.shape) == 3:
            return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        return image.copy()

    def get_analyzer_info(self) -> dict:
        """
        Get analyzer configuration and capabilities.

        Returns:
            Dictionary with analyzer information
        """
        return {
            "opencv_available": OPENCV_AVAILABLE,
            "edge_thresholds": {"low": self.low_threshold, "high": self.high_threshold},
        }
