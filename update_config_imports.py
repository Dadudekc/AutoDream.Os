#!/usr/bin/env python3
"""
Configuration Import Update Script
Updates all Python files to use the new organized configuration structure
"""

import os
import re
from pathlib import Path
from typing import List, Tuple

# Configuration file mapping: old path -> new path
CONFIG_FILE_MAPPINGS = {
    # System configurations
    "config/system/performance.json": "config/system/performance.json",
    "config/system/integration.json": "config/system/integration.json",
    "config/system/communication.json": "config/system/communication.json",
    "config/system/endpoints.json": "config/system/endpoints.json",
    
    # Service configurations
    "config/services/financial.yaml": "config/services/financial.yaml",
    "config/services/portal.yaml": "config/services/portal.yaml",
    "config/services/broadcast.yaml": "config/services/broadcast.yaml",
    "config/services/message_queue.json": "config/services/message_queue.json",
    "config/services/unified.yaml": "config/services/unified.yaml",
    
    # Agent configurations
    "config/agents/agent_config.json": "config/agents/agent_config.json",
    "config/agents/coordinates.json": "config/agents/coordinates.json",
    "config/agents/stall_prevention.json": "config/agents/stall_prevention.json",
    "config/agents/stall_prevention_legacy.json": "config/agents/stall_prevention_legacy.json",
    "config/agents/modes.json": "config/agents/modes.json",
    "config/agents/fsm_communication.json": "config/agents/fsm_communication.json",
    
    # Development configurations
    "config/development/pytest.ini": "config/development/pytest.ini",
    "config/development/coverage.ini": "config/development/coverage.ini",
    "config/development/test.yaml": "config/development/test.yaml",
    "config/development/requirements.txt": "config/development/requirements.txt",
    
    # AI/ML configurations
    "config/ai_ml/ai_ml.json": "config/ai_ml/ai_ml.json",
    "config/ai_ml/api_keys.template.json": "config/ai_ml/api_keys.template.json",
    
    # Contract files
    "config/contracts/contract_input.txt": "config/contracts/contract_input.txt"
}

# Import statement patterns to update
IMPORT_PATTERNS = [
    # Direct file imports
    (r'from config\.([^\.]+) import', r'from config.\1 import'),
    (r'import config\.([^\.]+)', r'import config.\1'),
    
    # Specific configuration file references
    (r'config/performance_monitoring_config\.json', r'config/system/performance.json'),
    (r'config/integration_config\.json', r'config/system/integration.json'),
    (r'config/cross_system_communication_config\.json', r'config/system/communication.json'),
    (r'config/system_endpoints\.json', r'config/system/endpoints.json'),
    (r'config/financial_config\.yaml', r'config/services/financial.yaml'),
    (r'config/portal_config\.yaml', r'config/services/portal.yaml'),
    (r'config/improved_broadcast_config\.yaml', r'config/services/broadcast.yaml'),
    (r'config/message_queue_config\.json', r'config/services/message_queue.json'),
    (r'config/unified_config\.yaml', r'config/services/unified.yaml'),
    (r'config/8_agent_config\.json', r'config/agents/agent_config.json'),
    (r'config/cursor_agent_coords\.json', r'config/agents/coordinates.json'),
    (r'config/captain_stall_prevention_config\.json', r'config/agents/stall_prevention.json'),
    (r'config/stall_prevention_config\.json', r'config/agents/stall_prevention_legacy.json'),
    (r'config/modes_runtime\.json', r'config/agents/modes.json'),
    (r'config/fsm_communication_config\.json', r'config/agents/fsm_communication.json'),
    (r'config/pytest\.ini', r'config/development/pytest.ini'),
    (r'config/\.coveragerc', r'config/development/coverage.ini'),
    (r'config/test_config\.yaml', r'config/development/test.yaml'),
    (r'config/requirements_basic\.txt', r'config/development/requirements.txt'),
    (r'config/ai_ml/ai_ml_config\.json', r'config/ai_ml/ai_ml.json'),
    (r'config/ai_ml/api_keys\.template\.json', r'config/ai_ml/api_keys.template.json'),
    (r'config/contract_input\.txt', r'config/contracts/contract_input.txt'),
    
    # Configuration key references (for 8_agent_config)
    (r'"agent_config"', r'"agent_config"'),
    (r"'agent_config'", r"'agent_config'"),
]

