from __future__ import annotations

import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.core.semantic.router_hooks import route_message, similar_status


def test_route_message_smoke():
    res = route_message("optimize database performance and add observability")
    assert "priority" in res
    assert "agent_suggestions" in res
    assert isinstance(res["agent_suggestions"], list)
    print("✅ route_message smoke test passed")


def test_similar_status_smoke():
    res = similar_status(
        {"status": "SURVEY_MISSION_COMPLETED", "survey_results": {"total_files_analyzed": 50}}
    )
    assert "results" in res
    assert isinstance(res["results"], list)
    print("✅ similar_status smoke test passed")


if __name__ == "__main__":
    print("🧪 Running semantic integration smoke tests...")
    test_route_message_smoke()
    test_similar_status_smoke()
    print("🎉 All smoke tests passed!")
