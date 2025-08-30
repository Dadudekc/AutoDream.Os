"""Utility functions for contract database integrity operations."""

from __future__ import annotations

import logging
from typing import Dict, Any, Iterable, Tuple, List


def setup_logging(name: str,
                  level: int = logging.INFO,
                  fmt: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s") -> logging.Logger:
    """Create and configure a logger.

    Parameters
    ----------
    name: str
        Name of the logger to create.
    level: int, optional
        Logging level to set. Defaults to :data:`logging.INFO`.
    fmt: str, optional
        Log message format string. Defaults to a simple timestamped format.

    Returns
    -------
    logging.Logger
        Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(fmt))
        logger.addHandler(handler)

    return logger


def iter_contracts(task_list: Dict[str, Any]) -> Iterable[Tuple[str, Dict[str, Any]]]:
    """Yield all contracts from a task list structure.

    Parameters
    ----------
    task_list: Dict[str, Any]
        Parsed task list JSON data.

    Yields
    ------
    Tuple[str, Dict[str, Any]]
        Pairs of category name and individual contract dictionaries.
    """
    contracts_section = task_list.get("contracts", {})
    for category, category_data in contracts_section.items():
        items = category_data.get("contracts")
        if isinstance(items, list):
            for contract in items:
                yield category, contract


def is_contract_corrupted(contract: Dict[str, Any]) -> bool:
    """Determine if a contract appears corrupted."""
    return any([
        not contract.get("contract_id"),
        not contract.get("title"),
        not contract.get("description"),
        not contract.get("status"),
        contract.get("extra_credit_points", 0) < 0,
        contract.get("estimated_time") == "INVALID_TIME",
    ])


def identify_corruption_issues(contract: Dict[str, Any]) -> List[str]:
    """List specific corruption issues for a contract."""
    issues: List[str] = []
    if not contract.get("contract_id"):
        issues.append("Missing contract ID")
    if not contract.get("title"):
        issues.append("Missing title")
    if not contract.get("description"):
        issues.append("Missing description")
    if not contract.get("status"):
        issues.append("Missing status")
    if contract.get("extra_credit_points", 0) < 0:
        issues.append("Invalid extra credit points")
    if contract.get("estimated_time") == "INVALID_TIME":
        issues.append("Invalid estimated time")
    return issues
