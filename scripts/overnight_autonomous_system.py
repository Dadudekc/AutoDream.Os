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
from services.utils.agent_registry import list_agents

class OvernightAutonomousSystem:
    """Manages overnight autonomous work cycles for all agents."""

    def __init__(self):
        self.agents = list_agents()
        self.cycle_interval = 600  # 10 minutes in seconds
        self.work_cycle_message = self._create_work_cycle_message()
        self.message_count = 0
        self.cleanup_interval = 3  # Cleanup every 3 messages
        
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

🧹 CLEANUP SYSTEM: Automated cleanup every 3 messages (30 minutes)
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

        self.message_count += 1
        print(f"📤 Overnight cycle messages sent to all {len(self.agents)} agents (Message #{self.message_count})")

        # Trigger cleanup every 3 messages
        if self.message_count % self.cleanup_interval == 0:
            print(f"🧹 CLEANUP PHASE TRIGGERED - Message #{self.message_count} (every {self.cleanup_interval} messages)")
            self.perform_cleanup_phase()
    
    def create_overnight_devlog(self):
        """Create a devlog entry for the overnight system activation."""
        try:
            cmd = [
                sys.executable, "scripts/devlog.py",
                "Overnight Autonomous System Active - Cleanup System Integrated",
                f"Overnight autonomous work cycle system activated with automated cleanup every 3 messages (30 minutes). Sending work cycle reminders every 10 minutes to all agents. Agents instructed to continue working autonomously following established cycle: check inbox → claim task → complete task → update FSM → create devlog → repeat. Cleanup system will automatically remove cache files and temporary files to maintain optimal performance."
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=Path(__file__).parent.parent)
            
            if result.returncode == 0:
                print("📝 Created devlog entry for overnight system activation")
            else:
                print(f"❌ Failed to create devlog: {result.stderr}")
                
        except Exception as e:
            print(f"❌ Error creating devlog: {e}")

    def perform_cleanup_phase(self):
        """Perform cleanup operations every 3 messages."""
        print("🧹 STARTING CLEANUP PHASE...")

        try:
            # Remove Python cache files
            print("🗑️ Removing Python cache files...")
            cache_cleanup_cmd = [
                sys.executable, "scripts/cleanup_unnecessary_files.py"
            ] if os.path.exists("scripts/cleanup_unnecessary_files.py") else [
                "find", ".", "-name", "__pycache__", "-type", "d", "-exec", "rm", "-rf", "{}", "+"
            ]

            if os.path.exists("scripts/cleanup_unnecessary_files.py"):
                result = subprocess.run(cache_cleanup_cmd, capture_output=True, text=True, cwd=Path(__file__).parent.parent)
                if result.returncode == 0:
                    print("✅ Cache cleanup script executed successfully")
                else:
                    print(f"⚠️ Cache cleanup script failed: {result.stderr}")
            else:
                # Fallback: manual cache cleanup
                import shutil
                for root, dirs, files in os.walk(Path(__file__).parent.parent):
                    if '__pycache__' in dirs:
                        cache_dir = os.path.join(root, '__pycache__')
                        try:
                            shutil.rmtree(cache_dir)
                            print(f"🗑️ Removed cache: {cache_dir}")
                        except:
                            pass
                print("✅ Manual cache cleanup completed")

            # Remove temporary files
            print("🗂️ Cleaning temporary files...")
            temp_files = [
                "*.tmp", "*.temp", "*.bak", "*.backup",
                ".DS_Store", "Thumbs.db", "*.log.tmp"
            ]

            for pattern in temp_files:
                try:
                    import glob
                    for file_path in glob.glob(os.path.join(Path(__file__).parent.parent, "**", pattern), recursive=True):
                        try:
                            os.remove(file_path)
                            print(f"🗑️ Removed temp file: {file_path}")
                        except:
                            pass
                except:
                    pass

            print("✅ Cleanup phase completed successfully")

            # Create cleanup devlog
            self.create_cleanup_devlog()

        except Exception as e:
            print(f"❌ Error during cleanup phase: {e}")

    def create_cleanup_devlog(self):
        """Create a devlog entry for cleanup operations."""
        try:
            cmd = [
                sys.executable, "scripts/devlog.py",
                "Overnight System Cleanup Phase Completed",
                f"Automated cleanup phase executed after {self.message_count} messages. Removed cache files, temporary files, and performed system maintenance. System continues operating with optimal performance."
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, cwd=Path(__file__).parent.parent)

            if result.returncode == 0:
                print("📝 Created cleanup devlog entry")
            else:
                print(f"❌ Failed to create cleanup devlog: {result.stderr}")

        except Exception as e:
            print(f"❌ Error creating cleanup devlog: {e}")

    def run_overnight_cycle(self):
        """Run the overnight autonomous work cycle system."""
        print("🌙 OVERNIGHT AUTONOMOUS WORK SYSTEM STARTED")
        print(f"⏰ Sending work cycle messages every {self.cycle_interval // 60} minutes")
        print(f"🧹 Automated cleanup every {self.cleanup_interval} messages ({self.cleanup_interval * (self.cycle_interval // 60)} minutes)")
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
                    "Overnight System Shutdown - Cleanup System Deactivated",
                    f"Overnight autonomous work cycle system stopped after {cycle_count} cycles. System was sending work cycle reminders every 10 minutes and performing automated cleanup every 3 messages to maintain agent productivity and system performance during overnight operations."
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
