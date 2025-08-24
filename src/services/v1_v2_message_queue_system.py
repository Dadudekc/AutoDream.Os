#!/usr/bin/env python3
"""
V1-V2 Message Queue System
==========================

Integrates the proven V1 PyAutoGUI approach with V2 architecture.
Features:
- Message queuing system for multiple agents
- High-priority flag system (Ctrl+Enter x2)
- PyAutoGUI reliability with V2 architecture
- Multi-agent communication without inbox dependency
"""

import os
import sys
import json
import time
import logging
import threading
import queue
import hashlib
from typing import Dict, List, Any, Optional, Callable, Tuple
from pathlib import Path
from datetime import datetime, timedelta

# Optional GUI/keyboard libraries. Fall back to lightweight stubs when the
# packages are not available so the module remains importable in minimal
# environments.
try:  # pragma: no cover
    import pyautogui  # type: ignore
except Exception:  # pragma: no cover
    class _PyAutoGUIStub:
        FAILSAFE = False
        PAUSE = 0.0

        def __getattr__(self, name):
            raise RuntimeError("pyautogui is not available")

    pyautogui = _PyAutoGUIStub()  # type: ignore

try:  # pragma: no cover
    import keyboard  # type: ignore
except Exception:  # pragma: no cover
    keyboard = None  # type: ignore

try:  # pragma: no cover
    import pynput  # type: ignore
    from pynput import keyboard as pynput_keyboard  # type: ignore
except Exception:  # pragma: no cover
    pynput = None  # type: ignore

    class _KeyboardStub:
        def __getattr__(self, name):
            raise RuntimeError("pynput is not available")

    pynput_keyboard = _KeyboardStub()  # type: ignore

# Basic message enums re-exported for compatibility with tests
try:  # pragma: no cover
    from core.shared_enums import MessagePriority, MessageType, MessageStatus
except Exception:  # pragma: no cover
    from enum import Enum

    class MessagePriority(Enum):
        LOW = "low"
        NORMAL = "normal"
        HIGH = "high"
        URGENT = "urgent"

    class MessageType(Enum):
        TEXT = "text"
        SYSTEM_COMMAND = "system_command"

    class MessageStatus(Enum):
        PENDING = "pending"
        DELIVERED = "delivered"

# Configure PyAutoGUI safety
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.1

