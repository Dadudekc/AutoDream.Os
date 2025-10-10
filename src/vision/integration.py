"""
Vision System Integration - V2 Compliant Orchestrator
====================================================

Main integration orchestrator for the vision system.
Coordinates screen capture, OCR, and visual analysis with V2's infrastructure.

V2 Compliance: ≤200 lines, orchestrator pattern, SOLID principles.

Author: Agent-1 - Vision & Automation Specialist
Refactored: Agent-7 - Repository Cloning Specialist (V2 consolidation)
License: MIT
"""

import time
from typing import Any, Callable, Dict, Optional
import logging

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
        return type('MockConfig', (), {'get_env': lambda x, y=None: y})()
    
    def get_logger(name):
        return logging.getLogger(name)

# Import vision components
from .capture import ScreenCapture
from .ocr import TextExtractor
from .analysis import VisualAnalyzer
from .persistence import VisionPersistence
from .monitoring import VisionMonitoring


class VisionSystem:
    """
    Main vision system integration orchestrator.
    
    Coordinates specialized vision components:
    - ScreenCapture: Screen and region capture
    - TextExtractor: OCR capabilities
    - VisualAnalyzer: Visual analysis and UI detection
    - VisionPersistence: Data storage and history
    - VisionMonitoring: Continuous monitoring
    
    Provides unified interface for vision capabilities.
    """

    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize vision system orchestrator.
        
        Args:
            config: Configuration dictionary (uses config/vision.yml if None)
        """
        self.config = config or {}
        self.logger = get_logger(__name__)
        
        # V2 Integration
        self.coordinate_loader = get_coordinate_loader()
        self.unified_config = get_unified_config()
        
        # Initialize core components
        self.screen_capture = ScreenCapture(self.config)
        self.text_extractor = TextExtractor(self.config)
        self.visual_analyzer = VisualAnalyzer(self.config)
        
        # Initialize support modules
        integration_config = self.config.get('integration', {})
        self.persistence = VisionPersistence({
            'max_analysis_history': integration_config.get('max_analysis_history', 100),
            'data_persistence': integration_config.get('data_persistence', True)
        })
        
        self.monitoring = VisionMonitoring({
            'monitoring_frequency': integration_config.get('monitoring_frequency', 1.0)
        })
        
        # Integration settings
        self.coordinate_based_regions = integration_config.get('coordinate_based_regions', True)
        
        self.logger.info("Vision System initialized")

    def capture_and_analyze(
        self,
        region: Optional[tuple] = None,
        agent_id: Optional[str] = None,
        include_ocr: bool = True,
        include_ui_detection: bool = True
    ) -> Dict[str, Any]:
        """
        Capture screen and perform comprehensive analysis.
        
        Args:
            region: (x, y, width, height) for region capture
            agent_id: Agent ID for coordinate-based capture
            include_ocr: Whether to include OCR analysis
            include_ui_detection: Whether to include UI element detection
            
        Returns:
            Dictionary with complete analysis results
        """
        try:
            # Capture screen
            image = self._capture_image(agent_id, region)
            
            if image is None:
                return self._error_result('Screen capture failed')
            
            # Build analysis result
            analysis = {
                'success': True,
                'timestamp': time.time(),
                'image_shape': image.shape,
                'capture_method': self._get_capture_method(agent_id, region),
                'agent_id': agent_id,
                'region': region
            }
            
            # Visual analysis
            visual_analysis = self.visual_analyzer.analyze_screen_content(image)
            analysis.update(visual_analysis)
            
            # OCR analysis
            if include_ocr:
                analysis['ocr'] = self.text_extractor.extract_text_with_regions(image)
            
            # UI detection
            if include_ui_detection:
                analysis['ui_elements'] = self.visual_analyzer.detect_ui_elements(image)
            
            # Store in history
            self.persistence.store_analysis(analysis)
            
            self.logger.info("Screen capture and analysis completed")
            return analysis
            
        except Exception as e:
            self.logger.error(f"Capture and analysis failed: {e}")
            return self._error_result(str(e))

    def start_monitoring(
        self,
        callback: Callable[[Dict[str, Any]], None],
        duration: Optional[int] = None,
        agent_id: Optional[str] = None,
        frequency: Optional[float] = None
    ) -> None:
        """
        Start continuous monitoring with callback.
        
        Args:
            callback: Function to call with analysis results
            duration: Duration in seconds (None for indefinite)
            agent_id: Agent ID for monitoring specific region
            frequency: Capture frequency override (Hz)
        """
        # Create capture and analysis functions
        def capture_func():
            return self._capture_image(agent_id, None)
        
        def analysis_func(image):
            return self.visual_analyzer.analyze_screen_content(image)
        
        # Start monitoring
        self.monitoring.start_monitoring(
            capture_func=capture_func,
            analysis_func=analysis_func,
            callback=callback,
            duration=duration,
            frequency=frequency
        )

    def stop_monitoring(self) -> None:
        """Stop continuous monitoring."""
        self.monitoring.stop_monitoring()

    def detect_changes(
        self,
        agent_id: Optional[str] = None,
        region: Optional[tuple] = None,
        threshold: float = 0.1
    ) -> Dict[str, Any]:
        """
        Detect changes in screen content.
        
        Args:
            agent_id: Agent ID for coordinate-based capture
            region: Region for change detection
            threshold: Change detection threshold
            
        Returns:
            Change detection results
        """
        try:
            # Capture current screen
            current_image = self._capture_image(agent_id, region)
            
            if current_image is None:
                return self._error_result('Screen capture failed')
            
            # Get previous image
            previous_image = self.persistence.get_previous_image(agent_id, region)
            
            if previous_image is None:
                # No previous image to compare
                self.persistence.store_previous_image(current_image, agent_id, region)
                return {
                    'success': True,
                    'changes_detected': False,
                    'reason': 'No previous image for comparison',
                    'timestamp': time.time()
                }
            
            # Detect changes
            changes = self.visual_analyzer.detect_changes(previous_image, current_image, threshold)
            
            # Store current image for next comparison
            self.persistence.store_previous_image(current_image, agent_id, region)
            
            return {
                'success': True,
                'timestamp': time.time(),
                **changes
            }
            
        except Exception as e:
            self.logger.error(f"Change detection failed: {e}")
            return self._error_result(str(e))

    def _capture_image(self, agent_id: Optional[str], region: Optional[tuple]):
        """Capture image based on agent_id or region."""
        if agent_id and self.coordinate_based_regions:
            return self.screen_capture.capture_agent_region(agent_id)
        elif region:
            return self.screen_capture.capture_screen(region)
        else:
            return self.screen_capture.capture_screen()
    
    def _get_capture_method(self, agent_id: Optional[str], region: Optional[tuple]) -> str:
        """Get description of capture method used."""
        if agent_id:
            return 'agent_region'
        elif region:
            return 'region'
        else:
            return 'full_screen'
    
    def _error_result(self, error_message: str) -> Dict[str, Any]:
        """Create standardized error result."""
        return {
            'success': False,
            'error': error_message,
            'timestamp': time.time()
        }

    # Delegate persistence methods
    def save_vision_data(self, analysis: Dict[str, Any], filename: str) -> bool:
        """Save vision analysis data to JSON file."""
        return self.persistence.save_vision_data(analysis, filename)
    
    def cleanup_old_data(self, max_age_days: int = 7) -> int:
        """Clean up old vision data files."""
        return self.persistence.cleanup_old_data(max_age_days)
    
    def get_vision_capabilities(self) -> Dict[str, Any]:
        """Get information about vision system capabilities."""
        return {
            'screen_capture': self.screen_capture.get_capture_info(),
            'text_extraction': self.text_extractor.get_extractor_info(),
            'visual_analysis': self.visual_analyzer.get_analysis_info(),
            'persistence': self.persistence.get_persistence_info(),
            'monitoring': self.monitoring.get_monitoring_status(),
            'coordinate_based_regions': self.coordinate_based_regions,
            'version': '2.1.0'  # V2 consolidation version
        }
