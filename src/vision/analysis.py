"""
Visual Analysis - V2 Compliant Orchestrator
==========================================

Visual analysis orchestrator that coordinates specialized analyzer modules.
Provides a unified interface for computer vision capabilities.

V2 Compliance: ≤200 lines, orchestrator pattern, SOLID principles.

Author: Agent-1 - Vision & Automation Specialist
Refactored: Agent-7 - Repository Cloning Specialist (V2 consolidation)
License: MIT
"""

import time
import logging
from typing import Dict, List, Optional, Tuple
import numpy as np

# Optional dependencies
try:
    import cv2
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

# Import specialized analyzers
from .analyzers import UIDetector, EdgeAnalyzer, ColorAnalyzer, ChangeDetector


class VisualAnalyzer:
    """
    Visual analysis orchestrator for UI elements and screen content.
    
    Coordinates specialized analyzer modules:
    - UIDetector: UI element detection
    - EdgeAnalyzer: Edge detection and analysis
    - ColorAnalyzer: Color distribution analysis
    - ChangeDetector: Visual change detection
    
    Provides backward-compatible interface with original VisualAnalyzer.
    """

    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize visual analyzer orchestrator.
        
        Args:
            config: Configuration dictionary (uses config/vision.yml if None)
        """
        self.config = config or {}
        self.logger = get_logger(__name__)
        
        # V2 Integration
        self.unified_config = get_unified_config()
        
        # Get analysis configuration
        analysis_config = self.config.get('analysis', {})
        
        # Initialize specialized analyzers
        self.ui_detector = UIDetector({
            'min_element_area': analysis_config.get('min_element_area', 100),
            'contour_approximation': analysis_config.get('contour_approximation', 0.02),
            'low_threshold': analysis_config.get('edge_detection', {}).get('low_threshold', 50),
            'high_threshold': analysis_config.get('edge_detection', {}).get('high_threshold', 150)
        })
        
        self.edge_analyzer = EdgeAnalyzer({
            'low_threshold': analysis_config.get('edge_detection', {}).get('low_threshold', 50),
            'high_threshold': analysis_config.get('edge_detection', {}).get('high_threshold', 150)
        })
        
        self.color_analyzer = ColorAnalyzer()
        
        self.change_detector = ChangeDetector({
            'default_threshold': 0.1,
            'diff_threshold': 30,
            'min_region_size': 10
        })
        
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
        return self.ui_detector.detect_ui_elements(image)

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
            'analysis_version': '2.1.0'  # Incremented for V2 consolidation
        }
        
        try:
            # Basic image statistics
            analysis.update(self._get_image_statistics(image))
            
            # UI element detection
            analysis['ui_elements'] = self.ui_detector.detect_ui_elements(image)
            
            # Edge analysis
            analysis.update(self.edge_analyzer.analyze_edges(image))
            
            # Color analysis
            analysis.update(self.color_analyzer.analyze_colors(image))
            
            # Layout analysis
            analysis.update(self._analyze_layout(image))
            
            self.logger.info("Screen content analysis completed")
            return analysis
            
        except Exception as e:
            self.logger.error(f"Screen content analysis failed: {e}")
            analysis['error'] = str(e)
            return analysis

    def detect_changes(
        self,
        image1: np.ndarray,
        image2: np.ndarray,
        threshold: float = 0.1
    ) -> Dict:
        """
        Detect changes between two images.
        
        Args:
            image1: First image
            image2: Second image
            threshold: Change detection threshold (0.0 to 1.0)
            
        Returns:
            Dictionary with change detection results
        """
        return self.change_detector.detect_changes(image1, image2, threshold)

    def _get_image_statistics(self, image: np.ndarray) -> Dict:
        """Get basic image statistics."""
        return {
            'width': image.shape[1],
            'height': image.shape[0],
            'channels': image.shape[2] if len(image.shape) == 3 else 1,
            'dtype': str(image.dtype),
            'total_pixels': image.size
        }

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
            "analyzers": {
                "ui_detector": self.ui_detector.get_detector_info(),
                "edge_analyzer": self.edge_analyzer.get_analyzer_info(),
                "color_analyzer": self.color_analyzer.get_analyzer_info(),
                "change_detector": self.change_detector.get_detector_info()
            },
            "analysis_cache_size": self.analysis_cache_size,
            "version": "2.1.0"  # V2 consolidation version
        }
