#!/usr/bin/env python3
"""
Devlog Analytics System Startup Script
=====================================

Starts all components of the devlog analytics system:
1. Devlog Analytics API (port 8002)
2. Enhanced WebSocket Server (port 8001)
3. React Dashboard (port 3000)

Usage:
    python run_devlog_analytics_system.py

Components:
- Analytics API: REST endpoints for querying devlogs
- WebSocket Server: Real-time updates for dashboard
- React Dashboard: Web interface for visualization
"""

import subprocess
import sys
import time
import threading
import os
from pathlib import Path

# Colors for console output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header():
    """Print startup header."""
    print(f"{Colors.BOLD}{Colors.BLUE}🤖 Devlog Analytics System Starting...{Colors.ENDC}")
    print("=" * 50)
    print()

def run_service(name: str, command: list, port: int, delay: float = 0):
    """Run a service in a separate thread."""
    def _run():
        if delay > 0:
            print(f"{Colors.YELLOW}⏳ Starting {name} in {delay}s...{Colors.ENDC}")
            time.sleep(delay)

        try:
            print(f"{Colors.GREEN}🚀 Starting {name} on port {port}...{Colors.ENDC}")
            result = subprocess.run(command, cwd=Path(__file__).parent)
            if result.returncode != 0:
                print(f"{Colors.RED}❌ {name} exited with code {result.returncode}{Colors.ENDC}")
        except Exception as e:
            print(f"{Colors.RED}❌ Error starting {name}: {e}{Colors.ENDC}")

    thread = threading.Thread(target=_run, daemon=True)
    thread.start()
    return thread

def check_requirements():
    """Check if all required dependencies are installed."""
    print(f"{Colors.YELLOW}📋 Checking requirements...{Colors.ENDC}")

    requirements = [
        ("flask", "pip install flask"),
        ("flask-cors", "pip install flask-cors"),
        ("websockets", "pip install websockets"),
    ]

    missing = []
    for package, install_cmd in requirements:
        try:
            __import__(package.replace("-", "_"))
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} - missing")
            missing.append(install_cmd)

    if missing:
        print(f"{Colors.RED}❌ Missing dependencies. Install them with:{Colors.ENDC}")
        for cmd in missing:
            print(f"    {cmd}")
        return False

    print(f"{Colors.GREEN}✅ All Python requirements met{Colors.ENDC}")
    return True

def check_node_modules():
    """Check if React dependencies are installed."""
    dashboard_dir = Path(__file__).parent / "web_dashboard"
    package_json = dashboard_dir / "package.json"

    if not package_json.exists():
        print(f"{Colors.YELLOW}⚠️  React dashboard not found at {dashboard_dir}{Colors.ENDC}")
        return False

    node_modules = dashboard_dir / "node_modules"
    if not node_modules.exists():
        print(f"{Colors.RED}❌ React dependencies not installed{Colors.ENDC}")
        print(f"{Colors.YELLOW}💡 Run 'npm install' in the web_dashboard directory{Colors.ENDC}")
        return False

    print(f"{Colors.GREEN}✅ React dependencies installed{Colors.ENDC}")
    return True

def main():
    """Main startup function."""
    print_header()

    # Check requirements
    if not check_requirements():
        sys.exit(1)

    if not check_node_modules():
        print(f"{Colors.YELLOW}⚠️  Continuing without React dashboard...{Colors.ENDC}")

    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)

    # Start services
    services = []

    # 1. Start WebSocket Server (port 8001)
    services.append(run_service(
        "WebSocket Server",
        [sys.executable, "web_dashboard/websocket.py"],
        8001,
        delay=0
    ))

    # 2. Start Devlog Analytics API (port 8002)
    services.append(run_service(
        "Devlog Analytics API",
        [sys.executable, "src/services/devlog_analytics_api.py"],
        8002,
        delay=1
    ))

    # 3. Start React Dashboard (port 3000)
    dashboard_dir = Path(__file__).parent / "web_dashboard"
    if (dashboard_dir / "node_modules").exists():
        services.append(run_service(
            "React Dashboard",
            ["npm", "start"],
            3000,
            delay=2
        ))

    print()
    print(f"{Colors.BOLD}{Colors.GREEN}✅ Devlog Analytics System Started!{Colors.ENDC}")
    print("=" * 50)
    print(f"{Colors.BLUE}📊 Available Services:{Colors.ENDC}")
    print(f"  • WebSocket Server:   http://localhost:8001")
    print(f"  • Analytics API:      http://localhost:8002")
    print(f"  • React Dashboard:    http://localhost:3000")
    print()
    print(f"{Colors.BLUE}📋 API Endpoints:{Colors.ENDC}")
    print(f"  • /api/devlogs - Get devlogs with filtering")
    print(f"  • /api/devlogs/analytics - Get analytics data")
    print(f"  • /api/devlogs/export/<format> - Export devlogs")
    print(f"  • /api/devlogs/agents - Get agent statistics")
    print(f"  • /api/devlogs/trends - Get trend data")
    print()
    print(f"{Colors.YELLOW}🛠️  Development Notes:{Colors.ENDC}")
    print(f"  • Use Ctrl+C to stop all services")
    print(f"  • Check console output for service logs")
    print(f"  • WebSocket provides real-time updates")
    print(f"  • API supports JSON, CSV, and Excel export")
    print()
    print(f"{Colors.GREEN}🎯 Ready to use! Open http://localhost:3000 for the dashboard{Colors.ENDC}")

    try:
        # Keep main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print()
        print(f"{Colors.YELLOW}🛑 Shutting down services...{Colors.ENDC}")
        # Services will stop when main thread exits (daemon threads)

if __name__ == "__main__":
    main()

