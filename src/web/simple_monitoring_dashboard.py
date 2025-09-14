#!/usr/bin/env python3
"""
🔄 UNIFIED DASHBOARD WRAPPER - Simple_Monitoring
======================================================

This file replaces the original simple_monitoring_dashboard.py with a wrapper
that uses the unified dashboard system.

Original file: /workspace/src/web/simple_monitoring_dashboard.py
Dashboard type: simple_monitoring
Migration date: 2025-09-14T20:13:06.390070

This wrapper maintains backward compatibility while using the unified system.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from web.unified_dashboard_manager import create_dashboard, DashboardType

def main():
    """Main entry point for the unified dashboard."""
    try:
        # Create dashboard instance
        dashboard = create_dashboard("simple_monitoring")
        
        # Run the dashboard
        dashboard.run()
        
    except Exception as e:
        print(f"Error running simple_monitoring dashboard: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
