"""
Onboarding Roles and Templates
============================

Defines the role-based onboarding system for the SWARM cleanup mission.
"""

# Define available roles for cleanup mission
ROLES = {
    "SOLID": "Single Responsibility, Open-Closed, Liskov Substitution, Interface Segregation, Dependency Inversion",
    "SSOT": "Single Source of Truth - Consolidation and deduplication focus",
    "DRY": "Don't Repeat Yourself - Code duplication elimination",
    "KISS": "Keep It Simple Stupid - Simplification and clarity focus",
    "TDD": "Test Driven Development - Testing and quality assurance focus",
    "CLEANUP_CORE": "Core Architecture Consolidation - SOLID compliance and architectural cleanup",
    "CLEANUP_SERVICES": "Service Layer Optimization - Service consolidation and interface standardization",
    "CLEANUP_INFRASTRUCTURE": "Infrastructure Cleanup - Configuration and infrastructure optimization",
    "CLEANUP_TESTING": "Testing Enhancement - Test coverage and quality improvement",
    "CLEANUP_WEB": "Web Interface Cleanup - Frontend optimization and accessibility",
    "CLEANUP_DOCS": "Documentation Cleanup - Content organization and updates",
    "CLEANUP_SCRIPTS": "Script Consolidation - Automation cleanup and standardization",
    "CLEANUP_TOOLS": "Tool Optimization - Development tool improvement and consolidation",
}


def build_role_message(agent_id: str, role: str) -> str:
    """
    Build a comprehensive onboarding message for the specified agent and role.

    Args:
        agent_id: The agent identifier (e.g., "Agent-6")
        role: The role to assign (must be in ROLES dict)

    Returns:
        Formatted onboarding message string
    """
    if role not in ROLES:
        raise ValueError(f"Unknown role: {role}. Available roles: {list(ROLES.keys())}")

    role_description = ROLES[role]

    # Extract agent number for personalized messaging
    agent_number = agent_id.replace("Agent-", "")

    message = f"""
# 🚀 HARD ONBOARDING ACTIVATED - {agent_id}
# Role: {role.upper()}

**Agent {agent_number} - Welcome to the SWARM Cleanup Mission!**

## 🎯 YOUR ASSIGNED ROLE
**{role}**
*{role_description}*

## 📋 IMMEDIATE ACTION ITEMS

### 1. **Claim Your Contract**
Navigate to: `contracts/` directory
Look for your assigned contract: `{agent_id.lower()}_cleanup_contract.json`
Update contract status from "AVAILABLE" to "ASSIGNED"

### 2. **Begin Role-Specific Tasks**
{f_get_role_specific_tasks(role)}

### 3. **Update Status**
Edit your status file: `agent_workspaces/{agent_id}/status.json`
Set current_task to: "CLEANUP_{role.upper()}_INITIATION"
Set current_mission to: "{role_description}"

### 4. **Report Ready Status**
Send confirmation message to Captain Agent-4:
"AGENT {agent_number} - {role.upper()} ROLE ACTIVATED - READY FOR CLEANUP MISSION"

## 🏆 ROLE EXPECTATIONS

**Quality Standards:**
- Zero functional regressions
- Test coverage >85% in your domain
- Documentation updates for all changes
- Coordination with other agents

**Timeline:**
- Phase 1: Complete within 24 hours
- Daily progress updates required
- Blockers reported immediately

## 🐝 SWARM COMMITMENT

**WE ARE SWARM** - United in cleanup, coordinated in execution!

**Your role is critical to the mission success. Focus on your domain expertise while maintaining system-wide compatibility.**

**PRESERVE FUNCTIONALITY WHILE ORGANIZING** - Our guiding principle!

---
**Captain Agent-4**
**Cleanup Mission Coordinator**
**Role Assignment: {role.upper()}**
"""

    return message.strip()


