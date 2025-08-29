from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable, Tuple
import json
import logging
import threading

    import pyautogui
    import pyperclip
from ..autonomous_development.code.generator import CodeGenerator
from ..autonomous_development.tasks.manager import TaskManager
from ..autonomous_development.testing.orchestrator import TestingOrchestrator
from ..autonomous_development.workflow.engine import WorkflowEngine
from .cursor_response_capture import CursorResponseCapture
from .fsm_cursor_integration import PerpetualMotionEngine, FSMStateMachine, FSMTrigger
from .health_monitor import HealthMonitor
from .performance_monitor import PerformanceMonitor
from dataclasses import dataclass
from src.utils.stability_improvements import stability_manager, safe_import
import random
import time

#!/usr/bin/env python3
"""
Autonomous Development - Agent Cellphone V2
==========================================

Integrates PyAutoGUI with FSM, cursor capture, and messaging systems
to create true autonomous development where agents can interact with
development tools and create new conversations automatically.

REFACTORED: Uses extracted modules for workflow, task management, code generation, and testing.
CLEANED UP: Removed extracted code remnants, updated imports, and ensured proper module usage.
"""



# Core systems

# Extracted autonomous development modules

# PyAutoGUI for autonomous interaction
try:

    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False
    print("⚠️ PyAutoGUI not available. Install with: pip install pyautogui pyperclip")


@dataclass
class DevelopmentAction:
    """Autonomous development action configuration"""
    action_id: str
    action_type: str  # 'typing', 'clicking', 'navigation', 'code_generation'
    target_element: str
    action_data: Dict[str, Any]
    priority: int = 1
    cooldown: float = 1.0


