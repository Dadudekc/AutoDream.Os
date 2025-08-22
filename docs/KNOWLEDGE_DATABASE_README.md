# 🧠 CLI Knowledge Database System - Agent Cellphone V2

A comprehensive knowledge database system that agents can use to store, retrieve, and collaborate on knowledge through both CLI and Python API interfaces.

## 🎯 Overview

The Knowledge Database System provides agents with:

- **Persistent Knowledge Storage**: SQLite-based storage with integrity checks
- **Rich CLI Interface**: Command-line tools for knowledge management
- **Python API**: Programmatic access for agent automation
- **Intelligent Search**: Full-text search with relevance scoring
- **Agent Collaboration**: Knowledge sharing and relationship tracking
- **Learning Tracking**: Structured learning experiences and best practices
- **Troubleshooting Guides**: Step-by-step problem-solving knowledge

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install click rich
```

### 2. Run the Demo

```bash
python examples/demo_knowledge_database.py
```

### 3. Use the CLI

```bash
# Get help
python src/core/knowledge_database.py --help

# Add knowledge
python src/core/knowledge_database.py add \
  --title "Python Best Practices" \
  --content "Always use virtual environments..." \
  --category "programming" \
  --agent-id "agent_1" \
  --tags "python,best_practices,virtual_env"

# Search knowledge
python src/core/knowledge_database.py search "python"

# View statistics
python src/core/knowledge_database.py stats
```

## 🏗️ System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   CLI Interface │    │   Python API     │    │   SQLite DB     │
│                 │    │                  │    │                 │
│ • add          │◄──►│ • KnowledgeAPI   │───►│ • knowledge_    │
│ • search       │    │ • quick_* funcs  │    │   entries       │
│ • category     │    │ • specialized    │    │ • relationships │
│ • agent        │    │   methods        │    │ • search_index  │
│ • stats        │    │                  │    │ • indexes       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 📚 Core Components

### 1. KnowledgeDatabase Class
- **Location**: `src/core/knowledge_database.py`
- **Purpose**: Core database operations and schema management
- **Features**: SQLite backend, search indexing, data integrity

### 2. KnowledgeAPI Class
- **Location**: `src/core/knowledge_api.py`
- **Purpose**: Python API wrapper for programmatic access
- **Features**: High-level methods, specialized knowledge types

### 3. KnowledgeCLI Class
- **Location**: `src/core/knowledge_database.py`
- **Purpose**: Rich CLI interface with formatted output
- **Features**: Click-based commands, Rich console output

## 🔧 Usage Examples

### CLI Usage

#### Add Knowledge
```bash
python src/core/knowledge_database.py add \
  --title "Database Optimization Tips" \
  --content "Use indexes on frequently queried columns..." \
  --category "database" \
  --agent-id "agent_2" \
  --tags "database,optimization,performance" \
  --source "agent_research" \
  --confidence 0.9
```

#### Search Knowledge
```bash
# Basic search
python src/core/knowledge_database.py search "database"

# Search with limit
python src/core/knowledge_database.py search "python" --limit 10
```

#### View by Category
```bash
python src/core/knowledge_database.py category "programming" --limit 20
```

#### View by Agent
```bash
python src/core/knowledge_database.py agent "agent_1" --limit 15
```

#### View Statistics
```bash
python src/core/knowledge_database.py stats
```

### Python API Usage

#### Basic Operations
```python
from src.core.knowledge_api import KnowledgeAPI

# Create API instance
api = KnowledgeAPI("my_knowledge.db")

# Add knowledge
entry_id = api.add_knowledge(
    title="My Knowledge",
    content="Knowledge content here...",
    category="my_category",
    agent_id="my_agent",
    tags=["tag1", "tag2"]
)

# Search knowledge
results = api.search_knowledge("search term", limit=10)

# Get by category
category_results = api.get_knowledge_by_category("programming")
```

#### Specialized Knowledge Types
```python
# Add learning experience
learning_id = api.add_learning_experience(
    agent_id="agent_1",
    task_description="Implemented user authentication",
    outcome="Successfully deployed with 99.9% uptime",
    lessons_learned="Use OAuth 2.0 for better security",
    success_rate=0.95
)

