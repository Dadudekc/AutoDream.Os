#!/usr/bin/env python3
"""
V2 Compliance Code Quality Tools Installation - Tool Installation System
======================================================================

This module handles the installation and setup of code quality tools
for V2 compliance standards.

**Author:** Agent-5 (SPRINT ACCELERATION REFACTORING TOOL PREPARATION MANAGER)
**Contract:** V2-COMPLIANCE-003 - V2 Compliance Code Quality Implementation Modularization
**Status:** MODULARIZATION IN PROGRESS
**Target:** ≤250 lines per module, single responsibility principle
**V2 Compliance:** ✅ Under 250 lines, focused responsibility
"""

import os
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime


class V2ComplianceToolInstaller:
    """V2 compliance code quality tools installation system."""
    
    def __init__(self):
        """Initialize tool installer."""
        self.quality_tools = {
            'black': 'black',
            'flake8': 'flake8',
            'isort': 'isort',
            'autopep8': 'autopep8',
            'pre-commit': 'pre-commit'
        }
        self.installation_status = {}
        self.installation_results = {}
    
    def install_quality_tools(self) -> Dict[str, Any]:
        """Install required code quality tools."""
        print("🔧 INSTALLING: Code quality tools for V2 compliance...")
        
        results = {
            'tools_installed': 0,
            'tools_failed': 0,
            'installation_log': [],
            'status': 'active'
        }
        
        for tool_name, package_name in self.quality_tools.items():
            try:
                print(f"📦 Installing {tool_name}...")
                
                # Install using pip
                result = subprocess.run([
                    sys.executable, '-m', 'pip', 'install', package_name
                ], capture_output=True, text=True, check=True)
                
                if result.returncode == 0:
                    results['tools_installed'] += 1
                    self.installation_status[tool_name] = 'installed'
                    results['installation_log'].append(f"✅ {tool_name} installed successfully")
                    print(f"✅ {tool_name} installed successfully")
                else:
                    results['tools_failed'] += 1
                    self.installation_status[tool_name] = 'failed'
                    results['installation_log'].append(f"❌ {tool_name} installation failed")
                    print(f"❌ {tool_name} installation failed")
                    
            except subprocess.CalledProcessError as e:
                results['tools_failed'] += 1
                self.installation_status[tool_name] = 'failed'
                error_msg = f"❌ {tool_name} installation error: {e}"
                results['installation_log'].append(error_msg)
                print(error_msg)
            except Exception as e:
                results['tools_failed'] += 1
                self.installation_status[tool_name] = 'failed'
                error_msg = f"❌ {tool_name} installation exception: {e}"
                results['installation_log'].append(error_msg)
                print(error_msg)
        
        print(f"✅ INSTALLATION COMPLETE: {results['tools_installed']} tools installed, {results['tools_failed']} failed")
        self.installation_results = results
        return results
    
    def verify_tool_installation(self, tool_name: str) -> bool:
        """Verify that a specific tool is properly installed."""
        try:
            if tool_name == 'black':
                result = subprocess.run(['black', '--version'], capture_output=True, text=True)
            elif tool_name == 'flake8':
                result = subprocess.run(['flake8', '--version'], capture_output=True, text=True)
            elif tool_name == 'isort':
                result = subprocess.run(['isort', '--version'], capture_output=True, text=True)
            elif tool_name == 'autopep8':
                result = subprocess.run(['autopep8', '--version'], capture_output=True, text=True)
            elif tool_name == 'pre-commit':
                result = subprocess.run(['pre-commit', '--version'], capture_output=True, text=True)
            else:
                return False
            
            return result.returncode == 0
        except Exception:
            return False
    
    def get_installation_status(self) -> Dict[str, str]:
        """Get the current installation status of all tools."""
        return self.installation_status.copy()
    
    def get_installation_summary(self) -> Dict[str, Any]:
        """Get a summary of the installation results."""
        return {
            'total_tools': len(self.quality_tools),
            'installed_tools': len([s for s in self.installation_status.values() if s == 'installed']),
            'failed_tools': len([s for s in self.installation_status.values() if s == 'failed']),
            'success_rate': len([s for s in self.installation_status.values() if s == 'installed']) / len(self.quality_tools) * 100,
            'status': self.installation_results.get('status', 'unknown')
        }
    
    def list_available_tools(self) -> List[str]:
        """List all available quality tools."""
        return list(self.quality_tools.keys())
    
    def add_custom_tool(self, tool_name: str, package_name: str) -> bool:
        """Add a custom quality tool to the installation list."""
        try:
            self.quality_tools[tool_name] = package_name
            return True
        except Exception:
            return False
    
    def remove_tool(self, tool_name: str) -> bool:
        """Remove a tool from the installation list."""
        try:
            if tool_name in self.quality_tools:
                del self.quality_tools[tool_name]
                if tool_name in self.installation_status:
                    del self.installation_status[tool_name]
                return True
            return False
        except Exception:
            return False
    
    def export_installation_report(self, output_path: str = None) -> str:
        """Export installation report to JSON file."""
        if not output_path:
            output_path = f"v2_compliance_tools_installation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'installation_summary': self.get_installation_summary(),
            'installation_status': self.installation_status,
            'installation_log': self.installation_results.get('installation_log', [])
        }
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            return output_path
        except Exception as e:
            print(f"❌ ERROR: Could not export installation report: {e}")
            return ""


if __name__ == "__main__":
    # Test the tool installer
    installer = V2ComplianceToolInstaller()
    results = installer.install_quality_tools()
    print(f"Installation Results: {results}")
