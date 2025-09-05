# Vector Database System

A unified vector database powering semantic search across messages, devlogs and project
documentation. The database integrates with the Agent Cellphone V2 messaging system and
provides context-aware access to all project knowledge.

## Features
- Semantic search over messages, contracts, devlogs and docs
- Agent context awareness with per-agent search history
- ChromaDB persistence and optional OpenAI embeddings
- Intelligent chunking with real-time indexing
- CLI tools for messaging and documentation workflows

## Installation
```bash
# Core dependencies
pip install -r requirements.txt --extra vector_db

# Documentation features
pip install -r requirements-vector.txt
python scripts/setup_vector_database.py
```

## CLI Usage
### Messaging & General Search
```bash
# Search all indexed content
python -m src.services.vector_database_cli search "agent coordination"

# Index an agent inbox
python -m src.services.vector_database_cli index --inbox agent_workspaces/Agent-1/inbox --agent Agent-1

# Show database statistics
python -m src.services.vector_database_cli stats
```

### Documentation CLI
```bash
# Set agent context
python scripts/agent_documentation_cli.py set-agent Agent-7 --role "Web Development Specialist"

# Search project documentation
python scripts/agent_documentation_cli.py search "V2 compliance patterns" --agent Agent-7 --results 5

# Export agent knowledge base
python scripts/agent_documentation_cli.py export agent7.json --agent Agent-7
```

## Programmatic Integration
### Messaging System
```python
from src.services.vector_messaging_integration import VectorMessagingIntegration
integration = VectorMessagingIntegration()
results = integration.search_messages("urgent task", agent_id="Agent-1", limit=5)
```

### Agent Documentation
```python
from src.core.agent_docs_integration import get_agent_docs
agent_docs = get_agent_docs(agent_id="Agent-7", role="Web Development Specialist")
results = agent_docs.search("JavaScript patterns", max_results=5)
summary = agent_docs.get_summary()
```

## Configuration
- **Embedding models**: sentence transformers (default) or OpenAI
- **Document types**: messages, devlogs, contracts, code, documentation, config, status
- **Supported file types**: .md, .txt, .py, .js, .ts, .json, .yaml/.yml
- **Chunking**: 1000-token chunks with 200-token overlap (default)
- **Search**: default 5 results, maximum 50, similarity threshold configurable

## Testing
```bash
pytest tests/vector_database/ -v
```

## Troubleshooting
- Install missing packages: `pip install chromadb`
- Ensure models download on first run: `SentenceTransformer('all-MiniLM-L6-v2')`
- Set `OPENAI_API_KEY` when using OpenAI embeddings
- Ensure write access to `data/vector_db`

## Maintenance
- Re-index documentation: `python scripts/setup_vector_database.py`
- Backup database: `cp -r vector_db vector_db_backup_$(date +%Y%m%d)`

## Future Enhancements
- Real-time indexing and advanced filtering
- Multi-modal document support and analytics dashboard

## Contributing & License
Follow V2 compliance standards and add tests for new features.

MIT License. See `LICENSE` for details.
