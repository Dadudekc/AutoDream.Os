#!/usr/bin/env python3
"""
Captain Mode Manager
==================

Manages swarm mode switching with safety checks, lock management, and integration
with existing Captain tools and onboarding system.

Author: Agent-4 (Captain & Operations Coordinator)
License: MIT
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from glob import glob

# V2 Compliance: File under 400 lines, functions under 30 lines

BASE = Path(".")
CANVAS = {"min_x": 0, "max_x": 3840, "min_y": 0, "max_y": 2160}  # Adjust to your setup


def _load_json(p: Path) -> dict:
    """Load JSON file safely."""
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return {}


def _save_json(p: Path, data: dict) -> None:
    """Save JSON file with directory creation."""
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


class ModeManager:
    """Manages swarm mode switching with safety and validation."""
    
    def __init__(self, base: Path = BASE):
        """Initialize mode manager."""
        self.base = base
        self.lock_path = self.base / "runtime" / "mode.lock"
        self.active_roles_path = self.base / "runtime" / "active_roles.json"
        self.active_coords_path = self.base / "runtime" / "active_coordinates.json"
        self.history_path = self.base / "runtime" / "mode_history.json"
        self.mode_changed_flag = self.base / "runtime" / "mode_changed.flag"
    
    def _validate_coordinates(self, coords8: dict, mapping: dict) -> Tuple[bool, List[str]]:
        """Validate coordinates are within bounds."""
        issues = []
        
        for src in mapping.keys():
            pos = coords8.get(str(int(src)))
            if not pos:
                issues.append(f"Missing coordinates for agent {src}")
                continue
                
            # Handle both dict and list formats
            if isinstance(pos, dict):
                x, y = pos.get("x", 0), pos.get("y", 0)
            elif isinstance(pos, list) and len(pos) >= 2:
                x, y = pos[0], pos[1]
            else:
                issues.append(f"Invalid coordinate format for agent {src}")
                continue
            
            if not (CANVAS["min_x"] <= x <= CANVAS["max_x"] and 
                   CANVAS["min_y"] <= y <= CANVAS["max_y"]):
                issues.append(f"Coordinate out of bounds for agent {src}: ({x},{y})")
        
        return len(issues) == 0, issues
    
    def _bootstrap_workspaces(self, include: List[int]) -> None:
        """Bootstrap missing agent workspaces."""
        for agent_id in include:
            base = Path(f"agent_workspaces/{agent_id}")
            (base / "inbox").mkdir(parents=True, exist_ok=True)
            (base / "processed").mkdir(parents=True, exist_ok=True)
            
            # Create status.json if missing
            status_file = base / "status.json"
            if not status_file.exists():
                status_file.write_text('{"timestamp": 0, "state": "idle"}', encoding="utf-8")
    
    def _check_active_operations(self) -> bool:
        """Check if any agents are actively running operations."""
        now = time.time()
        
        for status_file in glob("agent_workspaces/*/status.json"):
            try:
                with open(status_file, 'r', encoding='utf-8') as f:
                    status = json.load(f)
                    
                timestamp = status.get("timestamp", 0)
                state = status.get("state", "idle")
                
                # Consider active if timestamp is recent and state is busy
                if (now - timestamp < 60 and 
                    state in {"running", "busy", "active"}):
                    return True
            except (json.JSONDecodeError, FileNotFoundError):
                continue
        
        return False
    
    def _acquire_lock(self, owner: str, timeout: int = 10) -> bool:
        """Acquire mode switch lock."""
        start_time = time.time()
        
        while self.lock_path.exists() and time.time() - start_time < timeout:
            time.sleep(0.2)
        
        if self.lock_path.exists():
            return False
        
        self.lock_path.parent.mkdir(parents=True, exist_ok=True)
        lock_data = {"owner": owner, "timestamp": time.time()}
        _save_json(self.lock_path, lock_data)
        return True
    
    def _release_lock(self) -> None:
        """Release mode switch lock."""
        if self.lock_path.exists():
            self.lock_path.unlink(missing_ok=True)
    
    def _apply_mode(self, target_mode: int) -> bool:
        """Apply mode configuration."""
        try:
            # Load mode preset
            preset_path = self.base / "config" / "mode_presets" / f"mode-{target_mode}.json"
            if not preset_path.exists():
                return False
            
            preset = _load_json(preset_path)
            mapping = preset.get("mapping", {})
            include = preset.get("include", [])
            
            # Load canonical coordinates
            coords_path = self.base / "config" / "coordinates" / "coords-8.json"
            if not coords_path.exists():
                return False
            
            coords8 = _load_json(coords_path)
            
            # Validate coordinates
            valid, issues = self._validate_coordinates(coords8, mapping)
            if not valid:
                print(f"Coordinate validation failed: {issues}")
                return False
            
            # Build active coordinates
            active_coords = {}
            for src_agent_str, dst_idx in mapping.items():
                pos = coords8[str(int(src_agent_str))]
                active_coords[str(dst_idx)] = pos
            
            _save_json(self.active_coords_path, active_coords)
            
            # Update active roles
            roles_path = self.base / "config" / "roles.json"
            if roles_path.exists():
                roles_config = _load_json(roles_path)
                runtime_roles = {
                    "mode": target_mode,
                    "mapping": mapping,
                    "include": include,
                    "roles": roles_config.get("roles", {})
                }
                _save_json(self.active_roles_path, runtime_roles)
            
            # Bootstrap workspaces
            self._bootstrap_workspaces(include)
            
            return True
            
        except Exception as e:
            print(f"Error applying mode: {e}")
            return False
    
    def switch_mode(self, target_mode: int, owner: str, force: bool = False) -> bool:
        """Safely switch to target mode."""
        if target_mode not in [2, 4, 5, 6, 8]:
            return False
        
        # Check authority
        if owner not in ["captain", "co_captain"]:
            return False
        
        # Acquire lock
        if not self._acquire_lock(owner):
            if not force:
                return False
        
        try:
            # Check for active operations
            if self._check_active_operations() and not force:
                return False
            
            # Get current mode for history
            current = self.get_current_mode()
            
            # Apply mode
            if not self._apply_mode(target_mode):
                return False
            
            # Record in history
            history = _save_json(self.history_path, [])
            history_events = _load_json(self.history_path)
            if not isinstance(history_events, list):
                history_events = []
            
            history_events.append({
                "from": current,
                "to": target_mode,
                "owner": owner,
                "timestamp": time.time()
            })
            
            _save_json(self.history_path, history_events)
            
            # Set mode changed flag
            self.mode_changed_flag.write_text(str(time.time()), encoding="utf-8")
            
            return True
            
        finally:
            self._release_lock()
    
    def get_current_mode(self) -> int:
        """Get current swarm mode."""
        active = _load_json(self.active_roles_path)
        return active.get("mode", 8)
    
    def get_active_agents(self) -> List[int]:
        """Get list of active agents in current mode."""
        active = _load_json(self.active_roles_path)
        return active.get("include", [1, 2, 3, 4, 5, 6, 7, 8])
    
    def is_agent_active(self, agent_id: int) -> bool:
        """Check if agent is active in current mode."""
        return agent_id in self.get_active_agents()
    
    def get_mode_history(self) -> List[Dict]:
        """Get mode switch history."""
        return _load_json(self.history_path)
    
    def get_mode_changed_flag(self) -> Optional[float]:
        """Check if mode has changed since last check."""
        if self.mode_changed_flag.exists():
            try:
                return float(self.mode_changed_flag.read_text(encoding="utf-8").strip())
            except ValueError:
                pass
        return None