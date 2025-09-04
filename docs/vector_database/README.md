# Vector Database System - Agent Cellphone V2

A comprehensive vector database solution integrated with the Agent Cellphone V2 messaging system, providing semantic search capabilities for messages, devlogs, contracts, and other documents.

## Features

- **Semantic Search**: Find similar content based on meaning, not just keywords
- **Multiple Embedding Models**: Support for Sentence Transformers and OpenAI embeddings
- **ChromaDB Integration**: Persistent vector storage with high performance
- **Messaging Integration**: Automatic indexing of agent messages and communications
- **CLI Interface**: Command-line tools for database management
- **Comprehensive Testing**: Full test coverage with unit tests

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Vector Database System                   │
├─────────────────────────────────────────────────────────────┤
│  CLI Interface (vector_database_cli.py)                    │
├─────────────────────────────────────────────────────────────┤
│  Integration Layer (vector_messaging_integration.py)       │
├─────────────────────────────────────────────────────────────┤
│  Core Services                                              │
│  ├── Vector Database Service (vector_database_service.py)  │
│  ├── Embedding Service (embedding_service.py)              │
│  └── Configuration (vector_database_config.py)             │
├─────────────────────────────────────────────────────────────┤
│  Data Models (vector_models.py)                            │
├─────────────────────────────────────────────────────────────┤
│  ChromaDB (Persistent Storage)                             │
└─────────────────────────────────────────────────────────────┘
```

## Installation

### 1. Install Dependencies

```bash
# Install vector database dependencies
pip install -r requirements.txt --extra vector_db

# Or install specific packages
pip install chromadb sentence-transformers langchain langchain-community
```

### 2. Environment Configuration

Create a `.env` file with optional vector database settings:

```bash
# Vector Database Configuration
VECTOR_DB_DIRECTORY=data/vector_db
VECTOR_DB_DEFAULT_COLLECTION=default
VECTOR_DB_EMBEDDING_MODEL=sentence-transformers
VECTOR_DB_BATCH_SIZE=32
VECTOR_DB_SEARCH_LIMIT=10
VECTOR_DB_SIMILARITY_THRESHOLD=0.0

# OpenAI Configuration (if using OpenAI embeddings)
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_EMBEDDING_MODEL=text-embedding-ada-002

# Performance Settings
VECTOR_DB_ENABLE_CACHING=true
VECTOR_DB_CACHE_SIZE=1000
```

## Usage

### CLI Commands

#### Search Commands

```bash
# Search all content
python -m src.services.vector_database_cli search "agent coordination"

# Search only messages
python -m src.services.vector_database_cli search "urgent task" --type messages

# Search only devlogs
python -m src.services.vector_database_cli search "system update" --type devlogs

# Search with filters
python -m src.services.vector_database_cli search "contract" --agent Agent-1 --limit 5

# Search with similarity threshold
python -m src.services.vector_database_cli search "error" --threshold 0.7
```

#### Indexing Commands

```bash
# Index agent inbox
python -m src.services.vector_database_cli index --inbox agent_workspaces/Agent-1/inbox --agent Agent-1

# Index single file
python -m src.services.vector_database_cli index --file docs/README.md

# Index with verbose output
python -m src.services.vector_database_cli index --inbox agent_workspaces/Agent-1/inbox --verbose
```

#### Management Commands

```bash
# Show database statistics
python -m src.services.vector_database_cli stats

# List all collections
python -m src.services.vector_database_cli collections

# Find related messages
python -m src.services.vector_database_cli related msg_20240101_120000_abc123 --limit 3
```

### Programmatic Usage

#### Basic Search

```python
from src.services.vector_messaging_integration import VectorMessagingIntegration
from src.services.vector_database_config import VectorDatabaseConfig

# Initialize integration
config = VectorDatabaseConfig()
integration = VectorMessagingIntegration(config)

# Search for similar messages
results = integration.search_messages(
    query_text="urgent task assignment",
    agent_id="Agent-1",
    limit=5,
    similarity_threshold=0.7
)

# Process results
for result in results:
    print(f"Similarity: {result.similarity_score:.3f}")
    print(f"Content: {result.document.content[:100]}...")
    print(f"Agent: {result.document.agent_id}")
    print()
```

#### Indexing Messages

```python
from src.services.models.messaging_models import UnifiedMessage, MessageType, Priority

# Create a message
message = UnifiedMessage(
    message_id="msg_123",
    content="Please complete the urgent task assignment",
    sender="Captain Agent-4",
    recipient="Agent-1",
    message_type=MessageType.TEXT,
    priority=Priority.URGENT
)

# Index the message
success = integration.index_message(message)
if success:
    print("Message indexed successfully")
```

#### Advanced Search

```python
# Search across all document types
results = integration.search_all(
    query_text="system architecture",
    limit=10,
    similarity_threshold=0.5
)

# Find related messages
related = integration.get_related_messages("msg_123", limit=3)

# Search devlogs with category filter
devlog_results = integration.search_devlogs(
    query_text="performance optimization",
    category="technical",
    limit=5
)
```

## Configuration

### Vector Database Configuration

The `VectorDatabaseConfig` class provides comprehensive configuration options:

```python
from src.services.vector_database_config import VectorDatabaseConfig

