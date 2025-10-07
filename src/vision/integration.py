"""
Vision System Integration - V2 Compliant
========================================

Main integration class for the vision system.
Coordinates screen capture, OCR, and visual analysis with V2's infrastructure.

V2 Compliance: ≤400 lines, SOLID principles, comprehensive error handling.

Author: Agent-1 - Vision & Automation Specialist
License: MIT
"""

import json
import time
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union
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

from .capture import ScreenCapture
from .ocr import TextExtractor
from .analysis import VisualAnalyzer


class VisionSystem:
    """
    Main vision system integration class.
    
    Coordinates screen capture, OCR, and visual analysis capabilities
    with V2's coordinate system and configuration management.
    """

    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize vision system.
        
        Args:
            config: Configuration dictionary (uses config/vision.yml if None)
        """
        self.config = config or {}
        self.logger = get_logger(__name__)
        
        # V2 Integration
        self.coordinate_loader = get_coordinate_loader()
        self.unified_config = get_unified_config()
        
        # Initialize components
        self.screen_capture = ScreenCapture(self.config)
        self.text_extractor = TextExtractor(self.config)
        self.visual_analyzer = VisualAnalyzer(self.config)
        
        # Integration settings
        integration_config = self.config.get('integration', {})
        self.coordinate_based_regions = integration_config.get('coordinate_based_regions', True)
        self.callback_enabled = integration_config.get('callback_enabled', True)
        self.data_persistence = integration_config.get('data_persistence', True)
        self.max_analysis_history = integration_config.get('max_analysis_history', 100)
        
        # State
        self.analysis_history = []
        self.is_monitoring = False
        self.monitoring_callback = None
        
        # Data persistence
        if self.data_persistence:
            self.data_directory = Path("runtime/vision_data")
            self.data_directory.mkdir(parents=True, exist_ok=True)
        
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
            if agent_id and self.coordinate_based_regions:
                image = self.screen_capture.capture_agent_region(agent_id)
            elif region:
                image = self.screen_capture.capture_screen(region)
            else:
                image = self.screen_capture.capture_screen()
            
            if image is None:
                return {
                    'success': False,
                    'error': 'Screen capture failed',
                    'timestamp': time.time()
                }
            
            # Perform analysis
            analysis = {
                'success': True,
                'timestamp': time.time(),
                'image_shape': image.shape,
                'capture_method': 'agent_region' if agent_id else 'region' if region else 'full_screen',
                'agent_id': agent_id,
                'region': region
            }
            
            # Visual analysis
            visual_analysis = self.visual_analyzer.analyze_screen_content(image)
            analysis.update(visual_analysis)
            
            # OCR analysis
            if include_ocr:
                ocr_results = self.text_extractor.extract_text_with_regions(image)
                analysis['ocr'] = ocr_results
            
            # UI detection
            if include_ui_detection:
                analysis['ui_elements'] = self.visual_analyzer.detect_ui_elements(image)
            
            # Store in history
            if self.data_persistence:
                self._store_analysis(analysis)
            
            self.logger.info("Screen capture and analysis completed")
            return analysis
            
        except Exception as e:
            self.logger.error(f"Capture and analysis failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': time.time()
            }

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
            frequency: Capture frequency override
        """
        if self.is_monitoring:
            self.logger.warning("Monitoring already active")
            return
        
        self.is_monitoring = True
        self.monitoring_callback = callback
        
        # Override frequency if specified
        if frequency:
            self.screen_capture.capture_frequency = frequency
        
        self.logger.info(f"Starting vision monitoring for {duration or 'indefinite'} seconds")
        
        try:
            self.screen_capture.continuous_capture(
                callback_func=self._monitoring_callback_wrapper,
                duration=duration,
                agent_id=agent_id
            )
        except Exception as e:
            self.logger.error(f"Monitoring failed: {e}")
        finally:
            self.is_monitoring = False
            self.monitoring_callback = None
            self.logger.info("Vision monitoring stopped")

    def stop_monitoring(self) -> None:
        """Stop continuous monitoring."""
        if self.is_monitoring:
            self.screen_capture.stop_monitoring()
            self.is_monitoring = False
            self.monitoring_callback = None
            self.logger.info("Monitoring stopped")

    def _monitoring_callback_wrapper(self, image) -> None:
        """Wrapper for monitoring callback with analysis."""
        try:
            if self.monitoring_callback:
                # Perform quick analysis
                analysis = self.capture_and_analyze(image=image, include_ocr=False)
                
                # Call user callback
                self.monitoring_callback(analysis)
        except Exception as e:
            self.logger.error(f"Monitoring callback failed: {e}")

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
            if agent_id and self.coordinate_based_regions:
                current_image = self.screen_capture.capture_agent_region(agent_id)
            elif region:
                current_image = self.screen_capture.capture_screen(region)
            else:
                current_image = self.screen_capture.capture_screen()
            
            if current_image is None:
                return {
                    'success': False,
                    'error': 'Screen capture failed',
                    'timestamp': time.time()
                }
            
            # Get previous image from history
            previous_image = self._get_previous_image(agent_id, region)
            
            if previous_image is None:
                # No previous image to compare with
                self._store_previous_image(current_image, agent_id, region)
                return {
                    'success': True,
                    'changes_detected': False,
                    'reason': 'No previous image for comparison',
                    'timestamp': time.time()
                }
            
            # Detect changes
            changes = self.visual_analyzer.detect_changes(previous_image, current_image, threshold)
            
            # Store current image for next comparison
            self._store_previous_image(current_image, agent_id, region)
            
            return {
                'success': True,
                'timestamp': time.time(),
                **changes
            }
            
        except Exception as e:
            self.logger.error(f"Change detection failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': time.time()
            }

    def _store_analysis(self, analysis: Dict[str, Any]) -> None:
        """Store analysis in history and optionally to disk."""
        # Add to memory history
        self.analysis_history.append(analysis)
        
        # Limit history size
        if len(self.analysis_history) > self.max_analysis_history:
            self.analysis_history = self.analysis_history[-self.max_analysis_history:]
        
        # Store to disk if persistence enabled
        if self.data_persistence and self.data_directory:
            try:
                timestamp = int(analysis['timestamp'])
                filename = self.data_directory / f"analysis_{timestamp}.json"
                
                with open(filename, 'w') as f:
                    json.dump(analysis, f, indent=2, default=str)
                    
            except Exception as e:
                self.logger.warning(f"Failed to store analysis to disk: {e}")

    def _get_previous_image(self, agent_id: Optional[str], region: Optional[tuple]) -> Optional[Any]:
        """Get previous image for change detection."""
        # Simple in-memory storage for previous images
        key = f"{agent_id or 'global'}_{region or 'full'}"
        return getattr(self, f'_previous_image_{key}', None)

    def _store_previous_image(self, image: Any, agent_id: Optional[str], region: Optional[tuple]) -> None:
        """Store previous image for change detection."""
        key = f"{agent_id or 'global'}_{region or 'full'}"
        setattr(self, f'_previous_image_{key}', image)

    def get_vision_capabilities(self) -> Dict[str, Any]:
        """Get information about vision system capabilities."""
        return {
            'screen_capture': self.screen_capture.get_capture_info(),
            'ocr': self.text_extractor.get_ocr_info(),
            'visual_analysis': self.visual_analyzer.get_analysis_info(),
            'integration': {
                'coordinate_loader_available': self.coordinate_loader is not None,
                'coordinate_based_regions': self.coordinate_based_regions,
                'callback_enabled': self.callback_enabled,
                'data_persistence': self.data_persistence,
                'is_monitoring': self.is_monitoring,
                'analysis_history_size': len(self.analysis_history),
                'max_analysis_history': self.max_analysis_history,
            }
        }

    def save_vision_data(self, analysis: Dict[str, Any], filename: str) -> bool:
        """
        Save vision analysis data to file.
        
        Args:
            analysis: Analysis data to save
            filename: Output filename
            
        Returns:
            True if successful, False otherwise
        """
        try:
            filepath = Path(filename)
            filepath.parent.mkdir(parents=True, exist_ok=True)
            
            with open(filepath, 'w') as f:
                json.dump(analysis, f, indent=2, default=str)
            
            self.logger.info(f"Vision data saved to {filename}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save vision data: {e}")
            return False

    def cleanup_old_data(self, max_age_days: int = 7) -> int:
        """
        Clean up old vision data files.
        
        Args:
            max_age_days: Maximum age of files to keep
            
        Returns:
            Number of files cleaned up
        """
        if not self.data_persistence or not self.data_directory:
            return 0
        
        try:
            current_time = time.time()
            max_age_seconds = max_age_days * 24 * 60 * 60
            cleaned_count = 0
            
            for file_path in self.data_directory.glob("analysis_*.json"):
                if file_path.stat().st_mtime < current_time - max_age_seconds:
                    file_path.unlink()
                    cleaned_count += 1
            
            self.logger.info(f"Cleaned up {cleaned_count} old vision data files")
            return cleaned_count
            
        except Exception as e:
            self.logger.error(f"Failed to cleanup old data: {e}")
            return 0
