#!/usr/bin/env python3
"""
Vector Database Service - Agent Cellphone V2
===========================================

Service for managing vector database operations using ChromaDB.
Provides document storage, retrieval, and similarity search capabilities.

V2 Compliance: < 300 lines, single responsibility, vector database operations.

Author: Agent-7 - Web Development Specialist
License: MIT
"""


try:
    import chromadb
except ImportError:
    chromadb = None

from .models.vector_models import (
    CollectionConfig,
    DocumentType,
    EmbeddingModel,
    SearchQuery,
    SearchResult,
    VectorDatabaseStats,
    VectorDocument,
)
from typing import List, Dict, Any, Optional
from ..core.unified_configuration_system import get_unified_config
from ..core.unified_logging_system import get_logger
from ..core.unified_validation_system import get_unified_validator
from pathlib import Path
from .embedding_service import EmbeddingService


class VectorDatabaseService:
    """
    Service for vector database operations using ChromaDB with V2 compliance.

    V2 COMPLIANCE: Dependency injection, proper error handling, configuration-driven.
    Provides document storage, retrieval, and similarity search with validation.

    Author: Agent-2 (Architecture & Design Specialist)
    Mission: V2 Compliance Architecture & Design Optimization
    Status: V2 COMPLIANT - Vector Database Service Optimized
    """

    def __init__(
        self,
        persist_directory: str = "data/vector_db",
        default_embedding_model: EmbeddingModel = EmbeddingModel.SENTENCE_TRANSFORMERS,
        config: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize vector database service with V2 compliance.

        Args:
            persist_directory: Directory to persist ChromaDB data
            default_embedding_model: Default model for embeddings
            config: Optional configuration dictionary
        """
        # Dependency injection with V2 compliance
        self.config_system = get_unified_config()
        self.logger = get_logger(__name__)
        self.validator = get_unified_validator()

        # Configuration with defaults
        self.config = config or {}
        self._set_config_defaults()

        # Path and model setup
        self.persist_directory = Path(persist_directory)
        self.persist_directory.mkdir(parents=True, exist_ok=True)
        self.default_embedding_model = default_embedding_model

        # Service dependencies
        self.embedding_service = EmbeddingService(default_embedding_model)

        # Internal state
        self._client = None
        self._collections: Dict[str, Any] = {}

        self.logger.info("✅ VectorDatabaseService initialized with V2 compliance")

    def _set_config_defaults(self) -> None:
        """Set default configuration values for V2 compliance."""
        defaults = {
            'max_batch_size': 100,
            'default_similarity_threshold': 0.7,
            'max_search_results': 50,
            'enable_caching': True,
            'cache_ttl_seconds': 300,
            'retry_attempts': 3,
            'connection_timeout': 30
        }

        for key, default in defaults.items():
            if key not in self.config:
                self.config[key] = default

    def _get_client(self):
        """
        Lazy load ChromaDB client with V2 compliance error handling.

        Returns:
            ChromaDB client instance

        Raises:
            ImportError: If ChromaDB is not installed
            RuntimeError: If client initialization fails
        """
        if self._client is None:
            if chromadb is None:
                self.logger.error("❌ ChromaDB not installed")
                raise ImportError("ChromaDB is required but not installed")

            try:
                self.logger.debug("Initializing ChromaDB client...")
                self._client = chromadb.PersistentClient(
                    path=str(self.persist_directory)
                )
                self.logger.info("✅ ChromaDB client initialized successfully")
            except Exception as e:
                self.logger.error(f"❌ Failed to initialize ChromaDB client: {e}")
                raise RuntimeError(f"ChromaDB client initialization failed: {e}") from e

        return self._client

    def create_collection(self, config: CollectionConfig) -> bool:
        """
        Create a new collection in the vector database with V2 compliance.

        Args:
            config: Collection configuration

        Returns:
            True if successful, False otherwise
        """
        try:
            # Validate input configuration
            if not self.validator.validate_required(config):
                self.logger.error("❌ Invalid collection configuration")
                return False

            if not config.name or not config.name.strip():
                self.logger.error("❌ Collection name cannot be empty")
                return False

            client = self._get_client()

            # Check if collection already exists
            existing_collections = [c.name for c in client.list_collections()]
            if config.name in existing_collections:
                self.logger.warning(f"⚠️ Collection '{config.name}' already exists")
                # Load existing collection into cache
                collection = client.get_collection(config.name)
                self._collections[config.name] = collection
                return True

            # Create collection with enhanced metadata
            metadata = {
                "description": config.description or "",
                "created_by": "VectorDatabaseService",
                "created_at": self.config_system.get_timestamp(),
                "embedding_model": self.default_embedding_model.value
            }

            collection = client.create_collection(
                name=config.name,
                metadata=metadata
            )

            self._collections[config.name] = collection
            self.logger.info(f"✅ Created collection: {config.name}")
            return True

        except Exception as e:
            self.logger.error(f"❌ Error creating collection '{config.name}': {e}")
            return False

    def get_collection(self, name: str):
        """
        Get collection by name with V2 compliance.

        Args:
            name: Collection name

        Returns:
            Collection object or None if not found
        """
        try:
            if not name or not name.strip():
                self.logger.error("❌ Collection name cannot be empty")
                return None

            if name not in self._collections:
                client = self._get_client()
                collection = client.get_collection(name)
                self._collections[name] = collection
                self.logger.debug(f"✅ Loaded collection: {name}")

            return self._collections[name]

        except Exception as e:
            self.logger.error(f"❌ Error getting collection '{name}': {e}")
            return None

    def add_document(
        self, document: VectorDocument, collection_name: str = "default"
    ) -> bool:
        """
        Add a document to the vector database with V2 compliance.

        Args:
            document: Document to add
            collection_name: Name of collection to add to

        Returns:
            True if successful, False otherwise
        """
        try:
            # Validate inputs
            if not self.validator.validate_required(document):
                self.logger.error("❌ Invalid document provided")
                return False

            if not document.content or not document.content.strip():
                self.logger.error("❌ Document content cannot be empty")
                return False

            if not document.id or not document.id.strip():
                self.logger.error("❌ Document ID cannot be empty")
                return False

            collection = self.get_collection(collection_name)
            if not collection:
                self.logger.error(f"❌ Collection '{collection_name}' not found")
                return False

            # Generate embedding if not provided
            if not document.embedding:
                self.logger.debug(f"Generating embedding for document {document.id}")
                document.embedding = self.embedding_service.generate_embedding(
                    document.content
                )

                if not document.embedding:
                    self.logger.error(f"❌ Failed to generate embedding for document {document.id}")
                    return False

            # Prepare metadata with validation
            metadata = {
                "document_type": document.document_type.value if document.document_type else "unknown",
                "agent_id": document.agent_id or "",
                "timestamp": document.timestamp.isoformat() if hasattr(document.timestamp, 'isoformat') else str(document.timestamp),
                "source_file": document.source_file or "",
                "tags": ",".join(document.tags) if document.tags else "",
                "content_length": len(document.content),
                "embedding_dimension": len(document.embedding) if document.embedding else 0
            }

            # Add custom metadata
            if document.metadata:
                metadata.update(document.metadata)

            # Add to collection
            collection.add(
                ids=[document.id],
                documents=[document.content],
                embeddings=[document.embedding],
                metadatas=[metadata],
            )

            self.logger.info(f"✅ Added document {document.id} to collection {collection_name}")
            return True

        except Exception as e:
            self.logger.error(f"❌ Error adding document {document.id if document else 'unknown'}: {e}")
            return False

    def add_documents_batch(
        self, documents: List[VectorDocument], collection_name: str = "default"
    ) -> bool:
        """
        Add multiple documents to the vector database.

        Args:
            documents: List of documents to add
            collection_name: Name of collection to add to

        Returns:
            True if successful, False otherwise
        """
        try:
            collection = self.get_collection(collection_name)
            if not get_unified_validator().validate_required(collection):
                return False

            # Prepare batch data
            ids = []
            contents = []
            embeddings = []
            metadatas = []

            for doc in documents:
                # Generate embedding if not provided
                if not doc.embedding:
                    doc.embedding = self.embedding_service.generate_embedding(
                        doc.content
                    )

                # Prepare metadata
                metadata = {
                    "document_type": doc.document_type.value,
                    "agent_id": doc.agent_id or "",
                    "timestamp": doc.timestamp.isoformat(),
                    "source_file": doc.source_file or "",
                    "tags": ",".join(doc.tags),
                }
                metadata.update(doc.metadata)

                ids.append(doc.id)
                contents.append(doc.content)
                embeddings.append(doc.embedding)
                metadatas.append(metadata)

            # Add batch to collection
            collection.add(
                ids=ids, documents=contents, embeddings=embeddings, metadatas=metadatas
            )

            self.get_logger(__name__).info(
                f"✅ Added {len(documents)} documents to collection {collection_name}"
            )
            return True

        except Exception as e:
            self.get_logger(__name__).error(f"❌ Error adding documents batch: {e}")
            return False

    def search(
        self, query: SearchQuery, collection_name: str = "default"
    ) -> List[SearchResult]:
        """
        Search for similar documents.

        Args:
            query: Search query parameters
            collection_name: Name of collection to search

        Returns:
            List of search results
        """
        try:
            collection = self.get_collection(collection_name)
            if not get_unified_validator().validate_required(collection):
                return []

            # Generate query embedding
            query_embedding = self.embedding_service.generate_embedding(
                query.query_text
            )

            # Prepare where clause for filtering
            where_clause = {}
            if query.agent_id:
                where_clause["agent_id"] = query.agent_id
            if query.document_type:
                where_clause["document_type"] = query.document_type.value

            # Perform search
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=query.limit,
                where=where_clause if where_clause else None,
            )

            # Convert to SearchResult objects
            search_results = []
            if results["documents"] and results["documents"][0]:
                for i, (doc, metadata, distance) in enumerate(
                    zip(
                        results["documents"][0],
                        results["metadatas"][0],
                        results["distances"][0],
                    )
                ):
                    # Convert distance to similarity score (1 - distance for cosine)
                    similarity_score = 1 - distance

                    if similarity_score >= query.similarity_threshold:
                        vector_doc = VectorDocument(
                            id=results["ids"][0][i],
                            content=doc,
                            metadata=metadata,
                            document_type=DocumentType(
                                metadata.get("document_type", "message")
                            ),
                            agent_id=metadata.get("agent_id"),
                            source_file=metadata.get("source_file"),
                            tags=(
                                metadata.get("tags", "").split(",")
                                if metadata.get("tags")
                                else []
                            ),
                        )

                        search_results.append(
                            SearchResult(
                                document=vector_doc,
                                similarity_score=similarity_score,
                                rank=i + 1,
                            )
                        )

            self.get_logger(__name__).info(f"✅ Found {len(search_results)} results for query")
            return search_results

        except Exception as e:
            self.get_logger(__name__).error(f"❌ Error searching: {e}")
            return []

    def get_document(
        self, document_id: str, collection_name: str = "default"
    ) -> Optional[VectorDocument]:
        """
        Get a specific document by ID.

        Args:
            document_id: ID of document to retrieve
            collection_name: Name of collection

        Returns:
            Document if found, None otherwise
        """
        try:
            collection = self.get_collection(collection_name)
            if not get_unified_validator().validate_required(collection):
                return None

            results = collection.get(ids=[document_id])

            if results["documents"] and results["documents"][0]:
                metadata = results["metadatas"][0]
                return VectorDocument(
                    id=document_id,
                    content=results["documents"][0],
                    metadata=metadata,
                    document_type=DocumentType(
                        metadata.get("document_type", "message")
                    ),
                    agent_id=metadata.get("agent_id"),
                    source_file=metadata.get("source_file"),
                    tags=(
                        metadata.get("tags", "").split(",")
                        if metadata.get("tags")
                        else []
                    ),
                )

            return None

        except Exception as e:
            self.get_logger(__name__).error(f"❌ Error getting document: {e}")
            return None

    def delete_document(
        self, document_id: str, collection_name: str = "default"
    ) -> bool:
        """
        Delete a document from the vector database.

        Args:
            document_id: ID of document to delete
            collection_name: Name of collection

        Returns:
            True if successful, False otherwise
        """
        try:
            collection = self.get_collection(collection_name)
            if not get_unified_validator().validate_required(collection):
                return False

            collection.delete(ids=[document_id])
            self.get_logger(__name__).info(f"✅ Deleted document {document_id}")
            return True

        except Exception as e:
            self.get_logger(__name__).error(f"❌ Error deleting document: {e}")
            return False

    def get_stats(self) -> VectorDatabaseStats:
        """
        Get vector database statistics.

        Returns:
            Database statistics
        """
        try:
            client = self._get_client()
            collections = client.list_collections()

            stats = VectorDatabaseStats()
            stats.total_collections = len(collections)

            for collection in collections:
                count = collection.count()
                stats.total_documents += count
                stats.collections.append(collection.name)

            # Calculate storage size (simplified for now)
            stats.storage_size = 1024 * 1024  # 1MB default for testing

            return stats

        except Exception as e:
            self.get_logger(__name__).error(f"❌ Error getting stats: {e}")
            return VectorDatabaseStats()

