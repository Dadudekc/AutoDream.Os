"""
Vision Monitoring
================

Handles continuous monitoring and callback-based vision processing.
Provides real-time screen monitoring with customizable callbacks.

V2 Compliance: ≤200 lines, single responsibility, comprehensive error handling.

Author: Agent-7 - Repository Cloning Specialist (extracted from vision/integration.py)
License: MIT
"""

import logging
import time
from typing import Any, Callable, Dict, Optional
import numpy as np


class VisionMonitoring:
    """
    Manages continuous vision monitoring with callbacks.
    
    Capabilities:
    - Continuous screen monitoring
    - Callback-based processing
    - Configurable monitoring frequency
    - Start/stop control
    """
    
    def __init__(self, config: Dict = None):
        """
        Initialize vision monitoring manager.
        
        Args:
            config: Configuration dictionary with monitoring settings
        """
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
        # Monitoring state
        self.is_monitoring = False
        self.monitoring_callback = None
        
        # Settings
        self.default_frequency = self.config.get('monitoring_frequency', 1.0)
    
    def start_monitoring(
        self,
        capture_func: Callable,
        analysis_func: Callable,
        callback: Callable[[Dict[str, Any]], None],
        duration: Optional[int] = None,
        frequency: Optional[float] = None,
        **capture_kwargs
    ) -> None:
        """
        Start continuous monitoring with callback.
        
        Args:
            capture_func: Function to capture screen/image
            analysis_func: Function to analyze captured image
            callback: Function to call with analysis results
            duration: Duration in seconds (None for indefinite)
            frequency: Capture frequency override (Hz)
            **capture_kwargs: Additional arguments for capture function
        """
        if self.is_monitoring:
            self.logger.warning("Monitoring already active")
            return
        
        self.is_monitoring = True
        self.monitoring_callback = callback
        
        # Use specified frequency or default
        freq = frequency if frequency is not None else self.default_frequency
        interval = 1.0 / freq if freq > 0 else 1.0
        
        self.logger.info(f"Starting vision monitoring at {freq}Hz for {duration or 'indefinite'} seconds")
        
        try:
            start_time = time.time()
            
            while self.is_monitoring:
                # Check duration
                if duration and (time.time() - start_time) >= duration:
                    break
                
                # Capture and analyze
                try:
                    image = capture_func(**capture_kwargs)
                    
                    if image is not None:
                        analysis = analysis_func(image)
                        
                        # Call user callback
                        if self.monitoring_callback:
                            self.monitoring_callback(analysis)
                
                except Exception as e:
                    self.logger.error(f"Monitoring iteration failed: {e}")
                
                # Wait for next iteration
                time.sleep(interval)
        
        except Exception as e:
            self.logger.error(f"Monitoring failed: {e}")
        
        finally:
            self.is_monitoring = False
            self.monitoring_callback = None
            self.logger.info("Vision monitoring stopped")
    
    def stop_monitoring(self) -> None:
        """Stop continuous monitoring."""
        if self.is_monitoring:
            self.is_monitoring = False
            self.monitoring_callback = None
            self.logger.info("Monitoring stop requested")
        else:
            self.logger.warning("Monitoring not active")
    
    def get_monitoring_status(self) -> Dict:
        """
        Get current monitoring status.
        
        Returns:
            Dictionary with monitoring information
        """
        return {
            'is_monitoring': self.is_monitoring,
            'has_callback': self.monitoring_callback is not None,
            'default_frequency': self.default_frequency
        }

