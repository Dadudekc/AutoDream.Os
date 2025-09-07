import json

from src.utils.stability_improvements import stability_manager, safe_import
from pathlib import Path

import pytest

from services import unified_contract_manager
from services.unified_contract_manager import UnifiedContractManager


class DummyContractManager:
    def __init__(self, *args, **kwargs):
        pass


def setup_dummy(monkeypatch):
    monkeypatch.setattr(unified_contract_manager, "SERVICES_AVAILABLE", True, raising=False)
    monkeypatch.setattr(unified_contract_manager, "ContractManager", DummyContractManager, raising=False)


def test_load_legacy_contracts_creates_directory(tmp_path, monkeypatch):
    setup_dummy(monkeypatch)
    contracts_path = tmp_path / "Agent_Cellphone" / "CONTRACTS"
    manager = UnifiedContractManager(legacy_contracts_path=str(contracts_path))
    manager._load_legacy_contracts()
    assert contracts_path.exists()


def test_load_legacy_contracts_migrates_existing(tmp_path, monkeypatch):
    setup_dummy(monkeypatch)
    contracts_path = tmp_path / "Agent_Cellphone" / "CONTRACTS"
    contracts_path.mkdir(parents=True)
    legacy_file = contracts_path / "legacy.json"
    legacy_file.write_text(json.dumps({"payload": {"task": "x"}}))
    manager = UnifiedContractManager(legacy_contracts_path=str(contracts_path))

    calls = []

    def fake_migrate(data, filename):
        calls.append(filename)
        return "ID"

    monkeypatch.setattr(manager, "_migrate_legacy_contract", fake_migrate)
    manager._load_legacy_contracts()
    assert calls == ["legacy.json"]
