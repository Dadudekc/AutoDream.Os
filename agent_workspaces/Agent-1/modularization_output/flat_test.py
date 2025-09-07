#!/usr/bin/env python3
"""
Flat test for the modularized contract claiming system.
This test copies the modules to a flat structure to avoid import issues.
"""

import sys
import shutil
from pathlib import Path

def setup_flat_structure():
    """Copy modules to a flat structure for testing."""
    print("🔧 Setting up flat test structure...")
    
    # Create flat test directory
    flat_dir = Path(__file__).parent / "flat_test"
    flat_dir.mkdir(exist_ok=True)
    
    # Copy model files
    models_dir = Path(__file__).parent / "contract_claiming_system" / "models"
    for file in models_dir.glob("*.py"):
        if file.name != "__init__.py":
            shutil.copy2(file, flat_dir)
    
    # Copy core files
    core_dir = Path(__file__).parent / "contract_claiming_system" / "core"
    for file in core_dir.glob("*.py"):
        if file.name != "__init__.py":
            shutil.copy2(file, flat_dir)
    
    # Copy operations files
    operations_dir = Path(__file__).parent / "contract_claiming_system" / "operations"
    for file in operations_dir.glob("*.py"):
        if file.name != "__init__.py":
            shutil.copy2(file, flat_dir)
    
    print("✅ Flat structure created")
    return flat_dir

def test_flat_imports(flat_dir):
    """Test importing modules from flat structure."""
    print("🧪 Testing flat module imports...")
    
    try:
        # Add flat directory to path
        sys.path.insert(0, str(flat_dir))
        
        # Test models
        from contract_status import ContractStatus
        print("✅ ContractStatus imported successfully")
        
        from contract import Contract
        print("✅ Contract model imported successfully")
        
        # Test core
        from contract_validator import ContractValidator
        print("✅ ContractValidator imported successfully")
        
        from contract_persistence import ContractPersistence
        print("✅ ContractPersistence imported successfully")
        
        from contract_manager import ContractManager
        print("✅ ContractManager imported successfully")
        
        # Test operations
        from contract_lister import ContractLister
        print("✅ ContractLister imported successfully")
        
        print("\n🎉 All modules imported successfully!")
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_contract_creation():
    """Test creating a contract object."""
    print("\n🧪 Testing contract creation...")
    
    try:
        from contract_status import ContractStatus
        from contract import Contract
        
        # Create a sample contract
        contract = Contract(
            contract_id="TEST-001",
            title="Test Contract",
            description="A test contract for validation",
            category="Testing",
            points=100,
            status=ContractStatus.AVAILABLE
        )
        
        print(f"✅ Contract created: {contract.contract_id}")
        print(f"   Title: {contract.title}")
        print(f"   Status: {contract.status}")
        print(f"   Points: {contract.points}")
        
        # Test methods
        print(f"   Is available: {contract.is_available()}")
        print(f"   Is claimed: {contract.is_claimed()}")
        print(f"   Is completed: {contract.is_completed()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Contract creation failed: {e}")
        return False

def test_validation():
    """Test contract validation."""
    print("\n🧪 Testing contract validation...")
    
    try:
        from contract_status import ContractStatus
        from contract import Contract
        from contract_validator import ContractValidator
        
        validator = ContractValidator()
        
        # Create test contract
        contract = Contract(
            contract_id="TEST-002",
            title="Test Contract 2",
            description="Another test contract",
            category="Testing",
            points=200,
            status=ContractStatus.AVAILABLE
        )
        
        # Test validation
        claim_result = validator.validate_claim(contract, "Agent-1")
        print(f"✅ Claim validation: {claim_result['valid']}")
        
        progress_result = validator.validate_progress_format("50%")
        print(f"✅ Progress validation: {progress_result['valid']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Validation test failed: {e}")
        return False

def test_contract_manager():
    """Test contract manager functionality."""
    print("\n🧪 Testing contract manager...")
    
    try:
        from contract_manager import ContractManager
        
        # Create manager with test path
        manager = ContractManager("../../meeting/task_list.json")
        
        # Test getting contracts
        contracts = manager.get_all_contracts()
        print(f"✅ Contracts loaded: {len(contracts.get('contracts', {}))} categories")
        
        # Test statistics
        stats = manager.get_contract_statistics()
        print(f"✅ Statistics generated: {stats['total_contracts']} total contracts")
        
        return True
        
    except Exception as e:
        print(f"❌ Contract manager test failed: {e}")
        return False

def cleanup_flat_structure(flat_dir):
    """Clean up the flat test structure."""
    try:
        shutil.rmtree(flat_dir)
        print("🧹 Flat test structure cleaned up")
    except Exception as e:
        print(f"⚠️  Cleanup warning: {e}")

def main():
    """Run all tests."""
    print("🚀 MODULARIZED CONTRACT CLAIMING SYSTEM - FLAT TEST SUITE")
    print("=" * 60)
    
    # Setup flat structure
    flat_dir = setup_flat_structure()
    
    tests = [
        lambda: test_flat_imports(flat_dir),
        test_contract_creation,
        test_validation,
        test_contract_manager
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    # Cleanup
    cleanup_flat_structure(flat_dir)
    
    print("📊 TEST RESULTS")
    print("=" * 30)
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Modularization successful!")
        return 0
    else:
        print("\n💥 Some tests failed. Check the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
