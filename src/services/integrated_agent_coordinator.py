#!/usr/bin/env python3
"""
Integrated Agent Coordinator - Agent Cellphone Context v2
=======================================================

Combines Agent-5 PyAutoGUI coordination with V1-V2 message queue system
for comprehensive agent management and communication.
"""

import json
import time
import asyncio
import pyautogui
import pyperclip
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import sys
import os

# Add CORE directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

# Import V1-V2 message queue system
from v1_v2_message_queue_system import (
    MessageQueueManager,
    MessageQueuePriority
)
from cdp_message_delivery import (
    CDPMessageDelivery,
    send_message_to_cursor,
    broadcast_message_to_cursor
)
from core.shared_enums import AgentCapability

# Import Discord communication (if available)
try:
    from discord_agent_communication_v2 import (
        ping_discord_status,
        ping_discord_progress,
        ping_discord_completion,
        ping_discord_coordination,
        ping_discord_error,
        ping_discord_system
    )
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    # Create mock functions
    async def ping_discord_status(agent, status, message): print(f"[DISCORD] {agent}: {status} - {message}")
    async def ping_discord_progress(agent, task, progress, message): print(f"[DISCORD] {agent}: {task} - {progress}% - {message}")
    async def ping_discord_completion(agent, task, message): print(f"[DISCORD] {agent}: {task} COMPLETE - {message}")
    async def ping_discord_coordination(agent, message): print(f"[DISCORD] {agent}: COORDINATION - {message}")
    async def ping_discord_error(agent, error, details): print(f"[DISCORD] {agent}: ERROR - {error} - {details}")
    async def ping_discord_system(agent, message): print(f"[DISCORD] {agent}: SYSTEM - {message}")


