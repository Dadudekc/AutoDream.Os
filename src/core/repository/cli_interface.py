#!/usr/bin/env python3
"""
CLI Interface
============

Handles command-line interface operations for the repository scanner.
Keeps the main scanner focused on core functionality.

Author: Agent-1 (Performance & Health Systems)
License: MIT
"""

import argparse
from pathlib import Path
from typing import Optional

from .repository_scanner import RepositoryScanner


class CLIInterface:
    """Handles command-line interface operations"""
    
    def __init__(self, scanner: RepositoryScanner):
        """Initialize the CLI interface"""
        self.scanner = scanner

    def run(self, args: Optional[list] = None):
        """Run the CLI interface"""
        parser = argparse.ArgumentParser(description="Repository Scanner - Main Orchestrator")
        parser.add_argument("--discover", type=str, help="Discover repositories in path")
        parser.add_argument("--scan", type=str, help="Scan specific repository")
        parser.add_argument("--scan-all", type=str, help="Scan all repositories in path")
        parser.add_argument("--export", action="store_true", help="Export discovery report")
        parser.add_argument("--status", action="store_true", help="Show system status")
        parser.add_argument("--reset", action="store_true", help="Reset system")

        parsed_args = parser.parse_args(args)

        try:
            if parsed_args.discover:
                self._handle_discover(parsed_args.discover)
            elif parsed_args.scan:
                self._handle_scan(parsed_args.scan)
            elif parsed_args.scan_all:
                self._handle_scan_all(parsed_args.scan_all)
            elif parsed_args.export:
                self._handle_export()
            elif parsed_args.status:
                self._handle_status()
            elif parsed_args.reset:
                self._handle_reset()
            else:
                self._show_help()

        except Exception as e:
            print(f"❌ Operation failed: {e}")
            exit(1)

    def _handle_discover(self, path: str):
        """Handle repository discovery"""
        print(f"🔍 Discovering repositories in: {path}")
        repositories = self.scanner.discovery_engine.discover_repositories(path)
        print(f"✅ Discovered {len(repositories)} repositories:")
        for repo in repositories[:10]:  # Show first 10
            print(f"  - {repo}")
        if len(repositories) > 10:
            print(f"  ... and {len(repositories) - 10} more")

    def _handle_scan(self, path: str):
        """Handle single repository scan"""
        print(f"🔍 Scanning repository: {path}")
        metadata = self.scanner.scan_repository(path, deep_scan=True)
        if metadata:
            print(f"✅ Repository scan completed:")
            print(f"  Name: {metadata.name}")
            print(f"  Language: {metadata.technology_stack.get('language', 'unknown')}")
            print(f"  Health Score: {metadata.health_score}/100")
            print(f"  Market Readiness: {metadata.market_readiness}/100")
        else:
            print("❌ Repository scan failed")

    def _handle_scan_all(self, path: str):
        """Handle scanning all repositories in a path"""
        print(f"🔍 Scanning all repositories in: {path}")
        results = self.scanner.discover_and_scan(path)
        if results:
            print(f"✅ Scanned {len(results)} repositories")
            summary = self.scanner.report_generator.get_discovery_summary()
            if "error" not in summary:
                print(f"📊 Summary: {summary['total_repositories']} repos, "
                      f"Avg Health: {summary['average_health_score']:.1f}/100")
        else:
            print("❌ No repositories found to scan")

    def _handle_export(self):
        """Handle report export"""
        if self.scanner.report_generator.repositories:
            output_file = self.scanner.export_comprehensive_report()
            if output_file:
                print(f"📄 Report exported to: {output_file}")
            else:
                print("❌ Failed to export report")
        else:
            print("❌ No repositories to export. Run discovery first.")

    def _handle_status(self):
        """Handle system status display"""
        status = self.scanner.get_system_status()
        if "error" not in status:
            print(f"📊 System Status:")
            print(f"  Scanner: {status['scanner_status']}")
            print(f"  Cache Size: {status['scan_cache_size']}")
            print(f"  History Count: {status['scan_history_count']}")
        else:
            print(f"❌ Error getting status: {status['error']}")

    def _handle_reset(self):
        """Handle system reset"""
        self.scanner.reset_system()
        print("🔄 System reset completed")

    def _show_help(self):
        """Show help information"""
        print("🔍 Repository Scanner - Main Orchestrator ready")
        print("Use --discover <path> to discover repositories")
        print("Use --scan <path> to scan a specific repository")
        print("Use --scan-all <path> to scan all repositories in a path")
        print("Use --export to export discovery report")
        print("Use --status to show system status")
        print("Use --reset to reset system")

