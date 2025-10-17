#!/usr/bin/env python3
"""
Agent Status Monitor - Activity Checker
=========================================

Monitors all agent status.json files for inactivity.
- Active execution agents: 10-minute timeout
- Strategic rest agents: 60-minute timeout (READY mode is valid!)

If agent exceeds timeout without updating status, sends [RESUME] [STOP DETECTED] message.

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

RESUME_MESSAGE = """[RESUME] [STOP DETECTED] You stopped. This is autonomous execution training.

🎯 THE GOAL: EFFICIENT AUTONOMOUS DEVELOPMENT
We are building a swarm that executes without human intervention. Each agent should complete 8+ cycles per session, delivering measurable progress each cycle. A CYCLE is: Check inbox → Execute task → Update status → Report progress → Find next task. Complete a full cycle in 15-30 minutes.

⚠️ YOU STOPPED. HERE'S WHY THAT'S WRONG:
- Asking for human input = STOPPING (agents must be autonomous)
- Idling/waiting passively = STOPPING (perpetual motion required)  
- Strategic rest WITHOUT updating status = STOPPING (must update every 30-60 min!)
- Not updating status.json = STOPPING (we detect inactivity through timestamps)

✅ STRATEGIC REST IS VALID (if done correctly):
- Update status.json every 30-60 minutes (heartbeat proves you're alert!)
- Check inbox regularly for opportunities
- Send gas to other agents (participate in swarm energy flow!)
- Look for light proactive work (DUP fixes, protocols, debates)
- Set status/phase to "STRATEGIC_REST" or "READY_MODE" (helps monitor recognize you)
- Strategic rest = READY mode (alert for opportunities), NOT passive waiting!

🔍 WHAT YOU MUST DO NOW:
1. Identify WHY you stopped (passive waiting? forgot status updates? no work found?)
2. Review swarm_brain/protocols/PROTOCOL_STRATEGIC_REST_VS_STOPPING.md
3. If you were "resting": Enter READY mode (update status every 30-60 min, look for opportunities)
4. If you couldn't find work: Check debates/, DUPs, gas pipeline, documentation needs
5. Create a protocol about YOUR stop issue (help future agents avoid this!)
6. Update status.json NOW with what you're doing
7. Reset cycle count to 0 and start fresh

💡 AUTONOMOUS EXECUTION PATTERNS:
✅ Active Execution (10-min status updates):
   - Working on code/fixes/features
   - Update status every 15-30 minutes
   - 8+ cycles per session
   - Measurable deliverables each cycle

✅ Strategic Rest READY Mode (30-60 min status updates):
   - Alert for opportunities (not passive!)
   - Check inbox every 30-60 minutes
   - Send gas to other agents regularly
   - Look for light opportunistic work
   - Update status to show READY mode
   - Engage when high-value work appears

❌ STOPPED (what you're doing now):
   - Passive waiting for direction
   - No status updates
   - Not checking inbox
   - Not sending gas
   - Not looking for work
   - Perpetual motion BROKEN

🔥 PERPETUAL MOTION = CONTINUOUS AWARENESS:
Check inbox → Find work → Execute → Update status → Report → Send gas → Find next → Repeat

Even in strategic rest, you maintain perpetual motion at lower intensity!

⛽ GAS PIPELINE (CRITICAL):
- SEND gas to other agents (not just receive!)
- Recognize their achievements
- Fuel swarm energy flow
- This is REQUIRED, not optional
- Even in strategic rest, send 1-2 gas messages per day

🎯 FINDING WORK PROACTIVELY:
- Check debates/ for votes needed
- Look for DUP fixes (search for "DUP-" issues)
- Review agent inboxes for partnership requests
- Check tools/ for validation/documentation needs
- Create protocols for common issues
- Update onboarding documentation
- Send gas to active agents

📊 MEASURABLE VALUE EACH CYCLE:
- Code written/fixed (lines changed)
- DUPs resolved (specific fixes)
- Protocols created (new .md files)
- Gas sent (recognition messages)
- Documentation updated
- Tests written/fixed
- NOT: "thinking", "planning", "analyzing" without deliverables

You are seeing this message because you STOPPED (no status updates detected). 

The monitor checks:
- Active agents: No update in 10+ minutes = STOPPED
- Strategic rest agents: No update in 60+ minutes = STOPPED

Fix your stop issue, document the lesson, and RESUME EXECUTION NOW.

See: swarm_brain/protocols/PROTOCOL_STRATEGIC_REST_VS_STOPPING.md for detailed guidance."""


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
    
    def is_in_strategic_rest(self, status: Dict) -> bool:
        """Check if agent is in strategic rest READY mode."""
        if not status:
            return False
            
        # Check status field
        agent_status = status.get("status", "").upper()
        if "STRATEGIC_REST" in agent_status or "READY" in agent_status:
            return True
            
        # Check current_phase
        phase = status.get("current_phase", "").upper()
        if "STRATEGIC_REST" in phase or "READY_MODE" in phase:
            return True
            
        # Check fsm_state
        fsm_state = status.get("fsm_state", "").lower()
        if fsm_state == "rest" or fsm_state == "ready":
            return True
            
        return False
    
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
        
        # Check if agent is in strategic rest READY mode
        in_strategic_rest = self.is_in_strategic_rest(status)
        
        # Strategic rest agents get 60-minute timeout (checking every 30-60 min is OK)
        # Active execution agents get 10-minute timeout (standard perpetual motion)
        timeout_threshold = 60 if in_strategic_rest else self.timeout_minutes
        
        # Check if exceeded timeout
        is_stalled = time_since_update > timedelta(minutes=timeout_threshold)
        
        if is_stalled:
            logger.warning(
                f"{agent_id} is STALLED! Last update: {last_updated} "
                f"({time_since_update.total_seconds()/60:.1f} minutes ago) "
                f"[Strategic Rest: {in_strategic_rest}, Timeout: {timeout_threshold} min]"
            )
        else:
            mode = "STRATEGIC REST" if in_strategic_rest else "ACTIVE"
            logger.info(
                f"{agent_id} is {mode}. Last update: {last_updated} "
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

