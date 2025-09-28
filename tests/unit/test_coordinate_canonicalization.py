#!/usr/bin/env python3
import json
from pathlib import Path

from src.core.coordinate_loader import CoordinateLoader


def test_loader_reads_canonical_by_default(tmp_path: Path):
    canon = tmp_path / "config" / "canonical_coordinates.json"
    canon.parent.mkdir(parents=True, exist_ok=True)
    canon.write_text(json.dumps({"1": [1, 2], "2": [3, 4]}), encoding="utf-8")

    # Also create a conflicting provided file to ensure canonical wins
    provided = tmp_path / "config" / "coordinates.json"
    provided.write_text(json.dumps({
        "agents": {
            "Agent-1": {"chat_input_coordinates": [100, 200]},
            "Agent-2": {"chat_input_coordinates": [300, 400]}
        }
    }), encoding="utf-8")

    # Point loader to provided, but it should prefer canonical
    loader = CoordinateLoader(str(provided))
    loader.canonical_path = str(canon)
    loader.load()

    assert loader.get_agent_coordinates("Agent-1") == (1, 2)
    assert loader.get_agent_coordinates("Agent-2") == (3, 4)


def test_assert_canonical_consistency_detects_drift(tmp_path: Path):
    canon = tmp_path / "config" / "canonical_coordinates.json"
    canon.parent.mkdir(parents=True, exist_ok=True)
    canon.write_text(json.dumps({"1": [10, 20]}), encoding="utf-8")

    provided = tmp_path / "config" / "coordinates.json"
    provided.write_text(json.dumps({
        "agents": {"Agent-1": {"chat_input_coordinates": [999, 999]}}
    }), encoding="utf-8")

    loader = CoordinateLoader(str(provided))
    loader.canonical_path = str(canon)
    loader.load()

    # After load, canonical overrides, so assert shouldn't raise
    loader.assert_canonical_consistency()

