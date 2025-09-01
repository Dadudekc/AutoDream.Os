#!/usr/bin/env python3
"""
Phase 3 Validation Utils - Agent Cellphone V2
============================================

Utility functions for Phase 3 validation coordination.
Extracted from phase3_validation_coordinator.py for V2 compliance.

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

import asyncio
import time
import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional, Callable, Tuple
from .models.phase3_validation_models import (
    Phase3ValidationType, Phase3ValidationProfile, Phase3ValidationResult,
    Phase3ValidationConfig, Phase3ValidationMetrics, Phase3ValidationStrategy
)

class Phase3ValidationUtils:
    """Utility functions for Phase 3 validation coordination."""
    
    def __init__(self):
        """Initialize Phase 3 validation utilities."""
        self.validation_configs = {
            Phase3ValidationType.CLI_MODULAR_VALIDATION: Phase3ValidationConfig(
                validation_type=Phase3ValidationType.CLI_MODULAR_VALIDATION,
                priority="HIGH",
                target_reduction=30,
                max_file_lines=200,
                required_patterns=["component_extraction", "factory_pattern", "service_layer"],
                timeout_seconds=300,
                retry_attempts=3,
                parallel_execution=True
            ),
            Phase3ValidationType.JAVASCRIPT_V2_VALIDATION: Phase3ValidationConfig(
                validation_type=Phase3ValidationType.JAVASCRIPT_V2_VALIDATION,
                priority="HIGH",
                target_reduction=25,
                max_file_lines=400,
                required_patterns=["modular_architecture", "component_separation"],
                timeout_seconds=300,
                retry_attempts=3,
                parallel_execution=True
            ),
            Phase3ValidationType.REPOSITORY_PATTERN_VALIDATION: Phase3ValidationConfig(
                validation_type=Phase3ValidationType.REPOSITORY_PATTERN_VALIDATION,
                priority="MEDIUM",
                target_reduction=20,
                max_file_lines=300,
                required_patterns=["repository_pattern", "service_layer"],
                timeout_seconds=300,
                retry_attempts=3,
                parallel_execution=True
            ),
            Phase3ValidationType.GAMING_PERFORMANCE_VALIDATION: Phase3ValidationConfig(
                validation_type=Phase3ValidationType.GAMING_PERFORMANCE_VALIDATION,
                priority="HIGH",
                target_reduction=35,
                max_file_lines=250,
                required_patterns=["performance_optimization", "modular_architecture"],
                timeout_seconds=300,
                retry_attempts=3,
                parallel_execution=True
            )
        }
    
    def create_validation_profile(self, agent_id: str, agent_name: str, 
                                validation_type: Phase3ValidationType, 
                                target_files: List[str]) -> Phase3ValidationProfile:
        """Create a validation profile for an agent."""
        return Phase3ValidationProfile(
            agent_id=agent_id,
            agent_name=agent_name,
            validation_type=validation_type,
            target_files=target_files,
            validation_status="pending",
            validation_results={},
            compliance_score=0.0,
            achievements=[],
            recommendations=[],
            last_validated=None
        )
    
    def calculate_compliance_score(self, validation_results: Dict[str, Any]) -> float:
        """Calculate compliance score from validation results."""
        try:
            total_checks = validation_results.get("total_checks", 0)
            passed_checks = validation_results.get("passed_checks", 0)
            
            if total_checks == 0:
                return 0.0
            
            base_score = (passed_checks / total_checks) * 100
            
            # Bonus for V2 compliance
            v2_compliant = validation_results.get("v2_compliant", False)
            if v2_compliant:
                base_score += 10
            
            # Bonus for pattern implementation
            patterns_implemented = validation_results.get("patterns_implemented", 0)
            pattern_bonus = min(20, patterns_implemented * 5)
            
            final_score = base_score + pattern_bonus
            return min(100, max(0, final_score))
            
        except Exception:
            return 0.0
    
    def generate_achievements(self, validation_results: Dict[str, Any]) -> List[str]:
        """Generate achievements from validation results."""
        achievements = []
        
        try:
            # V2 compliance achievement
            if validation_results.get("v2_compliant", False):
                achievements.append("V2 Compliance Achieved")
            
            # Pattern implementation achievements
            patterns = validation_results.get("patterns_implemented", [])
            for pattern in patterns:
                achievements.append(f"{pattern.replace('_', ' ').title()} Pattern Implemented")
            
            # Performance achievements
            if validation_results.get("performance_improved", False):
                achievements.append("Performance Optimization Achieved")
            
            # Modularity achievements
            if validation_results.get("modular_architecture", False):
                achievements.append("Modular Architecture Implemented")
            
            # Cross-agent coordination achievements
            if validation_results.get("cross_agent_coordination", False):
                achievements.append("Cross-Agent Coordination Established")
            
        except Exception:
            pass
        
        return achievements
    
    def generate_recommendations(self, validation_results: Dict[str, Any]) -> List[str]:
        """Generate recommendations from validation results."""
        recommendations = []
        
        try:
            # V2 compliance recommendations
            if not validation_results.get("v2_compliant", False):
                recommendations.append("Implement V2 compliance standards")
            
            # Pattern recommendations
            missing_patterns = validation_results.get("missing_patterns", [])
            for pattern in missing_patterns:
                recommendations.append(f"Implement {pattern.replace('_', ' ')} pattern")
            
            # Performance recommendations
            if validation_results.get("performance_issues", False):
                recommendations.append("Optimize performance bottlenecks")
            
            # Modularity recommendations
            if not validation_results.get("modular_architecture", False):
                recommendations.append("Implement modular architecture")
            
            # Cross-agent coordination recommendations
            if not validation_results.get("cross_agent_coordination", False):
                recommendations.append("Establish cross-agent coordination")
            
        except Exception:
            pass
        
        return recommendations
    
    def execute_validation_with_timeout(self, validation_func: Callable, 
                                      timeout_seconds: int = 300) -> Dict[str, Any]:
        """Execute validation function with timeout."""
        try:
            # Run validation with timeout
            result = asyncio.run(asyncio.wait_for(
                asyncio.to_thread(validation_func), 
                timeout=timeout_seconds
            ))
            return {"success": True, "result": result, "error": None}
        except asyncio.TimeoutError:
            return {"success": False, "result": None, "error": "Validation timeout"}
        except Exception as e:
            return {"success": False, "result": None, "error": str(e)}
    
    def retry_validation(self, validation_func: Callable, 
                        max_retries: int = 3, 
                        delay_seconds: float = 1.0) -> Dict[str, Any]:
        """Retry validation function with exponential backoff."""
        for attempt in range(max_retries):
            try:
                result = validation_func()
                return {"success": True, "result": result, "attempt": attempt + 1}
            except Exception as e:
                if attempt == max_retries - 1:
                    return {"success": False, "result": None, "error": str(e), "attempts": max_retries}
                time.sleep(delay_seconds * (2 ** attempt))
        
        return {"success": False, "result": None, "error": "Max retries exceeded"}
    
    def create_validation_result(self, validation_type: Phase3ValidationType,
                               agent_id: str, execution_time: float,
                               validation_results: Dict[str, Any]) -> Phase3ValidationResult:
        """Create a validation result from execution data."""
        compliance_score = self.calculate_compliance_score(validation_results)
        achievements = self.generate_achievements(validation_results)
        recommendations = self.generate_recommendations(validation_results)
        
        return Phase3ValidationResult(
            validation_type=validation_type,
            agent_id=agent_id,
            execution_time=execution_time,
            validation_results=validation_results,
            compliance_score=compliance_score,
            achievements=achievements,
            recommendations=recommendations,
            timestamp=datetime.now()
        )
    
    def calculate_validation_metrics(self, validation_history: List[Phase3ValidationResult]) -> Phase3ValidationMetrics:
        """Calculate validation metrics from history."""
        if not validation_history:
            return Phase3ValidationMetrics(
                total_validations=0,
                successful_validations=0,
                failed_validations=0,
                average_execution_time=0.0,
                total_compliance_score=0.0,
                average_compliance_score=0.0,
                validation_coverage=0.0,
                cross_agent_coordinations=0,
                integration_tests=0
            )
        
        total_validations = len(validation_history)
        successful_validations = len([r for r in validation_history if r.compliance_score >= 70])
        failed_validations = total_validations - successful_validations
        
        average_execution_time = sum(r.execution_time for r in validation_history) / total_validations
        total_compliance_score = sum(r.compliance_score for r in validation_history)
        average_compliance_score = total_compliance_score / total_validations
        
        cross_agent_coordinations = len([r for r in validation_history 
                                       if r.validation_type == Phase3ValidationType.CROSS_AGENT_COORDINATION])
        integration_tests = len([r for r in validation_history 
                               if r.validation_type == Phase3ValidationType.INTEGRATION_TESTING])
        
        return Phase3ValidationMetrics(
            total_validations=total_validations,
            successful_validations=successful_validations,
            failed_validations=failed_validations,
            average_execution_time=average_execution_time,
            total_compliance_score=total_compliance_score,
            average_compliance_score=average_compliance_score,
            validation_coverage=(successful_validations / total_validations) * 100,
            cross_agent_coordinations=cross_agent_coordinations,
            integration_tests=integration_tests
        )
