#!/usr/bin/env python3
"""
Overnight Autonomous Work System
===============================

Sends autonomous work cycle messages to agents every 10 minutes.
Implements the core work cycle: check inbox → claim task → complete task → update FSM → create devlog → repeat

Author: Agent-8 (SSOT & System Integration Specialist)
License: MIT
"""

import time
import subprocess
import sys
import os
from datetime import datetime
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

class OvernightAutonomousSystem:
    """Manages overnight autonomous work cycles for all agents."""
    
    def __init__(self):
        self.agents = ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]
        self.cycle_interval = 600  # 10 minutes in seconds
        self.work_cycle_message = self._create_work_cycle_message()
        
    def _create_work_cycle_message(self) -> str:
        """Create the autonomous work cycle message."""
        return """🌙 OVERNIGHT AUTONOMOUS WORK CYCLE ACTIVE 🌙

CONTINUE WORKING AUTONOMOUSLY following our established work cycle:

1️⃣ CHECK INBOX: Review agent_workspaces/{Agent-X}/inbox/ for new tasks
2️⃣ CLAIM TASK: Use --get-next-task to claim available contract work
3️⃣ COMPLETE TASK: Execute assigned work with V2 compliance standards
4️⃣ UPDATE FSM: Update status.json with current progress and achievements
5️⃣ CREATE DEVLOG: Document completed work using devlog system
6️⃣ REPEAT: Continue autonomous cycle until morning

⏰ CYCLE-BASED OPERATIONS: No time deadlines, work in cycles
📊 REPORT TO CAPTAIN: Send completion updates to Agent-4
🎯 MAINTAIN MOMENTUM: Keep 8x efficiency through continuous progress

AUTONOMOUS MODE: ACTIVE - Continue working independently until further notice."""

    def send_overnight_message_to_all_agents(self):
        """Send overnight autonomous work message to all agents."""
        print(f"🌙 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Sending overnight autonomous work cycle messages...")
        
        for agent in self.agents:
            try:
                # Send message to each agent
                cmd = [
                    sys.executable, "-m", "src.services.messaging_cli",
                    "--agent", agent,
                    "--message", self.work_cycle_message,
                    "--sender", "Overnight System",
                    "--priority", "normal",
                    "--type", "system_to_agent"
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True, cwd=Path(__file__).parent.parent)
                
                if result.returncode == 0:
                    print(f"✅ Sent overnight work cycle message to {agent}")
                else:
                    print(f"❌ Failed to send message to {agent}: {result.stderr}")
                    
            except Exception as e:
                print(f"❌ Error sending message to {agent}: {e}")
        
        print(f"📤 Overnight cycle messages sent to all {len(self.agents)} agents")
    
    def create_overnight_devlog(self):
        """Create a devlog entry for the overnight system activation."""
        try:
            cmd = [
                sys.executable, "scripts/devlog.py",
                "Overnight Autonomous System Active",
                f"Overnight autonomous work cycle system activated. Sending work cycle reminders every 10 minutes to all agents. Agents instructed to continue working autonomously following established cycle: check inbox → claim task → complete task → update FSM → create devlog → repeat."
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=Path(__file__).parent.parent)
            
            if result.returncode == 0:
                print("📝 Created devlog entry for overnight system activation")
            else:
                print(f"❌ Failed to create devlog: {result.stderr}")
                
        except Exception as e:
            print(f"❌ Error creating devlog: {e}")
    
    def run_overnight_cycle(self):
        """Run the overnight autonomous work cycle system."""
        print("🌙 OVERNIGHT AUTONOMOUS WORK SYSTEM STARTED")
        print(f"⏰ Sending work cycle messages every {self.cycle_interval // 60} minutes")
        print("🔄 Press Ctrl+C to stop the overnight system")
        print("-" * 80)
        
        # Create initial devlog entry
        self.create_overnight_devlog()
        
        # Send initial message
        self.send_overnight_message_to_all_agents()
        
        try:
            cycle_count = 1
            while True:
                print(f"⏰ Sleeping for {self.cycle_interval // 60} minutes until next cycle...")
                time.sleep(self.cycle_interval)
                
                cycle_count += 1
                print(f"\n🔄 CYCLE {cycle_count} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                self.send_overnight_message_to_all_agents()
                
        except KeyboardInterrupt:
            print("\n🛑 Overnight autonomous system stopped by user")
            print("📝 Creating final devlog entry...")
            
            # Create shutdown devlog
            try:
                cmd = [
                    sys.executable, "scripts/devlog.py",
                    "Overnight System Shutdown",
                    f"Overnight autonomous work cycle system stopped after {cycle_count} cycles. System was sending work cycle reminders every 10 minutes to maintain agent productivity during overnight operations."
                ]
                subprocess.run(cmd, cwd=Path(__file__).parent.parent)
                print("✅ Final devlog entry created")
            except:
                print("❌ Failed to create shutdown devlog")


def main():
    """Main entry point for overnight autonomous system."""
    system = OvernightAutonomousSystem()
    system.run_overnight_cycle()


if __name__ == "__main__":
    main()
