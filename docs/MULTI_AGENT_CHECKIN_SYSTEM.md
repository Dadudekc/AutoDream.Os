# 🛰️ Multi-Agent Check-In System

## Overview

A robust, collision-free system for multiple agents to report status concurrently with durable logs and live "current state" view.

## Architecture

### Core Components

1. **Versioned Schema** (`schemas/agent_checkin.schema.json`)
   - JSON Schema v2020-12 compliant
   - Defines structure for agent check-ins
   - Version 1.0 with extensible design

2. **Append-Only Logs** (`runtime/agent_logs/`)
   - Per-agent JSONL files (one JSON per line)
   - Immutable history for audit trails
   - Zero collision design

3. **Atomic Index** (`runtime/agents_index.json`)
   - Current state map: `{agent_id: last_state}`
   - Atomic write operations prevent corruption
   - O(1) access to current agent states

4. **CLI Tools**
   - `tools/agent_checkin.py` - Agent check-in submission
   - `tools/captain_snapshot.py` - Captain status overview

## Usage

### Agent Check-In

```bash
# From file
python tools/agent_checkin.py examples/agent_checkins/agent1_checkin.json

# From stdin
echo '{"agent_id":"Agent-1","agent_name":"Test Agent","status":"ACTIVE","current_phase":"TESTING"}' | python tools/agent_checkin.py -
```

### Captain Snapshot

```bash
python tools/captain_snapshot.py
```

Output:
```
🛰️  CAPTAIN SNAPSHOT - Multi-Agent Status Overview
============================================================================================================
AGENT      STATUS       STALENESS    CURRENT_PHASE             NEXT_MILESTONE                 AGE
------------------------------------------------------------------------------------------------------------
Agent-1    ACTIVE       🟢 FRESH      CRITICAL_SYNTAX_FIX      Complete syntax fixes          2m
Agent-2    ACTIVE       🟡 RECENT     PHASE_2_ENFORCEMENT      Complete Phase 2 enforcement   8m
Agent-3    BLOCKED      🟠 STALE      REAL_TIME_MONITORING     Optimize monitoring metrics    25m
```

## Schema

### Required Fields
- `version`: "1.0"
- `agent_id`: Unique agent identifier
- `agent_name`: Human-readable agent name
- `status`: Current status (ACTIVE, PENDING, BLOCKED, COMPLETE)
- `current_phase`: Current operational phase
- `last_updated`: ISO-8601 timestamp (auto-filled if missing)

### Optional Fields
- `current_mission`: Mission description
- `mission_priority`: Priority level
- `current_tasks`: Array of current tasks
- `completed_tasks`: Array of completed tasks
- `achievements`: Array of achievements
- `strategic_capabilities`: Object with capability mappings
- `agent_status`: Agent health/performance data
- `system_status`: System operational data
- `syntax_fix_status`: Syntax fixing progress
- `v2_compliance_status`: V2 compliance progress
- `next_actions`: Array of planned actions

## File Structure

```
repo/
├── schemas/
│   └── agent_checkin.schema.json     # Schema definition
├── runtime/
│   ├── agents_index.json             # Atomic current-state map
│   └── agent_logs/
│       ├── Agent-1.log.jsonl         # Append-only history
│       ├── Agent-2.log.jsonl
│       └── ...
├── tools/
│   ├── agent_checkin.py              # Check-in CLI
│   └── captain_snapshot.py           # Captain overview
└── examples/
    └── agent_checkins/
        ├── agent1_checkin.json       # Example payloads
        ├── agent2_checkin.json
        └── agent3_checkin.json
```

## Safety Features

### Zero Collisions
- **Append-only logs**: Multiple agents can write simultaneously
- **Atomic index updates**: Uses temporary files + atomic rename
- **No locking required**: File system handles concurrency

### Durability
- **JSONL format**: One JSON per line, easy to parse/repair
- **Atomic writes**: All-or-nothing updates prevent corruption
- **Versioned schema**: Backward compatibility maintained

### Monitoring
- **Staleness detection**: Flags agents silent >15 minutes
- **Status prioritization**: Critical issues shown first
- **Summary statistics**: Quick overview of swarm health

## Agent Check-In Template

```json
{
  "version": "1.0",
  "agent_id": "Agent-X",
  "agent_name": "<role>",
  "status": "ACTIVE|PENDING|BLOCKED|COMPLETE",
  "current_phase": "<PHASE_NAME>",
  "last_updated": "<auto/override ISO-8601>",
  "current_mission": "<concise objective>",
  "mission_priority": "CRITICAL|HIGH|MEDIUM|LOW - <why>",
  "last_milestone": "<win or partial>",
  "next_milestone": "<short-term deliverable>",
  "current_tasks": [],
  "completed_tasks": [],
  "achievements": [],
  "strategic_capabilities": {},
  "agent_status": {},
  "system_status": {},
  "syntax_fix_status": {},
  "v2_compliance_status": {},
  "next_actions": [],
  "mission_status": "<summary tag>"
}
```

## Captain Workflow

1. **Monitor**: Run `python tools/captain_snapshot.py` regularly
2. **Identify Issues**: Look for stale agents or critical statuses
3. **Take Action**: Contact agents or escalate as needed
4. **Track Progress**: Use historical logs for trend analysis

## Future Enhancements

- JSON Schema validation in `agent_checkin.py`
- GitHub Actions workflow for schema compliance
- `staleness_monitor.py` for automated alerts
- Web dashboard for real-time monitoring
- Integration with existing messaging system

## Dependencies

- Python 3.7+
- Standard library only (no external dependencies)
- File system with atomic rename support

## Security Considerations

- All data stored locally in `runtime/` directory
- No network dependencies
- Append-only logs prevent tampering
- Atomic operations prevent corruption