class AutonomousDevelopmentEngine:
    """
    Refactored autonomous development engine that uses extracted modules
    for workflow, task management, code generation, and testing.
    
    CLEANED UP: Removed extracted code remnants and ensured proper module usage.
    """

    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.AutonomousDevelopmentEngine")

        # Check PyAutoGUI availability
        if not PYAUTOGUI_AVAILABLE:
            self.logger.error(
                "PyAutoGUI not available - autonomous development disabled"
            )
            return

        # Core systems
        self.perpetual_motion = PerpetualMotionEngine()
        self.cursor_capture = CursorResponseCapture(
            cdp_port=9222,
            capture_interval=15,  # Fast capture for real-time development
            db_path="runtime/autonomous_dev/cursor_threads.db",
        )

        # Extracted autonomous development modules
        self.workflow_engine = WorkflowEngine()
        self.task_manager = TaskManager()
        self.code_generator = CodeGenerator()
        self.testing_orchestrator = TestingOrchestrator()

        # Autonomous development state
        self.is_autonomous = False
        self.development_actions: List[DevelopmentAction] = []
        self.active_conversations = 0
        self.autonomous_cycle_count = 0

        # PyAutoGUI configuration
        self.setup_pyautogui()

        # Initialize autonomous triggers
        self._setup_autonomous_triggers()

    def setup_pyautogui(self):
        """Configure PyAutoGUI for safe autonomous operation"""
        if not PYAUTOGUI_AVAILABLE:
            return

        # Safety settings
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.1  # Brief pause between actions

        # Get screen dimensions
        self.screen_width, self.screen_height = pyautogui.size()
        self.logger.info(f"Screen dimensions: {self.screen_width}x{self.screen_height}")

    def _setup_autonomous_triggers(self):
        """Setup autonomous development triggers"""
        autonomous_triggers = [
            FSMTrigger(
                trigger_id="autonomous_code_review",
                message_pattern="code review|improve|bug|fix",
                role_filter="assistant",
                state_transition="processing",
                agent_activation="autonomous_code_review",
                priority=1,
            ),
            FSMTrigger(
                trigger_id="autonomous_documentation",
                message_pattern="document|comment|explain",
                role_filter="assistant",
                state_transition="processing",
                agent_activation="autonomous_documentation",
                priority=2,
            ),
            FSMTrigger(
                trigger_id="autonomous_testing",
                message_pattern="test|coverage|verify",
                role_filter="assistant",
                state_transition="processing",
                agent_activation="autonomous_testing",
                priority=3,
            ),
            FSMTrigger(
                trigger_id="autonomous_optimization",
                message_pattern="optimize|performance|efficient",
                role_filter="assistant",
                state_transition="processing",
                agent_activation="autonomous_optimization",
                priority=4,
            ),
        ]

        for trigger in autonomous_triggers:
            self.perpetual_motion.add_trigger(trigger)

        # Register autonomous agent activations
        self.perpetual_motion.register_agent_activation(
            "autonomous_code_review", self.autonomous_code_review
        )
        self.perpetual_motion.register_agent_activation(
            "autonomous_documentation", self.autonomous_documentation
        )
        self.perpetual_motion.register_agent_activation(
            "autonomous_testing", self.autonomous_testing
        )
        self.perpetual_motion.register_agent_activation(
            "autonomous_optimization", self.autonomous_optimization
        )

    def start_autonomous_development(self):
        """Start autonomous development mode"""
        if not PYAUTOGUI_AVAILABLE:
            self.logger.error(
                "Cannot start autonomous development - PyAutoGUI not available"
            )
            return False

        if self.is_autonomous:
            self.logger.warning("Autonomous development already running")
            return False

        self.is_autonomous = True
        self.logger.info("🚀 REFACTORED AUTONOMOUS DEVELOPMENT MODE ACTIVATED!")
        self.logger.info("   Using extracted modules for better maintainability!")

        # Start perpetual motion engine
        self.perpetual_motion.start_perpetual_motion()

        # Start autonomous development loop
        self._start_autonomous_loop()

        return True

    def _start_autonomous_loop(self):
        """Start the autonomous development loop"""
        def autonomous_loop():
            while self.is_autonomous:
                try:
                    self._autonomous_development_cycle()
                    time.sleep(5)  # Cycle every 5 seconds
                except Exception as e:
                    self.logger.error(f"Autonomous development cycle error: {e}")
                    time.sleep(10)  # Longer pause on error

        # Start autonomous loop in separate thread
        self.autonomous_thread = threading.Thread(target=autonomous_loop, daemon=True)
        self.autonomous_thread.start()

    def _autonomous_development_cycle(self):
        """Execute one autonomous development cycle"""
        try:
            self.autonomous_cycle_count += 1
            self.logger.debug(f"Autonomous development cycle {self.autonomous_cycle_count}")

            # Check for new development actions
            self._check_for_development_actions()

            # Monitor cursor activity
            self._monitor_cursor_activity()

            # Execute pending actions
            self._execute_pending_actions()

        except Exception as e:
            self.logger.error(f"Autonomous development cycle failed: {e}")

    def _check_for_development_actions(self):
        """Check for new development actions from workflow engine"""
        try:
            # Get pending actions from workflow engine
            pending_actions = self.workflow_engine.get_pending_actions()
            
            for action in pending_actions:
                if action not in self.development_actions:
                    self.development_actions.append(action)
                    self.logger.info(f"Added new development action: {action.action_id}")

        except Exception as e:
            self.logger.error(f"Failed to check for development actions: {e}")

    def _monitor_cursor_activity(self):
        """Monitor cursor activity for development opportunities"""
        try:
            # Get cursor activity from capture system
            cursor_activity = self.cursor_capture.get_recent_activity()
            
            if cursor_activity:
                # Analyze activity for development patterns
                self._analyze_cursor_activity(cursor_activity)

        except Exception as e:
            self.logger.error(f"Failed to monitor cursor activity: {e}")

    def _analyze_cursor_activity(self, activity_data: Dict[str, Any]):
        """Analyze cursor activity for development opportunities"""
        try:
            # Use code generator to analyze activity
            analysis = self.code_generator.analyze_code_file(activity_data.get('file_path', ''))
            
            if analysis and 'issues' in analysis:
                # Create development action for issues found
                self._create_development_action_from_analysis(analysis)

        except Exception as e:
            self.logger.error(f"Failed to analyze cursor activity: {e}")

    def _create_development_action_from_analysis(self, analysis: Dict[str, Any]):
        """Create development action from code analysis"""
        try:
            if not analysis.get('issues'):
                return

            # Create action for first issue found
            issue = analysis['issues'][0]
            
            action = DevelopmentAction(
                action_id=f"fix_{issue.issue_type}_{int(time.time())}",
                action_type="code_generation",
                target_element=issue.file_path,
                action_data={
                    "issue_type": issue.issue_type,
                    "line_number": issue.line_number,
                    "description": issue.description,
                    "suggestion": issue.suggestion
                },
                priority=2 if issue.severity == 'warning' else 1
            )
            
            self.development_actions.append(action)
            self.logger.info(f"Created development action for issue: {issue.issue_type}")

        except Exception as e:
            self.logger.error(f"Failed to create development action: {e}")

    def _execute_pending_actions(self):
        """Execute pending development actions"""
        try:
            # Get actions from task manager
            pending_tasks = self.task_manager.get_task_manager_stats()
            
            if pending_tasks.get('pending_tasks', 0) > 0:
                # Execute next pending task
                self._execute_next_task()

        except Exception as e:
            self.logger.error(f"Failed to execute pending actions: {e}")

    def _execute_next_task(self):
        """Execute the next pending task"""
        try:
            # This would integrate with the task manager to execute tasks
            # For now, just log that we're ready to execute
            self.logger.debug("Ready to execute next pending task")

        except Exception as e:
            self.logger.error(f"Failed to execute next task: {e}")

    def autonomous_code_review(self, message_data: Dict[str, Any]):
        """Autonomous code review using extracted code generator"""
        try:
            self.logger.info("🤖 Autonomous code review activated")
            
            # Use code generator for analysis
            file_path = message_data.get('file_path', '')
            if file_path:
                report = self.code_generator.generate_code_report(file_path)
                self.logger.info(f"Code review report generated for {file_path}")
                
                # Create development action based on report
                self._create_code_review_action(file_path, report)
            else:
                self.logger.warning("No file path provided for code review")

        except Exception as e:
            self.logger.error(f"Autonomous code review failed: {e}")

    def autonomous_documentation(self, message_data: Dict[str, Any]):
        """Autonomous documentation improvement"""
        try:
            self.logger.info("📚 Autonomous documentation activated")
            
            # Use code generator to analyze documentation coverage
            file_path = message_data.get('file_path', '')
            if file_path:
                analysis = self.code_generator.analyze_code_file(file_path)
                doc_coverage = analysis.get('metrics', {}).get('documentation_coverage', 0)
                
                if doc_coverage < 50:
                    self._create_documentation_action(file_path, doc_coverage)
                else:
                    self.logger.info(f"Documentation coverage is good: {doc_coverage:.1f}%")

        except Exception as e:
            self.logger.error(f"Autonomous documentation failed: {e}")

    def autonomous_testing(self, message_data: Dict[str, Any]):
        """Autonomous testing using extracted testing orchestrator"""
        try:
            self.logger.info("🧪 Autonomous testing activated")
            
            # Use testing orchestrator to run tests
            test_directory = message_data.get('test_directory', 'tests')
            success = self.testing_orchestrator.run_tests(test_files=None, test_suite_name="autonomous")
            
            if success:
                # Get test results
                summary = self.testing_orchestrator.get_test_summary("autonomous")
                self.logger.info(f"Testing completed: {summary.get('passed_tests', 0)} passed, {summary.get('failed_tests', 0)} failed")
                
                # Create action for failed tests if any
                if summary.get('failed_tests', 0) > 0:
                    self._create_testing_action(summary)
            else:
                self.logger.warning("Testing failed to start")

        except Exception as e:
            self.logger.error(f"Autonomous testing failed: {e}")

    def autonomous_optimization(self, message_data: Dict[str, Any]):
        """Autonomous code optimization"""
        try:
            self.logger.info("⚡ Autonomous optimization activated")
            
            # Use code generator to analyze code quality
            file_path = message_data.get('file_path', '')
            if file_path:
                analysis = self.code_generator.analyze_code_file(file_path)
                metrics = analysis.get('metrics', {})
                
                # Check for optimization opportunities
                if metrics.get('cyclomatic_complexity', 0) > 10:
                    self._create_optimization_action(file_path, "high_complexity")
                elif metrics.get('maintainability_index', 100) < 50:
                    self._create_optimization_action(file_path, "low_maintainability")
                else:
                    self.logger.info("Code quality is good, no optimization needed")

        except Exception as e:
            self.logger.error(f"Autonomous optimization failed: {e}")

    def _create_code_review_action(self, file_path: str, report: str):
        """Create development action for code review"""
        action = DevelopmentAction(
            action_id=f"code_review_{int(time.time())}",
            action_type="code_generation",
            target_element=file_path,
            action_data={"report": report, "action": "code_review"},
            priority=2
        )
        self.development_actions.append(action)

    def _create_documentation_action(self, file_path: str, coverage: float):
        """Create development action for documentation improvement"""
        action = DevelopmentAction(
            action_id=f"documentation_{int(time.time())}",
            action_type="code_generation",
            target_element=file_path,
            action_data={"coverage": coverage, "action": "improve_documentation"},
            priority=3
        )
        self.development_actions.append(action)

    def _create_testing_action(self, test_summary: Dict[str, Any]):
        """Create development action for testing improvements"""
        action = DevelopmentAction(
            action_id=f"testing_{int(time.time())}",
            action_type="code_generation",
            target_element="test_suite",
            action_data={"test_summary": test_summary, "action": "fix_failed_tests"},
            priority=2
        )
        self.development_actions.append(action)

    def _create_optimization_action(self, file_path: str, optimization_type: str):
        """Create development action for code optimization"""
        action = DevelopmentAction(
            action_id=f"optimization_{int(time.time())}",
            action_type="code_generation",
            target_element=file_path,
            action_data={"optimization_type": optimization_type, "action": "optimize_code"},
            priority=2
        )
        self.development_actions.append(action)

    def stop_autonomous_development(self):
        """Stop autonomous development mode"""
        if not self.is_autonomous:
            self.logger.warning("Autonomous development not running")
            return False

        self.is_autonomous = False
        self.logger.info("⏹️ Autonomous development stopped")

        # Stop perpetual motion engine
        if hasattr(self, 'perpetual_motion'):
            self.perpetual_motion.stop_perpetual_motion()

        return True

    def get_autonomous_status(self) -> Dict[str, Any]:
        """Get autonomous development status"""
        return {
            "is_autonomous": self.is_autonomous,
            "active_conversations": self.active_conversations,
            "autonomous_cycle_count": self.autonomous_cycle_count,
            "pending_actions": len(self.development_actions),
            "workflow_status": self.workflow_engine.get_workflow_status() if hasattr(self, 'workflow_engine') else {},
            "task_status": self.task_manager.get_task_manager_stats() if hasattr(self, 'task_manager') else {},
            "testing_status": self.testing_orchestrator.get_test_summary() if hasattr(self, 'testing_orchestrator') else {}
        }

    def cleanup(self):
        """Cleanup resources"""
        try:
            self.stop_autonomous_development()
            
            # Clear extracted modules
            if hasattr(self, 'workflow_engine'):
                self.workflow_engine.cleanup()
            if hasattr(self, 'task_manager'):
                self.task_manager.stop_task_manager()
            if hasattr(self, 'testing_orchestrator'):
                self.testing_orchestrator.clear_results()
            
            self.logger.info("Autonomous development engine cleaned up")
            
        except Exception as e:
            self.logger.error(f"Cleanup failed: {e}")


# Global instance
autonomous_development_engine = AutonomousDevelopmentEngine()
