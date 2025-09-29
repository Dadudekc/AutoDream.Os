"""
Event Format Utilities
======================
Single-line event formatters for structured Discord logging.
"""

from datetime import UTC, datetime


def iso_now() -> str:
    """Get current UTC timestamp in ISO format."""
    return datetime.now(UTC).isoformat(timespec="seconds")


def cycle_done(agent: str, summary: str, next_intent: str) -> str:
    """
    Format cycle completion event.

    Args:
        agent: Agent identifier
        summary: What was accomplished
        next_intent: What will be done next

    Returns:
        Formatted event line
    """
    return f"CYCLE_DONE|{agent}|{summary}|{next_intent}|ts={iso_now()}"


def blocker(agent: str, reason: str, need: str, severity: str = "med") -> str:
    """
    Format blocker event.

    Args:
        agent: Agent identifier
        reason: Why blocked
        need: What is needed
        severity: Severity level (low/med/high)

    Returns:
        Formatted event line
    """
    return f"BLOCKER|{agent}|{reason}|{need}|severity={severity}|ts={iso_now()}"


def ssot_validation(agent: str, scope: str, passed: bool, notes: str = "") -> str:
    """
    Format SSOT validation event.

    Args:
        agent: Agent identifier
        scope: What was validated
        passed: Whether validation passed
        notes: Additional notes

    Returns:
        Formatted event line
    """
    pf = "pass" if passed else "fail"
    notes_part = f"|notes={notes}" if notes else ""
    return f"SSOT_VALIDATION|{agent}|{scope}|{pf}{notes_part}|ts={iso_now()}"


def integration_scan(agent: str, systems: str, depth: int, result: str) -> str:
    """
    Format integration scan event.

    Args:
        agent: Agent identifier
        systems: Systems scanned
        depth: Scan depth
        result: Scan result

    Returns:
        Formatted event line
    """
    return (
        f"INTEGRATION_SCAN|{agent}|systems={systems}|depth={depth}|result={result}|ts={iso_now()}"
    )
