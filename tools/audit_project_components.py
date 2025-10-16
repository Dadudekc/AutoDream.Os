#!/usr/bin/env python3
"""
Project Component Audit - Identify Non-Working Components
Tests all major components and quarantines broken ones.
"""

import sys
import importlib
from pathlib import Path

repo_root = Path(__file__).parent.parent
sys.path.insert(0, str(repo_root))


def test_import(module_path: str) -> dict:
    """Test if a module can be imported."""
    try:
        importlib.import_module(module_path)
        return {'status': 'WORKING', 'error': None}
    except ImportError as e:
        return {'status': 'BROKEN', 'error': f'ImportError: {e}'}
    except Exception as e:
        return {'status': 'ERROR', 'error': f'{type(e).__name__}: {e}'}


def main():
    """Audit all major project components."""
    
    print("🔍 PROJECT COMPONENT AUDIT")
    print("=" * 70)
    print()
    
    # Define critical components to test
    components = {
        "Core Systems": [
            "src.core.messaging_core",
            "src.core.messaging_pyautogui",
            "src.core.coordinate_loader",
            "src.core.unified_config",
        ],
        "Services": [
            "src.services.messaging_cli",
            "src.services.soft_onboarding_service",
            "src.services.hard_onboarding_service",
            "src.services.unified_messaging_service",
        ],
        "Repositories": [
            "src.repositories.agent_repository",
            "src.repositories.contract_repository",
            "src.repositories.message_repository",
        ],
        "Utilities": [
            "src.core.utilities",
            "src.utils.file_utils",
            "src.utils.logger_utils",
        ],
        "Tools V2": [
            "tools_v2.core.tool_facade",
            "tools_v2.core.tool_spec",
        ],
        "Discord": [
            "src.discord_commander.unified_discord_bot",
            "src.discord_commander.discord_gui_controller",
        ],
    }
    
    results = {}
    total_tested = 0
    total_working = 0
    total_broken = 0
    
    for category, modules in components.items():
        print(f"📦 {category}")
        print("-" * 70)
        
        category_results = []
        for module in modules:
            total_tested += 1
            result = test_import(module)
            category_results.append({
                'module': module,
                'status': result['status'],
                'error': result['error']
            })
            
            if result['status'] == 'WORKING':
                total_working += 1
                print(f"  ✅ {module}")
            else:
                total_broken += 1
                print(f"  ❌ {module}")
                if result['error']:
                    print(f"     {result['error']}")
        
        results[category] = category_results
        print()
    
    # Summary
    print("=" * 70)
    print("📊 AUDIT SUMMARY")
    print("=" * 70)
    print(f"Total components tested: {total_tested}")
    print(f"Working: {total_working} ({total_working/total_tested*100:.1f}%)")
    print(f"Broken: {total_broken} ({total_broken/total_tested*100:.1f}%)")
    print()
    
    if total_broken > 0:
        print("🚨 COMPONENTS REQUIRING QUARANTINE:")
        print("-" * 70)
        for category, category_results in results.items():
            broken_in_category = [r for r in category_results if r['status'] != 'WORKING']
            if broken_in_category:
                print(f"\n{category}:")
                for item in broken_in_category:
                    print(f"  ❌ {item['module']}")
                    if item['error']:
                        print(f"     → {item['error'][:100]}")
        print()
        return 1
    else:
        print("✅ All components working!")
        return 0

if __name__ == "__main__":
    sys.exit(main())

