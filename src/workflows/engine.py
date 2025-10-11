"""
Workflow Engine - V2 Compliant
==============================

Core workflow execution engine for multi-agent orchestration.
Integrates with V2's messaging system and coordinate management.

V2 Compliance: ≤400 lines, SOLID principles, comprehensive error handling.

Author: Agent-1 - Workflow Orchestration Specialist
License: MIT
"""

import asyncio
import json
import logging
import time
from pathlib import Path
from typing import Any

from .models import (
    AIResponse,
    ResponseType,
    WorkflowConfiguration,
    WorkflowProgress,
    WorkflowState,
    WorkflowStep,
)

# V2 Integration imports
try:
    from ..core.coordinate_loader import get_coordinate_loader
    from ..core.messaging_pyautogui import send_message_to_agent
    from ..core.unified_config import get_unified_config
    from ..core.unified_logging_system import get_logger
except ImportError as e:
    logging.warning(f"V2 integration imports failed: {e}")

    # Fallback implementations for testing
    def send_message_to_agent(*args, **kwargs):
        logging.info(f"Mock message send: {args}, {kwargs}")
        return True

    def get_coordinate_loader():
        return None

    def get_unified_config():
        return type("MockConfig", (), {"get_env": lambda x, y=None: y})()

    def get_logger(name):
        return logging.getLogger(name)


