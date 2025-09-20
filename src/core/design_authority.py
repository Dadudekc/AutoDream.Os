"""
Design Authority Agent - Enforces simplicity and prevents overcomplication.
Acts as the arbiter of design decisions and keeper of project philosophy.
"""

import json
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

from .project_registry import registry_manager, get_registry, DesignPattern


class DecisionSeverity(Enum):
    """Severity levels for design decisions."""
    ERROR = "error"      # Blocks implementation
    WARNING = "warning"  # Suggests reconsideration
    INFO = "info"        # General guidance


@dataclass
class DesignReview:
    """Represents a design review decision."""
    request_id: str
    requester: str
    component_name: str
    decision: str
    context: str
    severity: DecisionSeverity
    feedback: str
    approved: bool
    timestamp: str
    alternatives: List[str] = None
    
    def __post_init__(self):
        if self.alternatives is None:
            self.alternatives = []


class DesignAuthority:
    """
    The Design Authority Agent - Enforces KISS, YAGNI, and simplicity principles.
    
    This agent doesn't write code. It only reviews plans and outputs to ensure
    they align with the project's design philosophy of simplicity and clarity.
    """
    
    def __init__(self):
        self.knowledge_base = self._load_knowledge_base()
        self.review_history: List[DesignReview] = []
    
    def _load_knowledge_base(self) -> Dict[str, Any]:
        """Load the design authority's knowledge base."""
        return {
            "principles": {
                "KISS": {
                    "description": "Keep It Simple, Stupid",
                    "guidelines": [
                        "Prefer simple functions over complex classes",
                        "Use built-in types when possible",
                        "Avoid premature abstractions",
                        "Choose clarity over cleverness"
                    ],
                    "red_flags": [
                        "complex", "advanced", "sophisticated", "enterprise",
                        "framework", "architecture", "pattern", "design"
                    ]
                },
                "YAGNI": {
                    "description": "You Aren't Gonna Need It",
                    "guidelines": [
                        "Build only what you need right now",
                        "Avoid speculative features",
                        "Start simple, add complexity when required",
                        "Prefer composition over inheritance"
                    ],
                    "red_flags": [
                        "future-proof", "extensible", "scalable", "generic",
                        "reusable", "flexible", "configurable"
                    ]
                },
                "Single_Responsibility": {
                    "description": "One component, one purpose",
                    "guidelines": [
                        "Each function should do one thing well",
                        "Separate concerns clearly",
                        "Avoid god classes or functions",
                        "Keep modules focused"
                    ],
                    "red_flags": [
                        "manager", "handler", "controller", "processor",
                        "service", "facade", "adapter"
                    ]
                }
            },
            "anti_patterns": [
                "Creating interfaces before understanding requirements",
                "Building generic solutions for specific problems",
                "Over-engineering simple data structures",
                "Premature optimization",
                "Complex inheritance hierarchies",
                "Deeply nested conditional logic",
                "Functions with too many parameters",
                "Classes with too many responsibilities"
            ],
            "preferred_alternatives": {
                "complex_class": "simple_function",
                "inheritance": "composition",
                "interface": "concrete_type",
                "factory": "direct_instantiation",
                "builder": "constructor",
                "strategy": "if_statement",
                "observer": "callback_function"
            }
        }
    
    def review_component_plan(self, requester: str, component_name: str, 
                            plan: str, context: str = "") -> DesignReview:
        """
        Review a component creation plan for simplicity violations.
        
        Args:
            requester: Agent requesting the review
            component_name: Name of the component to be created
            plan: Description of what will be implemented
            context: Additional context about the component
            
        Returns:
            DesignReview with approval status and feedback
        """
        request_id = f"REVIEW_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{component_name}"
        
        # Check for existing component
        if registry_manager.check_component_exists(component_name):
            return DesignReview(
                request_id=request_id,
                requester=requester,
                component_name=component_name,
                decision=plan,
                context=context,
                severity=DecisionSeverity.ERROR,
                feedback=f"Component '{component_name}' already exists. Check registry before creating.",
                approved=False,
                timestamp=datetime.now().isoformat(),
                alternatives=[f"Use existing component: {component_name}"]
            )
        
        # Analyze plan for violations
        violations = self._analyze_plan(plan)
        recommendations = self._generate_recommendations(plan)
        
        # Determine approval status
        error_violations = [v for v in violations if v['severity'] == DecisionSeverity.ERROR]
        approved = len(error_violations) == 0
        
        # Generate feedback
        feedback = self._generate_feedback(violations, recommendations)
        
        review = DesignReview(
            request_id=request_id,
            requester=requester,
            component_name=component_name,
            decision=plan,
            context=context,
            severity=DecisionSeverity.ERROR if not approved else DecisionSeverity.INFO,
            feedback=feedback,
            approved=approved,
            timestamp=datetime.now().isoformat(),
            alternatives=recommendations
        )
        
        self.review_history.append(review)
        return review
    
    def review_code_complexity(self, requester: str, component_name: str, 
                             code_snippet: str) -> DesignReview:
        """
        Review code for complexity violations.
        
        Args:
            requester: Agent requesting the review
            component_name: Name of the component being reviewed
            code_snippet: Code to be reviewed
            
        Returns:
            DesignReview with complexity analysis
        """
        request_id = f"COMPLEXITY_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{component_name}"
        
        # Analyze code complexity
        complexity_issues = self._analyze_code_complexity(code_snippet)
        
        # Generate feedback
        feedback = self._generate_complexity_feedback(complexity_issues)
        
        # Determine if code is too complex
        critical_issues = [issue for issue in complexity_issues if issue['severity'] == DecisionSeverity.ERROR]
        approved = len(critical_issues) == 0
        
        review = DesignReview(
            request_id=request_id,
            requester=requester,
            component_name=component_name,
            decision=f"Code complexity review for {component_name}",
            context="",
            severity=DecisionSeverity.ERROR if not approved else DecisionSeverity.INFO,
            feedback=feedback,
            approved=approved,
            timestamp=datetime.now().isoformat(),
            alternatives=self._suggest_simplifications(complexity_issues)
        )
        
        self.review_history.append(review)
        return review
    
    def _analyze_plan(self, plan: str) -> List[Dict[str, Any]]:
        """Analyze a plan for design principle violations."""
        violations = []
        plan_lower = plan.lower()
        
        # Check against knowledge base principles
        for principle_name, principle_data in self.knowledge_base["principles"].items():
            for red_flag in principle_data["red_flags"]:
                if red_flag in plan_lower:
                    violations.append({
                        'principle': principle_name,
                        'violation': f"Contains complexity indicator: '{red_flag}'",
                        'severity': DecisionSeverity.WARNING,
                        'guideline': principle_data["guidelines"][0] if principle_data["guidelines"] else ""
                    })
        
        # Check for anti-patterns
        for anti_pattern in self.knowledge_base["anti_patterns"]:
            if any(word in plan_lower for word in anti_pattern.lower().split()):
                violations.append({
                    'principle': 'Anti-Pattern',
                    'violation': anti_pattern,
                    'severity': DecisionSeverity.ERROR,
                    'guideline': "Avoid this pattern"
                })
        
        return violations
    
    def _generate_recommendations(self, plan: str) -> List[str]:
        """Generate simple alternatives to complex plans."""
        recommendations = []
        plan_lower = plan.lower()
        
        # Suggest alternatives based on preferred patterns
        for complex_pattern, simple_alternative in self.knowledge_base["preferred_alternatives"].items():
            if complex_pattern in plan_lower:
                recommendations.append(f"Consider {simple_alternative} instead of {complex_pattern}")
        
        # General simplicity recommendations
        if not recommendations:
            recommendations.extend([
                "Start with the simplest implementation that works",
                "Use built-in Python types when possible",
                "Prefer functions over classes for simple logic",
                "Avoid creating abstractions until you have multiple use cases"
            ])
        
        return recommendations
    
    def _analyze_code_complexity(self, code: str) -> List[Dict[str, Any]]:
        """Analyze code for complexity issues."""
        issues = []
        lines = code.split('\n')
        
        # Check for long functions (rough estimate by lines)
        function_lines = 0
        for line in lines:
            if line.strip().startswith('def '):
                if function_lines > 30:  # V2 compliance limit
                    issues.append({
                        'type': 'function_length',
                        'description': f"Function exceeds 30 lines ({function_lines} lines)",
                        'severity': DecisionSeverity.ERROR,
                        'line': len(lines) - function_lines
                    })
                function_lines = 0
            elif line.strip() and not line.startswith('#'):
                function_lines += 1
        
        # Check for deep nesting
        max_nesting = 0
        current_nesting = 0
        for line in lines:
            stripped = line.strip()
            if stripped.startswith(('if ', 'for ', 'while ', 'try:', 'with ')):
                current_nesting += 1
                max_nesting = max(max_nesting, current_nesting)
            elif stripped and not stripped.startswith('#') and current_nesting > 0:
                if not line.startswith(' ') and not line.startswith('\t'):
                    current_nesting = 0
        
        if max_nesting > 3:  # V2 compliance limit
            issues.append({
                'type': 'deep_nesting',
                'description': f"Nesting depth exceeds 3 levels ({max_nesting} levels)",
                'severity': DecisionSeverity.ERROR,
                'line': 'multiple'
            })
        
        # Check for too many parameters (rough estimate)
        for i, line in enumerate(lines):
            if 'def ' in line and line.count(',') > 5:  # More than 5 parameters
                issues.append({
                    'type': 'too_many_parameters',
                    'description': f"Function has too many parameters ({line.count(',') + 1} parameters)",
                    'severity': DecisionSeverity.WARNING,
                    'line': i + 1
                })
        
        return issues
    
    def _generate_feedback(self, violations: List[Dict[str, Any]], 
                          recommendations: List[str]) -> str:
        """Generate comprehensive feedback from violations and recommendations."""
        feedback_parts = []
        
        if violations:
            feedback_parts.append("🚨 Design Review Issues:")
            for violation in violations:
                severity_icon = "❌" if violation['severity'] == DecisionSeverity.ERROR else "⚠️"
                feedback_parts.append(f"{severity_icon} {violation['violation']}")
                if violation.get('guideline'):
                    feedback_parts.append(f"   💡 {violation['guideline']}")
        
        if recommendations:
            feedback_parts.append("\n💡 Recommendations:")
            for rec in recommendations[:3]:  # Limit to top 3
                feedback_parts.append(f"   • {rec}")
        
        if not violations and not recommendations:
            feedback_parts.append("✅ Plan looks good! Proceed with implementation.")
        
        return '\n'.join(feedback_parts)
    
    def _generate_complexity_feedback(self, issues: List[Dict[str, Any]]) -> str:
        """Generate feedback for code complexity issues."""
        if not issues:
            return "✅ Code complexity is acceptable."
        
        feedback_parts = ["🚨 Code Complexity Issues:"]
        
        for issue in issues:
            severity_icon = "❌" if issue['severity'] == DecisionSeverity.ERROR else "⚠️"
            feedback_parts.append(f"{severity_icon} {issue['description']}")
        
        feedback_parts.append("\n💡 Consider refactoring to reduce complexity.")
        return '\n'.join(feedback_parts)
    
    def _suggest_simplifications(self, issues: List[Dict[str, Any]]) -> List[str]:
        """Suggest specific simplifications for complexity issues."""
        suggestions = []
        
        for issue in issues:
            if issue['type'] == 'function_length':
                suggestions.append("Break the function into smaller, focused functions")
            elif issue['type'] == 'deep_nesting':
                suggestions.append("Use early returns or guard clauses to reduce nesting")
            elif issue['type'] == 'too_many_parameters':
                suggestions.append("Consider using a dataclass or dictionary for parameters")
        
        return suggestions
    
    def get_review_history(self, requester: str = None) -> List[DesignReview]:
        """Get review history, optionally filtered by requester."""
        if requester:
            return [review for review in self.review_history if review.requester == requester]
        return self.review_history
    
    def get_knowledge_summary(self) -> Dict[str, Any]:
        """Get a summary of the design authority's knowledge."""
        return {
            'principles': list(self.knowledge_base['principles'].keys()),
            'anti_patterns_count': len(self.knowledge_base['anti_patterns']),
            'total_reviews': len(self.review_history),
            'approval_rate': len([r for r in self.review_history if r.approved]) / max(len(self.review_history), 1),
            'last_updated': datetime.now().isoformat()
        }


# Global design authority instance
design_authority = DesignAuthority()


def review_component_plan(requester: str, component_name: str, plan: str, 
                         context: str = "") -> DesignReview:
    """Review a component creation plan."""
    return design_authority.review_component_plan(requester, component_name, plan, context)


def review_code_complexity(requester: str, component_name: str, code_snippet: str) -> DesignReview:
    """Review code for complexity issues."""
    return design_authority.review_code_complexity(requester, component_name, code_snippet)