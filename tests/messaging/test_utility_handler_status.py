"""Tests for utility handler status checks."""

import importlib.util
from pathlib import Path
import sys
import types


def _load_vector_models():
    module_path = (
        Path(__file__).resolve().parents[2]
        / "src/services/vector_database/vector_database_models.py"
    )
    spec = importlib.util.spec_from_file_location("vector_models", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.SearchResult, module.VectorDocument


def _load_utility_handler():
    root = Path(__file__).resolve().parents[2]
    sys.path.insert(0, str(root))
    package = "src.services.handlers"
    sys.modules.setdefault("src", types.ModuleType("src"))
    sys.modules["src"].__path__ = [str(root / "src")]
    sys.modules.setdefault("src.services", types.ModuleType("src.services"))
    sys.modules["src.services"].__path__ = [str(root / "src/services")]
    sys.modules.setdefault(package, types.ModuleType(package))
    sys.modules[package].__path__ = [str(root / "src/services/handlers")]
    sys.modules["src"].services = sys.modules["src.services"]
    sys.modules["src.services"].handlers = sys.modules[package]
    module_path = root / "src/services/handlers/utility_handler.py"
    spec = importlib.util.spec_from_file_location(
        f"{package}.utility_handler", module_path
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[f"{package}.utility_handler"] = module
    spec.loader.exec_module(module)
    setattr(sys.modules[package], "utility_handler", module)
    return module.UtilityHandler


def test_check_status_returns_matches(monkeypatch):
    UtilityHandler = _load_utility_handler()
    SearchResult, VectorDocument = _load_vector_models()
    handler = UtilityHandler()

    class DummyService:
        def search_by_content(self, query_text, collection_name="agent_status", limit=5, similarity_threshold=0.7):  # noqa: D401
            doc = VectorDocument(
                id="status_Agent-1",
                content="networking issues detected",
                metadata={"agent_id": "Agent-1"},
            )
            return [SearchResult(document=doc, similarity_score=0.9, rank=0, collection_name=collection_name)]

    fake_module = types.ModuleType(
        "src.services.vector_database.vector_database_orchestrator"
    )
    fake_module.get_vector_database_service = lambda: DummyService()
    sys.modules[
        "src.services.vector_database.vector_database_orchestrator"
    ] = fake_module

    fake_paths = types.ModuleType("src.core.constants.paths")
    fake_paths.get_agent_status_file = (
        lambda agent_num: Path(__file__).resolve().parents[2]
        / f"agent_workspaces/Agent-{agent_num}/status.json"
    )
    root = Path(__file__).resolve().parents[2]
    sys.modules.setdefault("src.core", types.ModuleType("src.core"))
    sys.modules["src.core"].__path__ = [str(root / "src/core")]
    sys.modules.setdefault("src.core.constants", types.ModuleType("src.core.constants"))
    sys.modules["src.core.constants"].__path__ = [str(root / "src/core/constants")]
    sys.modules["src.core.constants"].paths = fake_paths
    sys.modules["src"].core = sys.modules["src.core"]
    sys.modules["src.core"].constants = sys.modules["src.core.constants"]
    sys.modules["src.core.constants.paths"] = fake_paths

    result = handler.check_status(query="networking issues")
    assert result["statuses"]["Agent-1"] is True
    assert result["matches"][0]["agent_id"] == "Agent-1"
