"""
Enhanced Project Scanner V2 - Modular Architecture
==================================================

Refactored enhanced project scanner using modular design.
V2 Compliance: ≤400 lines, single responsibility, KISS principle.
"""

import logging
from pathlib import Path
from typing import Dict, Set

from .enhanced_scanner.core_analyzer import EnhancedCoreAnalyzer
from .enhanced_scanner.caching_system import EnhancedCachingSystem
from .enhanced_scanner.report_generator import EnhancedReportGenerator
from .enhanced_scanner.language_analyzer import EnhancedLanguageAnalyzer

logger = logging.getLogger(__name__)


class EnhancedProjectScannerV2:
    """Enhanced Project Scanner V2 - Modular architecture."""
    
    def __init__(self, project_root: Path, cache_file: str = "dependency_cache.json"):
        """Initialize enhanced project scanner."""
        self.project_root = project_root
        self.cache_file = cache_file
        
        # Initialize modular components
        self.core_analyzer = EnhancedCoreAnalyzer(project_root)
        self.caching_system = EnhancedCachingSystem(cache_file)
        self.language_analyzer = EnhancedLanguageAnalyzer()
        
        logger.info("✅ Enhanced Project Scanner V2 initialized")
    
    def run_full_analysis(self, extensions: list = None) -> Dict[str, Dict]:
        """
        Run full enhanced analysis with caching and modular components.
        
        Args:
            extensions: File extensions to analyze
            
        Returns:
            Complete analysis results
        """
        logger.info("🚀 Starting Enhanced Project Scanner V2 analysis")
        
        # Step 1: Discover files
        discovered_files = self.core_analyzer.discover_files(extensions)
        logger.info(f"📁 Discovered {len(discovered_files)} files")
        
        # Step 2: Check cache and detect moved files
        moved_files = self.caching_system.detect_moved_files(discovered_files, self.project_root)
        if moved_files:
            logger.info(f"🔄 Detected {len(moved_files)} moved files")
        
        # Step 3: Clean up missing files from cache
        self.caching_system.cleanup_missing_files(discovered_files, self.project_root)
        
        # Step 4: Analyze files (with caching)
        analysis_results = {}
        files_to_analyze = []
        
        for file_path in discovered_files:
            relative_path = str(file_path.relative_to(self.project_root))
            
            # Check if file is cached and unchanged
            if self.caching_system.is_file_cached(file_path, relative_path):
                cached_analysis = self.caching_system.get_cached_analysis(relative_path)
                analysis_results[relative_path] = cached_analysis
                logger.debug(f"✅ Using cached analysis for {relative_path}")
            else:
                files_to_analyze.append(file_path)
        
        logger.info(f"📊 {len(analysis_results)} files from cache, {len(files_to_analyze)} to analyze")
        
        # Step 5: Analyze new/changed files
        for file_path in files_to_analyze:
            try:
                relative_path = str(file_path.relative_to(self.project_root))
                
                # Basic analysis
                basic_analysis = self.core_analyzer.analyze_file_basic(file_path)
                
                # Language-specific analysis
                if file_path.suffix.lower() in [".py", ".rs", ".js", ".ts"]:
                    with file_path.open('r', encoding='utf-8', errors='ignore') as f:
                        source_code = f.read()
                    
                    language_analysis = self.language_analyzer.analyze_file(file_path, source_code)
                    
                    # Merge analyses
                    combined_analysis = {**basic_analysis, **language_analysis}
                else:
                    combined_analysis = basic_analysis
                
                analysis_results[relative_path] = combined_analysis
                
                # Update cache
                self.caching_system.update_file_cache(file_path, relative_path, combined_analysis)
                
                logger.debug(f"✅ Analyzed {relative_path}")
                
            except Exception as e:
                logger.error(f"❌ Error analyzing {file_path}: {e}")
        
        # Step 6: Calculate project metrics
        project_metrics = self.core_analyzer.calculate_project_metrics(analysis_results)
        logger.info(f"📈 Project metrics: {project_metrics['total_files']} files, {project_metrics['total_lines']} lines")
        
        # Step 7: Save cache
        self.caching_system.save_cache()
        
        # Step 8: Generate reports
        report_generator = EnhancedReportGenerator(self.project_root, analysis_results)
        report_generator.generate_enhanced_reports()
        
        # Step 9: Generate __init__.py files
        report_generator.generate_init_files()
        
        logger.info("🎉 Enhanced Project Scanner V2 analysis complete")
        return analysis_results
    
    def get_cache_stats(self) -> Dict:
        """Get caching system statistics."""
        return self.caching_system.get_cache_stats()
    
    def clear_cache(self):
        """Clear the analysis cache."""
        self.caching_system.clear_cache()
        logger.info("🗑️ Analysis cache cleared")
    
    def invalidate_file(self, file_path: str):
        """Invalidate cache for specific file."""
        self.caching_system.invalidate_file(file_path)
        logger.info(f"🔄 Invalidated cache for {file_path}")
    
    def run_quick_analysis(self, extensions: list = None) -> Dict[str, Dict]:
        """
        Run quick analysis without language-specific parsing.
        
        Args:
            extensions: File extensions to analyze
            
        Returns:
            Basic analysis results
        """
        logger.info("⚡ Running quick analysis")
        
        # Discover files
        discovered_files = self.core_analyzer.discover_files(extensions)
        
        # Run basic analysis only
        analysis_results = self.core_analyzer.run_basic_analysis(discovered_files)
        
        # Filter results
        filtered_results = self.core_analyzer.filter_analysis_files(analysis_results)
        
        # Calculate metrics
        metrics = self.core_analyzer.calculate_project_metrics(filtered_results)
        
        # Save basic analysis
        self.core_analyzer.save_basic_analysis(filtered_results, metrics)
        
        logger.info("⚡ Quick analysis complete")
        return filtered_results
    
    def analyze_single_file(self, file_path: Path) -> Dict:
        """
        Analyze a single file with full language analysis.
        
        Args:
            file_path: Path to file to analyze
            
        Returns:
            Analysis results for the file
        """
        logger.info(f"🔍 Analyzing single file: {file_path}")
        
        try:
            # Basic analysis
            basic_analysis = self.core_analyzer.analyze_file_basic(file_path)
            
            # Language-specific analysis
            if file_path.suffix.lower() in [".py", ".rs", ".js", ".ts"]:
                with file_path.open('r', encoding='utf-8', errors='ignore') as f:
                    source_code = f.read()
                
                language_analysis = self.language_analyzer.analyze_file(file_path, source_code)
                combined_analysis = {**basic_analysis, **language_analysis}
            else:
                combined_analysis = basic_analysis
            
            logger.info(f"✅ Single file analysis complete: {file_path}")
            return combined_analysis
            
        except Exception as e:
            logger.error(f"❌ Error analyzing single file {file_path}: {e}")
            return {"error": str(e), "file_path": str(file_path)}


