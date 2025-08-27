#!/usr/bin/env python3
"""
Duplication Detector Main - Agent Cellphone V2
==============================================

Main entry point for the refactored duplication detection system.
Follows V2 standards: ≤200 LOC, OOP design, SRP compliance.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import argparse
import logging
import sys

from src.utils.stability_improvements import safe_import  # stability_manager removed due to abstract class issues
from pathlib import Path

from duplication.duplication_detector import DuplicationDetector
from duplication.duplication_reporter import DuplicationReporter


class DuplicationDetectorMain:
    """Main orchestrator for duplication detection"""
    
    def __init__(self):
        self.setup_logging()
        self.detector = DuplicationDetector()
        self.reporter = DuplicationReporter()
    
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )
    
    def run_analysis(self, root_path: str, output_path: str = None, 
                    min_similarity: float = 0.8, min_block_size: int = 5):
        """Run complete duplication analysis"""
        try:
            # Configure detector
            self.detector.min_similarity = min_similarity
            self.detector.min_block_size = min_block_size
            
            # Run analysis
            issues = self.detector.analyze_codebase(root_path)
            
            # Count Python files
            python_files = list(Path(root_path).rglob("*.py"))
            total_files = len(python_files)
            
            # Generate report
            report = self.reporter.generate_report(issues, total_files)
            
            # Display results
            self.reporter.print_report(report)
            
            # Save report if output path specified
            if output_path:
                self.reporter.save_json_report(report, output_path)
            
            return len(issues)
            
        except Exception as e:
            logging.error(f"Analysis failed: {e}")
            return -1
    
    def main(self):
        """Main entry point"""
        parser = argparse.ArgumentParser(
            description="Advanced Duplication Detector for Agent Cellphone V2"
        )
        parser.add_argument(
            "path", 
            help="Path to analyze (default: current directory)",
            nargs="?", 
            default="."
        )
        parser.add_argument(
            "--output", "-o",
            help="Output JSON report path"
        )
        parser.add_argument(
            "--min-similarity", "-s",
            type=float,
            default=0.8,
            help="Minimum similarity threshold (0.0-1.0)"
        )
        parser.add_argument(
            "--min-block-size", "-b",
            type=int,
            default=5,
            help="Minimum code block size to analyze"
        )
        parser.add_argument(
            "--verbose", "-v",
            action="store_true",
            help="Verbose output"
        )
        
        args = parser.parse_args()
        
        if args.verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        
        # Validate arguments
        if not Path(args.path).exists():
            print(f"Error: Path '{args.path}' does not exist")
            sys.exit(1)
        
        if not (0.0 <= args.min_similarity <= 1.0):
            print("Error: min-similarity must be between 0.0 and 1.0")
            sys.exit(1)
        
        if args.min_block_size < 1:
            print("Error: min-block-size must be at least 1")
            sys.exit(1)
        
        # Run analysis
        print(f"🔍 Analyzing codebase at: {args.path}")
        print(f"📊 Settings: min-similarity={args.min_similarity}, min-block-size={args.min_block_size}")
        print()
        
        issue_count = self.run_analysis(
            args.path,
            args.output,
            args.min_similarity,
            args.min_block_size
        )
        
        if issue_count >= 0:
            print(f"\n✅ Analysis complete! Found {issue_count} duplication issues.")
            if args.output:
                print(f"📄 Report saved to: {args.output}")
        else:
            print("\n❌ Analysis failed!")
            sys.exit(1)


if __name__ == "__main__":
    main_app = DuplicationDetectorMain()
    main_app.main()

