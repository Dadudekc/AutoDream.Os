"""Dashboard rendering module."""

from __future__ import annotations

import json
from typing import Any, Dict


class DashboardRenderer:
    """Render dashboard summaries to JSON."""

    def render(self, summary: Dict[str, Any]) -> str:
        """Return a JSON string for the dashboard summary."""
        return json.dumps(summary, indent=2)
