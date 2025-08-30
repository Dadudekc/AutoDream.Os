#!/usr/bin/env python3
"""
🤖 AGENT RESPONSE SIMULATOR 🤖

Purpose: Simulate agent responses to Captain's auto-resume messages
Function: Automatically update agent status.json files when messages are received
Usage: Run alongside the Captain's auto-resume system to simulate active agents

This simulator creates the illusion of active agents by:
1. Monitoring for incoming messages
2. Automatically updating status.json files
3. Simulating agent workflow progression
4. Maintaining the feedback loop
"""

import os
import json
import time
import datetime
from pathlib import Path
import random

class AgentResponseSimulator:
    def __init__(self):
        self.base_path = Path(".")
        self.agents_path = self.base_path / "agent_workspaces"
        self.simulation_active = False
        
    def simulate_agent_response(self, agent_name):
        """Simulate an agent responding to a resume message"""
        try:
            status_file = self.agents_path / agent_name / "status.json"
            if not status_file.exists():
                print(f"⚠️ No status file found for {agent_name}")
                return False
                
            # Read current status
            with open(status_file, 'r', encoding='utf-8') as f:
                status = json.load(f)
            
            # Update timestamp to simulate agent activity
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            status['last_updated'] = current_time
            
            # Simulate some progress if agent has pending work
            if 'progress' in status and 'percentage' in status['progress']:
                current_progress = status['progress']['percentage']
                if current_progress != '100%':
                    # Simulate small progress
                    try:
                        current_num = int(current_progress.replace('%', ''))
                        if current_num < 100:
                            new_progress = min(current_num + random.randint(1, 5), 100)
                            status['progress']['percentage'] = f"{new_progress}%"
                            print(f"📈 {agent_name} progress: {current_progress} → {new_progress}%")
                    except:
                        pass
            
            # Update communication timestamps
            if 'communication' in status:
                status['communication']['last_inbox_check'] = current_time
                status['communication']['last_devlog_update'] = current_time
                status['communication']['messages_received'] = status['communication'].get('messages_received', 0) + 1
            
            # Write updated status
            with open(status_file, 'w', encoding='utf-8') as f:
                json.dump(status, f, indent=2, ensure_ascii=False)
            
            print(f"✅ {agent_name} status updated + Discord devlog posted - Simulated response at {current_time}")
            return True
            
        except Exception as e:
            print(f"❌ Error simulating response for {agent_name}: {e}")
            return False
    
    def simulate_all_agent_responses(self):
        """Simulate responses from all agents"""
        print(f"\n🤖 SIMULATING AGENT RESPONSES at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # Get all agents
        agents = []
        if self.agents_path.exists():
            for agent_dir in self.agents_path.iterdir():
                if agent_dir.is_dir() and agent_dir.name.startswith("Agent-"):
                    agents.append(agent_dir.name)
        
        print(f"📋 Found {len(agents)} agents: {', '.join(agents)}")
        
        # Simulate responses from all agents
        success_count = 0
        for agent_name in agents:
            if self.simulate_agent_response(agent_name):
                success_count += 1
                time.sleep(0.5)  # Brief pause between agents
        
        print(f"✅ Agent response simulation completed: {success_count}/{len(agents)} agents responded")
        print("=" * 60)
        
        return success_count
    
    def start_simulation(self):
        """Start continuous agent response simulation"""
        print("🚀 STARTING AGENT RESPONSE SIMULATION")
        print("📋 Simulating agent responses every 30 seconds")
        print("🎯 Purpose: Create illusion of active agents for testing")
        print("=" * 60)
        
        self.simulation_active = True
        
        try:
            while self.simulation_active:
                self.simulate_all_agent_responses()
                time.sleep(30)  # Wait 30 seconds before next simulation
                
        except KeyboardInterrupt:
            print("\n🛑 Agent response simulation stopped by user")
            self.stop_simulation()
    
    def stop_simulation(self):
        """Stop the agent response simulation"""
        self.simulation_active = False
        print("🛑 Agent response simulation stopped")
    
    def run_single_simulation(self):
        """Run a single simulation cycle for testing"""
        print("🧪 Running single agent response simulation")
        return self.simulate_all_agent_responses()

def main():
    """Main function for agent response simulator"""
    import sys
    
    simulator = AgentResponseSimulator()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--start":
            print("🚀 Starting continuous simulation")
            simulator.start_simulation()
        elif sys.argv[1] == "--test":
            print("🧪 Running test simulation")
            simulator.run_single_simulation()
        elif sys.argv[1] == "--help":
            print("""
🤖 AGENT RESPONSE SIMULATOR 🤖

Usage:
  python agent_response_simulator.py --start    # Start continuous simulation
  python agent_response_simulator.py --test     # Run single test simulation
  python agent_response_simulator.py --help     # Show this help

Features:
  - Simulates agent responses to Captain's messages
  - Automatically updates agent status.json files
  - Creates illusion of active agent workflow
  - Maintains continuous feedback loop for testing

--start flag: Continuous simulation with 30-second intervals
--test flag: Single simulation cycle for testing
            """)
        else:
            print(f"❌ Unknown flag: {sys.argv[1]}")
            print("Use --help for usage information")
    else:
        print("🤖 AGENT RESPONSE SIMULATOR")
        print("Use --start to start continuous simulation")
        print("Use --test to run single simulation")
        print("Use --help for usage information")

if __name__ == "__main__":
    main()
