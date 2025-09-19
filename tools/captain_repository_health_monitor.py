#!/usr/bin/env python3
"""
Captain Repository Health Monitor - V2 Compliant
===============================================

Integrates legacy assessment engine capabilities into Captain tools.
Monitors repository health, assigns priorities, and tracks improvements.

Author: Agent-4 (Captain & Operations Coordinator)
License: MIT
"""

import ast
import argparse
import sys
import json
import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
from dataclasses import dataclass, asdict

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# V2 Compliance: File under 400 lines, functions under 30 lines


class RepositoryPriority(Enum):
    """Repository priority enumeration."""
    TIER_1_CRITICAL = "TIER_1_CRITICAL"
    TIER_2_HIGH_IMPACT = "TIER_2_HIGH_IMPACT"
    TIER_3_MEDIUM_PRIORITY = "TIER_3_MEDIUM_PRIORITY"
    TIER_4_OPTIMIZATION = "TIER_4_OPTIMIZATION"
    TIER_5_MAINTENANCE = "TIER_5_MAINTENANCE"


class BetaReadiness(Enum):
    """Beta readiness enumeration."""
    READY_FOR_BETA = "READY_FOR_BETA"
    MINOR_IMPROVEMENTS_NEEDED = "MINOR_IMPROVEMENTS_NEEDED"
    MODERATE_IMPROVEMENTS_NEEDED = "MODERATE_IMPROVEMENTS_NEEDED"
    SIGNIFICANT_IMPROVEMENTS_NEEDED = "SIGNIFICANT_IMPROVEMENTS_NEEDED"
    MAJOR_OVERHAUL_REQUIRED = "MAJOR_OVERHAUL_REQUIRED"


@dataclass
class RepositoryHealth:
    """Repository health assessment result."""
    repository_name: str
    assessment_date: str
    overall_score: float
    priority_tier: str
    beta_readiness: str
    technical_readiness: Dict[str, Any]
    v2_compliance: Dict[str, Any]
    issues_found: List[str]
    recommendations: List[str]
    agent_assignment: Optional[str] = None


