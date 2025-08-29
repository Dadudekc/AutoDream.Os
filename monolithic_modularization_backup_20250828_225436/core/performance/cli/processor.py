#!/usr/bin/env python3
"""
Performance CLI Processor - Agent Cellphone V2
=============================================

Orchestrates CLI workflow and command execution.
Follows V2 standards: SRP, OOP principles.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import logging
import sys
from typing import Optional

from .interface import PerformanceCLIInterface
from .commands import PerformanceCLICommands


class PerformanceCLIProcessor:
    """Orchestrates CLI workflow and command execution"""
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.PerformanceCLIProcessor")
        self.interface = PerformanceCLIInterface()
        self.commands = PerformanceCLICommands()
    
    def run(self, args: Optional[list] = None) -> int:
        """
        Run the CLI with the given arguments.
        
        Args:
            args: Command line arguments (uses sys.argv if None)
            
        Returns:
            Exit code (0 for success, non-zero for failure)
        """
        try:
            # Parse arguments
            parsed_args = self.interface.parse_args(args)
            
            # Setup logging
            self.interface.setup_logging(parsed_args.verbose)
            
            # Load configuration if specified
            if parsed_args.config:
                if not self.commands.config_manager.load_config(parsed_args.config):
                    self.interface.print_error(f"Failed to load configuration from {parsed_args.config}")
                    return 1
            
            # Execute command
            if parsed_args.command == "test":
                return self.commands.run_test(parsed_args)
            elif parsed_args.command == "benchmark":
                return self.commands.run_benchmark(parsed_args)
            elif parsed_args.command == "report":
                return self.commands.run_report(parsed_args)
            elif parsed_args.command == "config":
                return self.commands.run_config(parsed_args)
            elif parsed_args.command == "status":
                return self.commands.run_status(parsed_args)
            else:
                self.interface.print_help()
                return 0
                
        except KeyboardInterrupt:
            print("\nOperation cancelled by user")
            return 130
        except Exception as e:
            self.logger.error(f"CLI execution failed: {e}")
            self.interface.print_error(f"CLI execution failed: {e}")
            return 1
    
    def execute_command(self, command: str, **kwargs) -> int:
        """
        Execute a specific command programmatically.
        
        Args:
            command: Command to execute
            **kwargs: Command arguments
            
        Returns:
            Exit code (0 for success, non-zero for failure)
        """
        try:
            # Create mock args object
            class MockArgs:
                def __init__(self, **kwargs):
                    for key, value in kwargs.items():
                        setattr(self, key, value)
            
            mock_args = MockArgs(**kwargs)
            
            # Execute command
            if command == "test":
                return self.commands.run_test(mock_args)
            elif command == "benchmark":
                return self.commands.run_benchmark(mock_args)
            elif command == "report":
                return self.commands.run_report(mock_args)
            elif command == "config":
                return self.commands.run_config(mock_args)
            elif command == "status":
                return self.commands.run_status(mock_args)
            else:
                self.logger.error(f"Unknown command: {command}")
                return 1
                
        except Exception as e:
            self.logger.error(f"Command execution failed: {e}")
            return 1
    
    def get_help(self) -> str:
        """Get help information as a string."""
        import io
        from contextlib import redirect_stdout
        
        # Capture help output
        help_output = io.StringIO()
        with redirect_stdout(help_output):
            self.interface.print_help()
        
        return help_output.getvalue()
    
    def validate_args(self, args: list) -> bool:
        """
        Validate command line arguments without executing.
        
        Args:
            args: Command line arguments
            
        Returns:
            True if valid, False otherwise
        """
        try:
            self.interface.parse_args(args)
            return True
        except Exception:
            return False
    
    def get_available_commands(self) -> list:
        """Get list of available commands."""
        return ["test", "benchmark", "report", "config", "status"]
    
    def get_command_help(self, command: str) -> str:
        """
        Get help for a specific command.
        
        Args:
            command: Command name
            
        Returns:
            Help text for the command
        """
        try:
            # Create mock args for help generation
            class MockArgs:
                def __init__(self, command_name: str):
                    self.command = command_name
            
            mock_args = MockArgs(command)
            
            # Get help from interface
            return self.interface.parser.format_help()
            
        except Exception as e:
            self.logger.error(f"Failed to get command help: {e}")
            return f"Help not available for command: {command}"
