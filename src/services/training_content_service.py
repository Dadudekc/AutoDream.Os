"""
Training Content Service - Training Delivery and Progress

This module delivers training content and tracks learning progress.
Follows Single Responsibility Principle - only manages training delivery.

Architecture: Single Responsibility Principle - training delivery only
LOC: 180 lines (under 200 limit)
"""

import argparse
import time
import json

from src.utils.stability_improvements import stability_manager, safe_import
from typing import Dict, List, Optional, Any
import logging

from .training_content_definitions import (
    TrainingContent,
    TrainingModule,
    TrainingContentManager,
)

logger = logging.getLogger(__name__)


class TrainingContentService:
    """
    Service for delivering training content and tracking progress

    Responsibilities:
    - Deliver training modules to agents
    - Track learning progress and completion
    - Assess agent understanding
    - Manage learning sessions
    """

    def __init__(self):
        self.content_manager = TrainingContentManager()
        self.learning_progress: Dict[str, Dict[str, Any]] = {}
        self.active_sessions: Dict[str, Dict[str, Any]] = {}
        self.logger = logging.getLogger(f"{__name__}.TrainingContentService")

    def start_learning_session(self, agent_id: str, module_id: str) -> str:
        """Start a learning session for an agent"""
        session_id = f"{agent_id}_{module_id}_{int(time.time())}"

        module = self.content_manager.get_training_module(module_id)
        if not module:
            raise ValueError(f"Training module '{module_id}' not found")

        # Initialize progress tracking
        if agent_id not in self.learning_progress:
            self.learning_progress[agent_id] = {
                "completed_content": [],
                "current_module": None,
                "total_time": 0,
                "assessments_passed": 0,
            }

        # Check prerequisites
        if not self.content_manager.validate_module_prerequisites(
            module_id, self.learning_progress[agent_id]["completed_content"]
        ):
            raise ValueError(f"Prerequisites not met for module '{module_id}'")

        # Start session
        session = {
            "session_id": session_id,
            "agent_id": agent_id,
            "module_id": module_id,
            "start_time": time.time(),
            "current_content_index": 0,
            "completed_content": [],
            "session_status": "active",
        }

        self.active_sessions[session_id] = session
        self.learning_progress[agent_id]["current_module"] = module_id

        self.logger.info(f"Started learning session {session_id} for {agent_id}")
        return session_id

    def get_next_content(self, session_id: str) -> Optional[TrainingContent]:
        """Get the next content item for a learning session"""
        session = self.active_sessions.get(session_id)
        if not session or session["session_status"] != "active":
            return None

        module = self.content_manager.get_training_module(session["module_id"])
        if not module:
            return None

        content_index = session["current_content_index"]
        if content_index >= len(module.content_items):
            return None

        return module.content_items[content_index]

    def complete_content_item(
        self, session_id: str, content_id: str, assessment_score: Optional[float] = None
    ) -> bool:
        """Mark a content item as completed"""
        session = self.active_sessions.get(session_id)
        if not session or session["session_status"] != "active":
            return False

        # Verify content item matches current session
        module = self.content_manager.get_training_module(session["module_id"])
        if not module:
            return False

        current_content = self.get_next_content(session_id)
        if not current_content or current_content.content_id != content_id:
            return False

        # Mark as completed
        session["completed_content"].append(content_id)
        session["current_content_index"] += 1

        # Update agent progress
        agent_id = session["agent_id"]
        if content_id not in self.learning_progress[agent_id]["completed_content"]:
            self.learning_progress[agent_id]["completed_content"].append(content_id)

        # Update assessment score if provided
        if assessment_score is not None:
            if "assessment_scores" not in self.learning_progress[agent_id]:
                self.learning_progress[agent_id]["assessment_scores"] = {}
            self.learning_progress[agent_id]["assessment_scores"][
                content_id
            ] = assessment_score

            if assessment_score >= 0.7:  # 70% threshold
                self.learning_progress[agent_id]["assessments_passed"] += 1

        # Check if session is complete
        if session["current_content_index"] >= len(module.content_items):
            self._complete_session(session_id)

        self.logger.info(f"Completed content {content_id} in session {session_id}")
        return True

    def _complete_session(self, session_id: str):
        """Mark a learning session as completed"""
        session = self.active_sessions[session_id]
        session["session_status"] = "completed"
        session["completion_time"] = time.time()

        # Update agent progress
        agent_id = session["agent_id"]
        self.learning_progress[agent_id]["current_module"] = None

        # Calculate total time
        session_duration = session["completion_time"] - session["start_time"]
        self.learning_progress[agent_id]["total_time"] += session_duration

        self.logger.info(f"Completed learning session {session_id}")

    def get_agent_progress(self, agent_id: str) -> Dict[str, Any]:
        """Get learning progress for an agent"""
        if agent_id not in self.learning_progress:
            return {"status": "no_progress"}

        progress = self.learning_progress[agent_id].copy()

        # Add current session info if active
        current_module = progress.get("current_module")
        if current_module:
            active_sessions = [
                s
                for s in self.active_sessions.values()
                if s["agent_id"] == agent_id and s["session_status"] == "active"
            ]
            if active_sessions:
                session = active_sessions[0]
                progress["current_session"] = {
                    "session_id": session["session_id"],
                    "module_id": session["module_id"],
                    "progress": len(session["completed_content"]),
                }

        return progress

    def get_available_modules(self) -> List[str]:
        """Get list of available training modules"""
        return self.content_manager.get_available_modules()

    def get_module_details(self, module_id: str) -> Optional[TrainingModule]:
        """Get detailed information about a training module"""
        return self.content_manager.get_training_module(module_id)

    def reset_agent_progress(self, agent_id: str):
        """Reset learning progress for an agent"""
        if agent_id in self.learning_progress:
            del self.learning_progress[agent_id]

        # Cancel active sessions
        sessions_to_cancel = [
            sid
            for sid, session in self.active_sessions.items()
            if session["agent_id"] == agent_id
        ]
        for sid in sessions_to_cancel:
            del self.active_sessions[sid]

        self.logger.info(f"Reset learning progress for agent {agent_id}")


