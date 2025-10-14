#!/usr/bin/env python3
"""
Task CLI - Quick Task Management
================================

Simplified interface for common task operations.
Wraps messaging_cli task system for easy access.

Author: Agent-8 (Quality Assurance) - Thread Experience Tool
Created: 2025-10-14
"""

import argparse
import subprocess
import sys
from pathlib import Path


def run_messaging_cli(args: list[str]) -> int:
    """Run messaging CLI with given arguments."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "src.services.messaging_cli"] + args,
            cwd=Path(__file__).parent.parent,
            capture_output=True,
            text=True
        )
        
        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        
        return result.returncode
        
    except Exception as e:
        print(f"Error: {e}")
        return 1


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Task CLI - Quick task management"
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Get next task
    get_parser = subparsers.add_parser('get', help='Get next task')
    get_parser.add_argument('--agent', required=True, help='Agent ID (e.g., Agent-8)')
    
    # List tasks
    list_parser = subparsers.add_parser('list', help='List all tasks')
    
    # Check status
    status_parser = subparsers.add_parser('status', help='Check task status')
    status_parser.add_argument('task_id', help='Task ID to check')
    
    # Complete task
    complete_parser = subparsers.add_parser('complete', help='Mark task complete')
    complete_parser.add_argument('task_id', help='Task ID to complete')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Map to messaging_cli commands
    if args.command == 'get':
        return run_messaging_cli(['--get-next-task', '--agent', args.agent])
    
    elif args.command == 'list':
        return run_messaging_cli(['--list-tasks'])
    
    elif args.command == 'status':
        return run_messaging_cli(['--task-status', args.task_id])
    
    elif args.command == 'complete':
        return run_messaging_cli(['--complete-task', args.task_id])
    
    return 1


if __name__ == "__main__":
    sys.exit(main())

