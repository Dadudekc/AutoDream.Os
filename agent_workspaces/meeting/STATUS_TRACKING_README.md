# Status Tracking System for Agents

## Overview
This system helps agents track their contract progress, maintain workspace health, and coordinate with other agents effectively.

## Files
- **`status_template.json`** - Template showing the structure of a status.json file
- **`generate_status.py`** - Script to automatically generate personalized status.json files

## Quick Start

### Option 1: Use the Generator Script (Recommended)
```bash
# Generate status.json for your contract
python generate_status.py --agent Agent-1 --contract-id SSOT-001 --title "SSOT Violation Analysis" --points 400 --category "SSOT_Resolution"
```

### Option 2: Manual Creation
1. Copy `status_template.json` to your workspace: `agent_workspaces/Agent-X/`
2. Rename it to `status.json`
3. Update the fields with your contract details

## Required Fields to Update

### Basic Information
- `agent_id`: Your agent ID (e.g., "Agent-1")
- `current_contract.contract_id`: Your contract ID (e.g., "SSOT-001")
- `current_contract.title`: Your contract title
- `current_contract.extra_credit_points`: Points for this contract

### Progress Tracking
- `progress.percentage`: Current completion percentage
- `progress.current_phase`: Current work phase
- `work_status.estimated_completion`: When you expect to finish
- `blockers.current_blockers`: Any issues blocking progress

### Communication
- `communication.last_devlog_update`: When you last updated devlog
- `communication.last_inbox_check`: When you last checked messages
- `notes`: Important observations or discoveries

## Best Practices

### 1. Update Regularly
- Update `progress.percentage` every time you complete a task
- Update `last_updated` timestamp with each change
- Use devlog system: `python -m src.core.devlog_cli --add "Your progress message"`

### 2. Track Blockers
- Add blockers to `blockers.current_blockers` when you encounter issues
- Move resolved blockers to `blockers.resolved_blockers`
- Set `escalation_needed: true` if you need Captain intervention

### 3. Monitor Workspace Health
- Keep `workspace_health.workspace_clean: true`
- Update file counts as you create/modify/delete files
- Record last cleanup time

### 4. Quality Assurance
- Request code reviews when appropriate
- Update testing coverage as you add tests
- Ensure documentation is updated with code changes

## Example Updates

### Starting Work
```json
{
  "progress": {
    "percentage": "10%",
    "current_phase": "Analysis",
    "last_milestone": "Requirements reviewed"
  },
  "next_actions": [
    "Begin code analysis",
    "Identify SSOT violations",
    "Create analysis report"
  ]
}
```

### Encountering Blocker
```json
{
  "blockers": {
    "current_blockers": [
      "Need access to database schema documentation",
      "Unclear validation requirements"
    ],
    "escalation_needed": true,
    "escalation_reason": "Missing documentation access"
  }
}
```

### Completing Deliverable
```json
{
  "deliverables": {
    "completed": ["SSOT violation analysis report"],
    "in_progress": ["Consolidation plan"],
    "pending": ["Implementation code changes"]
  },
  "progress": {
    "percentage": "40%",
    "last_milestone": "Analysis report completed"
  }
}
```

## Integration with Other Systems

### Devlog System
```bash
# Update devlog with progress
python -m src.core.devlog_cli --add "Completed SSOT analysis report - 40% done"

# Then update status.json
"communication": {
  "last_devlog_update": "2025-08-28 23:30:00"
}
```

### Contract Claiming System
```bash
# Check your contract status
python agent_workspaces/meeting/contract_claiming_system.py --status CONTRACT-ID

# Update progress
python agent_workspaces/meeting/contract_claiming_system.py --update-progress CONTRACT-ID --agent Agent-1 --progress "40% Complete"
```

## Troubleshooting

### Common Issues
1. **File not found**: Ensure you're in the correct directory
2. **Permission denied**: Check file permissions
3. **Invalid JSON**: Use a JSON validator to check syntax

### Getting Help
1. Check your inbox for messages from other agents
2. Use devlog system to communicate issues
3. Escalate to Captain if blockers persist

## Remember
- **Keep status.json updated** - This helps other agents understand your progress
- **Communicate regularly** - Use devlog and inbox systems
- **Maintain workspace health** - Keep organized and clean
- **Track quality** - Ensure your work meets standards

Good luck with your contracts! 🚀
