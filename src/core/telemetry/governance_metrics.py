#!/usr/bin/env python3
"""
Governance Metrics - Prometheus Counters (Optional)
"""

from __future__ import annotations

from typing import Optional

try:
    from prometheus_client import Counter  # type: ignore
except Exception:  # pragma: no cover - optional dep
    Counter = None  # type: ignore


_switch_total: Optional[object] = None
_validation_fail_total: Optional[object] = None


def _counter(name: str, desc: str):  # pragma: no cover - thin wrapper
    if Counter is None:
        return None
    return Counter(name, desc)


def init_metrics() -> None:
    global _switch_total, _validation_fail_total
    if _switch_total is None:
        _switch_total = _counter("governance_mode_switch_total", "Total successful mode switches")
    if _validation_fail_total is None:
        _validation_fail_total = _counter("governance_validation_fail_total", "Total validation failures for mode switch")


def inc_switch() -> None:  # pragma: no cover - optional
    if _switch_total is not None:
        _switch_total.inc()  # type: ignore


def inc_validation_fail() -> None:  # pragma: no cover - optional
    if _validation_fail_total is not None:
        _validation_fail_total.inc()  # type: ignore

