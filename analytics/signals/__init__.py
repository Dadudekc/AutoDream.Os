"""
CI Signal Collectors
===================

Signal harvesters for CI artifacts (coverage, test results, lint).
"""

from .collect_ci_signals import collect, parse_pytest_summary

__all__ = ["collect", "parse_pytest_summary"]