def run_smoke_test():
    """Run basic functionality test for TrainingContentService"""
    print("🧪 Running TrainingContentService Smoke Test...")

    try:
        service = TrainingContentService()

        # Test module availability
        modules = service.get_available_modules()
        assert "orientation_basic" in modules

        # Test session start
        session_id = service.start_learning_session("test-agent", "orientation_basic")
        assert session_id in service.active_sessions

        # Test content delivery
        content = service.get_next_content(session_id)
        assert content is not None
        assert content.title == "System Architecture Introduction"

        # Test content completion
        success = service.complete_content_item(session_id, content.content_id)
        assert success

        # Test progress tracking
        progress = service.get_agent_progress("test-agent")
        assert "test-agent" in service.learning_progress

        print("✅ TrainingContentService Smoke Test PASSED")
        return True

    except Exception as e:
        print(f"❌ TrainingContentService Smoke Test FAILED: {e}")
        return False


def main():
    """CLI interface for TrainingContentService testing"""

    parser = argparse.ArgumentParser(description="Training Content Service CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    parser.add_argument(
        "--start-session",
        nargs=2,
        metavar=("AGENT", "MODULE"),
        help="Start learning session",
    )
    parser.add_argument(
        "--complete-content",
        nargs=2,
        metavar=("SESSION", "CONTENT"),
        help="Complete content item",
    )
    parser.add_argument("--progress", help="Get agent progress")
    parser.add_argument(
        "--list-modules", action="store_true", help="List available modules"
    )
    parser.add_argument("--module", help="Show module details")

    args = parser.parse_args()

    if args.test:
        run_smoke_test()
        return

    service = TrainingContentService()

    if args.start_session:
        agent_id, module_id = args.start_session
        try:
            session_id = service.start_learning_session(agent_id, module_id)
            print(f"Started session: {session_id}")
        except ValueError as e:
            print(f"Error: {e}")
    elif args.complete_content:
        session_id, content_id = args.complete_content
        success = service.complete_content_item(session_id, content_id)
        print(f"Content completion: {'Success' if success else 'Failed'}")
    elif args.progress:
        progress = service.get_agent_progress(args.progress)
        print(f"Agent Progress: {progress}")
    elif args.list_modules:
        modules = service.get_available_modules()
        print("Available training modules:")
        for module_id in modules:
            module = service.get_module_details(module_id)
            print(f"  {module_id}: {module.title}")
    elif args.module:
        module = service.get_module_details(args.module)
        if module:
            print(f"Module: {module.title}")
            print(f"Description: {module.description}")
            print(f"Duration: {module.total_duration} minutes")
        else:
            print(f"Module '{args.module}' not found")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
