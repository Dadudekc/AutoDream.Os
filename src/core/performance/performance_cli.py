#!/usr/bin/env python3
"""
Performance CLI Orchestrator - Agent Cellphone V2
================================================

Orchestrates performance CLI workflow using extracted modules.
Follows V2 standards: ≤400 LOC, SRP, OOP principles.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import sys
from typing import Optional

from .cli.processor import PerformanceCLIProcessor


class PerformanceCLIOrchestrator:
    """Orchestrates performance CLI workflow using extracted modules"""
    
    def __init__(self):
        self.processor = PerformanceCLIProcessor()
    
    def run(self, args: Optional[list] = None) -> int:
        """
        Run the CLI with the given arguments.
        
        Args:
            args: Command line arguments (uses sys.argv if None)
            
        Returns:
            Exit code (0 for success, non-zero for failure)
        """
        return self.processor.run(args)
    
    def execute_command(self, command: str, **kwargs) -> int:
        """
        Execute a specific command programmatically.
        
        Args:
            command: Command to execute
            **kwargs: Command arguments
            
        Returns:
            Exit code (0 for success, non-zero for failure)
        """
        return self.processor.execute_command(command, **kwargs)
    
    def get_help(self) -> str:
        """Get help information as a string."""
        return self.processor.get_help()
    
    def validate_args(self, args: list) -> bool:
        """
        Validate command line arguments without executing.
        
        Args:
            args: Command line arguments
            
        Returns:
            True if valid, False otherwise
        """
        return self.processor.validate_args(args)
    
    def get_available_commands(self) -> list:
        """Get list of available commands."""
        return self.processor.get_available_commands()
    
    def get_command_help(self, command: str) -> str:
        """
        Get help for a specific command.
        
        Args:
            command: Command name
            
        Returns:
            Help text for the command
        """
        return self.processor.get_command_help(command)


# Backward compatibility - maintain existing interface
class PerformanceValidationCLI(PerformanceCLIOrchestrator):
    """Backward compatibility alias for existing code"""
    pass


def main():
    """Main entry point for the CLI."""
    cli = PerformanceCLIOrchestrator()
    exit_code = cli.run()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
