#!/usr/bin/env python3
"""
Markdown Consolidator Tool
=========================

Scans and consolidates markdown files for duplicates and outdated content.

Author: Agent-4 (Captain)
License: MIT
V2 Compliance: ≤400 lines, modular design
"""

import argparse
import hashlib
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]


def normalize_markdown_content(content: str) -> str:
    """Normalize markdown content for comparison"""
    # Remove frontmatter
    content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
    
    # Normalize whitespace
    content = re.sub(r'\s+', ' ', content)
    
    # Remove timestamps and dates
    content = re.sub(r'\d{4}-\d{2}-\d{2}', '', content)
    content = re.sub(r'\d{2}:\d{2}:\d{2}', '', content)
    
    # Remove common variable content
    content = re.sub(r'Agent-\d+', 'Agent-X', content)
    content = re.sub(r'CUE_\w+_\d+', 'CUE_TYPE_001', content)
    
    return content.strip()


def hash_file_content(file_path: Path) -> str:
    """Generate hash of normalized markdown content"""
    try:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
        normalized = normalize_markdown_content(content)
        return hashlib.sha256(normalized.encode()).hexdigest()
    except Exception:
        return ""


def analyze_markdown_files() -> Dict[str, List[str]]:
    """Analyze markdown files for duplicates and consolidation opportunities"""
    print("🔍 Scanning markdown files for consolidation opportunities...")
    
    md_files = list(ROOT.rglob("*.md"))
    print(f"Found {len(md_files)} markdown files")
    
    # Group by content hash
    content_groups: Dict[str, List[str]] = {}
    file_analysis = {
        "duplicates": [],
        "outdated": [],
        "agent_workspace": [],
        "docs": [],
        "root_level": [],
        "consolidation_candidates": []
    }
    
    for md_file in md_files:
        rel_path = str(md_file.relative_to(ROOT))
        
        # Categorize files
        if "agent_workspaces" in rel_path:
            file_analysis["agent_workspace"].append(rel_path)
        elif "docs" in rel_path:
            file_analysis["docs"].append(rel_path)
        elif md_file.parent == ROOT:
            file_analysis["root_level"].append(rel_path)
        
        # Check for content duplicates
        content_hash = hash_file_content(md_file)
        if content_hash:
            if content_hash not in content_groups:
                content_groups[content_hash] = []
            content_groups[content_hash].append(rel_path)
    
    # Identify duplicates
    for hash_val, files in content_groups.items():
        if len(files) > 1:
            file_analysis["duplicates"].append(files)
    
    # Identify consolidation candidates
    consolidation_patterns = [
        r".*README.*\.md$",
        r".*guide.*\.md$", 
        r".*manual.*\.md$",
        r".*status.*\.md$",
        r".*report.*\.md$",
        r".*summary.*\.md$"
    ]
    
    for md_file in md_files:
        rel_path = str(md_file.relative_to(ROOT))
        for pattern in consolidation_patterns:
            if re.match(pattern, rel_path, re.IGNORECASE):
                file_analysis["consolidation_candidates"].append(rel_path)
                break
    
    return file_analysis


