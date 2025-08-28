"""Central configuration for test categories."""
from typing import Any, Dict


TEST_CATEGORIES: Dict[str, Dict[str, Any]] = {
    "smoke": {
        "description": "Smoke tests for basic functionality validation",
        "marker": "smoke",
        "timeout": 60,
        "critical": True,
        "directory": "smoke",
    },
    "unit": {
        "description": "Unit tests for individual components",
        "marker": "unit",
        "timeout": 120,
        "critical": True,
        "directory": "unit",
    },
    "integration": {
        "description": "Integration tests for component interaction",
        "marker": "integration",
        "timeout": 300,
        "critical": False,
        "directory": "integration",
    },
    "performance": {
        "description": "Performance and load testing",
        "marker": "performance",
        "timeout": 600,
        "critical": False,
        "directory": "performance",
    },
    "security": {
        "description": "Security and vulnerability testing",
        "marker": "security",
        "timeout": 180,
        "critical": True,
        "directory": "security",
    },
    "api": {
        "description": "API endpoint testing",
        "marker": "api",
        "timeout": 240,
        "critical": False,
        "directory": "api",
    },
    "behavior": {
        "description": "Behavior tree tests",
        "marker": "behavior",
        "timeout": 120,
        "critical": False,
        "directory": "behavior_trees",
    },
    "decision": {
        "description": "Decision engine tests",
        "marker": "decision",
        "timeout": 120,
        "critical": False,
        "directory": "decision_engines",
    },
    "coordination": {
        "description": "Multi-agent coordination tests",
        "marker": "coordination",
        "timeout": 180,
        "critical": False,
        "directory": "multi_agent",
    },
    "learning": {
        "description": "Learning component tests",
        "marker": "learning",
        "timeout": 180,
        "critical": False,
        "directory": "learning",
    },
}
