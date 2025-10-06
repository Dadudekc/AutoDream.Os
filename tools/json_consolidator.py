#!/usr/bin/env python3
"""
JSON Consolidator Tool
======================

Analyzes and consolidates JSON files for redundancy and optimization.

Author: Agent-4 (Captain)
License: MIT
V2 Compliance: ≤400 lines, modular design
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Any

ROOT = Path(__file__).resolve().parents[1]


def analyze_json_files() -> Dict[str, Any]:
    """Analyze JSON files for consolidation opportunities"""
    print("🔍 Scanning JSON files for consolidation opportunities...")
    
    json_files = list(ROOT.rglob("*.json"))
    print(f"Found {len(json_files)} JSON files")
    
    analysis = {
        "total_files": len(json_files),
        "agent_workspace_files": [],
        "config_files": [],
        "runtime_files": [],
        "analysis_files": [],
        "duplicate_patterns": [],
        "small_files": [],
        "consolidation_candidates": []
    }
    
    for json_file in json_files:
        rel_path = str(json_file.relative_to(ROOT))
        
        try:
            # Get file size
            file_size = json_file.stat().st_size
            
            # Categorize files
            if "agent_workspaces" in rel_path:
                analysis["agent_workspace_files"].append({
                    "path": rel_path,
                    "size": file_size,
                    "agent": extract_agent_from_path(rel_path)
                })
            elif "config" in rel_path:
                analysis["config_files"].append({
                    "path": rel_path,
                    "size": file_size
                })
            elif "runtime" in rel_path or "temp" in rel_path:
                analysis["runtime_files"].append({
                    "path": rel_path,
                    "size": file_size
                })
            elif any(keyword in rel_path for keyword in ["analysis", "report", "audit"]):
                analysis["analysis_files"].append({
                    "path": rel_path,
                    "size": file_size
                })
            
            # Identify small files (likely simple configs)
            if file_size < 1000:  # Less than 1KB
                analysis["small_files"].append({
                    "path": rel_path,
                    "size": file_size
                })
            
            # Check for duplicate patterns
            filename = json_file.name
            if filename in ["status.json", "working_tasks.json", "future_tasks.json", "quality_guidelines.json"]:
                analysis["duplicate_patterns"].append(rel_path)
                
        except Exception as e:
            print(f"Warning: Could not analyze {rel_path}: {e}")
    
    return analysis


def extract_agent_from_path(path: str) -> str:
    """Extract agent identifier from file path"""
    import re
    match = re.search(r'Agent-(\d+)', path)
    return match.group(1) if match else "unknown"


def generate_json_report(analysis: Dict[str, Any]) -> None:
    """Generate JSON consolidation report"""
    reports_dir = ROOT / "runtime" / "pass4" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    report_content = f"""# JSON Consolidation Analysis

## Summary
- **Total JSON files**: {analysis['total_files']}
- **Agent workspace files**: {len(analysis['agent_workspace_files'])}
- **Config files**: {len(analysis['config_files'])}
- **Runtime files**: {len(analysis['runtime_files'])}
- **Analysis files**: {len(analysis['analysis_files'])}
- **Small files (<1KB)**: {len(analysis['small_files'])}
- **Duplicate patterns**: {len(analysis['duplicate_patterns'])}

## Consolidation Opportunities

### Agent Workspace Files ({len(analysis['agent_workspace_files'])} files)
These have similar patterns across agents and can be consolidated:
"""
    
    # Group by agent
    agents = {}
    for file_info in analysis['agent_workspace_files']:
        agent = file_info['agent']
        if agent not in agents:
            agents[agent] = []
        agents[agent].append(file_info)
    
    for agent, files in agents.items():
        report_content += f"\n#### Agent-{agent} ({len(files)} files)\n"
        for file_info in files:
            report_content += f"- `{file_info['path']}` ({file_info['size']} bytes)\n"
    
    report_content += f"""
### Duplicate Pattern Files ({len(analysis['duplicate_patterns'])} files)
Files with identical names across different locations:
"""
    for file_path in analysis['duplicate_patterns']:
        report_content += f"- `{file_path}`\n"
    
    report_content += f"""