# Configure logging
logging.basicConfig(
    level=logging.WARNING,  # Reduced from INFO to WARNING for cleaner output
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("v1_v2_message_queue.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)


class V1V2MessageQueueSystem:
    """
    V1-V2 Message Queue System
    Integrates PyAutoGUI reliability with V2 architecture
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or self._default_config()
        self.is_running = False
        self.message_queue = queue.Queue()
        self.high_priority_queue = queue.PriorityQueue()
        self.agent_registry = {}
        self.message_history = []
        self.keyboard_listener = None
        self.processing_thread = None
        self.ctrl_enter_count = 0
        self.last_ctrl_enter_time = 0

        # Initialize message queue system
        self._initialize_message_system()

        # Start keyboard monitoring
        self._start_keyboard_monitoring()

        logger.info("🚀 V1-V2 Message Queue System initialized successfully")

    def _default_config(self) -> Dict[str, Any]:
        """Default configuration for message queue system - 8 Agent Mode"""
        return {
            "max_queue_size": 1000,
            "high_priority_timeout": 5.0,  # seconds
            "message_retry_attempts": 3,
            "retry_delay": 2.0,  # seconds
            "enable_pyautogui": True,
            "enable_keyboard_monitoring": True,
            "ctrl_enter_double_timeout": 1.0,  # seconds
            "message_persistence": True,
            "persistence_file": "message_history.json",
            "agent_coordinates": {
                "agent_1": {"x": 400, "y": 300},  # Foundation & Testing
                "agent_2": {"x": 1200, "y": 300},  # AI & ML Integration
                "agent_3": {"x": 400, "y": 900},  # Multimedia & Content
                "agent_4": {"x": 1200, "y": 900},  # Security & Infrastructure
                "agent_5": {"x": 2000, "y": 300},  # Business Intelligence
                "agent_6": {"x": 2000, "y": 900},  # Gaming & Entertainment
                "agent_7": {"x": 2800, "y": 300},  # Web Development
                "agent_8": {"x": 2800, "y": 900},  # Integration & Performance
            },
        }

    def _initialize_message_system(self):
        """Initialize the message queue system"""
        try:
            # Create message persistence directory
            persistence_dir = Path("message_data")
            persistence_dir.mkdir(exist_ok=True)
            logger.info(f"✅ Message persistence directory created: {persistence_dir}")

            # Load message history if persistence enabled
            if self.config["message_persistence"]:
                self._load_message_history()

            # Initialize agent registry
            self._initialize_agent_registry()

            # Start message processing thread
            self._start_message_processing()

        except Exception as e:
            logger.error(f"❌ Failed to initialize message system: {e}")
            raise

    def _initialize_agent_registry(self):
        """Initialize agent registry with coordinates and capabilities"""
        for agent_id, coords in self.config["agent_coordinates"].items():
            self.agent_registry[agent_id] = {
                "id": agent_id,
                "coordinates": coords,
                "status": "available",
                "last_message": None,
                "message_count": 0,
                "capabilities": ["text", "image", "file"],
                "priority_level": 1,
            }

        logger.info(f"✅ Initialized {len(self.agent_registry)} agents in registry")

    def _start_keyboard_monitoring(self):
        """Start monitoring for Ctrl+Enter combinations"""
        if not self.config["enable_keyboard_monitoring"]:
            return

        try:
            # Start keyboard listener
            self.keyboard_listener = pynput_keyboard.Listener(
                on_press=self._on_key_press, on_release=self._on_key_release
            )
            self.keyboard_listener.start()

            logger.info("✅ Keyboard monitoring started")

        except Exception as e:
            logger.error(f"❌ Failed to start keyboard monitoring: {e}")

    def _on_key_press(self, key):
        """Handle key press events"""
        try:
            # Check for Ctrl+Enter combination
            if hasattr(key, "char") and key.char == "\r":  # Enter key
                if keyboard.is_pressed("ctrl"):
                    current_time = time.time()

                    # Check if this is a double Ctrl+Enter
                    if (current_time - self.last_ctrl_enter_time) < self.config[
                        "ctrl_enter_double_timeout"
                    ]:
                        self.ctrl_enter_count += 1
                        if self.ctrl_enter_count >= 2:
                            logger.info("🚨 HIGH PRIORITY FLAG TRIGGERED: Ctrl+Enter x2")
                            self._trigger_high_priority_mode()
                            self.ctrl_enter_count = 0
                    else:
                        self.ctrl_enter_count = 1

                    self.last_ctrl_enter_time = current_time

        except Exception as e:
            logger.error(f"❌ Key press handling error: {e}")

    def _on_key_release(self, key):
        """Handle key release events"""
        # Reset Ctrl+Enter count after timeout
        current_time = time.time()
        if (current_time - self.last_ctrl_enter_time) > self.config[
            "ctrl_enter_double_timeout"
        ]:
            self.ctrl_enter_count = 0

    def _trigger_high_priority_mode(self):
        """Trigger high priority message processing mode"""
        try:
            logger.info("🚨 HIGH PRIORITY MODE ACTIVATED")

            # Process all high priority messages immediately
            while not self.high_priority_queue.empty():
                priority, timestamp, message = self.high_priority_queue.get()
                self._process_message_immediately(message)

            # Flash screen or notification to indicate high priority mode
            self._show_high_priority_notification()

        except Exception as e:
            logger.error(f"❌ High priority mode error: {e}")

    def _show_high_priority_notification(self):
        """Show high priority notification"""
        try:
            # Flash screen briefly
            original_position = pyautogui.position()

            # Move to corner and back (subtle flash effect)
            pyautogui.moveTo(0, 0, duration=0.1)
            pyautogui.moveTo(original_position, duration=0.1)

            logger.info("🚨 High priority notification displayed")

        except Exception as e:
            logger.error(f"❌ High priority notification error: {e}")

    def _start_message_processing(self):
        """Start the message processing thread"""

        def process_messages():
            while self.is_running:
                try:
                    # Process high priority messages first
                    if not self.high_priority_queue.empty():
                        priority, timestamp, message = self.high_priority_queue.get()
                        self._process_message_immediately(message)
                        continue

                    # Process regular messages
                    if not self.message_queue.empty():
                        message = self.message_queue.get()
                        self._process_message(message)

                    time.sleep(0.1)  # Small delay to prevent CPU spinning

                except Exception as e:
                    logger.error(f"❌ Message processing error: {e}")
                    time.sleep(1.0)

        self.processing_thread = threading.Thread(target=process_messages, daemon=True)
        self.processing_thread.start()
        logger.info("✅ Message processing thread started")

    def _process_message(self, message: Dict[str, Any]):
        """Process a regular priority message"""
        try:
            logger.info(f"📨 Processing message: {message.get('id', 'unknown')}")

            # Add to history
            self.message_history.append(
                {
                    "timestamp": datetime.now().isoformat(),
                    "message": message,
                    "status": "processing",
                }
            )

            # Send message to target agent
            success = self._send_message_to_agent(message)

            # Update history
            if success:
                self.message_history[-1]["status"] = "sent"
                logger.info(
                    f"✅ Message sent successfully to {message.get('target_agent')}"
                )
            else:
                self.message_history[-1]["status"] = "failed"
                logger.warning(
                    f"⚠️ Message failed to send to {message.get('target_agent')}"
                )

            # Persist if enabled
            if self.config["message_persistence"]:
                self._save_message_history()

        except Exception as e:
            logger.error(f"❌ Message processing error: {e}")

    def _process_message_immediately(self, message: Dict[str, Any]):
        """Process a high priority message immediately"""
        try:
            logger.info(f"🚨 IMMEDIATE PROCESSING: {message.get('id', 'unknown')}")

            # Add to history with high priority flag
            self.message_history.append(
                {
                    "timestamp": datetime.now().isoformat(),
                    "message": message,
                    "status": "high_priority_processing",
                    "priority": "high",
                }
            )

            # Send message immediately
            success = self._send_message_to_agent(message)

            # Update history
            if success:
                self.message_history[-1]["status"] = "high_priority_sent"
                logger.info(f"🚨 High priority message sent successfully")
            else:
                self.message_history[-1]["status"] = "high_priority_failed"
                logger.error(f"❌ High priority message failed")

            # Persist if enabled
            if self.config["message_persistence"]:
                self._save_message_history()

        except Exception as e:
            logger.error(f"❌ High priority message processing error: {e}")

    def _send_message_to_agent(self, message: Dict[str, Any]) -> bool:
        """Send message to target agent using PyAutoGUI with Shift+Enter line break support"""
        if not self.config["enable_pyautogui"]:
            logger.warning("⚠️ PyAutoGUI disabled - cannot send message")
            return False

        try:
            target_agent = message.get("target_agent")
            if target_agent not in self.agent_registry:
                logger.error(f"❌ Target agent '{target_agent}' not found")
                return False

            agent_info = self.agent_registry[target_agent]
            coords = agent_info["coordinates"]

            # Move to agent location
            pyautogui.moveTo(coords["x"], coords["y"], duration=0.5)

            # Click to focus
            pyautogui.click()
            time.sleep(0.2)

            # Type the message with line break support
            message_text = message.get("content", "")
            self._type_message_with_line_breaks(message_text)
            time.sleep(0.1)

            # Press Enter to send
            pyautogui.press("enter")

            # Update agent registry
            agent_info["last_message"] = datetime.now().isoformat()
            agent_info["message_count"] += 1

            return True

        except Exception as e:
            logger.error(f"❌ Failed to send message to agent: {e}")
            return False

    def _type_message_with_line_breaks(self, message_text: str):
        """Type message with proper line break handling using clipboard paste for speed"""
        try:
            # Use clipboard paste for much faster message delivery
            import pyperclip

            # Store current clipboard content
            original_clipboard = pyperclip.paste()

            try:
                # Set message to clipboard
                pyperclip.copy(message_text)
                time.sleep(0.1)  # Small delay for clipboard

                # Paste the message (Ctrl+V)
                pyautogui.hotkey("ctrl", "v")
                time.sleep(0.1)  # Small delay for paste

            finally:
                # Restore original clipboard content
                pyperclip.copy(original_clipboard)

        except ImportError:
            # Fallback to typing if pyperclip not available
            logger.warning("⚠️ pyperclip not available - falling back to typing")
            pyautogui.typewrite(message_text, interval=0.01)
        except Exception as e:
            logger.error(f"❌ Failed to paste message: {e}")
            # Fallback to simple typing if paste fails
            pyautogui.typewrite(message_text, interval=0.01)

    def send_message(
        self,
        sender_agent: str,
        target_agent: str,
        content: str,
        priority: str = "normal",
        message_type: str = "text",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Send a message from sender_agent to target_agent"""
        try:
            # Generate message ID
            message_id = self._generate_message_id()

            # Create message object
            message = {
                "id": message_id,
                "sender_agent": sender_agent,
                "target_agent": target_agent,
                "content": content,
                "type": message_type,
                "priority": priority,
                "timestamp": datetime.now().isoformat(),
                "metadata": metadata or {},
                "retry_count": 0,
            }

            # Add to appropriate queue
            if priority == "high" or priority == "urgent" or priority == "critical":
                # Add to high priority queue with proper tuple structure (priority, timestamp, message)
                # Use numeric priority for proper comparison
                priority_value = {
                    "low": 3,
                    "normal": 2,
                    "high": 1,
                    "urgent": 0,
                    "critical": -1,
                }.get(priority, 2)
                self.high_priority_queue.put((priority_value, time.time(), message))
                logger.info(f"🚨 High priority message queued: {message_id}")
            else:
                # Add to regular queue
                if self.message_queue.qsize() >= self.config["max_queue_size"]:
                    logger.warning("⚠️ Message queue full - dropping oldest message")
                    try:
                        self.message_queue.get_nowait()  # Remove oldest message
                    except queue.Empty:
                        pass

                self.message_queue.put(message)
                logger.info(f"📨 Message queued: {message_id}")

            return message_id

        except Exception as e:
            logger.error(f"❌ Failed to queue message: {e}")
            return ""

    def send_message_to_all_agents(
        self,
        sender_agent: str,
        content: str,
        priority: str = "normal",
        message_type: str = "text",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> List[str]:
        """Send a message from sender_agent to all agents"""
        message_ids = []

        for agent_id in self.agent_registry.keys():
            message_id = self.send_message(
                sender_agent, agent_id, content, priority, message_type, metadata
            )
            if message_id:
                message_ids.append(message_id)

        logger.info(f"📨 Broadcast message sent to {len(message_ids)} agents")
        return message_ids

    def send_high_priority_message(
        self,
        sender_agent: str,
        target_agent: str,
        content: str,
        message_type: str = "text",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Send a high priority message from sender_agent to target_agent (equivalent to Ctrl+Enter x2)"""
        return self.send_message(
            sender_agent, target_agent, content, "high", message_type, metadata
        )

    def _generate_message_id(self) -> str:
        """Generate unique message ID"""
        timestamp = datetime.now().isoformat()
        random_component = str(time.time())[-6:]  # Last 6 digits of timestamp
        return hashlib.md5(f"{timestamp}{random_component}".encode()).hexdigest()[:8]

    def get_queue_status(self) -> Dict[str, Any]:
        """Get current queue status"""
        return {
            "regular_queue_size": self.message_queue.qsize(),
            "high_priority_queue_size": self.high_priority_queue.qsize(),
            "total_messages_processed": len(self.message_history),
            "agents_registered": len(self.agent_registry),
            "system_running": self.is_running,
        }

    def get_agent_status(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific agent"""
        if agent_id in self.agent_registry:
            return self.agent_registry[agent_id].copy()
        return None

    def get_all_agents_status(self) -> Dict[str, Any]:
        """Get status of all agents"""
        return {
            "agents": self.agent_registry.copy(),
            "total_agents": len(self.agent_registry),
            "available_agents": len(
                [a for a in self.agent_registry.values() if a["status"] == "available"]
            ),
        }

    def clear_message_history(self) -> bool:
        """Clear message history"""
        try:
            self.message_history.clear()
            logger.info("✅ Message history cleared")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to clear message history: {e}")
            return False

    def _load_message_history(self):
        """Load message history from persistence file"""
        try:
            history_file = Path(self.config["persistence_file"])
            if history_file.exists():
                with open(history_file, "r") as f:
                    self.message_history = json.load(f)
                logger.info(
                    f"✅ Loaded {len(self.message_history)} messages from history"
                )
            else:
                logger.info("📁 No message history file found - starting fresh")
        except Exception as e:
            logger.warning(f"⚠️ Could not load message history: {e}")

    def _save_message_history(self):
        """Save message history to persistence file"""
        try:
            history_file = Path(self.config["persistence_file"])
            with open(history_file, "w") as f:
                json.dump(self.message_history, f, indent=2)
        except Exception as e:
            logger.error(f"❌ Failed to save message history: {e}")

    def start_system(self) -> bool:
        """Start the message queue system"""
        if self.is_running:
            logger.warning("⚠️ Message queue system already running")
            return False

        try:
            self.is_running = True
            logger.info("🚀 Starting V1-V2 Message Queue System...")

            # Start message processing if not already running
            if not self.processing_thread or not self.processing_thread.is_alive():
                self._start_message_processing()

            logger.info("✅ V1-V2 Message Queue System started successfully")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to start message queue system: {e}")
            self.is_running = False
            return False

    def stop_system(self) -> bool:
        """Stop the message queue system"""
        if not self.is_running:
            logger.warning("⚠️ Message queue system not running")
            return False

        try:
            logger.info("🛑 Stopping V1-V2 Message Queue System...")

            self.is_running = False

            # Stop keyboard listener
            if self.keyboard_listener:
                self.keyboard_listener.stop()
                logger.info("✅ Keyboard monitoring stopped")

            # Wait for processing thread to finish
            if self.processing_thread and self.processing_thread.is_alive():
                self.processing_thread.join(timeout=5.0)
                logger.info("✅ Message processing thread stopped")

            # Save message history
            if self.config["message_persistence"]:
                self._save_message_history()
                logger.info("✅ Message history saved")

            logger.info("✅ V1-V2 Message Queue System stopped successfully")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to stop message queue system: {e}")
            return False

    def health_check(self) -> Dict[str, Any]:
        """Perform health check of the message queue system"""
        health_status = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "checks": {},
        }

        # Check system running status
        if self.is_running:
            health_status["checks"]["system_running"] = {
                "status": "healthy",
                "running": True,
            }
        else:
            health_status["checks"]["system_running"] = {
                "status": "unhealthy",
                "running": False,
            }
            health_status["status"] = "degraded"

        # Check message processing thread
        if self.processing_thread and self.processing_thread.is_alive():
            health_status["checks"]["message_processing"] = {
                "status": "healthy",
                "thread_alive": True,
            }
        else:
            health_status["checks"]["message_processing"] = {
                "status": "unhealthy",
                "thread_alive": False,
            }
            health_status["status"] = "degraded"

        # Check keyboard monitoring
        if self.keyboard_listener and self.keyboard_listener.is_alive():
            health_status["checks"]["keyboard_monitoring"] = {
                "status": "healthy",
                "listener_alive": True,
            }
        else:
            health_status["checks"]["keyboard_monitoring"] = {
                "status": "unhealthy",
                "listener_alive": False,
            }
            health_status["status"] = "degraded"

        # Check queue health
        regular_queue_size = self.message_queue.qsize()
        high_priority_queue_size = self.high_priority_queue.qsize()

        if regular_queue_size < self.config["max_queue_size"] * 0.8:
            health_status["checks"]["regular_queue"] = {
                "status": "healthy",
                "size": regular_queue_size,
                "max_size": self.config["max_queue_size"],
            }
        else:
            health_status["checks"]["regular_queue"] = {
                "status": "warning",
                "size": regular_queue_size,
                "max_size": self.config["max_queue_size"],
            }
            if health_status["status"] == "healthy":
                health_status["status"] = "warning"

        health_status["checks"]["high_priority_queue"] = {
            "status": "healthy",
            "size": high_priority_queue_size,
        }

        return health_status


# Global instance for easy access
message_queue_system = V1V2MessageQueueSystem()


# Add missing MessageQueuePriority enum
class MessageQueuePriority:
    """Message priority levels for the queue system."""

    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"
    CRITICAL = "critical"


class MessageQueueManager:
    """
    Message Queue Manager - High-level interface for agent communication.
    Provides agent registration, messaging, and broadcast capabilities.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or self._default_config()
        self.agent_registry = {}
        self.message_history = []
        self.queue_system = V1V2MessageQueueSystem(self.config)

        # Start the queue system
        self.queue_system.start_system()
        logger.info("🚀 MessageQueueManager initialized successfully")

    def _default_config(self) -> Dict[str, Any]:
        """Default configuration for 8-agent mode"""
        return {
            "max_queue_size": 1000,
            "high_priority_timeout": 5.0,
            "message_retry_attempts": 3,
            "retry_delay": 2.0,
            "enable_pyautogui": True,
            "enable_keyboard_monitoring": True,
            "ctrl_enter_double_timeout": 1.0,
            "message_persistence": True,
            "persistence_file": "message_history.json",
            "agent_coordinates": {
                "agent_1": {"x": 400, "y": 300},  # Foundation & Testing
                "agent_2": {"x": 1200, "y": 300},  # AI & ML Integration
                "agent_3": {"x": 400, "y": 900},  # Multimedia & Content
                "agent_4": {"x": 1200, "y": 900},  # Security & Infrastructure
                "agent_5": {"x": 2000, "y": 300},  # Business Intelligence
                "agent_6": {"x": 2000, "y": 900},  # Gaming & Entertainment
                "agent_7": {"x": 2800, "y": 300},  # Web Development
                "agent_8": {"x": 2800, "y": 900},  # Integration & Performance
            },
        }

    def register_agent(
        self, agent_id: str, agent_name: str, capabilities: List[str], window_title: str
    ) -> bool:
        """Register an agent in the system"""
        try:
            # Add agent to registry
            self.agent_registry[agent_id] = {
                "id": agent_id,
                "name": agent_name,
                "capabilities": capabilities,
                "window_title": window_title,
                "status": "available",
                "last_message": None,
                "message_count": 0,
            }

            # Add to queue system with proper coordinate synchronization
            if hasattr(self.queue_system, "agent_registry"):
                # Use default coordinates for now - these should be calibrated
                default_coords = self._get_default_coordinates(agent_id)
                if default_coords:
                    # Validate coordinates before adding
                    if self._validate_coordinates(default_coords):
                        self.queue_system.agent_registry[agent_id] = {
                            "id": agent_id,
                            "coordinates": default_coords,
                            "status": "available",
                            "last_message": None,
                            "message_count": 0,
                            "capabilities": ["text", "image", "file"],
                            "priority_level": 1,
                        }
                        logger.info(
                            f"✅ Agent {agent_id} coordinates validated and synchronized"
                        )
                    else:
                        logger.warning(
                            f"⚠️ Agent {agent_id} has invalid coordinates: {default_coords}"
                        )
                        # Add agent without coordinates - will need manual calibration
                        self.queue_system.agent_registry[agent_id] = {
                            "id": agent_id,
                            "coordinates": None,
                            "status": "needs_calibration",
                            "last_message": None,
                            "message_count": 0,
                            "capabilities": ["text", "image", "file"],
                            "priority_level": 1,
                        }
                else:
                    logger.warning(f"⚠️ No coordinates found for agent {agent_id}")
                    # Add agent without coordinates - will need manual calibration
                    self.queue_system.agent_registry[agent_id] = {
                        "id": agent_id,
                        "coordinates": None,
                        "status": "needs_calibration",
                        "last_message": None,
                        "message_count": 0,
                        "capabilities": ["text", "image", "file"],
                        "priority_level": 1,
                    }

            logger.info(f"✅ Agent registered: {agent_name} ({agent_id})")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to register agent {agent_id}: {e}")
            return False

    def _validate_coordinates(self, coords: Dict[str, int]) -> bool:
        """Validate that coordinates are within reasonable screen bounds"""
        try:
            if not coords or "x" not in coords or "y" not in coords:
                return False

            x, y = coords["x"], coords["y"]

            # Basic validation - coordinates should be positive and reasonable
            # Assuming maximum screen resolution of 4000x3000 for safety
            if x < 0 or y < 0 or x > 4000 or y > 3000:
                return False

            return True

        except Exception as e:
            logger.error(f"❌ Coordinate validation error: {e}")
            return False

    def _get_default_coordinates(self, agent_id: str) -> Optional[Dict[str, int]]:
        """Get default coordinates for an agent based on 8-agent layout"""
        # 8-agent coordinate layout (3200x1200 screen)
        # These coordinates should be calibrated for your actual screen setup
        default_coords = {
            "agent_1": {"x": 400, "y": 300},  # Foundation & Testing
            "agent_2": {"x": 1200, "y": 300},  # AI & ML Integration
            "agent_3": {"x": 400, "y": 900},  # Multimedia & Content
            "agent_4": {"x": 1200, "y": 900},  # Security & Infrastructure
            "agent_5": {"x": 2000, "y": 300},  # Business Intelligence
            "agent_6": {"x": 2000, "y": 900},  # Gaming & Entertainment
            "agent_7": {"x": 2800, "y": 300},  # Web Development
            "agent_8": {"x": 2800, "y": 900},  # Integration & Performance
        }

        coords = default_coords.get(agent_id)
        if coords:
            logger.info(f"📍 Using default coordinates for {agent_id}: {coords}")
        return coords

    def calibrate_coordinates(self, agent_id: str, x: int, y: int) -> bool:
        """Calibrate coordinates for a specific agent"""
        try:
            if agent_id not in self.agent_registry:
                logger.error(f"❌ Agent {agent_id} not found in registry")
                return False

            # Validate coordinates
            if not self._validate_coordinates({"x": x, "y": y}):
                logger.error(f"❌ Invalid coordinates: x={x}, y={y}")
                return False

            # Update coordinates in both registries
            new_coords = {"x": x, "y": y}

            # Update main registry
            if agent_id in self.queue_system.agent_registry:
                self.queue_system.agent_registry[agent_id]["coordinates"] = new_coords
                self.queue_system.agent_registry[agent_id]["status"] = "available"
                logger.info(f"✅ Updated coordinates for {agent_id}: {new_coords}")

            # Update local registry status
            if agent_id in self.agent_registry:
                self.agent_registry[agent_id]["status"] = "available"

            return True

        except Exception as e:
            logger.error(f"❌ Failed to calibrate coordinates for {agent_id}: {e}")
            return False

    def get_coordinate_status(self) -> Dict[str, Any]:
        """Get status of all agent coordinates"""
        try:
            status = {}
            for agent_id in self.agent_registry.keys():
                if agent_id in self.queue_system.agent_registry:
                    agent_info = self.queue_system.agent_registry[agent_id]
                    status[agent_id] = {
                        "name": self.agent_registry[agent_id].get("name", "Unknown"),
                        "coordinates": agent_info.get("coordinates"),
                        "status": agent_info.get("status", "unknown"),
                        "has_coordinates": agent_info.get("coordinates") is not None,
                    }
                else:
                    status[agent_id] = {
                        "name": self.agent_registry[agent_id].get("name", "Unknown"),
                        "coordinates": None,
                        "status": "not_in_queue_system",
                        "has_coordinates": False,
                    }

            return status

        except Exception as e:
            logger.error(f"❌ Failed to get coordinate status: {e}")
            return {"error": str(e)}

    def get_current_mouse_position(self) -> Dict[str, int]:
        """Get current mouse position for coordinate calibration"""
        try:
            import pyautogui

            x, y = pyautogui.position()
            return {"x": x, "y": y}
        except Exception as e:
            logger.error(f"❌ Failed to get mouse position: {e}")
            return {"x": 0, "y": 0}

    def broadcast_message(
        self,
        source_agent: str,
        content: str,
        priority: str = "normal",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> List[str]:
        """Broadcast a message to all registered agents"""
        try:
            message_ids = []
            successful_sends = 0
            failed_sends = 0

            for agent_id in self.agent_registry.keys():
                if agent_id != source_agent:  # Don't send to self
                    # Check if agent has valid coordinates
                    if agent_id in self.queue_system.agent_registry:
                        agent_info = self.queue_system.agent_registry[agent_id]
                        if (
                            agent_info.get("coordinates")
                            and agent_info.get("status") == "available"
                        ):
                            message_id = self.send_message(
                                source_agent, agent_id, content, priority, metadata
                            )
                            if message_id:
                                message_ids.append(message_id)
                                successful_sends += 1
                            else:
                                failed_sends += 1
                        else:
                            logger.warning(
                                f"⚠️ Agent {agent_id} has no coordinates or is not available"
                            )
                            failed_sends += 1
                    else:
                        logger.warning(f"⚠️ Agent {agent_id} not found in queue system")
                        failed_sends += 1

            logger.info(
                f"📢 Broadcast message sent to {successful_sends} agents, {failed_sends} failed"
            )
            return message_ids

        except Exception as e:
            logger.error(f"❌ Failed to broadcast message: {e}")
            return []

    def send_message(
        self,
        source_agent: str,
        target_agent: str,
        content: str,
        priority: str = "normal",
        high_priority: bool = False,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Send a message from source_agent to target_agent."""
        try:
            # Handle high_priority flag
            if high_priority:
                priority = "high"

            message_id = self.queue_system.send_message(
                sender_agent=source_agent,
                target_agent=target_agent,
                content=content,
                priority=priority,
                message_type="text",
                metadata=metadata,
            )

            # Add to history
            self.message_history.append(
                {
                    "timestamp": datetime.now().isoformat(),
                    "source": source_agent,
                    "target": target_agent,
                    "content": content,
                    "priority": priority,
                    "message_id": message_id,
                    "status": "sent",
                    "high_priority": high_priority,
                }
            )

            return message_id

        except Exception as e:
            logger.error(f"❌ Failed to send message: {e}")
            return ""

    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status."""
        try:
            queue_status = self.queue_system.get_queue_status()
            agent_details = {}

            for agent_id, agent_info in self.agent_registry.items():
                agent_details[agent_id] = {
                    "name": agent_info.get("name", "Unknown"),
                    "status": agent_info.get("status", "unknown"),
                    "capabilities": agent_info.get("capabilities", []),
                    "window_title": agent_info.get("window_title", "Unknown"),
                    "coordinates": agent_info.get("coordinates", {}),
                }

            return {
                "registered_agents": len(self.agent_registry),
                "queue_system": queue_status,
                "agent_details": agent_details,
            }

        except Exception as e:
            logger.error(f"❌ Failed to get system status: {e}")
            return {"error": str(e)}

    def stop(self):
        """Stop the message queue system."""
        self.queue_system.stop_system()


def send_message(target_agent: str, content: str, priority: str = "normal") -> str:
    """Convenience function to send a message"""
    return message_queue_system.send_message(target_agent, content, priority)


def send_high_priority_message(target_agent: str, content: str) -> str:
    """Convenience function to send a high priority message"""
    return message_queue_system.send_high_priority_message(target_agent, content)


def send_to_all_agents(content: str, priority: str = "normal") -> List[str]:
    """Convenience function to send message to all agents"""
    return message_queue_system.send_message_to_all_agents(content, priority)


if __name__ == "__main__":
    # Example usage
    try:
        # Start the system
        message_queue_system.start_system()

        # Send a test message
        message_id = send_message(
            "agent_7",
            "Hello from Multimedia & Content Specialist! Testing the message queue system.",
        )
        print(f"Test message sent with ID: {message_id}")

        # Keep system running for a bit
        time.sleep(10)

        # Stop the system
        message_queue_system.stop_system()

    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
        message_queue_system.stop_system()
    except Exception as e:
        print(f"❌ Error: {e}")
        message_queue_system.stop_system()
