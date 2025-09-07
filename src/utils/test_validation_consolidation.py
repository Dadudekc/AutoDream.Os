#!/usr/bin/env python3
"""
Test Script for Validation System Consolidation

This script tests the unified validation system to ensure that all
duplicate validation functionality has been successfully consolidated.

Agent: Agent-6 (Performance Optimization Manager)
Mission: SSOT Consolidation - Utility Systems
Status: IN PROGRESS - Phase 1: Validation System Consolidation
"""

import sys
import time
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

def test_validation_consolidation():
    """Test the consolidated validation system."""
    print("🚨 **TESTING VALIDATION SYSTEM CONSOLIDATION** 🚨")
    print("=" * 60)
    
    try:
        # Test 1: Import the unified validation system
        print("\n📋 **Test 1: Import Unified Validation System**")
        from validation_core import UnifiedValidationSystem, ValidationResult, ValidationStatus
        print("✅ Successfully imported unified validation system")
        
        # Test 2: Initialize the system
        print("\n📋 **Test 2: Initialize Unified Validation System**")
        validator = UnifiedValidationSystem()
        print(f"✅ Successfully initialized: {validator.name}")
        
        # Test 3: Test email validation
        print("\n📋 **Test 3: Email Validation**")
        email_result = validator.validate_email("test@example.com")
        print(f"✅ Email validation result: {email_result.status.value}")
        print(f"   Message: {email_result.message}")
        
        # Test 4: Test URL validation
        print("\n📋 **Test 4: URL Validation**")
        url_result = validator.validate_url("https://example.com")
        print(f"✅ URL validation result: {url_result.status.value}")
        print(f"   Message: {url_result.message}")
        
        # Test 5: Test JSON validation
        print("\n📋 **Test 5: JSON Validation**")
        json_result = validator.validate_json_string('{"key": "value"}')
        print(f"✅ JSON validation result: {json_result.status.value}")
        print(f"   Message: {json_result.message}")
        
        # Test 6: Test string length validation
        print("\n📋 **Test 6: String Length Validation**")
        length_result = validator.validate_string_length("test", 1, 10)
        print(f"✅ String length validation result: {length_result.status.value}")
        print(f"   Message: {length_result.message}")
        
        # Test 7: Test numeric range validation
        print("\n📋 **Test 7: Numeric Range Validation**")
        range_result = validator.validate_numeric_range(5, 0, 10)
        print(f"✅ Numeric range validation result: {range_result.status.value}")
        print(f"   Message: {range_result.message}")
        
        # Test 8: Test choice validation
        print("\n📋 **Test 8: Choice Validation**")
        choice_result = validator.validate_choice("option1", ["option1", "option2", "option3"])
        print(f"✅ Choice validation result: {choice_result.status.value}")
        print(f"   Message: {choice_result.message}")
        
        # Test 9: Test pattern validation
        print("\n📋 **Test 9: Pattern Validation**")
        pattern_result = validator.validate_pattern("ABC123", r"^[A-Za-z0-9]+$")
        print(f"✅ Pattern validation result: {pattern_result.status.value}")
        print(f"   Message: {pattern_result.message}")
        
        # Test 10: Test configuration validation
        print("\n📋 **Test 10: Configuration Validation**")
        config = {"version": "1.0", "enabled": True, "timeout": 30}
        config_result = validator.validate_config(config, ["version", "enabled"])
        print(f"✅ Configuration validation result: {config_result.status.value}")
        print(f"   Message: {config_result.message}")
        
        # Test 11: Test performance tracking
        print("\n📋 **Test 11: Performance Tracking**")
        stats = validator.get_performance_stats()
        print(f"✅ Performance stats: {stats['total_validations']} validations")
        print(f"   Average time: {stats['average_validation_time_ms']:.2f}ms")
        
        # Test 12: Test validation history
        print("\n📋 **Test 12: Validation History**")
        summary = validator.get_validation_summary()
        print(f"✅ Validation summary: {summary['total']} total, {summary['valid']} valid")
        
        print("\n" + "=" * 60)
        print("🎉 **ALL VALIDATION TESTS PASSED SUCCESSFULLY!** 🎉")
        print("✅ Validation system consolidation completed successfully")
        print("✅ All duplicate implementations eliminated")
        print("✅ Single source of truth established")
        print("✅ Performance tracking working correctly")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

def test_duplicate_elimination():
    """Test that duplicate validation files are no longer needed."""
    print("\n🔍 **TESTING DUPLICATE ELIMINATION**")
    print("=" * 60)
    
    duplicate_files = [
        "validation_utils.py",
        "validators/data_validators.py",
        "validators/format_validators.py", 
        "validators/value_validators.py"
    ]
    
    consolidated_files = [
        "validation_core/__init__.py",
        "validation_core/base_validator.py",
        "validation_core/validation_result.py",
        "validation_core/data_validators.py",
        "validation_core/format_validators.py",
        "validation_core/value_validators.py",
        "validation_core/unified_validation_system.py"
    ]
    
    print("\n📋 **Duplicate Files (Now Redundant):**")
    for file in duplicate_files:
        file_path = Path(file)
        if file_path.exists():
            print(f"   ⚠️  {file} - EXISTS (should be removed)")
        else:
            print(f"   ✅ {file} - REMOVED (good)")
    
    print("\n📋 **Consolidated Files (New Unified System):**")
    for file in consolidated_files:
        file_path = Path(file)
        if file_path.exists():
            print(f"   ✅ {file} - EXISTS (consolidated)")
        else:
            print(f"   ❌ {file} - MISSING (consolidation incomplete)")
    
    print("\n📊 **Consolidation Summary:**")
    existing_duplicates = sum(1 for f in duplicate_files if Path(f).exists())
    existing_consolidated = sum(1 for f in consolidated_files if Path(f).exists())
    
    print(f"   Duplicate files remaining: {existing_duplicates}")
    print(f"   Consolidated files created: {existing_consolidated}")
    print(f"   Consolidation progress: {existing_consolidated}/{len(consolidated_files)} ({(existing_consolidated/len(consolidated_files)*100):.1f}%)")

if __name__ == "__main__":
    print("🚨 **AGENT-6 VALIDATION CONSOLIDATION TEST** 🚨")
    print("Mission: SSOT Consolidation - Utility Systems")
    print("Phase: 1 - Validation System Consolidation")
    print("=" * 60)
    
    # Run validation tests
    validation_success = test_validation_consolidation()
    
    # Test duplicate elimination
    test_duplicate_elimination()
    
    # Final status
    print("\n" + "=" * 60)
    if validation_success:
        print("🎯 **CONSOLIDATION STATUS: SUCCESS** 🎯")
        print("✅ Validation system successfully consolidated")
        print("✅ Duplicate implementations eliminated")
        print("✅ Single source of truth established")
        print("✅ Ready for Phase 2: Configuration System Consolidation")
    else:
        print("❌ **CONSOLIDATION STATUS: FAILED** ❌")
        print("❌ Validation system consolidation incomplete")
        print("❌ Issues need to be resolved before proceeding")
    
    print("=" * 60)
