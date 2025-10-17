#!/usr/bin/env python3
"""
Tests for Agent Knowledge Discovery CLI
========================================

Author: Agent-5
Date: 2025-10-17
"""

import pytest
from unittest.mock import patch, MagicMock
from tools.agent_knowledge_discovery_cli import (
    cmd_search_protocols,
    cmd_quick_ref,
    cmd_cycle_context,
    cmd_search_knowledge,
    cmd_list_resources
)


class TestSearchProtocolsCommand:
    """Tests for search protocols CLI command."""
    
    @patch('tools.agent_knowledge_discovery_cli.search_protocols')
    def test_search_with_results(self, mock_search, capsys):
        """Test search command with results."""
        mock_search.return_value = [
            {
                'title': 'Gas Pipeline Protocol',
                'file': 'swarm_brain/protocols/GAS_SYSTEM.md',
                'content': 'Send gas at 75-80% completion...',
                'relevance': 1.0
            }
        ]
        
        args = MagicMock(query='gas pipeline', agent='Agent-5')
        cmd_search_protocols(args)
        
        captured = capsys.readouterr()
        assert 'Gas Pipeline Protocol' in captured.out
        assert '1 protocols found' in captured.out
    
    @patch('tools.agent_knowledge_discovery_cli.search_protocols')
    def test_search_no_results(self, mock_search, capsys):
        """Test search with no results."""
        mock_search.return_value = []
        
        args = MagicMock(query='nonexistent', agent='Agent-5')
        cmd_search_protocols(args)
        
        captured = capsys.readouterr()
        assert 'No protocols found' in captured.out


class TestQuickRefCommand:
    """Tests for quick reference CLI command."""
    
    @patch('tools.agent_knowledge_discovery_cli.get_quick_ref')
    def test_quick_ref_valid_topic(self, mock_quick_ref, capsys):
        """Test quick ref with valid topic."""
        mock_quick_ref.return_value = "Send gas at 75-80% completion. 3-send redundancy..."
        
        args = MagicMock(topic='gas_pipeline', agent='Agent-5')
        cmd_quick_ref(args)
        
        captured = capsys.readouterr()
        assert 'GAS_PIPELINE' in captured.out
        assert 'Send gas at 75-80%' in captured.out
    
    @patch('tools.agent_knowledge_discovery_cli.get_quick_ref')
    def test_quick_ref_invalid_topic(self, mock_quick_ref, capsys):
        """Test quick ref with invalid topic."""
        mock_quick_ref.return_value = None
        
        args = MagicMock(topic='invalid', agent='Agent-5')
        cmd_quick_ref(args)
        
        captured = capsys.readouterr()
        assert 'No quick reference available' in captured.out
        assert 'Available topics' in captured.out


class TestCycleContextCommand:
    """Tests for cycle context CLI command."""
    
    @patch('tools.agent_knowledge_discovery_cli.get_cycle_context')
    def test_cycle_context_valid(self, mock_context, capsys):
        """Test cycle context with valid type."""
        mock_context.return_value = {
            'protocols': ['ANTI_STOP_PROTOCOL', 'NEVER_STOP_V2'],
            'best_practices': ['8+ cycles per session', 'Code:Celebrate = 3:1'],
            'success_metrics': {'cycles_complete': 8, 'lines_coded': 1000}
        }
        
        args = MagicMock(cycle_type='ANTI_STOP', agent='Agent-5')
        cmd_cycle_context(args)
        
        captured = capsys.readouterr()
        assert 'ANTI_STOP' in captured.out
        assert 'ANTI_STOP_PROTOCOL' in captured.out
        assert '8+ cycles per session' in captured.out
        assert 'cycles_complete: 8' in captured.out
    
    @patch('tools.agent_knowledge_discovery_cli.get_cycle_context')
    def test_cycle_context_invalid(self, mock_context, capsys):
        """Test cycle context with invalid type."""
        mock_context.return_value = {}
        
        args = MagicMock(cycle_type='INVALID', agent='Agent-5')
        cmd_cycle_context(args)
        
        captured = capsys.readouterr()
        assert 'No context available' in captured.out
        assert 'Available cycle types' in captured.out


class TestSearchKnowledgeCommand:
    """Tests for search knowledge CLI command."""
    
    @patch('tools.agent_knowledge_discovery_cli.SwarmVectorIntegration')
    def test_search_knowledge_with_results(self, mock_integration, capsys):
        """Test knowledge search with results."""
        mock_instance = MagicMock()
        mock_instance.search_swarm_knowledge.return_value = [
            {
                'source': 'swarm_brain/knowledge/validation.md',
                'type': 'knowledge',
                'content': 'Validation patterns...',
                'agent_relevant': True
            }
        ]
        mock_integration.return_value = mock_instance
        
        args = MagicMock(query='validation', agent='Agent-5')
        cmd_search_knowledge(args)
        
        captured = capsys.readouterr()
        assert 'Found 1 knowledge entries' in captured.out
        assert 'KNOWLEDGE' in captured.out


class TestListResourcesCommand:
    """Tests for list resources command."""
    
    @patch('tools.agent_knowledge_discovery_cli.get_quick_ref')
    @patch('tools.agent_knowledge_discovery_cli.get_cycle_context')
    def test_list_resources(self, mock_context, mock_quick_ref, capsys):
        """Test listing all resources."""
        mock_quick_ref.return_value = "Test reference..."
        mock_context.return_value = {
            'protocols': ['TEST_PROTOCOL'],
            'best_practices': ['Test practice']
        }
        
        args = MagicMock(agent='Agent-5')
        cmd_list_resources(args)
        
        captured = capsys.readouterr()
        assert 'QUICK REFERENCES' in captured.out
        assert 'CYCLE CONTEXTS' in captured.out
        assert 'PROTOCOL DIRECTORIES' in captured.out


class TestCLIIntegration:
    """Integration tests for CLI."""
    
    def test_cli_help(self):
        """Test CLI help output."""
        import subprocess
        result = subprocess.run(
            ['python', 'tools/agent_knowledge_discovery_cli.py', '--help'],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert 'Agent Knowledge Discovery' in result.stdout
    
    def test_cli_list_command(self):
        """Test CLI list command."""
        import subprocess
        result = subprocess.run(
            ['python', 'tools/agent_knowledge_discovery_cli.py', 'list'],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert 'QUICK REFERENCES' in result.stdout

