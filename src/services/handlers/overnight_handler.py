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
from typing import Any, Dict, List, Optional


class OvernightHandler:
    """
    Handles overnight autonomous system commands.
    
    Manages overnight work cycle activation and monitoring.
    """
    
    def __init__(self):
        """Initialize overnight handler."""
        self.is_running = False
        self.cycle_count = 0
    
    def handle_overnight_commands(self, args) -> bool:
        """Handle overnight autonomous system commands."""
        try:
            if args.overnight:
                print("🌙 Starting Overnight Autonomous Work Cycle System...")
                print("⏰ Will send work cycle messages every 10 minutes")
                print("🔄 Press Ctrl+C to stop the system")
                print("-" * 60)
                
                # Run the overnight autonomous system
                script_path = Path(__file__).parent.parent.parent.parent / "scripts" / "overnight_autonomous_system.py"
                subprocess.run([sys.executable, str(script_path)])
                return True
                
        except Exception as e:
            print(f"❌ Error with overnight system: {e}")
            return False
        
        return False
    
    def start_overnight_cycle(self) -> bool:
        """Start overnight work cycle."""
        try:
            self.is_running = True
            self.cycle_count = 0
            print("🌙 Overnight cycle started")
            return True
        except Exception as e:
            print(f"❌ Error starting overnight cycle: {e}")
            return False
    
    def stop_overnight_cycle(self) -> bool:
        """Stop overnight work cycle."""
        try:
            self.is_running = False
            print("🌙 Overnight cycle stopped")
            return True
        except Exception as e:
            print(f"❌ Error stopping overnight cycle: {e}")
            return False
    
    def get_cycle_status(self) -> Dict[str, Any]:
        """Get current cycle status."""
        return {
            "is_running": self.is_running,
            "cycle_count": self.cycle_count,
            "status": "active" if self.is_running else "stopped"
        }
    
    def increment_cycle(self):
        """Increment cycle count."""
        self.cycle_count += 1
    
    def reset_cycle(self):
        """Reset cycle count."""
        self.cycle_count = 0
