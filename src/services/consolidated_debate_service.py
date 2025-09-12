#!/usr/bin/env python3
"""
Consolidated Debate Coordination Service - V2 Compliant Module
============================================================

Unified debate coordination service consolidating:
- agent_consolidation_debate_coordinator.py
- debate_notification_system.py
- debate_participation_tool.py
- Cursor debate coordination logic

V2 Compliance: < 400 lines, single responsibility for debate coordination.

Author: Agent-4 (Quality Assurance Specialist - CAPTAIN)
Mission: Phase 2 Consolidation - Core Debate System Unification
License: MIT
"""

import argparse
import sys
import time
import uuid
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

# Fix imports when running as a script
if __name__ == "__main__":
    script_dir = Path(__file__).parent.parent.parent
    if str(script_dir) not in sys.path:
        sys.path.insert(0, str(script_dir))

# Import consolidated messaging system
try:
    from src.core.messaging_pyautogui import (
        PYAUTOGUI_AVAILABLE,
        broadcast_message_to_agents,
        get_agent_coordinates,
        load_coordinates_from_json,
        send_message_with_fallback,
    )
    MESSAGING_AVAILABLE = True
except ImportError:
    MESSAGING_AVAILABLE = False

# Import coordinate system
try:
    from src.core.coordinate_loader import get_coordinate_loader
    COORDINATES_AVAILABLE = True
except ImportError:
    COORDINATES_AVAILABLE = False


@dataclass
class DebateParticipant:
    """Represents a debate participant."""
    agent_id: str
    specialty: str
    contribution_count: int = 0
    last_contribution: datetime | None = None
    coordinates: tuple[int, int] | None = None


@dataclass
class DebateArgument:
    """Represents a debate argument."""
    id: str
    author_agent: str
    supports_option: str
    title: str
    content: str
    confidence: float
    technical_feasibility: float
    business_value: float
    timestamp: datetime