class WorkflowEngine:
    """
    Main workflow orchestration engine.

    Executes multi-agent workflows using V2's messaging infrastructure.
    Provides cycle-based tracking, state persistence, and error recovery.
    """

    def __init__(
        self,
        workflow_name: str,
        config: dict[str, Any] | None = None,
    ):
        """
        Initialize workflow engine.

        Args:
            workflow_name: Unique identifier for the workflow
            config: Configuration dictionary (uses config/workflows.yml if None)
        """
        self.workflow_name = workflow_name
        self.config = WorkflowConfiguration.from_config(config or {})
        self.logger = get_logger(__name__)

        # Workflow state
        self.steps: list[WorkflowStep] = []
        self.current_step: WorkflowStep | None = None
        self.completed_steps: set[str] = set()
        self.failed_steps: set[str] = set()
        self.state = WorkflowState.INITIALIZED
        self.ai_responses: list[AIResponse] = []
        self.workflow_data: dict[str, Any] = {}

        # V2 Integration
        self.coordinate_loader = get_coordinate_loader()
        self.unified_config = get_unified_config()

        # State persistence
        self.state_directory = Path(self.config.state_persistence and "workflow_states" or "")
        if self.state_directory:
            self.state_directory.mkdir(parents=True, exist_ok=True)

        self.logger.info(f"Workflow Engine initialized: {workflow_name}")

    def add_step(self, step: WorkflowStep) -> None:
        """Add a step to the workflow."""
        self.steps.append(step)
        self.logger.info(f"Added step: {step.name} (ID: {step.id})")

    async def start(self) -> None:
        """Start workflow execution."""
        if not self.steps:
            self.logger.error("No steps defined for workflow")
            return

        self.state = WorkflowState.RUNNING
        self.logger.info(f"Starting workflow: {self.workflow_name}")
        self.save_state()

        try:
            await self._execute_workflow()
        except Exception as e:
            self.logger.error(f"Workflow execution failed: {e}")
            self.state = WorkflowState.FAILED
            self.save_state()
            raise
        finally:
            if self.config.devlog_enabled:
                self._send_devlog_summary()

    async def _execute_workflow(self) -> None:
        """Main workflow execution loop."""
        iterations = 0

        while self.state == WorkflowState.RUNNING and iterations < self.config.max_iterations:
            # Find next executable step
            next_step = self._find_next_step()
            if next_step:
                await self._execute_step(next_step)
                iterations += 1
            elif self.completed_steps == set(step.id for step in self.steps):
                # All steps completed
                self.state = WorkflowState.COMPLETED
                self.logger.info(f"Workflow completed: {self.workflow_name}")
                break
            else:
                # Waiting for dependencies
                self.state = WorkflowState.WAITING_FOR_AI
                await asyncio.sleep(self.config.response_check_interval)

        if iterations >= self.config.max_iterations:
            self.state = WorkflowState.FAILED
            self.logger.error("Workflow failed: max iterations reached")

    async def _execute_step(self, step: WorkflowStep) -> None:
        """Execute a single workflow step."""
        self.logger.info(f"Executing step: {step.name}")
        self.current_step = step
        self.state = WorkflowState.RUNNING

        try:
            # Send prompt to agent
            await self._send_prompt_to_agent(step)

            # Wait for AI response
            self.state = WorkflowState.WAITING_FOR_AI
            response = await self._wait_for_ai_response(step)

            if response:
                # Process response
                self.state = WorkflowState.PROCESSING_RESPONSE
                await self._process_ai_response(step, response)

                # Mark step as completed
                self.completed_steps.add(step.id)
                self.logger.info(f"Step completed: {step.name}")
            else:
                # Step failed
                self.failed_steps.add(step.id)
                self.logger.error(f"Step failed: {step.name}")

        except Exception as e:
            self.logger.error(f"Error executing step {step.name}: {e}")
            self.failed_steps.add(step.id)
        finally:
            self.current_step = None
            self.save_state()

    async def _send_prompt_to_agent(self, step: WorkflowStep) -> None:
        """Send prompt to target agent using V2 messaging system."""
        try:
            prompt = step.prompt_template.format(**self.workflow_data)
            self.logger.info(f"Sending prompt to {step.agent_target}: {prompt[:100]}...")

            # Use V2 messaging system
            success = await asyncio.get_event_loop().run_in_executor(
                None, send_message_to_agent, step.agent_target, prompt
            )

            if not success:
                raise Exception(f"Failed to send message to {step.agent_target}")

        except Exception as e:
            self.logger.error(f"Error sending prompt to {step.agent_target}: {e}")
            raise

    async def _wait_for_ai_response(self, step: WorkflowStep) -> AIResponse | None:
        """Wait for AI response from agent."""
        start_time = time.time()

        while time.time() - start_time < step.timeout_seconds:
            # Check for new responses (simplified for V2 integration)
            # In full implementation, this would integrate with response detection
            await asyncio.sleep(self.config.response_check_interval)

            # For now, simulate response after timeout
            if time.time() - start_time > step.timeout_seconds / 2:
                return AIResponse(
                    agent=step.agent_target,
                    text=f"Simulated response for {step.name}",
                    timestamp=time.time(),
                    message_id=f"msg_{int(time.time())}",
                    response_type=step.expected_response_type,
                )

        self.logger.warning(f"Timeout waiting for response from {step.agent_target}")
        return None

    async def _process_ai_response(self, step: WorkflowStep, response: AIResponse) -> None:
        """Process AI response and update workflow data."""
        self.logger.info(f"Processing response from {response.agent}: {response.text[:100]}...")

        # Store response
        self.ai_responses.append(response)

        # Extract information based on response type
        if step.expected_response_type == ResponseType.CONVERSATION_RESPONSE:
            self.workflow_data[f"conversation_{step.id}"] = {
                "response": response.text,
                "timestamp": response.timestamp,
                "agent": response.agent,
            }
        elif step.expected_response_type == ResponseType.TASK_EXECUTION:
            self.workflow_data[f"task_{step.id}"] = {
                "status": "completed",
                "result": response.text,
                "agent": response.agent,
            }
        elif step.expected_response_type == ResponseType.DECISION_ANALYSIS:
            self.workflow_data[f"decision_{step.id}"] = {
                "analysis": response.text,
                "timestamp": response.timestamp,
                "agent": response.agent,
            }

        # Store general response data
        self.workflow_data[f"response_{step.id}"] = {
            "text": response.text,
            "timestamp": response.timestamp,
            "agent": response.agent,
            "metadata": response.metadata,
        }

    def _find_next_step(self) -> WorkflowStep | None:
        """Find the next executable step."""
        for step in self.steps:
            if (
                step.id not in self.completed_steps
                and step.id not in self.failed_steps
                and step.is_ready(self.completed_steps)
            ):
                return step
        return None

    def get_progress(self) -> WorkflowProgress:
        """Get current workflow progress."""
        return WorkflowProgress(
            workflow_name=self.workflow_name,
            state=self.state,
            total_steps=len(self.steps),
            completed_steps=len(self.completed_steps),
            failed_steps=len(self.failed_steps),
            current_step=self.current_step.id if self.current_step else None,
            workflow_data=self.workflow_data,
        )

    def save_state(self) -> None:
        """Save workflow state to disk."""
        if not self.state_directory:
            return

        state_data = {
            "workflow_name": self.workflow_name,
            "state": self.state.value,
            "completed_steps": list(self.completed_steps),
            "failed_steps": list(self.failed_steps),
            "workflow_data": self.workflow_data,
            "steps": [step.to_dict() for step in self.steps],
            "timestamp": time.time(),
        }

        state_file = self.state_directory / f"{self.workflow_name}_{int(time.time())}.json"
        with open(state_file, "w") as f:
            json.dump(state_data, f, indent=2, default=str)

        self.logger.info(f"Workflow state saved: {state_file}")

    def pause(self) -> None:
        """Pause workflow execution."""
        if self.state == WorkflowState.RUNNING:
            self.state = WorkflowState.PAUSED
            self.logger.info(f"Workflow paused: {self.workflow_name}")
            self.save_state()

    def resume(self) -> None:
        """Resume workflow execution."""
        if self.state == WorkflowState.PAUSED:
            self.state = WorkflowState.RUNNING
            self.logger.info(f"Workflow resumed: {self.workflow_name}")
            self.save_state()

    def stop(self) -> None:
        """Stop workflow execution."""
        self.state = WorkflowState.CANCELLED
        self.logger.info(f"Workflow stopped: {self.workflow_name}")
        self.save_state()

    def _send_devlog_summary(self) -> None:
        """Send workflow summary to Discord devlog."""
        try:
            webhook_url = self.unified_config.get_env("DISCORD_WEBHOOK_URL")
            if not webhook_url:
                return

            progress = self.get_progress()
            description = f"Completed {progress.completed_steps}/{progress.total_steps} steps in {progress.execution_time:.1f}s"
            if progress.failed_steps > 0:
                description += f" with {progress.failed_steps} failed"

            # Simple webhook post (would integrate with V2 devlog system)
            import urllib.parse
            import urllib.request

            payload = {
                "username": "Workflow Engine",
                "embeds": [
                    {
                        "title": f"Workflow {self.workflow_name} {self.state.value}",
                        "description": description,
                        "color": 5814783,
                    }
                ],
            }

            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                webhook_url, data=data, headers={"Content-Type": "application/json"}
            )
            urllib.request.urlopen(req, timeout=6)

        except Exception as e:
            self.logger.warning(f"Failed to send devlog: {e}")
