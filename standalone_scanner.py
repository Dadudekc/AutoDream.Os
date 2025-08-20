#!/usr/bin/env python3
"""
Refactored Standalone Scanner - Agent Cellphone V2
==================================================

Facade for the new scanner services, maintaining backward compatibility.
Follows V2 standards: ≤200 LOC, SRP, OOP principles.
"""

import os
import json
import logging
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional

from src.services.language_analyzer_service import LanguageAnalyzerService
from src.services.file_processor_service import FileProcessorService
from src.services.report_generator_service import ReportGeneratorService
from src.services.project_scanner_service import ProjectScannerService
from src.services.scanner_cache_service import ScannerCacheService

logger = logging.getLogger(__name__)

# Cache file configuration
CACHE_FILE = "dependency_cache.json"


class StandaloneScanner:
    """
    Refactored standalone scanner using new service architecture.
    
    Responsibilities:
    - Coordinate scanner services
    - Maintain backward compatibility
    - Provide unified scanning interface
    """
    
    def __init__(self, project_path: str = ".", output_dir: str = "scanner_output"):
        """Initialize scanner with new services"""
        self.project_path = Path(project_path)
        self.output_dir = Path(output_dir)
        
        # Initialize services
        self.language_analyzer = LanguageAnalyzerService()
        self.file_processor = FileProcessorService()
        self.report_generator = ReportGeneratorService(output_dir=self.output_dir)
        self.project_scanner = ProjectScannerService()
        self.cache_service = ScannerCacheService()
        
        # Ensure output directory exists
        self.output_dir.mkdir(exist_ok=True)
        
        logger.info(f"🚀 Standalone Scanner initialized for {self.project_path}")
    
    def scan_project(self, include_hidden: bool = False, max_workers: int = 4) -> Dict[str, Any]:
        """Scan entire project using new services"""
        try:
            logger.info(f"🔍 Starting project scan: {self.project_path}")
            
            # Use project scanner service
            scan_result = self.project_scanner.scan_project(
                project_path=self.project_path,
                include_hidden=include_hidden,
                max_workers=max_workers
            )
            
            if scan_result.get('error'):
                logger.error(f"❌ Project scan failed: {scan_result['error']}")
                return {'error': scan_result['error'], 'status': 'failed'}
            
            # Generate comprehensive report
            report = self.report_generator.generate_project_report(
                project_data=scan_result,
                include_details=True
            )
            
            # Save report
            self._save_report(report, "project_analysis.json")
            
            logger.info("✅ Project scan completed successfully")
            return {
                'status': 'success',
                'files_analyzed': len(scan_result.get('files', [])),
                'languages_detected': len(scan_result.get('language_stats', {}).get('file_counts', {})),
                'report_path': str(self.output_dir / "project_analysis.json")
            }
            
        except Exception as e:
            logger.error(f"❌ Project scan error: {e}")
            return {'error': str(e), 'status': 'failed'}
    
    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """Analyze single file using new services"""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return {'error': f'File not found: {file_path}', 'status': 'failed'}
            
            # Check cache first
            cached_result = self.cache_service.get_cached_result(file_path)
            if cached_result:
                logger.info(f"📋 Using cached analysis for {file_path}")
                return cached_result['analysis_result']
            
            # Process file
            file_data = self.file_processor.process_file(file_path)
            if file_data.get('error'):
                return {'error': file_data['error'], 'status': 'failed'}
            
            # Analyze language-specific content
            analysis = self.language_analyzer.analyze_file(file_path, file_data['content'])
            
            # Cache result
            self.cache_service.cache_result(file_path, analysis)
            
            return {
                'status': 'success',
                'file_path': str(file_path),
                'analysis': analysis,
                'metadata': file_data
            }
            
        except Exception as e:
            logger.error(f"❌ File analysis error: {e}")
            return {'error': str(e), 'status': 'failed'}
    
    def generate_report(self, analysis_data: Dict[str, Any], report_type: str = "comprehensive") -> str:
        """Generate report using new service"""
        try:
            if report_type == "comprehensive":
                report = self.report_generator.generate_project_report(analysis_data, include_details=True)
            elif report_type == "code_quality":
                report = self.report_generator.generate_code_quality_report(analysis_data)
            else:
                report = self.report_generator.generate_project_report(analysis_data, include_details=False)
            
            # Save report
            filename = f"{report_type}_report.json"
            self._save_report(report, filename)
            
            return str(self.output_dir / filename)
            
        except Exception as e:
            logger.error(f"❌ Report generation error: {e}")
            return ""
    
    def _save_report(self, report: Dict[str, Any], filename: str):
        """Save report to output directory"""
        try:
            output_file = self.output_dir / filename
            with open(output_file, 'w') as f:
                json.dump(report, f, indent=2, default=str)
            logger.info(f"💾 Report saved: {output_file}")
        except Exception as e:
            logger.error(f"❌ Failed to save report: {e}")
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        return self.cache_service.get_cache_stats()
    
    def clear_cache(self) -> bool:
        """Clear scanner cache"""
        return self.cache_service.clear_cache()


def main():
    """Main entry point for standalone scanner"""
    parser = argparse.ArgumentParser(description="Refactored Standalone Project Scanner")
    parser.add_argument("project_path", nargs="?", default=".", help="Path to project directory")
    parser.add_argument("--output", "-o", default="scanner_output", help="Output directory for reports")
    parser.add_argument("--include-hidden", action="store_true", help="Include hidden files/directories")
    parser.add_argument("--max-workers", type=int, default=4, help="Maximum worker threads")
    parser.add_argument("--clear-cache", action="store_true", help="Clear scanner cache")
    parser.add_argument("--cache-stats", action="store_true", help="Show cache statistics")
    
    args = parser.parse_args()
    
    # Initialize scanner
    scanner = StandaloneScanner(args.project_path, args.output)
    
    # Handle cache operations
    if args.clear_cache:
        if scanner.clear_cache():
            print("✅ Cache cleared successfully")
        else:
            print("❌ Failed to clear cache")
        return
    
    if args.cache_stats:
        stats = scanner.get_cache_stats()
        print("📊 Cache Statistics:")
        print(json.dumps(stats, indent=2))
        return
    
    # Perform project scan
    print(f"🔍 Scanning project: {args.project_path}")
    result = scanner.scan_project(
        include_hidden=args.include_hidden,
        max_workers=args.max_workers
    )
    
    if result.get('status') == 'success':
        print(f"✅ Scan completed: {result['files_analyzed']} files analyzed")
        print(f"🌍 Languages detected: {result['languages_detected']}")
        print(f"📄 Report saved: {result['report_path']}")
    else:
        print(f"❌ Scan failed: {result.get('error', 'Unknown error')}")


if __name__ == "__main__":
    main()