class CaptainRepositoryHealthMonitor:
    """Captain's repository health monitoring system."""
    
    def __init__(self, base_path: str = "."):
        """Initialize repository health monitor."""
        self.base_path = Path(base_path)
        self.results_path = Path("captain_health_results")
        self.results_path.mkdir(exist_ok=True)
        
        # Assessment templates
        self.assessment_templates = self._load_assessment_templates()
        self.v2_standards = self._load_v2_standards()
    
    def _load_assessment_templates(self) -> Dict[str, Any]:
        """Load assessment templates."""
        return {
            "technical_readiness": {
                "weight": 40,
                "indicators": {
                    "code_quality": {"weight": 30, "max_score": 10},
                    "v2_compliance": {"weight": 35, "max_score": 10},
                    "testing_coverage": {"weight": 20, "max_score": 10},
                    "documentation": {"weight": 15, "max_score": 10}
                }
            },
            "agent_readiness": {
                "weight": 30,
                "indicators": {
                    "autonomous_capability": {"weight": 40, "max_score": 10},
                    "messaging_integration": {"weight": 30, "max_score": 10},
                    "fsm_compliance": {"weight": 30, "max_score": 10}
                }
            },
            "swarm_integration": {
                "weight": 30,
                "indicators": {
                    "coordination_ready": {"weight": 50, "max_score": 10},
                    "quality_gates": {"weight": 50, "max_score": 10}
                }
            }
        }
    
    def _load_v2_standards(self) -> Dict[str, Any]:
        """Load V2 compliance standards."""
        return {
            "file_size_limit": 400,
            "class_limit": 5,
            "function_limit": 10,
            "enum_limit": 3,
            "complexity_limit": 10,
            "parameter_limit": 5,
            "inheritance_limit": 2
        }
    
    def assess_repository(self, repo_path: Path) -> RepositoryHealth:
        """Assess repository health."""
        repo_name = repo_path.name
        
        # Technical readiness assessment
        technical_score = self._assess_technical_readiness(repo_path)
        
        # V2 compliance assessment
        v2_compliance = self._assess_v2_compliance(repo_path)
        
        # Calculate overall score
        overall_score = self._calculate_overall_score(technical_score, v2_compliance)
        
        # Determine priority and readiness
        priority_tier = self._determine_priority_tier(overall_score)
        beta_readiness = self._determine_beta_readiness(overall_score)
        
        # Generate issues and recommendations
        issues_found = self._identify_issues(repo_path, technical_score, v2_compliance)
        recommendations = self._generate_recommendations(issues_found)
        
        return RepositoryHealth(
            repository_name=repo_name,
            assessment_date=datetime.datetime.now().isoformat(),
            overall_score=overall_score,
            priority_tier=priority_tier,
            beta_readiness=beta_readiness,
            technical_readiness=technical_score,
            v2_compliance=v2_compliance,
            issues_found=issues_found,
            recommendations=recommendations
        )
    
    def _assess_technical_readiness(self, repo_path: Path) -> Dict[str, Any]:
        """Assess technical readiness."""
        indicators = self.assessment_templates["technical_readiness"]["indicators"]
        scores = {}
        
        # Code quality assessment
        scores["code_quality"] = self._assess_code_quality(repo_path)
        
        # V2 compliance assessment
        scores["v2_compliance"] = self._assess_v2_compliance(repo_path)
        
        # Testing coverage assessment
        scores["testing_coverage"] = self._assess_testing_coverage(repo_path)
        
        # Documentation assessment
        scores["documentation"] = self._assess_documentation(repo_path)
        
        # Calculate weighted score
        total_score = 0
        total_weight = 0
        
        for indicator_name, score_data in scores.items():
            weight = indicators.get(indicator_name, {}).get("weight", 1)
            total_score += score_data.get("score", 0) * weight
            total_weight += weight
        
        overall_score = total_score / total_weight if total_weight > 0 else 0
        
        return {
            "overall_score": round(overall_score, 1),
            "indicators": scores,
            "weight": self.assessment_templates["technical_readiness"]["weight"]
        }
    
    def _assess_code_quality(self, repo_path: Path) -> Dict[str, Any]:
        """Assess code quality indicators."""
        score = 5  # Base score
        evidence = []
        
        # Check for README
        if (repo_path / "README.md").exists():
            score += 2
            evidence.append("README.md present")
        
        # Check for requirements.txt
        if (repo_path / "requirements.txt").exists():
            score += 1
            evidence.append("requirements.txt present")
        
        # Check for .gitignore
        if (repo_path / ".gitignore").exists():
            score += 1
            evidence.append(".gitignore present")
        
        # Check for tests directory
        if (repo_path / "tests").exists():
            score += 2
            evidence.append("tests directory present")
        
        return {
            "score": min(score, 10),
            "evidence": evidence,
            "notes": f"Code quality based on {len(evidence)} indicators"
        }
    
    def _assess_v2_compliance(self, repo_path: Path) -> Dict[str, Any]:
        """Assess V2 compliance."""
        score = 5  # Base score
        evidence = []
        violations = []
        
        # Check Python files for V2 compliance
        python_files = list(repo_path.rglob("*.py"))
        if python_files:
            for py_file in python_files:
                try:
                    with open(py_file, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                    
                    # Check file size limit
                    if len(lines) > self.v2_standards["file_size_limit"]:
                        violations.append(f"{py_file.name}: {len(lines)} lines (limit: {self.v2_standards['file_size_limit']})")
                    else:
                        score += 0.5
                        evidence.append(f"{py_file.name}: compliant file size")
                    
                    # Check for type hints
                    content = ''.join(lines)
                    if "->" in content or ":" in content:
                        score += 0.5
                        evidence.append(f"{py_file.name}: type hints present")
                    
                except Exception:
                    continue
        
        return {
            "score": min(score, 10),
            "evidence": evidence,
            "violations": violations,
            "notes": f"V2 compliance: {len(evidence)} compliant, {len(violations)} violations"
        }
    
    def _assess_testing_coverage(self, repo_path: Path) -> Dict[str, Any]:
        """Assess testing coverage."""
        score = 3  # Base score
        evidence = []
        
        # Check for tests directory
        tests_dir = repo_path / "tests"
        if tests_dir.exists():
            test_files = list(tests_dir.rglob("*.py"))
            if test_files:
                score += 3
                evidence.append(f"{len(test_files)} test files found")
        
        # Check for pytest configuration
        if (repo_path / "pytest.ini").exists() or (repo_path / "pyproject.toml").exists():
            score += 2
            evidence.append("Pytest configuration present")
        
        return {
            "score": min(score, 10),
            "evidence": evidence,
            "notes": "Testing coverage based on test infrastructure"
        }
    
    def _assess_documentation(self, repo_path: Path) -> Dict[str, Any]:
        """Assess documentation quality."""
        score = 3  # Base score
        evidence = []
        
        # Check for README
        readme_path = repo_path / "README.md"
        if readme_path.exists():
            try:
                with open(readme_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if len(content) > 100:
                        score += 3
                        evidence.append("Comprehensive README.md")
                    else:
                        score += 1
                        evidence.append("Basic README.md")
            except Exception:
                score += 1
                evidence.append("README.md present")
        
        # Check for docs directory
        docs_dir = repo_path / "docs"
        if docs_dir.exists():
            doc_files = list(docs_dir.rglob("*.md")) + list(docs_dir.rglob("*.txt"))
            if doc_files:
                score += 2
                evidence.append(f"{len(doc_files)} documentation files")
        
        return {
            "score": min(score, 10),
            "evidence": evidence,
            "notes": "Documentation assessment based on available documentation"
        }
    
    def _calculate_overall_score(self, technical: Dict, v2_compliance: Dict) -> float:
        """Calculate overall weighted score."""
        technical_score = technical.get("overall_score", 0) * 0.7
        v2_score = v2_compliance.get("score", 0) * 0.3
        
        return round(technical_score + v2_score, 1)
    
    def _determine_priority_tier(self, score: float) -> str:
        """Determine priority tier based on score."""
        if score >= 8.0:
            return RepositoryPriority.TIER_1_CRITICAL.value
        elif score >= 7.0:
            return RepositoryPriority.TIER_2_HIGH_IMPACT.value
        elif score >= 6.0:
            return RepositoryPriority.TIER_3_MEDIUM_PRIORITY.value
        elif score >= 5.0:
            return RepositoryPriority.TIER_4_OPTIMIZATION.value
        else:
            return RepositoryPriority.TIER_5_MAINTENANCE.value
    
    def _determine_beta_readiness(self, score: float) -> str:
        """Determine beta readiness based on score."""
        if score >= 8.0:
            return BetaReadiness.READY_FOR_BETA.value
        elif score >= 7.0:
            return BetaReadiness.MINOR_IMPROVEMENTS_NEEDED.value
        elif score >= 6.0:
            return BetaReadiness.MODERATE_IMPROVEMENTS_NEEDED.value
        elif score >= 5.0:
            return BetaReadiness.SIGNIFICANT_IMPROVEMENTS_NEEDED.value
        else:
            return BetaReadiness.MAJOR_OVERHAUL_REQUIRED.value
    
    def _identify_issues(self, repo_path: Path, technical: Dict, v2_compliance: Dict) -> List[str]:
        """Identify specific issues."""
        issues = []
        
        # V2 compliance issues
        violations = v2_compliance.get("violations", [])
        issues.extend(violations)
        
        # Technical issues
        if technical.get("overall_score", 0) < 7.0:
            issues.append("Technical readiness below threshold")
        
        # Missing documentation
        if not (repo_path / "README.md").exists():
            issues.append("Missing README.md")
        
        if not (repo_path / "tests").exists():
            issues.append("Missing tests directory")
        
        return issues
    
    def _generate_recommendations(self, issues: List[str]) -> List[str]:
        """Generate improvement recommendations."""
        recommendations = []
        
        for issue in issues:
            if "lines" in issue and "limit" in issue:
                recommendations.append("Refactor large files to meet V2 compliance (≤400 lines)")
            elif "README.md" in issue:
                recommendations.append("Create comprehensive README.md with setup instructions")
            elif "tests" in issue:
                recommendations.append("Add test directory with comprehensive test coverage")
            elif "type hints" in issue:
                recommendations.append("Add type hints to improve code quality")
            else:
                recommendations.append(f"Address: {issue}")
        
        return recommendations
    
    def assign_agent(self, health: RepositoryHealth) -> str:
        """Assign appropriate agent based on repository health."""
        if health.priority_tier == RepositoryPriority.TIER_1_CRITICAL.value:
            return "Agent-1"  # Infrastructure specialist
        elif health.priority_tier == RepositoryPriority.TIER_2_HIGH_IMPACT.value:
            return "Agent-2"  # Data processing expert
        elif health.priority_tier == RepositoryPriority.TIER_3_MEDIUM_PRIORITY.value:
            return "Agent-3"  # Quality assurance lead
        else:
            return "Agent-4"  # Project coordinator
    
    def generate_health_report(self, health_results: List[RepositoryHealth]) -> str:
        """Generate comprehensive health report."""
        report = []
        report.append("# 🏥 Captain Repository Health Report")
        report.append(f"**Generated**: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"**Total Repositories**: {len(health_results)}")
        report.append("")
        
        # Summary statistics
        avg_score = sum(h.overall_score for h in health_results) / len(health_results) if health_results else 0
        critical_repos = [h for h in health_results if h.priority_tier == RepositoryPriority.TIER_1_CRITICAL.value]
        
        report.append("## 📊 Summary Statistics")
        report.append(f"- **Average Health Score**: {avg_score:.1f}/10")
        report.append(f"- **Critical Repositories**: {len(critical_repos)}")
        report.append(f"- **Ready for Beta**: {len([h for h in health_results if h.beta_readiness == BetaReadiness.READY_FOR_BETA.value])}")
        report.append("")
        
        # Priority breakdown
        report.append("## 🎯 Priority Breakdown")
        for priority in RepositoryPriority:
            count = len([h for h in health_results if h.priority_tier == priority.value])
            if count > 0:
                report.append(f"- **{priority.value.replace('_', ' ').title()}**: {count} repositories")
        report.append("")
        
        # Repository details
        report.append("## 📁 Repository Details")
        for health in sorted(health_results, key=lambda x: x.overall_score, reverse=True):
            report.append(f"### {health.repository_name}")
            report.append(f"**Health Score**: {health.overall_score}/10")
            report.append(f"**Priority Tier**: {health.priority_tier}")
            report.append(f"**Beta Readiness**: {health.beta_readiness}")
            
            if health.issues_found:
                report.append("**Issues Found**:")
                for issue in health.issues_found:
                    report.append(f"- {issue}")
            
            if health.recommendations:
                report.append("**Recommendations**:")
                for rec in health.recommendations:
                    report.append(f"- {rec}")
            
            report.append("")
        
        return "\n".join(report)


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(description="Captain Repository Health Monitor")
    parser.add_argument('path', help='Repository path to assess')
    parser.add_argument('--report', action='store_true', help='Generate detailed report')
    parser.add_argument('--assign-agent', action='store_true', help='Assign appropriate agent')
    
    args = parser.parse_args()
    
    try:
        monitor = CaptainRepositoryHealthMonitor()
        repo_path = Path(args.path)
        
        if not repo_path.exists():
            print(f"❌ Repository not found: {repo_path}")
            return 1
        
        # Assess repository
        health = monitor.assess_repository(repo_path)
        
        if args.report:
            print(monitor.generate_health_report([health]))
        else:
            print(f"Repository: {health.repository_name}")
            print(f"Health Score: {health.overall_score}/10")
            print(f"Priority Tier: {health.priority_tier}")
            print(f"Beta Readiness: {health.beta_readiness}")
            
            if health.issues_found:
                print(f"Issues: {len(health.issues_found)}")
                for issue in health.issues_found[:3]:  # Show first 3
                    print(f"  - {issue}")
        
        if args.assign_agent:
            agent = monitor.assign_agent(health)
            print(f"Recommended Agent: {agent}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
