#!/usr/bin/env python3
"""
Migration Script - Onboarding Services Consolidation
===================================================

This script migrates from the old separate onboarding services to the new
consolidated onboarding service.

Author: Agent-1 (Integration & Core Systems Specialist)
Mission: Phase 2 Consolidation - Onboarding Services
"""

import os
import shutil
from pathlib import Path

def migrate_onboarding_services():
    """Migrate from old onboarding services to consolidated service."""
    print("🔄 Starting onboarding services migration...")
    
    # Files to be replaced
    old_files = [
        "src/services/onboarding_service.py",
        "src/services/simple_onboarding.py", 
        "src/services/onboarding_message_generator.py"
    ]
    
    # Create backup directory
    backup_dir = Path("backup/onboarding_services")
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    # Backup old files
    print("📦 Creating backups of old services...")
    for file_path in old_files:
        if os.path.exists(file_path):
            backup_path = backup_dir / Path(file_path).name
            shutil.copy2(file_path, backup_path)
            print(f"  ✅ Backed up {file_path} -> {backup_path}")
    
    # Create stub files that import from consolidated service
    print("🔧 Creating migration stubs...")
    
    # onboarding_service.py stub
    with open("src/services/onboarding_service.py", "w") as f:
        f.write('''#!/usr/bin/env python3
"""
Onboarding Service - MIGRATED TO CONSOLIDATED SERVICE
====================================================

This file has been MIGRATED to the consolidated onboarding service.

NEW LOCATION: src/services/consolidated_onboarding_service.py

This stub file exists only for backward compatibility during the migration period.
All imports should be updated to use: from src.services.consolidated_onboarding_service import ConsolidatedOnboardingService

V2 Compliance: Single Source of Truth (SSOT) Implementation
Migration Status: LEGACY FILE - UPDATE IMPORTS IMMEDIATELY

Author: Agent-1 (Integration & Core Systems Specialist) - Onboarding Consolidation Champion
"""

import warnings
from .consolidated_onboarding_service import ConsolidatedOnboardingService

# Issue deprecation warning
warnings.warn(
    "src.services.onboarding_service is deprecated. "
    "Use src.services.consolidated_onboarding_service instead (Single Source of Truth). "
    "Update your imports: from src.services.consolidated_onboarding_service import ConsolidatedOnboardingService",
    DeprecationWarning,
    stacklevel=2
)

# Legacy content removed - use consolidated_onboarding_service instead
OnboardingService = ConsolidatedOnboardingService
''')
    
    # simple_onboarding.py stub
    with open("src/services/simple_onboarding.py", "w") as f:
        f.write('''#!/usr/bin/env python3
"""
Simple Onboarding - MIGRATED TO CONSOLIDATED SERVICE
===================================================

This file has been MIGRATED to the consolidated onboarding service.

NEW LOCATION: src/services/consolidated_onboarding_service.py

This stub file exists only for backward compatibility during the migration period.
All imports should be updated to use: from src.services.consolidated_onboarding_service import ConsolidatedOnboardingService

V2 Compliance: Single Source of Truth (SSOT) Implementation
Migration Status: LEGACY FILE - UPDATE IMPORTS IMMEDIATELY

Author: Agent-1 (Integration & Core Systems Specialist) - Onboarding Consolidation Champion
"""

import warnings
from .consolidated_onboarding_service import ConsolidatedOnboardingService

# Issue deprecation warning
warnings.warn(
    "src.services.simple_onboarding is deprecated. "
    "Use src.services.consolidated_onboarding_service instead (Single Source of Truth). "
    "Update your imports: from src.services.consolidated_onboarding_service import ConsolidatedOnboardingService",
    DeprecationWarning,
    stacklevel=2
)

# Legacy content removed - use consolidated_onboarding_service instead
SimpleOnboarding = ConsolidatedOnboardingService
''')
    
    # onboarding_message_generator.py stub
    with open("src/services/onboarding_message_generator.py", "w") as f:
        f.write('''#!/usr/bin/env python3
"""
Onboarding Message Generator - MIGRATED TO CONSOLIDATED SERVICE
==============================================================

This file has been MIGRATED to the consolidated onboarding service.

NEW LOCATION: src/services/consolidated_onboarding_service.py

This stub file exists only for backward compatibility during the migration period.
All imports should be updated to use: from src.services.consolidated_onboarding_service import ConsolidatedOnboardingService

V2 Compliance: Single Source of Truth (SSOT) Implementation
Migration Status: LEGACY FILE - UPDATE IMPORTS IMMEDIATELY

Author: Agent-1 (Integration & Core Systems Specialist) - Onboarding Consolidation Champion
"""

import warnings
from .consolidated_onboarding_service import ConsolidatedOnboardingService

# Issue deprecation warning
warnings.warn(
    "src.services.onboarding_message_generator is deprecated. "
    "Use src.services.consolidated_onboarding_service instead (Single Source of Truth). "
    "Update your imports: from src.services.consolidated_onboarding_service import ConsolidatedOnboardingService",
    DeprecationWarning,
    stacklevel=2
)

# Legacy content removed - use consolidated_onboarding_service instead
OnboardingMessageGenerator = ConsolidatedOnboardingService
''')
    
    print("✅ Migration stubs created successfully!")
    print("📋 Next steps:")
    print("  1. Update all imports to use consolidated_onboarding_service")
    print("  2. Test the consolidated service functionality")
    print("  3. Remove stub files after migration is complete")
    print("  4. Update documentation to reference new service")
    
    return True

if __name__ == "__main__":
    migrate_onboarding_services()
