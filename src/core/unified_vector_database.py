#!/usr/bin/env python3
"""
Unified Vector Database - V2 Compliance (< 300 lines)
===============================================

Single source of truth for vector database operations.
Eliminates duplication between ChromaDB and Simple implementations.
Provides unified interface with backend switching capability.

V2 Compliance: Single responsibility, dependency injection, < 300 lines

Author: Agent-4 - Strategic Oversight & Emergency Intervention Manager
"""


logger = logging.getLogger(__name__)


class VectorDatabaseInterface(Protocol):
    """Unified interface for vector database implementations."""

    def add_document(self, doc_id: str, content: str, metadata: Dict[str, Any]) -> bool:
        """Add document to database."""
        ...

    def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search documents by semantic similarity."""
        ...

    def get_document(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve specific document."""
        ...

    def delete_document(self, doc_id: str) -> bool:
        """Delete document from database."""
        ...

    def list_documents(self) -> List[str]:
        """List all document IDs."""
        ...


class VectorDatabaseFactory:
    """Factory for creating vector database instances."""

    @staticmethod
    def create(backend: str = "simple", **kwargs) -> VectorDatabaseInterface:
        """Create vector database instance with specified backend."""
        if backend == "chromadb":
            return ChromaDBVectorDatabase(**kwargs)
        elif backend == "simple":
            return SimpleVectorDatabase(**kwargs)
        else:
            get_unified_validator().raise_validation_error(f"Unknown backend: {backend}")


class ChromaDBVectorDatabase(VectorDatabaseInterface):
    """ChromaDB implementation - Production-grade semantic search."""

    def __init__(
        self, db_path: str = "vector_db", collection_name: str = "project_docs"
    ):
        try:

            self.db_path = db_path
            self.collection_name = collection_name
            self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

            self.client = chromadb.PersistentClient(
                path=db_path,
                settings=Settings(anonymized_telemetry=False, allow_reset=True),
            )

            try:
                self.collection = self.client.get_collection(collection_name)
            except:
                self.collection = self.client.create_collection(collection_name)

            get_logger(__name__).info(f"ChromaDB initialized: {collection_name}")
        except ImportError as e:
            get_logger(__name__).error(f"ChromaDB dependencies not available: {e}")
            raise RuntimeError("ChromaDB backend requires additional dependencies")

    def add_document(self, doc_id: str, content: str, metadata: Dict[str, Any]) -> bool:
        """Add document with semantic embedding."""
        try:
            embedding = self.embedding_model.encode(content).tolist()
            self.collection.add(
                documents=[content],
                embeddings=[embedding],
                metadatas=[metadata],
                ids=[doc_id],
            )
            return True
        except Exception as e:
            get_logger(__name__).error(f"Failed to add document {doc_id}: {e}")
            return False

    def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Semantic search using embeddings."""
        try:
            query_embedding = self.embedding_model.encode(query).tolist()
            results = self.collection.query(
                query_embeddings=[query_embedding], n_results=limit
            )

            return [
                {
                    "id": doc_id,
                    "content": content,
                    "metadata": metadata,
                    "score": distance,
                }
                for doc_id, content, metadata, distance in zip(
                    results["ids"][0] if results["ids"] else [],
                    results["documents"][0] if results["documents"] else [],
                    results["metadatas"][0] if results["metadatas"] else [],
                    results["distances"][0] if results["distances"] else [],
                )
            ]
        except Exception as e:
            get_logger(__name__).error(f"Search failed: {e}")
            return []

    def get_document(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve document by ID."""
        try:
            result = self.collection.get(ids=[doc_id])
            if result["documents"]:
                return {
                    "id": doc_id,
                    "content": result["documents"][0],
                    "metadata": result["metadatas"][0],
                }
        except Exception as e:
            get_logger(__name__).error(f"Failed to get document {doc_id}: {e}")
        return None

    def delete_document(self, doc_id: str) -> bool:
        """Delete document from collection."""
        try:
            self.collection.delete(ids=[doc_id])
            return True
        except Exception as e:
            get_logger(__name__).error(f"Failed to delete document {doc_id}: {e}")
            return False

    def list_documents(self) -> List[str]:
        """List all document IDs."""
        try:
            return self.collection.get()["ids"]
        except Exception as e:
            get_logger(__name__).error(f"Failed to list documents: {e}")
            return []


