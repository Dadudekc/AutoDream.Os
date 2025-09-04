# Enhanced Messaging System V2 - Message Types Guide

## Overview

The messaging system has been enhanced to better facilitate different types of communication with clear sender/receiver identification:

- **A2A (Agent-to-Agent)**: When agents coordinate with other agents
- **S2A (System-to-Agent)**: System messages like onboarding or pre-made messages
- **H2A (Human-to-Agent)**: Messages from humans (like Discord) to agents

## New Message Types

### 1. A2A (Agent-to-Agent) Communication

When agents need to coordinate with other agents:

```bash
# Agent-1 sending a message to Agent-7
python -m src.services.messaging_cli \
  --agent Agent-7 \
  --message "Need help with the integration task" \
  --sender "Agent-1" \
  --type agent_to_agent \
  --sender-type agent \
  --recipient-type agent
```

### 2. S2A (System-to-Agent) Communication

System messages like onboarding or automated messages:

```bash
# System sending onboarding message to Agent-6
python -m src.services.messaging_cli \
  --agent Agent-6 \
  --message "Welcome to the system" \
  --sender "Captain Agent-4" \
  --type system_to_agent \
  --sender-type system \
  --recipient-type agent
```

### 3. H2A (Human-to-Agent) Communication

Messages from humans (like Discord) to agents:

```bash
# Human sending message to Agent-5
python -m src.services.messaging_cli \
  --agent Agent-5 \
  --message "Please check the database connection" \
  --sender "Human Operator" \
  --type human_to_agent \
  --sender-type human \
  --recipient-type agent
```

## Enhanced Onboarding

The onboarding sequence now clearly identifies each agent ID to prevent confusion:

```bash
# Send onboarding to specific agent with clear ID identification
python -m src.services.messaging_cli \
  --onboard \
  --agent Agent-6 \
  --onboarding-style friendly
```

The onboarding message now includes:
- Clear agent identity confirmation at the top
- Message type information (S2A)
- Sender/recipient type classification
- Enhanced formatting to prevent agent confusion

## Message Formatting

### PyAutoGUI Delivery
Messages delivered via PyAutoGUI now include:
- Agent identity reminder
- Message type header (A2A/S2A/H2A)
- Sender/recipient type information
- Enhanced visual formatting

### Inbox Delivery
Messages delivered to inbox files now include:
- Message type classification
- Sender/recipient type information
- Tags and metadata
- Enhanced markdown formatting

## CLI Flags

### New Flags Added:
- `--sender-type`: Specify sender type (agent/system/human)
- `--recipient-type`: Specify recipient type (agent/system/human)
- Enhanced `--type` choices: text, broadcast, onboarding, agent_to_agent, system_to_agent, human_to_agent

### Usage Examples:

```bash
# A2A message with explicit types
python -m src.services.messaging_cli \
  --agent Agent-7 \
  --message "Task completed, ready for review" \
  --sender "Agent-1" \
  --type agent_to_agent \
  --sender-type agent \
  --recipient-type agent

# S2A broadcast to all agents
python -m src.services.messaging_cli \
  --bulk \
  --message "System maintenance scheduled" \
  --sender "Captain Agent-4" \
  --type system_to_agent \
  --sender-type system \
  --recipient-type agent

# H2A message from human
python -m src.services.messaging_cli \
  --agent Agent-5 \
  --message "Please update the documentation" \
  --sender "Human Operator" \
  --type human_to_agent \
  --sender-type human \
  --recipient-type agent
```

## Validation Rules

New validation rules ensure proper message routing:
- Message type consistency with sender/recipient types
- Proper sender/recipient identification
- Agent ID validation for proper routing

## Benefits

1. **Clear Communication Context**: Agents know exactly who sent the message and what type of communication it is
2. **Prevented Confusion**: Enhanced onboarding prevents agents from misidentifying themselves
3. **Better Routing**: Messages are properly categorized and routed based on type
4. **Enhanced Formatting**: Messages include clear headers and type information
5. **Improved Coordination**: A2A messages facilitate better agent-to-agent coordination

## Migration Notes

- Existing messages will continue to work with automatic type inference
- New CLI flags are optional but recommended for clarity
- Onboarding messages now use S2A type by default
- Enhanced formatting is applied automatically to all new messages
