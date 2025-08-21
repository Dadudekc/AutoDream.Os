#!/usr/bin/env python3
"""
Intelligent Code Reviewer
Agent-2: AI & ML Framework Integration
TDD Integration Project - Agent_Cellphone_V2_Repository

AI-powered code review and quality assurance
"""
import os
import json
import logging
import ast
import re
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Any, Union, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import asyncio

from .code_crafter import CodeCrafter, CodeAnalysis
from .api_key_manager import get_openai_api_key, get_anthropic_api_key
from .utils import performance_monitor, get_config_manager

logger = logging.getLogger(__name__)

@dataclass
class ReviewIssue:
    """A code review issue"""
    severity: str  # "critical", "high", "medium", "low", "info"
    category: str  # "security", "performance", "style", "maintainability", "documentation"
    title: str
    description: str
    line_number: Optional[int] = None
    code_snippet: Optional[str] = None
    suggestion: Optional[str] = None
    cwe_id: Optional[str] = None  # Common Weakness Enumeration
    fix_priority: str = "medium"

@dataclass
class CodeReview:
    """Complete code review results"""
    file_path: str
    review_date: datetime
    overall_score: float
    issues: List[ReviewIssue] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)
    ai_insights: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)

@dataclass
class SecurityVulnerability:
    """Security vulnerability information"""
    vulnerability_type: str
    description: str
    severity: str
    cwe_id: str
    affected_code: str
    remediation: str
    references: List[str] = field(default_factory=list)

