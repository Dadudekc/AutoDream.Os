-- Migration: Add fingerprint and source tracking to tasks
-- Date: 2025-10-13
-- Purpose: Enable message-task integration with deduplication
-- Idempotent: Safe to run multiple times

BEGIN;

-- Add fingerprint column (for deduplication)
ALTER TABLE tasks ADD COLUMN IF NOT EXISTS fingerprint TEXT;

-- Add source JSON column (message metadata)
ALTER TABLE tasks ADD COLUMN IF NOT EXISTS source_json TEXT;

-- Add state column (FSM integration)
ALTER TABLE tasks ADD COLUMN IF NOT EXISTS state TEXT DEFAULT 'todo';

-- Add tags column (categorization)
ALTER TABLE tasks ADD COLUMN IF NOT EXISTS tags TEXT;

-- Create unique index on fingerprint (prevents duplicates)
CREATE UNIQUE INDEX IF NOT EXISTS idx_tasks_fingerprint ON tasks(fingerprint);

-- Create index on state + priority (performance)
CREATE INDEX IF NOT EXISTS idx_tasks_state_priority ON tasks(state, priority);

COMMIT;