class SimpleVectorDatabase(VectorDatabaseInterface):
    """Simple TF-IDF implementation - No external dependencies."""

    def __init__(
        self, db_path: str = "simple_vector_db", collection_name: str = "project_docs"
    ):
        self.db_path = get_unified_utility().Path(db_path)
        self.collection_name = collection_name
        self.db_path.mkdir(exist_ok=True)

        self.documents_file = self.db_path / f"{collection_name}_documents.json"
        self.index_file = self.db_path / f"{collection_name}_index.json"

        self.documents = {}
        self.index = {}
        self.doc_frequencies = {}
        self.total_docs = 0

        self._load_database()

    def _load_database(self):
        """Load existing database from files."""
        try:
            if self.documents_file.exists():
                with open(self.documents_file, "r") as f:
                    self.documents = read_json(f)

            if self.index_file.exists():
                with open(self.index_file, "r") as f:
                    index_data = read_json(f)
                    self.index = index_data.get("index", {})
                    self.doc_frequencies = index_data.get("doc_frequencies", {})
                    self.total_docs = index_data.get("total_docs", 0)
        except Exception as e:
            get_logger(__name__).warning(f"Failed to load database: {e}")

    def _save_database(self):
        """Save database to files."""
        try:
            with open(self.documents_file, "w") as f:
                write_json(self.documents, f, indent=2)

            with open(self.index_file, "w") as f:
                write_json(
                    {
                        "index": self.index, "doc_frequencies": self.doc_frequencies,
                        "total_docs": self.total_docs,
                    },
                    f,
                    indent=2,
                )
        except Exception as e:
            get_logger(__name__).error(f"Failed to save database: {e}")

    def _tokenize(self, text: str) -> List[str]:
        """Simple tokenization."""
        return re.findall(r"\b\w+\b", text.lower())

    def _calculate_tf_idf(self, term: str, doc_id: str) -> float:
        """Calculate TF-IDF score."""
        if doc_id not in self.documents:
            return 0.0

        doc_content = self.documents[doc_id]["content"]
        term_freq = doc_content.lower().count(term.lower())

        if term_freq == 0:
            return 0.0

        tf = term_freq / len(self._tokenize(doc_content))
        idf = (
            1.0
            if self.doc_frequencies.get(term, 0) == 0
            else self.total_docs / self.doc_frequencies[term]
        )

        return tf * idf

    def add_document(self, doc_id: str, content: str, metadata: Dict[str, Any]) -> bool:
        """Add document to database."""
        try:
            self.documents[doc_id] = {
                "content": content,
                "metadata": metadata,
                "timestamp": datetime.now().isoformat(),
            }

            # Update index
            tokens = self._tokenize(content)
            for token in tokens:
                if token not in self.index:
                    self.index[token] = {}
                self.index[token][doc_id] = self.index[token].get(doc_id, 0) + 1

                if token not in self.doc_frequencies:
                    self.doc_frequencies[token] = 0
                self.doc_frequencies[token] += 1

            self.total_docs = len(self.documents)
            self._save_database()
            return True
        except Exception as e:
            get_logger(__name__).error(f"Failed to add document {doc_id}: {e}")
            return False

    def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search using TF-IDF similarity."""
        try:
            query_tokens = self._tokenize(query)
            doc_scores = defaultdict(float)

            for token in query_tokens:
                if token in self.index:
                    for doc_id in self.index[token]:
                        doc_scores[doc_id] += self._calculate_tf_idf(token, doc_id)

            # Sort by score and return top results
            sorted_docs = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)
            results = []

            for doc_id, score in sorted_docs[:limit]:
                if doc_id in self.documents:
                    results.append(
                        {
                            "id": doc_id,
                            "content": self.documents[doc_id]["content"],
                            "metadata": self.documents[doc_id]["metadata"],
                            "score": score,
                        }
                    )

            return results
        except Exception as e:
            get_logger(__name__).error(f"Search failed: {e}")
            return []

    def get_document(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve specific document."""
        return self.documents.get(doc_id)

    def delete_document(self, doc_id: str) -> bool:
        """Delete document from database."""
        try:
            if doc_id in self.documents:
                del self.documents[doc_id]

                # Remove from index
                for token_docs in self.index.values():
                    if doc_id in token_docs:
                        del token_docs[doc_id]

                self.total_docs = len(self.documents)
                self._save_database()
                return True
        except Exception as e:
            get_logger(__name__).error(f"Failed to delete document {doc_id}: {e}")
        return False

    def list_documents(self) -> List[str]:
        """List all document IDs."""
        return list(self.documents.keys())


# Convenience functions for easy usage
def create_vector_database(
    backend: str = "simple", **kwargs
) -> VectorDatabaseInterface:
    """Create vector database instance."""
    return VectorDatabaseFactory.create(backend, **kwargs)


def search_documents(
    db: VectorDatabaseInterface, query: str, limit: int = 5
) -> List[Dict[str, Any]]:
    """Search documents in database."""
    return db.search(query, limit)


def add_project_document(
    db: VectorDatabaseInterface, doc_id: str, content: str, doc_type: str = "general"
) -> bool:
    """Add project document with metadata."""
    metadata = {
        "type": doc_type,
        "timestamp": datetime.now().isoformat(),
        "word_count": len(content.split()),
    }
    return db.add_document(doc_id, content, metadata)


# Example usage and testing
if __name__ == "__main__":
    # Test both backends
    get_logger(__name__).info("Testing Simple Vector Database...")
    simple_db = create_vector_database("simple", db_path="test_simple_db")
    simple_db.add_document(
        "test1", "This is a test document about Python programming", {"type": "code"}
    )
    results = simple_db.search("Python programming")
    get_logger(__name__).info(f"Simple DB results: {len(results)}")

    get_logger(__name__).info("\nTesting ChromaDB (if available)...")
    try:
        chroma_db = create_vector_database("chromadb", db_path="test_chroma_db")
        chroma_db.add_document(
            "test1",
            "This is a test document about Python programming",
            {"type": "code"},
        )
        results = chroma_db.search("Python programming")
        get_logger(__name__).info(f"ChromaDB results: {len(results)}")
    except RuntimeError as e:
        get_logger(__name__).info(f"ChromaDB not available: {e}")

    get_logger(__name__).info("\nVector database consolidation complete!")
