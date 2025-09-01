#!/usr/bin/env python3
"""
Devlog Enforcement Module - Agent Cellphone V2
=============================================

Enforces mandatory Discord devlog usage across all agent operations.
Implements SSOT (Single Source of Truth) for team communication.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

import os
import sys
import json
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from pathlib import Path

# Add scripts directory to path for devlog import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))

try:
    from devlog import DevlogSystem
except ImportError:
    print("❌ ERROR: Devlog system not available")
    print("Please ensure scripts/devlog.py exists")
    sys.exit(1)


@dataclass
class DevlogEnforcementResult:
    """Result of devlog enforcement check."""
    is_compliant: bool
    violation_type: Optional[str] = None
    violation_details: Optional[str] = None
    suggested_action: Optional[str] = None


class DevlogEnforcement:
    """
    Enforces mandatory Discord devlog usage across all agent operations.
    
    This module implements SSOT principles by ensuring all project updates
    are logged through the centralized devlog system.
    """
    
    def __init__(self):
        """Initialize devlog enforcement system."""
        self.devlog = DevlogSystem()
        self.enforcement_config = self._load_enforcement_config()
        self.violation_log = []
        
    def _load_enforcement_config(self) -> Dict[str, Any]:
        """Load devlog enforcement configuration."""
        default_config = {
            "mandatory_operations": [
                "task_completion",
                "milestone_achievement", 
                "error_occurrence",
                "system_status_change",
                "coordination_event",
                "v2_compliance_update",
                "contract_assignment",
                "cross_agent_communication"
            ],
            "enforcement_level": "strict",  # strict, warning, disabled
            "violation_threshold": 3,  # Max violations before enforcement action
            "auto_devlog_fallback": True,  # Auto-create devlog if missing
            "required_categories": ["progress", "success", "issue", "warning", "info"]
        }
        
        config_path = Path("config/devlog_enforcement.json")
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
            except Exception as e:
                print(f"⚠️  WARNING: Could not load devlog enforcement config: {e}")
                
        return default_config
    
    def check_operation_compliance(self, operation_type: str, agent_id: str, 
                                 details: str = "") -> DevlogEnforcementResult:
        """
        Check if an operation requires devlog entry and if it's compliant.
        
        Args:
            operation_type: Type of operation being performed
            agent_id: Agent performing the operation
            details: Additional details about the operation
            
        Returns:
            DevlogEnforcementResult with compliance status
        """
        if self.enforcement_config["enforcement_level"] == "disabled":
            return DevlogEnforcementResult(is_compliant=True)
            
        # Check if operation type requires devlog entry
        if operation_type not in self.enforcement_config["mandatory_operations"]:
            return DevlogEnforcementResult(is_compliant=True)
            
        # Check if devlog entry exists for this operation
        recent_entries = self._get_recent_devlog_entries(agent_id, minutes=5)
        
        if not recent_entries:
            violation_details = f"Operation '{operation_type}' requires devlog entry but none found"
            suggested_action = f"Create devlog entry: python scripts/devlog.py \"{operation_type.title()}\" \"{details}\" --category progress"
            
            return DevlogEnforcementResult(
                is_compliant=False,
                violation_type="missing_devlog_entry",
                violation_details=violation_details,
                suggested_action=suggested_action
            )
            
        return DevlogEnforcementResult(is_compliant=True)
    
    def enforce_devlog_usage(self, operation_type: str, agent_id: str, 
                           title: str, content: str, category: str = "progress") -> bool:
        """
        Enforce devlog usage by creating entry if missing.
        
        Args:
            operation_type: Type of operation
            agent_id: Agent performing operation
            title: Devlog entry title
            content: Devlog entry content
            category: Devlog category
            
        Returns:
            bool: True if devlog entry created successfully
        """
        if not self.enforcement_config["auto_devlog_fallback"]:
            return False
            
        try:
            # Create devlog entry
            success = self.devlog.create_entry(title, content, category)
            
            if success:
                print(f"✅ DEVLOG ENFORCEMENT: Entry created for {operation_type}")
                return True
            else:
                print(f"❌ DEVLOG ENFORCEMENT: Failed to create entry for {operation_type}")
                return False
                
        except Exception as e:
            print(f"❌ DEVLOG ENFORCEMENT ERROR: {e}")
            return False
    
    def validate_agent_devlog_compliance(self, agent_id: str, 
                                       time_window_hours: int = 24) -> Dict[str, Any]:
        """
        Validate agent's devlog compliance over time window.
        
        Args:
            agent_id: Agent to validate
            time_window_hours: Time window for compliance check
            
        Returns:
            Dict with compliance metrics and violations
        """
        recent_entries = self._get_recent_devlog_entries(agent_id, time_window_hours * 60)
        
        compliance_metrics = {
            "agent_id": agent_id,
            "time_window_hours": time_window_hours,
            "total_entries": len(recent_entries),
            "compliance_score": 0.0,
            "violations": [],
            "recommendations": []
        }
        
        # Calculate compliance score based on entry frequency and quality
        if recent_entries:
            compliance_metrics["compliance_score"] = min(1.0, len(recent_entries) / 10.0)
        else:
            compliance_metrics["violations"].append({
                "type": "no_recent_entries",
                "message": f"No devlog entries found in last {time_window_hours} hours",
                "severity": "high"
            })
            compliance_metrics["recommendations"].append(
                "Create regular devlog entries for all significant operations"
            )
            
        return compliance_metrics
    
    def _get_recent_devlog_entries(self, agent_id: str, minutes: int) -> List[Dict[str, Any]]:
        """Get recent devlog entries for an agent."""
        try:
            # This would integrate with the actual devlog system
            # For now, return empty list as placeholder
            return []
        except Exception:
            return []
    
    def log_violation(self, agent_id: str, violation_type: str, 
                     details: str, operation_type: str) -> None:
        """Log a devlog enforcement violation."""
        violation = {
            "timestamp": time.time(),
            "agent_id": agent_id,
            "violation_type": violation_type,
            "details": details,
            "operation_type": operation_type
        }
        
        self.violation_log.append(violation)
        
        # Check if agent has exceeded violation threshold
        agent_violations = [v for v in self.violation_log if v["agent_id"] == agent_id]
        if len(agent_violations) >= self.enforcement_config["violation_threshold"]:
            self._trigger_enforcement_action(agent_id, agent_violations)
    
    def _trigger_enforcement_action(self, agent_id: str, violations: List[Dict[str, Any]]) -> None:
        """Trigger enforcement action for repeated violations."""
        print(f"🚨 DEVLOG ENFORCEMENT: Agent {agent_id} has {len(violations)} violations")
        print("   Mandatory devlog usage required for all operations")
        print("   Use: python scripts/devlog.py \"Title\" \"Content\" --category [category]")
        
        # Could implement additional enforcement actions here
        # such as blocking operations, sending alerts, etc.
    
    def get_enforcement_status(self) -> Dict[str, Any]:
        """Get current enforcement system status."""
        return {
            "enforcement_level": self.enforcement_config["enforcement_level"],
            "mandatory_operations": self.enforcement_config["mandatory_operations"],
            "total_violations": len(self.violation_log),
            "auto_devlog_fallback": self.enforcement_config["auto_devlog_fallback"],
            "devlog_system_status": self.devlog.get_status()
        }
    
    def print_enforcement_report(self) -> None:
        """Print comprehensive enforcement report."""
        print("🔍 DEVLOG ENFORCEMENT REPORT")
        print("=" * 50)
        
        status = self.get_enforcement_status()
        
        print(f"📊 Enforcement Level: {status['enforcement_level'].upper()}")
        print(f"📝 Mandatory Operations: {len(status['mandatory_operations'])}")
        print(f"⚠️  Total Violations: {status['total_violations']}")
        print(f"🤖 Auto Devlog Fallback: {'✅ Enabled' if status['auto_devlog_fallback'] else '❌ Disabled'}")
        
        print("\n📋 MANDATORY OPERATIONS:")
        for operation in status['mandatory_operations']:
            print(f"  • {operation}")
            
        print("\n📂 REQUIRED CATEGORIES:")
        for category in self.enforcement_config["required_categories"]:
            print(f"  • {category}")
            
        if status['total_violations'] > 0:
            print(f"\n⚠️  RECENT VIOLATIONS:")
            recent_violations = self.violation_log[-5:]  # Last 5 violations
            for violation in recent_violations:
                print(f"  • {violation['agent_id']}: {violation['violation_type']}")
                
        print("\n💡 USAGE:")
        print("  python scripts/devlog.py \"Title\" \"Content\" --category [category]")
        print("  python -m src.core.devlog_cli create \"Title\" \"Content\" [category]")


def enforce_devlog_for_operation(operation_type: str, agent_id: str, 
                               title: str, content: str, category: str = "progress") -> bool:
    """
    Convenience function to enforce devlog usage for an operation.
    
    Args:
        operation_type: Type of operation
        agent_id: Agent performing operation
        title: Devlog entry title
        content: Devlog entry content
        category: Devlog category
        
    Returns:
        bool: True if devlog entry created successfully
    """
    enforcement = DevlogEnforcement()
    
    # Check compliance first
    compliance_result = enforcement.check_operation_compliance(operation_type, agent_id, content)
    
    if not compliance_result.is_compliant:
        print(f"⚠️  DEVLOG ENFORCEMENT: {compliance_result.violation_details}")
        print(f"💡 SUGGESTED ACTION: {compliance_result.suggested_action}")
        
        # Log violation
        enforcement.log_violation(agent_id, compliance_result.violation_type, 
                                compliance_result.violation_details, operation_type)
        
        # Auto-create devlog entry if enabled
        if enforcement.enforcement_config["auto_devlog_fallback"]:
            return enforcement.enforce_devlog_usage(operation_type, agent_id, title, content, category)
    
    return True


if __name__ == "__main__":
    """CLI interface for devlog enforcement."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Devlog Enforcement System")
    parser.add_argument("--status", action="store_true", help="Show enforcement status")
    parser.add_argument("--check", help="Check compliance for operation type")
    parser.add_argument("--agent", help="Agent ID for compliance check")
    parser.add_argument("--enforce", help="Enforce devlog for operation")
    parser.add_argument("--title", help="Devlog entry title")
    parser.add_argument("--content", help="Devlog entry content")
    parser.add_argument("--category", default="progress", help="Devlog category")
    
    args = parser.parse_args()
    
    enforcement = DevlogEnforcement()
    
    if args.status:
        enforcement.print_enforcement_report()
    elif args.check and args.agent:
        result = enforcement.check_operation_compliance(args.check, args.agent)
        print(f"Compliance: {'✅ PASS' if result.is_compliant else '❌ FAIL'}")
        if not result.is_compliant:
            print(f"Violation: {result.violation_details}")
            print(f"Action: {result.suggested_action}")
    elif args.enforce and args.agent and args.title and args.content:
        success = enforcement.enforce_devlog_usage(args.enforce, args.agent, 
                                                 args.title, args.content, args.category)
        print(f"Enforcement: {'✅ SUCCESS' if success else '❌ FAILED'}")
    else:
        parser.print_help()
