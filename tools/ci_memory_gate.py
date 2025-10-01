#!/usr/bin/env python3
"""
CI Memory Gate - V2_SWARM
=========================

CI/CD integration for memory monitoring and enforcement.
Runs memory checks in CI pipeline.

Author: Agent-5 (Coordinator)
License: MIT
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.observability.memory.watchdog import EnforcementMode, IntegratedWatchdog


def run_memory_gate(config_path: str = "config/memory_policy.yaml",
                   enforcement: str = "observe",
                   output: Optional[str] = None,
                   fail_on_critical: bool = True) -> int:
    """Run memory gate check for CI"""
    
    # Map enforcement mode
    mode_map = {
        'observe': EnforcementMode.OBSERVE,
        'quarantine': EnforcementMode.QUARANTINE,
        'kill': EnforcementMode.KILL
    }
    enforcement_mode = mode_map.get(enforcement, EnforcementMode.OBSERVE)
    
    print("🔍 Running CI Memory Gate...")
    print(f"   Mode: {enforcement_mode.value}")
    print(f"   Config: {config_path}")
    
    try:
        # Create watchdog
        watchdog = IntegratedWatchdog(config_path, enforcement_mode)
        
        # Run full check
        results = watchdog.run_full_check()
        
        # Check for failures
        critical_count = 0
        warning_count = 0
        
        for service, check in results.get('budget_checks', {}).items():
            status = check.get('status', 'ok')
            if status == 'critical':
                critical_count += 1
                print(f"   🚨 CRITICAL: {service} - {check.get('current_mb', 0):.2f} MB")
            elif status == 'warning':
                warning_count += 1
                print(f"   ⚠️  WARNING: {service} - {check.get('current_mb', 0):.2f} MB")
        
        # Save results if output specified
        if output:
            Path(output).parent.mkdir(parents=True, exist_ok=True)
            with open(output, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"   📄 Results saved to {output}")
        
        # Stop watchdog
        watchdog.stop_monitoring()
        
        # Determine exit code
        if fail_on_critical and critical_count > 0:
            print(f"\n❌ CI MEMORY GATE FAILED: {critical_count} critical issues")
            return 1
        
        if warning_count > 0:
            print(f"\n⚠️  CI MEMORY GATE WARNING: {warning_count} warnings")
        else:
            print("\n✅ CI MEMORY GATE PASSED")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ CI MEMORY GATE ERROR: {e}")
        return 2


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="CI Memory Gate for V2_SWARM")
    
    parser.add_argument(
        '--config',
        default='config/memory_policy.yaml',
        help='Path to memory policy configuration'
    )
    
    parser.add_argument(
        '--enforcement',
        choices=['observe', 'quarantine', 'kill'],
        default='observe',
        help='Enforcement mode'
    )
    
    parser.add_argument(
        '--output',
        help='Output file for results (JSON)'
    )
    
    parser.add_argument(
        '--no-fail',
        action='store_true',
        help='Do not fail on critical issues'
    )
    
    args = parser.parse_args()
    
    exit_code = run_memory_gate(
        config_path=args.config,
        enforcement=args.enforcement,
        output=args.output,
        fail_on_critical=not args.no_fail
    )
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()

