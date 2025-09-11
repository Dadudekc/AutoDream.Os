#!/usr/bin/env python3
"""
Migration Script - Consolidated Services
=======================================

This script migrates from the old separate services to the new consolidated services.

Author: Agent-1 (Integration & Core Systems Specialist)
Mission: Phase 2 Consolidation - Chunk 002 (Services)
"""

import os
import shutil
from pathlib import Path

def migrate_consolidated_services():
    """Migrate from old services to consolidated services."""
    print("🔄 Starting consolidated services migration...")
    
    # Create backup directory
    backup_dir = Path("backup/consolidated_services")
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    # Files to be replaced with stubs
    old_files = [
        # Messaging services
        "src/services/messaging_core.py",
        "src/services/messaging_cli.py", 
        "src/services/messaging_pyautogui.py",
        
        # Onboarding services (already handled)
        "src/services/onboarding_service.py",
        "src/services/simple_onboarding.py",
        "src/services/onboarding_message_generator.py",
        
        # Vector services
        "src/services/vector_database/vector_database_orchestrator.py",
        "src/services/agent_vector_integration.py",
        "src/services/embedding_service.py",
        
        # Coordination services
        "src/services/coordination/strategy_coordinator.py",
        "src/services/handlers/command_handler.py",
        "src/services/coordinator.py",
        
        # Utility services
        "src/services/utils/agent_utils_registry.py",
        "src/services/performance_analyzer.py",
        "src/services/compliance_validator.py"
    ]
    
    # Create migration stubs
    for old_file in old_files:
        if os.path.exists(old_file):
            # Backup original
            backup_path = backup_dir / Path(old_file).name
            shutil.copy2(old_file, backup_path)
            print(f"✅ Backed up {old_file} to {backup_path}")
            
            # Create stub
            create_migration_stub(old_file)
            print(f"✅ Created migration stub for {old_file}")
    
    print("🎉 Consolidated services migration completed!")
    print(f"📁 Backups saved to: {backup_dir}")

def create_migration_stub(file_path: str):
    """Create a migration stub for the old service."""
    stub_content = f'''#!/usr/bin/env python3
"""
MIGRATION NOTICE: SERVICE CONSOLIDATION
======================================

This file has been MIGRATED to the consolidated services system.

NEW LOCATION: See consolidated services below

V2 Compliance: Single Source of Truth (SSOT) Implementation
Migration Status: LEGACY FILE - UPDATE IMPORTS IMMEDIATELY

Author: Agent-1 (Integration & Core Systems Specialist)
Mission: Phase 2 Consolidation - Chunk 002 (Services)
"""

import warnings

# Import from consolidated services
try:
    if "messaging" in "{file_path}":
        from .consolidated_messaging_service import ConsolidatedMessagingService
        warnings.warn(
            "This service has been consolidated. Use ConsolidatedMessagingService instead.",
            DeprecationWarning,
            stacklevel=2
        )
    elif "onboarding" in "{file_path}":
        from .consolidated_onboarding_service import ConsolidatedOnboardingService
        warnings.warn(
            "This service has been consolidated. Use ConsolidatedOnboardingService instead.",
            DeprecationWarning,
            stacklevel=2
        )
    elif "vector" in "{file_path}":
        from .consolidated_vector_service import ConsolidatedVectorService
        warnings.warn(
            "This service has been consolidated. Use ConsolidatedVectorService instead.",
            DeprecationWarning,
            stacklevel=2
        )
    elif "coordination" in "{file_path}" or "command_handler" in "{file_path}" or "coordinator" in "{file_path}":
        from .consolidated_coordination_service import ConsolidatedCoordinationService
        warnings.warn(
            "This service has been consolidated. Use ConsolidatedCoordinationService instead.",
            DeprecationWarning,
            stacklevel=2
        )
    elif "utility" in "{file_path}" or "performance" in "{file_path}" or "compliance" in "{file_path}":
        from .consolidated_utility_service import ConsolidatedUtilityService
        warnings.warn(
            "This service has been consolidated. Use ConsolidatedUtilityService instead.",
            DeprecationWarning,
            stacklevel=2
        )
except ImportError as e:
    warnings.warn(f"Consolidated service not available: {{e}}", ImportWarning)

# Legacy content removed - use consolidated services instead
'''
    
    with open(file_path, 'w') as f:
        f.write(stub_content)

if __name__ == "__main__":
    migrate_consolidated_services()
