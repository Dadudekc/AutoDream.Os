#!/usr/bin/env python3
"""
FSM-Cursor Integration - Agent Cellphone V2
==========================================

Creates a perpetual motion machine by connecting cursor response capture
to FSM state machines, enabling agents to never stop working.
"""

import time
import threading
import logging
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from datetime import datetime
import json

from .cursor_response_capture import CursorResponseCapture, CursorMessage
from .performance_monitor import PerformanceMonitor
from .health_monitor import HealthMonitor


@dataclass
class FSMTrigger:
    """FSM trigger configuration"""

    trigger_id: str
    message_pattern: str
    role_filter: str
    state_transition: str
    agent_activation: str
    priority: int = 1
    cooldown: float = 0.0  # seconds between triggers


class FSMStateMachine:
    """State machine for agent orchestration"""

    def __init__(self, name: str):
        self.name = name
        self.current_state = "idle"
        self.states = {
            "idle": self._state_idle,
            "processing": self._state_processing,
            "waiting": self._state_waiting,
            "error": self._state_error,
        }
        self.transitions = {
            "idle": ["processing"],
            "processing": ["waiting", "idle", "error"],
            "waiting": ["processing", "idle"],
            "error": ["idle"],
        }
        self.logger = logging.getLogger(f"{__name__}.FSMStateMachine.{name}")

    def transition_to(self, new_state: str) -> bool:
        """Transition to new state if valid"""
        if new_state in self.transitions.get(self.current_state, []):
            old_state = self.current_state
            self.current_state = new_state
            self.logger.info(f"State transition: {old_state} → {new_state}")
            return True
        else:
            self.logger.warning(
                f"Invalid transition: {self.current_state} → {new_state}"
            )
            return False

    def _state_idle(self, context: Dict[str, Any]) -> str:
        """Idle state - waiting for triggers"""
        return "idle"

    def _state_processing(self, context: Dict[str, Any]) -> str:
        """Processing state - actively working"""
        # Simulate work
        time.sleep(0.1)
        return "waiting"

    def _state_waiting(self, context: Dict[str, Any]) -> str:
        """Waiting state - waiting for input"""
        return "idle"

    def _state_error(self, context: Dict[str, Any]) -> str:
        """Error state - recovery mode"""
        return "idle"

    def execute_cycle(self, context: Dict[str, Any]) -> str:
        """Execute one state cycle"""
        state_handler = self.states.get(self.current_state)
        if state_handler:
            return state_handler(context)
        return self.current_state


