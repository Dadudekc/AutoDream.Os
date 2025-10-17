"""
Autonomous Task Engine - Task Discovery
=======================================
Methods for discovering available task opportunities from the codebase.

Author: Agent-2 (Architecture & Design Specialist)
Date: 2025-10-16
License: MIT
"""

import json
import subprocess
import re
from pathlib import Path
from typing import List
from collections import defaultdict

from .models import Task


class TaskDiscovery:
    """Discovers available tasks from the codebase"""
    
    def __init__(self, repo_path: Path):
        self.repo_path = repo_path
    
    def discover_all(self) -> List[Task]:
        """
        Scan codebase and discover ALL available task opportunities
        
        This is the heart of autonomous intelligence - finding work
        """
        discovered = []
        
        # 1. V2 Violations (highest priority)
        discovered.extend(self.discover_v2_violations())
        
        # 2. Technical Debt
        discovered.extend(self.discover_tech_debt())
        
        # 3. TODO/FIXME comments
        discovered.extend(self.discover_code_todos())
        
        # 4. Optimization opportunities
        discovered.extend(self.discover_optimizations())
        
        # 5. Missing tests
        discovered.extend(self.discover_test_gaps())
        
        return discovered
    
    def discover_v2_violations(self) -> List[Task]:
        """Discover V2 compliance violations"""
        tasks = []
        
        try:
            # Run V2 compliance checker
            result = subprocess.run(
                ["python", "tools/v2_compliance_checker.py", ".", "--json"],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                report = json.loads(result.stdout)
                violations = report.get("violations", [])
                
                for v in violations:
                    severity = "CRITICAL" if "CRITICAL" in v.get("type", "") else "MAJOR"
                    file_path = v.get("file", "")
                    
                    # Estimate effort based on violation type
                    effort = 2 if severity == "CRITICAL" else 1
                    points = 600 if severity == "CRITICAL" else 300
                    
                    # Parse line count if available
                    current_lines = v.get("current_lines")
                    target_lines = v.get("target_lines")
                    reduction = None
                    if current_lines and target_lines:
                        reduction = ((current_lines - target_lines) / current_lines) * 100
                    
                    task = Task(
                        task_id=f"V2-{hash(file_path) % 10000:04d}",
                        title=f"Fix V2 violation in {Path(file_path).name}",
                        description=v.get("message", "V2 compliance violation"),
                        file_path=file_path,
                        task_type="V2_VIOLATION",
                        severity=severity,
                        estimated_effort=effort,
                        estimated_points=points,
                        roi_score=points / effort,
                        impact_score=9.0 if severity == "CRITICAL" else 7.0,
                        current_lines=current_lines,
                        target_lines=target_lines,
                        reduction_percent=reduction,
                        blockers=[],
                        dependencies=[],
                        coordination_needed=[],
                        skill_match={},
                        claimed_by=None,
                        claimed_at=None,
                        status="AVAILABLE"
                    )
                    tasks.append(task)
        
        except Exception:
            pass
        
        return tasks
    
    def discover_tech_debt(self) -> List[Task]:
        """Discover technical debt opportunities"""
        tasks = []
        
        # Look for files with high complexity, long functions, etc.
        for py_file in self.repo_path.rglob("*.py"):
            if "venv" in str(py_file) or "node_modules" in str(py_file):
                continue
            
            try:
                content = py_file.read_text(encoding="utf-8")
                lines = content.count("\n")
                
                # Simple heuristic: files >300 lines might need refactoring
                if lines > 300:
                    effort = 3 if lines > 500 else 2
                    points = 400 if lines > 500 else 250
                    
                    task = Task(
                        task_id=f"DEBT-{hash(str(py_file)) % 10000:04d}",
                        title=f"Refactor large file {py_file.name}",
                        description=f"File has {lines} lines, consider modularization",
                        file_path=str(py_file.relative_to(self.repo_path)),
                        task_type="TECH_DEBT",
                        severity="MAJOR",
                        estimated_effort=effort,
                        estimated_points=points,
                        roi_score=points / effort,
                        impact_score=6.0,
                        current_lines=lines,
                        target_lines=int(lines * 0.6),
                        reduction_percent=40.0,
                        blockers=[],
                        dependencies=[],
                        coordination_needed=[],
                        skill_match={},
                        claimed_by=None,
                        claimed_at=None,
                        status="AVAILABLE"
                    )
                    tasks.append(task)
            
            except Exception:
                pass
        
        return tasks[:20]  # Limit to top 20
    
    def discover_code_todos(self) -> List[Task]:
        """Discover TODO and FIXME comments"""
        tasks = []
        
        try:
            result = subprocess.run(
                ["git", "grep", "-n", "-E", "TODO|FIXME"],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            
            for line in result.stdout.split("\n")[:50]:  # Limit to 50
                if not line:
                    continue
                
                match = re.match(r"([^:]+):(\d+):(.*)", line)
                if match:
                    file_path, line_num, comment = match.groups()
                    
                    severity = "MAJOR" if "FIXME" in comment else "MINOR"
                    effort = 1
                    points = 150 if severity == "MAJOR" else 50
                    
                    task = Task(
                        task_id=f"TODO-{hash(line) % 10000:04d}",
                        title=f"Address TODO in {Path(file_path).name}:{line_num}",
                        description=comment.strip(),
                        file_path=file_path,
                        task_type="TECH_DEBT",
                        severity=severity,
                        estimated_effort=effort,
                        estimated_points=points,
                        roi_score=points / effort,
                        impact_score=5.0 if severity == "MAJOR" else 3.0,
                        current_lines=None,
                        target_lines=None,
                        reduction_percent=None,
                        blockers=[],
                        dependencies=[],
                        coordination_needed=[],
                        skill_match={},
                        claimed_by=None,
                        claimed_at=None,
                        status="AVAILABLE"
                    )
                    tasks.append(task)
        
        except Exception:
            pass
        
        return tasks
    
    def discover_optimizations(self) -> List[Task]:
        """Discover optimization opportunities"""
        # Could integrate with complexity analyzer
        return []
    
    def discover_test_gaps(self) -> List[Task]:
        """Discover files without tests"""
        tasks = []
        
        src_files = list(self.repo_path.glob("src/**/*.py"))
        test_files = set(self.repo_path.glob("tests/**/*.py"))
        
        for src_file in src_files[:30]:  # Limit
            # Check if test exists
            relative = src_file.relative_to(self.repo_path / "src")
            expected_test = self.repo_path / "tests" / f"test_{relative.name}"
            
            if expected_test not in test_files:
                task = Task(
                    task_id=f"TEST-{hash(str(src_file)) % 10000:04d}",
                    title=f"Add tests for {src_file.name}",
                    description=f"Missing test coverage for {relative}",
                    file_path=str(src_file.relative_to(self.repo_path)),
                    task_type="FEATURE",
                    severity="MINOR",
                    estimated_effort=2,
                    estimated_points=200,
                    roi_score=100.0,
                    impact_score=6.0,
                    current_lines=None,
                    target_lines=None,
                    reduction_percent=None,
                    blockers=[],
                    dependencies=[],
                    coordination_needed=[],
                    skill_match={},
                    claimed_by=None,
                    claimed_at=None,
                    status="AVAILABLE"
                )
                tasks.append(task)
        
        return tasks

