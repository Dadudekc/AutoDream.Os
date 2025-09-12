"""
Collection Utils
================

Collection management utility functions for vector database operations.
V2 Compliance: < 100 lines, single responsibility.

Author: Agent-3 - Infrastructure & DevOps Specialist
"""

from datetime import datetime

from .models import Collection, ExportData, ExportRequest


class CollectionUtils:
    """Utility functions for collection operations."""

    def simulate_get_collections(self) -> list[Collection]:
        """
        Simulate retrieval of collections.

        EXAMPLE USAGE:
        ==============

        # Basic usage example
        from src.web.vector_database.collection_utils import CollectionUtils

        # Initialize collection utils
        collections = CollectionUtils()

        # Get all collections
        result = collections.simulate_get_collections()
        print(f"Found {len(result)} collections")

        # Display collection information
        for collection in result:
            print(f"Collection: {collection.name}, Documents: {collection.document_count}")

        Returns:
            list[Collection]: List of available collections
        """
        # Simulate realistic collection data based on common use cases
        import random
        from datetime import datetime, timedelta

        # Generate sample collections for different domains
        collection_templates = [
            ("user_documents", 384, 150),
            ("code_repositories", 512, 75),
            ("knowledge_base", 768, 200),
            ("chat_history", 256, 300),
            ("analytics_data", 128, 50)
        ]

        collections = []
        base_time = datetime.utcnow()

        for name, dimension, base_docs in collection_templates:
            # Add some randomness to document counts and creation times
            doc_count = base_docs + random.randint(-20, 20)
            days_ago = random.randint(1, 30)
            created_at = (base_time - timedelta(days=days_ago)).isoformat() + "Z"

            collections.append(Collection(
                name=name,
                dimension=dimension,
                document_count=max(0, doc_count),  # Ensure non-negative
                created_at=created_at
            ))

        return collections

    def simulate_export_data(self, request: ExportRequest) -> ExportData:
        """
        Simulate data export operation.

        EXAMPLE USAGE:
        ==============

        # Export collection data
        from src.web.vector_database.collection_utils import CollectionUtils
        from src.web.vector_database.models import ExportRequest

        collections = CollectionUtils()
        export_request = ExportRequest(
            collection_name="my_collection",
            format="json",
            include_vectors=False
        )

        result = collections.simulate_export_data(export_request)
        print(f"Export completed: {result.collection_name}")

        Args:
            request: Export request parameters

        Returns:
            ExportData: Export result information
        """
        # Generate sample documents based on collection type
        import random
        from datetime import datetime

        # Determine document count based on collection name patterns
        base_docs = 50
        if "large" in request.collection_name.lower():
            base_docs = 200
        elif "small" in request.collection_name.lower():
            base_docs = 25

        doc_count = base_docs + random.randint(-10, 10)

        # Generate sample documents
        documents = []
        for i in range(max(1, doc_count)):
            doc = {
                "id": f"doc_{i:04d}",
                "content": f"Sample document content for {request.collection_name} - item {i}",
                "metadata": {
                    "source": f"source_{i % 5}",
                    "category": ["tech", "business", "science", "health", "education"][i % 5],
                    "created_at": (datetime.now().replace(hour=i % 24)).isoformat(),
                    "tags": [f"tag_{j}" for j in range(random.randint(1, 3))]
                }
            }

            # Include vectors if requested
            if request.include_vectors:
                # Generate a sample vector (simplified for demo)
                vector_dim = 384 if "document" in request.collection_name else 512
                doc["vector"] = [random.uniform(-1, 1) for _ in range(vector_dim)]

            documents.append(doc)

        return ExportData(
            collection_name=request.collection_name,
            documents=documents,
            exported_at=datetime.now().isoformat(),
            format=request.format
        )
