#!/usr/bin/env python3
"""
🐝 SWARM MONITORING DASHBOARD LAUNCHER - Agent-7
Quick launcher for the SWARM web monitoring interface

Usage:
    python run_web_monitoring_dashboard.py

This will start the web monitoring dashboard on http://localhost:8000
"""

import sys
import os
from pathlib import Path

# Add src to Python path
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

try:
    from web.swarm_monitoring_dashboard import SwarmMonitoringDashboard

    def main():
        """Main function to run the dashboard"""
        print("🐝 SWARM MONITORING DASHBOARD - Agent-7")
        print("=" * 50)
        print("🚀 Starting SWARM Web Monitoring Interface...")
        print("📊 Real-time monitoring for SWARM operations")
        print("🌐 Dashboard will be available at: http://localhost:8000")
        print("⏹️  Press Ctrl+C to stop the server")
        print("=" * 50)

        # Create and run dashboard
        dashboard = SwarmMonitoringDashboard()

        try:
            dashboard.run(host="localhost", port=8000)
        except KeyboardInterrupt:
            print("\n🐝 Shutting down SWARM Monitoring Dashboard...")
            dashboard.stop_monitoring()
            print("✅ Dashboard stopped successfully")
        except Exception as e:
            print(f"❌ Error running dashboard: {e}")
            dashboard.stop_monitoring()
            sys.exit(1)

    if __name__ == "__main__":
        main()

except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running this from the project root directory")
    print("Expected path structure:")
    print("  src/web/swarm_monitoring_dashboard.py")
    sys.exit(1)
