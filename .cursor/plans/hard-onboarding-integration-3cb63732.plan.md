<!-- 3cb63732-2581-4a03-83a4-d8c3a4069a71 2e5a30a9-5446-4f8d-a3f1-e1817e32cc45 -->
# Hard-Onboarding Readiness — Complete Integration

## Overview

Unify task DB, FSM, Onboarder, and Workflow systems with closure-first approach for production-ready agent hard onboarding.

## Implementation Steps

### 1. Database Schema & Migration

**File**: `tools/migrations/2025_10_04_hard_onboarding.sql`

- Create idempotent SQL migration with JSON1-safe defaults
- Add `cursor_tasks_integrated`, `scanner_tasks`, `fsm_task_tracking` tables
- Create performance indexes for status, agent_id, and fsm_state queries
- Enable WAL mode and foreign keys for data integrity

### 2. Integration Bridge Module

**File**: `src/integrations/hard_onboarding_bridge.py` (new)

- Implement `ensure_db()` for schema bootstrapping
- Create `create_and_assign_onboarding(agent_id)` for task creation + assignment
- Add `execute_hard_onboarding(agent_id, dry_run)` wrapper for PyAutoGUI execution
- Implement `mark_onboarding_result(task_id, success)` for status updates
- Build `captain_hard_onboard(agent_id, dry_run)` orchestrator (one-shot flow)

Key integration points:

- `CursorTaskIntegrationManager` for DB operations
- `process_hard_onboard_command` from `agent_hard_onboarding.py`
- FSM state transitions: CREATED → ASSIGNED → ACTIVE → COMPLETED/FAILED

### 3. Captain CLI Tool

**File**: `tools/captain_onboard_cli.py` (new)

- Argparse interface: `--agent`, `--dry-run`, `--report` flags
- Call `captain_hard_onboard()` orchestrator
- Print JSON summary with task_id, success status, execution orders
- Optional integration report export for Captain review

### 4. Coordinates Validator

**File**: `tools/validate_coordinates.py` (new)

- Pre-flight validation of `config/coordinates.json` schema
- Check `chat_input_coordinates` and `onboarding_coordinates` format
- Validate all required agents have valid integer coordinate pairs
- Exit with error codes for CI integration

### 5. Update Existing Integration Manager

**File**: `tools/cursor_task_database_integration.py`

- Verify `create_hard_onboarding_task()` method exists (already present)
- Confirm `assign_task_with_workflow_integration()` works correctly
- Validate `update_task_fsm_state()` handles JSON1 safely with COALESCE
- Ensure `generate_captain_execution_orders()` includes onboarding tasks

### 6. Smoke Tests

**File**: `tests/test_hard_onboarding_smoke.py` (new)

- Test dry-run flow end-to-end without PyAutoGUI clicks
- Verify task creation, assignment, FSM transitions in test DB
- Validate JSON report structure and execution orders
- CI-friendly headless execution

### 7. Captain Runbook Documentation

**File**: `docs/CAPTAIN_HARD_ONBOARDING_RUNBOOK.md` (new)

- Pre-flight checklist: migration, validation, dry-run
- Execution commands with examples
- Troubleshooting guide for common issues
- Emergency rollback procedures

## Files to Create

1. `tools/migrations/2025_10_04_hard_onboarding.sql` - DB schema
2. `src/integrations/hard_onboarding_bridge.py` - Integration glue
3. `tools/captain_onboard_cli.py` - CLI interface
4. `tools/validate_coordinates.py` - Pre-flight validator
5. `tests/test_hard_onboarding_smoke.py` - Smoke tests
6. `docs/CAPTAIN_HARD_ONBOARDING_RUNBOOK.md` - Operations guide

## Files to Update

1. `tools/cursor_task_database_integration.py` - Verify integration points
2. `src/services/agent_hard_onboarding.py` - Ensure compatibility

## Verification Steps

1. Run migration: `sqlite3 unified.db < tools/migrations/2025_10_04_hard_onboarding.sql`
2. Validate coordinates: `python tools/validate_coordinates.py`
3. Dry-run test: `python tools/captain_onboard_cli.py --agent Agent-6 --dry-run`
4. Execute real onboarding: `python tools/captain_onboard_cli.py --agent Agent-6 --report`
5. Run smoke tests: `pytest tests/test_hard_onboarding_smoke.py`

## Success Criteria

- Database schema created with proper indexes
- CLI can execute dry-run without errors
- Coordinates validation passes for all agents
- Task lifecycle tracked: CREATED → ASSIGNED → ACTIVE → COMPLETED
- FSM state transitions logged correctly
- Smoke tests pass in CI environment
- Captain can onboard agents with single command

## Note on Workflow Integration

The `simple_workflow_automation.py` integration (auto-assign follow-up tasks after onboarding) is deferred to avoid increasing file count during the current optimization phase. Can be added later as a post-onboarding task seeder.