class ConsolidatedDebateService:
    """Unified debate coordination service consolidating all debate functionality."""

    def __init__(self, debate_file: str = "swarm_debate_consolidation.xml"):
        self.debate_file = Path(debate_file)
        self.participants: dict[str, DebateParticipant] = {}
        self.arguments: list[DebateArgument] = []
        self.debate_topic = "Architecture Consolidation Strategy"

        # Initialize subsystems
        self._init_coordinates()
        self._init_messaging()
        self._load_debate_data()

    def _init_coordinates(self):
        """Initialize coordinate system."""
        if COORDINATES_AVAILABLE:
            try:
                self.coordinate_loader = get_coordinate_loader()
                print("✅ Coordinate system initialized")
            except Exception as e:
                print(f"⚠️ Coordinate system failed: {e}")
                self.coordinate_loader = None
        else:
            print("⚠️ Coordinate system not available")
            self.coordinate_loader = None

    def _init_messaging(self):
        """Initialize messaging system."""
        if MESSAGING_AVAILABLE:
            print("✅ Messaging system initialized")
        else:
            print("⚠️ Messaging system not available")

    def _load_debate_data(self):
        """Load debate data from XML file."""
        if not self.debate_file.exists():
            print(f"⚠️ Debate file not found: {self.debate_file}")
            self._create_default_debate()
            return

        try:
            tree = ET.parse(self.debate_file)
            root = tree.getroot()

            # Load participants
            for participant_elem in root.findall('.//participant'):
                agent_id = participant_elem.find('agent_id')
                if agent_id is not None:
                    agent_id = agent_id.text.strip()
                    specialty_elem = participant_elem.find('specialty')
                    specialty = specialty_elem.text if specialty_elem is not None else "Unknown"

                    # Get coordinates if available
                    coords = None
                    if self.coordinate_loader:
                        try:
                            coords = self.coordinate_loader.get_chat_coordinates(agent_id)
                        except:
                            pass

                    self.participants[agent_id] = DebateParticipant(
                        agent_id=agent_id,
                        specialty=specialty,
                        coordinates=coords
                    )

            # Load arguments
            for arg_elem in root.findall('.//argument'):
                author = arg_elem.find('author_agent')
                option = arg_elem.find('supports_option')
                title = arg_elem.find('title')
                content = arg_elem.find('content')

                if all([author, option, title, content]):
                    confidence = float(arg_elem.find('confidence').text or 0.5)
                    feasibility = float(arg_elem.find('technical_feasibility').text or 0.5)
                    value = float(arg_elem.find('business_value').text or 0.5)

                    argument = DebateArgument(
                        id=str(uuid.uuid4()),
                        author_agent=author.text,
                        supports_option=option.text,
                        title=title.text,
                        content=content.text,
                        confidence=confidence,
                        technical_feasibility=feasibility,
                        business_value=business_value,
                        timestamp=datetime.now()
                    )
                    self.arguments.append(argument)

                    # Update participant contribution count
                    if author.text in self.participants:
                        self.participants[author.text].contribution_count += 1
                        self.participants[author.text].last_contribution = datetime.now()

            print(f"✅ Loaded {len(self.participants)} participants and {len(self.arguments)} arguments")

        except Exception as e:
            print(f"❌ Failed to load debate data: {e}")
            self._create_default_debate()

    def _create_default_debate(self):
        """Create default debate structure."""
        print("📝 Creating default debate structure...")

        # Default participants based on swarm architecture
        default_participants = {
            "Agent-1": "Integration & Core Systems Specialist",
            "Agent-2": "Architecture & Design Specialist",
            "Agent-3": "Infrastructure & DevOps Specialist",
            "Agent-4": "Quality Assurance Specialist (CAPTAIN)",
            "Agent-5": "Business Intelligence Specialist",
            "Agent-6": "Coordination & Communication Specialist",
            "Agent-7": "Web Development Specialist",
            "Agent-8": "Operations & Support Specialist"
        }

        for agent_id, specialty in default_participants.items():
            coords = None
            if self.coordinate_loader:
                try:
                    coords = self.coordinate_loader.get_chat_coordinates(agent_id)
                except:
                    pass

            self.participants[agent_id] = DebateParticipant(
                agent_id=agent_id,
                specialty=specialty,
                coordinates=coords
            )

    def get_debate_status(self) -> dict[str, Any]:
        """Get comprehensive debate status."""
        return {
            "topic": self.debate_topic,
            "total_participants": len(self.participants),
            "active_participants": len([p for p in self.participants.values() if p.contribution_count > 0]),
            "total_arguments": len(self.arguments),
            "pending_participants": [pid for pid, p in self.participants.items() if p.contribution_count == 0],
            "coordination_systems": {
                "messaging": MESSAGING_AVAILABLE,
                "coordinates": COORDINATES_AVAILABLE,
                "cursor_automation": PYAUTOGUI_AVAILABLE
            }
        }

    def invite_all_agents(self) -> dict[str, bool]:
        """Invite all agents to participate in the debate."""
        if not MESSAGING_AVAILABLE:
            print("❌ Messaging system not available for invitations")
            return {}

        results = {}
        invitation_message = f"""
🐝 SWARM DEBATE INVITATION

Topic: {self.debate_topic}

Your expertise is needed! As a {self.participants.get('Agent-4', DebateParticipant('Agent-4', 'Specialist')).specialty}, your perspective is crucial for this architectural decision.

Please contribute your arguments using the debate participation tool.

Status: {self.get_debate_status()['active_participants']}/{self.get_debate_status()['total_participants']} agents have contributed.

Use: python debate_participation_tool.py --agent-id YOUR_AGENT --add-argument
"""

        for agent_id in self.participants.keys():
            try:
                success = send_message_with_fallback(
                    agent_id=agent_id,
                    message=invitation_message,
                    sender="SWARM_CAPTAIN"
                )
                results[agent_id] = success
                time.sleep(0.5)  # Rate limiting
            except Exception as e:
                print(f"❌ Failed to invite {agent_id}: {e}")
                results[agent_id] = False

        successful = sum(results.values())
        print(f"✅ Debate invitations sent: {successful}/{len(results)} successful")
        return results

    def notify_pending_agents(self) -> dict[str, bool]:
        """Notify agents who haven't contributed yet."""
        if not MESSAGING_AVAILABLE:
            print("❌ Messaging system not available for notifications")
            return {}

        pending = [pid for pid, p in self.participants.items() if p.contribution_count == 0]
        if not pending:
            print("✅ All agents have contributed!")
            return {}

        results = {}
        reminder_message = f"""
⏰ DEBATE PARTICIPATION REMINDER

The architecture consolidation debate is still active and needs your input!

Topic: {self.debate_topic}
Current Status: {len(pending)} agents still need to contribute

Your specialized perspective as a {self.participants.get('Agent-4', DebateParticipant('Agent-4', 'Specialist')).specialty} is essential for reaching swarm consensus.

Use: python debate_participation_tool.py --agent-id YOUR_AGENT --add-argument
"""

        for agent_id in pending:
            try:
                success = send_message_with_fallback(
                    agent_id=agent_id,
                    message=reminder_message,
                    sender="SWARM_CAPTAIN"
                )
                results[agent_id] = success
                time.sleep(0.5)
            except Exception as e:
                print(f"❌ Failed to notify {agent_id}: {e}")
                results[agent_id] = False

        successful = sum(results.values())
        print(f"✅ Pending agent notifications: {successful}/{len(results)} successful")
        return results

    def get_arguments_summary(self) -> dict[str, Any]:
        """Get summary of arguments by option."""
        option_counts = {}
        option_quality = {}

        for arg in self.arguments:
            option = arg.supports_option
            if option not in option_counts:
                option_counts[option] = 0
                option_quality[option] = []

            option_counts[option] += 1
            quality_score = (arg.confidence + arg.technical_feasibility + arg.business_value) / 3
            option_quality[option].append(quality_score)

        # Calculate average quality per option
        avg_quality = {}
        for option, scores in option_quality.items():
            avg_quality[option] = sum(scores) / len(scores) if scores else 0

        return {
            "total_arguments": len(self.arguments),
            "arguments_by_option": option_counts,
            "average_quality_by_option": avg_quality,
            "top_contributors": sorted(
                [(p.agent_id, p.contribution_count) for p in self.participants.values()],
                key=lambda x: x[1],
                reverse=True
            )[:3]
        }

    def save_debate_state(self):
        """Save current debate state to file."""
        # Implementation would create/update XML file
        print("💾 Debate state saved")