class IntegratedAgentCoordinator:
    """Integrated coordinator combining PyAutoGUI and message queue systems."""
    
    def __init__(self, election_mode: bool = False, round_robin: bool = False):
        # Setup logging first
        self.setup_logging()
        
        # Initialize both coordination systems
        self.pyautogui_coordinator = Agent5PyAutoGUICoordinator(election_mode, round_robin)
        self.message_queue_manager = MessageQueueManager()
        
        # Integration state
        self.integration_mode = "hybrid"  # pyautogui, message_queue, hybrid
        self.coordination_cycle = 0
        self.last_coordination = None
        
        # Agent mapping between systems
        self.agent_mapping = {
            "Agent-1": "agent_1",
            "Agent-2": "agent_2", 
            "Agent-3": "agent_3",
            "Agent-4": "agent_4",
            "Agent-5": "agent_5"
        }
        
        # Register agents in message queue system
        self.register_agents_in_queue()
        
        self.logger.info("🚀 Integrated Agent Coordinator initialized successfully")
    
    def setup_logging(self):
        """Setup logging for integrated coordination system"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s | %(levelname)s | %(message)s',
            handlers=[
                logging.FileHandler(log_dir / "integrated_coordinator.log", encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def register_agents_in_queue(self):
        """Register all agents in the message queue system"""
        try:
            agents = [
                {
                    "id": "agent_1",
                    "name": "Foundation & Testing Specialist",
                    "capabilities": [AgentCapability.TASK_EXECUTION, AgentCapability.MONITORING],
                    "window_title": "Cursor - Agent_Cellphone_V2_Repository"
                },
                {
                    "id": "agent_2", 
                    "name": "AI/ML Specialist",
                    "capabilities": [AgentCapability.DECISION_MAKING, AgentCapability.DATA_PROCESSING],
                    "window_title": "Cursor - AI_ML_Project"
                },
                {
                    "id": "agent_3",
                    "name": "Web Development Specialist", 
                    "capabilities": [AgentCapability.TASK_EXECUTION, AgentCapability.COMMUNICATION],
                    "window_title": "Cursor - Web_Development_Project"
                },
                {
                    "id": "agent_4",
                    "name": "Multimedia & Gaming Specialist",
                    "capabilities": [AgentCapability.DATA_PROCESSING, AgentCapability.MONITORING],
                    "window_title": "Cursor - Multimedia_Gaming_Project"
                },
                {
                    "id": "agent_5",
                    "name": "CAPTAIN Coordination & PyAutoGUI Leadership",
                    "capabilities": [AgentCapability.DECISION_MAKING, AgentCapability.COMMUNICATION],
                    "window_title": "Cursor - Agent_Cellphone_V2_Repository"
                }
            ]
            
            for agent in agents:
                success = self.message_queue_manager.register_agent(
                    agent_id=agent["id"],
                    agent_name=agent["name"],
                    capabilities=agent["capabilities"],
                    window_title=agent["window_title"]
                )
                
                if success:
                    self.logger.info(f"✅ Registered {agent['name']} in message queue")
                else:
                    self.logger.warning(f"⚠️ Failed to register {agent['name']} in message queue")
            
            self.logger.info(f"📋 Message queue registration complete: {len(agents)} agents")
            
        except Exception as e:
            self.logger.error(f"Error registering agents in message queue: {e}")
    
    async def send_message_hybrid(self, agent_id: str, message: str, priority: MessageQueuePriority = MessageQueuePriority.NORMAL, use_pyautogui: bool = True) -> bool:
        """Send message using hybrid approach - try message queue first, fallback to PyAutoGUI"""
        try:
            success = False
            
            # Try message queue first (CDP-based, no mouse movement)
            try:
                if self.integration_mode in ["hybrid", "message_queue"]:
                    message_id = self.message_queue_manager.send_message(
                        source_agent="agent_5",  # Agent-5 is the coordinator
                        target_agent=agent_id,
                        content=message,
                        priority=priority
                    )
                    
                    if message_id:
                        self.logger.info(f"✅ Message sent via queue to {agent_id}: {message_id}")
                        success = True
                        
                        # Update coordination metrics
                        self.coordination_cycle += 1
                        self.last_coordination = datetime.now()
                        
            except Exception as e:
                self.logger.warning(f"Message queue failed for {agent_id}: {e}")
                success = False
            
            # Fallback to PyAutoGUI if queue failed or explicitly requested
            if not success and use_pyautogui:
                self.logger.info(f"🔄 Falling back to PyAutoGUI for {agent_id}")
                
                # Map agent ID to PyAutoGUI format
                pyautogui_agent = None
                for key, value in self.agent_mapping.items():
                    if value == agent_id:
                        pyautogui_agent = key
                        break
                
                if pyautogui_agent:
                    success = self.pyautogui_coordinator.send_message_to_agent(pyautogui_agent, message)
                    
                    if success:
                        self.logger.info(f"✅ Message sent via PyAutoGUI to {pyautogui_agent}")
                        self.coordination_cycle += 1
                        self.last_coordination = datetime.now()
                    else:
                        self.logger.error(f"❌ PyAutoGUI fallback failed for {pyautogui_agent}")
                else:
                    self.logger.error(f"❌ Could not map agent ID {agent_id} to PyAutoGUI format")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error in hybrid message sending to {agent_id}: {e}")
            return False
    
    async def broadcast_message_hybrid(self, message: str, priority: MessageQueuePriority = MessageQueuePriority.NORMAL, use_pyautogui: bool = True) -> Dict[str, bool]:
        """Broadcast message to all agents using hybrid approach"""
        try:
            results = {}
            
            # Try message queue broadcast first
            try:
                if self.integration_mode in ["hybrid", "message_queue"]:
                    message_ids = self.message_queue_manager.broadcast_message(
                        source_agent="agent_5",
                        content=message,
                        priority=priority
                    )
                    
                    if message_ids:
                        self.logger.info(f"✅ Broadcast sent via queue to {len(message_ids)} agents")
                        
                        # Mark all as successful initially
                        for agent_id in self.agent_mapping.values():
                            results[agent_id] = True
                        
                        self.coordination_cycle += 1
                        self.last_coordination = datetime.now()
                        
            except Exception as e:
                self.logger.warning(f"Message queue broadcast failed: {e}")
                # Mark all as failed initially
                for agent_id in self.agent_mapping.values():
                    results[agent_id] = False
            
            # Fallback to PyAutoGUI if queue failed or explicitly requested
            if not any(results.values()) and use_pyautogui:
                self.logger.info("🔄 Falling back to PyAutoGUI broadcast")
                
                for pyautogui_agent in self.agent_mapping.keys():
                    success = self.pyautogui_coordinator.send_message_to_agent(pyautogui_agent, message)
                    results[self.agent_mapping[pyautogui_agent]] = success
                    
                    if success:
                        self.logger.info(f"✅ PyAutoGUI broadcast to {pyautogui_agent}")
                    else:
                        self.logger.error(f"❌ PyAutoGUI broadcast failed to {pyautogui_agent}")
                
                self.coordination_cycle += 1
                self.last_coordination = datetime.now()
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error in hybrid broadcast: {e}")
            return {agent_id: False for agent_id in self.agent_mapping.values()}
    
    async def coordinate_agent_workflow_hybrid(self, agent_id: str, workflow_type: str, use_pyautogui: bool = True) -> bool:
        """Coordinate agent workflow using hybrid approach"""
        try:
            # Determine workflow message based on type
            workflow_messages = {
                "strategic_coordination": f"Agent-5 CAPTAIN: Execute strategic coordination workflow. Report status to Discord.",
                "task_management": f"Agent-5 CAPTAIN: Begin task breakdown and resource allocation. Coordinate with other agents.",
                "technical_implementation": f"Agent-5 CAPTAIN: Start technical implementation tasks. Report progress to Discord.",
                "security_protocols": f"Agent-5 CAPTAIN: Implement security protocols and communication standards.",
                "general_coordination": f"Agent-5 CAPTAIN: Execute general coordination workflow. Report status to Discord."
            }
            
            message = workflow_messages.get(workflow_type, f"Agent-5 CAPTAIN: Execute {workflow_type} workflow.")
            
            # Send message using hybrid approach
            success = await self.send_message_hybrid(agent_id, message, MessageQueuePriority.HIGH, use_pyautogui)
            
            if success:
                self.logger.info(f"✅ {agent_id} workflow '{workflow_type}' coordinated successfully")
                
                # Report to Discord if available
                if DISCORD_AVAILABLE:
                    await ping_discord_progress("Agent-5", f"Agent Coordination", 
                                             int((list(self.agent_mapping.values()).index(agent_id) + 1) * 20),
                                             f"Successfully coordinated {agent_id}")
            else:
                self.logger.error(f"❌ Failed to coordinate {agent_id} workflow '{workflow_type}'")
                
                # Report error to Discord if available
                if DISCORD_AVAILABLE:
                    await ping_discord_error("Agent-5", f"Coordination failed for {agent_id}", 
                                           f"Workflow: {workflow_type}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error coordinating workflow for {agent_id}: {e}")
            return False
    
    async def execute_coordination_cycle_hybrid(self) -> bool:
        """Execute a complete coordination cycle using hybrid approach"""
        try:
            self.coordination_cycle += 1
            self.logger.info(f"🚀 Starting hybrid coordination cycle {self.coordination_cycle}")
            
            # Report cycle start to Discord
            if DISCORD_AVAILABLE:
                await ping_discord_status("Agent-5", "Hybrid Coordinating", f"Starting coordination cycle {self.coordination_cycle}")
            
            # Coordinate each agent
            coordination_results = {}
            
            for agent_id, role in self.pyautogui_coordinator.agent_roles.items():
                # Map to message queue agent ID
                queue_agent_id = self.agent_mapping.get(agent_id)
                if not queue_agent_id:
                    self.logger.warning(f"⚠️ No mapping found for {agent_id}")
                    continue
                
                self.logger.info(f"🎯 Coordinating {agent_id}: {role}")
                
                # Determine workflow type based on agent role
                if "Strategic" in role:
                    workflow_type = "strategic_coordination"
                elif "Task" in role:
                    workflow_type = "task_management"
                elif "Technical" in role:
                    workflow_type = "technical_implementation"
                elif "Security" in role:
                    workflow_type = "security_protocols"
                else:
                    workflow_type = "general_coordination"
                
                # Execute coordination using hybrid approach
                success = await self.coordinate_agent_workflow_hybrid(queue_agent_id, workflow_type)
                coordination_results[agent_id] = success
                
                # Wait between agents
                await asyncio.sleep(2.0)
            
            # Report cycle completion
            success_count = sum(coordination_results.values())
            total_agents = len(coordination_results)
            
            if success_count == total_agents:
                if DISCORD_AVAILABLE:
                    await ping_discord_completion("Agent-5", f"Hybrid Coordination Cycle {self.coordination_cycle}", 
                                               f"{success_count}/{total_agents} agents coordinated successfully")
                self.logger.info(f"✅ Hybrid coordination cycle {self.coordination_cycle} completed successfully")
            else:
                if DISCORD_AVAILABLE:
                    await ping_discord_error("Agent-5", f"Hybrid coordination cycle {self.coordination_cycle} incomplete", 
                                          f"Only {success_count}/{total_agents} agents coordinated successfully")
                self.logger.warning(f"⚠️ Hybrid coordination cycle {self.coordination_cycle} partially completed")
            
            return success_count == total_agents
            
        except Exception as e:
            self.logger.error(f"Error in hybrid coordination cycle: {e}")
            if DISCORD_AVAILABLE:
                await ping_discord_error("Agent-5", "Hybrid coordination cycle error", str(e))
            return False
    
    async def run_continuous_coordination_hybrid(self, cycles: int = 5, interval: int = 120):
        """Run continuous coordination cycles using hybrid approach"""
        try:
            self.logger.info(f"🚀 Starting continuous hybrid coordination: {cycles} cycles, {interval}s interval")
            
            if DISCORD_AVAILABLE:
                await ping_discord_status("Agent-5", "Continuous Hybrid Coordination", f"Starting {cycles} coordination cycles")
            
            for cycle in range(1, cycles + 1):
                self.logger.info(f"🔄 Hybrid coordination cycle {cycle}/{cycles}")
                
                # Execute coordination cycle
                success = await self.execute_coordination_cycle_hybrid()
                
                if cycle < cycles:
                    self.logger.info(f"⏳ Waiting {interval}s before next cycle...")
                    
                    if DISCORD_AVAILABLE:
                        await ping_discord_status("Agent-5", "Standby", f"Waiting {interval}s before cycle {cycle + 1}")
                    
                    await asyncio.sleep(interval)
            
            # Final status report
            if DISCORD_AVAILABLE:
                await ping_discord_completion("Agent-5", "Continuous Hybrid Coordination Complete", 
                                           f"Completed {cycles} coordination cycles")
            
            self.logger.info("✅ Continuous hybrid coordination completed successfully")
            
        except Exception as e:
            self.logger.error(f"Error in continuous hybrid coordination: {e}")
            if DISCORD_AVAILABLE:
                await ping_discord_error("Agent-5", "Continuous hybrid coordination error", str(e))
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status from both coordination systems"""
        try:
            # Get message queue status
            queue_status = self.message_queue_manager.get_system_status()
            
            # Get PyAutoGUI coordinator status
            pyautogui_status = {
                "coordination_cycle": self.pyautogui_coordinator.coordination_cycle,
                "agent_status": self.pyautogui_coordinator.agent_status,
                "election_mode": self.pyautogui_coordinator.election_mode,
                "round_robin": self.pyautogui_coordinator.round_robin
            }
            
            # Combined status
            status = {
                "integration_mode": self.integration_mode,
                "coordination_cycle": self.coordination_cycle,
                "last_coordination": self.last_coordination.isoformat() if self.last_coordination else None,
                "message_queue_system": queue_status,
                "pyautogui_coordinator": pyautogui_status,
                "agent_mapping": self.agent_mapping,
                "discord_available": DISCORD_AVAILABLE
            }
            
            return status
            
        except Exception as e:
            self.logger.error(f"Error getting system status: {e}")
            return {"error": str(e)}
    
    def generate_integrated_status_report(self) -> str:
        """Generate comprehensive status report from both systems"""
        try:
            status = self.get_system_status()
            
            report = f"""
🎖️ INTEGRATED AGENT COORDINATOR STATUS REPORT
{'=' * 70}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Integration Mode: {status['integration_mode'].upper()}
Coordination Cycles: {status['coordination_cycle']}
Last Coordination: {status['last_coordination'] or 'Never'}

📊 MESSAGE QUEUE SYSTEM STATUS
{'-' * 50}
Registered Agents: {status['message_queue_system']['registered_agents']}
Queue Size: {status['message_queue_system']['queue_system']['queue_size']}
System Running: {status['message_queue_system']['queue_system']['is_running']}
Delivery Workers: {status['message_queue_system']['queue_system']['delivery_workers']}

🤖 PYAUTOGUI COORDINATOR STATUS
{'-' * 50}
Coordination Cycles: {status['pyautogui_coordinator']['coordination_cycle']}
Election Mode: {'ENABLED' if status['pyautogui_coordinator']['election_mode'] else 'DISABLED'}
Round-Robin Mode: {'ENABLED' if status['pyautogui_coordinator']['round_robin'] else 'DISABLED'}

📋 AGENT MAPPING
{'-' * 50}
"""
            
            for pyautogui_agent, queue_agent in status['agent_mapping'].items():
                report += f"  {pyautogui_agent} → {queue_agent}\n"
            
            report += f"""
🎯 INTEGRATION METRICS
{'-' * 50}
Total Agents: {len(status['agent_mapping'])}
Integration Status: {'FULLY OPERATIONAL' if status['coordination_cycle'] > 0 else 'STANDBY'}
Discord Integration: {'AVAILABLE' if status['discord_available'] else 'UNAVAILABLE'}

🚀 SYSTEM STATUS: {'FULLY OPERATIONAL' if status['coordination_cycle'] > 0 else 'STANDBY'}
"""
            
            return report
            
        except Exception as e:
            self.logger.error(f"Error generating integrated status report: {e}")
            return f"Error generating integrated status report: {e}"
    
    async def send_integrated_status_report_to_discord(self):
        """Send integrated status report to Discord"""
        try:
            if not DISCORD_AVAILABLE:
                self.logger.warning("Discord integration not available")
                return
            
            report = self.generate_integrated_status_report()
            
            # Split report into chunks if too long
            max_length = 1900  # Discord limit with buffer
            if len(report) > max_length:
                chunks = [report[i:i+max_length] for i in range(0, len(report), max_length)]
                for i, chunk in enumerate(chunks):
                    await ping_discord_system("Agent-5", f"Integrated Status Report Part {i+1}/{len(chunks)}")
                    await asyncio.sleep(1.0)  # Small delay between chunks
            else:
                await ping_discord_system("Agent-5", "Integrated Coordination Status Report")
            
            self.logger.info("✅ Integrated status report sent to Discord successfully")
            
        except Exception as e:
            self.logger.error(f"Error sending integrated status report to Discord: {e}")


