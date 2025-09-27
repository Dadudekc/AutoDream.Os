"""
Enhanced Project Scanner - Main Scanner Class
============================================

Integrates all enhanced features into a unified project scanning system.
"""

import logging
import os
import time
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Union

from .enhanced_analyzer import EnhancedLanguageAnalyzer, EnhancedCachingSystem, EnhancedReportGenerator
from .workers import MultibotManager, FileProcessor

logger = logging.getLogger(__name__)


class EnhancedProjectScanner:
    """
    Enhanced project scanner with advanced language analysis, intelligent caching,
    agent categorization, and swarm intelligence features.
    """
    
    def __init__(self, project_root: Union[str, Path] = "."):
        """Initialize enhanced project scanner."""
        self.project_root = Path(project_root).resolve()
        self.analysis: Dict[str, Dict[str, Any]] = {}
        
        # Initialize enhanced components
        self.language_analyzer = EnhancedLanguageAnalyzer()
        self.caching_system = EnhancedCachingSystem()
        self.file_processor = FileProcessor()
        
        # Additional ignore directories
        self.additional_ignore_dirs: Set[str] = set()
        
        logger.info(f"🔍 Initialized Enhanced Project Scanner for: {self.project_root}")
    
    def scan_project(self, 
                    progress_callback: Optional[Callable[[int], None]] = None,
                    num_workers: Optional[int] = None,
                    file_extensions: Optional[Set[str]] = None) -> None:
        """
        Orchestrate enhanced project scan with all advanced features.
        
        Args:
            progress_callback: Optional callback for progress updates
            num_workers: Number of worker threads (default: CPU count)
            file_extensions: File extensions to scan (default: .py, .rs, .js, .ts)
        """
        if file_extensions is None:
            file_extensions = {'.py', '.rs', '.js', '.ts'}
        
        if num_workers is None:
            num_workers = os.cpu_count() or 4
        
        logger.info(f"🚀 Starting enhanced project scan...")
        start_time = time.time()
        
        # Step 1: Discover files with enhanced filtering
        valid_files = self._discover_files(file_extensions)
        total_files = len(valid_files)
        
        logger.info(f"📁 Found {total_files} files for enhanced analysis")
        
        # Step 2: Detect moved files and update cache
        current_files = set(valid_files)
        moved_files = self.caching_system.detect_moved_files(current_files, self.project_root)
        
        if moved_files:
            logger.info(f"🔄 Detected {len(moved_files)} moved files")
            self._handle_moved_files(moved_files)
        
        # Step 3: Clean up cache for missing files
        self.caching_system.cleanup_missing_files(current_files, self.project_root)
        
        # Step 4: Process files with enhanced analysis
        processed_count = 0
        skipped_count = 0
        
        for file_path in valid_files:
            relative_path = str(file_path.relative_to(self.project_root))
            
            # Check cache first
            if self.caching_system.is_file_cached(file_path, relative_path):
                skipped_count += 1
                logger.debug(f"⏭️ Skipped cached file: {relative_path}")
                continue
            
            # Process file with enhanced analysis
            try:
                analysis_result = self._analyze_file_enhanced(file_path)
                
                if analysis_result:
                    self.analysis[relative_path] = analysis_result
                    self.caching_system.update_file_cache(file_path, relative_path, analysis_result)
                    processed_count += 1
                    
                    logger.debug(f"✅ Processed: {relative_path}")
                else:
                    logger.warning(f"⚠️ No analysis result for: {relative_path}")
                
            except Exception as e:
                logger.error(f"❌ Error processing {relative_path}: {e}")
            
            # Update progress
            if progress_callback:
                total_processed = processed_count + skipped_count
                percent = int((total_processed / total_files) * 100)
                progress_callback(percent)
        
        # Step 5: Generate enhanced reports
        self._generate_enhanced_reports()
        
        # Step 6: Save updated cache
        self.caching_system.save_cache()
        
        # Final statistics
        end_time = time.time()
        duration = end_time - start_time
        
        logger.info(f"🎉 Enhanced scan complete!")
        logger.info(f"📊 Processed: {processed_count} files")
        logger.info(f"⏭️ Skipped (cached): {skipped_count} files")
        logger.info(f"⏱️ Duration: {duration:.2f} seconds")
        logger.info(f"🐝 WE. ARE. SWARM. Enhanced scanner ready! ⚡️🔥")
    
    def _discover_files(self, file_extensions: Set[str]) -> List[Path]:
        """Discover files with enhanced filtering."""
        valid_files = []
        
        for root, dirs, files in os.walk(self.project_root):
            root_path = Path(root)
            
            # Skip excluded directories
            if self._should_exclude_directory(root_path):
                continue
            
            for file in files:
                file_path = root_path / file
                
                if (file_path.suffix.lower() in file_extensions and 
                    not self._should_exclude_file(file_path)):
                    valid_files.append(file_path)
        
        return valid_files
    
    def _should_exclude_directory(self, dir_path: Path) -> bool:
        """Check if directory should be excluded from scanning."""
        # Common exclusion patterns
        exclude_patterns = {
            "__pycache__", "node_modules", ".git", ".venv", "venv", "env",
            "build", "dist", "target", "coverage", "htmlcov", ".pytest_cache",
            "migrations", "chrome_profile", "temp", "tmp", "logs"
        }
        
        # Check directory name
        if dir_path.name in exclude_patterns:
            return True
        
        # Check additional ignore directories
        for ignore_dir in self.additional_ignore_dirs:
            ignore_path = Path(ignore_dir)
            if not ignore_path.is_absolute():
                ignore_path = self.project_root / ignore_path
            
            try:
                dir_path.relative_to(ignore_path)
                return True
            except ValueError:
                continue
        
        # Check for virtual environment indicators
        try:
            if any((dir_path / indicator).exists() for indicator in 
                   ["pyvenv.cfg", "bin/activate", "Scripts/activate.bat"]):
                return True
        except (OSError, PermissionError):
            pass
        
        return False
    
    def _should_exclude_file(self, file_path: Path) -> bool:
        """Check if file should be excluded from scanning."""
        # Exclude the scanner itself
        try:
            if file_path.resolve() == Path(__file__).resolve():
                return True
        except NameError:
            pass
        
        # Check for additional exclusions
        return False
    
    def _analyze_file_enhanced(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Analyze file with enhanced language analyzer."""
        try:
            with file_path.open("r", encoding="utf-8", errors="ignore") as f:
                source_code = f.read()
            
            # Use enhanced language analyzer
            analysis_result = self.language_analyzer.analyze_file(file_path, source_code)
            
            # Add file metadata
            analysis_result.update({
                "file_path": str(file_path),
                "relative_path": str(file_path.relative_to(self.project_root)),
                "size_bytes": file_path.stat().st_size,
                "modified_time": file_path.stat().st_mtime,
                "scan_timestamp": time.time()
            })
            
            return analysis_result
            
        except Exception as e:
            logger.error(f"Error analyzing {file_path}: {e}")
            return None
    
    def _handle_moved_files(self, moved_files: Dict[str, str]) -> None:
        """Handle moved files in cache."""
        with self.caching_system.cache_lock:
            for old_path, new_path in moved_files.items():
                if old_path in self.caching_system.cache:
                    # Move cache entry to new path
                    cache_data = self.caching_system.cache.pop(old_path)
                    self.caching_system.cache[new_path] = cache_data
                    
                    # Update analysis dictionary if it exists
                    if old_path in self.analysis:
                        self.analysis[new_path] = self.analysis.pop(old_path)
                    
                    logger.debug(f"🔄 Moved cache entry: {old_path} -> {new_path}")
    
    def _generate_enhanced_reports(self) -> None:
        """Generate all enhanced reports."""
        logger.info("📝 Generating enhanced reports...")
        
        report_generator = EnhancedReportGenerator(self.project_root, self.analysis)
        report_generator.generate_enhanced_reports()
        
        logger.info("✅ Enhanced reports generated successfully")
    
    def generate_init_files(self, overwrite: bool = True) -> None:
        """Generate __init__.py files for Python packages."""
        logger.info("📦 Generating __init__.py files...")
        
        report_generator = EnhancedReportGenerator(self.project_root, self.analysis)
        report_generator.generate_init_files(overwrite)
        
        logger.info("✅ __init__.py files generated")
    
    def categorize_agents(self) -> None:
        """Categorize agents with enhanced analysis."""
        logger.info("🤖 Categorizing agents...")
        
        # Agent categorization is now handled by the enhanced analyzer
        # This method is kept for compatibility
        
        logger.info("✅ Agent categorization complete")
    
    def export_chatgpt_context(self, template_path: Optional[str] = None, 
                             output_path: Optional[str] = None) -> None:
        """Export enhanced ChatGPT context."""
        logger.info("💬 Exporting enhanced ChatGPT context...")
        
        report_generator = EnhancedReportGenerator(self.project_root, self.analysis)
        report_generator.export_chatgpt_context()
        
        logger.info("✅ Enhanced ChatGPT context exported")
    
    def get_analysis_summary(self) -> Dict[str, Any]:
        """Get summary of analysis results."""
        if not self.analysis:
            return {"error": "No analysis data available"}
        
        languages = {}
        agent_types = {}
        maturity_levels = {}
        total_complexity = 0
        total_files = len(self.analysis)
        
        for analysis in self.analysis.values():
            # Language distribution
            lang = analysis.get("language", "unknown")
            languages[lang] = languages.get(lang, 0) + 1
            
            # Agent type distribution
            for class_data in analysis.get("classes", {}).values():
                agent_type = class_data.get("agent_type", "Unknown")
                agent_types[agent_type] = agent_types.get(agent_type, 0) + 1
                
                maturity = class_data.get("maturity", "Unknown")
                maturity_levels[maturity] = maturity_levels.get(maturity, 0) + 1
            
            # Complexity
            total_complexity += analysis.get("complexity", 0)
        
        return {
            "total_files": total_files,
            "languages": languages,
            "agent_types": agent_types,
            "maturity_levels": maturity_levels,
            "total_complexity": total_complexity,
            "average_complexity": total_complexity / max(total_files, 1),
            "v2_compliance": self._calculate_v2_compliance()
        }
    
    def _calculate_v2_compliance(self) -> Dict[str, Any]:
        """Calculate V2 compliance metrics."""
        compliant_files = 0
        violation_files = 0
        total_lines = 0
        
        for analysis in self.analysis.values():
            file_size = analysis.get("file_size", 0)
            total_lines += file_size
            
            if file_size <= 400:
                compliant_files += 1
            else:
                violation_files += 1
        
        total_files = len(self.analysis)
        compliance_rate = (compliant_files / max(total_files, 1)) * 100
        
        return {
            "compliant_files": compliant_files,
            "violation_files": violation_files,
            "total_files": total_files,
            "compliance_rate": compliance_rate,
            "total_lines": total_lines,
            "average_file_size": total_lines / max(total_files, 1)
        }
    
    def add_ignore_directory(self, directory: str) -> None:
        """Add directory to ignore list."""
        self.additional_ignore_dirs.add(directory)
        logger.info(f"➕ Added ignore directory: {directory}")
    
    def remove_ignore_directory(self, directory: str) -> None:
        """Remove directory from ignore list."""
        self.additional_ignore_dirs.discard(directory)
        logger.info(f"➖ Removed ignore directory: {directory}")
    
    def clear_cache(self) -> None:
        """Clear the analysis cache."""
        self.caching_system.cache.clear()
        self.caching_system.save_cache()
        logger.info("🗑️ Analysis cache cleared")
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        cache_size = len(self.caching_system.cache)
        
        return {
            "cache_size": cache_size,
            "cache_file": str(self.caching_system.cache_file),
            "cache_exists": self.caching_system.cache_file.exists(),
            "ignored_directories": list(self.additional_ignore_dirs)
        }


def main():
    """Enhanced scanner CLI entry point."""
    import argparse
    
    logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s] %(message)s"
    )
    
    parser = argparse.ArgumentParser(
        description="Enhanced project scanner with advanced language analysis and agent categorization."
    )
    parser.add_argument(
        "--project-root", 
        default=".", 
        help="Root directory to scan"
    )
    parser.add_argument(
        "--ignore", 
        nargs="*", 
        default=[], 
        help="Additional directories to ignore"
    )
    parser.add_argument(
        "--workers", 
        type=int, 
        help="Number of worker threads"
    )
    parser.add_argument(
        "--extensions", 
        nargs="*", 
        default=['.py', '.rs', '.js', '.ts'], 
        help="File extensions to scan"
    )
    parser.add_argument(
        "--no-chatgpt-context", 
        action="store_true", 
        help="Skip exporting ChatGPT context"
    )
    parser.add_argument(
        "--no-init-files", 
        action="store_true", 
        help="Skip generating __init__.py files"
    )
    parser.add_argument(
        "--clear-cache", 
        action="store_true", 
        help="Clear cache before scanning"
    )
    parser.add_argument(
        "--summary", 
        action="store_true", 
        help="Show analysis summary"
    )
    
    args = parser.parse_args()
    
    # Initialize enhanced scanner
    scanner = EnhancedProjectScanner(project_root=args.project_root)
    
    # Add ignore directories
    for ignore_dir in args.ignore:
        scanner.add_ignore_directory(ignore_dir)
    
    # Clear cache if requested
    if args.clear_cache:
        scanner.clear_cache()
    
    # Progress callback
    def progress_callback(percent: int):
        if percent % 10 == 0:  # Log every 10%
            logger.info(f"📊 Scan progress: {percent}%")
    
    # Run enhanced scan
    scanner.scan_project(
        progress_callback=progress_callback,
        num_workers=args.workers,
        file_extensions=set(args.extensions)
    )
    
    # Generate additional outputs
    if not args.no_init_files:
        scanner.generate_init_files(overwrite=True)
    
    if not args.no_chatgpt_context:
        scanner.export_chatgpt_context()
    
    # Show summary if requested
    if args.summary:
        summary = scanner.get_analysis_summary()
        logger.info("📊 Analysis Summary:")
        logger.info(f"  Total files: {summary['total_files']}")
        logger.info(f"  Languages: {summary['languages']}")
        logger.info(f"  Agent types: {summary['agent_types']}")
        logger.info(f"  V2 Compliance: {summary['v2_compliance']['compliance_rate']:.1f}%")
    
    logger.info("🐝 Enhanced Project Scanner complete! ⚡️🔥")


if __name__ == "__main__":
    main()

