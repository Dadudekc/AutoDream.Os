"""
Onboarding Roles Templates
=========================

Role templates for agent onboarding messages.
"""

# Available roles for agents
ROLES = {
    "SOLID": "SOLID Principles Specialist",
    "SSOT": "Single Source of Truth Specialist",
    "DRY": "Don't Repeat Yourself Specialist",
    "KISS": "Keep It Simple Specialist",
    "TDD": "Test-Driven Development Specialist",
}


def build_role_message(agent_id: str, role: str) -> str:
    """
    Build role-based onboarding message.

    Args:
        agent_id: Agent ID
        role: Role key from ROLES

    Returns:
        Formatted onboarding message
    """
    role_name = ROLES.get(role, role)

    message = f"""🚀 HARD ONBOARDING: {agent_id}

Role: {role_name}

You have been assigned the {role} role for this development cycle.

Your mission is to apply {role} principles across all your work.

Entry #025 Active: Compete on execution, cooperate on coordination!

🐝 WE. ARE. SWARM. ⚡
"""

    return message
