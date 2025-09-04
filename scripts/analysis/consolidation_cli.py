from ..core.unified_entry_point_system import main
#!/usr/bin/env python3
"""
CLI Interface for Logic Consolidation System
==========================================

Command-line interface for the logic consolidation system.

Author: Agent-8 (Integration Enhancement Optimization Manager)
License: MIT
"""




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



if __name__ == "__main__":
    main()
