"""Aggregate rule evaluators for code validation."""

from typing import Any, Dict, List

from .base_validator import BaseValidator, ValidationResult
from .structure_rule_evaluator import StructureRuleEvaluator
from .content_rule_evaluator import ContentRuleEvaluator
from .metrics_rule_evaluator import MetricsRuleEvaluator
from .naming_rule_evaluator import NamingRuleEvaluator
from .complexity_rule_evaluator import ComplexityRuleEvaluator


class CodeRuleEvaluator:
    """Delegates code rule checks to specialized evaluators."""

    def __init__(
        self,
        validator: BaseValidator,
        code_standards: Dict[str, float],
        python_keywords: List[str],
    ) -> None:
        self.structure = StructureRuleEvaluator(validator)
        self.content = ContentRuleEvaluator(validator, code_standards, python_keywords)
        self.metrics = MetricsRuleEvaluator(validator, code_standards)
        self.naming = NamingRuleEvaluator(validator)
        self.complexity = ComplexityRuleEvaluator(validator, code_standards)

    def validate_code_structure(self, code_data: Dict[str, Any]) -> List[ValidationResult]:
        return self.structure.validate(code_data)

    def validate_code_content(self, content: Any, language: str = None) -> List[ValidationResult]:
        return self.content.validate(content, language)

    def validate_code_metrics(self, metrics: Any) -> List[ValidationResult]:
        return self.metrics.validate(metrics)

    def validate_naming_conventions(self, naming: Any) -> List[ValidationResult]:
        return self.naming.validate(naming)

    def validate_code_complexity(self, complexity: Any) -> List[ValidationResult]:
        return self.complexity.validate(complexity)
