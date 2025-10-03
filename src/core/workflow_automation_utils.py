"""
Workflow Automation Utilities - V2 Compliant
============================================

Utility functions for workflow automation.
V2 Compliance: ≤400 lines, ≤10 functions, single responsibility
"""

import json
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Any


def scan_agent_inbox(agent_id: str) -> List[Dict]:
    """Scan agent inbox for messages."""
    try:
        # Simulate inbox scanning
        inbox_path = Path(f"agent_workspaces/{agent_id}/inbox")
        if not inbox_path.exists():
            return []
        
        messages = []
        for file_path in inbox_path.glob("*.md"):
            with open(file_path, 'r') as f:
                content = f.read()
                messages.append({
                    "file": str(file_path),
                    "content": content[:100],  # First 100 chars
                    "timestamp": file_path.stat().st_mtime
                })
        
        return messages
    except Exception:
        return []


def evaluate_available_tasks(agent_id: str) -> List[Dict]:
    """Evaluate available tasks for an agent."""
    try:
        # Simulate task evaluation
        tasks = [
            {
                "task_id": "task_001",
                "description": "Quality gates check",
                "priority": "high",
                "estimated_time": 30
            },
            {
                "task_id": "task_002", 
                "description": "Code refactoring",
                "priority": "medium",
                "estimated_time": 120
            }
        ]
        return tasks
    except Exception:
        return []


def create_devlog_entry(agent_id: str, action: str, details: str = "") -> Dict:
    """Create a devlog entry."""
    try:
        devlog_entry = {
            "agent_id": agent_id,
            "action": action,
            "details": details,
            "timestamp": time.time(),
            "status": "created"
        }
        
        # Save to devlogs directory
        devlog_path = Path("devlogs")
        devlog_path.mkdir(exist_ok=True)
        
        filename = f"{agent_id}_{action}_{int(time.time())}.json"
        with open(devlog_path / filename, 'w') as f:
            json.dump(devlog_entry, f, indent=2)
        
        return devlog_entry
    except Exception:
        return {"error": "Failed to create devlog entry"}


def check_v2_compliance(file_path: str) -> Dict:
    """Check V2 compliance for a file."""
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
        
        line_count = len(lines)
        violations = []
        
        if line_count > 400:
            violations.append(f"File size violation: {line_count} lines (limit: 400)")
        
        # Check for other violations
        class_count = sum(1 for line in lines if line.strip().startswith('class '))
        if class_count > 5:
            violations.append(f"Too many classes: {class_count} (limit: 5)")
        
        return {
            "file_path": file_path,
            "line_count": line_count,
            "violations": violations,
            "compliant": len(violations) == 0
        }
    except Exception:
        return {"error": "Failed to check compliance"}


def check_directory_compliance(directory: str) -> List[Dict]:
    """Check V2 compliance for all files in a directory."""
    try:
        results = []
        dir_path = Path(directory)
        
        for file_path in dir_path.rglob("*.py"):
            if file_path.is_file():
                result = check_v2_compliance(str(file_path))
                results.append(result)
        
        return results
    except Exception:
        return []


def query_devlog_database(query: str) -> List[Dict]:
    """Query devlog database."""
    try:
        # Simulate database query
        devlog_path = Path("devlogs")
        if not devlog_path.exists():
            return []
        
        results = []
        for file_path in devlog_path.glob("*.json"):
            with open(file_path, 'r') as f:
                data = json.load(f)
                if query.lower() in str(data).lower():
                    results.append(data)
        
        return results
    except Exception:
        return []


def query_project_analysis() -> Dict[str, Any]:
    """Query project analysis data."""
    try:
        analysis_file = Path("project_analysis.json")
        if analysis_file.exists():
            with open(analysis_file, 'r') as f:
                return json.load(f)
        return {}
    except Exception:
        return {}


def run_quality_gates() -> Dict:
    """Run quality gates check."""
    try:
        result = subprocess.run(
            ["python", "quality_gates.py"],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "return_code": result.returncode
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "return_code": -1
        }