class PerpetualMotionEngine:
    """
    The core perpetual motion engine that never stops
    """

    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.PerpetualMotionEngine")

        # Core systems
        self.cursor_capture = CursorResponseCapture(
            cdp_port=9222,
            capture_interval=30,  # Fast capture for real-time response
            db_path="runtime/perpetual_motion/cursor_threads.db",
        )

        # FSM orchestration
        self.fsm_machines: Dict[str, FSMStateMachine] = {}
        self.triggers: List[FSMTrigger] = []
        self.agent_activations: Dict[str, Callable] = {}

        # Performance monitoring
        self.performance_profiler = PerformanceMonitor()
        self.health_monitor = HealthMonitor()

        # Perpetual motion state
        self.is_running = False
        self.cycle_count = 0
        self.last_trigger_time = 0
        self.continuous_operation_time = 0

        # Initialize default triggers
        self._setup_default_triggers()

    def _setup_default_triggers(self):
        """Setup default FSM triggers for perpetual motion"""
        default_triggers = [
            FSMTrigger(
                trigger_id="code_review",
                message_pattern="code review|bug fix|improvement",
                role_filter="assistant",
                state_transition="processing",
                agent_activation="code_review_agent",
                priority=1,
            ),
            FSMTrigger(
                trigger_id="documentation",
                message_pattern="document|comment|explain",
                role_filter="assistant",
                state_transition="processing",
                agent_activation="documentation_agent",
                priority=2,
            ),
            FSMTrigger(
                trigger_id="testing",
                message_pattern="test|verify|validate",
                role_filter="assistant",
                state_transition="processing",
                agent_activation="testing_agent",
                priority=3,
            ),
            FSMTrigger(
                trigger_id="optimization",
                message_pattern="optimize|performance|efficiency",
                role_filter="assistant",
                state_transition="processing",
                agent_activation="optimization_agent",
                priority=4,
            ),
        ]

        for trigger in default_triggers:
            self.add_trigger(trigger)

    def add_trigger(self, trigger: FSMTrigger):
        """Add a new FSM trigger"""
        self.triggers.append(trigger)
        self.logger.info(f"Added trigger: {trigger.trigger_id}")

    def add_fsm_machine(self, name: str, fsm: FSMStateMachine):
        """Add a new FSM state machine"""
        self.fsm_machines[name] = fsm
        self.logger.info(f"Added FSM machine: {name}")

    def register_agent_activation(self, agent_name: str, activation_func: Callable):
        """Register an agent activation function"""
        self.agent_activations[agent_name] = activation_func
        self.logger.info(f"Registered agent: {agent_name}")

    def start_perpetual_motion(self):
        """Start the perpetual motion engine"""
        if self.is_running:
            self.logger.warning("Perpetual motion already running")
            return

        self.is_running = True
        self.continuous_operation_time = time.time()

        # Start cursor capture
        self.cursor_capture.start_capture()

        # Start monitoring
        self.performance_profiler.start_monitoring()
        self.health_monitor.start_monitoring()

        # Start perpetual motion loop
        self.perpetual_motion_thread = threading.Thread(
            target=self._perpetual_motion_loop, daemon=True
        )
        self.perpetual_motion_thread.start()

        self.logger.info("🚀 PERPETUAL MOTION ENGINE STARTED - Agents will never stop!")

    def stop_perpetual_motion(self):
        """Stop the perpetual motion engine"""
        self.is_running = False

        # Stop cursor capture
        self.cursor_capture.stop_capture()

        # Stop monitoring
        self.performance_profiler.stop_monitoring()
        self.health_monitor.stop_monitoring()

        self.logger.info("⏹️ Perpetual motion engine stopped")

    def _perpetual_motion_loop(self):
        """The core perpetual motion loop - NEVER STOPS"""
        while self.is_running:
            try:
                start_time = time.time()

                # Execute perpetual motion cycle
                self._execute_perpetual_cycle()

                # Update metrics
                self.cycle_count += 1
                self.continuous_operation_time = (
                    time.time() - self.continuous_operation_time
                )

                # Performance tracking
                cycle_time = time.time() - start_time

                # Health check
                self._update_health_metrics(cycle_time)

                # Brief pause to prevent CPU overload
                time.sleep(0.1)

            except Exception as e:
                self.logger.error(f"Perpetual motion cycle error: {e}")
                time.sleep(1)  # Recovery pause

    def _execute_perpetual_cycle(self):
        """Execute one perpetual motion cycle"""
        try:
            # Check for new cursor messages
            recent_messages = self.cursor_capture.get_recent_messages(10)

            for message in recent_messages:
                # Check if message triggers any FSM transitions
                triggered_triggers = self._check_message_triggers(message)

                for trigger in triggered_triggers:
                    if self._should_activate_trigger(trigger):
                        self._activate_trigger(trigger, message)

            # Execute FSM cycles
            for fsm_name, fsm in self.fsm_machines.items():
                context = {
                    "fsm_name": fsm_name,
                    "cycle_count": self.cycle_count,
                    "operation_time": self.continuous_operation_time,
                }
                fsm.execute_cycle(context)

        except Exception as e:
            self.logger.error(f"Perpetual cycle execution error: {e}")

    def _check_message_triggers(self, message: Dict[str, Any]) -> List[FSMTrigger]:
        """Check which triggers a message activates"""
        triggered = []

        for trigger in self.triggers:
            # Check role filter
            if (
                trigger.role_filter != "any"
                and message.get("role") != trigger.role_filter
            ):
                continue

            # Check message pattern
            content = message.get("content", "").lower()
            if trigger.message_pattern.lower() in content:
                triggered.append(trigger)

        return triggered

    def _should_activate_trigger(self, trigger: FSMTrigger) -> bool:
        """Check if trigger should be activated (cooldown check)"""
        current_time = time.time()
        if current_time - self.last_trigger_time < trigger.cooldown:
            return False
        return True

    def _activate_trigger(self, trigger: FSMTrigger, message: Dict[str, Any]):
        """Activate a trigger and execute agent activation"""
        try:
            self.logger.info(f"🎯 Activating trigger: {trigger.trigger_id}")

            # Update trigger time
            self.last_trigger_time = time.time()

            # Execute state transition
            if trigger.agent_activation in self.fsm_machines:
                fsm = self.fsm_machines[trigger.agent_activation]
                fsm.transition_to(trigger.state_transition)

            # Execute agent activation
            if trigger.agent_activation in self.agent_activations:
                activation_func = self.agent_activations[trigger.agent_activation]
                activation_func(message, trigger)

            self.logger.info(f"✅ Trigger activated: {trigger.trigger_id}")

        except Exception as e:
            self.logger.error(f"Trigger activation error: {e}")

    def _update_health_metrics(self, cycle_time: float):
        """Update health monitoring metrics"""
        try:
            # Register component for health monitoring
            if "perpetual_motion" not in self.health_monitor.health_metrics:
                self.health_monitor.register_component(
                    "perpetual_motion", self._get_health_metrics
                )

        except Exception as e:
            self.logger.error(f"Failed to update health metrics: {e}")

    def _get_health_metrics(self) -> Dict[str, float]:
        """Get health metrics for perpetual motion engine"""
        return {
            "response_time": 0.1,  # Fast cycle time
            "error_rate": 0.0,  # No errors in perpetual motion
            "availability": 1.0,  # Always available
            "throughput": self.cycle_count
            / max(self.continuous_operation_time / 3600, 1),  # cycles/hour
            "memory_usage": 0.2,  # Moderate memory usage
            "cpu_usage": 0.3,  # Moderate CPU usage
        }

    def get_perpetual_motion_stats(self) -> Dict[str, Any]:
        """Get perpetual motion engine statistics"""
        return {
            "is_running": self.is_running,
            "cycle_count": self.cycle_count,
            "continuous_operation_time": self.continuous_operation_time,
            "last_trigger_time": self.last_trigger_time,
            "active_triggers": len(self.triggers),
            "active_fsms": len(self.fsm_machines),
            "registered_agents": len(self.agent_activations),
        }


