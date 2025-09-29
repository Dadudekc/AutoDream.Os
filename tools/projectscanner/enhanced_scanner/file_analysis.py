#!/usr/bin/env python3
"""
File Analysis Handler - V2 Compliant
====================================

Handles file analysis for enhanced project scanner.
V2 Compliance: ≤150 lines, single responsibility, KISS principle.
"""

import logging
from pathlib import Path
from typing import Dict, Optional, Any

logger = logging.getLogger(__name__)


class FileAnalysisHandler:
    """Handles file analysis for enhanced project scanner."""
    
    def __init__(self, core):
        """Initialize file analysis handler."""
        self.core = core
        self.moved_files = {}
    
    def analyze_file_enhanced(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Analyze file with enhanced language analysis."""
        
        try:
            # Check cache first
            cache_key = str(file_path)
            cached_result = self.core.caching_system.get(cache_key)
            if cached_result:
                return cached_result
            
            # Perform enhanced analysis
            analysis_result = self.core.language_analyzer.analyze_file(file_path)
            
            if analysis_result:
                # Add additional metadata
                analysis_result['file_path'] = str(file_path)
                analysis_result['relative_path'] = str(file_path.relative_to(self.core.project_root))
                analysis_result['file_size'] = file_path.stat().st_size
                
                # Cache the result
                self.core.caching_system.set(cache_key, analysis_result)
                
                logger.debug(f"📄 Analyzed: {file_path}")
                return analysis_result
            
        except Exception as e:
            logger.warning(f"⚠️ Failed to analyze {file_path}: {e}")
        
        return None
    
    def handle_moved_files(self) -> None:
        """Handle moved files detection and cleanup."""
        
        if not self.moved_files:
            return
        
        logger.info(f"🔄 Handling {len(self.moved_files)} moved files")
        
        for old_path, new_path in self.moved_files.items():
            # Remove old analysis
            if old_path in self.core.analysis:
                del self.core.analysis[old_path]
            
            # Update cache
            self.core.caching_system.remove(old_path)
            
            logger.info(f"📁 Moved: {old_path} → {new_path}")
        
        # Clear moved files tracking
        self.moved_files.clear()
    
    def detect_moved_files(self) -> Dict[str, str]:
        """Detect files that have been moved."""
        
        moved_files = {}
        
        # Simple heuristic: check if files with same content exist in different locations
        content_hash_map = {}
        
        for file_path, analysis in self.core.analysis.items():
            content_hash = analysis.get('content_hash')
            if content_hash:
                if content_hash in content_hash_map:
                    # Potential move detected
                    old_path = content_hash_map[content_hash]
                    moved_files[old_path] = file_path
                else:
                    content_hash_map[content_hash] = file_path
        
        return moved_files
