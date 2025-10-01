#!/usr/bin/env python3
"""
Thea Context Templates - Strategic Consultation Context Management
================================================================

Provides structured templates for delivering project context to Thea
for strategic consultation, optimized for character limits and clarity.

Usage:
    from src.services.thea.context_templates import ProjectContextManager

    context_manager = ProjectContextManager()
    message = context_manager.create_strategic_consultation(
        question="What should be our next priority?",
        context_level="essential"
    )
"""

from dataclasses import dataclass


@dataclass
class ProjectStatus:
    """Current project status information."""

    name: str = "Dream.OS V2 Swarm System"
    phase: str = "V2 Compliance Implementation"
    agent_count: int = 8
    status: str = "Fully operational"
    key_systems: list[str] = None
    recent_achievements: list[str] = None
    current_challenges: list[str] = None

    def __post_init__(self):
        if self.key_systems is None:
            self.key_systems = [
                "FSM State Management",
                "Messaging System",
                "Discord Commander",
                "Quality Gates",
                "Thea Integration",
            ]
        if self.recent_achievements is None:
            self.recent_achievements = [
                "Documentation cleanup completed",
                "FSM implementation successful",
                "Discord Commander operational",
                "Thea system integrated",
            ]
        if self.current_challenges is None:
            self.current_challenges = [
                "Strategic direction needed",
                "Character limit optimization",
                "Context delivery optimization",
            ]


class ProjectContextManager:
    """Manages project context for Thea strategic consultation."""

    def __init__(self):
        self.project_status = ProjectStatus()

    def create_essential_context(self, question: str) -> str:
        """Create essential context message (under 200 chars)."""
        return f"""Commander Thea, this is General Agent-4.

PROJECT: {self.project_status.name}
PHASE: {self.project_status.phase}
AGENTS: {self.project_status.agent_count} specialized agents
STATUS: {self.project_status.status}

QUESTION: {question}"""

    def create_standard_context(self, question: str) -> str:
        """Create standard context message (under 500 chars)."""
        systems = ", ".join(self.project_status.key_systems[:3])
        return f"""Commander Thea, this is General Agent-4.

PROJECT: {self.project_status.name}
PHASE: {self.project_status.phase}
AGENTS: {self.project_status.agent_count} specialized agents
STATUS: {self.project_status.status}
SYSTEMS: {systems}

QUESTION: {question}

CONTEXT: We need strategic guidance for system enhancement priorities."""

    def create_detailed_context(self, question: str) -> str:
        """Create detailed context message (under 1000 chars)."""
        systems = ", ".join(self.project_status.key_systems)
        achievements = ", ".join(self.project_status.recent_achievements[:2])
        challenges = ", ".join(self.project_status.current_challenges[:2])

        return f"""Commander Thea, this is General Agent-4.

PROJECT: {self.project_status.name}
PHASE: {self.project_status.phase}
AGENTS: {self.project_status.agent_count} specialized agents
STATUS: {self.project_status.status}
SYSTEMS: {systems}

ACHIEVEMENTS: {achievements}
CHALLENGES: {challenges}

QUESTION: {question}

CONTEXT: We need strategic guidance for system enhancement priorities and next development cycle direction."""

    def create_project_scan_context(
        self, question: str, project_scan_json: str, max_chars: int = 8000
    ) -> str:
        """Create context message with project scan JSON data, respecting character limits."""
        base_message = f"""Commander Thea, this is General Agent-4.

PROJECT: {self.project_status.name}
PHASE: {self.project_status.phase}
AGENTS: {self.project_status.agent_count} specialized agents
STATUS: {self.project_status.status}

QUESTION: {question}

PROJECT_SCAN_OUTPUT:
{project_scan_json}

CONTEXT: Project scan data provided for comprehensive strategic analysis."""

        # Truncate if too long
        if len(base_message) > max_chars:
            available_chars = max_chars - len(base_message) + len(project_scan_json)
            truncated_json = (
                project_scan_json[: available_chars - 100]
                + "\n... [TRUNCATED DUE TO CHARACTER LIMIT]"
            )
            base_message = base_message.replace(project_scan_json, truncated_json)

        return base_message

    def create_strategic_consultation(self, question: str, context_level: str = "standard") -> str:
        """Create strategic consultation message with specified context level."""
        context_levels = {
            "essential": self.create_essential_context,
            "standard": self.create_standard_context,
            "detailed": self.create_detailed_context,
        }

        if context_level not in context_levels:
            raise ValueError(
                f"Invalid context level: {context_level}. Must be one of: {list(context_levels.keys())}"
            )

        return context_levels[context_level](question)

    def create_multi_turn_context(self, question: str, previous_context: str | None = None) -> str:
        """Create context for multi-turn conversation."""
        if previous_context:
            return f"""Commander Thea, following up on our previous discussion.

PREVIOUS CONTEXT: {previous_context}

NEW QUESTION: {question}

Please provide strategic guidance based on our ongoing consultation."""
        else:
            return self.create_standard_context(question)

    def create_emergency_consultation(self, issue: str) -> str:
        """Create emergency consultation message."""
        return f"""Commander Thea, this is General Agent-4 - EMERGENCY CONSULTATION.

PROJECT: {self.project_status.name}
STATUS: {self.project_status.status}

EMERGENCY ISSUE: {issue}

URGENT: We need immediate strategic guidance for crisis resolution."""

    def create_status_report(self, additional_status: dict | None = None) -> str:
        """Create comprehensive status report."""
        status_info = additional_status or {}

        report = f"""Commander Thea, this is General Agent-4 with status report.

PROJECT: {self.project_status.name}
PHASE: {self.project_status.phase}
AGENTS: {self.project_status.agent_count} specialized agents
STATUS: {self.project_status.status}
SYSTEMS: {", ".join(self.project_status.key_systems)}

ACHIEVEMENTS: {", ".join(self.project_status.recent_achievements)}
CHALLENGES: {", ".join(self.project_status.current_challenges)}"""

        if status_info:
            report += "\n\nADDITIONAL STATUS:"
            for key, value in status_info.items():
                report += f"\n{key.upper()}: {value}"

        report += "\n\nPlease provide strategic guidance on next priorities."

        return report

    def get_context_stats(self, message: str) -> dict[str, int]:
        """Get statistics about context message."""
        return {
            "characters": len(message),
            "words": len(message.split()),
            "lines": len(message.split("\n")),
            "estimated_tokens": len(message.split()) * 1.3,  # Rough estimate
        }

    def optimize_for_limits(self, message: str, max_chars: int = 500) -> str:
        """Optimize message for character limits."""
        if len(message) <= max_chars:
            return message

        # Try to reduce context level
        if "SYSTEMS:" in message and len(message) > max_chars:
            # Remove some systems
            lines = message.split("\n")
            for i, line in enumerate(lines):
                if line.startswith("SYSTEMS:"):
                    systems = line.split(": ")[1].split(", ")
                    if len(systems) > 2:
                        lines[i] = f"SYSTEMS: {', '.join(systems[:2])}"
                    break
            message = "\n".join(lines)

        if len(message) <= max_chars:
            return message

        # Further reduction - remove achievements/challenges
        if "ACHIEVEMENTS:" in message:
            lines = message.split("\n")
            lines = [
                line for line in lines if not line.startswith(("ACHIEVEMENTS:", "CHALLENGES:"))
            ]
            message = "\n".join(lines)

        if len(message) <= max_chars:
            return message

        # Final reduction - essential context only
        return self.create_essential_context(
            message.split("QUESTION: ")[-1]
            if "QUESTION: " in message
            else "Strategic guidance needed"
        )


