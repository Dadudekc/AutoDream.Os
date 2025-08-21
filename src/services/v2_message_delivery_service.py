#!/usr/bin/env python3
"""
V2 Message Delivery Service
Actually delivers messages to agent input coordinates using V2 integration
"""

import logging
import json
import time
import threading
from typing import Dict, Any, Optional, List
from pathlib import Path
from datetime import datetime
import queue

# Import PyAutoGUI for actual message delivery
try:
    import pyautogui
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.5
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False
    logging.warning("⚠️ PyAutoGUI not available - message delivery will be simulated")

# Optional clipboard library for paste-based delivery
try:
    import pyperclip  # type: ignore
    PYPERCLIP_AVAILABLE = True
except Exception:
    PYPERCLIP_AVAILABLE = False

logger = logging.getLogger(__name__)

class V2MessageDeliveryService:
    """
    V2 Message Delivery Service
    Actually delivers messages to agent input coordinates
    """
    
    def __init__(self):
        self.agent_coordinates = {}
        self.message_queue = queue.Queue()
        self.delivery_status = {}
        self.delivery_thread = None
        
        # Initialize agent coordinates (these would normally come from V2 system)
        self._initialize_agent_coordinates()
        
        # Start message delivery thread
        self._start_delivery_thread()
    
    def _initialize_agent_coordinates(self):
        """Initialize agent input coordinates"""
        try:
            logger.info("📍 Initializing agent input coordinates...")
            
            # Load real agent coordinates from the V2 system
            try:
                # Try to load from the actual coordinate files
                import json
                import os

                repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

                # Preferred sources (in order): cursor_agent_coords.json (repo config), cursor_agent_coords.json (runtime), agent_complete_locations.json
                cursor_repo_path = os.path.join(repo_root, "Agent_Cellphone_V2_Repository", "config", "cursor_agent_coords.json")
                cursor_runtime_path = os.path.join(repo_root, "runtime", "agent_comms", "cursor_agent_coords.json")
                v2_locations_path = os.path.join(repo_root, "agent_complete_locations.json")

                def _load_cursor_coords(path: str) -> bool:
                    if os.path.exists(path):
                        with open(path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        layout = data.get("8-agent") or data.get("5-agent") or {}
                        if not layout:
                            return False
                        self.agent_coordinates = {}
                        for i in range(1, 9):
                            key = f"Agent-{i}"
                            info = layout.get(key)
                            if not info:
                                continue
                            box = info.get("input_box") or {}
                            input_x = box.get("x")
                            input_y = box.get("y")
                            if input_x is None or input_y is None:
                                continue
                            normalized_id = f"agent_{i}"
                            self.agent_coordinates[normalized_id] = {
                                'input_x': int(input_x),
                                'input_y': int(input_y),
                                'status': 'active',
                                'last_delivery': time.time(),
                                'name': key,
                                'color': ''
                            }
                        if self.agent_coordinates:
                            logger.info(f"✅ Loaded agent coordinates from cursor coords: {path}")
                            return True
                    return False

                def _load_v2_locations(path: str) -> bool:
                    if os.path.exists(path):
                        with open(path, 'r', encoding='utf-8') as f:
                            agent_locations = json.load(f)
                        self.agent_coordinates = {}
                        for agent_id, agent_info in agent_locations.items():
                            normalized_id = agent_id.lower().replace('-', '_')
                            input_x, input_y = agent_info['input_location']
                            self.agent_coordinates[normalized_id] = {
                                'input_x': int(input_x),
                                'input_y': int(input_y),
                                'status': 'active',
                                'last_delivery': time.time(),
                                'name': agent_info.get('name', agent_id),
                                'color': agent_info.get('color', '')
                            }
                        if self.agent_coordinates:
                            logger.info(f"✅ Loaded agent coordinates from V2 locations: {path}")
                            return True
                    return False

                loaded = (
                    _load_cursor_coords(cursor_repo_path) or
                    _load_cursor_coords(cursor_runtime_path) or
                    _load_v2_locations(v2_locations_path)
                )

                if not loaded:
                    logger.warning("⚠️ No coordinate sources found, using placeholder coordinates")
                    self._initialize_placeholder_coordinates()
                    
            except Exception as e:
                logger.warning(f"⚠️ Error loading V2 coordinates: {e}, using placeholder coordinates")
                self._initialize_placeholder_coordinates()
            
            logger.info(f"✅ Agent coordinates initialized for {len(self.agent_coordinates)} agents")
            
        except Exception as e:
            logger.error(f"❌ Error initializing agent coordinates: {e}")
            raise
    
    def _initialize_placeholder_coordinates(self):
        """Initialize placeholder coordinates as fallback"""
        self.agent_coordinates = {
            'agent_1': {
                'input_x': 500,
                'input_y': 300,
                'status': 'active',
                'last_delivery': time.time(),
                'name': 'Foundation & Testing',
                'color': '🟢'
            },
            'agent_2': {
                'input_x': 600,
                'input_y': 300,
                'status': 'active',
                'last_delivery': time.time(),
                'name': 'AI & ML Integration',
                'color': '🔵'
            },
            'agent_3': {
                'input_x': 700,
                'input_y': 300,
                'status': 'active',
                'last_delivery': time.time(),
                'name': 'Multimedia & Content',
                'color': '🟡'
            },
            'agent_4': {
                'input_x': 800,
                'input_y': 300,
                'status': 'active',
                'last_delivery': time.time(),
                'name': 'Security & Infrastructure',
                'color': '🔴'
            },
            'agent_5': {
                'input_x': 500,
                'input_y': 400,
                'status': 'active',
                'last_delivery': time.time(),
                'name': 'Business Intelligence',
                'color': '🟣'
            },
            'agent_6': {
                'input_x': 600,
                'input_y': 400,
                'status': 'active',
                'last_delivery': time.time(),
                'name': 'Gaming & Entertainment',
                'color': '⚪'
            },
            'agent_7': {
                'input_x': 700,
                'input_y': 400,
                'status': 'active',
                'last_delivery': time.time(),
                'name': 'Web Development',
                'color': '⚫'
            },
            'agent_8': {
                'input_x': 800,
                'input_y': 400,
                'status': 'active',
                'last_delivery': time.time(),
                'name': 'Integration & Performance',
                'color': '⚪'
            }
        }
    
    def _start_delivery_thread(self):
        """Start the message delivery thread"""
        try:
            logger.info("📤 Starting message delivery thread...")
            
            self.delivery_thread = threading.Thread(
                target=self._message_delivery_loop,
                daemon=True
            )
            self.delivery_thread.start()
            
            logger.info("✅ Message delivery thread started")
            
        except Exception as e:
            logger.error(f"❌ Error starting delivery thread: {e}")
            raise
    
    def _message_delivery_loop(self):
        """Main message delivery loop"""
        while True:
            try:
                # Process messages from queue
                if not self.message_queue.empty():
                    message_data = self.message_queue.get_nowait()
                    self._deliver_message(message_data)
                else:
                    # Sleep if no messages
                    time.sleep(0.1)
                    
            except Exception as e:
                logger.error(f"❌ Error in message delivery loop: {e}")
                time.sleep(1)  # Wait longer on error
    
    def _deliver_message(self, message_data: Dict[str, Any]):
        """Deliver a message to an agent"""
        try:
            agent_id = message_data.get('agent_id')
            message_type = message_data.get('type', 'unknown')
            message_content = message_data.get('content', '')
            
            if not agent_id or agent_id not in self.agent_coordinates:
                logger.warning(f"⚠️ Invalid agent ID: {agent_id}")
                return
            
            agent_coords = self.agent_coordinates[agent_id]
            
            if agent_coords['status'] != 'active':
                logger.warning(f"⚠️ Agent {agent_id} is not active")
                return
            
            logger.info(f"📤 Delivering {message_type} message to {agent_id} at ({agent_coords['input_x']}, {agent_coords['input_y']})")
            
            # Format message for delivery
            formatted_message = self._format_message_for_delivery(message_type, message_content, message_data)
            
            # Actually deliver the message using PyAutoGUI
            if PYAUTOGUI_AVAILABLE:
                success = self._deliver_via_pyautogui(agent_coords, formatted_message)
            else:
                success = self._simulate_delivery(agent_coords, formatted_message)
            
            if success:
                # Update delivery status with proper tracking
                current_time = time.time()
                agent_coords['last_delivery'] = current_time
                
                # Initialize delivery status for this agent if it doesn't exist
                if agent_id not in self.delivery_status:
                    self.delivery_status[agent_id] = {
                        'delivery_count': 0,
                        'successful_deliveries': 0,
                        'failed_deliveries': 0,
                        'last_message_type': None,
                        'last_delivery_time': None,
                        'last_success_time': None,
                        'last_failure_time': None
                    }
                
                # Update delivery status
                self.delivery_status[agent_id].update({
                    'last_message_type': message_type,
                    'last_delivery_time': current_time,
                    'last_success_time': current_time,
                    'delivery_count': self.delivery_status[agent_id]['delivery_count'] + 1,
                    'successful_deliveries': self.delivery_status[agent_id]['successful_deliveries'] + 1
                })
                
                logger.info(f"✅ Message delivered successfully to {agent_id}")
            else:
                # Track failed delivery
                current_time = time.time()
                if agent_id not in self.delivery_status:
                    self.delivery_status[agent_id] = {
                        'delivery_count': 0,
                        'successful_deliveries': 0,
                        'failed_deliveries': 0,
                        'last_message_type': None,
                        'last_delivery_time': None,
                        'last_success_time': None,
                        'last_failure_time': None
                    }
                
                self.delivery_status[agent_id].update({
                    'last_message_type': message_type,
                    'last_delivery_time': current_time,
                    'last_failure_time': current_time,
                    'delivery_count': self.delivery_status[agent_id]['delivery_count'] + 1,
                    'failed_deliveries': self.delivery_status[agent_id]['failed_deliveries'] + 1
                })
                
                logger.error(f"❌ Failed to deliver message to {agent_id}")
                
        except Exception as e:
            logger.error(f"❌ Error delivering message: {e}")
            # Track error in delivery status
            if agent_id in self.agent_coordinates:
                current_time = time.time()
                if agent_id not in self.delivery_status:
                    self.delivery_status[agent_id] = {
                        'delivery_count': 0,
                        'successful_deliveries': 0,
                        'failed_deliveries': 0,
                        'last_message_type': None,
                        'last_delivery_time': None,
                        'last_success_time': None,
                        'last_failure_time': None
                    }
                
                self.delivery_status[agent_id].update({
                    'last_message_type': message_type,
                    'last_delivery_time': current_time,
                    'last_failure_time': current_time,
                    'delivery_count': self.delivery_status[agent_id]['delivery_count'] + 1,
                    'failed_deliveries': self.delivery_status[agent_id]['failed_deliveries'] + 1
                })
    
    def _format_message_for_delivery(self, message_type: str, message_content: str, message_data: Dict[str, Any]) -> str:
        """Format message for delivery to agent"""
        try:
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            if message_type == 'task_assigned':
                return f"[{timestamp}] 📋 TASK ASSIGNED: {message_data.get('title', 'Unknown Task')}\n\n{message_data.get('description', 'No description')}\n\nPriority: {message_data.get('priority', 'Normal').upper()}\n\nPlease acknowledge receipt."
            
            elif message_type == 'task_progress_update':
                return f"[{timestamp}] 📈 PROGRESS UPDATE: {message_data.get('task_title', 'Unknown Task')}\n\nProgress: {message_data.get('old_progress', 0)}% → {message_data.get('new_progress', 0)}%\nStatus: {message_data.get('status', 'Unknown')}\n\nPlease update your progress tracking."
            
            elif message_type == 'collaboration_session_started':
                return f"[{timestamp}] 🤝 COLLABORATION SESSION: {message_data.get('title', 'Unknown Session')}\n\nObjective: {message_data.get('objective', 'No objective')}\n\nSession ID: {message_data.get('session_id', 'Unknown')}\n\nPlease join the session."
            
            elif message_type == 'presidential_decision_proposed':
                return f"[{timestamp}] 🏛️ PRESIDENTIAL DECISION: {message_data.get('title', 'Unknown Decision')}\n\n{message_data.get('description', 'No description')}\n\nPresident: {message_data.get('president', 'Unknown')}\n\nPlease review and provide feedback."
            
            elif message_type == 'significant_progress':
                return f"[{timestamp}] 🎯 SIGNIFICANT PROGRESS: {message_data.get('task_title', 'Unknown Task')}\n\nProgress: {message_data.get('progress', 0)}% complete\n\nThis is a major milestone! Please coordinate with team members."
            
            elif message_type == 'task_completed':
                return f"[{timestamp}] 🎉 TASK COMPLETED: {message_data.get('task_title', 'Unknown Task')}\n\nCongratulations! Task has been marked as complete.\n\nAssigned Agents: {', '.join(message_data.get('assigned_agents', []))}\n\nPlease update your records."
            
            elif message_type == 'multimedia_update':
                return f"[{timestamp}] 🎬 MULTIMEDIA UPDATE: {message_data.get('message', 'No message')}\n\nMultimedia services are now available.\n\nPlease test your multimedia capabilities."
            
            else:
                # Generic message format
                return f"[{timestamp}] {message_type.upper()}: {message_content}"
                
        except Exception as e:
            logger.error(f"❌ Error formatting message: {e}")
            return f"Message delivery error: {str(e)}"
    
    def _deliver_via_pyautogui(self, agent_coords: Dict[str, Any], message: str) -> bool:
        """Actually deliver message using PyAutoGUI"""
        try:
            input_x = agent_coords['input_x']
            input_y = agent_coords['input_y']
            
            # Move to agent input coordinates
            pyautogui.moveTo(input_x, input_y, duration=0.5)
            time.sleep(0.2)
            
            # Click to focus the input area
            pyautogui.click(input_x, input_y)
            time.sleep(0.2)
            
            # Clear any existing text (Ctrl+A, Delete)
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.1)
            pyautogui.press('delete')
            time.sleep(0.1)
            
            # Keystroke typing with Shift+Enter for line breaks (more reliable in some setups)
            lines = message.split('\n')
            for i, line in enumerate(lines):
                content = line if line is not None else ""
                pyautogui.write(content)
                if i < len(lines) - 1:
                    pyautogui.hotkey('shift', 'enter')
                    time.sleep(0.1)
            
            time.sleep(0.2)
            
            # Press Enter to send the message
            pyautogui.press('enter')
            time.sleep(0.5)  # Wait for message to be processed
            
            logger.info(f"✅ Message delivered via PyAutoGUI to ({input_x}, {input_y})")
            return True
            
        except Exception as e:
            logger.error(f"❌ PyAutoGUI delivery failed: {e}")
            return False
    
    def _simulate_delivery(self, agent_coords: Dict[str, Any], message: str) -> bool:
        """Simulate message delivery when PyAutoGUI is not available"""
        try:
            logger.info(f"🎭 SIMULATED DELIVERY to {agent_coords['input_x']}, {agent_coords['input_y']}: {message[:100]}...")
            time.sleep(0.5)  # Simulate delivery time
            return True
            
        except Exception as e:
            logger.error(f"❌ Simulated delivery failed: {e}")
            return False
    
    def send_message(self, agent_id: str, message_type: str, content: str = "", **kwargs) -> bool:
        """Send a message to a specific agent"""
        try:
            message_data = {
                'agent_id': agent_id,
                'type': message_type,
                'content': content,
                'timestamp': time.time(),
                **kwargs
            }
            
            # Add message to delivery queue
            self.message_queue.put(message_data)
            
            logger.info(f"📤 Message queued for delivery to {agent_id}: {message_type}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error queuing message: {e}")
            return False
    
    def send_message_sync(self, agent_id: str, message_type: str, content: str = "", **kwargs) -> bool:
        """Send a message to a specific agent synchronously (for testing)"""
        try:
            message_data = {
                'agent_id': agent_id,
                'type': message_type,
                'content': content,
                'timestamp': time.time(),
                **kwargs
            }
            
            # Deliver message immediately (bypassing queue)
            logger.info(f"📤 Sending message synchronously to {agent_id}: {message_type}")
            self._deliver_message(message_data)
            return True
            
        except Exception as e:
            logger.error(f"❌ Error sending message synchronously: {e}")
            return False
    
    def broadcast_message(self, message_type: str, content: str = "", target_agents: List[str] = None, **kwargs) -> Dict[str, bool]:
        """Broadcast a message to multiple agents"""
        try:
            if target_agents is None:
                target_agents = list(self.agent_coordinates.keys())
            
            results = {}
            
            for agent_id in target_agents:
                success = self.send_message(agent_id, message_type, content, **kwargs)
                results[agent_id] = success
            
            logger.info(f"📢 Broadcast message sent to {len(target_agents)} agents")
            return results
            
        except Exception as e:
            logger.error(f"❌ Error broadcasting message: {e}")
            return {}
    
    def update_agent_coordinates(self, agent_id: str, input_x: int, input_y: int) -> bool:
        """Update agent input coordinates"""
        try:
            if agent_id in self.agent_coordinates:
                self.agent_coordinates[agent_id]['input_x'] = input_x
                self.agent_coordinates[agent_id]['input_y'] = input_y
                logger.info(f"📍 Updated coordinates for {agent_id}: ({input_x}, {input_y})")
                return True
            else:
                logger.warning(f"⚠️ Agent {agent_id} not found in coordinates")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error updating coordinates: {e}")
            return False
    
    def get_delivery_status(self) -> Dict[str, Any]:
        """Get message delivery status"""
        try:
            return {
                'delivery_status': self.delivery_status,
                'agent_coordinates': self.agent_coordinates,
                'queue_size': self.message_queue.qsize(),
                'pyautogui_available': PYAUTOGUI_AVAILABLE,
                'timestamp': time.time()
            }
            
        except Exception as e:
            logger.error(f"❌ Error getting delivery status: {e}")
            return {'error': str(e)}

