"""
KISS Principle Enforcement System - V2 Compliant (Simplified)
============================================================

Core KISS principle enforcement with essential functionality only.
Eliminates overcomplexity while maintaining core features.

V2 Compliance: < 400 lines, single responsibility
Author: Agent-1 (Integration Specialist)
License: MIT
"""
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum
from dataclasses import dataclass, field
import threading

logger = logging.getLogger(__name__)


class ComplexityLevel(Enum):
    """Complexity level enumeration."""
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    OVERCOMPLEX = "overcomplex"


@dataclass
class ComplexityMetric:
    """Complexity metric structure."""
    component_name: str
    complexity_level: ComplexityLevel
    line_count: int
    enum_count: int
    class_count: int
    method_count: int
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class SimplicityRule:
    """Simplicity rule structure."""
    rule_name: str
    max_lines: int = 400
    max_enums: int = 3
    max_classes: int = 5
    max_methods: int = 10
    enabled: bool = True


class ComplexityAnalyzer:
    """Core complexity analyzer."""
    
    def __init__(self):
        self._metrics: Dict[str, ComplexityMetric] = {}
        self._rules: Dict[str, SimplicityRule] = {}
        self._violations: List[Dict[str, Any]] = []
        self._lock = threading.Lock()
    
    def add_rule(self, rule: SimplicityRule) -> None:
        """Add a simplicity rule."""
        with self._lock:
            self._rules[rule.rule_name] = rule
            logger.debug(f"Simplicity rule added: {rule.rule_name}")
    
    def analyze_component(self, component_name: str, line_count: int, 
                         enum_count: int, class_count: int, method_count: int) -> ComplexityMetric:
        """Analyze component complexity."""
        # Determine complexity level
        if line_count <= 200 and enum_count <= 2 and class_count <= 3 and method_count <= 5:
            level = ComplexityLevel.SIMPLE
        elif line_count <= 400 and enum_count <= 3 and class_count <= 5 and method_count <= 10:
            level = ComplexityLevel.MODERATE
        elif line_count <= 600 and enum_count <= 5 and class_count <= 8 and method_count <= 15:
            level = ComplexityLevel.COMPLEX
        else:
            level = ComplexityLevel.OVERCOMPLEX
        
        metric = ComplexityMetric(
            component_name=component_name,
            complexity_level=level,
            line_count=line_count,
            enum_count=enum_count,
            class_count=class_count,
            method_count=method_count
        )
        
        with self._lock:
            self._metrics[component_name] = metric
            logger.debug(f"Component analyzed: {component_name} - {level.value}")
        
        return metric
    
    def get_metric(self, component_name: str) -> Optional[ComplexityMetric]:
        """Get complexity metric."""
        return self._metrics.get(component_name)
    
    def get_all_metrics(self) -> Dict[str, ComplexityMetric]:
        """Get all complexity metrics."""
        return self._metrics.copy()
    
    def get_overcomplex_components(self) -> List[str]:
        """Get overcomplex components."""
        return [name for name, metric in self._metrics.items() 
                if metric.complexity_level == ComplexityLevel.OVERCOMPLEX]
    
    def check_compliance(self, component_name: str, rule_name: str) -> bool:
        """Check compliance with a rule."""
        if component_name not in self._metrics or rule_name not in self._rules:
            return False
        
        metric = self._metrics[component_name]
        rule = self._rules[rule_name]
        
        violations = []
        
        if metric.line_count > rule.max_lines:
            violations.append(f"Line count {metric.line_count} exceeds limit {rule.max_lines}")
        
        if metric.enum_count > rule.max_enums:
            violations.append(f"Enum count {metric.enum_count} exceeds limit {rule.max_enums}")
        
        if metric.class_count > rule.max_classes:
            violations.append(f"Class count {metric.class_count} exceeds limit {rule.max_classes}")
        
        if metric.method_count > rule.max_methods:
            violations.append(f"Method count {metric.method_count} exceeds limit {rule.max_methods}")
        
        if violations:
            violation = {
                'component': component_name,
                'rule': rule_name,
                'violations': violations,
                'timestamp': datetime.now()
            }
            with self._lock:
                self._violations.append(violation)
            return False
        
        return True
    
    def get_violations(self) -> List[Dict[str, Any]]:
        """Get compliance violations."""
        return self._violations.copy()
    
    def clear_violations(self) -> None:
        """Clear compliance violations."""
        with self._lock:
            self._violations.clear()
            logger.info("Compliance violations cleared")