# Import the PyAutoGUI coordinator class
class Agent5PyAutoGUICoordinator:
    """Agent-5 CAPTAIN PyAutoGUI coordination system with election capabilities"""
    
    def __init__(self, election_mode: bool = False, round_robin: bool = False):
        # Setup logging first
        self.setup_logging()
        
        self.coord_file = Path("../runtime/agent_comms/cursor_agent_coords.json")
        self.coordinates = self.load_coordinates()
        self.agent_status = {}
        self.coordination_cycle = 0
        
        # Election and round-robin flags
        self.election_mode = election_mode
        self.round_robin = round_robin
        self.current_captain_index = 0
        
        # Campaign directory setup
        self.campaigns_dir = Path("../Agent_Cellphone_V2/agent_workspaces/campaigns")
        self.campaigns_dir.mkdir(exist_ok=True)
        
        # Initialize PyAutoGUI settings
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.5
        
        # Agent role definitions with election capabilities (INCLUDING AGENT-5)
        self.agent_roles = {
            "Agent-1": "Strategic Coordination & Knowledge Management",
            "Agent-2": "Task Breakdown & Resource Allocation", 
            "Agent-3": "Data Analysis & Technical Implementation",
            "Agent-4": "Communication Protocols & Security",
            "Agent-5": "CAPTAIN Coordination & PyAutoGUI Leadership"
        }
        
        # Election state
        self.election_state = {
            "active": False,
            "phase": "idle",  # idle, campaigning, voting, results
            "candidates": [],
            "votes": {},
            "current_captain": None,
            "campaign_duration": 300,  # 5 minutes
            "voting_duration": 120,    # 2 minutes
            "term_duration": 1800      # 30 minutes
        }
        
        # Initialize agent status
        for agent_id in self.agent_roles.keys():
            self.agent_status[agent_id] = {
                "status": "standby",
                "last_activity": None,
                "coordination_count": 0,
                "errors": [],
                "captain_terms": 0,
                "campaign_success": 0,
                "voting_record": {}
            }
    
    def setup_logging(self):
        """Setup logging for coordination system"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s | %(levelname)s | %(message)s',
            handlers=[
                logging.FileHandler(log_dir / "agent5_coordination.log", encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def load_coordinates(self) -> Dict[str, Any]:
        """Load agent coordinates from configuration file"""
        try:
            if self.coord_file.exists():
                with open(self.coord_file, 'r') as f:
                    coords = json.load(f)
                    self.logger.info(f"Coordinates loaded: {len(coords)} agent configurations")
                    return coords
            else:
                self.logger.error(f"Coordinate file not found: {self.coord_file}")
                return {}
        except Exception as e:
            self.logger.error(f"Error loading coordinates: {e}")
            return {}
    
    def send_message_to_agent(self, agent_id: str, message: str, use_shift_enter: bool = True) -> bool:
        """Send a message to an agent by typing in their input box with optional Shift+Enter line breaks"""
        try:
            coords = self.get_agent_coordinates(agent_id)
            if not coords or "input_box" not in coords:
                self.logger.error(f"No input coordinates for {agent_id}")
                return False
            
            x = coords["input_box"]["x"]
            y = coords["input_box"]["y"]
            
            self.logger.info(f"Sending message to {agent_id} at coordinates ({x}, {y})")
            
            # Click input box
            pyautogui.moveTo(x, y, duration=0.5)
            pyautogui.click()
            
            # Clear existing text and type message
            pyautogui.hotkey('ctrl', 'a')  # Select all
            pyautogui.press('delete')       # Clear
            
            if use_shift_enter and '\n' in message:
                # Handle multi-line messages with Shift+Enter
                lines = message.split('\n')
                for i, line in enumerate(lines):
                    if i > 0:  # Add line break for all lines except the first
                        pyautogui.hotkey('shift', 'enter')  # Shift+Enter for line break
                    pyautogui.typewrite(line, interval=0.05)
            else:
                # Single line message
                pyautogui.typewrite(message, interval=0.05)
            
            # Send message (Enter key)
            pyautogui.press('enter')
            
            # Update agent status
            self.agent_status[agent_id]["last_activity"] = datetime.now()
            self.agent_status[agent_id]["coordination_count"] += 1
            
            self.logger.info(f"✅ Message sent to {agent_id}: {message[:50]}...")
            return True
            
        except Exception as e:
            self.logger.error(f"Error sending message to {agent_id}: {e}")
            self.agent_status[agent_id]["errors"].append(str(e))
            return False
    
    def get_agent_coordinates(self, agent_id: str, mode: str = "5-agent") -> Optional[Dict[str, Any]]:
        """Get coordinates for a specific agent"""
        try:
            if mode in self.coordinates and agent_id in self.coordinates[mode]:
                return self.coordinates[mode][agent_id]
            else:
                self.logger.warning(f"Coordinates not found for {agent_id} in {mode} mode")
                return None
        except Exception as e:
            self.logger.error(f"Error getting coordinates for {agent_id}: {e}")
            return None


async def main():
    """Main integrated coordination function"""
    print("🚀 INTEGRATED AGENT COORDINATOR")
    print("=" * 60)
    print("🎯 Combining PyAutoGUI + Message Queue coordination")
    print("🚀 Initializing integrated system...")
    
    # Check for election mode flags
    import sys
    election_mode = "--election" in sys.argv
    round_robin = "--round-robin" in sys.argv
    
    if election_mode:
        print("🗳️ ELECTION MODE ENABLED")
    if round_robin:
        print("🔄 ROUND-ROBIN MODE ENABLED")
    
    # Create integrated coordinator
    coordinator = IntegratedAgentCoordinator(election_mode=election_mode, round_robin=round_robin)
    
    print(f"✅ Integrated coordinator initialized")
    print(f"🎯 Agent mapping: {len(coordinator.agent_mapping)} agents")
    print(f"📋 Message queue: {len(coordinator.message_queue_manager.agent_registry)} agents registered")
    
    try:
        # Run continuous coordination using hybrid approach
        print("\n🚀 Starting integrated hybrid coordination...")
        await coordinator.run_continuous_coordination_hybrid(cycles=3, interval=60)
        
        # Generate and send final status report
        print("\n📊 Generating integrated status report...")
        await coordinator.send_integrated_status_report_to_discord()
        
        print("\n🎉 Integrated mission completed successfully!")
        
    except KeyboardInterrupt:
        print("\n⏹️ Operation interrupted by user")
        await coordinator.send_integrated_status_report_to_discord()
    except Exception as e:
        print(f"\n❌ Operation error: {e}")
        if DISCORD_AVAILABLE:
            await ping_discord_error("Agent-5", "Integrated system error", str(e))


if __name__ == "__main__":
    print("🚀 Starting Integrated Agent Coordinator...")
    print("🎯 Ready to coordinate using PyAutoGUI + Message Queue hybrid system")
    print("=" * 60)
    
    # Run coordination
    asyncio.run(main())
