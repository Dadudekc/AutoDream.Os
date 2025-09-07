#!/usr/bin/env python3
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
    
    print(f"\n📊 Validation Results:")
    print(f"Total Agents: {results['total_agents']}")
    print(f"Valid Files: {results['valid_files']}")
    print(f"Invalid Files: {results['invalid_files']}")
    
    print(f"\n📋 Detailed Results:")
    for agent_id, validation in results["agent_results"].items():
        status_icon = "✅" if validation.get("valid_json") and len(validation.get("missing_fields", [])) == 0 else "❌"
        print(f"{status_icon} {agent_id}: {validation.get('schema_version', 'UNKNOWN')}")
    
    print(f"\n✅ Validation completed!")
