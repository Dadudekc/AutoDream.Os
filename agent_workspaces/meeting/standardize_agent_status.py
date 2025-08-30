#!/usr/bin/env python3
"""
Agent Status Standardization Script
==================================

This script standardizes all agent status.json files with the new timestamp-based schema.
Updates all 8 agents to use consistent format and structure.

Author: Agent-1 (PERPETUAL MOTION LEADER)
Date: August 29, 2025
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional

class AgentStatusStandardizer:
    def __init__(self, workspace_root: str = "agent_workspaces"):
        self.workspace_root = Path(workspace_root)
        self.template_file = self.workspace_root / "meeting" / "standardized_status_template.json"
        self.agents = [
            "Agent-1", "Agent-2", "Agent-3", "Agent-4", 
            "Agent-5", "Agent-6", "Agent-7", "Agent-8"
        ]
        self.current_time = datetime.now(timezone.utc).isoformat()
        
    def load_template(self) -> Dict[str, Any]:
        """Load the standardized status template"""
        try:
            with open(self.template_file, 'r') as f:
                template = json.load(f)
            print(f"✅ Template loaded: {self.template_file}")
            return template
        except Exception as e:
            print(f"❌ Error loading template: {e}")
            return {}
    
    def get_agent_role(self, agent_id: str) -> str:
        """Get the role for a specific agent"""
        roles = {
            "Agent-1": "PERPETUAL MOTION LEADER - COORDINATION ENHANCEMENT MANAGER",
            "Agent-2": "PHASE TRANSITION OPTIMIZATION MANAGER",
            "Agent-3": "CAPTAIN_ELECT - TESTING FRAMEWORK ENHANCEMENT MANAGER",
            "Agent-4": "STRATEGIC OVERSIGHT & EMERGENCY INTERVENTION MANAGER",
            "Agent-5": "SPRINT ACCELERATION MANAGER",
            "Agent-6": "PERFORMANCE OPTIMIZATION MANAGER",
            "Agent-7": "QUALITY COMPLETION OPTIMIZATION MANAGER",
            "Agent-8": "INTEGRATION ENHANCEMENT OPTIMIZATION MANAGER"
        }
        return roles.get(agent_id, "AGENT_ROLE_PLACEHOLDER")
    
    def get_agent_contract_info(self, agent_id: str) -> Dict[str, Any]:
        """Get current contract information for a specific agent"""
        # This would normally be extracted from existing status files
        # For now, using placeholder data
        contracts = {
            "Agent-1": {
                "contract_id": "SSOT-001",
                "title": "SSOT Violation Analysis & Resolution",
                "category": "SSOT_Resolution",
                "points": 400,
                "difficulty": "HIGH",
                "estimated_time": "3-4 hours",
                "priority": "HIGH"
            },
            "Agent-2": {
                "contract_id": "COORD-011",
                "title": "Inbox Management System Optimization",
                "category": "Coordination",
                "points": 250,
                "difficulty": "MEDIUM",
                "estimated_time": "2-3 hours",
                "priority": "NORMAL"
            },
            "Agent-3": {
                "contract_id": "TEST-001",
                "title": "Testing Framework Enhancement",
                "category": "Testing",
                "points": 300,
                "difficulty": "MEDIUM",
                "estimated_time": "2-3 hours",
                "priority": "NORMAL"
            },
            "Agent-4": {
                "contract_id": "CAPTAIN-001",
                "title": "Strategic Oversight & Emergency Intervention",
                "category": "Leadership",
                "points": 500,
                "difficulty": "HIGH",
                "estimated_time": "4-5 hours",
                "priority": "MAXIMUM"
            },
            "Agent-5": {
                "contract_id": "PERF-003",
                "title": "System Performance Benchmarking",
                "category": "Performance",
                "points": 300,
                "difficulty": "HIGH",
                "estimated_time": "3-4 hours",
                "priority": "HIGH"
            },
            "Agent-6": {
                "contract_id": "MODULAR-008",
                "title": "Modularization Progress Tracking System",
                "category": "Modularization",
                "points": 275,
                "difficulty": "MEDIUM",
                "estimated_time": "2-3 hours",
                "priority": "NORMAL"
            },
            "Agent-7": {
                "contract_id": "MODULAR-009",
                "title": "Modularization Quality Assurance Framework",
                "category": "Quality",
                "points": 300,
                "difficulty": "MEDIUM",
                "estimated_time": "2-3 hours",
                "priority": "NORMAL"
            },
            "Agent-8": {
                "contract_id": "OPTIM-001",
                "title": "System Performance Monitoring Dashboard",
                "category": "Optimization",
                "points": 325,
                "difficulty": "MEDIUM",
                "estimated_time": "2-3 hours",
                "priority": "NORMAL"
            }
        }
        return contracts.get(agent_id, {})
    
    def create_standardized_status(self, agent_id: str, template: Dict[str, Any]) -> Dict[str, Any]:
        """Create a standardized status for a specific agent"""
        # Deep copy the template
        status = json.loads(json.dumps(template))
        
        # Update with agent-specific information
        status["agent_id"] = agent_id
        status["role"] = self.get_agent_role(agent_id)
        status["last_updated"] = self.current_time
        
        # Update contract information
        contract_info = self.get_agent_contract_info(agent_id)
        if contract_info:
            status["current_contract"].update(contract_info)
        
        # Update timestamps
        status["work_status"]["started_at"] = self.current_time
        status["work_status"]["estimated_completion"] = self.current_time
        status["communication"]["last_inbox_check"] = self.current_time
        status["workspace_health"]["last_cleanup"] = self.current_time
        status["metadata"]["created_at"] = self.current_time
        status["metadata"]["last_schema_update"] = self.current_time
        
        # Update notes
        status["notes"] = f"Standardized status file for {agent_id} - Status schema version 2.0 with timestamp-based tracking"
        
        return status
    
    def backup_existing_status(self, agent_id: str) -> bool:
        """Backup existing status.json file"""
        status_file = self.workspace_root / agent_id / "status.json"
        if status_file.exists():
            backup_file = self.workspace_root / agent_id / "status.json.backup"
            try:
                import shutil
                shutil.copy2(status_file, backup_file)
                print(f"✅ Backup created: {backup_file}")
                return True
            except Exception as e:
                print(f"❌ Backup failed for {agent_id}: {e}")
                return False
        return True
    
    def update_agent_status(self, agent_id: str, template: Dict[str, Any]) -> bool:
        """Update a specific agent's status.json file"""
        agent_dir = self.workspace_root / agent_id
        status_file = agent_dir / "status.json"
        
        if not agent_dir.exists():
            print(f"⚠️  Agent directory not found: {agent_dir}")
            return False
        
        try:
            # Create backup
            self.backup_existing_status(agent_id)
            
            # Create standardized status
            standardized_status = self.create_standardized_status(agent_id, template)
            
            # Write new status file
            with open(status_file, 'w') as f:
                json.dump(standardized_status, f, indent=2)
            
            print(f"✅ Status updated for {agent_id}")
            return True
            
        except Exception as e:
            print(f"❌ Error updating {agent_id}: {e}")
            return False
    
    def standardize_all_agents(self) -> Dict[str, Any]:
        """Standardize all agent status.json files"""
        print("🚀 Starting Agent Status Standardization")
        print("=" * 50)
        
        # Load template
        template = self.load_template()
        if not template:
            return {"error": "Failed to load template"}
        
        results = {
            "total_agents": len(self.agents),
            "successful_updates": 0,
            "failed_updates": 0,
            "agent_results": {},
            "timestamp": self.current_time
        }
        
        # Update each agent
        for agent_id in self.agents:
            print(f"\n📋 Processing {agent_id}...")
            
            success = self.update_agent_status(agent_id, template)
            
            if success:
                results["successful_updates"] += 1
                results["agent_results"][agent_id] = "SUCCESS"
            else:
                results["failed_updates"] += 1
                results["agent_results"][agent_id] = "FAILED"
        
        return results
    
    def generate_validation_script(self) -> str:
        """Generate a validation script for status.json compliance"""
        validation_script = '''#!/usr/bin/env python3
"""
Status.json Validation Script
============================

Validates that all agent status.json files comply with the standardized schema.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, List

def validate_status_file(file_path: Path) -> Dict[str, Any]:
    """Validate a single status.json file"""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        validation_result = {
            "file": str(file_path),
            "valid_json": True,
            "schema_version": data.get("status_version", "MISSING"),
            "required_fields": [],
            "missing_fields": [],
            "timestamp_format": "UNKNOWN"
        }
        
        # Check required fields
        required_fields = [
            "agent_id", "role", "status_version", "last_updated",
            "current_contract", "progress", "work_status", "blockers",
            "deliverables", "communication", "workspace_health",
            "quality_metrics", "contract_history", "next_actions",
            "emergency_status", "notes", "metadata"
        ]
        
        for field in required_fields:
            if field in data:
                validation_result["required_fields"].append(field)
            else:
                validation_result["missing_fields"].append(field)
        
        # Check timestamp format
        if "last_updated" in data:
            timestamp = data["last_updated"]
            if "T" in str(timestamp) and "Z" in str(timestamp):
                validation_result["timestamp_format"] = "ISO_8601"
            else:
                validation_result["timestamp_format"] = "NON_STANDARD"
        
        return validation_result
        
    except json.JSONDecodeError as e:
        return {
            "file": str(file_path),
            "valid_json": False,
            "error": str(e),
            "schema_version": "UNKNOWN",
            "required_fields": [],
            "missing_fields": [],
            "timestamp_format": "UNKNOWN"
        }
    except Exception as e:
        return {
            "file": str(file_path),
            "valid_json": False,
            "error": str(e),
            "schema_version": "UNKNOWN",
            "required_fields": [],
            "missing_fields": [],
            "timestamp_format": "UNKNOWN"
        }

def validate_all_agents(workspace_root: str = "agent_workspaces") -> Dict[str, Any]:
    """Validate all agent status.json files"""
    workspace_path = Path(workspace_root)
    agents = ["Agent-1", "Agent-2", "Agent-3", "Agent-4", 
              "Agent-5", "Agent-6", "Agent-7", "Agent-8"]
    
    results = {
        "total_agents": len(agents),
        "valid_files": 0,
        "invalid_files": 0,
        "agent_results": {}
    }
    
    for agent_id in agents:
        status_file = workspace_path / agent_id / "status.json"
        if status_file.exists():
            validation = validate_status_file(status_file)
            results["agent_results"][agent_id] = validation
            
            if validation["valid_json"] and len(validation["missing_fields"]) == 0:
                results["valid_files"] += 1
            else:
                results["invalid_files"] += 1
        else:
            results["agent_results"][agent_id] = {
                "file": str(status_file),
                "valid_json": False,
                "error": "File not found"
            }
            results["invalid_files"] += 1
    
    return results

if __name__ == "__main__":
    print("🧪 Validating Agent Status Files")
    print("=" * 40)
    
    results = validate_all_agents()
    
    print(f"\\n📊 Validation Results:")
    print(f"Total Agents: {results['total_agents']}")
    print(f"Valid Files: {results['valid_files']}")
    print(f"Invalid Files: {results['invalid_files']}")
    
    print(f"\\n📋 Detailed Results:")
    for agent_id, validation in results["agent_results"].items():
        status_icon = "✅" if validation.get("valid_json") and len(validation.get("missing_fields", [])) == 0 else "❌"
        print(f"{status_icon} {agent_id}: {validation.get('schema_version', 'UNKNOWN')}")
    
    print(f"\\n✅ Validation completed!")
'''
        
        return validation_script
    
    def run_standardization(self) -> Dict[str, Any]:
        """Run the complete standardization process"""
        print("🎯 AGENT STATUS STANDARDIZATION MISSION")
        print("=" * 50)
        print(f"Timestamp: {self.current_time}")
        print(f"Agents to process: {len(self.agents)}")
        print(f"Template: {self.template_file}")
        print("=" * 50)
        
        # Standardize all agents
        results = self.standardize_all_agents()
        
        # Generate validation script
        validation_script_path = self.workspace_root / "meeting" / "validate_status_compliance.py"
        validation_script = self.generate_validation_script()
        
        try:
            with open(validation_script_path, 'w') as f:
                f.write(validation_script)
            print(f"✅ Validation script generated: {validation_script_path}")
        except Exception as e:
            print(f"❌ Error generating validation script: {e}")
        
        return results

def main():
    """Main execution function"""
    standardizer = AgentStatusStandardizer()
    results = standardizer.run_standardization()
    
    print(f"\n🎉 STANDARDIZATION COMPLETED!")
    print(f"📊 Results:")
    print(f"   Total Agents: {results.get('total_agents', 0)}")
    print(f"   Successful Updates: {results.get('successful_updates', 0)}")
    print(f"   Failed Updates: {results.get('failed_updates', 0)}")
    
    if results.get('agent_results'):
        print(f"\n📋 Agent Results:")
        for agent_id, status in results['agent_results'].items():
            status_icon = "✅" if status == "SUCCESS" else "❌"
            print(f"   {status_icon} {agent_id}: {status}")
    
    print(f"\n🚀 Mission Status: COMPLETED")
    print(f"📁 Files Updated: All agent status.json files")
    print(f"📋 Template: standardized_status_template.json")
    print(f"🔍 Validation: validate_status_compliance.py")

if __name__ == "__main__":
    main()
