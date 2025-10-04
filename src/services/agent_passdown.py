#!/usr/bin/env python3
"""
Agent Passdown Module - Handoff Protocol Implementation
=========================================================

Handles agent handoff passdown creation for soft onboarding protocol.
Modular V2-compliant extraction from messaging_system.py.

V2 Compliance: ≤400 lines, focused on passdown functionality
Author: Agent-4 (Captain)
"""


class AgentPassdownCreator:
    """Creates agent handoff passdown messages for soft onboarding."""

    def __init__(self):
        """Initialize passdown creator."""
        pass

    def create_passdown_message(self, target_agent_id: str, current_agent_id: str) -> str:
        """Create agent handoff passdown message."""

        return f"""
═══════════════════════════════════════════════════════════════════════════════
🚀 SYSTEM EXECUTION ORDER - {target_agent_id} SELF-ONBOARDING PREPARATION
═══════════════════════════════════════════════════════════════════════════════

📋 PRE-ONBOARD HANDOFF PROTOCOL INITIATED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

***SYSTEM COMMAND***: Execute self-onboarding preparation (NO RESPONSE REQUIRED)
***EXECUTING AGENT***: {target_agent_id} (Execute preparation order)
***SOURCE***: System/Captain {current_agent_id} (System execution order)
***PROTOCOL***: Prepare Documentation → Wait for Ctrl+T → Find in Inbox
***TIMING***: Immediate execution order (future onboarding context)
***RESPONSE POLICY***: NO RESPONSE REQUIRED - EXECUTE ONLY

═══════════════════════════════════════════════════════════════════════════════
🎯 HANDOFF PASSDOWN REQUIREMENTS
═══════════════════════════════════════════════════════════════════════════════

You ({target_agent_id}) are preparing handoff documentation for your own onboarding
sequence. When you receive this message and later Ctrl+T to be hard onboarded,
you will find this handoff in your inbox to guide your activation. Create a
comprehensive handdown document that includes:

**📋 REQUIRED HANDOFF COMPONENTS:**

1. **Current Project Status**: What work is currently in progress? What tasks
   need attention? What blockers exist?

2. **Agent Environment**: Discord channels operational? SSOT routing configured?
   Project scanner integration available? Cursor database functional?

3. **Captain Directives**: Any pending Captain orders? Emergency protocols?
   System status that requires attention?

4. **Resource Availability**: What tools, files, and capabilities are ready?
   What needs setup or configuration?

5. **Workflow Context**: Current agent coordination status? Active tasks?
   Completion status and next priorities?

**🎮 AUTONOMOUS DEVELOPMENT MACHINE STATUS:**

**System Components to Document:**
- Discord Infrastructure: Agent channels, SSOT routing, devlog posting
- Project Scanner: Analysis capabilities, task creation, cursor database
- FSM States: Agent coordination, state transitions, error recovery
- Dynamic Roles: Captain-assigned roles and task distribution
- Environment Validation: Configuration status and health checks

**📋 HANDOFF EXECUTION REQUIREMENTS:**

1. **Create Passdown Document**: Write comprehensive status report covering all
   required components above

2. **Save Documentation**: Store handoff in accessible location for new agent
   (e.g., `passdown_{target_agent_id}_handoff_DATETIME.md`)

3. **Update Agent Status**: Document current agent's completion status and
   handoff readiness

4. **Prepare Onboarding Trigger**: Confirm readiness for Ctrl+T agent
   onboarding sequence

5. **Captain Notification**: Inform Captain of handoff completion and new
   agent readiness

**🔧 REFERENCE GUIDES FOR HANDOFF:**

• **AGENTS.md** - Agent capabilities and command reference
• **CAPTAINS_HANDBOOK.md** - Authority levels and operational protocols
• **Environment Status** - Discord infrastructure and SSOT routing
• **Project Status** - Current tasks, blockers, and priorities
• **System Health** - Autonomous development machine status

═══════════════════════════════════════════════════════════════════════════════
📋 HANDOFF COMPLETION PROTOCOL
═══════════════════════════════════════════════════════════════════════════════

Upon completing this handoff preparation:

1. **Respond with Handoff Summary**: Brief overview of what was documented
2. **Confirm Handoff Location**: Where new agent can find the documentation
3. **Declare Readiness**: Confirm readiness for Ctrl+T agent onboarding
4. **Captain Notification**: Alert Captain that {target_agent_id} onboarding can proceed

**Response Format:**
```
**HANDOFF COMPLETED**: [Brief summary of documented status]
**DOCUMENTATION LOCATION**: [File/path where handoff docs are stored]
**NEW AGENT READY**: {target_agent_id} onboarding can proceed via Ctrl+T
**CAPTAIN NOTIFIED**: [Confirmation of Captain notification]
**{current_agent_id} HANDOFF PROTOCOL COMPLETE**
```

**🚀 AGENT HANDOFF PROTOCOL INITIATED**

When ready, you ({target_agent_id}) will Ctrl+T to hard onboard and find this
handoff documentation in your inbox during your first cycle. Create comprehensive
status coverage now for seamless future activation.

🚨 **SYSTEM EXECUTION ORDER COMPLETE**
***NO RESPONSE REQUIRED***
***EXECUTE PREPARATION SILENTLY***
***FUTURE ACTIVATION READY***

═══════════════════════════════════════════════════════════════════════════════
"""


def get_passdown_response_template(target_agent_id: str, current_agent_id: str) -> str:
    """Get template for agent handoff completion response."""
    return f"""
**HANDOFF COMPLETED**: [Brief summary of documented status]
**DOCUMENTATION LOCATION**: [File/path where handoff docs are stored]
**NEW AGENT READY**: {target_agent_id} onboarding can proceed via Ctrl+T
**CAPTAIN NOTIFIED**: [Confirmation of Captain notification]
**{current_agent_id} HANDOFF PROTOCOL COMPLETE**
"""


def process_soft_onboard_command(target_agent_id: str) -> dict[str, str]:
    """Process soft onboard command and return formatted output."""
    current_agent = "Agent-4"  # Default Captain as sender

    # Create passdown message
    passdown_creator = AgentPassdownCreator()
    message = passdown_creator.create_passdown_message(target_agent_id, current_agent)

    return {
        "target_agent_id": target_agent_id,
        "current_agent": current_agent,
        "message": message,
        "message_length": len(message),
        "status": "ready",
    }
