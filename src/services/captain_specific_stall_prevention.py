#!/usr/bin/env python3
"""
Captain-Specific Stall Prevention Service - Agent Cellphone V2
============================================================

Prevents Captain-5 from going dark for 5+ minutes by monitoring cursor responses
and sending captaincy duty prompts. Uses cursor response detection to monitor
all 5 agent instances simultaneously.
"""

import json
import time
import logging
import threading
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
log = logging.getLogger("captain_stall_prevention")

@dataclass
class CaptainDutyPrompt:
    """Captain duty prompt configuration"""
    prompt_id: str
    message: str
    frequency_minutes: int
    last_sent: str
    priority: str  # "normal", "urgent", "critical"

@dataclass
class CursorResponseData:
    """Cursor response monitoring data"""
    agent_id: str
    last_response: str
    response_count: int
    status: str  # "active", "responding", "stalled"
    last_activity: str

class CaptainSpecificStallPrevention:
    """Service to prevent Captain-5 from going dark using cursor response detection"""
    
    def __init__(self):
        self.project_root = Path(__file__).resolve().parents[3]
        self.config_file = self.project_root / "config" / "captain_stall_prevention_config.json"
        self.cursor_db_file = self.project_root / "runtime" / "agent_comms" / "cursor_response_db.json"
        self.captain_status_file = self.project_root / "persistent_data" / "captain_5_status.json"
        
        # Ensure directories exist
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        self.captain_status_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Load configuration
        self.config = self._load_config()
        
        # Initialize captain status
        self.captain_status = self._load_captain_status()
        
        # Timer settings
        self.captain_check_interval = self.config.get("captain_check_interval_minutes", 5)  # 5 minutes
        self.cursor_monitor_interval = self.config.get("cursor_monitor_interval_seconds", 30)  # 30 seconds
        self.max_captain_dark_time = self.config.get("max_captain_dark_minutes", 5)  # 5 minutes
        
        # Service state
        self.is_running = False
        self.captain_monitoring_thread = None
        self.cursor_monitoring_thread = None
        self.last_captain_check = None
        self.last_cursor_check = None
        
        # Captain duty prompts
        self.duty_prompts = self._initialize_duty_prompts()
        
        log.info("Captain-Specific Stall Prevention Service initialized")
        log.info(f"Captain check interval: {self.captain_check_interval} minutes")
        log.info(f"Cursor monitor interval: {self.cursor_monitor_interval} seconds")
        log.info(f"Max captain dark time: {self.max_captain_dark_time} minutes")
    
    def _load_config(self) -> Dict[str, Any]:
        """Load captain stall prevention configuration"""
        default_config = {
            "captain_check_interval_minutes": 5,
            "cursor_monitor_interval_seconds": 30,
            "max_captain_dark_minutes": 5,
            "captain_duty_prompts_enabled": True,
            "cursor_response_monitoring": True,
            "auto_agent_activation": True,
            "log_captain_activity": True
        }
        
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    # Merge with defaults
                    for key, value in default_config.items():
                        if key not in config:
                            config[key] = value
                    return config
            else:
                # Create default config
                with open(self.config_file, 'w') as f:
                    json.dump(default_config, f, indent=2)
                return default_config
        except Exception as e:
            log.error(f"Error loading config: {e}")
            return default_config
    
    def _load_captain_status(self) -> Dict[str, Any]:
        """Load Captain-5 status"""
        try:
            if self.captain_status_file.exists():
                with open(self.captain_status_file, 'r') as f:
                    return json.load(f)
            else:
                # Initialize default captain status
                status = {
                    "captain_id": "Captain-5",
                    "last_activity": datetime.now().isoformat(),
                    "last_duty_prompt": datetime.now().isoformat(),
                    "status": "active",
                    "dark_time_minutes": 0,
                    "duty_prompts_sent": 0,
                    "agents_activated": 0
                }
                self._save_captain_status(status)
                return status
        except Exception as e:
            log.error(f"Error loading captain status: {e}")
            return {
                "captain_id": "Captain-5",
                "last_activity": datetime.now().isoformat(),
                "last_duty_prompt": datetime.now().isoformat(),
                "status": "active",
                "dark_time_minutes": 0,
                "duty_prompts_sent": 0,
                "agents_activated": 0
            }
    
    def _save_captain_status(self, status: Dict[str, Any]):
        """Save captain status to file"""
        try:
            with open(self.captain_status_file, 'w') as f:
                json.dump(status, f, indent=2)
        except Exception as e:
            log.error(f"Error saving captain status: {e}")
    
    def _initialize_duty_prompts(self) -> List[CaptainDutyPrompt]:
        """Initialize captain duty prompts"""
        prompts = [
            CaptainDutyPrompt(
                prompt_id="DUTY-001",
                message="🎖️ CAPTAIN-5 DUTY REMINDER - You are the active Captain!\n\nYour responsibilities:\n1. Monitor agent progress\n2. Assign new contracts\n3. Coordinate team efforts\n4. Lead toward 50-contract goal\n\nPlease acknowledge and continue leading!",
                frequency_minutes=5,
                last_sent=datetime.now().isoformat(),
                priority="normal"
            ),
            CaptainDutyPrompt(
                prompt_id="DUTY-002",
                message="🚨 CAPTAIN-5 URGENT DUTY REMINDER - You have been inactive!\n\nIMMEDIATE ACTION REQUIRED:\n1. Check agent status\n2. Assign pending contracts\n3. Coordinate team efforts\n4. Resume leadership duties\n\nCAPTAIN-5 - Please respond NOW!",
                frequency_minutes=3,
                last_sent=datetime.now().isoformat(),
                priority="urgent"
            ),
            CaptainDutyPrompt(
                prompt_id="DUTY-003",
                message="🚨🚨 CAPTAIN-5 CRITICAL DUTY REMINDER - You are going DARK!\n\nCRITICAL ACTION REQUIRED:\n1. IMMEDIATELY check all agents\n2. Assign ALL pending contracts\n3. Activate stalled agents\n4. Resume captaincy NOW\n\nCAPTAIN-5 - EMERGENCY RESPONSE REQUIRED!",
                frequency_minutes=1,
                last_sent=datetime.now().isoformat(),
                priority="critical"
            )
        ]
        return prompts
    
    def start_monitoring(self):
        """Start captain-specific monitoring"""
        if self.is_running:
            log.warning("Captain monitoring already running")
            return
        
        self.is_running = True
        
        # Start captain monitoring thread
        self.captain_monitoring_thread = threading.Thread(target=self._captain_monitoring_loop, daemon=True)
        self.captain_monitoring_thread.start()
        
        # Start cursor monitoring thread
        self.cursor_monitoring_thread = threading.Thread(target=self._cursor_monitoring_loop, daemon=True)
        self.cursor_monitoring_thread.start()
        
        log.info("Captain-specific stall prevention monitoring started")
        log.info(f"Checking Captain-5 every {self.captain_check_interval} minutes")
        log.info(f"Monitoring cursor responses every {self.cursor_monitor_interval} seconds")
    
    def stop_monitoring(self):
        """Stop the monitoring system"""
        self.is_running = False
        if self.captain_monitoring_thread:
            self.captain_monitoring_thread.join(timeout=5.0)
        if self.cursor_monitoring_thread:
            self.cursor_monitoring_thread.join(timeout=5.0)
        
        log.info("Captain-specific stall prevention monitoring stopped")
    
    def _captain_monitoring_loop(self):
        """Main captain monitoring loop with 5-minute timer"""
        while self.is_running:
            try:
                # Check captain status
                self._check_captain_status()
                
                # Wait for next check interval
                time.sleep(self.captain_check_interval * 60)  # Convert minutes to seconds
                
            except Exception as e:
                log.error(f"Error in captain monitoring loop: {e}")
                time.sleep(60)  # Wait 1 minute before retrying
    
    def _cursor_monitoring_loop(self):
        """Cursor response monitoring loop"""
        while self.is_running:
            try:
                # Monitor cursor responses
                self._check_cursor_responses()
                
                # Wait for next check interval
                time.sleep(self.cursor_monitor_interval)
                
            except Exception as e:
                log.error(f"Error in cursor monitoring loop: {e}")
                time.sleep(30)  # Wait 30 seconds before retrying
    
    def _check_captain_status(self):
        """Check if Captain-5 is active and performing duties"""
        try:
            current_time = datetime.now()
            self.last_captain_check = current_time
            
            log.info("🔍 Performing scheduled Captain-5 status check...")
            
            # Check if captain has been active recently
            last_activity = datetime.fromisoformat(self.captain_status["last_activity"])
            time_since_activity = (current_time - last_activity).total_seconds() / 60  # minutes
            
            # Update captain dark time
            self.captain_status["dark_time_minutes"] = time_since_activity
            
            if time_since_activity > self.max_captain_dark_time:
                log.warning(f"⚠️ Captain-5 dark for {time_since_activity:.1f} minutes - sending duty prompt")
                self._send_captain_duty_prompt(priority="critical")
                self._activate_all_agents()
            elif time_since_activity > self.max_captain_dark_time * 0.6:  # 60% of max time
                log.info(f"⚠️ Captain-5 inactive for {time_since_activity:.1f} minutes - sending duty prompt")
                self._send_captain_duty_prompt(priority="urgent")
            else:
                log.info(f"✅ Captain-5 active {time_since_activity:.1f} minutes ago - status normal")
                # Send normal duty prompt if due
                self._check_duty_prompt_schedule()
            
            # Save updated status
            self._save_captain_status(self.captain_status)
            
        except Exception as e:
            log.error(f"Error checking captain status: {e}")
    
    def _check_cursor_responses(self):
        """Check cursor responses for all 5 agent instances"""
        try:
            current_time = datetime.now()
            self.last_cursor_check = current_time
            
            # Load cursor response database
            cursor_data = self._load_cursor_response_db()
            
            if not cursor_data:
                log.warning("⚠️ No cursor response data found")
                return
            
            # Check each agent's cursor response
            for agent_id, agent_data in cursor_data.items():
                if agent_id == "Captain-5":
                    continue  # Skip captain in cursor monitoring
                
                last_response = datetime.fromisoformat(agent_data["last_response"])
                time_since_response = (current_time - last_response).total_seconds() / 60  # minutes
                
                # Update agent status based on cursor response
                if time_since_response > 10:  # 10 minutes without cursor activity
                    log.warning(f"⚠️ {agent_id} cursor inactive for {time_since_response:.1f} minutes")
                    agent_data["status"] = "stalled"
                elif time_since_response > 5:  # 5 minutes without cursor activity
                    log.info(f"⚠️ {agent_id} cursor slow for {time_since_response:.1f} minutes")
                    agent_data["status"] = "responding"
                else:
                    agent_data["status"] = "active"
                
                # Update last activity
                agent_data["last_activity"] = current_time.isoformat()
            
            # Save updated cursor data
            self._save_cursor_response_db(cursor_data)
            
        except Exception as e:
            log.error(f"Error checking cursor responses: {e}")
    
    def _load_cursor_response_db(self) -> Dict[str, Any]:
        """Load cursor response database"""
        try:
            if self.cursor_db_file.exists():
                with open(self.cursor_db_file, 'r') as f:
                    return json.load(f)
            else:
                # Initialize default cursor data
                default_data = {}
                for agent_id in ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Captain-5"]:
                    default_data[agent_id] = {
                        "last_response": datetime.now().isoformat(),
                        "response_count": 0,
                        "status": "active",
                        "last_activity": datetime.now().isoformat()
                    }
                
                # Save default data
                self._save_cursor_response_db(default_data)
                return default_data
        except Exception as e:
            log.error(f"Error loading cursor response db: {e}")
            return {}
    
    def _save_cursor_response_db(self, data: Dict[str, Any]):
        """Save cursor response database"""
        try:
            with open(self.cursor_db_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            log.error(f"Error saving cursor response db: {e}")
    
    def _check_duty_prompt_schedule(self):
        """Check if duty prompts are due to be sent"""
        try:
            current_time = datetime.now()
            
            for prompt in self.duty_prompts:
                last_sent = datetime.fromisoformat(prompt.last_sent)
                time_since_sent = (current_time - last_sent).total_seconds() / 60  # minutes
                
                if time_since_sent >= prompt.frequency_minutes:
                    log.info(f"📝 Sending scheduled duty prompt: {prompt.prompt_id}")
                    self._send_captain_duty_prompt(priority=prompt.priority)
                    prompt.last_sent = current_time.isoformat()
                    
        except Exception as e:
            log.error(f"Error checking duty prompt schedule: {e}")
    
    def _send_captain_duty_prompt(self, priority: str = "normal"):
        """Send captain duty prompt based on priority"""
        try:
            # Find appropriate prompt
            prompt = next((p for p in self.duty_prompts if p.priority == priority), None)
            if not prompt:
                log.error(f"❌ No prompt found for priority: {priority}")
                return
            
            # Import captain coordinator for messaging
            import sys
            sys.path.append(str(self.project_root / "src" / "services"))
            
            from captain_coordinator_v2 import CaptainCoordinatorV2
            
            coordinator = CaptainCoordinatorV2()
            
            # Send HIGH PRIORITY duty prompt to Captain-5
            success = coordinator.send_message_to_agent("Captain-5", prompt.message, high_priority=True)
            
            if success:
                log.info(f"✅ Duty prompt sent to Captain-5: {prompt.prompt_id}")
                
                # Update captain status
                self.captain_status["last_duty_prompt"] = datetime.now().isoformat()
                self.captain_status["duty_prompts_sent"] += 1
                self._save_captain_status(self.captain_status)
                
                # Update prompt timestamp
                prompt.last_sent = datetime.now().isoformat()
            else:
                log.error(f"❌ Failed to send duty prompt to Captain-5")
                
        except Exception as e:
            log.error(f"Error sending captain duty prompt: {e}")
    
    def _activate_all_agents(self):
        """Activate all agents when Captain-5 goes dark"""
        try:
            log.info("🚀 Activating all agents due to Captain-5 dark status")
            
            # Import captain coordinator for messaging
            import sys
            sys.path.append(str(self.project_root / "src" / "services"))
            
            from captain_coordinatorV2 import CaptainCoordinatorV2
            
            coordinator = CaptainCoordinatorV2()
            
            activation_message = f"""🚨 CAPTAIN-5 DARK STATUS DETECTED - AGENT ACTIVATION REQUIRED!

AGENT STALL PREVENTION SERVICE:
Captain-5 has been inactive for {self.captain_status['dark_time_minutes']:.1f} minutes.

IMMEDIATE ACTION REQUIRED:
1. All agents must acknowledge this activation message
2. Resume current contract work IMMEDIATELY
3. Report current status and progress
4. Confirm back online and working

CAPTAIN-5 - Please respond and resume captaincy duties!

AUTOMATIC AGENT ACTIVATION SYSTEM - EMERGENCY MODE"""
            
            # Send HIGH PRIORITY activation message to all agents
            results = coordinator.send_message_to_all_agents(activation_message, high_priority=True)
            
            success_count = sum(results.values())
            log.info(f"✅ Agent activation messages sent: {success_count}/{len(results)} successful")
            
            # Update captain status
            self.captain_status["agents_activated"] += 1
            self._save_captain_status(self.captain_status)
            
        except Exception as e:
            log.error(f"Error activating all agents: {e}")
    
    def update_captain_activity(self):
        """Update Captain-5 activity timestamp (called when captain performs actions)"""
        try:
            current_time = datetime.now()
            self.captain_status["last_activity"] = current_time.isoformat()
            self.captain_status["status"] = "active"
            self.captain_status["dark_time_minutes"] = 0
            self._save_captain_status(self.captain_status)
            
            log.info("✅ Captain-5 activity updated")
            
        except Exception as e:
            log.error(f"Error updating captain activity: {e}")
    
    def get_service_status(self) -> Dict[str, Any]:
        """Get current service status"""
        return {
            "timestamp": datetime.now().isoformat(),
            "is_running": self.is_running,
            "captain_check_interval_minutes": self.captain_check_interval,
            "cursor_monitor_interval_seconds": self.cursor_monitor_interval,
            "max_captain_dark_time_minutes": self.max_captain_dark_time,
            "last_captain_check": self.last_captain_check.isoformat() if self.last_captain_check else None,
            "last_cursor_check": self.last_cursor_check.isoformat() if self.last_cursor_check else None,
            "captain_status": self.captain_status,
            "duty_prompts": [asdict(p) for p in self.duty_prompts],
            "config": self.config
        }

def main():
    """CLI interface for Captain-Specific Stall Prevention Service"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Captain-Specific Stall Prevention Service")
    parser.add_argument("--start", action="store_true", help="Start monitoring service")
    parser.add_argument("--stop", action="store_true", help="Stop monitoring service")
    parser.add_argument("--status", action="store_true", help="Show service status")
    parser.add_argument("--test", action="store_true", help="Test duty prompt")
    parser.add_argument("--config", action="store_true", help="Show configuration")
    parser.add_argument("--activate-agents", action="store_true", help="Force activate all agents")
    
    args = parser.parse_args()
    
    service = CaptainSpecificStallPrevention()
    
    if args.start:
        service.start_monitoring()
        print("✅ Captain-specific stall prevention monitoring started")
        print("Press Ctrl+C to stop")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            service.stop_monitoring()
            print("\n🛑 Monitoring stopped")
    
    elif args.stop:
        service.stop_monitoring()
        print("✅ Captain-specific stall prevention monitoring stopped")
    
    elif args.status:
        status = service.get_service_status()
        print(json.dumps(status, indent=2, default=str))
    
    elif args.test:
        print("🧪 Testing captain duty prompt...")
        service._send_captain_duty_prompt(priority="normal")
        print("✅ Test duty prompt sent")
    
    elif args.config:
        print("⚙️ Service Configuration:")
        print(json.dumps(service.config, indent=2))
    
    elif args.activate_agents:
        print("🚀 Force activating all agents...")
        service._activate_all_agents()
        print("✅ Agent activation initiated")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
