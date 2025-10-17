"""Message Templates - Extracted from messaging_infrastructure.py for V2 compliance."""

CLI_HELP_EPILOG = """🐝 SWARM MESSAGING CLI
EXAMPLES: --message "..." --agent Agent-1 | --broadcast | --priority urgent
"""

SURVEY_MESSAGE_TEMPLATE = """🐝 SWARM SURVEY - SRC/ ANALYSIS
OBJECTIVE: 683→250 files consolidation
PHASES: Structural→Functional→Quality→Planning
"""

ASSIGNMENT_MESSAGE_TEMPLATE = """🐝 SURVEY ASSIGNMENT - {agent}
ROLE: {assignment}
DELIVERABLES: Analysis reports + Recommendations
"""

CONSOLIDATION_MESSAGE_TEMPLATE = """🔧 CONSOLIDATION UPDATE
BATCH: {batch} | STATUS: {status} | TIME: {timestamp}
"""

AGENT_ASSIGNMENTS = {
    "Agent-1": "Service Layer Specialist - Analyze src/services/",
    "Agent-2": "Core Systems Architect - Analyze src/core/",
    "Agent-3": "Web & API Integration - Analyze src/web/ and src/infrastructure/",
    "Agent-4": "Domain & Quality Assurance - Cross-cutting analysis + coordination",
    "Agent-5": "Trading & Gaming Systems - Analyze specialized systems",
    "Agent-6": "Testing & Infrastructure - Analyze tests/ and tools/",
    "Agent-7": "Performance & Monitoring - Analyze monitoring components",
    "Agent-8": "Integration & Coordination - Analyze integration points",
}

SWARM_AGENTS = [
    "Agent-1",
    "Agent-2",
    "Agent-3",
    "Agent-4",
    "Agent-5",
    "Agent-6",
    "Agent-7",
    "Agent-8",
]

