"""Quickstart agent workflow demo.

This script demonstrates a minimal agent workflow using AutoDream OS services."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Agent:
    """Simple agent representation used for demonstration purposes."""

    name: str

    def greet(self) -> str:
        """Return a greeting message."""
        return f"Hello from {self.name}!"


def run_demo() -> None:
    """Run the workflow demo."""
    agent = Agent(name="DemoAgent")
    print(agent.greet())


if __name__ == "__main__":
    run_demo()
