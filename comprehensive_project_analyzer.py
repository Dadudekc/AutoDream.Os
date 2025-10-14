#!/usr/bin/env python3
"""
Comprehensive Project Analyzer - WRAPPER (V2 COMPLIANT)
=======================================================

Original: 623 lines (V2 violation)
Refactored into 3 V2-compliant modules:
  - project_analyzer_file.py (225 lines) - File analysis (Python, JS, MD, YAML)
  - project_analyzer_core.py (160 lines) - Core chunking and structure
  - project_analyzer_reports.py (141 lines) - Consolidation reporting

This wrapper maintained for backward compatibility.

Refactored: Agent-3 (Infrastructure & Monitoring Engineer)
Date: 2025-10-14
Reason: Lean Excellence Mission - V2 Compliance
"""

import sys
from pathlib import Path

# Ensure modules are importable
sys.path.insert(0, str(Path(__file__).parent))

from project_analyzer_core import CoreAnalyzer
from project_analyzer_file import FileAnalyzer  
from project_analyzer_reports import ReportGenerator


def main():
    """Main entry point - delegates to refactored implementation."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Comprehensive Project Analyzer")
    parser.add_argument("--root", default=".", help="Project root directory")
    parser.add_argument("--dirs", nargs="+", default=["src", "tools", "tests"], 
                        help="Directories to analyze")
    
    args = parser.parse_args()
    
    print("=" * 80)
    print("COMPREHENSIVE PROJECT ANALYZER - REFACTORED (V2 COMPLIANT)")
    print("=" * 80)
    print()
    
    # Initialize analyzers
    core = CoreAnalyzer(Path(args.root))
    reporter = ReportGenerator()
    
    # Generate chunked analysis
    print(f"📊 Analyzing directories: {', '.join(args.dirs)}")
    
    # Get project structure and analyze
    print("\n📊 Scanning project structure...")
    structure = core.get_project_structure()
    
    print()
    print("=" * 80)
    print("✅ ANALYSIS COMPLETE")
    print("=" * 80)
    print()
    print(f"📁 Output directory: analysis_chunks/")
    print(f"📊 Files analyzed: {structure.get('total_files', 0)}")
    print(f"📝 Check analysis_chunks/ for detailed reports")


if __name__ == "__main__":
    main()