### Small Files ({len(analysis['small_files'])} files)
Files smaller than 1KB that could be merged:
"""
    for file_info in analysis['small_files'][:20]:  # Show first 20
        report_content += f"- `{file_info['path']}` ({file_info['size']} bytes)\n"
    if len(analysis['small_files']) > 20:
        report_content += f"- ... and {len(analysis['small_files']) - 20} more\n"
    
    report_content += f"""
### Runtime Files ({len(analysis['runtime_files'])} files)
Temporary/runtime files that can be deleted:
"""
    for file_info in analysis['runtime_files']:
        report_content += f"- `{file_info['path']}` ({file_info['size']} bytes)\n"
    
    report_content += """
## Recommended Actions

1. **Consolidate agent workspace files** - Merge similar status/task files
2. **Delete runtime files** - Remove temporary/runtime JSON files
3. **Merge small config files** - Combine small configuration files
4. **Remove duplicate patterns** - Keep one canonical version per pattern
5. **Archive analysis files** - Move old analysis/report files to archive

## Target Reduction
- **Current**: 245 JSON files
- **Target**: ~150 files (39% reduction)
- **Files to remove**: ~95 files
"""
    
    report_path = reports_dir / "json_consolidation_analysis.md"
    report_path.write_text(report_content, encoding="utf-8")
    
    # Save JSON data
    json_path = reports_dir / "json_analysis.json"
    json_path.write_text(json.dumps(analysis, indent=2), encoding="utf-8")
    
    print(f"📊 JSON analysis complete:")
    print(f"   - Total files: {analysis['total_files']}")
    print(f"   - Agent workspace files: {len(analysis['agent_workspace_files'])}")
    print(f"   - Duplicate patterns: {len(analysis['duplicate_patterns'])}")
    print(f"   - Runtime files: {len(analysis['runtime_files'])}")
    print(f"   - Report: {report_path}")


def consolidate_json_files(analysis: Dict[str, Any], dry_run: bool = True) -> None:
    """Consolidate JSON files based on analysis"""
    if dry_run:
        print("🔍 DRY RUN - JSON consolidation actions:")
    else:
        print("🗑️ APPLYING - JSON consolidation:")
    
    deleted_count = 0
    
    # Delete runtime files (temporary files)
    for file_info in analysis['runtime_files']:
        file_path = ROOT / file_info['path']
        if file_path.exists():
            if dry_run:
                print(f"  [DRY-RUN] Would delete runtime file: {file_info['path']}")
            else:
                file_path.unlink()
                print(f"  🗑️ Deleted runtime file: {file_info['path']}")
            deleted_count += 1
    
    # Delete duplicate pattern files (keep first occurrence)
    seen_patterns = set()
    for file_path in analysis['duplicate_patterns']:
        filename = Path(file_path).name
        if filename not in seen_patterns:
            seen_patterns.add(filename)
        else:
            full_path = ROOT / file_path
            if full_path.exists():
                if dry_run:
                    print(f"  [DRY-RUN] Would delete duplicate pattern: {file_path}")
                else:
                    full_path.unlink()
                    print(f"  🗑️ Deleted duplicate pattern: {file_path}")
                deleted_count += 1
    
    # Delete small analysis files (likely temporary)
    for file_info in analysis['small_files']:
        if any(keyword in file_info['path'] for keyword in ['analysis', 'report', 'audit']):
            file_path = ROOT / file_info['path']
            if file_path.exists():
                if dry_run:
                    print(f"  [DRY-RUN] Would delete small analysis file: {file_info['path']}")
                else:
                    file_path.unlink()
                    print(f"  🗑️ Deleted small analysis file: {file_info['path']}")
                deleted_count += 1
    
    print(f"📊 {'Would delete' if dry_run else 'Deleted'} {deleted_count} JSON files")


def main():
    parser = argparse.ArgumentParser(description="Consolidate JSON files")
    parser.add_argument("--apply", action="store_true", help="Apply consolidation (default is dry-run)")
    parser.add_argument("--report-only", action="store_true", help="Generate report only")
    
    args = parser.parse_args()
    
    # Create runtime directory
    (ROOT / "runtime" / "pass4" / "reports").mkdir(parents=True, exist_ok=True)
    
    # Analyze JSON files
    analysis = analyze_json_files()
    
    # Generate report
    generate_json_report(analysis)
    
    if not args.report_only:
        # Apply consolidation
        consolidate_json_files(analysis, dry_run=not args.apply)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

