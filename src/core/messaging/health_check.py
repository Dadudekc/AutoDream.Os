"""
Health check system for messaging systems registry.

Provides import verification and health monitoring for all registered
messaging systems to prevent silent failures and ensure system integrity.
"""

from __future__ import annotations
import logging
import sys
from typing import NamedTuple
from .registry_loader import iter_specs, resolve, SystemSpec

logger = logging.getLogger(__name__)


class HealthCheckResult(NamedTuple):
    """Result of a health check for a single system."""
    system_id: str
    system_name: str
    category: str
    critical: bool
    healthy: bool
    error_message: str | None
    status_icon: str


def check_imports() -> list[HealthCheckResult]:
    """
    Check import health for all registered messaging systems.

    Returns:
        List of HealthCheckResult objects with health status for each system
    """
    results = []

    for spec in iter_specs():
        try:
            # Attempt to resolve the system
            resolve(spec)

            # Determine status icon based on criticality and health
            if spec.critical:
                status_icon = "✅"  # Critical systems get green checkmark
            else:
                status_icon = "✓"   # Non-critical systems get simple checkmark

            result = HealthCheckResult(
                system_id=spec.id,
                system_name=spec.name,
                category=spec.category,
                critical=spec.critical,
                healthy=True,
                error_message=None,
                status_icon=status_icon
            )

        except Exception as e:
            # Determine status icon based on criticality and failure
            if spec.critical:
                status_icon = "❌"  # Critical failures get red X
            else:
                status_icon = "⚠️"  # Non-critical failures get warning

            error_msg = f"{type(e).__name__}: {str(e)}"
            result = HealthCheckResult(
                system_id=spec.id,
                system_name=spec.name,
                category=spec.category,
                critical=spec.critical,
                healthy=False,
                error_message=error_msg,
                status_icon=status_icon
            )

            logger.warning(f"Health check failed for {spec.id}: {error_msg}")

        results.append(result)

    return results


def check_critical_systems() -> list[HealthCheckResult]:
    """
    Check health for only critical messaging systems.

    Returns:
        List of HealthCheckResult objects for critical systems only
    """
    return [result for result in check_imports() if result.critical]


def assert_all_importable() -> None:
    """
    Assert that all messaging systems can be imported.

    Raises:
        SystemExit: If any critical systems fail health checks
    """
    results = check_imports()
    failures = [r for r in results if not r.healthy]

    if not failures:
        logger.info("All messaging systems passed health checks")
        return

    # Separate critical and non-critical failures
    critical_failures = [f for f in failures if f.critical]
    non_critical_failures = [f for f in failures if not f.critical]

    # Always report failures
    failure_lines = []
    for failure in failures:
        failure_lines.append(f"- {failure.status_icon} {failure.system_id}: {failure.error_message}")

    failure_report = "\n".join(failure_lines)

    # Critical failures cause system exit
    if critical_failures:
        logger.error(f"Critical messaging systems failed health checks:\n{failure_report}")
        sys.exit(1)

    # Non-critical failures are warnings
    if non_critical_failures:
        logger.warning(f"Non-critical messaging systems failed health checks:\n{failure_report}")


def get_health_summary() -> dict[str, int]:
    """
    Get a summary of health check results.

    Returns:
        Dictionary with counts of healthy/unhealthy systems by category
    """
    results = check_imports()
    summary = {
        "total": len(results),
        "healthy": len([r for r in results if r.healthy]),
        "unhealthy": len([r for r in results if not r.healthy]),
        "critical_healthy": len([r for r in results if r.critical and r.healthy]),
        "critical_unhealthy": len([r for r in results if r.critical and not r.healthy]),
    }

    # Add category breakdown
    categories = {}
    for result in results:
        if result.category not in categories:
            categories[result.category] = {"healthy": 0, "unhealthy": 0}
        if result.healthy:
            categories[result.category]["healthy"] += 1
        else:
            categories[result.category]["unhealthy"] += 1

    summary["by_category"] = categories
    return summary


def print_health_report(verbose: bool = False) -> None:
    """
    Print a formatted health report for all messaging systems.

    Args:
        verbose: If True, include detailed error messages
    """
    results = check_imports()
    summary = get_health_summary()

    print(f"\n🏥 Messaging Systems Health Report")
    print(f"Total Systems: {summary['total']}")
    print(f"Healthy: {summary['healthy']} | Unhealthy: {summary['unhealthy']}")
    print(f"Critical Systems: {summary['critical_healthy']}/{summary['critical_healthy'] + summary['critical_unhealthy']} healthy")

    if summary['unhealthy'] > 0:
        print(f"\n❌ Unhealthy Systems:")
        for result in results:
            if not result.healthy:
                print(f"  {result.status_icon} [{result.category}] {result.system_id}")
                if verbose and result.error_message:
                    print(f"    Error: {result.error_message}")

    if summary['healthy'] > 0:
        print(f"\n✅ Healthy Systems:")
        for result in results:
            if result.healthy:
                print(f"  {result.status_icon} [{result.category}] {result.system_id}")

    # Category breakdown
    print(f"\n📊 By Category:")
    for category, counts in summary["by_category"].items():
        total = counts["healthy"] + counts["unhealthy"]
        healthy_pct = (counts["healthy"] / total * 100) if total > 0 else 0
        print(f"  {category}: {counts['healthy']}/{total} ({healthy_pct:.1f}%)")
