#!/usr/bin/env python3
"""
SSOT Integration Execution Script - Agent-8 Integration & Performance Specialist

This script executes the complete SSOT integration mission, providing V2 compliance
and cross-agent system integration.

Agent: Agent-8 (Integration & Performance Specialist)
Mission: V2 Compliance SSOT Maintenance & System Integration
Status: ACTIVE - SSOT Integration & System Validation
Priority: HIGH (650 points)
"""

import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

# Import SSOT systems
from src.core.ssot.ssot_execution_coordinator import get_ssot_execution_coordinator
from src.core.ssot.unified_ssot_integration_system import get_unified_ssot_integration
from src.core.ssot.ssot_validation_system import get_ssot_validation_system

# Import unified systems
import importlib.util

# Import unified logging system
spec = importlib.util.spec_from_file_location("unified_logging_system", "src/core/consolidation/unified-logging-system.py")
unified_logging_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(unified_logging_module)

# Import unified configuration system  
spec = importlib.util.spec_from_file_location("unified_configuration_system", "src/core/consolidation/unified-configuration-system.py")
unified_config_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(unified_config_module)

# Get the functions
get_unified_logger = unified_logging_module.get_unified_logger
get_unified_config = unified_config_module.get_unified_config

def main():
    """Main execution function."""
    print("🚀 SSOT Integration Mission Execution - Agent-8")
    print("=" * 60)
    
    # Initialize systems
    logger = get_unified_logger()
    config_system = get_unified_config()
    ssot_integration = get_unified_ssot_integration()
    validation_system = get_ssot_validation_system()
    execution_coordinator = get_ssot_execution_coordinator()
    
    # Log mission start
    logger.log_operation_start("SSOT Integration Mission - Agent-8")
    
    try:
        # Execute SSOT integration mission
        print("📋 Executing SSOT Integration Mission...")
        mission_results = execution_coordinator.execute_ssot_integration_mission()
        
        # Generate and display report
        print("\n📊 Mission Results:")
        print(f"Overall Status: {mission_results['overall_status']}")
        print(f"Execution Time: {mission_results['execution_time']:.2f} seconds")
        print(f"Phases Completed: {len(mission_results['phases_completed'])}")
        print(f"Tasks Completed: {mission_results['tasks_completed']}")
        print(f"Tasks Failed: {mission_results['tasks_failed']}")
        
        # Generate detailed report
        report = execution_coordinator.generate_execution_report(mission_results)
        
        # Save report
        report_path = "agent_workspaces/Agent-8/ssot_integration_mission_report.md"
        with open(report_path, 'w') as f:
            f.write(report)
        
        print(f"\n📄 Detailed report saved to: {report_path}")
        
        # Export results
        results_path = "agent_workspaces/Agent-8/ssot_integration_mission_results.json"
        execution_coordinator.export_execution_results(mission_results, results_path)
        
        print(f"📊 Results exported to: {results_path}")
        
        # Log mission completion
        if mission_results['overall_status'] == 'completed':
            logger.log_operation_complete("SSOT Integration Mission - Agent-8")
            print("\n✅ SSOT Integration Mission COMPLETED successfully!")
        else:
            logger.log_operation_failed("SSOT Integration Mission - Agent-8", f"{mission_results['tasks_failed']} tasks failed")
            print(f"\n❌ SSOT Integration Mission FAILED - {mission_results['tasks_failed']} tasks failed")
        
        return mission_results['overall_status'] == 'completed'
        
    except Exception as e:
        logger.log_operation_failed("SSOT Integration Mission - Agent-8", str(e))
        print(f"\n💥 SSOT Integration Mission ERROR: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
