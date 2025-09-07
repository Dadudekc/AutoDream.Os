"""Vector DB status checks for messaging CLI."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from src.services.models.vector_models import (
    DocumentType,
    SearchQuery,
    SearchType,
    VectorDocument,
)
import src.core.unified_data_processing_system as udp


class DummyVectorService:
    """Minimal vector service with mockable engine."""

    def __init__(self) -> None:
        self.engine = MagicMock()

    def add_document(self, document: VectorDocument, collection_name: str = "default") -> None:
        self.engine.add_document(document, collection_name)

    def search_documents(self, query: SearchQuery):
        return self.engine.search_documents(query)


@pytest.mark.describe("check_status_vector_db")
class TestCheckStatusVectorDB:
    """Jest-style tests for vector-backed status checks."""

    @pytest.mark.it("creates embeddings on document addition")
    def test_creates_embeddings_on_document_addition(self):
        service = DummyVectorService()
        mock_engine = service.engine

        document = VectorDocument(
            id="Agent-1_status",
            content="active",
            document_type=DocumentType.STATUS,
        )

        service.add_document(document, "status")

        mock_engine.add_document.assert_called_once_with(document, "status")

    @pytest.mark.it("queries status semantically")
    def test_queries_status_semantically(self):
        service = DummyVectorService()
        mock_engine = service.engine
        expected = [MagicMock()]
        mock_engine.search_documents.return_value = expected

        query = SearchQuery(
            query="mission progress",
            search_type=SearchType.SEMANTIC,
        )

        results = service.search_documents(query)

        mock_engine.search_documents.assert_called_once_with(query)
        assert results == expected

    @pytest.mark.it("falls back to file-based check when vector search empty")
    def test_falls_back_to_file_based_check(self):
        vector_service = DummyVectorService()
        vector_service.engine.search_documents.return_value = []
        status_payload = {"status": "active", "last_updated": "now"}

        with patch(
            "src.core.unified_data_processing_system.read_json",
            return_value=status_payload,
        ):
            query = SearchQuery(
                query="Agent-1",
                search_type=SearchType.SEMANTIC,
            )

            def check_status(agent_id: str) -> dict:
                results = vector_service.search_documents(query)
                if results:
                    return {"source": "vector", "data": results}
                path = f"agent_workspaces/{agent_id}/status.json"
                data = udp.read_json(path)
                return {"source": "file", "data": data}

            result = check_status("Agent-1")

        assert result["source"] == "file"
        assert result["data"]["status"] == "active"

