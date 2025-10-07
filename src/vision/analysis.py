"""
Visual Analysis - V2 Compliant
=============================

Visual analysis capabilities for UI element detection and screen content analysis.
Provides computer vision features for agent automation and monitoring.

V2 Compliance: ≤400 lines, SOLID principles, comprehensive error handling.

Author: Agent-1 - Vision & Automation Specialist
License: MIT
"""

import time
from typing import Dict, List, Optional, Tuple
import logging

# Optional dependencies for visual analysis
try:
    import cv2
    import numpy as np
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False
    logging.warning("OpenCV not available - visual analysis disabled")

# V2 Integration imports
try:
    from ..core.unified_config import get_unified_config
    from ..core.unified_logging_system import get_logger
except ImportError as e:
    logging.warning(f"V2 integration imports failed: {e}")
    # Fallback implementations
    def get_unified_config():
        return type('MockConfig', (), {'get_env': lambda x, y=None: y})()
    
    def get_logger(name):
        return logging.getLogger(name)


class VisualAnalyzer:
    """
    Visual analysis for UI elements and screen content.
    
    Provides computer vision capabilities with:
    - UI element detection (buttons, text fields, etc.)
    - Edge detection and contour analysis
    - Screen content analysis
    - Visual change detection
    """

    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize visual analyzer.
        
        Args:
            config: Configuration dictionary (uses config/vision.yml if None)
        """
        self.config = config or {}
        self.logger = get_logger(__name__)
        
        # V2 Integration
        self.unified_config = get_unified_config()
        
        # Analysis settings
        analysis_config = self.config.get('analysis', {})
        self.ui_detection_enabled = analysis_config.get('ui_element_detection', True)
        self.min_element_area = analysis_config.get('min_element_area', 100)
        self.contour_approximation = analysis_config.get('contour_approximation', 0.02)
        
        # Edge detection settings
        edge_config = analysis_config.get('edge_detection', {})
        self.low_threshold = edge_config.get('low_threshold', 50)
        self.high_threshold = edge_config.get('high_threshold', 150)
        
        # Performance settings
        self.analysis_cache_size = self.config.get('performance', {}).get('analysis_cache_size', 50)
        self.analysis_cache = {}
        
        if not OPENCV_AVAILABLE:
            self.logger.warning("Visual analysis disabled - OpenCV not available")

    def detect_ui_elements(self, image: np.ndarray) -> List[Dict]:
        """
        Detect UI elements like buttons, text fields, etc.
        
        Args:
            image: Input image array
            
        Returns:
            List of dictionaries with detected UI elements
        """
        if not OPENCV_AVAILABLE:
            self.logger.warning("UI detection disabled - OpenCV not available")
            return []
        
        if not self.ui_detection_enabled:
            return []
        
        try:
            ui_elements = []
            
            # Convert to grayscale
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            else:
                gray = image.copy()
            
            # Detect edges
            edges = cv2.Canny(gray, self.low_threshold, self.high_threshold)
            
            # Find contours
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                # Calculate area
                area = cv2.contourArea(contour)
                
                # Filter by minimum area
                if area < self.min_element_area:
                    continue
                
                # Approximate contour to polygon
                epsilon = self.contour_approximation * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)
                
                # Get bounding rectangle
                x, y, w, h = cv2.boundingRect(contour)
                
                # Classify element type based on shape
                element_type = self._classify_ui_element(approx, area, w, h)
                
                ui_element = {
                    'type': element_type,
                    'position': (x, y),
                    'size': (w, h),
                    'area': area,
                    'corners': len(approx),
                    'bbox': (x, y, x + w, y + h),
                    'contour_points': approx.tolist(),
                    'confidence': min(1.0, area / 1000.0)  # Simple confidence based on area
                }
                
                ui_elements.append(ui_element)
            
            self.logger.info(f"Detected {len(ui_elements)} UI elements")
            return ui_elements
            
        except Exception as e:
            self.logger.error(f"UI detection failed: {e}")
            return []

    def analyze_screen_content(self, image: np.ndarray) -> Dict:
        """
        Comprehensive screen content analysis.
        
        Args:
            image: Input image array
            
        Returns:
            Dictionary with complete analysis results
        """
        analysis = {
            'timestamp': time.time(),
            'image_shape': image.shape,
            'analysis_version': '2.0.0'
        }
        
        try:
            # Basic image statistics
            analysis.update(self._get_image_statistics(image))
            
            # UI element detection
            if self.ui_detection_enabled:
                analysis['ui_elements'] = self.detect_ui_elements(image)
            
            # Edge analysis
            if OPENCV_AVAILABLE:
                analysis.update(self._analyze_edges(image))
            
            # Color analysis
            analysis.update(self._analyze_colors(image))
            
            # Layout analysis
            analysis.update(self._analyze_layout(image))
            
            self.logger.info("Screen content analysis completed")
            return analysis
            
        except Exception as e:
            self.logger.error(f"Screen content analysis failed: {e}")
            analysis['error'] = str(e)
            return analysis

    def detect_changes(self, image1: np.ndarray, image2: np.ndarray, threshold: float = 0.1) -> Dict:
        """
        Detect changes between two images.
        
        Args:
            image1: First image
            image2: Second image
            threshold: Change detection threshold (0.0 to 1.0)
            
        Returns:
            Dictionary with change detection results
        """
        if not OPENCV_AVAILABLE:
            return {'changes_detected': False, 'reason': 'OpenCV not available'}
        
        try:
            # Ensure images are the same size
            if image1.shape != image2.shape:
                # Resize image2 to match image1
                image2 = cv2.resize(image2, (image1.shape[1], image1.shape[0]))
            
            # Convert to grayscale if needed
            if len(image1.shape) == 3:
                gray1 = cv2.cvtColor(image1, cv2.COLOR_RGB2GRAY)
            else:
                gray1 = image1.copy()
            
            if len(image2.shape) == 3:
                gray2 = cv2.cvtColor(image2, cv2.COLOR_RGB2GRAY)
            else:
                gray2 = image2.copy()
            
            # Calculate absolute difference
            diff = cv2.absdiff(gray1, gray2)
            
            # Apply threshold
            _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
            
            # Calculate change percentage
            total_pixels = thresh.size
            changed_pixels = np.count_nonzero(thresh)
            change_percentage = changed_pixels / total_pixels
            
            # Determine if significant changes occurred
            changes_detected = change_percentage > threshold
            
            # Find change regions
            change_regions = []
            if changes_detected:
                contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                for contour in contours:
                    x, y, w, h = cv2.boundingRect(contour)
                    if w > 10 and h > 10:  # Filter small changes
                        change_regions.append({
                            'position': (x, y),
                            'size': (w, h),
                            'bbox': (x, y, x + w, y + h)
                        })
            
            return {
                'changes_detected': changes_detected,
                'change_percentage': change_percentage,
                'change_regions': change_regions,
                'threshold_used': threshold,
                'timestamp': time.time()
            }
            
        except Exception as e:
            self.logger.error(f"Change detection failed: {e}")
            return {'changes_detected': False, 'error': str(e)}

    def _classify_ui_element(self, approx: np.ndarray, area: float, width: int, height: int) -> str:
        """Classify UI element type based on shape characteristics."""
        corners = len(approx)
        aspect_ratio = width / height if height > 0 else 1.0
        
        # Simple classification based on shape and size
        if corners == 4:  # Rectangle
            if 0.8 <= aspect_ratio <= 1.2:  # Square-ish
                return "button" if area > 500 else "icon"
            else:  # Rectangular
                return "text_field" if height > 30 else "button"
        elif corners > 4:  # More complex shape
            return "container"
        else:  # Simple shape
            return "element"

    def _get_image_statistics(self, image: np.ndarray) -> Dict:
        """Get basic image statistics."""
        return {
            'width': image.shape[1],
            'height': image.shape[0],
            'channels': image.shape[2] if len(image.shape) == 3 else 1,
            'dtype': str(image.dtype),
            'total_pixels': image.size
        }

    def _analyze_edges(self, image: np.ndarray) -> Dict:
        """Analyze edge content in the image."""
        if not OPENCV_AVAILABLE:
            return {}
        
        try:
            # Convert to grayscale
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            else:
                gray = image.copy()
            
            # Detect edges
            edges = cv2.Canny(gray, self.low_threshold, self.high_threshold)
            
            # Calculate edge density
            total_pixels = edges.size
            edge_pixels = np.count_nonzero(edges)
            edge_density = edge_pixels / total_pixels
            
            return {
                'edge_density': edge_density,
                'edge_pixels': edge_pixels,
                'total_pixels': total_pixels
            }
        except Exception as e:
            self.logger.error(f"Edge analysis failed: {e}")
            return {}

    def _analyze_colors(self, image: np.ndarray) -> Dict:
        """Analyze color distribution in the image."""
        try:
            if len(image.shape) == 3:
                # Calculate mean color values
                mean_colors = np.mean(image, axis=(0, 1))
                return {
                    'mean_colors': mean_colors.tolist(),
                    'color_channels': image.shape[2]
                }
            else:
                # Grayscale image
                mean_intensity = np.mean(image)
                return {
                    'mean_intensity': float(mean_intensity),
                    'color_channels': 1
                }
        except Exception as e:
            self.logger.error(f"Color analysis failed: {e}")
            return {}

    def _analyze_layout(self, image: np.ndarray) -> Dict:
        """Analyze layout structure of the image."""
        try:
            height, width = image.shape[:2]
            
            # Divide image into regions
            regions = {
                'top_left': (0, 0, width // 2, height // 2),
                'top_right': (width // 2, 0, width, height // 2),
                'bottom_left': (0, height // 2, width // 2, height),
                'bottom_right': (width // 2, height // 2, width, height),
                'center': (width // 4, height // 4, 3 * width // 4, 3 * height // 4)
            }
            
            return {
                'layout_regions': regions,
                'image_center': (width // 2, height // 2),
                'golden_ratio_points': [
                    (int(width * 0.382), int(height * 0.382)),
                    (int(width * 0.618), int(height * 0.618))
                ]
            }
        except Exception as e:
            self.logger.error(f"Layout analysis failed: {e}")
            return {}

    def get_analysis_info(self) -> Dict[str, any]:
        """Get information about analysis capabilities."""
        return {
            "opencv_available": OPENCV_AVAILABLE,
            "ui_detection_enabled": self.ui_detection_enabled,
            "min_element_area": self.min_element_area,
            "contour_approximation": self.contour_approximation,
            "edge_thresholds": {
                "low": self.low_threshold,
                "high": self.high_threshold
            },
            "analysis_cache_size": self.analysis_cache_size,
        }
