"""
Messaging CLI Templates
======================
Message templates for CLI operations. Extracted for V2 compliance.

Author: Agent-5 (extracted from Agent-6's messaging_cli.py)
License: MIT
"""

CLI_HELP_EPILOG = """
🐝 SWARM MESSAGING CLI - COMMAND YOUR AGENTS!
==============================================

EXAMPLES:
--------
# Send message to specific agent
python -m src.services.messaging_cli --message "Start survey" --agent Agent-1
# Broadcast to all agents
python -m src.services.messaging_cli --message "SWARM ALERT!" --broadcast
# Send with priority and tags
python -m src.services.messaging_cli --message "URGENT: Fix issue" \\
    --agent Agent-2 --priority urgent --tags bug critical

🐝 WE. ARE. SWARM - COORDINATE THROUGH PYAUTOGUI!
"""

SURVEY_MESSAGE_TEMPLATE = """
🐝 SWARM SURVEY INITIATED - SRC/ DIRECTORY ANALYSIS
================================================

**OBJECTIVE:** Comprehensive analysis of src/ directory for consolidation planning
**TARGET:** 683 → ~250 files with full functionality preservation

**PHASES:**
1. Structural Analysis (Directories, files, dependencies)
2. Functional Analysis (Services, capabilities, relationships)
3. Quality Assessment (V2 compliance, violations, anti-patterns)
4. Consolidation Planning (Opportunities, risks, rollback strategies)

**COORDINATION:** Real-time via PyAutoGUI messaging system
**COMMANDER:** Captain Agent-4 (Quality Assurance Specialist)

🐝 WE ARE SWARM - UNITED IN ANALYSIS!
"""

ASSIGNMENT_MESSAGE_TEMPLATE = """
🐝 SURVEY ASSIGNMENT - {agent}
============================

**ROLE:** {assignment}

**DELIVERABLES:**
1. Structural Analysis Report
2. Functional Analysis Report
3. Quality Assessment Report
4. Consolidation Recommendations

**TIMELINE:** 8 days total survey
**COORDINATION:** Real-time via PyAutoGUI

🐝 YOUR EXPERTISE IS CRUCIAL FOR SUCCESSFUL CONSOLIDATION!
"""

CONSOLIDATION_MESSAGE_TEMPLATE = """
🔧 CONSOLIDATION UPDATE
======================

**BATCH:** {batch}
**STATUS:** {status}
**TIMESTAMP:** {timestamp}

**COORDINATION:** Real-time swarm coordination active
**COMMANDER:** Captain Agent-4

🔧 CONSOLIDATION PROGRESS CONTINUES...
"""
