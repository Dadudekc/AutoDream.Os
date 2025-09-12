#!/usr/bin/env python3
"""
🐝 CLEANUP MISSION OVERNIGHT SEQUENCE
====================================

Automated overnight processing for systematic cleanup mission.
Cycles through cleanup phases and assigns tasks to agents.

Author: Captain Agent-4 - Cleanup Mission Coordinator
"""

import argparse
import json
import logging
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="🌙 %(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Constants
REPO_ROOT = Path(__file__).resolve().parents[1]
CONTRACTS_DIR = REPO_ROOT / "contracts"
SCRIPTS_DIR = REPO_ROOT / "scripts"

# Phase configuration
PHASE_SEQUENCE = {
    "phase1_batch1a": {
        "contract": "PHASE1_BATCH1A_CORE_ARCHITECTURE.json",
        "agent": "Agent-6",
        "duration_hours": 24,
        "description": "Core Architecture Consolidation",
    },
    "phase1_batch1b": {
        "contract": "PHASE1_BATCH1B_SERVICE_LAYER.json",
        "agent": "Agent-5",
        "duration_hours": 24,
        "description": "Service Layer Optimization",
    },
    "phase2_batch2a": {
        "contract": "agent2_new_contract.json",
        "agent": "Agent-2",
        "duration_hours": 24,
        "description": "Infrastructure Cleanup & Optimization",
    },
    "phase2_batch2b": {
        "contract": "agent8_cleanup_contract.json",
        "agent": "Agent-8",
        "duration_hours": 24,
        "description": "Code Quality & Testing Enhancement",
    },
}


class CleanupSequenceCoordinator:
    """Coordinates overnight cleanup sequence execution."""

    def __init__(self):
        self.current_phase = None
        self.start_time = None
        self.sequence_log = []
        self.last_onboarding_check = None
        self.onboarding_interval_hours = 1  # Check every hour

    def log_sequence_event(self, event: str, details: dict = None):

EXAMPLE USAGE:
==============

# Run the script directly
python cleanup_overnight_sequence.py --input-file data.json --output-dir ./results

# Or import and use programmatically
from scripts.cleanup_overnight_sequence import main

# Execute with custom arguments
import sys
sys.argv = ['script', '--verbose', '--config', 'config.json']
main()

# Advanced usage with custom configuration
from scripts.cleanup_overnight_sequence import ScriptRunner