class SimplicityEnforcer:
    """Simplicity enforcement system."""
    
    def __init__(self):
        self._analyzer = ComplexityAnalyzer()
        self._enabled = True
        
        # Add default V2 compliance rules
        self._analyzer.add_rule(SimplicityRule(
            rule_name="v2_compliance",
            max_lines=400,
            max_enums=3,
            max_classes=5,
            max_methods=10
        ))
    
    def enable(self) -> None:
        """Enable simplicity enforcement."""
        self._enabled = True
        logger.info("Simplicity enforcement enabled")
    
    def disable(self) -> None:
        """Disable simplicity enforcement."""
        self._enabled = False
        logger.info("Simplicity enforcement disabled")
    
    def is_enabled(self) -> bool:
        """Check if simplicity enforcement is enabled."""
        return self._enabled
    
    def get_analyzer(self) -> ComplexityAnalyzer:
        """Get complexity analyzer."""
        return self._analyzer
    
    def enforce_simplicity(self, component_name: str, line_count: int, 
                          enum_count: int, class_count: int, method_count: int) -> Dict[str, Any]:
        """Enforce simplicity rules."""
        if not self._enabled:
            return {'success': True, 'message': 'Simplicity enforcement disabled'}
        
        # Analyze component
        metric = self._analyzer.analyze_component(
            component_name, line_count, enum_count, class_count, method_count
        )
        
        # Check compliance
        compliant = self._analyzer.check_compliance(component_name, "v2_compliance")
        
        result = {
            'success': compliant,
            'component': component_name,
            'complexity_level': metric.complexity_level.value,
            'metrics': {
                'line_count': metric.line_count,
                'enum_count': metric.enum_count,
                'class_count': metric.class_count,
                'method_count': metric.method_count
            },
            'message': 'Component is simple and compliant' if compliant else 'Component violates simplicity rules'
        }
        
        if not compliant:
            violations = self._analyzer.get_violations()
            result['violations'] = [v for v in violations if v['component'] == component_name]
        
        logger.info(f"Simplicity enforcement: {component_name} - {'COMPLIANT' if compliant else 'VIOLATION'}")
        return result
    
    def get_simplicity_report(self) -> Dict[str, Any]:
        """Get simplicity report."""
        metrics = self._analyzer.get_all_metrics()
        violations = self._analyzer.get_violations()
        overcomplex = self._analyzer.get_overcomplex_components()
        
        total_components = len(metrics)
        compliant_components = total_components - len(violations)
        
        return {
            'total_components': total_components,
            'compliant_components': compliant_components,
            'violating_components': len(violations),
            'overcomplex_components': len(overcomplex),
            'compliance_rate': (compliant_components / total_components * 100) if total_components > 0 else 100,
            'violations': violations,
            'overcomplex_components': overcomplex,
            'last_check': datetime.now()
        }


class KISSManager:
    """KISS principle manager."""
    
    def __init__(self):
        self._enforcer = SimplicityEnforcer()
        self._recommendations: List[str] = []
    
    def get_enforcer(self) -> SimplicityEnforcer:
        """Get simplicity enforcer."""
        return self._enforcer
    
    def add_recommendation(self, recommendation: str) -> None:
        """Add a simplicity recommendation."""
        self._recommendations.append(recommendation)
        logger.debug(f"Recommendation added: {recommendation}")
    
    def get_recommendations(self) -> List[str]:
        """Get simplicity recommendations."""
        return self._recommendations.copy()
    
    def clear_recommendations(self) -> None:
        """Clear recommendations."""
        self._recommendations.clear()
        logger.info("Recommendations cleared")
    
    def generate_simplicity_recommendations(self, component_name: str) -> List[str]:
        """Generate simplicity recommendations for a component."""
        metric = self._enforcer.get_analyzer().get_metric(component_name)
        if not metric:
            return []
        
        recommendations = []
        
        if metric.line_count > 400:
            recommendations.append(f"Reduce {component_name} from {metric.line_count} to ≤400 lines")
        
        if metric.enum_count > 3:
            recommendations.append(f"Reduce enums in {component_name} from {metric.enum_count} to ≤3")
        
        if metric.class_count > 5:
            recommendations.append(f"Reduce classes in {component_name} from {metric.class_count} to ≤5")
        
        if metric.method_count > 10:
            recommendations.append(f"Reduce methods in {component_name} from {metric.method_count} to ≤10")
        
        if metric.complexity_level == ComplexityLevel.OVERCOMPLEX:
            recommendations.append(f"Simplify {component_name} - currently overcomplex")
        
        return recommendations


# Global KISS manager
kiss_manager = KISSManager()


def get_kiss_manager() -> KISSManager:
    """Get the global KISS manager."""
    return kiss_manager


def enforce_simplicity(component_name: str, line_count: int, enum_count: int, 
                      class_count: int, method_count: int) -> Dict[str, Any]:
    """Enforce simplicity rules."""
    return kiss_manager.get_enforcer().enforce_simplicity(
        component_name, line_count, enum_count, class_count, method_count
    )