# CLI interface for testing
def main():
    """CLI interface for V2 Message Delivery Service"""
    import argparse
    
    parser = argparse.ArgumentParser(description='V2 Message Delivery Service')
    parser.add_argument('--status', action='store_true', help='Show delivery status')
    parser.add_argument('--send', nargs=3, metavar=('AGENT', 'TYPE', 'MESSAGE'), 
                       help='Send message to agent (agent type message)')
    parser.add_argument('--send-file', nargs=3, metavar=('AGENT', 'TYPE', 'FILEPATH'), 
                       help='Send message to agent from file (agent type file)')
    parser.add_argument('--broadcast', nargs=2, metavar=('TYPE', 'MESSAGE'), 
                       help='Broadcast message to all agents (type message)')
    parser.add_argument('--broadcast-file', nargs=2, metavar=('TYPE', 'FILEPATH'), 
                       help='Broadcast message to all agents from file (type file)')
    parser.add_argument('--broadcast-sync', nargs=2, metavar=('TYPE', 'MESSAGE'),
                       help='Broadcast message synchronously to all agents (type message)')
    parser.add_argument('--broadcast-file-sync', nargs=2, metavar=('TYPE', 'FILEPATH'), 
                       help='Broadcast message synchronously to all agents from file (type file)')
    parser.add_argument('--update-coords', nargs=3, metavar=('AGENT', 'X', 'Y'), 
                       help='Update agent coordinates (agent x y)')
    parser.add_argument('--test', action='store_true', help='Test message delivery')
    parser.add_argument('--agents', action='store_true', help='List all available agents')
    parser.add_argument('--ping', nargs=1, metavar='AGENT', help='Send ping message to specific agent')
    parser.add_argument('--ping-all', action='store_true', help='Send ping to all agents')
    parser.add_argument('--coordinate', nargs=2, metavar=('AGENTS', 'MESSAGE'), 
                       help='Send coordination message to specific agents (comma-separated list)')
    parser.add_argument('--emergency', nargs=1, metavar='MESSAGE', help='Send emergency broadcast to all agents')
    parser.add_argument('--send-sync', nargs=3, metavar=('AGENT', 'TYPE', 'MESSAGE'), 
                       help='Send message to agent synchronously (agent type message)')
    parser.add_argument('--test-sync', action='store_true', help='Test synchronous message delivery')
    
    args = parser.parse_args()
    
    try:
        delivery_service = V2MessageDeliveryService()
        
        if args.status:
            status = delivery_service.get_delivery_status()
            print("📊 V2 MESSAGE DELIVERY SERVICE STATUS")
            print("=" * 50)
            
            # Agent status summary
            print(f"\n🤖 AGENT STATUS ({len(status['agent_coordinates'])} agents)")
            print("-" * 40)
            for agent_id, agent_info in status['agent_coordinates'].items():
                status_icon = "🟢" if agent_info['status'] == 'active' else "🔴"
                last_delivery = time.strftime("%H:%M:%S", time.localtime(agent_info['last_delivery']))
                print(f"{status_icon} {agent_id}: {agent_info['name']} at ({agent_info['input_x']}, {agent_info['input_y']}) - Last: {last_delivery}")
            
            # Delivery statistics
            print(f"\n📈 DELIVERY STATISTICS")
            print("-" * 40)
            
            # Fix the statistics calculation
            total_deliveries = 0
            total_success = 0
            total_failures = 0
            
            for agent_status in status['delivery_status'].values():
                total_deliveries += agent_status.get('delivery_count', 0)
                total_success += agent_status.get('successful_deliveries', 0)
                total_failures += agent_status.get('failed_deliveries', 0)
            
            print(f"Total Messages: {total_deliveries}")
            print(f"Successful: {total_success}")
            print(f"Failed: {total_failures}")
            print(f"Success Rate: {(total_success/total_deliveries*100):.1f}%" if total_deliveries > 0 else "Success Rate: N/A")
            
            # Show individual agent delivery status
            if status['delivery_status']:
                print(f"\n📊 INDIVIDUAL AGENT DELIVERY STATUS")
                print("-" * 40)
                for agent_id, agent_status in status['delivery_status'].items():
                    print(f"{agent_id}: {agent_status.get('delivery_count', 0)} messages, "
                          f"{agent_status.get('successful_deliveries', 0)} success, "
                          f"{agent_status.get('failed_deliveries', 0)} failed")
            
            # System status
            print(f"\n⚙️ SYSTEM STATUS")
            print("-" * 40)
            print(f"PyAutoGUI Available: {'✅ Yes' if status['pyautogui_available'] else '❌ No'}")
            print(f"Queue Size: {status['queue_size']}")
            print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(status['timestamp']))}")
            
        elif args.agents:
            print("🤖 AVAILABLE AGENTS")
            print("=" * 50)
            status = delivery_service.get_delivery_status()
            for agent_id, agent_info in status['agent_coordinates'].items():
                status_icon = "🟢" if agent_info['status'] == 'active' else "🔴"
                print(f"{status_icon} {agent_id}: {agent_info['name']}")
                print(f"   Coordinates: ({agent_info['input_x']}, {agent_info['input_y']})")
                print(f"   Status: {agent_info['status']}")
                print()
            
        elif args.ping:
            agent_id = args.ping[0]
            success = delivery_service.send_message(agent_id, 'ping', 'Ping message - please acknowledge receipt')
            print(f"{'✅' if success else '❌'} Ping {'sent' if success else 'failed'} to {agent_id}")
            
        elif args.ping_all:
            print("📡 Pinging all agents...")
            results = delivery_service.broadcast_message('ping', 'System ping - all agents please acknowledge')
            success_count = sum(1 for success in results.values() if success)
            print(f"📊 Ping results: {success_count}/{len(results)} agents responded")
            for agent_id, success in results.items():
                status_icon = "✅" if success else "❌"
                print(f"{status_icon} {agent_id}")
            
        elif args.coordinate:
            agents_str, message = args.coordinate
            target_agents = [agent.strip() for agent in agents_str.split(',')]
            print(f"🤝 Coordinating with agents: {', '.join(target_agents)}")
            results = delivery_service.broadcast_message('coordination', message, target_agents)
            success_count = sum(1 for success in results.values() if success)
            print(f"📊 Coordination results: {success_count}/{len(target_agents)} agents received")
            
        elif args.emergency:
            message = args.emergency[0]
            print("🚨 Sending emergency broadcast...")
            results = delivery_service.broadcast_message('emergency', f"EMERGENCY: {message}")
            success_count = sum(1 for success in results.values() if success)
            print(f"🚨 Emergency broadcast sent to {success_count}/8 agents")
            
        elif args.send:
            agent_id, message_type, message = args.send
            success = delivery_service.send_message(agent_id, message_type, message)
            print(f"{'✅' if success else '❌'} Message {'sent' if success else 'failed'} to {agent_id}")
        elif args.send_file:
            agent_id, message_type, filepath = args.send_file
            try:
                with open(filepath, 'rb') as f:
                    raw = f.read()
                content = None
                for enc in ('utf-8-sig', 'cp1252', 'latin-1'):
                    try:
                        content = raw.decode(enc)
                        break
                    except Exception:
                        continue
                if content is None:
                    raise UnicodeDecodeError('unknown', raw, 0, 1, 'cannot decode')
                success = delivery_service.send_message(agent_id, message_type, content)
                print(f"{'✅' if success else '❌'} File message {'sent' if success else 'failed'} to {agent_id}")
            except Exception as e:
                print(f"❌ Error reading file: {e}")
            
        elif args.send_sync:
            agent_id, message_type, message = args.send_sync
            success = delivery_service.send_message_sync(agent_id, message_type, message)
            print(f"{'✅' if success else '❌'} Synchronous message {'sent' if success else 'failed'} to {agent_id}")
            
        elif args.broadcast:
            message_type, message = args.broadcast
            results = delivery_service.broadcast_message(message_type, message)
            success_count = sum(1 for success in results.values() if success)
            print(f"📢 Broadcast sent to {success_count}/8 agents")
            print(f"Results: {results}")
        elif args.broadcast_sync:
            message_type, message = args.broadcast_sync
            agents = list(delivery_service.agent_coordinates.keys())
            results = {}
            for agent_id in agents:
                ok = delivery_service.send_message_sync(agent_id, message_type, message)
                results[agent_id] = ok
                time.sleep(0.2)
            success_count = sum(1 for success in results.values() if success)
            print(f"📢 Broadcast (sync) sent to {success_count}/{len(results)} agents")
            print(f"Results: {results}")
        elif args.broadcast_file:
            message_type, filepath = args.broadcast_file
            try:
                with open(filepath, 'rb') as f:
                    raw = f.read()
                content = None
                for enc in ('utf-8-sig', 'cp1252', 'latin-1'):
                    try:
                        content = raw.decode(enc)
                        break
                    except Exception:
                        continue
                if content is None:
                    raise UnicodeDecodeError('unknown', raw, 0, 1, 'cannot decode')
                results = delivery_service.broadcast_message(message_type, content)
                success_count = sum(1 for success in results.values() if success)
                print(f"📢 Broadcast sent to {success_count}/8 agents")
                print(f"Results: {results}")
            except Exception as e:
                print(f"❌ Error reading file: {e}")
        elif args.broadcast_file_sync:
            message_type, filepath = args.broadcast_file_sync
            try:
                with open(filepath, 'rb') as f:
                    raw = f.read()
                content = None
                for enc in ('utf-8-sig', 'cp1252', 'latin-1'):
                    try:
                        content = raw.decode(enc)
                        break
                    except Exception:
                        continue
                if content is None:
                    raise UnicodeDecodeError('unknown', raw, 0, 1, 'cannot decode')
                agents = list(delivery_service.agent_coordinates.keys())
                results = {}
                for agent_id in agents:
                    ok = delivery_service.send_message_sync(agent_id, message_type, content)
                    results[agent_id] = ok
                    time.sleep(0.2)
                success_count = sum(1 for success in results.values() if success)
                print(f"📢 Broadcast (sync) sent to {success_count}/{len(results)} agents")
                print(f"Results: {results}")
            except Exception as e:
                print(f"❌ Error reading file: {e}")
            
        elif args.update_coords:
            agent_id, x, y = args.update_coords
            success = delivery_service.update_agent_coordinates(agent_id, int(x), int(y))
            print(f"{'✅' if success else '❌'} Coordinates {'updated' if success else 'failed'} for {agent_id}")
            
        elif args.test:
            print("🧪 Testing message delivery...")
            
            # Test individual message
            delivery_service.send_message('agent_1', 'test', 'This is a test message')
            time.sleep(1)
            
            # Test broadcast
            delivery_service.broadcast_message('test_broadcast', 'This is a test broadcast')
            time.sleep(1)
            
            # Show status
            status = delivery_service.get_delivery_status()
            print(json.dumps(status, indent=2, default=str))
            
        elif args.test_sync:
            print("🧪 Testing synchronous message delivery...")
            delivery_service.send_message_sync('agent_1', 'test_sync', 'This is a synchronous test message')
            time.sleep(1)
            status = delivery_service.get_delivery_status()
            print(json.dumps(status, indent=2, default=str))
            
        else:
            print("📤 V2 Message Delivery Service - Enhanced CLI")
            print("=" * 50)
            print("Available commands:")
            print("  --status          Show detailed delivery status")
            print("  --agents          List all available agents")
            print("  --send AGENT TYPE MESSAGE             Send message to specific agent")
            print("  --send-file AGENT TYPE FILE           Send file content to agent")
            print("  --broadcast TYPE MESSAGE              Broadcast to all agents")
            print("  --broadcast-file TYPE FILE            Broadcast file content to all agents")
            print("  --broadcast-sync TYPE MESSAGE         Broadcast synchronously to all agents")
            print("  --broadcast-file-sync TYPE FILE       Broadcast file content synchronously to all agents")
            print("  --ping AGENT      Send ping to specific agent")
            print("  --ping-all        Send ping to all agents")
            print("  --coordinate AGENTS MESSAGE  Coordinate with specific agents")
            print("  --emergency MESSAGE          Emergency broadcast")
            print("  --update-coords AGENT X Y    Update agent coordinates")
            print("  --test           Test message delivery")
            print("  --test-sync      Test synchronous message delivery")
            print("\nExamples:")
            print("  python v2_message_delivery_service.py --ping agent_1")
            print("  python v2_message_delivery_service.py --coordinate 'agent_1,agent_3' 'Coordinate multimedia integration'")
            print("  python v2_message_delivery_service.py --emergency 'System maintenance required'")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())
