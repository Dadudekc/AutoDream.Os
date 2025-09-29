#!/usr/bin/env python3
"""
Enhanced Project Scanner Core - V2 Compliant
============================================

Core enhanced project scanner functionality.
V2 Compliance: ≤200 lines, single responsibility, KISS principle.
"""

import logging
import os
import time
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Union

from .file_discovery import FileDiscoveryHandler
from .file_analysis import FileAnalysisHandler
from .report_generation import ReportGenerationHandler
from .agent_categorization import AgentCategorizationHandler
from ..enhanced_analyzer import EnhancedLanguageAnalyzer, EnhancedCachingSystem, EnhancedReportGenerator
from ..workers import MultibotManager, FileProcessor

logger = logging.getLogger(__name__)


class EnhancedProjectScannerCore:
    """Core enhanced project scanner functionality."""
    
    def __init__(self, project_root: Union[str, Path] = "."):
        """Initialize enhanced project scanner."""
        self.project_root = Path(project_root).resolve()
        self.analysis: Dict[str, Dict[str, Any]] = {}
        
        # Initialize enhanced components
        self.language_analyzer = EnhancedLanguageAnalyzer()
        self.caching_system = EnhancedCachingSystem()
        self.file_processor = FileProcessor()
        
        # Initialize specialized handlers
        self.file_discovery = FileDiscoveryHandler(self)
        self.file_analysis = FileAnalysisHandler(self)
        self.report_generation = ReportGenerationHandler(self)
        self.agent_categorization = AgentCategorizationHandler(self)
        
        # Additional ignore directories
        self.additional_ignore_dirs: Set[str] = set()
        
        logger.info(f"🔍 Initialized Enhanced Project Scanner for: {self.project_root}")
    
    def scan_project(self, 
                    progress_callback: Optional[Callable[[int], None]] = None,
                    num_workers: Optional[int] = None,
                    file_extensions: Optional[Set[str]] = None) -> None:
        """Orchestrate enhanced project scan with all advanced features."""
        
        start_time = time.time()
        logger.info("🚀 Starting Enhanced Project Scan")
        
        # Discover files
        files_to_scan = self.file_discovery.discover_files(file_extensions)
        
        # Process files with workers
        if num_workers is None:
            num_workers = min(os.cpu_count() or 4, len(files_to_scan))
        
        logger.info(f"📁 Processing {len(files_to_scan)} files with {num_workers} workers")
        
        # Initialize multibot manager
        multibot = MultibotManager(num_workers)
        
        # Process files
        processed_count = 0
        for file_path in files_to_scan:
            if progress_callback and processed_count % 10 == 0:
                progress = int((processed_count / len(files_to_scan)) * 100)
                progress_callback(progress)
            
            analysis_result = self.file_analysis.analyze_file_enhanced(file_path)
            if analysis_result:
                self.analysis[str(file_path)] = analysis_result
            
            processed_count += 1
        
        # Final progress update
        if progress_callback:
            progress_callback(100)
        
        # Handle moved files
        self.file_analysis.handle_moved_files()
        
        # Generate enhanced reports
        self.report_generation.generate_enhanced_reports()
        
        # Categorize agents
        self.agent_categorization.categorize_agents()
        
        # Export ChatGPT context
        self.report_generation.export_chatgpt_context()
        
        scan_time = time.time() - start_time
        logger.info(f"✅ Enhanced Project Scan completed in {scan_time:.2f} seconds")
    
    def get_analysis_summary(self) -> Dict[str, Any]:
        """Get comprehensive analysis summary."""
        total_files = len(self.analysis)
        total_lines = sum(analysis.get('line_count', 0) for analysis in self.analysis.values())
        
        # Calculate V2 compliance
        v2_compliance = self._calculate_v2_compliance()
        
        # Language breakdown
        language_stats = {}
        for analysis in self.analysis.values():
            lang = analysis.get('language', 'Unknown')
            language_stats[lang] = language_stats.get(lang, 0) + 1
        
        return {
            'total_files': total_files,
            'total_lines': total_lines,
            'v2_compliance': v2_compliance,
            'language_breakdown': language_stats,
            'scan_timestamp': time.time(),
            'project_root': str(self.project_root)
        }
    
    def _calculate_v2_compliance(self) -> Dict[str, Any]:
        """Calculate V2 compliance metrics."""
        compliant_files = 0
        minor_violations = 0
        major_violations = 0
        critical_violations = 0
        
        for analysis in self.analysis.values():
            line_count = analysis.get('line_count', 0)
            if line_count <= 400:
                compliant_files += 1
            elif line_count <= 600:
                minor_violations += 1
            elif line_count <= 1000:
                major_violations += 1
            else:
                critical_violations += 1
        
        total_files = len(self.analysis)
        compliance_rate = (compliant_files / total_files * 100) if total_files > 0 else 0
        
        return {
            'compliant_files': compliant_files,
            'minor_violations': minor_violations,
            'major_violations': major_violations,
            'critical_violations': critical_violations,
            'compliance_rate': compliance_rate,
            'total_files': total_files
        }
    
    def add_ignore_directory(self, directory: str) -> None:
        """Add directory to ignore list."""
        self.additional_ignore_dirs.add(directory)
    
    def remove_ignore_directory(self, directory: str) -> None:
        """Remove directory from ignore list."""
        self.additional_ignore_dirs.discard(directory)
    
    def clear_cache(self) -> None:
        """Clear analysis cache."""
        self.caching_system.clear_cache()
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        return self.caching_system.get_stats()
