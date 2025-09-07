"""Distribution utilities for emergency documentation."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def save_document_to_file(base_path: Path, document: Any) -> None:
    """Persist a document dataclass to the filesystem."""
    type_dir = {
        "event_log": "events",
        "response_timeline": "timelines",
        "recovery_validation": "validations",
        "lessons_learned": "lessons",
    }.get(getattr(document, "document_type").value, "reports")

    file_path = base_path / type_dir / f"{document.document_id}.json"

    doc_data = {
        "document_id": document.document_id,
        "document_type": document.document_type.value,
        "title": document.title,
        "content": document.content,
        "created_at": document.created_at.isoformat(),
        "updated_at": document.updated_at.isoformat(),
        "author": document.author,
        "priority": document.priority.value,
        "tags": document.tags,
        "related_emergencies": document.related_emergencies,
    }

    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w") as f:
        json.dump(doc_data, f, indent=2)

    document.file_path = str(file_path)
