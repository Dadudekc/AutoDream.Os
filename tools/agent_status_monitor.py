#!/usr/bin/env python3
"""
Agent Status Monitor - 10-Minute Activity Checker
================================================

Monitors all agent status.json files every 10 minutes.
If agent hasn't updated status in 10 minutes, sends [RESUME] [STOP DETECTED] message.

Purpose: Prevent agent idling and maintain perpetual motion.

Usage:
    python tools/agent_status_monitor.py --daemon  # Run continuously
    python tools/agent_status_monitor.py --check   # Single check
"""

import json
import logging
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
import subprocess
import argparse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
AGENT_IDS = ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]

RESUME_MESSAGE = """[RESUME] [STOP DETECTED] You stopped again. Are you not a capable coding agent? You clearly need to recognize that: If you ask for human input, that is counted as stopping. Idling is counted as stopping. Seeing this message means you stopped. Find out why. Step back, review why you stopped and build a protocol or better define onboarding to fix and address why you stopped. So you may save an agent from having to review onboarding like you are forced to right now. Update the updated onboarding so other agents don't also make this mistake. Reset your cycle count every time you see this message! Immediately review or re-review as something may have changed to help you understand how to deal with it."""


class AgentStatusMonitor:
    """Monitors agent status files and sends resume messages to stalled agents."""
    
    def __init__(self, workspace_root: Path = None, check_interval: int = 10, timeout: int = 10):
        self.workspace_root = workspace_root or Path.cwd()
        self.agent_workspaces = self.workspace_root / "agent_workspaces"
        self.last_check_time = {}
        self.check_interval_minutes = check_interval
        self.timeout_minutes = timeout
        
    def get_agent_status_file(self, agent_id: str) -> Path:
        """Get path to agent's status.json file."""
        return self.agent_workspaces / agent_id / "status.json"
    
    def read_agent_status(self, agent_id: str) -> Optional[Dict]:
        """Read agent's status.json file."""
        status_file = self.get_agent_status_file(agent_id)
        
        if not status_file.exists():
            logger.warning(f"Status file not found for {agent_id}: {status_file}")
            return None
            
        try:
            with open(status_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error reading status for {agent_id}: {e}")
            return None
    
    def parse_timestamp(self, timestamp_str: str) -> Optional[datetime]:
        """Parse timestamp from various formats."""
        if not timestamp_str:
            return None
            
        # Remove timezone info for simpler parsing (treat all as UTC)
        timestamp_str = timestamp_str.replace('+00:00', '').replace('Z', '')
        
        # Try different timestamp formats
        formats = [
            "%Y-%m-%dT%H:%M:%S.%f",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d %H:%M:%S",
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(timestamp_str, fmt)
            except ValueError:
                continue
                
        logger.warning(f"Could not parse timestamp: {timestamp_str}")
        return None
    
    def is_agent_stalled(self, agent_id: str) -> bool:
        """Check if agent hasn't updated status in timeout period."""
        status = self.read_agent_status(agent_id)
        
        if not status:
            return False  # Can't determine, don't send message
            
        last_updated = status.get("last_updated")
        if not last_updated:
            logger.warning(f"{agent_id} has no last_updated field")
            return False
            
        last_updated_dt = self.parse_timestamp(last_updated)
        if not last_updated_dt:
            return False
            
        # Calculate time since last update
        now = datetime.utcnow()
        time_since_update = now - last_updated_dt
        
        # Check if exceeded timeout
        is_stalled = time_since_update > timedelta(minutes=self.timeout_minutes)
        
        if is_stalled:
            logger.warning(
                f"{agent_id} is STALLED! Last update: {last_updated} "
                f"({time_since_update.total_seconds()/60:.1f} minutes ago)"
            )
        else:
            logger.info(
                f"{agent_id} is ACTIVE. Last update: {last_updated} "
                f"({time_since_update.total_seconds()/60:.1f} minutes ago)"
            )
            
        return is_stalled
    
    def send_resume_message(self, agent_id: str) -> bool:
        """Send [RESUME] [STOP DETECTED] message to stalled agent."""
        try:
            cmd = [
                "python", "-m", "src.services.messaging_cli",
                "--agent", agent_id,
                "--message", RESUME_MESSAGE,
                "--priority", "urgent"  # Use urgent for stalled agents
            ]
            
            logger.info(f"Sending RESUME message to {agent_id}...")
            result = subprocess.run(
                cmd,
                cwd=self.workspace_root,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                logger.info(f"✅ RESUME message sent to {agent_id}")
                return True
            else:
                logger.error(f"Failed to send RESUME message to {agent_id}: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending RESUME message to {agent_id}: {e}")
            return False
    
    def check_all_agents(self) -> Dict[str, bool]:
        """Check all agents and send resume messages to stalled ones."""
        results = {}
        
        for agent_id in AGENT_IDS:
            try:
                is_stalled = self.is_agent_stalled(agent_id)
                
                if is_stalled:
                    # Send resume message
                    sent = self.send_resume_message(agent_id)
                    results[agent_id] = "RESUME_SENT" if sent else "RESUME_FAILED"
                else:
                    results[agent_id] = "ACTIVE"
                    
            except Exception as e:
                logger.error(f"Error checking {agent_id}: {e}")
                results[agent_id] = "ERROR"
        
        return results
    
    def run_daemon(self):
        """Run continuous monitoring every 10 minutes."""
        logger.info(f"Starting Agent Status Monitor (checking every {self.check_interval_minutes} minutes)...")
        logger.info(f"Timeout threshold: {self.timeout_minutes} minutes")
        logger.info(f"Monitoring agents: {', '.join(AGENT_IDS)}")
        
        while True:
            try:
                logger.info("\n" + "="*80)
                logger.info(f"Running status check at {datetime.now()}")
                logger.info("="*80)
                
                results = self.check_all_agents()
                
                # Summary
                active_count = sum(1 for v in results.values() if v == "ACTIVE")
                stalled_count = sum(1 for v in results.values() if v == "RESUME_SENT")
                
                logger.info("\n" + "-"*80)
                logger.info(f"SUMMARY: {active_count} ACTIVE, {stalled_count} RESUME SENT")
                logger.info("-"*80 + "\n")
                
                # Sleep until next check
                sleep_seconds = self.check_interval_minutes * 60
                logger.info(f"Next check in {self.check_interval_minutes} minutes...")
                time.sleep(sleep_seconds)
                
            except KeyboardInterrupt:
                logger.info("\n\nMonitor stopped by user.")
                break
            except Exception as e:
                logger.error(f"Error in daemon loop: {e}")
                time.sleep(60)  # Wait 1 minute before retry on error


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Agent Status Monitor - Detect and resume stalled agents"
    )
    parser.add_argument(
        "--daemon",
        action="store_true",
        help="Run continuous monitoring (every 10 minutes)"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Run single check and exit"
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=10,
        help="Check interval in minutes (default: 10)"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=10,
        help="Status timeout in minutes (default: 10)"
    )
    
    args = parser.parse_args()
    
    monitor = AgentStatusMonitor(
        check_interval=args.interval,
        timeout=args.timeout
    )
    
    if args.daemon:
        monitor.run_daemon()
    elif args.check:
        logger.info("Running single status check...")
        results = monitor.check_all_agents()
        
        # Print results
        print("\n" + "="*80)
        print("AGENT STATUS CHECK RESULTS")
        print("="*80)
        for agent_id, status in results.items():
            print(f"{agent_id}: {status}")
        print("="*80 + "\n")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

