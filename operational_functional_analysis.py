#!/usr/bin/env python3
"""
Agent-8 Functional Analysis for SWARM Survey
===========================================

Phase 2: Functional Analysis - Services, capabilities, relationships
Operational perspective on system interdependencies and service interactions
"""

import os
from pathlib import Path
import json

def analyze_functional_relationships():
    """Analyze functional relationships and service interdependencies"""

    print('🔍 AGENT-8 FUNCTIONAL ANALYSIS')
    print('=============================')
    print()

    src_path = Path('src')
    if not src_path.exists():
        print('❌ src/ directory not found')
        return

    # 1. Service Layer Analysis
    print('🔧 SERVICE LAYER ANALYSIS:')
    print('-' * 25)

    services_path = src_path / 'services'
    if services_path.exists():
        service_files = list(services_path.glob('*.py'))
        print(f'Service files found: {len(service_files)}')

        # Analyze service types
        service_types = {
            'messaging': [],
            'coordination': [],
            'onboarding': [],
            'core': [],
            'other': []
        }

        for service_file in service_files:
            filename = service_file.name.lower()
            if 'messaging' in filename:
                service_types['messaging'].append(service_file.name)
            elif 'coordinat' in filename:
                service_types['coordination'].append(service_file.name)
            elif 'onboard' in filename:
                service_types['onboarding'].append(service_file.name)
            elif 'core' in filename:
                service_types['core'].append(service_file.name)
            else:
                service_types['other'].append(service_file.name)

        for category, files in service_types.items():
            if files:
                print(f'{category.title()}: {len(files)} files')
                for f in files[:3]:  # Show first 3
                    print(f'  - {f}')
                if len(files) > 3:
                    print(f'  ... and {len(files) - 3} more')

    # 2. Core System Analysis
    print('\n🏛️  CORE SYSTEM ANALYSIS:')
    print('-' * 24)

    core_path = src_path / 'core'
    if core_path.exists():
        core_subdirs = [d for d in core_path.iterdir() if d.is_dir()]
        print(f'Core subsystems: {len(core_subdirs)}')

        for subdir in core_subdirs:
            py_files = list(subdir.glob('*.py'))
            print(f'{subdir.name}: {len(py_files)} files')

    # 3. Interdependency Analysis
    print('\n🔗 INTERDEPENDENCY ANALYSIS:')
    print('-' * 27)

    # Analyze import relationships
    import_patterns = {
        'core_to_services': 0,
        'services_to_core': 0,
        'cross_service': 0,
        'external_dependencies': 0
    }

    for py_file in src_path.rglob('*.py'):
        try:
            with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

                # Count different import patterns
                if 'from ..core' in content or 'from core' in content:
                    if 'services' in str(py_file):
                        import_patterns['services_to_core'] += 1
                    else:
                        import_patterns['core_to_services'] += 1

                if 'from ..services' in content or 'from services' in content:
                    import_patterns['cross_service'] += 1

                if any(pkg in content for pkg in ['import requests', 'import pyautogui', 'import yaml']):
                    import_patterns['external_dependencies'] += 1

        except Exception as e:
            continue

    print('Import relationship patterns:')
    for pattern, count in import_patterns.items():
        print(f'{pattern}: {count} files')

    # 4. Operational Capability Assessment
    print('\n⚙️  OPERATIONAL CAPABILITY ASSESSMENT:')
    print('-' * 37)

    capabilities = {
        'monitoring': [],
        'logging': [],
        'error_handling': [],
        'configuration': [],
        'coordination': [],
        'messaging': []
    }

    capability_keywords = {
        'monitoring': ['monitor', 'health', 'status', 'metrics'],
        'logging': ['log', 'logger', 'debug', 'info'],
        'error_handling': ['error', 'exception', 'try', 'catch'],
        'configuration': ['config', 'settings', 'env'],
        'coordination': ['coordinat', 'orchestrat', 'workflow'],
        'messaging': ['message', 'send', 'receive', 'comms']
    }

    for py_file in src_path.rglob('*.py'):
        try:
            with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read().lower()

                for cap, keywords in capability_keywords.items():
                    if any(keyword in content for keyword in keywords):
                        capabilities[cap].append(py_file.name)
        except Exception:
            continue

    print('System capabilities detected:')
    for cap, files in capabilities.items():
        unique_files = len(set(files))
        print(f'{cap.title()}: {unique_files} files')

    # 5. Consolidation Opportunity Analysis
    print('\n🎯 CONSOLIDATION OPPORTUNITY ANALYSIS:')
    print('-' * 38)

    consolidation_opportunities = {
        'duplicate_services': [],
        'overlapping_functionality': [],
        'thin_abstractions': [],
        'unused_capabilities': []
    }

    # Analyze for potential consolidation
    service_names = [f.stem for f in service_files] if 'service_files' in locals() else []

    # Look for similar naming patterns
    name_groups = {}
    for name in service_names:
        base_name = name.replace('_', '').replace('service', '').replace('manager', '')
        if base_name not in name_groups:
            name_groups[base_name] = []
        name_groups[base_name].append(name)

    duplicate_groups = {k: v for k, v in name_groups.items() if len(v) > 1}
    print(f'Potential duplicate service groups: {len(duplicate_groups)}')

    for base, services in duplicate_groups.items():
        print(f'  {base}: {services}')

    print('\n✅ FUNCTIONAL ANALYSIS COMPLETE')
    print('🔗 Interdependency mapping ready for SWARM coordination')

    return {
        'service_files': len(service_files) if 'service_files' in locals() else 0,
        'core_subsystems': len(core_subdirs) if 'core_subdirs' in locals() else 0,
        'import_patterns': import_patterns,
        'capabilities': {k: len(set(v)) for k, v in capabilities.items()},
        'duplicate_groups': len(duplicate_groups)
    }

if __name__ == '__main__':
    results = analyze_functional_relationships()

    # Save results for SWARM coordination
    with open('Agent-8_Functional_Analysis_Results.json', 'w') as f:
        json.dump(results, f, indent=2)

    print('\n💾 Results saved to: Agent-8_Functional_Analysis_Results.json')