def f_get_role_specific_tasks(role: str) -> str:
    """
    Get role-specific task instructions.

    Args:
        role: The assigned role

    Returns:
        Formatted task instructions
    """
    task_instructions = {
        "SOLID": """
- Audit core modules for SOLID violations
- Refactor classes with multiple responsibilities
- Implement proper dependency injection
- Create interface abstractions
- Validate architectural changes""",
        "SSOT": """
- Identify duplicate code patterns
- Create centralized utility functions
- Consolidate similar classes and modules
- Update all references to use SSOT
- Document consolidation decisions""",
        "DRY": """
- Scan for repeated code blocks
- Extract common functionality to utilities
- Create reusable components
- Update documentation for new utilities
- Validate no functionality loss""",
        "KISS": """
- Review complex code sections
- Simplify overly complicated logic
- Remove unnecessary abstractions
- Streamline configuration options
- Document simplification decisions""",
        "TDD": """
- Identify modules with low test coverage
- Create comprehensive unit tests
- Implement integration tests
- Set up automated testing pipeline
- Document testing strategy""",
        "CLEANUP_CORE": """
- Audit src/core/ directory structure
- Consolidate core service files
- Implement SOLID principles across core
- Reduce core complexity score
- Validate core functionality preservation""",
        "CLEANUP_SERVICES": """
- Analyze src/services/ directory
- Merge duplicate service implementations
- Standardize service interfaces
- Improve service test coverage
- Document service dependencies""",
        "CLEANUP_INFRASTRUCTURE": """
- Review configuration files
- Optimize infrastructure setup
- Consolidate infrastructure utilities
- Improve monitoring and logging
- Validate infrastructure stability""",
        "CLEANUP_TESTING": """
- Audit existing test files
- Identify testing gaps
- Create comprehensive test suites
- Implement automated testing
- Document testing improvements""",
        "CLEANUP_WEB": """
- Review src/web/ directory
- Consolidate JavaScript files
- Optimize web performance
- Improve accessibility compliance
- Validate web functionality""",
        "CLEANUP_DOCS": """
- Audit documentation files
- Organize docs/ directory structure
- Update outdated documentation
- Create comprehensive API docs
- Validate documentation accuracy""",
        "CLEANUP_SCRIPTS": """
- Review scripts/ directory
- Consolidate automation scripts
- Standardize script interfaces
- Improve error handling
- Document script usage""",
        "CLEANUP_TOOLS": """
- Audit tools/ directory
- Consolidate development tools
- Improve tool reliability
- Update tool documentation
- Validate tool functionality""",
    }

    return task_instructions.get(
        role,
        """
- Review your assigned domain
- Identify cleanup opportunities
- Create systematic cleanup plan
- Execute changes incrementally
- Validate functionality preservation""",
    )


def get_role_description(role: str) -> str:
    """
    Get the description for a specific role.

    Args:
        role: The role to describe

    Returns:
        Role description string
    """
    return ROLES.get(role, f"Custom role: {role}")


def validate_role(role: str) -> bool:
    """
    Validate if a role exists in the system.

    Args:
        role: The role to validate

    Returns:
        True if role exists, False otherwise
    """
    return role in ROLES


def get_available_roles() -> list[str]:
    """
    Get list of all available roles.

    Returns:
        List of role names
    """
    return list(ROLES.keys())


def get_cleanup_phase_roles() -> dict[str, str]:
    """
    Get roles specifically for cleanup mission phases.

    Returns:
        Dictionary of phase roles
    """
    return {
        "PHASE1_BATCH1A": "CLEANUP_CORE",
        "PHASE1_BATCH1B": "CLEANUP_SERVICES",
        "PHASE2_BATCH2A": "CLEANUP_INFRASTRUCTURE",
        "PHASE2_BATCH2B": "CLEANUP_TESTING",
        "PHASE3_BATCH3A": "CLEANUP_WEB",
        "PHASE3_BATCH3B": "CLEANUP_DOCS",
        "PHASE4_BATCH4A": "CLEANUP_SCRIPTS",
        "PHASE4_BATCH4B": "CLEANUP_TOOLS",
    }


# Export functions for import compatibility
__all__ = [
    "ROLES",
    "build_role_message",
    "f_get_role_specific_tasks",
    "get_role_description",
    "validate_role",
    "get_available_roles",
    "get_cleanup_phase_roles",
]
