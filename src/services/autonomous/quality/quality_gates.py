#!/usr/bin/env python3
"""
Quality Gates
=============

Enforces V2 compliance and quality standards (Operating Order v1.0).
"""

import json
import logging
import subprocess
import time
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

from ...agent_devlog_automation import auto_create_devlog

logger = logging.getLogger(__name__)


class QualityGates:
    """Enforces quality gates for autonomous agents."""
    
    def __init__(self, agent_id: str, workspace_dir: Path):
        """Initialize quality gates."""
        self.agent_id = agent_id
        self.workspace_dir = workspace_dir
        self.project_root = workspace_dir.parent.parent.parent.parent
        self.quality_gates_file = workspace_dir / "quality_gates.json"
    
    async def enforce_quality_gates(self, files_changed: List[str] = None) -> Dict[str, Any]:
        """Enforce all quality gates (Operating Order v1.0)."""
        try:
            results = {
                "v2_compliance": False,
                "tests_passed": False,
                "coverage_maintained": False,
                "devlog_created": False,
                "ssot_validated": False,
                "errors": [],
                "warnings": []
            }
            
            # V2 Compliance Check
            v2_result = await self._check_v2_compliance(files_changed)
            results["v2_compliance"] = v2_result["passed"]
            results["errors"].extend(v2_result["errors"])
            results["warnings"].extend(v2_result["warnings"])
            
            # Test Suite Check
            test_result = await self._run_test_suite()
            results["tests_passed"] = test_result["passed"]
            results["errors"].extend(test_result["errors"])
            results["warnings"].extend(test_result["warnings"])
            
            # Coverage Check
            coverage_result = await self._check_coverage(files_changed)
            results["coverage_maintained"] = coverage_result["passed"]
            results["errors"].extend(coverage_result["errors"])
            results["warnings"].extend(coverage_result["warnings"])
            
            # SSOT Validation
            ssot_result = await self._validate_ssot()
            results["ssot_validated"] = ssot_result["passed"]
            results["errors"].extend(ssot_result["errors"])
            results["warnings"].extend(ssot_result["warnings"])
            
            # Create devlog for quality gates
            await auto_create_devlog(
                self.agent_id,
                "Quality gates executed",
                "completed" if all([results["v2_compliance"], results["tests_passed"], results["coverage_maintained"], results["ssot_validated"]]) else "failed",
                results
            )
            results["devlog_created"] = True
            
            # Save quality gates results
            await self._save_quality_gates_results(results)
            
            return results
            
        except Exception as e:
            logger.error(f"{self.agent_id}: Error enforcing quality gates: {e}")
            return {
                "v2_compliance": False,
                "tests_passed": False,
                "coverage_maintained": False,
                "devlog_created": False,
                "ssot_validated": False,
                "errors": [str(e)],
                "warnings": []
            }
    
    async def _check_v2_compliance(self, files_changed: List[str] = None) -> Dict[str, Any]:
        """Check V2 compliance for changed files."""
        try:
            if not files_changed:
                return {"passed": True, "errors": [], "warnings": []}
            
            errors = []
            warnings = []
            
            for file_path in files_changed:
                file_path_obj = Path(file_path)
                if not file_path_obj.exists():
                    continue
                
                # Check file size (≤400 lines)
                with open(file_path_obj, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                if len(lines) > 400:
                    errors.append(f"File {file_path} exceeds 400 lines: {len(lines)} lines")
                
                # Check for Python files specifically
                if file_path_obj.suffix == '.py':
                    # Count classes, functions, enums
                    class_count = sum(1 for line in lines if line.strip().startswith('class '))
                    function_count = sum(1 for line in lines if line.strip().startswith('def '))
                    enum_count = sum(1 for line in lines if 'Enum' in line or 'enum' in line)
                    
                    if class_count > 5:
                        errors.append(f"File {file_path} has {class_count} classes (max 5)")
                    
                    if function_count > 10:
                        errors.append(f"File {file_path} has {function_count} functions (max 10)")
                    
                    if enum_count > 3:
                        errors.append(f"File {file_path} has {enum_count} enums (max 3)")
            
            passed = len(errors) == 0
            return {"passed": passed, "errors": errors, "warnings": warnings}
            
        except Exception as e:
            logger.error(f"{self.agent_id}: Error checking V2 compliance: {e}")
            return {"passed": False, "errors": [str(e)], "warnings": []}
    
    async def _run_test_suite(self) -> Dict[str, Any]:
        """Run test suite and check for failures."""
        try:
            # Run pytest
            result = subprocess.run(
                ["python", "-m", "pytest", "-v", "--tb=short"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            passed = result.returncode == 0
            errors = []
            warnings = []
            
            if not passed:
                errors.append(f"Test suite failed with return code {result.returncode}")
                if result.stderr:
                    errors.append(f"Test errors: {result.stderr}")
            
            return {"passed": passed, "errors": errors, "warnings": warnings}
            
        except subprocess.TimeoutExpired:
            return {"passed": False, "errors": ["Test suite timed out after 5 minutes"], "warnings": []}
        except Exception as e:
            logger.error(f"{self.agent_id}: Error running test suite: {e}")
            return {"passed": False, "errors": [str(e)], "warnings": []}
    
    async def _check_coverage(self, files_changed: List[str] = None) -> Dict[str, Any]:
        """Check that coverage hasn't regressed for touched modules."""
        try:
            if not files_changed:
                return {"passed": True, "errors": [], "warnings": []}
            
            # Run coverage for changed files
            python_files = [f for f in files_changed if f.endswith('.py')]
            if not python_files:
                return {"passed": True, "errors": [], "warnings": []}
            
            # Run coverage
            result = subprocess.run(
                ["python", "-m", "pytest", "--cov"] + python_files,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            passed = result.returncode == 0
            errors = []
            warnings = []
            
            if not passed:
                errors.append("Coverage check failed")
                if result.stderr:
                    errors.append(f"Coverage errors: {result.stderr}")
            
            return {"passed": passed, "errors": errors, "warnings": warnings}
            
        except subprocess.TimeoutExpired:
            return {"passed": False, "errors": ["Coverage check timed out"], "warnings": []}
        except Exception as e:
            logger.error(f"{self.agent_id}: Error checking coverage: {e}")
            return {"passed": False, "errors": [str(e)], "warnings": []}
    
    async def _validate_ssot(self) -> Dict[str, Any]:
        """Validate Single Source of Truth compliance."""
        try:
            errors = []
            warnings = []
            
            # Check for duplicate configuration files
            config_files = list(self.project_root.glob("**/config*.json"))
            config_files.extend(list(self.project_root.glob("**/config*.yaml")))
            config_files.extend(list(self.project_root.glob("**/config*.yml")))
            
            # Check for duplicate constants files
            constants_files = list(self.project_root.glob("**/constants*.py"))
            constants_files.extend(list(self.project_root.glob("**/config*.py")))
            
            # Simple duplicate detection (same filename in different directories)
            file_names = {}
            for file_path in config_files + constants_files:
                name = file_path.name
                if name in file_names:
                    warnings.append(f"Potential SSOT violation: {name} found in multiple locations")
                else:
                    file_names[name] = file_path
            
            # Check for registry files that should be the single source
            registry_files = list(self.project_root.glob("**/registry*.json"))
            if len(registry_files) > 1:
                warnings.append(f"Multiple registry files found: {[str(f) for f in registry_files]}")
            
            passed = len(errors) == 0
            return {"passed": passed, "errors": errors, "warnings": warnings}
            
        except Exception as e:
            logger.error(f"{self.agent_id}: Error validating SSOT: {e}")
            return {"passed": False, "errors": [str(e)], "warnings": []}
    
    async def _save_quality_gates_results(self, results: Dict[str, Any]) -> None:
        """Save quality gates results to file."""
        try:
            results["timestamp"] = time.strftime("%Y-%m-%dT%H:%M:%S")
            results["agent_id"] = self.agent_id
            
            with open(self.quality_gates_file, 'w') as f:
                json.dump(results, f, indent=2)
            
            logger.info(f"{self.agent_id}: Quality gates results saved")
            
        except Exception as e:
            logger.error(f"{self.agent_id}: Error saving quality gates results: {e}")
    
    async def get_quality_gates_status(self) -> Dict[str, Any]:
        """Get current quality gates status."""
        try:
            if not self.quality_gates_file.exists():
                return {"status": "no_results", "message": "No quality gates results found"}
            
            with open(self.quality_gates_file, 'r') as f:
                results = json.load(f)
            
            return {
                "status": "results_found",
                "results": results,
                "all_passed": all([
                    results.get("v2_compliance", False),
                    results.get("tests_passed", False),
                    results.get("coverage_maintained", False),
                    results.get("ssot_validated", False)
                ])
            }
            
        except Exception as e:
            logger.error(f"{self.agent_id}: Error getting quality gates status: {e}")
            return {"status": "error", "message": str(e)}


