"""
Overnight Handler - V2 Compliant Module
======================================

Handles overnight autonomous system commands.
Extracted from messaging_cli_handlers.py for V2 compliance.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

import subprocess
import sys
from pathlib import Path
from typing import Any, Dict


class OvernightHandler:
    """
    Handles overnight autonomous system commands.
    
    Manages overnight work cycle activation and monitoring.
    """
    
    def __init__(self):
        """Initialize overnight handler."""
        self.is_running = False
    
    def handle_overnight_commands(self, args) -> bool:
        """Handle overnight autonomous system commands."""
        try:
            if args.overnight:
                print("🌙 Starting Overnight Autonomous Work Cycle System...")
                print("⏰ Will send work cycle messages every 10 minutes")
                print("🔄 Press Ctrl+C to stop the system")
                print("-" * 60)

                self.is_running = True
                script_path = (
                    Path(__file__).parent.parent.parent.parent
                    / "scripts"
                    / "overnight_autonomous_system.py"
                )
                try:
                    subprocess.run([sys.executable, str(script_path)], check=False)
                finally:
                    self.is_running = False
                return True

        except Exception as e:
            print(f"❌ Error with overnight system: {e}")
            return False

        return False
    
    def get_status(self) -> Dict[str, Any]:
        """Get current overnight system status."""
        return {
            "is_running": self.is_running,
            "status": "active" if self.is_running else "stopped"
        }
