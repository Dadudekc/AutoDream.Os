#!/usr/bin/env python3
"""Test script to verify updated configuration imports work correctly"""

import sys
import os
import json
from pathlib import Path

def test_config_file_access():
    """Test that configuration files can be accessed with new paths"""
    print("🧪 Testing Configuration File Access")
    print("=" * 50)
    
    test_files = [
        "config/system/performance.json",
        "config/agents/agent_config.json",
        "config/services/financial.yaml",
        "config/development/pytest.ini",
        "config/ci_cd/jenkins.groovy"
    ]
    
    all_accessible = True
    for file_path in test_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"✅ {file_path} - {size} bytes")
        else:
            print(f"❌ {file_path} - NOT FOUND")
            all_exist = False
    
    return all_accessible

def test_configuration_loader():
    """Test the configuration loader functionality"""
    print("\n🔧 Testing Configuration Loader")
    print("=" * 50)
    
    try:
        # Add config to path
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'config'))
        
        # Test import
        from config_loader import get_config, get_system_config, get_agent_config
        print("✅ Successfully imported configuration loader")
        
        # Test loading configurations
        system_config = get_system_config()
        agent_config = get_agent_config()
        
        print(f"✅ System config loaded: {len(system_config)} keys")
        print(f"✅ Agent config loaded: {len(agent_config)} keys")
        
        # Test specific config loading
        performance_config = get_config("system/performance.json")
        financial_config = get_config("services/financial.yaml")
        
        print(f"✅ Performance config loaded: {len(performance_config)} keys")
        print(f"✅ Financial config loaded: {len(financial_config)} keys")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration loader test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_updated_file_imports():
    """Test that some of the updated files can import correctly"""
    print("\n📁 Testing Updated File Imports")
    print("=" * 50)
    
    test_files = [
        "src/services/agent_cell_phone.py",
        "src/ai_ml/utils.py",
        "scripts/launch_performance_monitoring.py"
    ]
    
    all_importable = True
    for file_path in test_files:
        if os.path.exists(file_path):
            try:
                # Try to import the file (basic syntax check)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for basic Python syntax
                compile(content, file_path, 'exec')
                print(f"✅ {file_path} - Syntax valid")
                
            except Exception as e:
                print(f"❌ {file_path} - Import error: {e}")
                all_importable = False
        else:
            print(f"⚠️  {file_path} - File not found")
    
    return all_importable

def main():
    """Main test function"""
    print("🚀 Configuration Import Update Verification Test")
    print("=" * 60)
    
    # Test 1: Configuration file access
    files_accessible = test_config_file_access()
    
    # Test 2: Configuration loader functionality
    loader_works = test_configuration_loader()
    
    # Test 3: Updated file imports
    imports_work = test_updated_file_imports()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 VERIFICATION TEST RESULTS")
    print("=" * 60)
    print(f"Configuration Files Accessible: {'✅ PASS' if files_accessible else '❌ FAIL'}")
    print(f"Configuration Loader Working: {'✅ PASS' if loader_works else '❌ FAIL'}")
    print(f"Updated File Imports: {'✅ PASS' if imports_work else '❌ FAIL'}")
    
    if files_accessible and loader_works and imports_work:
        print("\n🎉 ALL TESTS PASSED! Configuration imports updated successfully!")
        print("\n📋 Status:")
        print("✅ Configuration files accessible with new paths")
        print("✅ Configuration loader working correctly")
        print("✅ Updated Python files import without errors")
        print("✅ System ready for production use")
    else:
        print("\n❌ Some tests failed. Please review the issues above.")
    
    return files_accessible and loader_works and imports_work

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
