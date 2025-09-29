"""
Enhanced Project Scanner Core Analyzer
=====================================

Core analysis functionality for the enhanced project scanner.
Handles file discovery, basic analysis, and orchestration.
"""

import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Set

logger = logging.getLogger(__name__)


class EnhancedCoreAnalyzer:
    """Core analyzer for enhanced project scanning."""
    
    def __init__(self, project_root: Path):
        """Initialize core analyzer."""
        self.project_root = project_root
        self.analysis_results: Dict[str, Dict[str, Any]] = {}
        
    def discover_files(self, extensions: List[str] = None) -> Set[Path]:
        """
        Discover files in the project.
        
        Args:
            extensions: List of file extensions to include
            
        Returns:
            Set of discovered file paths
        """
        if extensions is None:
            extensions = [".py", ".rs", ".js", ".ts", ".json", ".yaml", ".yml"]
        
        discovered_files = set()
        
        logger.info(f"🔍 Discovering files with extensions: {extensions}")
        
        for root, dirs, files in os.walk(self.project_root):
            # Skip common directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in {
                '__pycache__', 'node_modules', 'venv', 'env', '.git'
            }]
            
            for file in files:
                file_path = Path(root) / file
                if file_path.suffix.lower() in extensions:
                    discovered_files.add(file_path)
        
        logger.info(f"✅ Discovered {len(discovered_files)} files")
        return discovered_files
    
    def analyze_file_basic(self, file_path: Path) -> Dict[str, Any]:
        """
        Perform basic file analysis.
        
        Args:
            file_path: Path to file to analyze
            
        Returns:
            Basic analysis results
        """
        try:
            relative_path = str(file_path.relative_to(self.project_root))
            
            # Basic file info
            stat = file_path.stat()
            with file_path.open('r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            lines = content.splitlines()
            
            return {
                "file_path": relative_path,
                "file_size": len(lines),
                "file_size_bytes": stat.st_size,
                "last_modified": stat.st_mtime,
                "language": file_path.suffix.lower(),
                "has_content": len(content.strip()) > 0,
                "line_count": len(lines),
                "char_count": len(content)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing file {file_path}: {e}")
            return {
                "file_path": str(file_path.relative_to(self.project_root)),
                "error": str(e),
                "file_size": 0,
                "language": file_path.suffix.lower()
            }
    
    def run_basic_analysis(self, files: Set[Path]) -> Dict[str, Dict[str, Any]]:
        """
        Run basic analysis on all files.
        
        Args:
            files: Set of files to analyze
            
        Returns:
            Dictionary of analysis results
        """
        logger.info(f"🔄 Running basic analysis on {len(files)} files")
        
        results = {}
        for file_path in files:
            try:
                analysis = self.analyze_file_basic(file_path)
                relative_path = str(file_path.relative_to(self.project_root))
                results[relative_path] = analysis
                
                if len(results) % 50 == 0:
                    logger.info(f"  Processed {len(results)}/{len(files)} files")
                    
            except Exception as e:
                logger.error(f"Error processing {file_path}: {e}")
        
        logger.info(f"✅ Basic analysis complete: {len(results)} files processed")
        return results
    
    def filter_analysis_files(self, analysis_results: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """
        Filter analysis results to focus on relevant files.
        
        Args:
            analysis_results: Full analysis results
            
        Returns:
            Filtered analysis results
        """
        filtered = {}
        
        for file_path, analysis in analysis_results.items():
            # Skip empty files, binary files, and common non-code files
            if not analysis.get("has_content", True):
                continue
                
            file_ext = analysis.get("language", "")
            if file_ext not in [".py", ".rs", ".js", ".ts"]:
                continue
                
            # Skip test files for basic analysis (can be enabled later)
            if "test" in file_path.lower() and file_ext == ".py":
                continue
                
            filtered[file_path] = analysis
        
        logger.info(f"✅ Filtered to {len(filtered)} relevant files from {len(analysis_results)} total")
        return filtered
    
    def calculate_project_metrics(self, analysis_results: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate project-level metrics.
        
        Args:
            analysis_results: Analysis results
            
        Returns:
            Project metrics
        """
        total_files = len(analysis_results)
        total_lines = sum(a.get("line_count", 0) for a in analysis_results.values())
        total_size = sum(a.get("file_size_bytes", 0) for a in analysis_results.values())
        
        languages = {}
        for analysis in analysis_results.values():
            lang = analysis.get("language", "unknown")
            languages[lang] = languages.get(lang, 0) + 1
        
        return {
            "total_files": total_files,
            "total_lines": total_lines,
            "total_size_bytes": total_size,
            "average_file_size": total_lines / max(total_files, 1),
            "languages": languages,
            "analysis_timestamp": os.path.getmtime(self.project_root / "project_analysis.json") if (self.project_root / "project_analysis.json").exists() else None
        }
    
    def save_basic_analysis(self, analysis_results: Dict[str, Dict[str, Any]], 
                          metrics: Dict[str, Any]):
        """
        Save basic analysis results.
        
        Args:
            analysis_results: Analysis results to save
            metrics: Project metrics
        """
        output_file = self.project_root / "basic_analysis.json"
        
        output_data = {
            "metrics": metrics,
            "files": analysis_results,
            "timestamp": metrics.get("analysis_timestamp")
        }
        
        import json
        with output_file.open('w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2)
        
        logger.info(f"✅ Basic analysis saved to {output_file}")

