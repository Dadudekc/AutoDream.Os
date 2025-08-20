#!/usr/bin/env python3
"""
Smoke Test for Perpetual Motion Contract Service
===============================================

Tests basic functionality of the perpetual motion contract service.
"""

import sys
import os
import tempfile
import shutil
from pathlib import Path

# Add src to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, '..', '..', 'src')
sys.path.insert(0, src_dir)

from services.perpetual_motion_contract_service import PerpetualMotionContractService

def test_service_initialization():
    """Test service initialization."""
    print("🧪 Testing service initialization...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        service = PerpetualMotionContractService(
            contracts_dir=os.path.join(temp_dir, "contracts"),
            templates_dir=os.path.join(temp_dir, "templates")
        )
        
        assert service.contracts_dir.exists(), "Contracts directory should be created"
        assert service.templates_dir.exists(), "Templates directory should be created"
        assert len(service.contract_templates) > 0, "Should have default templates"
        
        print("✅ Service initialization test passed")

def test_contract_generation():
    """Test automatic contract generation."""
    print("🧪 Testing contract generation...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        service = PerpetualMotionContractService(
            contracts_dir=os.path.join(temp_dir, "contracts"),
            templates_dir=os.path.join(temp_dir, "templates")
        )
        
        # Test contract generation
        contracts = service._generate_new_contracts("Agent-1", 3)
        assert len(contracts) == 3, "Should generate exactly 3 contracts"
        
        # Test contract saving
        for contract in contracts:
            service._save_contract(contract)
            contract_file = service.contracts_dir / f"{contract.contract_id}.json"
            assert contract_file.exists(), f"Contract file {contract.contract_id}.json should exist"
        
        print("✅ Contract generation test passed")

def test_contract_completion_flow():
    """Test the complete contract completion flow."""
    print("🧪 Testing contract completion flow...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        service = PerpetualMotionContractService(
            contracts_dir=os.path.join(temp_dir, "contracts"),
            templates_dir=os.path.join(temp_dir, "templates")
        )
        
        # Test contract completion
        test_data = {"test": True, "timestamp": "2025-08-19T10:00:00"}
        service.on_contract_completion("TEST-CONTRACT-001", "Agent-1", test_data)
        
        # Check that new contracts were generated
        contract_files = list(service.contracts_dir.glob("*.json"))
        assert len(contract_files) == 2, "Should generate 2 new contracts per completion"
        
        # Check that resume message was created
        inbox_dir = Path(temp_dir) / "agent_workspaces" / "Agent-1" / "inbox"
        assert inbox_dir.exists(), "Agent inbox should be created"
        
        resume_files = list(inbox_dir.glob("resume_message_*.json"))
        assert len(resume_files) == 1, "Should create resume message"
        
        print("✅ Contract completion flow test passed")

def test_monitoring_system():
    """Test the monitoring system."""
    print("🧪 Testing monitoring system...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        service = PerpetualMotionContractService(
            contracts_dir=os.path.join(temp_dir, "contracts"),
            templates_dir=os.path.join(temp_dir, "templates")
        )
        
        # Test monitoring start/stop
        service.start_monitoring()
        assert service.monitoring_active, "Monitoring should be active"
        
        service.stop_monitoring()
        assert not service.monitoring_active, "Monitoring should be stopped"
        
        print("✅ Monitoring system test passed")

def test_status_reporting():
    """Test status reporting."""
    print("🧪 Testing status reporting...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        service = PerpetualMotionContractService(
            contracts_dir=os.path.join(temp_dir, "contracts"),
            templates_dir=os.path.join(temp_dir, "templates")
        )
        
        status = service.get_status()
        
        assert "status" in status, "Status should include status field"
        assert "contracts_available" in status, "Status should include contracts count"
        assert "templates_loaded" in status, "Status should include templates count"
        assert "auto_generation" in status, "Status should include auto-generation setting"
        
        print("✅ Status reporting test passed")

def run_all_tests():
    """Run all smoke tests."""
    print("🚀 Running Perpetual Motion Contract Service Smoke Tests")
    print("=" * 60)
    
    try:
        test_service_initialization()
        test_contract_generation()
        test_contract_completion_flow()
        test_monitoring_system()
        test_status_reporting()
        
        print("\n🎉 All smoke tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