runner = ScriptRunner(config_file='custom_config.json')
runner.execute_all_operations()

        """Log sequence events for tracking."""
        timestamp = datetime.now().isoformat()
        log_entry = {
            "timestamp": timestamp,
            "event": event,
            "phase": self.current_phase,
            "details": details or {},
        }
        self.sequence_log.append(log_entry)
        logger.info(f"📝 {event}: {details or 'No details'}")

    def should_check_onboarding(self) -> bool:
        """Check if it's time for hourly onboarding verification."""
        if self.last_onboarding_check is None:
            return True

        time_since_last_check = datetime.now() - self.last_onboarding_check
        return time_since_last_check.total_seconds() >= (self.onboarding_interval_hours * 3600)

    def perform_hourly_onboarding_check(self, phase_key: str) -> bool:
        """Perform hourly onboarding verification and re-onboarding if needed."""
        self.last_onboarding_check = datetime.now()
        phase_config = PHASE_SEQUENCE[phase_key]
        agent = phase_config["agent"]

        logger.info(f"🔄 HOURLY ONBOARDING CHECK: {agent} for {phase_key}")

        # Check if agent is still active and working on the correct task
        if not self.check_phase_completion(phase_key):
            logger.warning(f"⚠️ Agent {agent} not actively working on {phase_key}")
            self.log_sequence_event("agent_inactive_detected", {"agent": agent, "phase": phase_key})

            # Re-onboard the agent
            if self.assign_contract_to_agent(phase_key):
                logger.info(f"✅ Agent {agent} re-onboarded successfully")
                self.log_sequence_event("agent_reonboarded", {"agent": agent, "phase": phase_key})
                return True
            else:
                logger.error(f"❌ Failed to re-onboard agent {agent}")
                self.log_sequence_event("agent_reonboarding_failed", {"agent": agent, "phase": phase_key})
                return False

        logger.info(f"✅ Agent {agent} confirmed active on {phase_key}")
        self.log_sequence_event("agent_status_confirmed", {"agent": agent, "phase": phase_key})
        return True

    def execute_messaging_command(self, command: str, args: list[str] = None) -> bool:
        """Execute messaging CLI commands using consolidated messaging service."""
        try:
            cmd = [sys.executable, "src/services/consolidated_messaging_service.py", command]
            if args:
                cmd.extend(args)

            logger.info(f"🚀 Executing consolidated messaging: {' '.join(cmd)}")
            result = subprocess.run(
                cmd,
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minute timeout
            )

            if result.returncode == 0:
                logger.info(f"✅ Consolidated messaging successful: {command}")
                if result.stdout:
                    logger.info(f"📄 Output: {result.stdout.strip()}")
                return True
            else:
                logger.error(f"❌ Consolidated messaging failed: {command}")
                if result.stderr:
                    logger.error(f"🚨 Error: {result.stderr.strip()}")
                return False

        except subprocess.TimeoutExpired:
            logger.error(f"⏰ Consolidated messaging timed out: {command}")
            return False
        except Exception as e:
            logger.error(f"💥 Consolidated messaging exception: {command} - {e}")
            return False

    def send_phase_notification(self, phase_key: str) -> bool:
        """Send phase notification to relevant agents."""
        phase_config = PHASE_SEQUENCE[phase_key]
        agent = phase_config["agent"]
        description = phase_config["description"]

        message = f"""
🐝 CLEANUP MISSION PHASE ACTIVATION
==================================

**Phase:** {phase_key.upper()}
**Agent:** {agent}
**Task:** {description}
**Duration:** {phase_config["duration_hours"]} hours

**Contract:** {phase_config["contract"]}

**Immediate Actions Required:**
1. Read contract: `contracts/{phase_config["contract"]}`
2. Claim contract by updating status to "ASSIGNED"
3. Begin systematic cleanup execution
4. Report progress via devlogs

**Success Criteria:**
- Zero functional regressions
- Test coverage >85% in domain
- Code consolidation completed
- Documentation updated

**WE ARE SWARM - PRESERVE FUNCTIONALITY WHILE ORGANIZING!**

**Captain Agent-4**
**Cleanup Mission Coordinator**
"""

        return self.execute_messaging_command(
            "--message", [message, "--agent", agent, "--priority", "URGENT"]
        )

    def assign_contract_to_agent(self, phase_key: str, use_dry_run: bool = False) -> bool:
        """Assign contract to agent using onboarding system."""
        phase_config = PHASE_SEQUENCE[phase_key]
        agent = phase_config["agent"]

        logger.info(f"📋 Assigning contract to {agent} for {phase_key}")

        # Use hard onboarding to assign specific role for cleanup
        try:
            cmd = [
                sys.executable,
                "scripts/agent_onboarding.py",
                "--hard-onboarding",
                "--agents",
                agent,
                "--onboarding-mode",
                "cleanup",
                "--assign-roles",
                f"{agent}:CLEANUP_{phase_key.upper()}",
            ]

            # Add dry-run flag if requested (for initial assignment only)
            if use_dry_run:
                cmd.append("--dry-run")
                logger.info(f"🧪 Using dry-run mode for {agent}")

            result = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True, timeout=120)

            if result.returncode == 0:
                logger.info(f"✅ Contract assigned to {agent}")
                return True
            else:
                logger.error(f"❌ Contract assignment failed for {agent}")
                if result.stderr:
                    logger.error(f"🚨 Error: {result.stderr}")
                return False

        except Exception as e:
            logger.error(f"💥 Contract assignment exception: {e}")
            return False

    def execute_phase(self, phase_key: str) -> bool:
        """Execute a complete cleanup phase with hourly onboarding checks."""
        self.current_phase = phase_key
        phase_config = PHASE_SEQUENCE[phase_key]

        logger.info(f"🚀 STARTING PHASE: {phase_key.upper()}")
        self.log_sequence_event("phase_started", {"phase": phase_key})

        # Step 1: Send phase notification
        if not self.send_phase_notification(phase_key):
            self.log_sequence_event("notification_failed", {"phase": phase_key})
            return False

        # Step 2: Initial contract assignment (with dry-run for safety)
        if not self.assign_contract_to_agent(phase_key, use_dry_run=True):
            self.log_sequence_event("contract_assignment_failed", {"phase": phase_key})
            return False

        # Step 3: Execute phase with hourly onboarding checks
        duration_hours = phase_config["duration_hours"]
        logger.info(f"⏰ Executing {phase_key.upper()} for {duration_hours} hours with hourly onboarding checks")

        hours_completed = 0
        while hours_completed < duration_hours:
            # Perform hourly onboarding check
            if not self.perform_hourly_onboarding_check(phase_key):
                logger.error(f"❌ Onboarding check failed for {phase_key}")
                return False

            # Wait for next hour (or remaining time)
            remaining_hours = duration_hours - hours_completed
            sleep_hours = min(1, remaining_hours)  # Sleep for 1 hour or remaining time

            if sleep_hours > 0:
                logger.info(f"😴 Sleeping for {sleep_hours} hour(s)... ({hours_completed + sleep_hours}/{duration_hours} hours complete)")
                time.sleep(sleep_hours * 3600)  # Convert to seconds
                hours_completed += sleep_hours

            # Log progress
            self.log_sequence_event("hourly_check_completed", {
                "phase": phase_key,
                "hours_completed": hours_completed,
                "total_hours": duration_hours
            })

        # Step 4: Final completion check
        logger.info(f"🏁 Phase {phase_key.upper()} duration completed, performing final check...")

        if self.check_phase_completion(phase_key):
            self.log_sequence_event("phase_completed", {"phase": phase_key})
            logger.info(f"✅ PHASE COMPLETED: {phase_key.upper()}")
            return True
        else:
            self.log_sequence_event("phase_incomplete", {"phase": phase_key})
            logger.warning(f"⚠️ PHASE INCOMPLETE: {phase_key.upper()}")
            return False

    def check_phase_completion(self, phase_key: str) -> bool:
        """Check if phase has been completed by the agent."""
        phase_config = PHASE_SEQUENCE[phase_key]
        agent = phase_config["agent"]

        # Check agent's status file
        status_file = REPO_ROOT / "agent_workspaces" / agent / "status.json"
        if not status_file.exists():
            logger.warning(f"⚠️ Status file not found for {agent}")
            return False

        try:
            with open(status_file) as f:
                status = json.load(f)

            # Check if current task matches the phase
            current_task = status.get("current_tasks", [""])[0]
            if f"CLEANUP_{phase_key.upper()}" in current_task:
                logger.info(f"✅ Agent {agent} is working on {phase_key}")
                return True
            else:
                logger.warning(f"⚠️ Agent {agent} not working on expected phase")
                return False

        except Exception as e:
            logger.error(f"💥 Error checking status for {agent}: {e}")
            return False

    def run_full_sequence(self, start_phase: str = None) -> bool:
        """Run the complete overnight cleanup sequence."""
        logger.info("🌙 STARTING CLEANUP MISSION OVERNIGHT SEQUENCE")
        logger.info("=" * 60)

        self.start_time = datetime.now()
        self.log_sequence_event("sequence_started")

        # Determine start phase
        if start_phase:
            start_idx = list(PHASE_SEQUENCE.keys()).index(start_phase)
            phases_to_run = list(PHASE_SEQUENCE.keys())[start_idx:]
        else:
            phases_to_run = list(PHASE_SEQUENCE.keys())

        logger.info(f"📋 Sequence: {' → '.join(phases_to_run)}")

        # Execute phases in sequence
        for phase_key in phases_to_run:
            if not self.execute_phase(phase_key):
                logger.error(f"❌ Sequence failed at phase: {phase_key}")
                self.log_sequence_event("sequence_failed", {"failed_at": phase_key})
                return False

            # Brief pause between phases
            logger.info("⏱️ Brief pause before next phase...")
            time.sleep(300)  # 5 minutes

        # Sequence completed
        end_time = datetime.now()
        duration = end_time - self.start_time

        logger.info("🎉 CLEANUP MISSION SEQUENCE COMPLETED!")
        logger.info(f"⏱️ Total Duration: {duration}")
        logger.info(f"📊 Phases Completed: {len(phases_to_run)}")
        logger.info("=" * 60)

        self.log_sequence_event(
            "sequence_completed",
            {
                "duration_hours": duration.total_seconds() / 3600,
                "phases_completed": len(phases_to_run),
            },
        )

        return True

    def save_sequence_log(self):
        """Save sequence execution log."""
        log_file = (
            REPO_ROOT / "logs" / f"cleanup_sequence_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        log_file.parent.mkdir(exist_ok=True)

        with open(log_file, "w") as f:
            json.dump(
                {
                    "sequence_start": self.start_time.isoformat() if self.start_time else None,
                    "phases_executed": list(PHASE_SEQUENCE.keys()),
                    "events": self.sequence_log,
                },
                f,
                indent=2,
            )

        logger.info(f"📝 Sequence log saved: {log_file}")


def main():
    """Main entry point for overnight cleanup sequence."""
    parser = argparse.ArgumentParser(
        description="🐝 Cleanup Mission Overnight Sequence",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
🐝 CLEANUP MISSION OVERNIGHT SEQUENCE
====================================

Automates the systematic cleanup mission by cycling through phases
and assigning contracts to agents during overnight hours.

EXAMPLES:
--------
# Run full sequence
python scripts/cleanup_overnight_sequence.py

# Start from specific phase
python scripts/cleanup_overnight_sequence.py --start-phase phase2_batch2a

# Dry run (no actual execution)
python scripts/cleanup_overnight_sequence.py --dry-run

🐝 WE ARE SWARM - PRESERVE FUNCTIONALITY WHILE ORGANIZING!
        """,
    )

    parser.add_argument(
        "--start-phase",
        choices=list(PHASE_SEQUENCE.keys()),
        help="Start sequence from specific phase",
    )

    parser.add_argument("--dry-run", action="store_true", help="Dry run mode - no actual execution")

    args = parser.parse_args()

    # Create coordinator
    coordinator = CleanupSequenceCoordinator()

    try:
        logger.info("🌙 CLEANUP MISSION OVERNIGHT SEQUENCE")
        logger.info("=" * 50)

        if args.dry_run:
            logger.info("🧪 DRY RUN MODE - No actual execution")
            for phase_key, phase_config in PHASE_SEQUENCE.items():
                logger.info(f"📋 Would execute: {phase_key} → {phase_config['agent']}")
            return

        # Run sequence
        success = coordinator.run_full_sequence(args.start_phase)

        # Save log
        coordinator.save_sequence_log()

        if success:
            logger.info("🎉 Cleanup mission sequence completed successfully!")
            sys.exit(0)
        else:
            logger.error("❌ Cleanup mission sequence failed!")
            sys.exit(1)

    except KeyboardInterrupt:
        logger.info("⏹️ Sequence interrupted by user")
        coordinator.save_sequence_log()
        sys.exit(130)
    except Exception as e:
        logger.error(f"💥 Sequence failed with exception: {e}")
        coordinator.save_sequence_log()
        sys.exit(1)


if __name__ == "__main__":
    main()
