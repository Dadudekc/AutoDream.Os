#!/usr/bin/env python3
"""
Comprehensive Tool Runtime Audit
================================

Tests tools by actually running them to identify runtime failures.

USAGE:
    python tools/comprehensive_tool_runtime_audit.py
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime
import json


class RuntimeAuditor:
    """Tests tools by running them"""
    
    def __init__(self):
        self.results = {
            'cli_working': [],
            'cli_broken': [],
            'library_only': [],
            'untestable': []
        }
        self.detailed_errors = []
    
    def is_cli_tool(self, file_path: Path) -> bool:
        """Check if file is a CLI tool"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            return any([
                'if __name__ == "__main__"' in content,
                'argparse.ArgumentParser' in content,
                'def main(' in content and 'if __name__' in content
            ])
        except:
            return False
    
    def test_cli_tool(self, file_path: Path) -> dict:
        """Test CLI tool with --help"""
        try:
            result = subprocess.run(
                [sys.executable, str(file_path), '--help'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            # Success if: exit 0, or help text shown, or specific error codes
            if result.returncode == 0:
                return {'works': True, 'output': 'Help OK'}
            elif 'usage:' in result.stdout.lower() or 'usage:' in result.stderr.lower():
                return {'works': True, 'output': 'Help shown'}
            elif result.returncode == 2:  # Common argparse error code
                return {'works': True, 'output': 'Argparse working'}
            else:
                error = result.stderr.strip()[:300] if result.stderr else 'Unknown'
                return {'works': False, 'error': error}
        
        except subprocess.TimeoutExpired:
            return {'works': False, 'error': 'Timeout (>5s)'}
        except Exception as e:
            return {'works': False, 'error': str(e)[:300]}
    
    def audit_directory(self, directory: Path):
        """Audit all Python files"""
        print(f"\n🔍 Auditing CLI tools in: {directory}\n")
        
        python_files = list(directory.rglob("*.py"))
        python_files = [
            f for f in python_files 
            if '__pycache__' not in str(f) and 'test_' not in f.name
        ]
        
        cli_tools = [f for f in python_files if self.is_cli_tool(f)]
        
        print(f"Found {len(python_files)} Python files")
        print(f"Identified {len(cli_tools)} CLI tools\n")
        print(f"Testing CLI tools:\n")
        
        for idx, tool in enumerate(cli_tools, 1):
            rel_path = str(tool)
            print(f"[{idx}/{len(cli_tools)}] {tool.name}...", end=" ")
            
            result = self.test_cli_tool(tool)
            
            if result['works']:
                self.results['cli_working'].append(rel_path)
                print(f"✅ {result['output']}")
            else:
                self.results['cli_broken'].append(rel_path)
                self.detailed_errors.append({
                    'file': rel_path,
                    'error': result['error']
                })
                print(f"❌ BROKEN")
                if len(result['error']) < 100:
                    print(f"    Error: {result['error']}")
    
    def generate_report(self) -> str:
        """Generate report"""
        working = len(self.results['cli_working'])
        broken = len(self.results['cli_broken'])
        total = working + broken
        
        report = f"""# 🔍 TOOL RUNTIME AUDIT REPORT

**Date:** {datetime.utcnow().isoformat()}Z  
**Audited By:** Agent-3 (Infrastructure & DevOps)

## 📊 SUMMARY

**CLI Tools Tested:** {total}  
**Working:** {working} ({working/total*100 if total > 0 else 0:.1f}%)  
**Broken:** {broken} ({broken/total*100 if total > 0 else 0:.1f}%)

---

## ❌ BROKEN TOOLS ({broken} total)

"""
        
        for item in self.detailed_errors:
            report += f"### `{Path(item['file']).name}`\n"
            report += f"**Path:** {item['file']}  \n"
            report += f"**Error:** {item['error'][:200]}  \n\n"
        
        report += f"""

---

## ✅ WORKING TOOLS ({working} total)

"""
        for tool in sorted(self.results['cli_working'])[:30]:
            report += f"- `{Path(tool).name}`\n"
        
        if len(self.results['cli_working']) > 30:
            report += f"\n... and {len(self.results['cli_working']) - 30} more\n"
        
        report += "\n---\n\n## 🎯 RECOMMENDATION\n\n"
        
        if broken > 0:
            report += f"Move {broken} broken tools to `tools_quarantine/` for systematic fixing.\n"
        else:
            report += "All CLI tools are functional! ✅\n"
        
        return report


def main():
    auditor = RuntimeAuditor()
    
    print("="*70)
    print("🔍 COMPREHENSIVE TOOL RUNTIME AUDIT")
    print("="*70)
    
    # Audit tools
    auditor.audit_directory(Path("tools"))
    
    # Audit tools_v2
    if Path("tools_v2").exists():
        auditor.audit_directory(Path("tools_v2"))
    
    # Generate report
    print("\n" + "="*70)
    print("📊 GENERATING REPORT")
    print("="*70 + "\n")
    
    report = auditor.generate_report()
    
    # Save
    with open("TOOL_RUNTIME_AUDIT_REPORT.md", 'w') as f:
        f.write(report)
    
    # Save JSON
    with open("BROKEN_TOOLS_MANIFEST.json", 'w') as f:
        json.dump({
            'audit_date': datetime.utcnow().isoformat() + 'Z',
            'broken_tools': auditor.detailed_errors,
            'summary': {
                'total': len(auditor.results['cli_working']) + len(auditor.results['cli_broken']),
                'working': len(auditor.results['cli_working']),
                'broken': len(auditor.results['cli_broken'])
            }
        }, f, indent=2)
    
    # Summary
    working = len(auditor.results['cli_working'])
    broken = len(auditor.results['cli_broken'])
    total = working + broken
    
    print(f"Total CLI Tools: {total}")
    print(f"✅ Working: {working}")
    print(f"❌ Broken: {broken}")
    print(f"\n✅ Reports saved:")
    print(f"   - TOOL_RUNTIME_AUDIT_REPORT.md")
    print(f"   - BROKEN_TOOLS_MANIFEST.json")
    
    if broken > 0:
        print(f"\n🚨 {broken} broken tools identified for quarantine!")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

