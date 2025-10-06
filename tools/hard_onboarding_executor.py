#!/usr/bin/env python3
"""
Hard Onboarding Execution Script - Task System Integration
=========================================================

Complete hard onboarding execution with task system integration.
V2 Compliance: ≤400 lines, single responsibility, KISS principle

Features:
- Task system integration
- FSM state management
- Agent cycle automation
- PyAutoGUI coordination
- Error handling and recovery
"""

import argparse
import json
import logging
import sys
import time
from datetime import datetime
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))
from src.core.coordination_workflow_core import Agent8CoordinationWorkflowCore
from src.services.agent_hard_onboarding import AgentHardOnboarder
from tools.cursor_task_database_integration import CursorTaskIntegrationManager

logger = logging.getLogger(__name__)


class HardOnboardingExecutor:
    """Execute hard onboarding with complete task system integration."""

    def __init__(self):
        """Initialize hard onboarding executor."""
        self.onboarder = AgentHardOnboarder()
        self.task_manager = CursorTaskIntegrationManager()
        self.coordination_manager = Agent8CoordinationWorkflowCore()

    def execute_hard_onboarding(
        self,
        agent_id: str,
        onboarding_type: str = "hard_onboard",
        priority: str = "CRITICAL",
    ) -> dict:
        """Execute complete hard onboarding sequence."""
        start_time = time.time()
        results = {
            "agent_id": agent_id,
            "onboarding_type": onboarding_type,
            "start_time": datetime.now().isoformat(),
            "success": False,
            "task_creation": False,
            "coordination_task": False,
            "pyautogui_execution": False,
            "fsm_transition": False,
            "error_message": None,
        }

        try:
            # Step 1: Create hard onboarding task
            logger.info(f"Creating hard onboarding task for {agent_id}")
            task = self.task_manager.create_hard_onboarding_task(
                agent_id=agent_id,
                onboarding_type=onboarding_type,
                priority=priority,
            )
            results["task_creation"] = True
            results["task_id"] = task.task_id

            # Step 2: Create coordination task
            logger.info(f"Creating coordination task for {agent_id}")
            coord_task_id = self.coordination_manager.create_hard_onboarding_task(
                agent_id=agent_id,
                onboarding_type=onboarding_type,
                priority=priority,
            )
            results["coordination_task"] = True
            results["coord_task_id"] = coord_task_id

            # Step 3: Execute PyAutoGUI hard onboarding
            logger.info(f"Executing PyAutoGUI hard onboarding for {agent_id}")
            pyautogui_success = self.onboarder.hard_onboard_agent(agent_id)
            results["pyautogui_execution"] = pyautogui_success

            if pyautogui_success:
                # Step 4: Update FSM state
                logger.info(f"Updating FSM state for {agent_id}")
                self.task_manager.update_task_fsm_state(
                    task.task_id, "ACTIVE", "Hard onboarding completed"
                )
                results["fsm_transition"] = True

                # Step 5: Complete coordination task
                self.coordination_manager.complete_task(coord_task_id)
                results["success"] = True

            else:
                results["error_message"] = "PyAutoGUI execution failed"

        except Exception as e:
            logger.error(f"Hard onboarding execution failed: {e}")
            results["error_message"] = str(e)

        results["end_time"] = datetime.now().isoformat()
        results["execution_time"] = time.time() - start_time

        return results

    def execute_batch_onboarding(self, agent_ids: list[str]) -> dict:
        """Execute hard onboarding for multiple agents."""
        batch_results = {
            "total_agents": len(agent_ids),
            "successful": 0,
            "failed": 0,
            "results": [],
        }

        for agent_id in agent_ids:
            logger.info(f"Starting hard onboarding for {agent_id}")
            result = self.execute_hard_onboarding(agent_id)
            batch_results["results"].append(result)

            if result["success"]:
                batch_results["successful"] += 1
            else:
                batch_results["failed"] += 1

        return batch_results

    def get_onboarding_status(self, agent_id: str) -> dict:
        """Get current onboarding status for agent."""
        try:
            # Get task status from database
            tasks = self.task_manager.get_tasks_by_agent(agent_id)
            onboarding_tasks = [t for t in tasks if t.metadata.get("hard_onboard", False)]

            # Get coordination status
            coord_tasks = self.coordination_manager.get_agent_tasks(agent_id)
            onboarding_coord_tasks = [
                t for t in coord_tasks if t.metadata.get("hard_onboard", False)
            ]

            return {
                "agent_id": agent_id,
                "onboarding_tasks": len(onboarding_tasks),
                "coordination_tasks": len(onboarding_coord_tasks),
                "latest_task_status": onboarding_tasks[-1].status.value
                if onboarding_tasks
                else "NONE",
                "latest_coord_status": onboarding_coord_tasks[-1].status.value
                if onboarding_coord_tasks
                else "NONE",
            }

        except Exception as e:
            return {"agent_id": agent_id, "error": str(e)}

    def cleanup_failed_onboarding(self, agent_id: str) -> bool:
        """Clean up failed onboarding tasks."""
        try:
            # Get failed tasks
            tasks = self.task_manager.get_tasks_by_agent(agent_id)
            failed_tasks = [
                t
                for t in tasks
                if t.metadata.get("hard_onboard", False) and t.status.value == "FAILED"
            ]

            # Clean up failed tasks
            for task in failed_tasks:
                self.task_manager.update_task_status(task.task_id, "CANCELLED")

            # Clean up coordination tasks
            coord_tasks = self.coordination_manager.get_agent_tasks(agent_id)
            failed_coord_tasks = [
                t
                for t in coord_tasks
                if t.metadata.get("hard_onboard", False) and t.status.value == "FAILED"
            ]

            for task in failed_coord_tasks:
                self.coordination_manager.cancel_task(task.task_id)

            return True

        except Exception as e:
            logger.error(f"Cleanup failed: {e}")
            return False


def main():
    """CLI entry point for hard onboarding execution."""
    parser = argparse.ArgumentParser(description="Hard Onboarding Execution")
    parser.add_argument("--agent", required=True, help="Agent ID to onboard")
    parser.add_argument("--type", default="hard_onboard", help="Onboarding type")
    parser.add_argument("--priority", default="CRITICAL", help="Task priority")
    parser.add_argument("--batch", help="Comma-separated list of agent IDs")
    parser.add_argument("--status", action="store_true", help="Get onboarding status")
    parser.add_argument("--cleanup", action="store_true", help="Cleanup failed onboarding")
    parser.add_argument("--verbose", action="store_true", help="Verbose logging")

    args = parser.parse_args()

    # Configure logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    executor = HardOnboardingExecutor()

    if args.status:
        # Get onboarding status
        status = executor.get_onboarding_status(args.agent)
        print(json.dumps(status, indent=2))

    elif args.cleanup:
        # Cleanup failed onboarding
        success = executor.cleanup_failed_onboarding(args.agent)
        print(f"Cleanup {'successful' if success else 'failed'}")

    elif args.batch:
        # Batch onboarding
        agent_ids = [aid.strip() for aid in args.batch.split(",")]
        results = executor.execute_batch_onboarding(agent_ids)
        print(json.dumps(results, indent=2))

    else:
        # Single agent onboarding
        results = executor.execute_hard_onboarding(args.agent, args.type, args.priority)
        print(json.dumps(results, indent=2))

        if results["success"]:
            print(f"✅ Hard onboarding completed for {args.agent}")
        else:
            print(f"❌ Hard onboarding failed for {args.agent}")
            sys.exit(1)


if __name__ == "__main__":
    main()

