from __future__ import annotations

import json
import tempfile
from pathlib import Path

from src.core.semantic.status_index import StatusIndex


def test_status_similarity():
    """Test status similarity search functionality."""

    # Create temporary directory for test
    with tempfile.TemporaryDirectory() as tmp_path:
        tmp_path = Path(tmp_path)

        cfg = {
            "status_index": {
                "seed_dir": str(tmp_path),
                "store_path": str(tmp_path / "store"),
                "top_k": 3,
                "min_confidence": 0.0,
            },
            "store": {"backend": "numpy", "normalize": True},
            "embedding": {"provider": "hash", "dim": 128},
        }

        # Seed two test statuses
        a1 = {
            "agent_id": "Agent-1",
            "status": "SURVEY_MISSION_COMPLETED",
            "current_tasks": ["Survey mission completed successfully"],
            "completed_tasks": ["analysis of src/services/"],
            "achievements": ["survey done"],
            "survey_results": {"total_files_analyzed": 50, "consolidation_opportunities": 50},
        }
        a2 = {
            "agent_id": "Agent-3",
            "status": "INFRA_AUDIT_PROGRESS",
            "current_tasks": ["dockerization"],
            "completed_tasks": ["CI pipeline sketch"],
            "achievements": ["infra baseline"],
            "survey_results": {"total_files_analyzed": 10, "consolidation_opportunities": 5},
        }

        # Write test files
        p1 = tmp_path / "Agent-1.json"
        p2 = tmp_path / "Agent-3.json"
        p1.write_text(json.dumps(a1), encoding="utf-8")
        p2.write_text(json.dumps(a2), encoding="utf-8")

        # Test ingestion
        idx = StatusIndex(cfg)
        n = idx.ingest_dir(cfg["status_index"]["seed_dir"])
        assert n == 2, f"Expected 2 files ingested, got {n}"

        # Test text similarity search
        hits = idx.similar("survey completed, 50 files analyzed")
        assert len(hits) >= 1, "Expected at least 1 similar result"
        assert hits[0][0] == "Agent-1", f"Expected Agent-1 as most similar, got {hits[0][0]}"

        # Test JSON similarity search
        hits2 = idx.similar(
            {"status": "SURVEY_MISSION_COMPLETED", "survey_results": {"total_files_analyzed": 50}}
        )
        assert len(hits2) >= 1, "Expected at least 1 similar result from JSON query"

        print("✅ All status similarity tests passed!")


if __name__ == "__main__":
    test_status_similarity()
