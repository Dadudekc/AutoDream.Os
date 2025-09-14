#!/usr/bin/env python3
"""
🔄 UNIFIED DASHBOARD WRAPPER - Analytics
======================================================

This file replaces the original analytics_dashboard.py with a wrapper
that uses the unified dashboard system.

Original file: /workspace/src/web/analytics_dashboard.py
Dashboard type: analytics
Migration date: 2025-09-14T20:13:06.389325

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
        dashboard = create_dashboard("analytics")
        
        # Run the dashboard
        dashboard.run()
        
    except Exception as e:
        print(f"Error running analytics dashboard: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