def generate_consolidation_report(analysis: Dict[str, List[str]]) -> None:
    """Generate markdown consolidation report"""
    reports_dir = ROOT / "runtime" / "pass4" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    report_content = f"""# Markdown Consolidation Analysis

## Summary
- **Total markdown files**: {sum(len(files) for files in analysis.values() if isinstance(files, list))}
- **Duplicate groups**: {len(analysis['duplicates'])}
- **Agent workspace files**: {len(analysis['agent_workspace'])}
- **Documentation files**: {len(analysis['docs'])}
- **Root level files**: {len(analysis['root_level'])}
- **Consolidation candidates**: {len(analysis['consolidation_candidates'])}

## Duplicate Files
"""
    
    for i, dup_group in enumerate(analysis['duplicates'], 1):
        report_content += f"\n### Group {i} ({len(dup_group)} files)\n"
        for file_path in dup_group:
            report_content += f"- `{file_path}`\n"
        report_content += f"\n**Action**: Keep `{dup_group[0]}` (canonical), delete others\n"
    
    report_content += f"""
## Consolidation Opportunities

### Agent Workspace Files ({len(analysis['agent_workspace'])} files)
These are mostly status reports and can be archived or deleted:
"""
    for file_path in analysis['agent_workspace'][:20]:  # Show first 20
        report_content += f"- `{file_path}`\n"
    if len(analysis['agent_workspace']) > 20:
        report_content += f"- ... and {len(analysis['agent_workspace']) - 20} more\n"
    
    report_content += f"""
### Consolidation Candidates ({len(analysis['consolidation_candidates'])} files)
Files that could be merged or consolidated:
"""
    for file_path in analysis['consolidation_candidates'][:20]:  # Show first 20
        report_content += f"- `{file_path}`\n"
    if len(analysis['consolidation_candidates']) > 20:
        report_content += f"- ... and {len(analysis['consolidation_candidates']) - 20} more\n"
    
    report_content += """
## Recommended Actions

1. **Delete duplicates** - Remove all but canonical versions
2. **Archive agent workspace files** - These are mostly status reports
3. **Consolidate similar docs** - Merge related documentation
4. **Remove outdated files** - Clean up superseded documentation
5. **Organize remaining docs** - Create clear documentation structure

## Target Reduction
- **Current**: 155 markdown files
- **Target**: ~80 files (48% reduction)
- **Files to remove**: ~75 files
"""
    
    report_path = reports_dir / "markdown_consolidation_analysis.md"
    report_path.write_text(report_content, encoding="utf-8")
    
    # Also save JSON data
    import json
    json_path = reports_dir / "markdown_analysis.json"
    json_path.write_text(json.dumps(analysis, indent=2), encoding="utf-8")
    
    print(f"📊 Markdown analysis complete:")
    print(f"   - Total files analyzed: {sum(len(files) for files in analysis.values() if isinstance(files, list))}")
    print(f"   - Duplicate groups: {len(analysis['duplicates'])}")
    print(f"   - Consolidation candidates: {len(analysis['consolidation_candidates'])}")
    print(f"   - Report: {report_path}")
    print(f"   - Data: {json_path}")


def consolidate_markdown_files(analysis: Dict[str, List[str]], dry_run: bool = True) -> None:
    """Consolidate markdown files based on analysis"""
    if dry_run:
        print("🔍 DRY RUN - Markdown consolidation actions:")
    else:
        print("🗑️ APPLYING - Markdown consolidation:")
    
    deleted_count = 0
    
    # Delete duplicates (keep first file as canonical)
    for dup_group in analysis['duplicates']:
        canonical = dup_group[0]
        duplicates = dup_group[1:]
        
        for dup_file in duplicates:
            file_path = ROOT / dup_file
            if file_path.exists():
                if dry_run:
                    print(f"  [DRY-RUN] Would delete duplicate: {dup_file}")
                else:
                    file_path.unlink()
                    print(f"  🗑️ Deleted duplicate: {dup_file}")
                deleted_count += 1
    
    # Delete agent workspace markdown files (mostly status reports)
    for file_path in analysis['agent_workspace']:
        full_path = ROOT / file_path
        if full_path.exists():
            if dry_run:
                print(f"  [DRY-RUN] Would delete agent workspace file: {file_path}")
            else:
                full_path.unlink()
                print(f"  🗑️ Deleted agent workspace file: {file_path}")
            deleted_count += 1
    
    print(f"📊 {'Would delete' if dry_run else 'Deleted'} {deleted_count} markdown files")


def main():
    parser = argparse.ArgumentParser(description="Consolidate markdown files")
    parser.add_argument("--apply", action="store_true", help="Apply consolidation (default is dry-run)")
    parser.add_argument("--report-only", action="store_true", help="Generate report only")
    
    args = parser.parse_args()
    
    # Create runtime directory
    (ROOT / "runtime" / "pass4" / "reports").mkdir(parents=True, exist_ok=True)
    
    # Analyze markdown files
    analysis = analyze_markdown_files()
    
    # Generate report
    generate_consolidation_report(analysis)
    
    if not args.report_only:
        # Apply consolidation
        consolidate_markdown_files(analysis, dry_run=not args.apply)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