config = VectorDatabaseConfig(
    persist_directory="data/vector_db",
    default_collection="default",
    default_embedding_model=EmbeddingModel.SENTENCE_TRANSFORMERS,
    embedding_batch_size=32,
    default_search_limit=10,
    default_similarity_threshold=0.0,
    enable_caching=True,
    cache_size=1000
)
```

### Embedding Models

Supported embedding models:

- **Sentence Transformers**: `all-MiniLM-L6-v2` (default, 384 dimensions)
- **OpenAI ADA**: `text-embedding-ada-002` (1536 dimensions)
- **OpenAI 3 Small**: `text-embedding-3-small` (1536 dimensions)
- **OpenAI 3 Large**: `text-embedding-3-large` (3072 dimensions)

### Document Types

The system supports various document types:

- `MESSAGE`: Agent messages and communications
- `DEVLOG`: Development log entries
- `CONTRACT`: Task contracts and assignments
- `CODE`: Source code files
- `DOCUMENTATION`: Documentation files
- `CONFIG`: Configuration files
- `STATUS`: Status and monitoring data

## API Reference

### VectorMessagingIntegration

Main integration class for vector database operations.

#### Methods

- `index_message(message: UnifiedMessage) -> bool`: Index a message
- `index_devlog_entry(entry: Dict[str, Any]) -> bool`: Index a devlog entry
- `search_messages(query_text: str, **kwargs) -> List[SearchResult]`: Search messages
- `search_devlogs(query_text: str, **kwargs) -> List[SearchResult]`: Search devlogs
- `search_all(query_text: str, **kwargs) -> List[SearchResult]`: Search all content
- `get_related_messages(message_id: str, limit: int) -> List[SearchResult]`: Find related messages
- `index_inbox_files(agent_id: str, inbox_path: str) -> int`: Index inbox files
- `get_database_stats() -> Dict[str, Any]`: Get database statistics

### VectorDatabaseService

Core vector database operations.

#### Methods

- `create_collection(config: CollectionConfig) -> bool`: Create a collection
- `add_document(document: VectorDocument, collection_name: str) -> bool`: Add document
- `add_documents_batch(documents: List[VectorDocument], collection_name: str) -> bool`: Add multiple documents
- `search(query: SearchQuery, collection_name: str) -> List[SearchResult]`: Search documents
- `get_document(document_id: str, collection_name: str) -> Optional[VectorDocument]`: Get document
- `delete_document(document_id: str, collection_name: str) -> bool`: Delete document
- `get_stats() -> VectorDatabaseStats`: Get database statistics

### EmbeddingService

Text embedding generation.

#### Methods

- `generate_embedding(text: str, model: EmbeddingModel) -> List[float]`: Generate single embedding
- `generate_embeddings_batch(texts: List[str], model: EmbeddingModel, batch_size: int) -> List[List[float]]`: Generate batch embeddings
- `get_embedding_dimension(model: EmbeddingModel) -> int`: Get embedding dimension
- `validate_text(text: str) -> bool`: Validate text for embedding
- `preprocess_text(text: str) -> str`: Preprocess text

## Testing

Run the test suite:

```bash
# Run all vector database tests
pytest tests/vector_database/ -v

# Run specific test files
pytest tests/vector_database/test_vector_models.py -v
pytest tests/vector_database/test_embedding_service.py -v
pytest tests/vector_database/test_vector_database_service.py -v

# Run with coverage
pytest tests/vector_database/ --cov=src.services --cov-report=html
```

## Performance Considerations

### Embedding Generation

- **Batch Processing**: Use batch operations for multiple documents
- **Model Selection**: Sentence Transformers for local processing, OpenAI for higher quality
- **Caching**: Enable caching for frequently accessed embeddings

### Search Performance

- **Similarity Threshold**: Use appropriate thresholds to filter results
- **Limit Results**: Set reasonable limits to avoid large result sets
- **Collection Organization**: Use separate collections for different document types

### Storage

- **Persistent Storage**: ChromaDB automatically persists to disk
- **Collection Management**: Regular cleanup of old or unused collections
- **Backup**: Regular backups of the vector database directory

## Troubleshooting

### Common Issues

1. **ChromaDB Import Error**
   ```bash
   pip install chromadb
   ```

2. **Sentence Transformers Model Download**
   ```python
   # First run will download the model
   from sentence_transformers import SentenceTransformer
   model = SentenceTransformer('all-MiniLM-L6-v2')
   ```

3. **OpenAI API Key Missing**
   ```bash
   export OPENAI_API_KEY=your_api_key_here
   ```

4. **Permission Errors**
   ```bash
   # Ensure write permissions for data directory
   chmod 755 data/vector_db
   ```

### Debug Mode

Enable verbose logging:

```bash
python -m src.services.vector_database_cli search "test" --verbose
```

Or programmatically:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Integration with Messaging System

The vector database automatically integrates with the existing messaging system:

1. **Message Indexing**: New messages are automatically indexed
2. **Devlog Integration**: Devlog entries are indexed for search
3. **Contract Search**: Task contracts are searchable
4. **Agent Coordination**: Find related communications between agents

## Future Enhancements

- **Real-time Indexing**: Automatic indexing of new messages
- **Advanced Filtering**: More sophisticated search filters
- **Multi-modal Support**: Support for images and other media
- **Federated Search**: Search across multiple vector databases
- **Analytics Dashboard**: Web interface for database management

## Contributing

When contributing to the vector database system:

1. Follow V2 compliance standards (< 300 lines per file)
2. Add comprehensive unit tests
3. Update documentation
4. Use type hints and proper error handling
5. Follow the existing architecture patterns

## License

MIT License - see LICENSE file for details.

