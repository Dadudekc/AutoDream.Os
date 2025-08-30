#!/usr/bin/env python3
"""
Unified Messaging Service - Agent Cellphone V2
==============================================

Main orchestrator for all messaging capabilities.
Single responsibility: Orchestrate messaging modules.
Follows V2 standards: OOP, SRP, clean production-grade code.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import logging

from src.utils.stability_improvements import safe_import  # stability_manager removed due to abstract class issues
from typing import Dict, Any, Optional, Union, List, Tuple

from .interfaces import (
    MessagingMode, MessageType, IMessageSender, IBulkMessaging,
    ICampaignMessaging, IYOLOMessaging, ICoordinateManager
)
from .coordinate_manager import CoordinateManager
from .unified_pyautogui_messaging import UnifiedPyAutoGUIMessaging
from .campaign_messaging import CampaignMessaging
from .yolo_messaging import YOLOMessaging
from .models.unified_message import UnifiedMessagePriority
from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from queue import Queue, PriorityQueue
import threading
import time

logger = logging.getLogger(__name__)


class AgentStatus(Enum):
    """Agent status states"""
    IDLE = "idle"
    WORKING = "working"
    WAITING = "waiting"
    COMPLETED = "completed"
    ERROR = "error"


@dataclass
class QueuedMessage:
    """Message in the queue"""
    priority: UnifiedMessagePriority
    timestamp: float
    agent_id: str
    message: str
    message_type: str
    requires_response: bool
    response_timeout: float = 30.0  # seconds


@dataclass
class AgentState:
    """Current state of an agent"""
    status: AgentStatus
    current_task: Optional[str]
    last_activity: float
    response_count: int
    compliance_score: float = 1.0


class UnifiedMessagingService:
    """
    Unified Messaging Service - Single responsibility: Orchestrate messaging modules
    
    This class only handles:
    - Coordinating between messaging modules
    - Providing unified interface
    - Mode selection and routing
    """
    
    def __init__(self, coordinates_file: str = "runtime/agent_comms/cursor_agent_coords.json"):
        """Initialize the unified messaging service with all modules"""
        # Initialize core modules
        self.coordinate_manager = CoordinateManager(coordinates_file)
        self.pyautogui_messaging = UnifiedPyAutoGUIMessaging(self.coordinate_manager)
        self.campaign_messaging = CampaignMessaging(self.coordinate_manager, self.pyautogui_messaging)
        self.yolo_messaging = YOLOMessaging(self.coordinate_manager, self.pyautogui_messaging)
        
        # Initialize message queue system (consolidated into unified service)
        self.message_queue = PriorityQueue()
        self.agent_states: Dict[str, AgentState] = {}
        self.response_queue = Queue()
        self.coordination_lock = threading.Lock()
        self.system_active = True
        
        # Initialize agent states
        for i in range(1, 9):
            agent_id = f"Agent-{i}"
            self.agent_states[agent_id] = AgentState(
                status=AgentStatus.IDLE,
                current_task=None,
                last_activity=time.time(),
                response_count=0
            )
        
        # Start coordination thread
        self.coordination_thread = threading.Thread(target=self._coordination_loop, daemon=True)
        self.coordination_thread.start()
        
        # Set default mode
        self.active_mode = MessagingMode.PYAUTOGUI
        
        logger.info("Unified Messaging Service initialized with all modules including message queue system")
    
    def set_mode(self, mode: MessagingMode):
        """Set the active messaging mode"""
        self.active_mode = mode
        logger.info(f"Messaging mode set to: {mode.value}")
    
    # Message Queue System Methods (consolidated from message_queue_system.py)
    
    def queue_message(self, agent_id: str, message: str, message_type: str = "text", 
                     priority: UnifiedMessagePriority = UnifiedMessagePriority.NORMAL, 
                     requires_response: bool = True) -> bool:
        """Queue a message for an agent"""
        try:
            queued_msg = QueuedMessage(
                priority=priority,
                timestamp=time.time(),
                agent_id=agent_id,
                message=message,
                message_type=message_type,
                requires_response=requires_response
            )
            
            # Add to priority queue (priority is negative for correct ordering)
            self.message_queue.put((-priority.value, queued_msg))
            logger.info(f"Message queued for {agent_id} with priority {priority.value}")
            return True
            
        except Exception as e:
            logger.error(f"Error queuing message for {agent_id}: {e}")
            return False
    
    def update_agent_state(self, agent_id: str, status: AgentStatus, task: str = None) -> None:
        """Update agent state"""
        with self.coordination_lock:
            if agent_id in self.agent_states:
                self.agent_states[agent_id].status = status
                self.agent_states[agent_id].current_task = task
                self.agent_states[agent_id].last_activity = time.time()
                
                if status == AgentStatus.COMPLETED:
                    self.agent_states[agent_id].response_count += 1
                    self.agent_states[agent_id].compliance_score = min(1.0, 
                        self.agent_states[agent_id].compliance_score + 0.1)
                
                logger.info(f"Agent {agent_id} state updated: {status.value}")
    
    def record_response(self, agent_id: str, response: str) -> None:
        """Record agent response"""
        with self.coordination_lock:
            if agent_id in self.agent_states:
                self.agent_states[agent_id].last_activity = time.time()
                self.agent_states[agent_id].response_count += 1
                self.agent_states[agent_id].compliance_score = min(1.0, 
                    self.agent_states[agent_id].compliance_score + 0.05)
                
                # Add to response queue for processing
                self.response_queue.put((agent_id, response, time.time()))
                
                logger.info(f"Response recorded from {agent_id}")
    
    def get_agent_status(self, agent_id: str) -> Optional[AgentState]:
        """Get current status of an agent"""
        return self.agent_states.get(agent_id)
    
    def get_all_agent_statuses(self) -> Dict[str, AgentState]:
        """Get status of all agents"""
        return self.agent_states.copy()
    
    def check_keyboard_conflicts(self) -> List[str]:
        """Check for potential keyboard conflicts between agents"""
        conflicts = []
        working_agents = []
        
        with self.coordination_lock:
            for agent_id, state in self.agent_states.items():
                if state.status == AgentStatus.WORKING:
                    working_agents.append(agent_id)
            
            # If more than 1 agent is working, potential conflict
            if len(working_agents) > 1:
                conflicts = working_agents
                logger.warning(f"Keyboard conflict detected: {conflicts}")
        
        return conflicts
    
    def enforce_agent_priority(self) -> None:
        """Enforce agent priority to prevent conflicts"""
        with self.coordination_lock:
            # Only allow 1 agent to work at a time
            working_count = sum(1 for state in self.agent_states.values() 
                              if state.status == AgentStatus.WORKING)
            
            if working_count > 1:
                # Force all but highest priority agent to wait
                highest_priority = None
                for agent_id, state in self.agent_states.items():
                    if state.status == AgentStatus.WORKING:
                        if highest_priority is None or state.compliance_score > self.agent_states[highest_priority].compliance_score:
                            highest_priority = agent_id
                
                for agent_id, state in self.agent_states.items():
                    if state.status == AgentStatus.WORKING and agent_id != highest_priority:
                        state.status = AgentStatus.WAITING
                        logger.info(f"Agent {agent_id} forced to wait to prevent keyboard conflict")
    
    def _coordination_loop(self) -> None:
        """Main coordination loop"""
        while self.system_active:
            try:
                # Check for keyboard conflicts
                conflicts = self.check_keyboard_conflicts()
                if conflicts:
                    self.enforce_agent_priority()
                
                # Process response queue
                while not self.response_queue.empty():
                    agent_id, response, timestamp = self.response_queue.get()
                    logger.info(f"Processing response from {agent_id}: {response[:50]}...")
                
                # Sleep to prevent excessive CPU usage
                time.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Error in coordination loop: {e}")
                time.sleep(1.0)
    
    def shutdown(self) -> None:
        """Shutdown the message queue system"""
        self.system_active = False
        logger.info("Message Queue System shutdown")
    
    def send_message(self, recipient: str, message_content: str, 
                    message_type: MessageType = MessageType.TEXT,
                    mode: MessagingMode = None, new_chat: bool = False) -> Union[bool, Dict[str, bool]]:
        """
        Unified message sending interface
        
        Args:
            recipient: Agent to send message to
            message_content: Message content
            message_type: Type of message
            mode: Messaging mode to use
            new_chat: Whether this is a new chat (onboarding) message
        """
        if mode is None:
            mode = self.active_mode
        
        logger.info(f"Sending {message_type.value} message via {mode.value} to {recipient} (new_chat: {new_chat})")
        
        try:
            if mode == MessagingMode.PYAUTOGUI:
                # Check if this is an onboarding message
                is_onboarding = (message_type == MessageType.ONBOARDING_START or new_chat)
                return self.pyautogui_messaging.send_message(recipient, message_content, message_type.value, is_onboarding)
            
            elif mode == MessagingMode.CAMPAIGN:
                return self.campaign_messaging.send_campaign_message(message_content)
            
            elif mode == MessagingMode.YOLO:
                return self.yolo_messaging.activate_yolo_mode(message_content)
            
            else:
                logger.error(f"Unsupported messaging mode: {mode}")
                return False
                
        except Exception as e:
            logger.error(f"Error in unified message sending: {e}")
            return False
    
    def send_campaign_message(self, message_content: str, campaign_type: str = "election") -> Dict[str, bool]:
        """Send campaign message using campaign messaging module"""
        return self.campaign_messaging.send_campaign_message(message_content, campaign_type)
    
    def activate_yolo_mode(self, message_content: str) -> Dict[str, bool]:
        """Activate YOLO mode using YOLO messaging module"""
        return self.yolo_messaging.activate_yolo_mode(message_content)
    
    def send_bulk_messages(self, messages: Dict[str, str], mode: str = "8-agent", message_type: MessageType = MessageType.TEXT, new_chat: bool = False) -> Dict[str, bool]:
        """
        Send bulk messages using PyAutoGUI messaging module
        
        Args:
            messages: Dictionary of agent_id: message_content
            mode: Coordinate mode to use
            message_type: Type of message
            new_chat: Whether these are new chat (onboarding) messages
        """
        return self.pyautogui_messaging.send_bulk_messages(messages, mode, message_type.value, "normal", new_chat)
    
    def validate_coordinates(self) -> Dict[str, Any]:
        """Validate coordinates using coordinate manager"""
        return self.coordinate_manager.validate_coordinates()
    
    def validate_agent_coordinates(self, agent_id: str, mode: str = "8-agent") -> Dict[str, Any]:
        """
        Validate coordinates for a specific agent before sending message
        
        Args:
            agent_id: Agent to validate coordinates for
            mode: Coordinate mode to use
            
        Returns:
            Dict with validation results including 'valid' boolean and 'error' if any
        """
        logger.info(f"🔍 Validating coordinates for {agent_id} in {mode} mode")
        
        try:
            # Get agent coordinates
            coords = self.coordinate_manager.get_agent_coordinates(agent_id, mode)
            if not coords:
                return {
                    "valid": False,
                    "error": f"No coordinates found for {agent_id} in {mode} mode"
                }
            
            # Test if coordinates are within multi-monitor bounds
            try:
                import pyautogui
                
                # For multi-monitor setups, we need to account for negative coordinates
                # Since PyAutoGUI 0.9.54 doesn't have getAllMonitors(), we'll use a heuristic approach
                screen_width, screen_height = pyautogui.size()
                
                # Check if coordinates suggest multi-monitor setup (negative X values)
                has_negative_x = any([
                    coords["input_box"][0] < 0,
                    coords["starter_location"][0] < 0
                ])
                
                if has_negative_x:
                    # Multi-monitor setup detected (negative X coordinates indicate left monitor)
                    # Assume left monitor is roughly the same size as primary monitor
                    min_x = -screen_width  # Left monitor extends to negative X
                    max_x = screen_width   # Right monitor extends to positive X
                    min_y = 0
                    max_y = screen_height
                    
                    logger.info(f"🔍 Multi-monitor setup detected (negative X coordinates)")
                    logger.info(f"   Extended bounds: X({min_x} to {max_x}), Y({min_y} to {max_y})")
                    logger.info(f"   Primary monitor: {screen_width}x{screen_height}")
                    
                else:
                    # Single monitor setup
                    min_x, max_x = 0, screen_width
                    min_y, max_y = 0, screen_height
                    logger.info(f"🔍 Single monitor setup: {screen_width}x{screen_height}")
                
                # Check input box coordinates
                input_x, input_y = coords["input_box"]
                if not (min_x <= input_x <= max_x and min_y <= input_y <= max_y):
                    return {
                        "valid": False,
                        "error": f"Input box coordinates ({input_x}, {input_y}) out of multi-monitor bounds (X: {min_x} to {max_x}, Y: {min_y} to {max_y})"
                    }
                
                # Check starter location coordinates
                starter_x, starter_y = coords["starter_location"]
                if not (min_x <= starter_x <= max_x and min_y <= starter_y <= max_y):
                    return {
                        "valid": False,
                        "error": f"Starter coordinates ({starter_x}, {starter_y}) out of multi-monitor bounds (X: {min_x} to {max_x}, Y: {min_y} to {max_y})"
                    }
                
                logger.info(f"✅ Coordinates validated for {agent_id}")
                return {
                    "valid": True,
                    "coordinates": coords,
                    "monitor_bounds": (min_x, max_x, min_y, max_y),
                    "monitor_count": 2 if has_negative_x else 1
                }
                
            except ImportError:
                logger.warning("PyAutoGUI not available - coordinate validation skipped")
                return {
                    "valid": True,
                    "coordinates": coords,
                    "warning": "PyAutoGUI not available, validation limited"
                }
                
        except Exception as e:
            logger.error(f"Error validating coordinates for {agent_id}: {e}")
            return {
                "valid": False,
                "error": f"Validation error: {str(e)}"
            }
    
    def get_available_modes(self) -> list:
        """Get available coordinate modes"""
        return self.coordinate_manager.get_available_modes()
    
    def get_agents_in_mode(self, mode: str) -> list:
        """Get agents available in a specific mode"""
        return self.coordinate_manager.get_agents_in_mode(mode)
    
    def map_coordinates(self, mode: str = "8-agent") -> Dict[str, Any]:
        """Map and display coordinate information for debugging and calibration"""
        logger.info(f"🗺️  Coordinate mapping requested for mode: {mode}")
        return self.coordinate_manager.map_coordinates(mode)
    
    def calibrate_coordinates(self, agent_id: str, input_coords: Tuple[int, int], starter_coords: Tuple[int, int], mode: str = "8-agent") -> bool:
        """Calibrate/update coordinates for a specific agent"""
        logger.info(f"🔧 Coordinate calibration requested for {agent_id}")
        return self.coordinate_manager.calibrate_coordinates(agent_id, input_coords, starter_coords, mode)
    
    def consolidate_coordinate_files(self) -> Dict[str, Any]:
        """Consolidate multiple coordinate files into primary location"""
        logger.info("🔄 Coordinate file consolidation requested")
        return self.coordinate_manager.consolidate_coordinate_files()
    
    def send_onboarding_message(self, agent_id: str, onboarding_message: str, mode: str = "8-agent") -> bool:
        """
        Send onboarding message using the proper sequence:
        starter location → Ctrl+N → validate → paste onboarding message
        
        Args:
            agent_id: Agent to onboard
            onboarding_message: Onboarding message content
            mode: Coordinate mode to use
        """
        logger.info(f"🚀 Sending onboarding message to {agent_id} via unified service")
        return self.pyautogui_messaging.send_onboarding_message(agent_id, onboarding_message, mode)
    
    def send_bulk_onboarding(self, onboarding_messages: Dict[str, str], mode: str = "8-agent") -> Dict[str, bool]:
        """
        Send onboarding messages to multiple agents using the proper sequence
        
        Args:
            onboarding_messages: Dictionary of agent_id: onboarding_message
            mode: Coordinate mode to use
        """
        logger.info(f"🚀 Sending bulk onboarding messages via unified service")
        return self.pyautogui_messaging.send_bulk_onboarding(onboarding_messages, mode)
    
    def send_high_priority_message(self, agent_id: str, urgent_message: str, mode: str = "8-agent") -> bool:
        """
        Send high priority message using Ctrl+Enter 2x sequence for urgent communications
        
        Args:
            agent_id: Agent to send urgent message to
            urgent_message: High priority message content
            mode: Coordinate mode to use
        """
        logger.info(f"🚨 Sending HIGH PRIORITY message to {agent_id} via unified service")
        return self.pyautogui_messaging.send_high_priority_message(agent_id, urgent_message, mode)
    
    def send_bulk_high_priority(self, urgent_messages: Dict[str, str], mode: str = "8-agent") -> Dict[str, bool]:
        """
        Send high priority messages to multiple agents using Ctrl+Enter 2x sequence
        
        Args:
            urgent_messages: Dictionary of agent_id: urgent_message
            mode: Coordinate mode to use
        """
        logger.info(f"🚨 Sending bulk HIGH PRIORITY messages via unified service")
        return self.pyautogui_messaging.send_bulk_high_priority(urgent_messages, mode)
    
    def send_coordinated_messages(self, messages: Dict[str, str], priority: UnifiedMessagePriority = UnifiedMessagePriority.NORMAL) -> Dict[str, bool]:
        """
        Send coordinated messages to all 8 agents through the message queue system
        
        Args:
            messages: Dictionary of agent_id: message_content
            priority: Priority level for all messages
            
        Returns:
            Dict with queuing results for each agent
        """
        logger.info(f"📡 Sending coordinated messages to all agents via queue system (Priority: {priority.value})")
        
        results = {}
        for agent_id, message in messages.items():
            # Queue message through the internal message queue system
            success = self.queue_message(
                agent_id=agent_id,
                message=message,
                message_type="text",
                priority=priority,
                requires_response=True
            )
            
            # Update agent state to working
            if success:
                self.update_agent_state(agent_id, AgentStatus.WORKING, "Coordinated message processing")
            
            results[agent_id] = success
            
            logger.info(f"Message queued for {agent_id}: {'✅ Success' if success else '❌ Failed'}")
        
        return results
    
    def get_queue_status(self) -> Dict[str, Any]:
        """
        Get current status of the message queue system
        
        Returns:
            Dict with queue status and agent states
        """
        return {
            "queue_size": self.message_queue.qsize(),
            "agent_states": self.get_all_agent_statuses(),
            "keyboard_conflicts": self.check_keyboard_conflicts()
        }