# Add best practice
practice_id = api.add_best_practice(
    agent_id="agent_2",
    practice_name="Code Review Process",
    description="Always review code before merging",
    when_to_use="Before any code deployment",
    examples=["Check security", "Verify tests", "Review documentation"]
)

# Add troubleshooting guide
troubleshooting_id = api.add_troubleshooting_guide(
    agent_id="agent_3",
    problem="API rate limiting errors",
    solution="Implement exponential backoff retry logic",
    steps=["Check rate limits", "Implement backoff", "Add monitoring"],
    prevention_tips=["Set appropriate rate limits", "Use caching"]
)
```

#### Quick Functions
```python
from src.core.knowledge_api import quick_add, quick_search, quick_stats

# Quick operations without creating API instance
entry_id = quick_add("Quick Title", "Quick content", "demo", "demo_agent")
results = quick_search("quick", limit=5)
stats = quick_stats()
```

## 🗄️ Database Schema

### knowledge_entries Table
```sql
CREATE TABLE knowledge_entries (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    category TEXT NOT NULL,
    tags TEXT NOT NULL,           -- JSON array
    source TEXT NOT NULL,
    confidence REAL NOT NULL,     -- 0.0 to 1.0
    created_at REAL NOT NULL,     -- Unix timestamp
    updated_at REAL NOT NULL,     -- Unix timestamp
    agent_id TEXT NOT NULL,
    related_entries TEXT NOT NULL, -- JSON array
    metadata TEXT NOT NULL        -- JSON object
);
```

### knowledge_relationships Table
```sql
CREATE TABLE knowledge_relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entry_id TEXT NOT NULL,
    related_id TEXT NOT NULL,
    relationship_type TEXT NOT NULL,
    strength REAL NOT NULL,       -- 0.0 to 1.0
    created_at REAL NOT NULL,
    FOREIGN KEY (entry_id) REFERENCES knowledge_entries (id),
    FOREIGN KEY (related_id) REFERENCES knowledge_entries (id)
);
```

### search_index Table
```sql
CREATE TABLE search_index (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entry_id TEXT NOT NULL,
    search_text TEXT NOT NULL,
    weight REAL NOT NULL,         -- Search relevance weight
    FOREIGN KEY (entry_id) REFERENCES knowledge_entries (id)
);
```

## 🎨 Knowledge Categories

### Built-in Categories
- **programming**: Code, algorithms, development practices
- **infrastructure**: Systems, deployment, operations
- **data_processing**: Data analysis, ETL, analytics
- **code_quality**: Testing, review, best practices
- **troubleshooting**: Problem-solving guides
- **learning_experience**: Agent learning and growth
- **best_practices**: Guidelines and recommendations

### Custom Categories
Agents can create any category they need for their specific domain.

## 🏷️ Tagging System

### Built-in Tags
- **learning**: Learning-related knowledge
- **experience**: Based on agent experience
- **best_practice**: Best practices and guidelines
- **troubleshooting**: Problem-solving knowledge
- **improvement**: Knowledge for improvement
- **recommendations**: Recommendations and advice

### Tag Best Practices
- Use lowercase, descriptive tags
- Separate multiple words with underscores
- Keep tags consistent across similar knowledge
- Use agent IDs as tags for attribution

## 🔍 Search Features

### Full-Text Search
- Searches across title, content, tags, and category
- Weighted scoring (title: 1.0, content: 0.8, tags: 0.9, category: 0.7)
- Relevance-based result ranking

### Search Examples
```bash
# Search for Python-related knowledge
python src/core/knowledge_database.py search "python"

# Search for debugging knowledge
python src/core/knowledge_database.py search "debugging techniques"