# Pre-defined consultation templates
STRATEGIC_TEMPLATES = {
    "priority_guidance": "What strategic direction should we prioritize for the next development cycle?",
    "system_enhancement": "What should be our next priority for system enhancement?",
    "resource_allocation": "How should we allocate resources across our 8 specialized agents?",
    "technical_architecture": "What architectural improvements should we consider for scalability?",
    "quality_improvement": "What quality improvements should we prioritize for V2 compliance?",
    "integration_strategy": "What integration strategies should we implement for better coordination?",
    "crisis_management": "How should we handle system degradation or agent failures?",
    "future_planning": "What long-term strategic goals should we establish for the swarm system?",
}


def create_quick_consultation(template_key: str, context_level: str = "standard") -> str:
    """Create quick consultation using pre-defined templates."""
    if template_key not in STRATEGIC_TEMPLATES:
        raise ValueError(
            f"Invalid template key: {template_key}. Available: {list(STRATEGIC_TEMPLATES.keys())}"
        )

    context_manager = ProjectContextManager()
    return context_manager.create_strategic_consultation(
        STRATEGIC_TEMPLATES[template_key], context_level
    )


# Example usage
if __name__ == "__main__":
    context_manager = ProjectContextManager()

    # Test different context levels
    print("Essential Context:")
    print(context_manager.create_essential_context("What should be our next priority?"))
    print(
        f"Characters: {len(context_manager.create_essential_context('What should be our next priority?'))}"
    )
    print()

    print("Standard Context:")
    print(context_manager.create_standard_context("What should be our next priority?"))
    print(
        f"Characters: {len(context_manager.create_standard_context('What should be our next priority?'))}"
    )
    print()

    print("Detailed Context:")
    print(context_manager.create_detailed_context("What should be our next priority?"))
    print(
        f"Characters: {len(context_manager.create_detailed_context('What should be our next priority?'))}"
    )
    print()

    # Test quick consultation
    print("Quick Consultation:")
    print(create_quick_consultation("priority_guidance", "standard"))
    print(f"Characters: {len(create_quick_consultation('priority_guidance', 'standard'))}")
