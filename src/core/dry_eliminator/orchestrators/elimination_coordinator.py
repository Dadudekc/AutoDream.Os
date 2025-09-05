"""
Elimination Coordinator - V2 Compliant Module
============================================

Coordinates DRY violation elimination operations.
Extracted from dry_eliminator_orchestrator.py for V2 compliance.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

import time
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime
import logging

from ..dry_eliminator_models import (
    DRYEliminatorConfig, DRYViolation, EliminationResult, EliminationMetrics,
    DRYViolationType, EliminationStrategy, ViolationSeverity,
    create_default_config, create_elimination_metrics
)
from ..dry_elimination_engine import DRYEliminationEngine


class EliminationCoordinator:
    """
    Coordinates DRY violation elimination operations.
    
    Handles the core elimination workflow and coordination
    between different elimination components.
    """
    
    def __init__(self, config: Optional[DRYEliminatorConfig] = None):
        """Initialize elimination coordinator."""
        self.config = config or create_default_config()
        self.logger = logging.getLogger(__name__)
        
        # Initialize elimination engine
        self.elimination_engine = DRYEliminationEngine(self.config)
        
        # Operation state
        self.is_active = False
        self.current_operation = None
        self.project_root = Path.cwd()
        
        # Results tracking
        self.elimination_results = {
            "files_processed": 0,
            "imports_consolidated": 0,
            "methods_consolidated": 0,
            "documentation_consolidated": 0,
            "classes_consolidated": 0,
            "constants_consolidated": 0,
            "error_handling_consolidated": 0,
            "algorithms_consolidated": 0,
            "interfaces_consolidated": 0,
            "tests_consolidated": 0,
            "data_structures_consolidated": 0,
            "unused_imports_removed": 0,
            "errors": []
        }
    
    def eliminate_advanced_dry_violations(self) -> Dict[str, Any]:
        """Execute advanced DRY violation elimination."""
        try:
            self.is_active = True
            self.current_operation = "advanced_elimination"
            start_time = time.time()
            
            self.logger.info(f"🚀 Starting advanced DRY elimination across project...")
            
            # Discover Python files
            python_files = self.elimination_engine.discover_python_files(self.project_root)
            self.elimination_results["files_processed"] = len(python_files)
            
            # Analyze violations
            violations = self.elimination_engine.analyze_dry_violations()
            
            # Eliminate violations
            if violations:
                elimination_results = self.elimination_engine.eliminate_violations(violations)
                self._update_results_from_elimination(elimination_results)
            
            # Generate final summary
            elimination_time = time.time() - start_time
            summary = self._generate_elimination_summary(elimination_time)
            
            self.logger.info(f"✅ Advanced DRY elimination completed in {elimination_time:.2f} seconds")
            return summary
            
        except Exception as e:
            self.logger.error(f"Error in advanced DRY elimination: {e}")
            self.elimination_results["errors"].append(str(e))
            return self.elimination_results
        finally:
            self.is_active = False
            self.current_operation = None
    
    def analyze_project_violations(self) -> Dict[str, Any]:
        """Analyze project for DRY violations without elimination."""
        try:
            self.logger.info("🔍 Analyzing project for DRY violations...")
            
            # Discover and analyze
            python_files = self.elimination_engine.discover_python_files(self.project_root)
            violations = self.elimination_engine.analyze_dry_violations()
            
            # Generate analysis report
            summary = self.elimination_engine.get_elimination_summary()
            
            self.logger.info(f"Found {len(violations)} DRY violations across {len(python_files)} files")
            return summary
            
        except Exception as e:
            self.logger.error(f"Error analyzing project violations: {e}")
            return {"error": str(e)}
    
    def eliminate_specific_violations(self, violation_types: List[DRYViolationType]) -> Dict[str, Any]:
        """Eliminate specific types of violations."""
        try:
            self.logger.info(f"Eliminating specific violation types: {[vt.value for vt in violation_types]}")
            
            # Analyze all violations first
            self.elimination_engine.discover_python_files(self.project_root)
            all_violations = self.elimination_engine.analyze_dry_violations()
            
            # Filter to specific types
            target_violations = [v for v in all_violations if v.violation_type in violation_types]
            
            if not target_violations:
                self.logger.info("No violations of specified types found")
                return {"message": "No violations of specified types found"}
            
            # Eliminate target violations
            elimination_results = self.elimination_engine.eliminate_violations(target_violations)
            self._update_results_from_elimination(elimination_results)
            
            return self.elimination_results
            
        except Exception as e:
            self.logger.error(f"Error eliminating specific violations: {e}")
            return {"error": str(e)}
    
    def _update_results_from_elimination(self, elimination_results: List[EliminationResult]):
        """Update results tracking from elimination operations."""
        metrics = self.elimination_engine.metrics
        
        # Update consolidated counts from metrics
        self.elimination_results.update({
            "imports_consolidated": metrics.imports_consolidated,
            "methods_consolidated": metrics.methods_consolidated,
            "constants_consolidated": metrics.constants_consolidated,
            "unused_imports_removed": metrics.unused_imports_removed,
            "documentation_consolidated": metrics.documentation_consolidated,
            "error_handling_consolidated": metrics.error_handling_consolidated,
            "algorithms_consolidated": metrics.algorithms_consolidated,
            "interfaces_consolidated": metrics.interfaces_consolidated,
            "tests_consolidated": metrics.tests_consolidated,
            "data_structures_consolidated": metrics.data_structures_consolidated,
            "classes_consolidated": metrics.classes_consolidated
        })
    
    def _generate_elimination_summary(self, elimination_time: float) -> Dict[str, Any]:
        """Generate comprehensive elimination summary."""
        engine_summary = self.elimination_engine.get_elimination_summary()
        metrics = engine_summary['metrics']
        
        return {
            **self.elimination_results,
            "elimination_time_seconds": elimination_time,
            "total_violations_found": metrics['total_violations_found'],
            "total_violations_eliminated": metrics['total_violations_eliminated'],
            "elimination_rate": metrics['elimination_rate'],
            "net_lines_reduced": metrics['net_reduction'],
            "success_rate": metrics['success_rate'],
            "violations_by_type": engine_summary['violations_by_type'],
            "violations_by_severity": engine_summary['violations_by_severity'],
            "summary": f"Processed {metrics['total_files_analyzed']} files, "
                      f"found {metrics['total_violations_found']} violations, "
                      f"eliminated {metrics['total_violations_eliminated']} violations, "
                      f"reduced {metrics['net_reduction']} lines of code"
        }
    
    def get_coordinator_status(self) -> Dict[str, Any]:
        """Get coordinator status and metrics."""
        return {
            "is_active": self.is_active,
            "current_operation": self.current_operation,
            "project_root": str(self.project_root),
            "elimination_results": self.elimination_results
        }
    
    def reset_coordinator_state(self):
        """Reset coordinator state and clear results."""
        self.elimination_engine = DRYEliminationEngine(self.config)
        self.elimination_results = {
            "files_processed": 0,
            "imports_consolidated": 0,
            "methods_consolidated": 0,
            "documentation_consolidated": 0,
            "classes_consolidated": 0,
            "constants_consolidated": 0,
            "error_handling_consolidated": 0,
            "algorithms_consolidated": 0,
            "interfaces_consolidated": 0,
            "tests_consolidated": 0,
            "data_structures_consolidated": 0,
            "unused_imports_removed": 0,
            "errors": []
        }
        self.logger.info("Elimination coordinator state reset")
