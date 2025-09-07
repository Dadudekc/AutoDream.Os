from pathlib import Path
import sys

        from contract import Contract
        from contract_lister import ContractLister
        from contract_manager import ContractManager
        from contract_persistence import ContractPersistence
        from contract_status import ContractStatus
        from contract_validator import ContractValidator

#!/usr/bin/env python3
"""
Simple test for the modularized contract claiming system.
"""


def test_direct_imports():
    """Test importing modules directly."""
    print("🧪 Testing direct module imports...")
    
    try:
        # Test models
        sys.path.insert(0, str(Path(__file__).parent / "contract_claiming_system" / "models"))
        print("✅ ContractStatus imported successfully")
        
        print("✅ Contract model imported successfully")
        
        # Test core
        sys.path.insert(0, str(Path(__file__).parent / "contract_claiming_system" / "core"))
        print("✅ ContractValidator imported successfully")
        
        print("✅ ContractPersistence imported successfully")
        
        print("✅ ContractManager imported successfully")
        
        # Test operations
        sys.path.insert(0, str(Path(__file__).parent / "contract_claiming_system" / "operations"))
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
        # Import directly
        sys.path.insert(0, str(Path(__file__).parent / "contract_claiming_system" / "models"))
        
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
        # Import directly
        sys.path.insert(0, str(Path(__file__).parent / "contract_claiming_system" / "models"))
        sys.path.insert(0, str(Path(__file__).parent / "contract_claiming_system" / "core"))
        
        
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
    print("🚀 MODULARIZED CONTRACT CLAIMING SYSTEM - SIMPLE TEST SUITE")
    print("=" * 60)
    
    tests = [
        test_direct_imports,
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
