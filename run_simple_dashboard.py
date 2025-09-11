#!/usr/bin/env python3
"""
🐝 SIMPLE SWARM MONITORING DASHBOARD LAUNCHER - Agent-7
Lightweight launcher for the SWARM web monitoring interface

Usage:
    python run_simple_dashboard.py

This will start the simple web monitoring dashboard on http://localhost:8000
No external dependencies required - uses only Python standard library.
"""

import sys
import os
from pathlib import Path

# Add src to Python path
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

try:
    from web.simple_monitoring_dashboard import SimpleSwarmDashboard

    def main():
        """Main function to run the simple dashboard"""
        print("🐝 SIMPLE SWARM MONITORING DASHBOARD - Agent-7")
        print("=" * 50)
        print("🚀 Starting lightweight SWARM monitoring interface...")
        print("📊 Real-time monitoring for SWARM operations")
        print("🌐 Dashboard will be available at: http://localhost:8000")
        print("⚡ No external dependencies required")
        print("⏹️  Press Ctrl+C to stop the server")
        print("=" * 50)

        # Create and run dashboard
        dashboard = SimpleSwarmDashboard(host="localhost", port=8000)

        try:
            dashboard.start()
        except KeyboardInterrupt:
            print("\n🐝 Shutting down SWARM Monitoring Dashboard...")
            dashboard.stop()
            print("✅ Dashboard stopped successfully")
        except Exception as e:
            print(f"❌ Error running dashboard: {e}")
            dashboard.stop()
            sys.exit(1)

    if __name__ == "__main__":
        main()

except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running this from the project root directory")
    print("Expected path structure:")
    print("  src/web/simple_monitoring_dashboard.py")
    sys.exit(1)
