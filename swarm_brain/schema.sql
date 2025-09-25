-- Swarm Brain Database Schema
-- ==========================
-- 
-- This schema supports the swarm intelligence system with:
-- - Normalized document storage with specialized lenses
-- - Embedding tracking for semantic search
-- - Agent activity and tool usage patterns
-- - Protocol and workflow effectiveness tracking
-- - Performance monitoring and optimization

PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;
PRAGMA synchronous=NORMAL;

-- Global documents table - central storage for all agent activities
CREATE TABLE IF NOT EXISTS documents (
  id INTEGER PRIMARY KEY,
  kind TEXT NOT NULL,               -- 'action'|'tool'|'protocol'|'workflow'|'performance'|'conversation'
  ref_id TEXT UNIQUE,               -- external reference (uuid etc.)
  project TEXT,                     -- repo or project id
  agent_id TEXT,                    -- Agent-1..Agent-8 or name
  ts INTEGER NOT NULL,              -- epoch seconds
  title TEXT,
  summary TEXT,                     -- short summary
  tags TEXT,                        -- JSON array
  meta TEXT,                        -- JSON object
  canonical TEXT NOT NULL           -- canonical text used for embeddings
);

-- Agent actions - tool usage and outcomes
CREATE TABLE IF NOT EXISTS actions (
  doc_id INTEGER PRIMARY KEY,
  tool TEXT,                        -- tool name (project_scanner, discord_commander, etc.)
  outcome TEXT,                     -- 'success'|'failure'|'partial'|free text
  context TEXT,                     -- JSON context data
  duration_ms INTEGER,             -- execution time in milliseconds
  FOREIGN KEY(doc_id) REFERENCES documents(id) ON DELETE CASCADE
);

-- Tool usage patterns and effectiveness
CREATE TABLE IF NOT EXISTS tools (
  doc_id INTEGER PRIMARY KEY,
  usage_pattern TEXT,               -- how the tool was used
  success_rate REAL,               -- success rate (0.0-1.0)
  failure_modes TEXT,               -- JSON array of failure modes
  optimizations TEXT,               -- JSON array of optimization strategies
  FOREIGN KEY(doc_id) REFERENCES documents(id) ON DELETE CASCADE
);

-- Protocol definitions and effectiveness tracking
CREATE TABLE IF NOT EXISTS protocols (
  doc_id INTEGER PRIMARY KEY,
  steps TEXT,                       -- JSON array of protocol steps
  effectiveness REAL,              -- effectiveness score (0.0-1.0)
  improvements TEXT,               -- JSON array of improvements
  adaptation_history TEXT,         -- JSON array of adaptations over time
  FOREIGN KEY(doc_id) REFERENCES documents(id) ON DELETE CASCADE
);

-- Workflow execution patterns and coordination
CREATE TABLE IF NOT EXISTS workflows (
  doc_id INTEGER PRIMARY KEY,
  execution_pattern TEXT,           -- JSON execution pattern
  coordination TEXT,               -- JSON coordination data
  outcomes TEXT,                    -- JSON outcomes data
  optimization TEXT,               -- JSON optimization strategies
  FOREIGN KEY(doc_id) REFERENCES documents(id) ON DELETE CASCADE
);

-- Performance monitoring and optimization
CREATE TABLE IF NOT EXISTS performance (
  doc_id INTEGER PRIMARY KEY,
  metrics TEXT,                     -- JSON performance metrics
  anomalies TEXT,                   -- JSON anomaly data
  optimizations TEXT,               -- JSON optimization strategies
  trends TEXT,                      -- JSON trend analysis
  FOREIGN KEY(doc_id) REFERENCES documents(id) ON DELETE CASCADE
);

-- Conversations and communication patterns
CREATE TABLE IF NOT EXISTS conversations (
  doc_id INTEGER PRIMARY KEY,
  channel TEXT,                     -- 'discord'|'slack'|'cli'|'devlog'
  thread_id TEXT,                   -- conversation thread ID
  role TEXT,                        -- 'user'|'agent'|'system'
  content TEXT,                     -- conversation content
  FOREIGN KEY(doc_id) REFERENCES documents(id) ON DELETE CASCADE
);

-- Embedding tracking - maps documents to their vector representations
CREATE TABLE IF NOT EXISTS embeddings (
  doc_id INTEGER PRIMARY KEY,
  backend TEXT NOT NULL,            -- embedding backend used
  dim INTEGER NOT NULL,             -- embedding dimension
  norm REAL,                        -- vector norm
  created_at INTEGER NOT NULL,      -- when embedding was created
  FOREIGN KEY(doc_id) REFERENCES documents(id) ON DELETE CASCADE
);

-- Agent coordination patterns
CREATE TABLE IF NOT EXISTS coordination (
  doc_id INTEGER PRIMARY KEY,
  coordination_type TEXT,           -- 'workflow'|'discord'|'pyautogui'|'direct'
  participants TEXT,                -- JSON array of participating agents
  coordination_data TEXT,           -- JSON coordination details
  effectiveness REAL,              -- coordination effectiveness (0.0-1.0)
  FOREIGN KEY(doc_id) REFERENCES documents(id) ON DELETE CASCADE
);

-- Indexes for efficient querying
CREATE INDEX IF NOT EXISTS idx_documents_ts ON documents(ts);
CREATE INDEX IF NOT EXISTS idx_documents_kind ON documents(kind);
CREATE INDEX IF NOT EXISTS idx_documents_project ON documents(project);
CREATE INDEX IF NOT EXISTS idx_documents_agent ON documents(agent_id);
CREATE INDEX IF NOT EXISTS idx_documents_ref_id ON documents(ref_id);

CREATE INDEX IF NOT EXISTS idx_actions_tool ON actions(tool);
CREATE INDEX IF NOT EXISTS idx_actions_outcome ON actions(outcome);

CREATE INDEX IF NOT EXISTS idx_conversations_channel ON conversations(channel);
CREATE INDEX IF NOT EXISTS idx_conversations_thread ON conversations(thread_id);

CREATE INDEX IF NOT EXISTS idx_coordination_type ON coordination(coordination_type);
CREATE INDEX IF NOT EXISTS idx_coordination_effectiveness ON coordination(effectiveness);

-- Views for common queries
CREATE VIEW IF NOT EXISTS agent_activity AS
SELECT 
  d.id,
  d.kind,
  d.project,
  d.agent_id,
  d.ts,
  d.title,
  d.summary,
  d.tags,
  a.tool,
  a.outcome,
  a.duration_ms
FROM documents d
LEFT JOIN actions a ON d.id = a.doc_id
WHERE d.kind = 'action';

CREATE VIEW IF NOT EXISTS tool_effectiveness AS
SELECT 
  a.tool,
  COUNT(*) as total_uses,
  SUM(CASE WHEN a.outcome = 'success' THEN 1 ELSE 0 END) as successful_uses,
  AVG(a.duration_ms) as avg_duration_ms,
  COUNT(DISTINCT d.agent_id) as unique_agents
FROM actions a
JOIN documents d ON a.doc_id = d.id
GROUP BY a.tool;

CREATE VIEW IF NOT EXISTS agent_coordination AS
SELECT 
  d.agent_id,
  c.coordination_type,
  COUNT(*) as coordination_count,
  AVG(c.effectiveness) as avg_effectiveness
FROM documents d
JOIN coordination c ON d.id = c.doc_id
GROUP BY d.agent_id, c.coordination_type;




