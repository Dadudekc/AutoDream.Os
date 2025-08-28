"""Report generation for validation finalization."""
import logging
from datetime import datetime
from typing import Any, Dict

from .finalization_constants import (
    AGENT_NAME,
    REPORT_PATH,
    STATUS_COMPLETE,
    TASK_ID,
    TASK_NAME,
)

logger = logging.getLogger(__name__)


def _format_completion_report(report: Dict[str, Any]) -> str:
    """Format report dictionary as markdown."""
    return (
        f"# {TASK_ID} - {TASK_NAME} COMPLETED\n\n"
        f"**Agent**: {report['agent']}\n"
        f"**Completion Time**: {report['completion_timestamp']}\n"
        f"**Execution Duration**: {report['execution_time']:.2f} seconds\n\n"
        "## System Health\n"
        f"- Overall Health: {report['system_health'].get('overall_health')}\n\n"
        "## Integration Tests\n"
        f"- Status: {report['integration_tests'].get('status')}\n"
        f"- Success Rate: {report['integration_tests'].get('success_rate'):.1f}%\n\n"
        "## Performance Metrics\n"
        f"- Improvement Factor: {report['performance_metrics'].get('improvement_factor'):.1f}x\n\n"
        "## Framework Validation\n"
        f"- Status: {report['framework_validation'].get('overall_status')}\n"
    )


def generate_completion_report(data: Dict[str, Any], start_time: datetime) -> Dict[str, Any]:
    """Create and persist the finalization report."""
    completion_report = {
        "task_id": TASK_ID,
        "task_name": TASK_NAME,
        "agent": AGENT_NAME,
        "completion_timestamp": datetime.now().isoformat(),
        "execution_time": (datetime.now() - start_time).total_seconds(),
        "system_health": data["system_health"],
        "integration_tests": data["integration_tests"],
        "performance_metrics": data["performance_metrics"],
        "framework_validation": data["framework_validation"],
        "overall_status": STATUS_COMPLETE,
    }
    REPORT_PATH.parent.mkdir(exist_ok=True)
    REPORT_PATH.write_text(_format_completion_report(completion_report))
    logger.info("Completion report saved to %s", REPORT_PATH)
    return {
        "completion_report": completion_report,
        "report_path": str(REPORT_PATH),
    }