# Search for agent-specific knowledge
python src/core/knowledge_database.py search "agent_1"
```

## 🤝 Agent Collaboration

### Knowledge Sharing
- Agents can share knowledge with each other
- Related entries can be linked together
- Collaborative knowledge building

### Learning from Others
- Search for knowledge from other agents
- Build on existing knowledge
- Avoid duplicating work

### Example Collaboration Workflow
1. **Agent A** encounters a problem and solves it
2. **Agent A** adds troubleshooting knowledge to the database
3. **Agent B** searches for similar problems
4. **Agent B** finds Agent A's solution and builds upon it
5. **Agent B** adds improved or additional knowledge
6. Both agents benefit from shared learning

## 📊 Monitoring and Analytics

### Database Statistics
```bash
python src/core/knowledge_database.py stats
```

### Statistics Include
- Total knowledge entries
- Entries by category
- Entries by agent
- Recent activity (last 24 hours)

### Performance Metrics
- Search response time
- Database size
- Index efficiency

## 🚀 Advanced Features

### 1. Knowledge Relationships
- Link related knowledge entries
- Build knowledge graphs
- Track knowledge dependencies

### 2. Confidence Scoring
- Rate knowledge reliability (0.0-1.0)
- Filter by confidence level
- Build trust in knowledge sources

### 3. Metadata Support
- Custom metadata for each entry
- API version tracking
- Creation method tracking

### 4. Search Indexing
- Automatic search index updates
- Weighted relevance scoring
- Fast full-text search

## 🔧 Configuration

### Database Path
```python
# Default: "knowledge_base.db"
api = KnowledgeAPI("custom_path.db")

# CLI: --db-path option
python src/core/knowledge_database.py --db-path "my_db.db" stats
```

### Logging
```python
import logging
logging.basicConfig(level=logging.INFO)
```

## 🧪 Testing

### Run Demo
```bash
python examples/demo_knowledge_database.py
```

### Test CLI Commands
```bash
# Test all commands
python src/core/knowledge_database.py --help
python src/core/knowledge_database.py stats
```

### Test Python API
```python
# Test basic operations
from src.core.knowledge_api import KnowledgeAPI
api = KnowledgeAPI("test.db")
# ... test operations
```

## 📝 Best Practices

### For Agents
1. **Add Knowledge Regularly**: Share what you learn
2. **Use Descriptive Titles**: Make knowledge easy to find
3. **Tag Appropriately**: Use consistent, descriptive tags
4. **Link Related Knowledge**: Connect related entries
5. **Rate Confidence Honestly**: Be accurate about reliability

### For Knowledge Management
1. **Regular Backups**: Backup the database regularly
2. **Monitor Growth**: Track database size and performance
3. **Clean Up**: Remove outdated or incorrect knowledge
4. **Validate Sources**: Ensure knowledge is from reliable sources

## 🚨 Troubleshooting

### Common Issues

#### Database Locked
```bash
# Check if another process is using the database
# Close any other applications using the database
# Restart the system if needed
```

#### Search Not Working
```bash
# Check if search index exists
# Rebuild search index if needed
# Verify database integrity
```

#### Performance Issues
```bash
# Check database size
# Verify indexes exist
# Consider database optimization
```

### Debug Mode
```python
import logging
logging.getLogger('core.knowledge_database').setLevel(logging.DEBUG)
```

## 🔮 Future Enhancements

### Planned Features
- **Knowledge Graphs**: Visual knowledge relationships
- **Machine Learning**: Intelligent knowledge recommendations
- **Version Control**: Knowledge versioning and history
- **Collaborative Editing**: Multi-agent knowledge editing
- **Knowledge Validation**: Automated quality checks
- **Export/Import**: Knowledge base portability

### Integration Opportunities
- **Agent Communication**: Direct knowledge sharing
- **Task Management**: Knowledge-based task generation
- **Performance Monitoring**: Knowledge-driven optimization
- **Learning Systems**: Adaptive knowledge delivery

## 📚 Additional Resources

### Documentation
- [V2 Coding Standards](../V2_CODING_STANDARDS.md)
- [Agent Integration Guide](../AGENT_INTEGRATION_ASSESSMENT_REPORT.md)
- [System Architecture](../README_MODULAR_V2_SYSTEM.md)

### Examples
- [Demo Script](../examples/demo_knowledge_database.py)
- [CLI Usage Examples](#cli-usage)
- [Python API Examples](#python-api-usage)

### Support
- Check existing knowledge in the database
- Search for similar issues
- Add new knowledge to help others

---

**🎯 Goal**: Create a collaborative knowledge ecosystem where agents can learn from each other and build collective intelligence.

**🚀 Status**: Ready for production use with full CLI and Python API support.
