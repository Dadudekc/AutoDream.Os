"""
Recovery System - V2 Compliant
==============================

Automatic recovery and error handling for overnight operations.
Provides agent rescue, task recovery, and system restoration.

V2 Compliance: ≤400 lines, SOLID principles, comprehensive error handling.

Author: Agent-1 - Autonomous Operations Specialist
License: MIT
"""

import time
from typing import Dict, List, Optional, Any
import logging

# V2 Integration imports
try:
    from ...core.messaging_pyautogui import send_message_to_agent
    from ...core.unified_config import get_unified_config
    from ...core.unified_logging_system import get_logger
except ImportError as e:
    logging.warning(f"V2 integration imports failed: {e}")
    # Fallback implementations
    def send_message_to_agent(*args, **kwargs):
        logging.info(f"Mock message send: {args}, {kwargs}")
        return True
    
    def get_unified_config():
        return type('MockConfig', (), {'get_env': lambda x, y=None: y})()
    
    def get_logger(name):
        return logging.getLogger(name)


class RecoverySystem:
    """
    Recovery system for overnight operations.
    
    Provides:
    - Automatic task recovery
    - Agent rescue capabilities
    - Error escalation
    - System restoration
    - Failure analysis
    """

    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize recovery system.
        
        Args:
            config: Configuration dictionary (uses config/orchestration.yml if None)
        """
        self.config = config or {}
        self.logger = get_logger(__name__)
        
        # V2 Integration
        self.unified_config = get_unified_config()
        
        # Recovery settings
        recovery_config = self.config.get('overnight', {}).get('recovery', {})
        self.max_retries = recovery_config.get('max_retries', 3)
        self.escalation_threshold = recovery_config.get('escalation_threshold', 5)
        self.auto_recovery = recovery_config.get('auto_recovery', True)
        self.agent_rescue = recovery_config.get('agent_rescue', True)
        
        # State
        self.recovery_attempts = {}  # Agent ID -> attempt count
        self.failure_history = []  # List of failure records
        self.escalated_issues = set()  # Set of escalated issue IDs
        self.last_recovery_time = 0
        
        self.logger.info("Recovery System initialized")

    async def initialize(self) -> None:
        """Initialize recovery system components."""
        try:
            # Initialize recovery tracking
            self.recovery_attempts = {f"Agent-{i}": 0 for i in range(1, 9)}
            
            self.logger.info("Recovery system initialized")
            
        except Exception as e:
            self.logger.error(f"Recovery system initialization failed: {e}")
            raise

    async def handle_cycle_failure(self, cycle_number: int, error_message: str) -> None:
        """
        Handle failure of an entire cycle.
        
        Args:
            cycle_number: Cycle that failed
            error_message: Error description
        """
        try:
            self.logger.error(f"Cycle {cycle_number} failure: {error_message}")
            
            # Record failure
            failure_record = {
                'type': 'cycle_failure',
                'cycle_number': cycle_number,
                'error_message': error_message,
                'timestamp': time.time(),
                'recovery_attempted': False,
            }
            self.failure_history.append(failure_record)
            
            # Attempt recovery
            if self.auto_recovery:
                await self._attempt_cycle_recovery(cycle_number, error_message)
                failure_record['recovery_attempted'] = True
            
            # Check for escalation
            await self._check_escalation_threshold()
            
        except Exception as e:
            self.logger.error(f"Failed to handle cycle failure: {e}")

    async def handle_task_failure(
        self,
        task_id: str,
        agent_id: str,
        error_message: str
    ) -> None:
        """
        Handle failure of an individual task.
        
        Args:
            task_id: Failed task ID
            agent_id: Agent that failed the task
            error_message: Error description
        """
        try:
            self.logger.error(f"Task failure: {task_id} by {agent_id} - {error_message}")
            
            # Record failure
            failure_record = {
                'type': 'task_failure',
                'task_id': task_id,
                'agent_id': agent_id,
                'error_message': error_message,
                'timestamp': time.time(),
                'recovery_attempted': False,
            }
            self.failure_history.append(failure_record)
            
            # Update recovery attempts for agent
            if agent_id in self.recovery_attempts:
                self.recovery_attempts[agent_id] += 1
            
            # Attempt recovery
            if self.auto_recovery:
                await self._attempt_task_recovery(task_id, agent_id, error_message)
                failure_record['recovery_attempted'] = True
            
            # Check for agent rescue
            if self.agent_rescue and agent_id in self.recovery_attempts:
                if self.recovery_attempts[agent_id] >= self.max_retries:
                    await self._rescue_agent(agent_id)
            
        except Exception as e:
            self.logger.error(f"Failed to handle task failure: {e}")

    async def handle_stalled_agents(self, stalled_agents: List[str]) -> None:
        """
        Handle stalled agents.
        
        Args:
            stalled_agents: List of stalled agent IDs
        """
        try:
            self.logger.warning(f"Handling {len(stalled_agents)} stalled agents")
            
            for agent_id in stalled_agents:
                await self._rescue_agent(agent_id)
                
        except Exception as e:
            self.logger.error(f"Failed to handle stalled agents: {e}")

    async def handle_health_issues(self, health_status: Dict[str, Any]) -> None:
        """
        Handle system health issues.
        
        Args:
            health_status: Health status information
        """
        try:
            issues = health_status.get('issues', [])
            
            if not issues:
                return
            
            self.logger.warning(f"Handling {len(issues)} health issues")
            
            for issue in issues:
                await self._handle_health_issue(issue)
                
        except Exception as e:
            self.logger.error(f"Failed to handle health issues: {e}")

    async def _attempt_cycle_recovery(self, cycle_number: int, error_message: str) -> None:
        """Attempt to recover from cycle failure."""
        try:
            self.logger.info(f"Attempting cycle {cycle_number} recovery")
            
            # Send recovery message to all agents
            recovery_message = f"""