class IntelligentReviewer:
    """AI-powered intelligent code reviewer"""
    
    def __init__(self):
        self.config = get_config_manager()
        self.code_crafter = CodeCrafter()
        self.openai_key = get_openai_api_key()
        self.anthropic_key = get_anthropic_api_key()
        
        # Security patterns
        self.security_patterns = {
            "sql_injection": [
                r"execute\s*\(\s*[\"'].*\+\s*\w+",
                r"cursor\.execute\s*\(\s*[\"'].*\+\s*\w+",
                r"\.execute\s*\(\s*[\"'].*\+\s*\w+"
            ],
            "xss": [
                r"innerHTML\s*=",
                r"document\.write\s*\(",
                r"eval\s*\(",
                r"setTimeout\s*\(\s*[\"'].*\+\s*\w+"
            ],
            "path_traversal": [
                r"open\s*\(\s*[\"'].*\+\s*\w+",
                r"file\s*\(\s*[\"'].*\+\s*\w+",
                r"Path\s*\(\s*[\"'].*\+\s*\w+"
            ],
            "command_injection": [
                r"os\.system\s*\(",
                r"subprocess\.run\s*\(",
                r"subprocess\.Popen\s*\(",
                r"subprocess\.call\s*\("
            ]
        }
        
        # Code quality patterns
        self.quality_patterns = {
            "long_function": r"def\s+\w+\s*\([^)]*\):\s*\n(?:[^\n]*\n){20,}",
            "magic_numbers": r"\b\d{3,}\b",
            "hardcoded_strings": r"[\"'][^\"']{50,}[\"']",
            "nested_loops": r"for\s+.*:\s*\n\s*for\s+.*:",
            "complex_conditionals": r"if\s+.*\sand\s+.*\sand\s+.*:"
        }
    
    @performance_monitor("code_review")
    def review_code(self, file_path: Union[str, Path]) -> CodeReview:
        """
        Perform comprehensive code review
        
        Args:
            file_path: Path to the code file
            
        Returns:
            Complete code review results
        """
        file_path = Path(file_path)
        logger.info(f"Reviewing code: {file_path}")
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Initialize review
            review = CodeReview(
                file_path=str(file_path),
                review_date=datetime.now(),
                overall_score=100.0
            )
            
            # Perform various analyses
            review.issues.extend(self._security_analysis(content, file_path))
            review.issues.extend(self._quality_analysis(content, file_path))
            review.issues.extend(self._style_analysis(content, file_path))
            review.issues.extend(self._maintainability_analysis(content, file_path))
            review.issues.extend(self._documentation_analysis(content, file_path))
            
            # Calculate metrics
            review.metrics = self._calculate_metrics(content, review.issues)
            
            # Get AI insights
            review.ai_insights = self._get_ai_insights(content, review.issues)
            
            # Generate recommendations
            review.recommendations = self._generate_recommendations(review.issues, review.metrics)
            
            # Calculate overall score
            review.overall_score = self._calculate_overall_score(review.issues, review.metrics)
            
            return review
            
        except Exception as e:
            logger.error(f"Code review failed: {e}")
            raise
    
    def _security_analysis(self, content: str, file_path: Path) -> List[ReviewIssue]:
        """Analyze code for security vulnerabilities"""
        issues = []
        
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            for vuln_type, patterns in self.security_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, line, re.IGNORECASE):
                        issue = ReviewIssue(
                            severity="high" if vuln_type in ["sql_injection", "command_injection"] else "medium",
                            category="security",
                            title=f"Potential {vuln_type.replace('_', ' ').title()}",
                            description=f"Detected potential {vuln_type} vulnerability",
                            line_number=line_num,
                            code_snippet=line.strip(),
                            suggestion=f"Use parameterized queries or input validation to prevent {vuln_type}",
                            cwe_id=self._get_cwe_id(vuln_type),
                            fix_priority="high"
                        )
                        issues.append(issue)
        
        # Check for common security anti-patterns
        if "import os" in content and "os.system" in content:
            issues.append(ReviewIssue(
                severity="high",
                category="security",
                title="Command Execution Risk",
                description="Direct command execution can lead to command injection",
                suggestion="Use subprocess with proper argument handling",
                cwe_id="CWE-78",
                fix_priority="high"
            ))
        
        if "eval(" in content:
            issues.append(ReviewIssue(
                severity="critical",
                category="security",
                title="Eval Usage",
                description="eval() can execute arbitrary code",
                suggestion="Avoid eval(), use safer alternatives like ast.literal_eval()",
                cwe_id="CWE-95",
                fix_priority="critical"
            ))
        
        return issues
    
    def _quality_analysis(self, content: str, file_path: Path) -> List[ReviewIssue]:
        """Analyze code quality"""
        issues = []
        
        lines = content.split('\n')
        
        # Check for long functions
        if file_path.suffix.lower() == '.py':
            try:
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        if len(node.body) > 20:
                            issues.append(ReviewIssue(
                                severity="medium",
                                category="maintainability",
                                title="Long Function",
                                description=f"Function '{node.name}' is {len(node.body)} lines long",
                                suggestion="Consider breaking into smaller functions",
                                fix_priority="medium"
                            ))
                        
                        if len(node.args.args) > 5:
                            issues.append(ReviewIssue(
                                severity="low",
                                category="maintainability",
                                title="Too Many Parameters",
                                description=f"Function '{node.name}' has {len(node.args.args)} parameters",
                                suggestion="Consider using a configuration object or data class",
                                fix_priority="low"
                            ))
            except SyntaxError:
                pass
        
        # Check for magic numbers
        for line_num, line in enumerate(lines, 1):
            magic_numbers = re.findall(r'\b\d{3,}\b', line)
            for number in magic_numbers:
                if int(number) > 999:  # Only flag large numbers
                    issues.append(ReviewIssue(
                        severity="low",
                        category="style",
                        title="Magic Number",
                        description=f"Large magic number: {number}",
                        line_number=line_num,
                        code_snippet=line.strip(),
                        suggestion="Define as a named constant",
                        fix_priority="low"
                    ))
        
        # Check for hardcoded strings
        for line_num, line in enumerate(lines, 1):
            if len(line.strip()) > 100:
                issues.append(ReviewIssue(
                    severity="low",
                    category="style",
                    title="Long Line",
                    description="Line exceeds recommended length",
                    line_number=line_num,
                    code_snippet=line.strip()[:50] + "...",
                    suggestion="Break into multiple lines or extract to variable",
                    fix_priority="low"
                ))
        
        return issues
    
    def _style_analysis(self, content: str, file_path: Path) -> List[ReviewIssue]:
        """Analyze code style and formatting"""
        issues = []
        
        lines = content.split('\n')
        
        # Check for consistent indentation
        for line_num, line in enumerate(lines, 1):
            if line.strip() and not line.startswith('#'):
                # Check for mixed tabs and spaces
                if '\t' in line and ' ' in line[:len(line) - len(line.lstrip())]:
                    issues.append(ReviewIssue(
                        severity="low",
                        category="style",
                        title="Mixed Indentation",
                        description="Mixed tabs and spaces in indentation",
                        line_number=line_num,
                        code_snippet=line.strip(),
                        suggestion="Use consistent indentation (spaces recommended)",
                        fix_priority="low"
                    ))
        
        # Check for trailing whitespace
        for line_num, line in enumerate(lines, 1):
            if line.rstrip() != line:
                issues.append(ReviewIssue(
                    severity="low",
                    category="style",
                    title="Trailing Whitespace",
                    description="Line has trailing whitespace",
                    line_number=line_num,
                    code_snippet=line.strip(),
                    suggestion="Remove trailing whitespace",
                    fix_priority="low"
                ))
        
        # Check for proper spacing around operators
        for line_num, line in enumerate(lines, 1):
            if re.search(r'[a-zA-Z0-9_]\s*[+\-*/=<>!]\s*[a-zA-Z0-9_]', line):
                if not re.search(r'[a-zA-Z0-9_]\s+[+\-*/=<>!]\s+[a-zA-Z0-9_]', line):
                    issues.append(ReviewIssue(
                        severity="low",
                        category="style",
                        title="Operator Spacing",
                        description="Inconsistent spacing around operators",
                        line_number=line_num,
                        code_snippet=line.strip(),
                        suggestion="Add consistent spacing around operators",
                        fix_priority="low"
                    ))
        
        return issues
    
    def _maintainability_analysis(self, content: str, file_path: Path) -> List[ReviewIssue]:
        """Analyze code maintainability"""
        issues = []
        
        if file_path.suffix.lower() == '.py':
            try:
                tree = ast.parse(content)
                
                # Check cyclomatic complexity
                complexity = self._calculate_cyclomatic_complexity(tree)
                if complexity > 10:
                    issues.append(ReviewIssue(
                        severity="medium",
                        category="maintainability",
                        title="High Cyclomatic Complexity",
                        description=f"Cyclomatic complexity is {complexity} (recommended < 10)",
                        suggestion="Consider breaking complex logic into smaller functions",
                        fix_priority="medium"
                    ))
                
                # Check for deeply nested structures
                max_depth = self._calculate_max_nesting_depth(tree)
                if max_depth > 4:
                    issues.append(ReviewIssue(
                        severity="medium",
                        category="maintainability",
                        title="Deep Nesting",
                        description=f"Maximum nesting depth is {max_depth} (recommended < 4)",
                        suggestion="Extract nested logic into separate functions",
                        fix_priority="medium"
                    ))
                
                # Check for duplicate code patterns
                duplicate_patterns = self._find_duplicate_patterns(content)
                if duplicate_patterns:
                    issues.append(ReviewIssue(
                        severity="low",
                        category="maintainability",
                        title="Potential Code Duplication",
                        description=f"Found {len(duplicate_patterns)} potential duplicate patterns",
                        suggestion="Consider extracting common functionality",
                        fix_priority="low"
                    ))
                
            except SyntaxError:
                pass
        
        return issues
    
    def _documentation_analysis(self, content: str, file_path: Path) -> List[ReviewIssue]:
        """Analyze code documentation"""
        issues = []
        
        if file_path.suffix.lower() == '.py':
            try:
                tree = ast.parse(content)
                
                # Count functions and classes
                functions = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
                classes = [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
                
                # Check for missing docstrings
                documented_functions = [f for f in functions if ast.get_docstring(f)]
                documented_classes = [c for c in classes if ast.get_docstring(c)]
                
                if functions and len(documented_functions) / len(functions) < 0.8:
                    issues.append(ReviewIssue(
                        severity="low",
                        category="documentation",
                        title="Missing Function Documentation",
                        description=f"Only {len(documented_functions)}/{len(functions)} functions have docstrings",
                        suggestion="Add docstrings to all public functions",
                        fix_priority="low"
                    ))
                
                if classes and len(documented_classes) / len(classes) < 0.8:
                    issues.append(ReviewIssue(
                        severity="low",
                        category="documentation",
                        title="Missing Class Documentation",
                        description=f"Only {len(documented_classes)}/{len(classes)} classes have docstrings",
                        suggestion="Add docstrings to all classes",
                        fix_priority="low"
                    ))
                
            except SyntaxError:
                pass
        
        # Check for TODO/FIXME comments
        lines = content.split('\n')
        for line_num, line in enumerate(lines, 1):
            if re.search(r'\b(TODO|FIXME|XXX|HACK)\b', line, re.IGNORECASE):
                issues.append(ReviewIssue(
                    severity="medium",
                    category="documentation",
                    title="Development Note",
                    description=f"Found {re.search(r'\b(TODO|FIXME|XXX|HACK)\b', line, re.IGNORECASE).group(1)} comment",
                    line_number=line_num,
                    code_snippet=line.strip(),
                    suggestion="Address the TODO/FIXME or remove if resolved",
                    fix_priority="medium"
                ))
        
        return issues
    
    def _calculate_metrics(self, content: str, issues: List[ReviewIssue]) -> Dict[str, Any]:
        """Calculate code quality metrics"""
        lines = content.split('\n')
        total_lines = len(lines)
        code_lines = len([line for line in lines if line.strip() and not line.strip().startswith('#')])
        comment_lines = len([line for line in lines if line.strip().startswith('#')])
        
        # Calculate issue distribution
        issue_counts = {}
        for issue in issues:
            issue_counts[issue.severity] = issue_counts.get(issue.severity, 0) + 1
            issue_counts[f"{issue.category}_total"] = issue_counts.get(f"{issue.category}_total", 0) + 1
        
        # Calculate complexity metrics
        complexity_score = 0
        if content.strip():
            try:
                tree = ast.parse(content)
                complexity_score = self._calculate_cyclomatic_complexity(tree)
            except SyntaxError:
                complexity_score = 999
        
        return {
            "total_lines": total_lines,
            "code_lines": code_lines,
            "comment_lines": comment_lines,
            "comment_ratio": comment_lines / max(code_lines, 1),
            "complexity_score": complexity_score,
            "issue_counts": issue_counts,
            "security_issues": len([i for i in issues if i.category == "security"]),
            "quality_issues": len([i for i in issues if i.category in ["maintainability", "style"]]),
            "documentation_issues": len([i for i in issues if i.category == "documentation"])
        }
    
    def _calculate_cyclomatic_complexity(self, tree: ast.AST) -> int:
        """Calculate cyclomatic complexity for Python AST"""
        complexity = 1  # Base complexity
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(node, ast.ExceptHandler):
                complexity += 1
            elif isinstance(node, ast.With):
                complexity += 1
            elif isinstance(node, ast.Assert):
                complexity += 1
            elif isinstance(node, ast.Return):
                complexity += 1
        
        return complexity
    
    def _calculate_max_nesting_depth(self, tree: ast.AST) -> int:
        """Calculate maximum nesting depth"""
        max_depth = 0
        
        def visit_node(node, depth):
            nonlocal max_depth
            max_depth = max(max_depth, depth)
            
            for child in ast.iter_child_nodes(node):
                if isinstance(child, (ast.If, ast.For, ast.While, ast.Try, ast.With)):
                    visit_node(child, depth + 1)
                else:
                    visit_node(child, depth)
        
        visit_node(tree, 0)
        return max_depth
    
    def _find_duplicate_patterns(self, content: str) -> List[str]:
        """Find potential duplicate code patterns"""
        lines = content.split('\n')
        patterns = []
        
        # Simple pattern detection (can be enhanced with more sophisticated algorithms)
        for i in range(len(lines) - 3):
            pattern = '\n'.join(lines[i:i+3])
            if len(pattern.strip()) > 20:  # Only consider substantial patterns
                if content.count(pattern) > 1:
                    patterns.append(pattern[:100] + "...")
        
        return patterns[:5]  # Limit to 5 patterns
    
    def _get_cwe_id(self, vulnerability_type: str) -> str:
        """Get CWE ID for vulnerability type"""
        cwe_mapping = {
            "sql_injection": "CWE-89",
            "xss": "CWE-79",
            "path_traversal": "CWE-22",
            "command_injection": "CWE-78"
        }
        return cwe_mapping.get(vulnerability_type, "CWE-unknown")
    
    def _get_ai_insights(self, content: str, issues: List[ReviewIssue]) -> List[str]:
        """Get AI-powered insights about the code"""
        try:
            if self.openai_key:
                return self._get_openai_insights(content, issues)
            elif self.anthropic_key:
                return self._get_anthropic_insights(content, issues)
        except Exception as e:
            logger.warning(f"Failed to get AI insights: {e}")
        
        return []
    
    def _get_openai_insights(self, content: str, issues: List[ReviewIssue]) -> List[str]:
        """Get insights using OpenAI"""
        try:
            import openai
            
            openai.api_key = self.openai_key
            
            # Summarize issues
            issue_summary = "\n".join([f"- {i.severity.upper()}: {i.title}" for i in issues[:10]])
            
            prompt = f"""Analyze this code and provide 3-5 high-level insights:

Code (first 1000 chars):
{content[:1000]}...

Issues found:
{issue_summary}

Provide insights about:
1. Overall code quality
2. Potential improvements
3. Best practices to follow
4. Architecture considerations

Format as a JSON list of strings."""
            
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a senior software architect and code reviewer."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.3
            )
            
            content = response.choices[0].message.content
            try:
                insights = json.loads(content)
                return insights if isinstance(insights, list) else []
            except json.JSONDecodeError:
                return []
                
        except Exception as e:
            logger.warning(f"OpenAI insights failed: {e}")
            return []
    
    def _get_anthropic_insights(self, content: str, issues: List[ReviewIssue]) -> List[str]:
        """Get insights using Anthropic Claude"""
        try:
            import anthropic
            
            client = anthropic.Anthropic(api_key=self.anthropic_key)
            
            # Summarize issues
            issue_summary = "\n".join([f"- {i.severity.upper()}: {i.title}" for i in issues[:10]])
            
            prompt = f"""Analyze this code and provide 3-5 high-level insights:

Code (first 1000 chars):
{content[:1000]}...

Issues found:
{issue_summary}

Provide insights about:
1. Overall code quality
2. Potential improvements
3. Best practices to follow
4. Architecture considerations

Format as a JSON list of strings."""
            
            response = client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}]
            )
            
            content = response.content[0].text
            try:
                insights = json.loads(content)
                return insights if isinstance(insights, list) else []
            except json.JSONDecodeError:
                return []
                
        except Exception as e:
            logger.warning(f"Anthropic insights failed: {e}")
            return []
    
    def _generate_recommendations(self, issues: List[ReviewIssue], metrics: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Security recommendations
        security_issues = [i for i in issues if i.category == "security"]
        if security_issues:
            recommendations.append("Address security vulnerabilities immediately, especially high-severity ones")
        
        # Quality recommendations
        if metrics.get("complexity_score", 0) > 10:
            recommendations.append("Reduce cyclomatic complexity by breaking down complex functions")
        
        if metrics.get("comment_ratio", 0) < 0.1:
            recommendations.append("Add more documentation and comments to improve code readability")
        
        # Issue-based recommendations
        severity_counts = {}
        for issue in issues:
            severity_counts[issue.severity] = severity_counts.get(issue.severity, 0) + 1
        
        if severity_counts.get("critical", 0) > 0:
            recommendations.append("Fix critical issues first as they pose immediate risks")
        
        if severity_counts.get("high", 0) > 5:
            recommendations.append("High number of high-severity issues - consider code refactoring")
        
        if not recommendations:
            recommendations.append("Code quality is good! Keep up the good practices.")
        
        return recommendations
    
    def _calculate_overall_score(self, issues: List[ReviewIssue], metrics: Dict[str, Any]) -> float:
        """Calculate overall code quality score"""
        base_score = 100.0
        
        # Deduct points for issues
        severity_penalties = {
            "critical": 20,
            "high": 10,
            "medium": 5,
            "low": 2,
            "info": 1
        }
        
        for issue in issues:
            base_score -= severity_penalties.get(issue.severity, 0)
        
        # Deduct points for complexity
        complexity = metrics.get("complexity_score", 0)
        if complexity > 20:
            base_score -= 20
        elif complexity > 10:
            base_score -= 10
        elif complexity > 5:
            base_score -= 5
        
        # Deduct points for low documentation
        comment_ratio = metrics.get("comment_ratio", 0)
        if comment_ratio < 0.05:
            base_score -= 10
        elif comment_ratio < 0.1:
            base_score -= 5
        
        return max(0.0, base_score)
    
    def generate_review_report(self, review: CodeReview) -> str:
        """Generate a comprehensive review report"""
        report = f"# Code Review Report\n\n"
        report += f"**File:** {review.file_path}\n"
        report += f"**Date:** {review.review_date.strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += f"**Overall Score:** {review.overall_score:.1f}/100\n\n"
        
        # Summary
        report += "## 📊 Summary\n\n"
        report += f"- **Total Issues:** {len(review.issues)}\n"
        report += f"- **Security Issues:** {len([i for i in review.issues if i.category == 'security'])}\n"
        report += f"- **Quality Issues:** {len([i for i in review.issues if i.category in ['maintainability', 'style']])}\n"
        report += f"- **Documentation Issues:** {len([i for i in review.issues if i.category == 'documentation'])}\n\n"
        
        # Critical Issues
        critical_issues = [i for i in review.issues if i.severity == "critical"]
        if critical_issues:
            report += "## 🚨 Critical Issues\n\n"
            for issue in critical_issues:
                report += f"### {issue.title}\n"
                report += f"**Description:** {issue.description}\n"
                if issue.line_number:
                    report += f"**Line:** {issue.line_number}\n"
                if issue.suggestion:
                    report += f"**Suggestion:** {issue.suggestion}\n"
                report += "\n"
        
        # High Priority Issues
        high_issues = [i for i in review.issues if i.severity == "high"]
        if high_issues:
            report += "## ⚠️ High Priority Issues\n\n"
            for issue in high_issues:
                report += f"### {issue.title}\n"
                report += f"**Description:** {issue.description}\n"
                if issue.line_number:
                    report += f"**Line:** {issue.line_number}\n"
                if issue.suggestion:
                    report += f"**Suggestion:** {issue.suggestion}\n"
                report += "\n"
        
        # AI Insights
        if review.ai_insights:
            report += "## 🤖 AI Insights\n\n"
            for insight in review.ai_insights:
                report += f"- {insight}\n"
            report += "\n"
        
        # Recommendations
        if review.recommendations:
            report += "## 💡 Recommendations\n\n"
            for rec in review.recommendations:
                report += f"- {rec}\n"
            report += "\n"
        
        # Metrics
        report += "## 📈 Metrics\n\n"
        for key, value in review.metrics.items():
            if isinstance(value, float):
                report += f"- **{key.replace('_', ' ').title()}:** {value:.2f}\n"
            else:
                report += f"- **{key.replace('_', ' ').title()}:** {value}\n"
        
        return report
    
    def is_configured(self) -> bool:
        """Check if Intelligent Reviewer is properly configured"""
        return bool(self.openai_key or self.anthropic_key)

def get_intelligent_reviewer() -> IntelligentReviewer:
    """Get global Intelligent Reviewer instance"""
    if not hasattr(get_intelligent_reviewer, '_instance'):
        get_intelligent_reviewer._instance = IntelligentReviewer()
    return get_intelligent_reviewer._instance

if __name__ == "__main__":
    # Example usage
    reviewer = get_intelligent_reviewer()
    
    if reviewer.is_configured():
        print("✅ Intelligent Reviewer is configured and ready!")
        
        # Example review
        try:
            review = reviewer.review_code("src/ai_ml/code_crafter.py")
            print(f"\n🎯 Review completed!")
            print(f"Overall Score: {review.overall_score:.1f}/100")
            print(f"Total Issues: {len(review.issues)}")
            
            # Generate report
            report = reviewer.generate_review_report(review)
            print(f"\n📋 Report Preview:\n{report[:500]}...")
            
        except Exception as e:
            print(f"❌ Review failed: {e}")
    else:
        print("❌ Intelligent Reviewer not configured. Please set up API keys.")