def find_python_files(directory: str = ".") -> List[Path]:
    """Find all Python files in the directory"""
    python_files = []
    for root, dirs, files in os.walk(directory):
        # Skip config directory itself and other non-source directories
        if any(skip in root for skip in ['config/', '__pycache__/', '.git/', 'node_modules/']):
            continue
            
        for file in files:
            if file.endswith('.py'):
                python_files.append(Path(root) / file)
    
    return python_files

def update_file_imports(file_path: Path) -> Tuple[bool, List[str]]:
    """Update imports in a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes_made = []
        
        # Apply all import pattern updates
        for old_pattern, new_pattern in IMPORT_PATTERNS:
            if re.search(old_pattern, content):
                content = re.sub(old_pattern, new_pattern, content)
                changes_made.append(f"Updated pattern: {old_pattern} -> {new_pattern}")
        
        # Apply configuration file path updates
        for old_path, new_path in CONFIG_FILE_MAPPINGS.items():
            if old_path in content:
                content = content.replace(old_path, new_path)
                changes_made.append(f"Updated path: {old_path} -> {new_path}")
        
        # Write back if changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, changes_made
        
        return False, []
        
    except Exception as e:
        return False, [f"Error processing {file_path}: {e}"]

def update_configuration_loader_imports():
    """Update imports to use the new configuration loader"""
    print("\n🔧 Updating Configuration Loader Imports...")
    
    # Find files that might need the new config loader
    loader_patterns = [
        (r'from config\.config_loader import', r'from config.config_loader import'),
        (r'import config\.config_loader', r'import config.config_loader'),
    ]
    
    python_files = find_python_files()
    updated_files = []
    
    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            for old_pattern, new_pattern in loader_patterns:
                if re.search(old_pattern, content):
                    content = re.sub(old_pattern, new_pattern, content)
            
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                updated_files.append(str(file_path))
                
        except Exception as e:
            print(f"⚠️  Error updating {file_path}: {e}")
    
    if updated_files:
        print(f"✅ Updated configuration loader imports in {len(updated_files)} files")
        for file_path in updated_files:
            print(f"   - {file_path}")
    else:
        print("ℹ️  No configuration loader imports found to update")

def main():
    """Main update function"""
    print("🚀 Configuration Import Update Script")
    print("=" * 60)
    
    # Step 1: Update configuration file paths
    print("\n📁 Step 1: Updating Configuration File Paths...")
    python_files = find_python_files()
    
    total_files = len(python_files)
    updated_files = 0
    total_changes = 0
    
    print(f"Found {total_files} Python files to process...")
    
    for file_path in python_files:
        try:
            was_updated, changes = update_file_imports(file_path)
            if was_updated:
                updated_files += 1
                total_changes += len(changes)
                print(f"✅ Updated: {file_path}")
                for change in changes:
                    print(f"   - {change}")
        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}")
    
    # Step 2: Update configuration loader imports
    update_configuration_loader_imports()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 UPDATE SUMMARY")
    print("=" * 60)
    print(f"Total Python files processed: {total_files}")
    print(f"Files updated: {updated_files}")
    print(f"Total changes made: {total_changes}")
    
    if updated_files > 0:
        print(f"\n✅ Successfully updated {updated_files} files with {total_changes} changes")
        print("\n📋 Next Steps:")
        print("1. Test the updated imports work correctly")
        print("2. Run your test suite to verify functionality")
        print("3. Check for any remaining import issues")
    else:
        print("\nℹ️  No files needed updating - configuration imports already correct")
    
    print("\n🎯 Configuration import updates complete!")
    return updated_files > 0

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