[RECOVERY] Cycle {cycle_number} Recovery
Error: {error_message}
Action: Continue with next cycle, report any issues.
Timestamp: {time.time()}
"""
            
            # Send to all agents
            for i in range(1, 9):
                agent_id = f"Agent-{i}"
                try:
                    await asyncio.get_event_loop().run_in_executor(
                        None,
                        send_message_to_agent,
                        agent_id,
                        recovery_message
                    )
                except Exception as e:
                    self.logger.error(f"Failed to send recovery message to {agent_id}: {e}")
            
            self.last_recovery_time = time.time()
            self.logger.info("Cycle recovery attempt completed")
            
        except Exception as e:
            self.logger.error(f"Cycle recovery failed: {e}")

    async def _attempt_task_recovery(
        self,
        task_id: str,
        agent_id: str,
        error_message: str
    ) -> None:
        """Attempt to recover from task failure."""
        try:
            self.logger.info(f"Attempting task recovery: {task_id}")
            
            # Send recovery message to agent
            recovery_message = f"""
[RECOVERY] Task {task_id} Recovery
Error: {error_message}
Action: Retry task or report if impossible.
Timestamp: {time.time()}
"""
            
            await asyncio.get_event_loop().run_in_executor(
                None,
                send_message_to_agent,
                agent_id,
                recovery_message
            )
            
            self.logger.info(f"Task recovery message sent to {agent_id}")
            
        except Exception as e:
            self.logger.error(f"Task recovery failed: {e}")

    async def _rescue_agent(self, agent_id: str) -> None:
        """Rescue a stalled or failing agent."""
        try:
            self.recovery_attempts[agent_id] = 0
            msg = f"[RESCUE] {agent_id} - Reset and resume operations. Report status."
            await asyncio.get_event_loop().run_in_executor(None, send_message_to_agent, agent_id, msg)
            
            self.failure_history.append({
                'type': 'agent_rescue',
                'agent_id': agent_id,
                'timestamp': time.time(),
            })
            self.logger.info(f"Agent rescue completed for {agent_id}")
        except Exception as e:
            self.logger.error(f"Agent rescue failed for {agent_id}: {e}")

    async def _handle_health_issue(self, issue: str) -> None:
        """Handle a specific health issue."""
        try:
            self.logger.info(f"Handling health issue: {issue}")
            
            # Create issue ID for tracking
            issue_id = f"health_{int(time.time())}"
            
            # Send health alert to all agents
            health_message = f"""