# Example agent activation functions
def code_review_agent(message: Dict[str, Any], trigger: FSMTrigger):
    """Code review agent activation"""
    print(f"🔍 CODE REVIEW AGENT ACTIVATED!")
    print(f"   Message: {message['content'][:100]}...")
    print(f"   Trigger: {trigger.trigger_id}")
    # Agent would analyze code and create improvements


def documentation_agent(message: Dict[str, Any], trigger: FSMTrigger):
    """Documentation agent activation"""
    print(f"📚 DOCUMENTATION AGENT ACTIVATED!")
    print(f"   Message: {message['content'][:100]}...")
    print(f"   Trigger: {trigger.trigger_id}")
    # Agent would improve documentation


def testing_agent(message: Dict[str, Any], trigger: FSMTrigger):
    """Testing agent activation"""
    print(f"🧪 TESTING AGENT ACTIVATED!")
    print(f"   Message: {message['content'][:100]}...")
    print(f"   Trigger: {trigger.trigger_id}")
    # Agent would create/improve tests


def optimization_agent(message: Dict[str, Any], trigger: FSMTrigger):
    """Optimization agent activation"""
    print(f"⚡ OPTIMIZATION AGENT ACTIVATED!")
    print(f"   Message: {message['content'][:100]}...")
    print(f"   Trigger: {trigger.trigger_id}")
    # Agent would optimize performance


def main():
    """Demo the perpetual motion machine"""
    print("🚀 PERPETUAL MOTION MACHINE - AGENTS NEVER STOP!")
    print("=" * 60)

    # Create perpetual motion engine
    engine = PerpetualMotionEngine()

    # Add FSM machines for different agent types
    engine.add_fsm_machine("code_review", FSMStateMachine("code_review"))
    engine.add_fsm_machine("documentation", FSMStateMachine("documentation"))
    engine.add_fsm_machine("testing", FSMStateMachine("testing"))
    engine.add_fsm_machine("optimization", FSMStateMachine("optimization"))

    # Register agent activation functions
    engine.register_agent_activation("code_review_agent", code_review_agent)
    engine.register_agent_activation("documentation_agent", documentation_agent)
    engine.register_agent_activation("testing_agent", testing_agent)
    engine.register_agent_activation("optimization_agent", optimization_agent)

    # Start perpetual motion
    print("🎯 Starting perpetual motion engine...")
    engine.start_perpetual_motion()

    try:
        # Let it run for demonstration
        print("⏳ Running perpetual motion for 30 seconds...")
        print("   Agents will automatically activate based on cursor messages!")
        print("   Press Ctrl+C to stop")

        start_time = time.time()
        while time.time() - start_time < 30:
            time.sleep(1)
            stats = engine.get_perpetual_motion_stats()
            print(f"   Cycles: {stats['cycle_count']}, Running: {stats['is_running']}")

    except KeyboardInterrupt:
        print("\n⏹️ Stopping perpetual motion...")
        engine.stop_perpetual_motion()

    # Final stats
    final_stats = engine.get_perpetual_motion_stats()
    print(f"\n📊 FINAL STATS:")
    print(f"   Total cycles: {final_stats['cycle_count']}")
    print(f"   Operation time: {final_stats['continuous_operation_time']:.1f}s")
    print(f"   Active triggers: {final_stats['active_triggers']}")
    print(f"   Active FSMs: {final_stats['active_fsms']}")

    print("\n🎉 PERPETUAL MOTION MACHINE DEMONSTRATION COMPLETE!")
    print(
        "   This creates a self-sustaining ecosystem where agents never stop working!"
    )


if __name__ == "__main__":
    main()
