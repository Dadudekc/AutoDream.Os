#!/usr/bin/env python3
"""
Core logic for devlog analytics system startup script.
"""

import os
import subprocess
import sys
import time
from pathlib import Path

# Import ThreadManager for safe threading
from src.core.resource_management.thread_manager import get_thread_manager


class Colors:
    """Colors for console output."""
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"


class DevlogAnalyticsSystem:
    """Devlog Analytics System startup manager."""
    
    def __init__(self):
        """Initialize the system."""
        self.script_dir = Path(__file__).parent
        self.services = []
        self.thread_manager = get_thread_manager()
    
    def print_header(self):
        """Print startup header."""
        print(f"{Colors.BOLD}{Colors.BLUE}🤖 Devlog Analytics System Starting...{Colors.ENDC}")
        print("=" * 50)
        print()
    
    def run_service(self, name: str, command: list, port: int, delay: float = 0):
        """Run a service in a separate thread using ThreadManager."""
        def _run():
            if delay > 0:
                print(f"{Colors.YELLOW}⏳ Starting {name} in {delay}s...{Colors.ENDC}")
                time.sleep(delay)

            try:
                print(f"{Colors.GREEN}🚀 Starting {name} on port {port}...{Colors.ENDC}")
                result = subprocess.run(command, cwd=self.script_dir)
                if result.returncode != 0:
                    print(f"{Colors.RED}❌ {name} exited with code {result.returncode}{Colors.ENDC}")
            except Exception as e:
                print(f"{Colors.RED}❌ Error starting {name}: {e}{Colors.ENDC}")

        # Use ThreadManager for proper thread lifecycle management
        thread = self.thread_manager.start_thread(target=_run, name=name, daemon=True)
        return thread
    
    def check_requirements(self):
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
    
    def check_node_modules(self):
        """Check if React dependencies are installed."""
        dashboard_dir = self.script_dir / "web_dashboard"
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
    
    def start_services(self):
        """Start all services."""
        # 1. Start WebSocket Server (port 8001)
        self.services.append(
            self.run_service(
                "WebSocket Server", [sys.executable, "web_dashboard/websocket.py"], 8001, delay=0
            )
        )

        # 2. Start Devlog Analytics API (port 8002)
        self.services.append(
            self.run_service(
                "Devlog Analytics API",
                [sys.executable, "src/services/devlog_analytics_api.py"],
                8002,
                delay=1,
            )
        )

        # 3. Start React Dashboard (port 3000)
        dashboard_dir = self.script_dir / "web_dashboard"
        if (dashboard_dir / "node_modules").exists():
            self.services.append(self.run_service("React Dashboard", ["npm", "start"], 3000, delay=2))
    
    def print_system_info(self):
        """Print system information."""
        print()
        print(f"{Colors.BOLD}{Colors.GREEN}✅ Devlog Analytics System Started!{Colors.ENDC}")
        print("=" * 50)
        print(f"{Colors.BLUE}📊 Available Services:{Colors.ENDC}")
        print("  • WebSocket Server:   http://localhost:8001")
        print("  • Analytics API:      http://localhost:8002")
        print("  • React Dashboard:    http://localhost:3000")
        print()
        print(f"{Colors.BLUE}📋 API Endpoints:{Colors.ENDC}")
        print("  • /api/devlogs - Get devlogs with filtering")
        print("  • /api/devlogs/analytics - Get analytics data")
        print("  • /api/devlogs/export/<format> - Export devlogs")
        print("  • /api/devlogs/agents - Get agent statistics")
        print("  • /api/devlogs/trends - Get trend data")
        print()
        print(f"{Colors.YELLOW}🛠️  Development Notes:{Colors.ENDC}")
        print("  • Use Ctrl+C to stop all services")
        print("  • Check console output for service logs")
        print("  • WebSocket provides real-time updates")
        print("  • API supports JSON, CSV, and Excel export")
        print()
        print(
            f"{Colors.GREEN}🎯 Ready to use! Open http://localhost:3000 for the dashboard{Colors.ENDC}"
        )
    
    def run(self):
        """Run the complete system."""
        self.print_header()

        # Check requirements
        if not self.check_requirements():
            sys.exit(1)

        if not self.check_node_modules():
            print(f"{Colors.YELLOW}⚠️  Continuing without React dashboard...{Colors.ENDC}")

        # Change to script directory
        os.chdir(self.script_dir)

        # Start services
        self.start_services()
        self.print_system_info()

        try:
            # Keep main thread alive
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print()
            print(f"{Colors.YELLOW}🛑 Shutting down services...{Colors.ENDC}")
            # Properly stop all threads using ThreadManager
            stopped = self.thread_manager.stop_all(timeout=5.0)
            print(f"{Colors.GREEN}✅ Stopped {stopped} service threads{Colors.ENDC}")