[HEALTH ALERT] System Issue Detected
Issue: {issue}
Action: Monitor and report status.
Issue ID: {issue_id}
Timestamp: {time.time()}
"""
            
            # Send to all agents
            for i in range(1, 9):
                agent_id = f"Agent-{i}"
                try:
                    await asyncio.get_event_loop().run_in_executor(
                        None,
                        send_message_to_agent,
                        agent_id,
                        health_message
                    )
                except Exception as e:
                    self.logger.error(f"Failed to send health alert to {agent_id}: {e}")
            
            # Record health issue
            health_record = {
                'type': 'health_issue',
                'issue_id': issue_id,
                'issue_description': issue,
                'timestamp': time.time(),
                'agents_notified': True,
            }
            self.failure_history.append(health_record)
            
        except Exception as e:
            self.logger.error(f"Failed to handle health issue: {e}")

    async def _check_escalation_threshold(self) -> None:
        """Check if escalation threshold has been reached."""
        try:
            # Count recent failures
            current_time = time.time()
            recent_failures = [
                f for f in self.failure_history
                if current_time - f['timestamp'] < 3600  # Last hour
            ]
            
            if len(recent_failures) >= self.escalation_threshold:
                await self._escalate_issues(recent_failures)
                
        except Exception as e:
            self.logger.error(f"Failed to check escalation threshold: {e}")

    async def _escalate_issues(self, recent_failures: List[Dict[str, Any]]) -> None:
        """Escalate issues when threshold is reached."""
        try:
            self.logger.error(f"Escalating {len(recent_failures)} recent failures")
            
            # Create escalation summary
            escalation_id = f"escalation_{int(time.time())}"
            failure_summary = self._summarize_failures(recent_failures)
            
            escalation_message = f"""
[ESCALATION] Critical System Issues
Escalation ID: {escalation_id}
Recent Failures: {len(recent_failures)}
Summary: {failure_summary}
Action: Manual intervention required.
Timestamp: {time.time()}
"""
            
            # Send escalation to all agents
            for i in range(1, 9):
                agent_id = f"Agent-{i}"
                try:
                    await asyncio.get_event_loop().run_in_executor(
                        None,
                        send_message_to_agent,
                        agent_id,
                        escalation_message
                    )
                except Exception as e:
                    self.logger.error(f"Failed to send escalation to {agent_id}: {e}")
            
            # Record escalation
            self.escalated_issues.add(escalation_id)
            
            escalation_record = {
                'type': 'escalation',
                'escalation_id': escalation_id,
                'failure_count': len(recent_failures),
                'failure_summary': failure_summary,
                'timestamp': time.time(),
                'agents_notified': True,
            }
            self.failure_history.append(escalation_record)
            
        except Exception as e:
            self.logger.error(f"Failed to escalate issues: {e}")

    def _summarize_failures(self, failures: List[Dict[str, Any]]) -> str:
        """Create a summary of recent failures."""
        failure_types = {}
        for failure in failures:
            failure_type = failure.get('type', 'unknown')
            failure_types[failure_type] = failure_types.get(failure_type, 0) + 1
        
        summary_parts = []
        for failure_type, count in failure_types.items():
            summary_parts.append(f"{failure_type}: {count}")
        
        return ", ".join(summary_parts)

    def get_recovery_status(self) -> Dict[str, Any]:
        """Get current recovery system status."""
        return {
            "max_retries": self.max_retries,
            "escalation_threshold": self.escalation_threshold,
            "auto_recovery": self.auto_recovery,
            "agent_rescue": self.agent_rescue,
            "recovery_attempts": self.recovery_attempts,
            "failure_history_count": len(self.failure_history),
            "escalated_issues_count": len(self.escalated_issues),
            "last_recovery_time": self.last_recovery_time,
        }
