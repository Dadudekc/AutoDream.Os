"""
Vision Data Persistence
======================

Handles storage, retrieval, and cleanup of vision analysis data and captured images.
Manages analysis history and data lifecycle.

V2 Compliance: ≤200 lines, single responsibility, comprehensive error handling.

Author: Agent-7 - Repository Cloning Specialist (extracted from vision/integration.py)
License: MIT
"""

import json
import time
from pathlib import Path
from typing import Any, Dict, List, Optional
import logging


class VisionPersistence:
    """
    Manages persistence of vision analysis data and images.
    
    Capabilities:
    - Analysis history storage
    - Image caching for change detection
    - Data cleanup and lifecycle management
    - JSON serialization of analysis results
    """
    
    def __init__(self, config: Dict = None):
        """
        Initialize vision persistence manager.
        
        Args:
            config: Configuration dictionary with persistence settings
        """
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
        # Persistence settings
        self.max_analysis_history = self.config.get('max_analysis_history', 100)
        self.data_persistence = self.config.get('data_persistence', True)
        
        # Storage
        self.analysis_history = []
        self.previous_images = {}  # Cache for change detection
        
        # Data directory
        if self.data_persistence:
            self.data_directory = Path("runtime/vision_data")
            self.data_directory.mkdir(parents=True, exist_ok=True)
    
    def store_analysis(self, analysis: Dict[str, Any]) -> None:
        """
        Store analysis results in history.
        
        Args:
            analysis: Analysis results dictionary
        """
        try:
            # Add to history
            self.analysis_history.append(analysis)
            
            # Trim history if needed
            if len(self.analysis_history) > self.max_analysis_history:
                self.analysis_history = self.analysis_history[-self.max_analysis_history:]
            
            self.logger.debug(f"Analysis stored (history size: {len(self.analysis_history)})")
            
        except Exception as e:
            self.logger.error(f"Failed to store analysis: {e}")
    
    def get_previous_image(self, agent_id: Optional[str], region: Optional[tuple]) -> Optional[Any]:
        """
        Get previously captured image for change detection.
        
        Args:
            agent_id: Agent ID for region-based lookup
            region: Region tuple for lookup
            
        Returns:
            Previously captured image or None
        """
        key = self._get_cache_key(agent_id, region)
        return self.previous_images.get(key)
    
    def store_previous_image(self, image: Any, agent_id: Optional[str], region: Optional[tuple]) -> None:
        """
        Store image for future change detection.
        
        Args:
            image: Image array to store
            agent_id: Agent ID for region-based storage
            region: Region tuple for storage
        """
        key = self._get_cache_key(agent_id, region)
        self.previous_images[key] = image
        self.logger.debug(f"Image stored for change detection (key: {key})")
    
    def save_vision_data(self, analysis: Dict[str, Any], filename: str) -> bool:
        """
        Save vision analysis data to JSON file.
        
        Args:
            analysis: Analysis results to save
            filename: Name of output file
            
        Returns:
            True if successful, False otherwise
        """
        if not self.data_persistence:
            self.logger.warning("Data persistence is disabled")
            return False
        
        try:
            filepath = self.data_directory / filename
            
            # Convert numpy arrays to lists for JSON serialization
            serializable_analysis = self._make_serializable(analysis)
            
            with open(filepath, 'w') as f:
                json.dump(serializable_analysis, f, indent=2)
            
            self.logger.info(f"Vision data saved to {filepath}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save vision data: {e}")
            return False
    
    def cleanup_old_data(self, max_age_days: int = 7) -> int:
        """
        Clean up old vision data files.
        
        Args:
            max_age_days: Maximum age of files to keep (in days)
            
        Returns:
            Number of files deleted
        """
        if not self.data_persistence:
            return 0
        
        try:
            current_time = time.time()
            max_age_seconds = max_age_days * 24 * 60 * 60
            deleted_count = 0
            
            for file_path in self.data_directory.glob('*.json'):
                # Check file age
                file_age = current_time - file_path.stat().st_mtime
                
                if file_age > max_age_seconds:
                    file_path.unlink()
                    deleted_count += 1
            
            self.logger.info(f"Cleaned up {deleted_count} old vision data files")
            return deleted_count
            
        except Exception as e:
            self.logger.error(f"Failed to cleanup old data: {e}")
            return 0
    
    def _get_cache_key(self, agent_id: Optional[str], region: Optional[tuple]) -> str:
        """Generate cache key for image storage."""
        if agent_id:
            return f"agent_{agent_id}"
        elif region:
            return f"region_{region}"
        else:
            return "full_screen"
    
    def _make_serializable(self, obj: Any) -> Any:
        """
        Convert object to JSON-serializable format.
        
        Args:
            obj: Object to convert
            
        Returns:
            JSON-serializable version of the object
        """
        if isinstance(obj, dict):
            return {k: self._make_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [self._make_serializable(item) for item in obj]
        elif hasattr(obj, 'tolist'):  # numpy array
            return obj.tolist()
        elif hasattr(obj, '__dict__'):  # Custom object
            return str(obj)
        else:
            return obj
    
    def get_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get analysis history.
        
        Args:
            limit: Maximum number of entries to return (None for all)
            
        Returns:
            List of analysis results
        """
        if limit:
            return self.analysis_history[-limit:]
        return self.analysis_history.copy()
    
    def clear_history(self) -> None:
        """Clear analysis history."""
        self.analysis_history.clear()
        self.logger.info("Analysis history cleared")
    
    def get_persistence_info(self) -> Dict:
        """
        Get information about persistence state.
        
        Returns:
            Dictionary with persistence information
        """
        return {
            'data_persistence': self.data_persistence,
            'max_analysis_history': self.max_analysis_history,
            'current_history_size': len(self.analysis_history),
            'cached_images': len(self.previous_images),
            'data_directory': str(self.data_directory) if self.data_persistence else None
        }

