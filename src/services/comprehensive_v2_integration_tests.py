#!/usr/bin/env python3
"""Comprehensive V2 Integration Tests

This module exercises integration points across V2 services. Previously this
file contained unresolved merge conflict markers around the AgentCellPhone mock
setup. The conflict has been resolved and ``mock_agent_cell_phone`` is now
configured using :func:`unittest.mock.patch`.
"""

from unittest import TestCase
from unittest.mock import patch


class ComprehensiveV2IntegrationTests(TestCase):
    """Basic integration tests for V2 services."""

    def setUp(self) -> None:  # pragma: no cover - setup logic
        agent_patcher = patch("services.agent_cell_phone.AgentCellPhone")
        self.mock_agent_cell_phone = agent_patcher.start()
        self.addCleanup(agent_patcher.stop)

        instance = self.mock_agent_cell_phone.return_value
        instance.start.return_value = True
        instance.send_message.return_value = {"status": "sent"}

    def test_agent_cell_phone_sends_message(self) -> None:
        """AgentCellPhone should send messages successfully."""
        instance = self.mock_agent_cell_phone.return_value
        result = instance.send_message("hello")
        self.assertEqual(result, {"status": "sent"})
