"""Report generation utilities for the emergency documentation system."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
from string import Template
from typing import Any, List, Optional


def _load_template(name: str) -> Template:
    """Load a Markdown template by name."""
    template_path = Path(__file__).resolve().parent / "templates" / f"{name}.md"
    return Template(template_path.read_text())


def generate_report_content(
    emergency_id: str,
    events: List[Any],
    timeline: Optional[Any],
    validations: List[Any],
    lessons: List[Any],
) -> str:
    """Generate emergency report content from provided data."""
    template = _load_template("report")

    if events:
        event_lines = [
            f"- **{e.timestamp.strftime('%H:%M:%S')}** ["
            f"{e.severity.upper()}] {e.event_type}: {e.description}"
            for e in events
        ]
        events_section = "\n".join(event_lines)
    else:
        events_section = "No events recorded for this emergency."

    timeline_section = ""
    if timeline:
        lines = [
            "## Response Timeline",
            f"**Start Time:** {timeline.start_time.strftime('%Y-%m-%d %H:%M:%S')}",
        ]
        if getattr(timeline, "end_time", None):
            lines.append(
                f"**End Time:** {timeline.end_time.strftime('%Y-%m-%d %H:%M:%S')}"
            )
            if getattr(timeline, "duration", None):
                lines.append(f"**Duration:** {timeline.duration}")
        lines.append("")

        if getattr(timeline, "actions", None):
            lines.append("### Response Actions")
            for action in timeline.actions:
                lines.append(
                    f"- **{action['timestamp'].strftime('%H:%M:%S')}** "
                    f"{action['action']}: {action['description']}"
                )
            lines.append("")

        if getattr(timeline, "milestones", None):
            lines.append("### Key Milestones")
            for milestone in timeline.milestones:
                lines.append(
                    f"- **{milestone['timestamp'].strftime('%H:%M:%S')}** "
                    f"{milestone['milestone']}: {milestone['description']}"
                )
            lines.append("")
        timeline_section = "\n".join(lines)

    validation_section = ""
    if validations:
        lines = ["## Recovery Validation Results"]
        for validation in validations:
            lines.append(f"**Validation ID:** {validation.validation_id}")
            lines.append(
                f"**Overall Success:** {'✅ PASSED' if validation.overall_success else '❌ FAILED'}"
            )
            lines.append(
                f"**Timestamp:** {validation.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
            )
            if getattr(validation, "notes", None):
                lines.append(f"**Notes:** {validation.notes}")
            lines.append("")
        validation_section = "\n".join(lines)

    lessons_section = ""
    if lessons:
        lines = ["## Lessons Learned"]
        for lesson in lessons:
            lines.append(f"**Category:** {lesson.category}")
            lines.append(f"**Description:** {lesson.description}")
            lines.append(f"**Impact:** {lesson.impact}")
            if getattr(lesson, "recommendations", None):
                lines.append("**Recommendations:**")
                for rec in lesson.recommendations:
                    lines.append(f"- {rec}")
            lines.append(f"**Priority:** {lesson.implementation_priority.value}")
            if getattr(lesson, "assigned_to", None):
                lines.append(f"**Assigned To:** {lesson.assigned_to}")
            lines.append("")
        lessons_section = "\n".join(lines)

    return template.substitute(
        emergency_id=emergency_id,
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        events_section=events_section,
        timeline_section=timeline_section,
        validation_section=validation_section,
        lessons_section=lessons_section,
    )
