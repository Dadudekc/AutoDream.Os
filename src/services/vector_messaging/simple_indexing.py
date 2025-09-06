#!/usr/bin/env python3
"""
Simple Document Indexing - KISS Compliant
=========================================

Simple document indexing utilities.
KISS PRINCIPLE: Keep It Simple, Stupid.

Author: Agent-6 - Coordination & Communication Specialist
License: MIT
"""

from datetime import datetime
from typing import Dict, List, Any


class SimpleDocumentIndexer:
    """Simple document indexing utilities."""

    def __init__(self):
        self.indexed_docs: List[Dict] = []

    def index_document(self, doc_id: str, content: str, doc_type: str = "text") -> bool:
        """Index a document."""
        try:
            doc = {
                "id": doc_id,
                "content": content,
                "type": doc_type,
                "indexed_at": datetime.now(),
            }
            self.indexed_docs.append(doc)
            return True
        except:
            return False

    def search_documents(self, query: str) -> List[Dict]:
        """Search indexed documents."""
        results = []
        for doc in self.indexed_docs:
            if query.lower() in doc["content"].lower():
                results.append(doc)
        return results

    def get_document(self, doc_id: str) -> Dict:
        """Get a specific document."""
        for doc in self.indexed_docs:
            if doc["id"] == doc_id:
                return doc
        return {}

    def get_index_stats(self) -> Dict[str, Any]:
        """Get indexing statistics."""
        return {
            "total_documents": len(self.indexed_docs),
            "last_indexed": (
                self.indexed_docs[-1]["indexed_at"] if self.indexed_docs else None
            ),
        }
