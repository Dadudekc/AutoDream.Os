-- Hard Onboarding Database Migration
-- Date: 2025-10-04
-- Purpose: Create tables for cursor task database integration with FSM tracking

PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;

-- Main cursor tasks table with full integration support
CREATE TABLE IF NOT EXISTS cursor_tasks_integrated (
    task_id TEXT PRIMARY KEY,
    agent_id TEXT NOT NULL,
    description TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'CREATED',
    priority TEXT NOT NULL DEFAULT 'NORMAL',
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')),
    metadata TEXT DEFAULT '{}',
    cursor_session_id TEXT,
    source_file TEXT,
    scan_context TEXT DEFAULT '{}',
    fsm_state TEXT,
    state_transitions TEXT DEFAULT '[]',
    dependencies TEXT DEFAULT '[]',
    assigned_by TEXT
);

-- Scanner tasks tracking for project analysis integration
CREATE TABLE IF NOT EXISTS scanner_tasks (
    scan_id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    scan_timestamp TEXT DEFAULT (datetime('now')),
    file_analysis TEXT,
    complexity_metrics TEXT,
    dependencies TEXT,
    agent_assignments TEXT,
    status TEXT DEFAULT 'PENDING'
);

-- FSM task tracking for state management
CREATE TABLE IF NOT EXISTS fsm_task_tracking (
    tracking_id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    agent_id TEXT NOT NULL,
    current_state TEXT,
    state_history TEXT DEFAULT '[]',
    transition_log TEXT DEFAULT '[]',
    execution_context TEXT
);

-- Performance indexes for common queries
CREATE INDEX IF NOT EXISTS idx_tasks_status ON cursor_tasks_integrated(status, priority);
CREATE INDEX IF NOT EXISTS idx_tasks_agent ON cursor_tasks_integrated(agent_id, status);
CREATE INDEX IF NOT EXISTS idx_tasks_created ON cursor_tasks_integrated(created_at);
CREATE INDEX IF NOT EXISTS idx_fsm_state ON fsm_task_tracking(current_state);
CREATE INDEX IF NOT EXISTS idx_fsm_agent ON fsm_task_tracking(agent_id, current_state);
CREATE INDEX IF NOT EXISTS idx_scanner_status ON scanner_tasks(status);

-- Ensure JSON1 extension is available (graceful fallback if not)
-- This allows json_set() operations for metadata updates
