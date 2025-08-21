#!/usr/bin/env python3
"""
Automated Quality Gates System
==============================
Enterprise-grade automated quality validation and gates.
Target: 300 LOC, Maximum: 350 LOC.
Focus: Automated quality control, LOC compliance, enterprise standards enforcement.
"""

import os
import sys
import time
import json
import ast
import inspect
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import V2 services for quality validation
try:
    from services.enterprise_quality_assurance import EnterpriseQualityAssurance
    from services.integration_monitoring import V2IntegrationMonitoring
    from services.core_coordinator_service import CoreCoordinatorService
except ImportError as e:
    print(f"Import warning: {e}")
    # Fallback mock services for quality validation
    EnterpriseQualityAssurance = None
    V2IntegrationMonitoring = None
    CoreCoordinatorService = None


@dataclass
class QualityGateResult:
    """Quality gate validation result"""
    gate_name: str
    status: str  # PASSED, FAILED, WARNING
    score: float
    details: Dict
    timestamp: float
    recommendations: List[str]


@dataclass
class CodeQualityMetrics:
    """Code quality metrics"""
    loc_count: int
    complexity_score: float
    maintainability_index: float
    documentation_coverage: float
    test_coverage: float
    compliance_score: float


class AutomatedQualityGates:
    """Automated quality gates system for enterprise standards enforcement"""
    
    def __init__(self, config_path: str = "quality_gates_config.json"):
        """Initialize automated quality gates system"""
        self.config_path = config_path
        self.config = self._load_configuration()
        self.quality_gates = self._initialize_quality_gates()
        self.validation_history = []
        
        # Initialize V2 services
        self.enterprise_qa = EnterpriseQualityAssurance() if EnterpriseQualityAssurance else None
        self.integration_monitoring = V2IntegrationMonitoring() if V2IntegrationMonitoring else None
        self.core_coordinator = CoreCoordinatorService() if CoreCoordinatorService else None
    
    def _load_configuration(self) -> Dict:
        """Load quality gates configuration"""
        default_config = {
            "loc_limits": {
                "target": 300,
                "maximum": 350,
                "critical": 400
            },
            "quality_thresholds": {
                "minimum_score": 80.0,
                "target_score": 90.0,
                "excellent_score": 95.0
            },
            "enforcement_rules": {
                "strict_mode": True,
                "auto_reject": False,
                "quality_gates": ["loc_compliance", "code_quality", "enterprise_standards"]
            }
        }
        
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            else:
                # Create default configuration
                with open(self.config_path, 'w') as f:
                    json.dump(default_config, f, indent=2)
                return default_config
        except Exception as e:
            print(f"Configuration loading error: {e}")
            return default_config
    
    def _initialize_quality_gates(self) -> Dict:
        """Initialize quality gates with validation rules"""
        return {
            "loc_compliance": {
                "name": "LOC Compliance Gate",
                "description": "Validates line count compliance",
                "weight": 0.25,
                "validator": self._validate_loc_compliance
            },
            "code_quality": {
                "name": "Code Quality Gate",
                "description": "Validates code quality metrics",
                "weight": 0.30,
                "validator": self._validate_code_quality
            },
            "enterprise_standards": {
                "name": "Enterprise Standards Gate",
                "description": "Validates enterprise coding standards",
                "weight": 0.25,
                "validator": self._validate_enterprise_standards
            },
            "test_coverage": {
                "name": "Test Coverage Gate",
                "description": "Validates test coverage requirements",
                "weight": 0.20,
                "validator": self._validate_test_coverage
            }
        }
    
    def validate_file(self, file_path: str) -> QualityGateResult:
        """Validate a single file through all quality gates"""
        print(f"🔍 Validating file: {file_path}")
        
        if not os.path.exists(file_path):
            return QualityGateResult(
                gate_name="file_validation",
                status="FAILED",
                score=0.0,
                details={"error": "File not found"},
                timestamp=time.time(),
                recommendations=["Ensure file path is correct"]
            )
        
        # Run all quality gates
        gate_results = {}
        total_score = 0.0
        total_weight = 0.0
        
        for gate_id, gate_config in self.quality_gates.items():
            try:
                result = gate_config["validator"](file_path)
                gate_results[gate_id] = result
                total_score += result.score * gate_config["weight"]
                total_weight += gate_config["weight"]
            except Exception as e:
                gate_results[gate_id] = {
                    "status": "ERROR",
                    "score": 0.0,
                    "error": str(e)
                }
        
        # Calculate overall score
        overall_score = total_score / total_weight if total_weight > 0 else 0.0
        
        # Determine overall status
        if overall_score >= self.config["quality_thresholds"]["excellent_score"]:
            status = "PASSED"
        elif overall_score >= self.config["quality_thresholds"]["target_score"]:
            status = "PASSED"
        elif overall_score >= self.config["quality_thresholds"]["minimum_score"]:
            status = "WARNING"
        else:
            status = "FAILED"
        
        # Generate recommendations
        recommendations = self._generate_recommendations(gate_results, overall_score)
        
        result = QualityGateResult(
            gate_name="comprehensive_validation",
            status=status,
            score=overall_score,
            details={"gate_results": gate_results, "overall_score": overall_score},
            timestamp=time.time(),
            recommendations=recommendations
        )
        
        # Store in validation history
        self.validation_history.append(result)
        
        return result
    
    def _validate_loc_compliance(self, file_path: str) -> Dict:
        """Validate LOC compliance"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            loc_count = len(lines)
            target = self.config["loc_limits"]["target"]
            maximum = self.config["loc_limits"]["maximum"]
            critical = self.config["loc_limits"]["critical"]
            
            # Calculate compliance score
            if loc_count <= target:
                score = 100.0
            elif loc_count <= maximum:
                score = 100.0 - ((loc_count - target) / (maximum - target)) * 20.0
            elif loc_count <= critical:
                score = 80.0 - ((loc_count - maximum) / (critical - maximum)) * 30.0
            else:
                score = 50.0
            
            return {
                "status": "PASSED" if score >= 80.0 else "FAILED",
                "score": score,
                "loc_count": loc_count,
                "target": target,
                "maximum": maximum,
                "critical": critical
            }
            
        except Exception as e:
            return {"status": "ERROR", "score": 0.0, "error": str(e)}
    
    def _validate_code_quality(self, file_path: str) -> Dict:
        """Validate code quality metrics"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse AST for analysis
            tree = ast.parse(content)
            
            # Calculate metrics
            loc_count = len(content.splitlines())
            function_count = len([node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)])
            class_count = len([node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)])
            
            # Complexity score (simplified)
            complexity_score = min(100.0, max(0.0, 100.0 - (function_count * 2) - (class_count * 3)))
            
            # Maintainability index
            maintainability = max(0.0, 100.0 - (loc_count / 10) - (function_count * 2))
            
            # Documentation coverage (simplified)
            doc_lines = len([line for line in content.splitlines() if line.strip().startswith('#') or line.strip().startswith('"""')])
            doc_coverage = min(100.0, (doc_lines / max(1, loc_count)) * 100.0)
            
            # Overall quality score
            quality_score = (complexity_score + maintainability + doc_coverage) / 3
            
            return {
                "status": "PASSED" if quality_score >= 70.0 else "FAILED",
                "score": quality_score,
                "metrics": {
                    "complexity_score": complexity_score,
                    "maintainability": maintainability,
                    "documentation_coverage": doc_coverage,
                    "function_count": function_count,
                    "class_count": class_count
                }
            }
            
        except Exception as e:
            return {"status": "ERROR", "score": 0.0, "error": str(e)}
    
    def _validate_enterprise_standards(self, file_path: str) -> Dict:
        """Validate enterprise coding standards"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            standards_score = 100.0
            violations = []
            
            # Check for required patterns
            required_patterns = [
                (r'#!/usr/bin/env python3', "Missing shebang"),
                (r'"""[\s\S]*?"""', "Missing docstring"),
                (r'class \w+', "Missing class definition"),
                (r'def \w+', "Missing function definition")
            ]
            
            for pattern, description in required_patterns:
                if not re.search(pattern, content):
                    standards_score -= 20.0
                    violations.append(description)
            
            # Check for enterprise practices
            enterprise_practices = [
                (r'from typing import', "Missing type hints"),
                (r'@dataclass', "Missing dataclass usage"),
                (r'class \w+\(unittest\.TestCase\)', "Missing unittest structure")
            ]
            
            for pattern, description in enterprise_practices:
                if not re.search(pattern, content):
                    standards_score -= 10.0
                    violations.append(description)
            
            standards_score = max(0.0, standards_score)
            
            return {
                "status": "PASSED" if standards_score >= 80.0 else "FAILED",
                "score": standards_score,
                "violations": violations,
                "standards_met": len(required_patterns) + len(enterprise_practices) - len(violations)
            }
            
        except Exception as e:
            return {"status": "ERROR", "score": 0.0, "error": str(e)}
    
    def _validate_test_coverage(self, file_path: str) -> Dict:
        """Validate test coverage requirements"""
        try:
            # Check if test file exists
            test_file_path = file_path.replace('.py', '_test.py')
            if not os.path.exists(test_file_path):
                test_file_path = file_path.replace('.py', 's.py')
            
            if os.path.exists(test_file_path):
                # Basic test file validation
                with open(test_file_path, 'r', encoding='utf-8') as f:
                    test_content = f.read()
                
                test_score = 100.0
                test_metrics = {}
                
                # Check for test methods
                if 'def test_' in test_content:
                    test_metrics['test_methods'] = True
                else:
                    test_score -= 30.0
                    test_metrics['test_methods'] = False
                
                # Check for unittest framework
                if 'unittest.TestCase' in test_content:
                    test_metrics['unittest_framework'] = True
                else:
                    test_score -= 20.0
                    test_metrics['unittest_framework'] = False
                
                # Check for assertions
                if 'assert' in test_content:
                    test_metrics['assertions'] = True
                else:
                    test_score -= 20.0
                    test_metrics['assertions'] = False
                
                test_score = max(0.0, test_score)
                
                return {
                    "status": "PASSED" if test_score >= 70.0 else "FAILED",
                    "score": test_score,
                    "test_file_found": True,
                    "test_metrics": test_metrics
                }
            else:
                return {
                    "status": "FAILED",
                    "score": 0.0,
                    "test_file_found": False,
                    "recommendation": "Create corresponding test file"
                }
                
        except Exception as e:
            return {"status": "ERROR", "score": 0.0, "error": str(e)}
    
    def _generate_recommendations(self, gate_results: Dict, overall_score: float) -> List[str]:
        """Generate improvement recommendations"""
        recommendations = []
        
        if overall_score < self.config["quality_thresholds"]["target_score"]:
            recommendations.append("Overall quality below target - review and improve code")
        
        for gate_id, result in gate_results.items():
            if result.get("status") == "FAILED":
                if gate_id == "loc_compliance":
                    recommendations.append("Reduce line count to meet LOC compliance")
                elif gate_id == "code_quality":
                    recommendations.append("Improve code structure and documentation")
                elif gate_id == "enterprise_standards":
                    recommendations.append("Follow enterprise coding standards")
                elif gate_id == "test_coverage":
                    recommendations.append("Improve test coverage and quality")
        
        if not recommendations:
            recommendations.append("Code meets enterprise quality standards")
        
        return recommendations
    
    def validate_directory(self, directory_path: str) -> Dict:
        """Validate all Python files in a directory"""
        print(f"🔍 Validating directory: {directory_path}")
        
        results = {}
        total_files = 0
        passed_files = 0
        failed_files = 0
        
        for file_path in Path(directory_path).rglob("*.py"):
            if file_path.is_file():
                total_files += 1
                result = self.validate_file(str(file_path))
                results[str(file_path)] = asdict(result)
                
                if result.status == "PASSED":
                    passed_files += 1
                else:
                    failed_files += 1
        
        # Calculate directory quality score
        directory_score = (passed_files / total_files * 100) if total_files > 0 else 0.0
        
        return {
            "directory_path": directory_path,
            "total_files": total_files,
            "passed_files": passed_files,
            "failed_files": failed_files,
            "quality_score": directory_score,
            "file_results": results,
            "timestamp": time.time()
        }
    
    def get_quality_summary(self) -> Dict:
        """Get overall quality summary"""
        if not self.validation_history:
            return {"status": "No validations performed"}
        
        total_validations = len(self.validation_history)
        passed_validations = len([r for r in self.validation_history if r.status == "PASSED"])
        failed_validations = len([r for r in self.validation_history if r.status == "FAILED"])
        warning_validations = len([r for r in self.validation_history if r.status == "WARNING"])
        
        average_score = sum(r.score for r in self.validation_history) / total_validations
        
        return {
            "total_validations": total_validations,
            "passed_validations": passed_validations,
            "failed_validations": failed_validations,
            "warning_validations": warning_validations,
            "success_rate": (passed_validations / total_validations * 100) if total_validations > 0 else 0.0,
            "average_score": average_score,
            "quality_grade": self._calculate_quality_grade(average_score),
            "last_validation": self.validation_history[-1].timestamp if self.validation_history else None
        }
    
    def _calculate_quality_grade(self, score: float) -> str:
        """Calculate quality grade based on score"""
        if score >= 95.0:
            return "A+"
        elif score >= 90.0:
            return "A"
        elif score >= 85.0:
            return "B+"
        elif score >= 80.0:
            return "B"
        elif score >= 75.0:
            return "C+"
        elif score >= 70.0:
            return "C"
        else:
            return "D"
    
    def export_quality_report(self, output_path: str = "quality_gates_report.json"):
        """Export comprehensive quality report"""
        report = {
            "timestamp": time.time(),
            "system": "Automated Quality Gates System",
            "configuration": self.config,
            "quality_summary": self.get_quality_summary(),
            "validation_history": [asdict(r) for r in self.validation_history],
            "recommendations": self._generate_system_recommendations()
        }
        
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"📊 Quality report exported to: {output_path}")
        return report
    
    def _generate_system_recommendations(self) -> List[str]:
        """Generate system-level recommendations"""
        summary = self.get_quality_summary()
        recommendations = []
        
        if summary.get("success_rate", 0) < 80.0:
            recommendations.append("Implement stricter quality controls to improve success rate")
        
        if summary.get("failed_validations", 0) > 0:
            recommendations.append("Address failed validations to meet enterprise standards")
        
        if summary.get("average_score", 0) < 85.0:
            recommendations.append("Focus on code quality improvements to achieve higher scores")
        
        if not recommendations:
            recommendations.append("System is performing well - maintain current quality standards")
        
        return recommendations


def main():
    """Run automated quality gates system"""
    print("🚀 Automated Quality Gates System")
    print("Enterprise Quality Validation")
    print("=" * 50)
    
    # Initialize quality gates
    quality_gates = AutomatedQualityGates()
    
    # Validate current directory
    current_dir = os.getcwd()
    print(f"🔍 Validating current directory: {current_dir}")
    
    # Validate directory
    directory_results = quality_gates.validate_directory(current_dir)
    
    # Display results
    print(f"\n📊 Directory Quality Results:")
    print(f"   Total Files: {directory_results['total_files']}")
    print(f"   Passed: {directory_results['passed_files']}")
    print(f"   Failed: {directory_results['failed_files']}")
    print(f"   Quality Score: {directory_results['quality_score']:.1f}%")
    
    # Get quality summary
    summary = quality_gates.get_quality_summary()
    print(f"\n🏆 Overall Quality Summary:")
    print(f"   Success Rate: {summary['success_rate']:.1f}%")
    print(f"   Average Score: {summary['average_score']:.1f}")
    print(f"   Quality Grade: {summary['quality_grade']}")
    
    # Export report
    report = quality_gates.export_quality_report()
    
    print(f"\n✅ Quality validation completed!")
    print(f"📁 Report saved to: quality_gates_report.json")
    
    return report


if __name__ == "__main__":
    import re  # Import regex for pattern matching
    main()
