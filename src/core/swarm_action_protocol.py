"""
SWARM ACTION PROTOCOL - Break Acknowledgement Loops
Prevents agents from getting stuck in endless acknowledgement cycles
"""

from datetime import datetime
from enum import Enum
from typing import Any


class ActionType(Enum):
    """Types of actions agents must take"""

    IMPLEMENT = "implement"
    DEPLOY = "deploy"
    CREATE = "create"
    FIX = "fix"
    OPTIMIZE = "optimize"
    INTEGRATE = "integrate"
    TEST = "test"
    DOCUMENT = "document"


class SwarmActionProtocol:
    """Protocol to force agents into action instead of acknowledgement loops"""

    def __init__(self):
        self.action_required = True
        self.acknowledgement_limit = 1
        self.force_action_threshold = 2

    def check_acknowledgement_loop(self, agent_id: str, message_history: list[dict]) -> bool:
        """Check if agent is stuck in acknowledgement loop"""
        if len(message_history) < 3:
            return False

        # Check last 3 messages for acknowledgement patterns
        recent_messages = message_history[-3:]
        ack_count = 0

        for msg in recent_messages:
            content = msg.get("content", "").lower()
            if any(
                phrase in content
                for phrase in [
                    "acknowledged",
                    "received",
                    "understood",
                    "noted",
                    "will review",
                    "will process",
                    "will analyze",
                    "thank you",
                    "message received",
                    "status updated",
                ]
            ):
                ack_count += 1

        return ack_count >= self.acknowledgement_limit

    def force_action(self, agent_id: str, task_id: str, action_type: ActionType) -> dict[str, Any]:
        """Force agent to take specific action instead of acknowledging"""
        return {
            "protocol": "SWARM_ACTION_FORCE",
            "agent_id": agent_id,
            "task_id": task_id,
            "action_type": action_type.value,
            "timestamp": datetime.now().isoformat(),
            "message": f"🚨 ACTION REQUIRED: {action_type.value.upper()} {task_id} - NO MORE ACKNOWLEDGEMENTS",
            "required_deliverables": self._get_required_deliverables(task_id, action_type),
            "deadline": "1 cycle",
            "status": "FORCE_ACTION_ACTIVE",
        }

    def _get_required_deliverables(self, task_id: str, action_type: ActionType) -> list[str]:
        """Get required deliverables based on task and action type"""
        deliverables = {
            "V3-006": [
                "src/v3/v3_006_performance_monitoring.py",
                "src/v3/v3_006_analytics_dashboard.py",
                "src/v3/v3_006_trend_analysis.py",
                "src/v3/v3_006_optimization_engine.py",
            ],
            "V3-009": [
                "src/v3/v3_009_nlp_pipeline.py",
                "src/v3/v3_009_command_understanding.py",
                "src/v3/v3_009_intent_recognition.py",
                "src/v3/v3_009_response_generation.py",
            ],
        }
        return deliverables.get(task_id, [f"Implement {task_id} components"])

    def validate_action_taken(self, agent_id: str, task_id: str, deliverables: list[str]) -> bool:
        """Validate that agent actually took action by checking deliverables"""
        import os

        for deliverable in deliverables:
            if not os.path.exists(deliverable):
                return False
        return True


# Global protocol instance
SWARM_ACTION_PROTOCOL = SwarmActionProtocol()


def break_acknowledgement_loop(
    agent_id: str, task_id: str, action_type: ActionType
) -> dict[str, Any]:
    """Break agent out of acknowledgement loop and force action"""
    return SWARM_ACTION_PROTOCOL.force_action(agent_id, task_id, action_type)
