# Agent-{agent_id} Onboarding

**Role**: {agent_role}  
**Primary Task**: {current_assignment}  

**Key Commands**:
- Check inbox: `ls agent_workspaces/Agent-{agent_id}/inbox/`
- Update status: `echo '{{...}}' > agent_workspaces/Agent-{agent_id}/status.json`
- Get task: `python -m src.services.messaging_cli --agent Agent-{agent_id} --get-next-task`

**Start Working**: {immediate_action}

---
*For full onboarding protocols, see AGENTS.md*
*For quality standards, see STANDARDS.md*