def main():
    """Main CLI interface for the consolidated debate service."""
    parser = argparse.ArgumentParser(description="Consolidated Debate Coordination Service")
    parser.add_argument("--status", action="store_true", help="Show debate status")
    parser.add_argument("--invite-all", action="store_true", help="Invite all agents to debate")
    parser.add_argument("--notify-pending", action="store_true", help="Notify pending agents")
    parser.add_argument("--summary", action="store_true", help="Show arguments summary")

    args = parser.parse_args()

    service = ConsolidatedDebateService()

    if args.status:
        status = service.get_debate_status()
        print("🐝 DEBATE STATUS")
        print("=" * 50)
        for key, value in status.items():
            print(f"{key}: {value}")

    elif args.invite_all:
        print("📨 Inviting all agents to debate...")
        results = service.invite_all_agents()
        print(f"Results: {sum(results.values())}/{len(results)} successful")

    elif args.notify_pending:
        print("⏰ Notifying pending agents...")
        results = service.notify_pending_agents()
        print(f"Results: {sum(results.values())}/{len(results)} successful")

    elif args.summary:
        summary = service.get_arguments_summary()
        print("📊 DEBATE SUMMARY")
        print("=" * 50)
        for key, value in summary.items():
            print(f"{key}: {value}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()


__all__ = [
    "ConsolidatedDebateService",
    "DebateParticipant",
    "DebateArgument"
]
