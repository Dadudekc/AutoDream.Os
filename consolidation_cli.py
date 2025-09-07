#!/usr/bin/env python3
"""
CLI Interface for Logic Consolidation System
==========================================

Command-line interface for the logic consolidation system.

Author: Agent-8 (Integration Enhancement Optimization Manager)
License: MIT
"""

import argparse
import sys
from typing import Dict, Any

from consolidation_core import LogicConsolidatorCore


def create_parser():
    """Create command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Logic Consolidation System - Agent-8 Mission",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run complete logic consolidation mission
  python consolidation_cli.py --mission
  
  # Scan for logic patterns only
  python consolidation_cli.py --scan
  
  # Identify duplicates only
  python consolidation_cli.py --identify
  
  # Create consolidated logic systems
  python consolidation_cli.py --consolidate
  
  # Generate report only
  python consolidation_cli.py --report
        """
    )
    
    # Mission options
    parser.add_argument("--mission", action="store_true", help="Run complete logic consolidation mission")
    parser.add_argument("--scan", action="store_true", help="Scan for logic patterns only")
    parser.add_argument("--identify", action="store_true", help="Identify duplicates only")
    parser.add_argument("--consolidate", action="store_true", help="Create consolidated logic systems")
    parser.add_argument("--report", action="store_true", help="Generate consolidation report")
    
    # Output options
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")
    parser.add_argument("--output", "-o", help="Output directory for consolidated files")
    
    return parser


def main():
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    # Initialize consolidator
    consolidator = LogicConsolidatorCore()
    
    # Handle mission execution
    if args.mission:
        print("🚀 Logic Consolidation System - Agent-8")
        print("=" * 60)
        print("Mission: SSOT Priority - Eliminate All Remaining Duplicates")
        print("Status: MISSION ACTIVE - Continuous operation until SSOT achieved")
        print()

        # Run logic consolidation mission
        results = consolidator.run_logic_consolidation_mission()

        if results['success']:
            print(f"\n✅ Logic consolidation mission completed successfully!")
            print(f"📊 Final Results:")
            print(f"   - Logic pattern types found: {results['logic_pattern_types_found']}")
            print(f"   - Total duplicates found: {results['total_duplicates_found']}")
            print(f"   - Total duplicates eliminated: {results['total_duplicates_eliminated']}")
            print(f"   - Consolidated logic systems created: {results['consolidated_logic_systems_created']}")
            print(f"   - Logic report: {results['logic_report']}")
            print()
            print("🎯 **MISSION ACCOMPLISHED - LOGIC CONSOLIDATION COMPLETE**")
        else:
            print(f"\n❌ Logic consolidation failed: {results.get('error', 'Unknown error')}")
        return
    
    # Handle individual operations
    if args.scan:
        print("🔍 Scanning for logic patterns...")
        logic_patterns = consolidator.scan_for_logic_patterns()
        print(f"✅ Found logic patterns in {len(logic_patterns)} categories")
        for pattern_type, patterns in logic_patterns.items():
            if patterns:
                print(f"   - {pattern_type}: {len(patterns)} patterns")
        return
    
    if args.identify:
        print("🔍 Identifying duplicate logic patterns...")
        # First scan, then identify
        consolidator.scan_for_logic_patterns()
        duplicates = consolidator.identify_duplicate_logic()
        print(f"✅ Identified duplicates in {len(duplicates)} categories")
        for pattern_type, duplicate_groups in duplicates.items():
            if duplicate_groups:
                total_duplicates = sum(len(group) for group in duplicate_groups)
                print(f"   - {pattern_type}: {total_duplicates} duplicates in {len(duplicate_groups)} groups")
        return
    
    if args.consolidate:
        print("🔧 Creating consolidated logic systems...")
        # First scan and identify, then consolidate
        consolidator.scan_for_logic_patterns()
        consolidator.identify_duplicate_logic()
        consolidated_files = consolidator.create_consolidated_logic_system()
        print(f"✅ Created {len(consolidated_files)} consolidated logic systems")
        for pattern_type, file_path in consolidated_files.items():
            print(f"   - {pattern_type}: {file_path}")
        return
    
    if args.report:
        print("📊 Generating logic consolidation report...")
        # Run full mission to generate report
        results = consolidator.run_logic_consolidation_mission()
        if results['success']:
            print(f"✅ Report generated: {results['logic_report']}")
        else:
            print(f"❌ Failed to generate report: {results.get('error', 'Unknown error')}")
        return
    
    # If no arguments provided, show help
    if len(sys.argv) == 1:
        parser.print_help()
        return
    
    print("❌ No action specified. Use --help for usage information.")


if __name__ == "__main__":
    main()
