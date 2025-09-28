#!/usr/bin/env python3
"""
Captain Role Manager
==================

Manages agent role assignments with validation, persistence, and history tracking.
Integrates with existing Captain tools and onboarding system.

Author: Agent-4 (Captain & Operations Coordinator)
License: MIT
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# V2 Compliance: File under 400 lines, functions under 30 lines

BASE = Path(".")
POLICY = {
    "unique": {"captain"},
    "caps": {"qc_v2": 2, "system_integrator": 2, "devlog_manager": 2, "co_captain": 1}
}
HISTORY = BASE / "runtime" / "role_history.json"
ACTIVE_ROLES = BASE / "runtime" / "active_roles.json"


def _load_json(p: Path) -> dict:
    """Load JSON file safely."""
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return {}


def _save_json(p: Path, data: dict) -> None:
    """Save JSON file with directory creation."""
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


class RoleManager:
    """Manages agent role assignments with validation and history."""
    
    def __init__(self, base: Path = BASE):
        """Initialize role manager."""
        self.base = base
        self.active_path = self.base / "runtime" / "active_roles.json"
        self.tasks_path = self.base / "runtime" / "consolidated_tasks.json"
        self.history_path = self.base / "runtime" / "role_history.json"
    
    def get_active_config(self) -> Dict:
        """Get active roles configuration."""
        return _load_json(self.active_path)
    
    def _validate_role_assignment(self, agent_idx: int, role_name: str) -> Tuple[bool, str]:
        """Validate role assignment against policy."""
        active = self.get_active_config()
        
        # Check if agent is in current mode
        if str(agent_idx) not in map(str, active.get("include", [])):
            return False, "agent_not_in_mode"
        
        # Check if role exists in catalog
        catalog = active.get("roles", {})
        if role_name not in catalog:
            return False, "unknown_role"
        
        assignments = active.get("assignments", {})
        
        # Check uniqueness policy
        if role_name in POLICY["unique"]:
            if role_name in assignments.values():
                return False, "role_unique_conflict"
        
        # Check caps policy
        cap = POLICY["caps"].get(role_name)
        if cap:
            current_count = list(assignments.values()).count(role_name)
            if current_count >= cap:
                return False, "role_cap_exceeded"
        
        return True, "ok"
    
    def assign_role(self, agent_idx: int, role_name: str) -> Dict:
        """Assign role to agent with validation."""
        ok, reason = self._validate_role_assignment(agent_idx, role_name)
        active = self.get_active_config()
        
        if not active:
            return {"ok": False, "reason": "no_active_config"}
        
        # Update assignments
        active.setdefault("assignments", {})
        
        if not ok:
            # Auto-demote if policy breached
            active["assignments"][str(agent_idx)] = "unassigned"
        else:
            active["assignments"][str(agent_idx)] = role_name
        
        _save_json(self.active_path, active)
        
        # Record in history
        self._record_role_change(agent_idx, role_name, reason)
        
        return {"ok": ok, "reason": reason}
    
    def unassign_role(self, agent_idx: int) -> None:
        """Unassign role from agent."""
        active = self.get_active_config()
        if "assignments" in active and str(agent_idx) in active["assignments"]:
            del active["assignments"][str(agent_idx)]
            _save_json(self.active_path, active)
            self._record_role_change(agent_idx, "unassigned", "manual_unassign")
    
    def list_assignments(self) -> Dict[str, str]:
        """List current role assignments."""
        active = self.get_active_config()
        return active.get("assignments", {})
    
    def get_agent_role(self, agent_idx: int) -> Optional[str]:
        """Get role for specific agent."""
        assignments = self.list_assignments()
        return assignments.get(str(agent_idx))
    
    def _record_role_change(self, agent_idx: int, role_name: str, result: str) -> None:
        """Record role change in history."""
        history = _load_json(self.history_path)
        events = history.get("events", [])
        
        events.append({
            "timestamp": time.time(),
            "agent": agent_idx,
            "role": role_name,
            "result": result
        })
        
        _save_json(self.history_path, {"events": events})
    
    def record_task_update(self, task_id: str, payload: Dict) -> None:
        """Record task update in consolidated tasks."""
        tasks = _load_json(self.tasks_path)
        tasks[task_id] = payload
        _save_json(self.tasks_path, tasks)
    
    def get_role_catalog(self) -> Dict:
        """Get available roles catalog."""
        active = self.get_active_config()
        return active.get("roles", {})
    
    def get_role_description(self, role_name: str) -> Optional[str]:
        """Get description for specific role."""
        catalog = self.get_role_catalog()
        role_info = catalog.get(role_name, {})
        return role_info.get("description")
    
    def get_role_procedures(self, role_name: str) -> List[str]:
        """Get extra procedures for specific role."""
        catalog = self.get_role_catalog()
        role_info = catalog.get(role_name, {})
        return role_info.get("extra_procedures", [])