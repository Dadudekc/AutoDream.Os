#!/usr/bin/env python3
"""
TASK 3J - Model & Enum Consolidation Execution Script

Main execution script for consolidating all scattered model and enum
implementations into the unified framework.

Author: Agent-3 Integration & Testing Specialist
Task: TASK 3J - Model & Enum Consolidation
V2 Standards: ≤400 LOC, SRP, OOP principles
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from core.models.unified_model_framework import UnifiedModelFramework
from core.models.model_consolidation_system import ModelConsolidationSystem
from core.models.model_elimination_system import ModelEliminationSystem


def main():
    """Main execution for TASK 3J"""
    print("🚨 AGENT-3: TASK 3J - MODEL & ENUM CONSOLIDATION 🎯")
    print("=" * 60)
    
    project_root = Path(__file__).parent
    
    try:
        # Step 1: Initialize unified framework
        print("\n📋 Step 1: Initializing Unified Model Framework...")
        framework = UnifiedModelFramework()
        info = framework.get_model_info()
        
        print(f"✅ Framework Version: {info['framework_version']}")
        print(f"✅ Available Models: {', '.join(info['available_models'])}")
        print(f"✅ Total Registered Models: {info['registry_summary']['total_models']}")
        
        # Step 2: Scan for consolidation targets
        print("\n🔍 Step 2: Scanning for Consolidation Targets...")
        consolidation_system = ModelConsolidationSystem(project_root)
        targets = consolidation_system.scan_for_consolidation_targets()
        
        if not targets:
            print("✅ No consolidation targets found - system already consolidated!")
            return 0
        
        print(f"🎯 Found {len(targets)} consolidation targets")
        
        # Display targets by priority
        high_priority = [t for t in targets if t.consolidation_priority == "HIGH"]
        medium_priority = [t for t in targets if t.consolidation_priority == "MEDIUM"]
        low_priority = [t for t in targets if t.consolidation_priority == "LOW"]
        
        print(f"🚨 HIGH Priority: {len(high_priority)} targets")
        print(f"⚠️  MEDIUM Priority: {len(medium_priority)} targets")
        print(f"ℹ️  LOW Priority: {len(low_priority)} targets")
        
        # Step 3: Create consolidation plan
        print("\n📋 Step 3: Creating Consolidation Plan...")
        plan = consolidation_system.create_consolidation_plan(targets)
        
        print(f"📊 Total Files: {plan.total_files}")
        print(f"📊 Total Models: {plan.total_models}")
        print(f"📊 Total Enums: {plan.total_enums}")
        print(f"📊 Estimated Duplication: {plan.estimated_duplication:.1%}")
        
        # Step 4: Execute consolidation
        print("\n🚀 Step 4: Executing Consolidation...")
        success = consolidation_system.execute_consolidation(plan)
        
        if not success:
            print("❌ Consolidation failed!")
            return 1
        
        print("✅ Consolidation completed successfully!")
        
        # Step 5: Execute elimination
        print("\n🗑️  Step 5: Executing Model Elimination...")
        elimination_system = ModelEliminationSystem(project_root)
        elimination_targets = elimination_system.scan_for_elimination_targets()
        
        if elimination_targets:
            elimination_plan = elimination_system.create_elimination_plan(elimination_targets)
            elimination_success = elimination_system.execute_elimination(elimination_plan)
            
            if elimination_success:
                print("✅ Model elimination completed successfully!")
            else:
                print("❌ Model elimination failed!")
        else:
            print("✅ No elimination targets found!")
        
        # Step 6: Final summary
        print("\n🎉 TASK 3J COMPLETE - Model & Enum Consolidation Achieved!")
        print("=" * 60)
        
        # Test the unified framework
        print("\n🧪 Testing Unified Framework...")
        health_model = framework.create_model("health", health_score=95.0)
        task_model = framework.create_model("task", title="TASK 3J Complete", priority="HIGH")
        
        print(f"✅ Health Model Created: {health_model.id}")
        print(f"✅ Task Model Created: {task_model.id}")
        print(f"✅ Health Score: {health_model.health_score}")
        print(f"✅ Task Title: {task_model.title}")
        
        print("\n🚀 UNIFIED MODEL FRAMEWORK READY!")
        print("All scattered model implementations have been consolidated!")
        
        return 0
        
    except Exception as e:
        print(f"❌ TASK 3J failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())

