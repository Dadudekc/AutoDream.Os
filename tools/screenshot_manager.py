#!/usr/bin/env python3
"""
Screenshot Management CLI - V2 Compliant
========================================

Automated screenshot management for V2_SWARM multi-agent coordination.
Provides structured screenshot triggers without human intervention.

Author: Agent-4 (Captain)
License: MIT
"""

import json
import logging
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

logger = logging.getLogger(__name__)


@dataclass
class ScreenshotTrigger:
    """Screenshot trigger configuration."""

    trigger_type: str  # COORDINATION, MILESTONE, CRITICAL, USER_REQUEST
    cycle_interval: int  # Every N cycles
    last_triggered: str = ""
    enabled: bool = True

    def __post_init__(self):
        if not self.last_triggered:
            self.last_triggered = datetime.now().isoformat()


class ScreenshotManager:
    """Automated screenshot management system."""

    def __init__(self, config_file: str = "config/screenshot_config.json"):
        """Initialize screenshot manager."""
        self.config_file = Path(config_file)
        self.triggers: dict[str, ScreenshotTrigger] = {}
        self.current_cycle = 0

        # Load configuration
        self._load_config()

        logger.info("Screenshot Manager initialized")

    def should_take_screenshot(self, cycle_type: str, event_type: str = "NORMAL") -> bool:
        """Determine if screenshot should be taken based on triggers."""
        try:
            # User request always triggers
            if event_type == "USER_REQUEST":
                logger.info("Screenshot triggered: User request")
                return True

            # Critical events always trigger
            if event_type in ["MAJOR_COMPLETION", "SYSTEM_FAILURE", "AGENT_ERROR"]:
                logger.info(f"Screenshot triggered: Critical event - {event_type}")
                return True

            # Check cycle-based triggers
            if cycle_type == "COORDINATION":
                coordination_trigger = self.triggers.get("COORDINATION")
                if coordination_trigger and coordination_trigger.enabled:
                    if self.current_cycle % coordination_trigger.cycle_interval == 0:
                        logger.info(
                            f"Screenshot triggered: Coordination cycle {self.current_cycle}"
                        )
                        return True

            # Check milestone triggers
            milestone_trigger = self.triggers.get("MILESTONE")
            if milestone_trigger and milestone_trigger.enabled:
                if self.current_cycle % milestone_trigger.cycle_interval == 0:
                    logger.info(f"Screenshot triggered: Milestone cycle {self.current_cycle}")
                    return True

            return False

        except Exception as e:
            logger.error(f"Error checking screenshot trigger: {e}")
            return False

    def increment_cycle(self):
        """Increment cycle counter."""
        self.current_cycle += 1
        self._save_config()
        logger.debug(f"Cycle incremented to {self.current_cycle}")

    def get_screenshot_context(self, trigger_reason: str) -> dict[str, Any]:
        """Generate screenshot context metadata."""
        return {
            "cycle_number": self.current_cycle,
            "trigger_reason": trigger_reason,
            "timestamp": datetime.now().isoformat(),
            "focus_agents": ["Agent-4", "Agent-5", "Agent-6", "Agent-7", "Agent-8"],
            "expected_content": self._get_expected_content(trigger_reason),
            "screenshot_type": self._get_screenshot_type(trigger_reason),
        }

    def configure_trigger(
        self, trigger_type: str, cycle_interval: int, enabled: bool = True
    ) -> bool:
        """Configure screenshot trigger."""
        try:
            self.triggers[trigger_type] = ScreenshotTrigger(
                trigger_type=trigger_type, cycle_interval=cycle_interval, enabled=enabled
            )
            self._save_config()
            logger.info(f"Configured trigger: {trigger_type} every {cycle_interval} cycles")
            return True

        except Exception as e:
            logger.error(f"Error configuring trigger: {e}")
            return False

    def get_status(self) -> dict[str, Any]:
        """Get screenshot manager status."""
        return {
            "current_cycle": self.current_cycle,
            "triggers": {
                trigger_type: {
                    "cycle_interval": trigger.cycle_interval,
                    "enabled": trigger.enabled,
                    "last_triggered": trigger.last_triggered,
                    "next_trigger": self._get_next_trigger_cycle(trigger),
                }
                for trigger_type, trigger in self.triggers.items()
            },
            "last_updated": datetime.now().isoformat(),
        }

    def _get_expected_content(self, trigger_reason: str) -> str:
        """Get expected screenshot content based on trigger."""
        content_map = {
            "COORDINATION": "Multi-agent coordination and A2A messages",
            "MILESTONE": "System-wide progress and agent status",
            "CRITICAL": "Error context and system state",
            "USER_REQUEST": "Specific user-requested context",
        }
        return content_map.get(trigger_reason, "General system status")

    def _get_screenshot_type(self, trigger_reason: str) -> str:
        """Get screenshot type based on trigger."""
        type_map = {
            "COORDINATION": "multi_agent_view",
            "MILESTONE": "system_overview",
            "CRITICAL": "error_context",
            "USER_REQUEST": "custom_context",
        }
        return type_map.get(trigger_reason, "general")

    def _get_next_trigger_cycle(self, trigger: ScreenshotTrigger) -> int:
        """Calculate next trigger cycle."""
        if not trigger.enabled:
            return -1

        next_cycle = ((self.current_cycle // trigger.cycle_interval) + 1) * trigger.cycle_interval
        return next_cycle

    def _load_config(self):
        """Load configuration from file."""
        try:
            if self.config_file.exists():
                with open(self.config_file) as f:
                    config_data = json.load(f)

                self.current_cycle = config_data.get("current_cycle", 0)

                # Load triggers
                triggers_data = config_data.get("triggers", {})
                for trigger_type, trigger_data in triggers_data.items():
                    self.triggers[trigger_type] = ScreenshotTrigger(**trigger_data)

                logger.info(
                    f"Loaded config: cycle {self.current_cycle}, {len(self.triggers)} triggers"
                )
            else:
                # Create default configuration
                self._create_default_config()

        except Exception as e:
            logger.error(f"Error loading config: {e}")
            self._create_default_config()

    def _save_config(self):
        """Save configuration to file."""
        try:
            # Ensure config directory exists
            self.config_file.parent.mkdir(parents=True, exist_ok=True)

            config_data = {
                "current_cycle": self.current_cycle,
                "triggers": {
                    trigger_type: {
                        "trigger_type": trigger.trigger_type,
                        "cycle_interval": trigger.cycle_interval,
                        "last_triggered": trigger.last_triggered,
                        "enabled": trigger.enabled,
                    }
                    for trigger_type, trigger in self.triggers.items()
                },
                "last_updated": datetime.now().isoformat(),
            }

            with open(self.config_file, "w") as f:
                json.dump(config_data, f, indent=2)

            logger.debug(f"Saved config: cycle {self.current_cycle}")

        except Exception as e:
            logger.error(f"Error saving config: {e}")

    def _create_default_config(self):
        """Create default configuration."""
        self.current_cycle = 0

        # Default triggers
        self.triggers = {
            "COORDINATION": ScreenshotTrigger("COORDINATION", 3),  # Every 3 cycles
            "MILESTONE": ScreenshotTrigger("MILESTONE", 10),  # Every 10 cycles
            "CRITICAL": ScreenshotTrigger("CRITICAL", 1),  # Always enabled
            "USER_REQUEST": ScreenshotTrigger("USER_REQUEST", 1),  # Always enabled
        }

        self._save_config()
        logger.info("Created default screenshot configuration")


def main():
    """CLI interface for screenshot manager."""
    import argparse

    parser = argparse.ArgumentParser(description="Screenshot Management CLI")
    parser.add_argument(
        "--check",
        nargs=2,
        metavar=("CYCLE_TYPE", "EVENT_TYPE"),
        help="Check if screenshot should be taken",
    )
    parser.add_argument("--increment", action="store_true", help="Increment cycle counter")
    parser.add_argument(
        "--configure",
        nargs=3,
        metavar=("TYPE", "INTERVAL", "ENABLED"),
        help="Configure trigger (TYPE INTERVAL true/false)",
    )
    parser.add_argument("--status", action="store_true", help="Show screenshot manager status")
    parser.add_argument("--context", help="Generate context for trigger reason")

    args = parser.parse_args()

    manager = ScreenshotManager()

    if args.check:
        cycle_type, event_type = args.check
        should_take = manager.should_take_screenshot(cycle_type, event_type)
        print(f"Screenshot needed: {'YES' if should_take else 'NO'}")
        if should_take:
            context = manager.get_screenshot_context(event_type)
            print(f"Context: {json.dumps(context, indent=2)}")

    elif args.increment:
        manager.increment_cycle()
        print(f"Cycle incremented to {manager.current_cycle}")

    elif args.configure:
        trigger_type, interval_str, enabled_str = args.configure
        interval = int(interval_str)
        enabled = enabled_str.lower() == "true"
        success = manager.configure_trigger(trigger_type, interval, enabled)
        status = "✅" if success else "❌"
        print(f"  {status} Configured {trigger_type}: every {interval} cycles, enabled={enabled}")

    elif args.status:
        status = manager.get_status()
        print("Screenshot Manager Status:")
        print(json.dumps(status, indent=2))

    elif args.context:
        context = manager.get_screenshot_context(args.context)
        print("Screenshot Context:")
        print(json.dumps(context, indent=2))

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
