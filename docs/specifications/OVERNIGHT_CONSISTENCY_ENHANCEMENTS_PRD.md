# Overnight Consistency Enhancements PRD

This document is the **single source of truth (SSOT)** for the overnight consistency enhancements.
It defines the objectives, features, and roadmap for improving the overnight flag functionality.

## Objective
Improve the overnight flag functionality to prevent duplication, reduce complexity, and ensure
agents detect when their terminal tasks are complete.

## Features
1. **Rotating Validation Prompts**
   - After the initial resume prompt, agents receive a sequence of validation tasks:
     KISS validation, a SOLID principles check, a monolithic check, and a V2 compliance review.
   - This built-in checklist is automatically followed overnight by each agent.
2. **Quality Control Agent (Optional)**
   - One agent can be designated as a QA checkpoint.
   - Before final tasks are pushed, results are sent to this agent for a final checklist review.
3. **Terminal Completion Detection**
   - Introduce a standard end-of-command marker for scripts and PowerShell commands.
   - Agents recognize this marker to know exactly when a task has completed.

## Roadmap
### Phase 1: Integration of Rotating Prompts
- Update the overnight workflow to include sequential validation prompts.
- Test each validation step to ensure agents proceed through all checks.

### Phase 2: QA Agent Assignment (Optional)
- Assign a designated QA agent role in the agent roster.
- Implement a routine where agents forward their final output to the QA agent for checklist
  verification.

### Phase 3: Terminal Completion Marker
- Add a universal completion signal at the end of scripts or PowerShell commands.
- Train agents to recognize this signal so they know exactly when a task is fully complete.

