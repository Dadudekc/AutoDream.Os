# 🗃️ Database Integration Guide
**Purpose**: Comprehensive database usage instructions for agents
**For**: All agents during onboarding and operation

## 🧠 Swarm Brain Database (.swarm_brain/brain.sqlite3)
**Usage**: Pattern recognition, decision support, knowledge storage
**Commands**: 
```python
from swarm_brain import Retriever
r = Retriever()
results = r.search("agent coordination", k=10)
expertise = r.get_agent_expertise("Agent-8", k=20)
```
**When**: Every cycle phase for historical knowledge and successful patterns

## 🔧 Unified Database (unified.db)
**Usage**: Task management, agent coordination, project operations
**Access**: Direct SQLite operations, tools/cursor_task_database_integration.py
**Purpose**: Current operations, task tracking, agent state management
**When**: Throughout all phases for task coordination and project state

## 🧠 Vector Database (.swarm_brain/index/)
**Usage**: Semantic search, similarity matching, pattern analysis
**Commands**:
```python
from src.services.vector_database import VectorDatabaseIntegration
vdb = VectorDatabaseIntegration()
similar = vdb.search_similar("integration challenges", k=5)
```
**When**: Similarity search and pattern matching across agent experiences

## 🤖 ML Predictor Model (src/models/dream_os_predictor_v1.0.0-*.pkl)
**Usage**: SSOT violation prediction, proactive prevention
**Access**: Automated through PredictiveSSOTEngine
**Purpose**: Predict and prevent conflicts before they occur
**When**: Automated during task execution and quality gates

## 🔧 Database Usage by Cycle Phase
- **PHASE 1 (CHECK_INBOX)**: Query Swarm Brain for patterns, search vector database for similar actions
- **PHASE 2 (EVALUATE_TASKS)**: Query Swarm Brain for task success patterns, check unified.db for task status
- **PHASE 3 (EXECUTE_ROLE)**: Store vector embeddings of work, update unified.db with progress
- **PHASE 4 (QUALITY_GATES)**: Store quality results in Swarm Brain, index results in vector database
- **PHASE 5 (CYCLE_DONE)**: Update all databases with cycle results and completion status

## 🛠️ Database Tools
```bash
python tools/database_search.py --query "pattern"
python tools/agent_vector_search.py --search "coordination"
```
