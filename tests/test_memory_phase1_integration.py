"""
Memory Leak Upgrade Phase 1 - Integration Test
==============================================

Verification test for memory policy framework integration.

Author: Agent-5 (Coordinator)
License: MIT
"""

import json
import tempfile
from pathlib import Path

import pytest
import yaml


def test_memory_policy_yaml_valid():
    """Test memory policy YAML is valid and loadable"""
    config_path = Path("config/memory_policy.yaml")
    
    assert config_path.exists(), "Memory policy YAML not found"
    
    with open(config_path) as f:
        config = yaml.safe_load(f)
    
    assert config is not None, "Failed to load YAML"
    assert "memory_budgets" in config
    assert "leak_detection" in config
    assert "monitoring" in config
    assert "alerts" in config
    assert "ledger" in config


def test_memory_policy_budgets():
    """Test memory budgets are properly configured"""
    with open("config/memory_policy.yaml") as f:
        config = yaml.safe_load(f)
    
    budgets = config["memory_budgets"]
    
    # Global budget
    assert "global" in budgets
    assert budgets["global"]["max_memory_mb"] == 512
    assert budgets["global"]["warning_threshold_percent"] == 80
    assert budgets["global"]["critical_threshold_percent"] == 95
    
    # Service budgets
    assert "services" in budgets
    services = budgets["services"]
    
    assert "messaging" in services
    assert services["messaging"]["max_memory_mb"] == 100
    
    assert "autonomous_workflow" in services
    assert "vector_database" in services
    assert "agent_workspace" in services


def test_memory_policy_loader():
    """Test MemoryPolicyLoader functionality"""
    from src.observability.memory import MemoryPolicyLoader
    
    loader = MemoryPolicyLoader("config/memory_policy.yaml")
    config = loader.load()
    
    assert config is not None
    assert "memory_budgets" in config
    
    # Test get_budget
    budget = loader.get_budget("messaging")
    assert budget.max_memory_mb == 100
    assert budget.warning_threshold_percent == 75
    assert budget.warning_mb == 75  # 100 * 0.75


def test_tracemalloc_integration():
    """Test tracemalloc integration"""
    from src.observability.memory import TracemallocIntegration
    
    tracer = TracemallocIntegration(trace_limit=10)
    
    # Start tracing
    assert tracer.start() is True
    assert tracer.is_tracing is True
    
    # Take snapshot
    snapshot = tracer.take_snapshot()
    assert snapshot is not None
    assert snapshot.current_mb >= 0
    assert snapshot.peak_mb >= 0
    assert snapshot.object_count > 0
    
    # Stop tracing
    assert tracer.stop() is True
    assert tracer.is_tracing is False


def test_memory_leak_detector():
    """Test memory leak detector"""
    from src.observability.memory import ComprehensiveLeakDetector, MemorySnapshot
    
    config = {
        'leak_detection': {
            'snapshot_retention_count': 10,
            'thresholds': {
                'memory_growth_mb': 10,
                'memory_growth_percent': 20,
                'object_count_growth': 1000
            },
            'auto_cleanup': {
                'enabled': True,
                'threshold_mb': 50,
                'methods': ['garbage_collection']
            }
        }
    }
    
    detector = ComprehensiveLeakDetector(config)
    
    # Add snapshots
    snapshot1 = MemorySnapshot(
        timestamp=100.0,
        current_mb=50.0,
        peak_mb=55.0,
        object_count=1000
    )
    
    snapshot2 = MemorySnapshot(
        timestamp=200.0,
        current_mb=55.0,
        peak_mb=60.0,
        object_count=1100
    )
    
    detector.add_snapshot(snapshot1)
    detector.add_snapshot(snapshot2)
    
    # Run detection
    results = detector.run_full_detection()
    
    assert 'leak_detection' in results
    assert 'trend_analysis' in results
    assert 'object_leaks' in results


def test_memory_ledger_persistence():
    """Test memory ledger persistence"""
    from src.observability.memory import LedgerEntry, MemoryLedger
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_path = f.name
    
    try:
        ledger = MemoryLedger(storage_path=temp_path, max_entries=100)
        
        # Add entries
        entry1 = ledger.record("test_service", 100.0, 5000)
        entry2 = ledger.record("test_service", 110.0, 5500)
        
        assert len(ledger.entries) == 2
        
        # Save ledger
        assert ledger.save() is True
        assert Path(temp_path).exists()
        
        # Load ledger
        new_ledger = MemoryLedger(storage_path=temp_path)
        assert new_ledger.load() is True
        assert len(new_ledger.entries) == 2
        
    finally:
        Path(temp_path).unlink(missing_ok=True)


def test_memory_policy_manager():
    """Test memory policy manager end-to-end"""
    from src.observability.memory import MemoryPolicyManager
    
    manager = MemoryPolicyManager("config/memory_policy.yaml")
    
    # Initialize
    assert manager.initialize() is True
    assert manager.initialized is True
    assert manager.tracer is not None
    assert manager.enforcer is not None
    
    # Take snapshot
    snapshot = manager.get_snapshot()
    assert snapshot is not None
    assert snapshot.current_mb >= 0
    
    # Check service
    result = manager.check_service("messaging", 50.0)
    assert 'service' in result
    assert result['service'] == 'messaging'
    assert 'status' in result
    
    # Shutdown
    assert manager.shutdown() is True


def test_a2a_messaging_integration():
    """Test A2A messaging integration configuration"""
    with open("config/memory_policy.yaml") as f:
        config = yaml.safe_load(f)
    
    alerts = config["alerts"]
    
    # Check messaging channel configured
    assert "messaging" in alerts["channels"]
    
    # Check recipients
    assert "recipients" in alerts
    recipients = alerts["recipients"]
    
    assert "Agent-5" in recipients["warning"]
    assert "Agent-4" in recipients["critical"]
    assert "Agent-8" in recipients["emergency"]


def test_ssot_consistency():
    """Test SSOT consistency across configuration"""
    with open("config/memory_policy.yaml") as f:
        config = yaml.safe_load(f)
    
    # Verify no hardcoded values conflict with policy
    budgets = config["memory_budgets"]["services"]
    
    # All service budgets should be defined
    for service in ["messaging", "autonomous_workflow", "vector_database", "agent_workspace"]:
        assert service in budgets
        assert "max_memory_mb" in budgets[service]
        assert "warning_threshold_percent" in budgets[service]
        assert "critical_threshold_percent" in budgets[service]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

