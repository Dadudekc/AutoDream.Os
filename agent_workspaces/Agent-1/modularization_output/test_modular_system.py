from pathlib import Path
import sys

        from contract_claiming_system.core.contract_manager import ContractManager
        from contract_claiming_system.core.contract_persistence import ContractPersistence
        from contract_claiming_system.core.contract_validator import ContractValidator
        from contract_claiming_system.models.contract import Contract
        from contract_claiming_system.models.contract_status import ContractStatus
        from contract_claiming_system.operations.contract_lister import ContractLister

#!/usr/bin/env python3
"""
Test script for the modularized contract claiming system.
"""


# Add the modularization output directory to the path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test that all modules can be imported correctly."""
    print("🧪 Testing module imports...")
    
    try:
        print("✅ ContractStatus imported successfully")
        
        print("✅ Contract model imported successfully")
        
        print("✅ ContractValidator imported successfully")
        
        print("✅ ContractPersistence imported successfully")
        
        print("✅ ContractManager imported successfully")
        
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

def main():
    """Run all tests."""
    print("🚀 MODULARIZED CONTRACT CLAIMING SYSTEM - TEST SUITE")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_contract_creation,
        test_validation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
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
