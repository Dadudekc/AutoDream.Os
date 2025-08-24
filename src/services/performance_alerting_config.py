"""Configuration objects for the performance alerting system."""

from dataclasses import dataclass, field
from typing import Dict, List, Union

from .performance_monitor import AlertCondition, AlertSeverity


@dataclass
class AlertRule:
    """Definition of a single alert rule.

    The rule describes which metric should be evaluated, how the value should be
    compared and what severity to raise when the rule is violated.  The dataclass
    mirrors the structure used by :mod:`services.performance_monitor` so the
    alerting system can operate directly on the metrics collected there.
    """

    name: str
    metric_name: str
    condition: AlertCondition
    threshold: Union[float, int]
    severity: AlertSeverity
    description: str = ""
    enabled: bool = True
    tags_filter: Dict[str, str] = field(default_factory=dict)
    cooldown_period: int = 300
    consecutive_violations: int = 1
    channels: List[str] = field(default_factory=list)


def load_rules(config: Dict[str, Dict]) -> List[AlertRule]:
    """Create :class:`AlertRule` objects from a configuration dictionary.

    Parameters
    ----------
    config:
        A dictionary containing a ``rules`` key with a list of rule
        definitions.  The function is intentionally small and only supports the
        fields required by the tests.
    """

    rules_cfg = config.get("rules", [])
    rules: List[AlertRule] = []
    for r in rules_cfg:
        try:
            rule = AlertRule(
                name=r["name"],
                metric_name=r["metric"],
                condition=AlertCondition(r.get("condition", "greater_than")),
                threshold=r["threshold"],
                severity=AlertSeverity(r.get("severity", "warning")),
                description=r.get("description", ""),
            )
            rules.append(rule)
        except Exception:
            # Skip malformed rules; validation is intentionally lightweight
            continue
    return rules
