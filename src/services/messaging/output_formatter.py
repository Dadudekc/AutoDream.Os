"""Utility helpers for formatting CLI output."""

from __future__ import annotations

from typing import Any, Dict


class OutputFormatter:
    """Provides helper methods for consistent CLI output formatting."""

    def validation_results(self, results: Dict[str, Any]) -> None:
        print("\U0001F4C8 Coordinate Validation Results:")
        for key, value in results.items():
            print(f"  {key}: {value}")

    def mapping_results(self, summary: Dict[str, Any]) -> None:
        print("\U0001F4CA Summary:")
        for key, value in summary.items():
            print(f"  {key}: {value}")

    def generic_results(
        self, title: str, results: Dict[str, bool], high_priority: bool = False
    ) -> None:
        print(title)
        for key, success in results.items():
            if high_priority:
                status = (
                    "\U0001F6A8 HIGH PRIORITY Success"
                    if success
                    else "\u274C HIGH PRIORITY Failed"
                )
            else:
                status = "\u2705 Success" if success else "\u274C Failed"
            print(f"  {key}: {status}")
