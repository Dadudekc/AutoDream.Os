from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
import json
import logging
import threading

            from captain_coordinator_v2 import CaptainCoordinatorV2
            import sys
    import argparse
from dataclasses import dataclass, asdict
from src.utils.stability_improvements import stability_manager, safe_import
import time

#!/usr/bin/env python3
"""
Agent Stall Prevention Service - Agent Cellphone V2
==================================================

Prevents Code Black emergencies by implementing a 5-minute timer system
that automatically checks captain status and restarts agents if needed.
"""



# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s"
)
log = logging.getLogger("agent_stall_prevention_service")


@dataclass
class CaptainStatus:
    """Captain status tracking"""

    captain_id: str
    last_activity: str
    last_response: str
    status: str  # "active", "stalled", "unresponsive"
    response_time: float  # seconds to respond


@dataclass
class AgentStallEvent:
    """Agent stall event record"""

    event_id: str
    timestamp: str
    captain_id: str
    stall_duration: float
    response_time: float
    action_taken: str
    status: str


class AgentStallPreventionService:
    """Service to prevent agent stalls using 5-minute timer system"""

    def __init__(self):
        self.project_root = Path(__file__).resolve().parents[3]
        self.config_file = self.project_root / "config" / "stall_prevention_config.json"
        self.log_file = self.project_root / "logs" / "stall_prevention_log.json"
        self.captain_status_file = (
            self.project_root / "persistent_data" / "captain_status.json"
        )

        # Ensure directories exist
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        self.captain_status_file.parent.mkdir(parents=True, exist_ok=True)

        # Load configuration
        self.config = self._load_config()

        # Initialize captain status
        self.captain_status = self._load_captain_status()

        # Timer settings
        self.check_interval = self.config.get("check_interval_minutes", 5)  # 5 minutes
        self.response_timeout = self.config.get(
            "response_timeout_minutes", 2
        )  # 2 minutes
        self.max_stall_duration = self.config.get(
            "max_stall_duration_minutes", 10
        )  # 10 minutes

        # Service state
        self.is_running = False
        self.monitoring_thread = None
        self.last_check_time = None

        log.info("Agent Stall Prevention Service initialized")
        log.info(f"Check interval: {self.check_interval} minutes")
        log.info(f"Response timeout: {self.response_timeout} minutes")
        log.info(f"Max stall duration: {self.max_stall_duration} minutes")

    def _load_config(self) -> Dict[str, Any]:
        """Load stall prevention configuration"""
        default_config = {
            "check_interval_minutes": 5,
            "response_timeout_minutes": 2,
            "max_stall_duration_minutes": 10,
            "auto_restart_enabled": True,
            "captain_notification_enabled": True,
            "log_stall_events": True,
        }

        try:
            if self.config_file.exists():
                with open(self.config_file, "r") as f:
                    config = json.load(f)
                    # Merge with defaults
                    for key, value in default_config.items():
                        if key not in config:
                            config[key] = value
                    return config
            else:
                # Create default config
                with open(self.config_file, "w") as f:
                    json.dump(default_config, f, indent=2)
                return default_config
        except Exception as e:
            log.error(f"Error loading config: {e}")
            return default_config

    def _load_captain_status(self) -> CaptainStatus:
        """Load current captain status"""
        try:
            if self.captain_status_file.exists():
                with open(self.captain_status_file, "r") as f:
                    data = json.load(f)
                    return CaptainStatus(**data)
            else:
                # Initialize default captain status
                status = CaptainStatus(
                    captain_id="Captain-5",
                    last_activity=datetime.now().isoformat(),
                    last_response=datetime.now().isoformat(),
                    status="active",
                    response_time=0.0,
                )
                self._save_captain_status(status)
                return status
        except Exception as e:
            log.error(f"Error loading captain status: {e}")
            return CaptainStatus(
                captain_id="Captain-5",
                last_activity=datetime.now().isoformat(),
                last_response=datetime.now().isoformat(),
                status="active",
                response_time=0.0,
            )

    def _save_captain_status(self, status: CaptainStatus):
        """Save captain status to file"""
        try:
            with open(self.captain_status_file, "w") as f:
                json.dump(asdict(status), f, indent=2)
        except Exception as e:
            log.error(f"Error saving captain status: {e}")

    def start_monitoring(self):
        """Start the 5-minute timer monitoring system"""
        if self.is_running:
            log.warning("Monitoring already running")
            return

        self.is_running = True
        self.monitoring_thread = threading.Thread(
            target=self._monitoring_loop, daemon=True
        )
        self.monitoring_thread.start()

        log.info("Agent stall prevention monitoring started")
        log.info(f"Checking captain status every {self.check_interval} minutes")

    def stop_monitoring(self):
        """Stop the monitoring system"""
        self.is_running = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5.0)

        log.info("Agent stall prevention monitoring stopped")

    def _monitoring_loop(self):
        """Main monitoring loop with 5-minute timer"""
        while self.is_running:
            try:
                # Check captain status
                self._check_captain_status()

                # Wait for next check interval
                time.sleep(self.check_interval * 60)  # Convert minutes to seconds

            except Exception as e:
                log.error(f"Error in monitoring loop: {e}")
                time.sleep(60)  # Wait 1 minute before retrying

    def _check_captain_status(self):
        """Check if captain is responsive and agents are working"""
        try:
            current_time = datetime.now()
            self.last_check_time = current_time

            log.info("🔍 Performing scheduled captain status check...")

            # Check if captain has been active recently
            last_activity = datetime.fromisoformat(self.captain_status.last_activity)
            time_since_activity = (
                current_time - last_activity
            ).total_seconds() / 60  # minutes

            if time_since_activity > self.max_stall_duration:
                log.warning(
                    f"⚠️ Captain inactive for {time_since_activity:.1f} minutes - potential stall detected"
                )
                self._handle_captain_stall()
            else:
                log.info(
                    f"✅ Captain active {time_since_activity:.1f} minutes ago - status normal"
                )

                # Send status check to captain
                if self.config.get("captain_notification_enabled", True):
                    self._send_captain_status_check()

        except Exception as e:
            log.error(f"Error checking captain status: {e}")

    def _send_captain_status_check(self):
        """Send status check message to current captain"""
        try:
            captain_id = self.captain_status.captain_id

            # Import captain coordinator for messaging

            sys.path.append(str(self.project_root / "src" / "services"))


            coordinator = CaptainCoordinatorV2()

            status_message = f"""🔍 CAPTAIN STATUS CHECK - {datetime.now().strftime('%H:%M:%S')}

This is an automated status check from the Agent Stall Prevention Service.

Current Status:
- Captain: {captain_id}
- Last Activity: {self.captain_status.last_activity}
- System Status: Normal

Please respond to confirm you are active and monitoring agents.

If no response within {self.response_timeout} minutes, the system will assume a stall and initiate recovery procedures.

CAPTAIN-5 - Please acknowledge this status check."""

            # Send HIGH PRIORITY status check
            success = coordinator.send_message_to_agent(
                captain_id, status_message, high_priority=True
            )

            if success:
                log.info(f"✅ Status check sent to {captain_id}")
                # Start response timer
                self._start_response_timer()
            else:
                log.error(f"❌ Failed to send status check to {captain_id}")

        except Exception as e:
            log.error(f"Error sending captain status check: {e}")

    def _start_response_timer(self):
        """Start timer for captain response"""

        def response_timer():
            time.sleep(self.response_timeout * 60)  # Wait for response timeout

            # Check if captain responded
            if not self._captain_responded():
                log.warning(
                    f"⚠️ Captain did not respond within {self.response_timeout} minutes"
                )
                self._handle_captain_stall()

        # Start response timer in background
        timer_thread = threading.Thread(target=response_timer, daemon=True)
        timer_thread.start()

    def _captain_responded(self) -> bool:
        """Check if captain has responded to status check"""
        try:
            # Check if captain has been active since status check
            current_time = datetime.now()
            last_activity = datetime.fromisoformat(self.captain_status.last_activity)

            # If captain was active in the last 2 minutes, consider it a response
            time_since_activity = (current_time - last_activity).total_seconds() / 60
            return time_since_activity < self.response_timeout

        except Exception as e:
            log.error(f"Error checking captain response: {e}")
            return False

    def _handle_captain_stall(self):
        """Handle captain stall by initiating recovery procedures"""
        try:
            log.warning("🚨 CAPTAIN STALL DETECTED - Initiating recovery procedures")

            # Record stall event
            stall_event = AgentStallEvent(
                event_id=f"STALL-{int(time.time())}",
                timestamp=datetime.now().isoformat(),
                captain_id=self.captain_status.captain_id,
                stall_duration=self.max_stall_duration,
                response_time=self.response_timeout,
                action_taken="Automatic recovery initiation",
                status="recovery_initiated",
            )

            self._log_stall_event(stall_event)

            # Update captain status
            self.captain_status.status = "stalled"
            self.captain_status.last_response = datetime.now().isoformat()
            self._save_captain_status(self.captain_status)

            # Initiate automatic recovery if enabled
            if self.config.get("auto_restart_enabled", True):
                self._initiate_automatic_recovery()

        except Exception as e:
            log.error(f"Error handling captain stall: {e}")

    def _initiate_automatic_recovery(self):
        """Initiate automatic agent recovery procedures"""
        try:
            log.info("🚀 Initiating automatic agent recovery procedures")

            # Import captain coordinator for recovery messaging

            sys.path.append(str(self.project_root / "src" / "services"))


            coordinator = CaptainCoordinatorV2()

            recovery_message = f"""🚨 AUTOMATIC RECOVERY INITIATED - {datetime.now().strftime('%H:%M:%S')}

AGENT STALL PREVENTION SERVICE:
Captain stall detected - automatic recovery initiated.

IMMEDIATE ACTION REQUIRED:
1. All agents must acknowledge this recovery message
2. Resume current contract work IMMEDIATELY
3. Report current status and progress
4. Confirm back online and working

This is an AUTOMATIC recovery message from the stall prevention system.

CAPTAIN-5 - Please take control and resume normal operations.

AUTOMATIC RECOVERY SYSTEM - EMERGENCY MODE"""

            # Send HIGH PRIORITY recovery message to all agents
            results = coordinator.send_message_to_all_agents(
                recovery_message, high_priority=True
            )

            success_count = sum(results.values())
            log.info(
                f"✅ Automatic recovery messages sent: {success_count}/{len(results)} successful"
            )

        except Exception as e:
            log.error(f"Error initiating automatic recovery: {e}")

    def _log_stall_event(self, event: AgentStallEvent):
        """Log stall event to file"""
        try:
            events = []
            if self.log_file.exists():
                with open(self.log_file, "r") as f:
                    data = json.load(f)
                    events = data.get("stall_events", [])

            events.append(asdict(event))

            with open(self.log_file, "w") as f:
                json.dump({"stall_events": events}, f, indent=2)

            log.info(f"📝 Stall event logged: {event.event_id}")

        except Exception as e:
            log.error(f"Error logging stall event: {e}")

    def update_captain_activity(self):
        """Update captain activity timestamp (called when captain performs actions)"""
        try:
            current_time = datetime.now()
            self.captain_status.last_activity = current_time.isoformat()
            self.captain_status.status = "active"
            self._save_captain_status(self.captain_status)

            log.info("✅ Captain activity updated")

        except Exception as e:
            log.error(f"Error updating captain activity: {e}")

    def get_service_status(self) -> Dict[str, Any]:
        """Get current service status"""
        return {
            "timestamp": datetime.now().isoformat(),
            "is_running": self.is_running,
            "check_interval_minutes": self.check_interval,
            "response_timeout_minutes": self.response_timeout,
            "max_stall_duration_minutes": self.max_stall_duration,
            "last_check_time": self.last_check_time.isoformat()
            if self.last_check_time
            else None,
            "captain_status": asdict(self.captain_status),
            "config": self.config,
        }


def main():
    """CLI interface for Agent Stall Prevention Service"""

    parser = argparse.ArgumentParser(description="Agent Stall Prevention Service")
    parser.add_argument("--start", action="store_true", help="Start monitoring service")
    parser.add_argument("--stop", action="store_true", help="Stop monitoring service")
    parser.add_argument("--status", action="store_true", help="Show service status")
    parser.add_argument("--test", action="store_true", help="Test status check")
    parser.add_argument("--config", action="store_true", help="Show configuration")

    args = parser.parse_args()

    service = AgentStallPreventionService()

    if args.start:
        service.start_monitoring()
        print("✅ Agent stall prevention monitoring started")
        print("Press Ctrl+C to stop")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            service.stop_monitoring()
            print("\n🛑 Monitoring stopped")

    elif args.stop:
        service.stop_monitoring()
        print("✅ Agent stall prevention monitoring stopped")

    elif args.status:
        status = service.get_service_status()
        print(json.dumps(status, indent=2, default=str))

    elif args.test:
        print("🧪 Testing captain status check...")
        service._send_captain_status_check()
        print("✅ Test status check sent")

    elif args.config:
        print("⚙️ Service Configuration:")
        print(json.dumps(service.config, indent=2))

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
