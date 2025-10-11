"""
UI Element Detector
==================

Detects UI elements like buttons, text fields, icons, and containers using
computer vision and contour analysis.

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
    logging.warning("OpenCV not available - UI detection disabled")


class UIDetector:
    """
    Detects and classifies UI elements in images.

    Capabilities:
    - Button detection
    - Text field detection
    - Icon detection
    - Container detection
    - Shape-based classification
    """

    def __init__(self, config: dict = None):
        """
        Initialize UI detector.

        Args:
            config: Configuration dictionary with detection settings
        """
        self.config = config or {}
        self.logger = logging.getLogger(__name__)

        # Detection settings
        self.min_element_area = self.config.get("min_element_area", 100)
        self.contour_approximation = self.config.get("contour_approximation", 0.02)

        # Edge detection thresholds
        self.low_threshold = self.config.get("low_threshold", 50)
        self.high_threshold = self.config.get("high_threshold", 150)

        if not OPENCV_AVAILABLE:
            self.logger.warning("UI detection disabled - OpenCV not available")

    def detect_ui_elements(self, image: np.ndarray) -> list[dict]:
        """
        Detect UI elements in an image.

        Args:
            image: Input image array (RGB or grayscale)

        Returns:
            List of dictionaries with detected UI elements:
            - type: Element type (button, text_field, icon, etc.)
            - position: (x, y) top-left corner
            - size: (width, height)
            - area: Contour area
            - confidence: Detection confidence (0.0 to 1.0)
        """
        if not OPENCV_AVAILABLE:
            self.logger.warning("UI detection disabled - OpenCV not available")
            return []

        try:
            ui_elements = []

            # Convert to grayscale
            gray = self._convert_to_grayscale(image)

            # Detect edges
            edges = cv2.Canny(gray, self.low_threshold, self.high_threshold)

            # Find contours
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Process each contour
            for contour in contours:
                element = self._process_contour(contour)
                if element:
                    ui_elements.append(element)

            self.logger.info(f"Detected {len(ui_elements)} UI elements")
            return ui_elements

        except Exception as e:
            self.logger.error(f"UI detection failed: {e}")
            return []

    def _convert_to_grayscale(self, image: np.ndarray) -> np.ndarray:
        """Convert image to grayscale if needed."""
        if len(image.shape) == 3:
            return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        return image.copy()

    def _process_contour(self, contour: np.ndarray) -> dict:
        """
        Process a single contour and extract UI element information.

        Args:
            contour: OpenCV contour

        Returns:
            Dictionary with element info, or None if filtered out
        """
        # Calculate area
        area = cv2.contourArea(contour)

        # Filter by minimum area
        if area < self.min_element_area:
            return None

        # Approximate contour to polygon
        epsilon = self.contour_approximation * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        # Get bounding rectangle
        x, y, w, h = cv2.boundingRect(contour)

        # Classify element type
        element_type = self._classify_element(approx, area, w, h)

        return {
            "type": element_type,
            "position": (x, y),
            "size": (w, h),
            "area": area,
            "corners": len(approx),
            "bbox": (x, y, x + w, y + h),
            "contour_points": approx.tolist(),
            "confidence": min(1.0, area / 1000.0),  # Simple area-based confidence
        }

    def _classify_element(self, approx: np.ndarray, area: float, width: int, height: int) -> str:
        """
        Classify UI element type based on shape characteristics.

        Args:
            approx: Approximated contour polygon
            area: Contour area
            width: Bounding box width
            height: Bounding box height

        Returns:
            Element type string (button, text_field, icon, container, element)
        """
        corners = len(approx)
        aspect_ratio = width / height if height > 0 else 1.0

        # Rectangle-based classification
        if corners == 4:
            if 0.8 <= aspect_ratio <= 1.2:  # Square-ish
                return "button" if area > 500 else "icon"
            else:  # Rectangular
                return "text_field" if height > 30 else "button"

        # Complex shapes
        elif corners > 4:
            return "container"

        # Simple shapes
        else:
            return "element"

    def get_detector_info(self) -> dict:
        """
        Get detector configuration and capabilities.

        Returns:
            Dictionary with detector information
        """
        return {
            "opencv_available": OPENCV_AVAILABLE,
            "min_element_area": self.min_element_area,
            "contour_approximation": self.contour_approximation,
            "edge_thresholds": {"low": self.low_threshold, "high": self.high_threshold},
        }
