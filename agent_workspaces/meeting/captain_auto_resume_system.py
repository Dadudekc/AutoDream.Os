#!/usr/bin/env python3
"""
🚨 CAPTAIN AUTO-RESUME SYSTEM 🚨
--auto flag implementation for continuous agent prompting

Purpose: Send resume messages every 10 minutes to keep agents in feedback loop
Target: All agents via input coordinates
Frequency: Every 10 minutes
Customization: Uses prompts from prompts/ directory
"""

import argparse
import datetime
import json
import os
import time
from pathlib import Path
import threading
import schedule
import pyautogui
import pyperclip

class CaptainAutoResumeSystem:
    def __init__(self):
        self.base_path = Path(".")
        self.prompts_path = self.base_path / "prompts"
        self.agents_path = self.base_path / "agent_workspaces"
        self.captain_path = self.base_path / "agent_workspaces" / "Agent-4"
        
        # System state
        self.is_running = False
        self.cycle_count = 0
        self.last_cycle = None
        
        # Load customizable prompts
        self.load_prompts()
        
    def load_prompts(self):
        """Load all customizable prompts from prompts directory"""
        try:
            # Load auto-resume prompt template
            auto_resume_file = self.prompts_path / "captain" / "auto_resume.md"
            if auto_resume_file.exists():
                with open(auto_resume_file, 'r', encoding='utf-8') as f:
                    self.auto_resume_template = f.read()
            else:
                self.auto_resume_template = self.get_default_auto_resume_template()
                
            # Load agent activation prompt template
            activation_file = self.prompts_path / "agents" / "activation.md"
            if activation_file.exists():
                with open(activation_file, 'r', encoding='utf-8') as f:
                    self.activation_template = f.read()
            else:
                self.activation_template = self.get_default_activation_template()
                
            print("✅ Prompts loaded successfully")
            
        except Exception as e:
            print(f"❌ Error loading prompts: {e}")
            self.auto_resume_template = self.get_default_auto_resume_template()
            self.activation_template = self.get_default_activation_template()
    
    def get_default_auto_resume_template(self):
        """Default auto-resume message template"""
        return """📋 RESUME WORKFLOW PROMPT 📋

**FROM:** Captain Agent-4
**TO:** [AGENT_NAME]
**PRIORITY:** HIGH - Maintain Momentum
**TIMESTAMP:** [CURRENT_TIME]

## 🎯 **RESUME YOUR FEEDBACK LOOP:**

**Agent [AGENT_NAME], it's time to resume your workflow:**

1. **Check your inbox** for new messages
2. **Update your status.json** with current timestamp
3. **Continue your current contract** implementation
4. **Report progress** to Captain Agent-4
5. **Maintain momentum** in your feedback loop

## 📋 **CURRENT STATUS CHECK:**
- **Contract:** [CONTRACT_ID] - [CONTRACT_TITLE]
- **Progress:** [X]% Complete
- **Phase:** [CURRENT_PHASE]
- **Next Action:** [NEXT_ACTION]

## 🔄 **FEEDBACK LOOP CONTINUATION:**
- **Check inbox** → **Respond to messages** → **Claim task** → **Update FSM** → **Complete task** → **Update FSM** → **Respond to inbox** → **Claim task** → **REPEAT**

## ⚡ **CAPTAIN DIRECTIVE:**
**Maintain your workflow momentum. The system depends on continuous agent activity.**

**Captain Agent-4 - Automated Oversight Active**
**10-Minute Resume Cycle: [CYCLE_NUMBER]**"""
    
    def get_default_activation_template(self):
        """Default agent activation message template"""
        return """🚨 AGENT ACTIVATION PROMPT 🚨

**FROM:** Captain Agent-4
**TO:** [AGENT_NAME]
**PRIORITY:** CRITICAL - EXECUTE NOW

## 🚨 **STALL DETECTION ALERT:**
- **Current Status:** ⚠️ POTENTIAL STALL - [X] hours inactive
- **Last Activity:** [TIMESTAMP]
- **Stall Duration:** [X] hours [X] minutes
- **Threshold Exceeded:** YES - 7-minute limit violated

## 🎯 **IMMEDIATE ACTION REQUIRED:**
1. **UPDATE YOUR STATUS.JSON** with current timestamp
2. **RESUME [CONTRACT_ID] CONTRACT** implementation
3. **IMPLEMENT [TASK_DESCRIPTION]** immediately
4. **REPORT PROGRESS** within 5 minutes

## 🔄 **CAPTAIN DIRECTIVE:**
**[AGENT_NAME], you are hereby ACTIVATED by Captain Agent-4. Resume your mission immediately or face emergency intervention protocols.**

**Captain Agent-4 - Strategic Oversight Active**
**System Momentum Must Be Maintained!**"""

    def get_agent_input_coordinates(self, agent_name):
        """Get input coordinates for an agent's messaging interface from config file"""
        try:
            config_file = self.base_path / "input_coordinates_config.json"
            if config_file.exists():
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                agent_coords = config.get("agent_input_coordinates", {})
                if agent_name in agent_coords:
                    coords = agent_coords[agent_name]
                    return (coords["x"], coords["y"])
            
            # Fallback to default coordinates if config not found
            print(f"⚠️ Using default coordinates for {agent_name}")
            default_coords = {
                "Agent-1": (100, 200),
                "Agent-2": (100, 300),
                "Agent-3": (100, 400),
                "Agent-4": (100, 500),
                "Agent-5": (100, 600),
                "Agent-6": (100, 700),
                "Agent-7": (100, 800),
                "Agent-8": (100, 900),
            }
            return default_coords.get(agent_name)
            
        except Exception as e:
            print(f"❌ Error loading input coordinates: {e}")
            return None
    
    def send_message_to_coordinates(self, coordinates, message, agent_name):
        """Send message to specific screen coordinates using pyautogui with fast pasting"""
        try:
            x, y = coordinates
            
            # Click on the input coordinates
            pyautogui.click(x, y)
            time.sleep(0.3)  # Brief pause for UI response
            
            # Copy message to clipboard
            pyperclip.copy(message)
            time.sleep(0.1)  # Brief pause for clipboard
            
            # Paste the entire message at once
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.2)  # Brief pause after pasting
            
            # Press Enter to send the message
            pyautogui.press('enter')
            time.sleep(0.3)  # Brief pause for message sending
            
            print(f"✅ Message pasted to {agent_name} at ({x}, {y})")
            return True
            
        except Exception as e:
            print(f"❌ Error sending message to coordinates {coordinates}: {e}")
            return False

    def get_all_agents(self):
        """Get list of all available agents"""
        agents = []
        if self.agents_path.exists():
            for agent_dir in self.agents_path.iterdir():
                if agent_dir.is_dir() and agent_dir.name.startswith("Agent-"):
                    agents.append(agent_dir.name)
        return sorted(agents)
    
    def get_agent_status(self, agent_name):
        """Get current status of an agent"""
        status_file = self.agents_path / agent_name / "status.json"
        if status_file.exists():
            try:
                with open(status_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return None
    
    def check_agent_stall(self, agent_status):
        """Check if agent is stalled (7+ minutes inactive)"""
        if not agent_status or 'last_updated' not in agent_status:
            return True, "Unknown"
        
        try:
            last_update = datetime.datetime.strptime(
                agent_status['last_updated'], 
                "%Y-%m-%d %H:%M:%S"
            )
            now = datetime.datetime.now()
            time_diff = now - last_update
            minutes_inactive = time_diff.total_seconds() / 60
            
            if minutes_inactive > 7:
                return True, f"{int(minutes_inactive)} minutes"
            return False, f"{int(minutes_inactive)} minutes"
        except:
            return True, "Unknown"
    
    def send_resume_message(self, agent_name, agent_status=None):
        """Send resume message to agent via pyautogui to input coordinates"""
        try:
            # Get input coordinates for this agent
            input_coords = self.get_agent_input_coordinates(agent_name)
            if not input_coords:
                print(f"⚠️ No input coordinates found for {agent_name}")
                return False
            
            # Determine message type based on agent status
            if agent_status:
                is_stalled, stall_duration = self.check_agent_stall(agent_status)
                
                if is_stalled:
                    # Send activation message for stalled agent
                    message = self.create_activation_message(agent_name, agent_status, stall_duration)
                else:
                    # Send regular resume message for active agent
                    message = self.create_resume_message(agent_name, agent_status)
            else:
                # Send generic resume message if no status available
                message = self.create_generic_resume_message(agent_name)
            
            # Send message via pyautogui to input coordinates
            success = self.send_message_to_coordinates(input_coords, message, agent_name)
            
            if success:
                print(f"✅ Resume message sent to {agent_name} at coordinates {input_coords}")
            else:
                print(f"❌ Failed to send message to {agent_name}")
            
            return success
            
        except Exception as e:
            print(f"❌ Error sending resume message to {agent_name}: {e}")
            return False
    
    def create_resume_message(self, agent_name, agent_status):
        """Create resume message for active agent"""
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Calculate stall duration
        last_update = agent_status.get('last_updated', 'Unknown')
        stall_duration = "Unknown"
        if last_update != 'Unknown':
            try:
                last_update_dt = datetime.datetime.strptime(last_update, "%Y-%m-%d %H:%M:%S")
                now = datetime.datetime.now()
                time_diff = now - last_update_dt
                hours = int(time_diff.total_seconds() // 3600)
                minutes = int((time_diff.total_seconds() % 3600) // 60)
                if hours > 0:
                    stall_duration = f"{hours} hours {minutes} minutes"
                else:
                    stall_duration = f"{minutes} minutes"
            except:
                stall_duration = "Unknown"
        
        # Extract contract info from status
        contract_id = agent_status.get('current_contract', {}).get('contract_id', 'UNKNOWN')
        contract_title = agent_status.get('current_contract', {}).get('title', 'Unknown Contract')
        progress = agent_status.get('progress', {}).get('percentage', '0%')
        current_phase = agent_status.get('progress', {}).get('current_phase', 'Unknown Phase')
        next_actions = agent_status.get('next_actions', ['Continue current work'])
        
        message = self.auto_resume_template
        message = message.replace('[AGENT_NAME]', agent_name)
        message = message.replace('[CURRENT_TIME]', current_time)
        message = message.replace('[CYCLE_NUMBER]', str(self.cycle_count))
        message = message.replace('[LAST_UPDATE]', last_update)
        message = message.replace('[STALL_DURATION]', stall_duration)
        message = message.replace('[CONTRACT_ID]', contract_id)
        message = message.replace('[CONTRACT_TITLE]', contract_title)
        message = message.replace('[PROGRESS]', progress)
        message = message.replace('[CURRENT_PHASE]', current_phase)
        message = message.replace('[NEXT_ACTION]', next_actions[0] if next_actions else 'Continue current work')
        
        return message
    
    def create_activation_message(self, agent_name, agent_status, stall_duration):
        """Create activation message for stalled agent"""
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Extract contract info from status
        contract_id = agent_status.get('current_contract', {}).get('contract_id', 'UNKNOWN')
        contract_title = agent_status.get('current_contract', {}).get('title', 'Unknown Contract')
        progress = agent_status.get('progress', {}).get('percentage', '0%')
        current_phase = agent_status.get('progress', {}).get('current_phase', 'Unknown Phase')
        next_actions = agent_status.get('next_actions', ['Resume current work'])
        
        message = self.activation_template
        message = message.replace('[AGENT_NAME]', agent_name)
        message = message.replace('[STALL_DURATION]', stall_duration)
        message = message.replace('[CONTRACT_ID]', contract_id)
        message = message.replace('[CONTRACT_TITLE]', contract_title)
        message = message.replace('[PROGRESS]', progress)
        message = message.replace('[CURRENT_PHASE]', current_phase)
        message = message.replace('[NEXT_ACTION]', next_actions[0] if next_actions else 'Resume current work')
        
        return message
    
    def create_generic_resume_message(self, agent_name):
        """Create generic resume message when no status available"""
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        message = self.auto_resume_template
        message = message.replace('[AGENT_NAME]', agent_name)
        message = message.replace('[CURRENT_TIME]', current_time)
        message = message.replace('[CONTRACT_ID]', 'UNKNOWN')
        message = message.replace('[CONTRACT_TITLE]', 'Unknown Contract')
        message = message.replace('[X]% Complete', '0%')
        message = message.replace('[CURRENT_PHASE]', 'Unknown Phase')
        message = message.replace('[NEXT_ACTION]', 'Check status and resume work')
        message = message.replace('[CYCLE_NUMBER]', str(self.cycle_count))
        
        return message
    
    def execute_resume_cycle(self):
        """Execute one complete resume cycle for all agents"""
        self.cycle_count += 1
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"\n🔄 EXECUTING RESUME CYCLE #{self.cycle_count} at {current_time}")
        print("=" * 60)
        
        # Get all agents
        agents = self.get_all_agents()
        print(f"📋 Found {len(agents)} agents: {', '.join(agents)}")
        
        # Send resume messages to all agents
        success_count = 0
        for agent_name in agents:
            agent_status = self.get_agent_status(agent_name)
            if self.send_resume_message(agent_name, agent_status):
                success_count += 1
        
        # Update cycle info
        self.last_cycle = current_time
        
        print(f"✅ Resume cycle #{self.cycle_count} completed: {success_count}/{len(agents)} messages sent")
        print("=" * 60)
        
        # Update Captain status
        self.update_captain_status()
    
    def update_captain_status(self):
        """Update Captain Agent-4 status with cycle information"""
        try:
            status_file = self.captain_path / "status.json"
            if status_file.exists():
                with open(status_file, 'r', encoding='utf-8') as f:
                    status = json.load(f)
                
                # Update auto-resume system info
                if 'auto_resume_system' not in status:
                    status['auto_resume_system'] = {}
                
                status['auto_resume_system'].update({
                    'last_cycle': self.last_cycle,
                    'cycle_count': self.cycle_count,
                    'is_running': self.is_running,
                    'last_updated': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                
                # Update last_updated timestamp
                status['last_updated'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Write updated status
                with open(status_file, 'w', encoding='utf-8') as f:
                    json.dump(status, f, indent=2, ensure_ascii=False)
                
                print(f"✅ Captain status updated - Cycle #{self.cycle_count}")
                
        except Exception as e:
            print(f"❌ Error updating Captain status: {e}")
    
    def start_auto_resume_system(self):
        """Start the auto-resume system with 10-minute intervals"""
        if self.is_running:
            print("⚠️ Auto-resume system is already running")
            return
        
        print("🚀 STARTING CAPTAIN AUTO-RESUME SYSTEM")
        print("📋 Sending resume messages every 10 minutes")
        print("🎯 Target: All agents via inbox messaging")
        print("=" * 60)
        
        self.is_running = True
        
        # Schedule resume cycles every 10 minutes
        schedule.every(10).minutes.do(self.execute_resume_cycle)
        
        # Execute first cycle immediately
        self.execute_resume_cycle()
        
        # Run the scheduler
        try:
            while self.is_running:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Auto-resume system stopped by user")
            self.stop_auto_resume_system()
    
    def stop_auto_resume_system(self):
        """Stop the auto-resume system"""
        self.is_running = False
        schedule.clear()
        print("🛑 Auto-resume system stopped")
    
    def run_single_cycle(self):
        """Run a single resume cycle for testing"""
        print("🧪 Running single resume cycle for testing")
        self.execute_resume_cycle()

def main():
    """Main function for --auto flag system"""
    import sys
    
    auto_system = CaptainAutoResumeSystem()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--auto":
            print("🚀 Starting --auto flag system")
            auto_system.start_auto_resume_system()
        elif sys.argv[1] == "--test":
            print("🧪 Running test cycle")
            auto_system.run_single_cycle()
        elif sys.argv[1] == "--help":
            print("""
🚨 CAPTAIN AUTO-RESUME SYSTEM 🚨

Usage:
  python captain_auto_resume_system.py --auto     # Start continuous 10-minute cycles
  python captain_auto_resume_system.py --test     # Run single test cycle
  python captain_auto_resume_system.py --help     # Show this help

Features:
  - Sends resume messages every 10 minutes
  - Uses customizable prompts from prompts/ directory
  - Automatically detects stalled agents
  - Sends appropriate message types (resume vs activation)
  - Updates Captain status with cycle information
  - Targets all agents via inbox messaging system

--auto flag: Continuous operation with 10-minute intervals
--test flag: Single cycle execution for testing
            """)
        else:
            print(f"❌ Unknown flag: {sys.argv[1]}")
            print("Use --help for usage information")
    else:
        print("🚨 CAPTAIN AUTO-RESUME SYSTEM")
        print("Use --auto to start continuous operation")
        print("Use --test to run single cycle")
        print("Use --help for usage information")

if __name__ == "__main__":
    main()
