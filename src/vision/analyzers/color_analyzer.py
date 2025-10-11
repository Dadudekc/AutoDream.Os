"""
Color Analyzer
=============

Analyzes color distribution and statistics in images. Handles both color
and grayscale images.

V2 Compliance: ≤200 lines, single responsibility, comprehensive error handling.

Author: Agent-7 - Repository Cloning Specialist (extracted from vision/analysis.py)
License: MIT
"""

import logging
from typing import Dict
import numpy as np


class ColorAnalyzer:
    """
    Analyzes color distribution and statistics in images.
    
    Capabilities:
    - Mean color calculation (RGB)
    - Mean intensity calculation (grayscale)
    - Color channel analysis
    """
    
    def __init__(self, config: Dict = None):
        """
        Initialize color analyzer.
        
        Args:
            config: Configuration dictionary (reserved for future use)
        """
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
    
    def analyze_colors(self, image: np.ndarray) -> Dict:
        """
        Analyze color distribution in the image.
        
        Args:
            image: Input image array (RGB or grayscale)
            
        Returns:
            Dictionary with color analysis results:
            For RGB images:
            - mean_colors: List of mean values per channel
            - color_channels: Number of color channels (3)
            
            For grayscale images:
            - mean_intensity: Mean intensity value
            - color_channels: Number of color channels (1)
        """
        try:
            if len(image.shape) == 3:
                # RGB image
                return self._analyze_rgb_image(image)
            else:
                # Grayscale image
                return self._analyze_grayscale_image(image)
        except Exception as e:
            self.logger.error(f"Color analysis failed: {e}")
            return {}
    
    def _analyze_rgb_image(self, image: np.ndarray) -> Dict:
        """
        Analyze RGB color image.
        
        Args:
            image: RGB image array
            
        Returns:
            Dictionary with RGB color analysis
        """
        # Calculate mean color values across all channels
        mean_colors = np.mean(image, axis=(0, 1))
        
        return {
            'mean_colors': mean_colors.tolist(),
            'color_channels': image.shape[2]
        }
    
    def _analyze_grayscale_image(self, image: np.ndarray) -> Dict:
        """
        Analyze grayscale image.
        
        Args:
            image: Grayscale image array
            
        Returns:
            Dictionary with grayscale intensity analysis
        """
        mean_intensity = np.mean(image)
        
        return {
            'mean_intensity': float(mean_intensity),
            'color_channels': 1
        }
    
    def get_analyzer_info(self) -> Dict:
        """
        Get analyzer configuration and capabilities.
        
        Returns:
            Dictionary with analyzer information
        """
        return {
            'supported_formats': ['RGB', 'grayscale'],
            'metrics': ['mean_colors', 'mean_intensity', 'color_channels']
        }