def main():
    """Main function for command-line usage."""
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(description="Enhanced Project Scanner V2")
    parser.add_argument("project_path", help="Path to project root")
    parser.add_argument("--cache", default="dependency_cache.json", help="Cache file path")
    parser.add_argument("--quick", action="store_true", help="Run quick analysis only")
    parser.add_argument("--clear-cache", action="store_true", help="Clear cache before analysis")
    parser.add_argument("--extensions", nargs="+", help="File extensions to analyze")
    
    args = parser.parse_args()
    
    project_root = Path(args.project_path)
    if not project_root.exists():
        print(f"Error: Project path {project_root} does not exist")
        sys.exit(1)
    
    # Initialize scanner
    scanner = EnhancedProjectScannerV2(project_root, args.cache)
    
    # Clear cache if requested
    if args.clear_cache:
        scanner.clear_cache()
    
    # Run analysis
    if args.quick:
        results = scanner.run_quick_analysis(args.extensions)
    else:
        results = scanner.run_full_analysis(args.extensions)
    
    # Print summary
    print(f"\n📊 Analysis Summary:")
    print(f"  Files analyzed: {len(results)}")
    
    if not args.quick:
        cache_stats = scanner.get_cache_stats()
        print(f"  Cache entries: {cache_stats['total_entries']}")
    
    print("✅ Analysis complete!")


if __name__ == "__main__":
    main()

