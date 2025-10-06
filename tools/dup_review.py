#!/usr/bin/env python3
"""
Duplicate Review Tool
====================

Content-based duplicate detection with canonical file recommendations.
Generates review report for manual approval before consolidation.

Author: Agent-4 (Captain)
License: MIT
V2 Compliance: ≤400 lines, modular design
"""

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple

ROOT = Path(__file__).resolve().parents[1]


def normalize_content(text: str) -> str:
    """Normalize content for comparison"""
    lines = []
    for line in text.splitlines():
        # Skip comments and empty lines
        if line.strip().startswith('#') or not line.strip():
            continue
        # Normalize whitespace
        normalized = re.sub(r'\s+', ' ', line.strip())
        lines.append(normalized)
    return '\n'.join(lines).strip()


def hash_file(file_path: Path) -> str:
    """Generate SHA256 hash of normalized file content"""
    try:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
        normalized = normalize_content(content)
        return hashlib.sha256(normalized.encode()).hexdigest()
    except Exception:
        return ""


def find_duplicates() -> Dict[str, List[str]]:
    """Find duplicate files based on content hash"""
    scan_roots = ["src", "tools", "scripts", "config"]
    exclude_patterns = [
        "**/__pycache__/**",
        "**/.*/**",
        "**/node_modules/**",
        "**/venv/**",
        "**/.git/**",
        "**/archive/**",
        "**/backups/**"
    ]
    
    file_hashes: Dict[str, List[str]] = {}
    
    for root_name in scan_roots:
        root_path = ROOT / root_name
        if not root_path.exists():
            continue
            
        for file_path in root_path.rglob("*"):
            if not file_path.is_file():
                continue
                
            # Skip excluded files
            rel_path = str(file_path.relative_to(ROOT)).replace("\\", "/")
            if any(Path(rel_path).match(pattern) for pattern in exclude_patterns):
                continue
                
            # Only process certain file types
            if file_path.suffix.lower() not in ['.py', '.md', '.json', '.yaml', '.yml']:
                continue
                
            file_hash = hash_file(file_path)
            if file_hash:
                if file_hash not in file_hashes:
                    file_hashes[file_hash] = []
                file_hashes[file_hash].append(rel_path)
    
    # Filter to only duplicates (2+ files with same hash)
    duplicates = {h: paths for h, paths in file_hashes.items() if len(paths) > 1}
    return duplicates


def recommend_canonical(duplicate_paths: List[str]) -> str:
    """Recommend canonical file based on path hierarchy"""
    # Priority order for canonical selection
    priority_patterns = [
        r'^src/',
        r'^tools/',
        r'^config/',
        r'^scripts/'
    ]
    
    # First, try to find file in priority directories
    for pattern in priority_patterns:
        for path in duplicate_paths:
            if re.match(pattern, path):
                return path
    
    # If no priority match, use shortest path
    return min(duplicate_paths, key=len)


def generate_review_report(duplicates: Dict[str, List[str]]) -> None:
    """Generate duplicate review report"""
    reports_dir = ROOT / "runtime" / "pass3" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate JSON report
    json_report = {
        "scan_timestamp": Path(__file__).stat().st_mtime,
        "total_groups": len(duplicates),
        "duplicate_groups": []
    }
    
    for file_hash, paths in duplicates.items():
        canonical = recommend_canonical(paths)
        group = {
            "hash": file_hash,
            "canonical": canonical,
            "duplicates": [p for p in paths if p != canonical],
            "total_files": len(paths)
        }
        json_report["duplicate_groups"].append(group)
    
    json_path = reports_dir / "duplicates_review.json"
    json_path.write_text(json.dumps(json_report, indent=2), encoding="utf-8")
    
    # Generate Markdown report
    md_content = f"""# Duplicate Review Report

**Scan Date**: {Path(__file__).stat().st_mtime}
**Total Duplicate Groups**: {len(duplicates)}

## Summary
- **Total files with duplicates**: {sum(len(paths) for paths in duplicates.values())}
- **Files that can be deleted**: {sum(len(paths) - 1 for paths in duplicates.values())}
- **Potential space savings**: Significant

## Duplicate Groups

"""
    
    for i, (file_hash, paths) in enumerate(duplicates.items(), 1):
        canonical = recommend_canonical(paths)
        md_content += f"### Group {i} ({len(paths)} files)\n\n"
        md_content += f"**Recommended Canonical**: `{canonical}`\n\n"
        md_content += "**Duplicates to delete**:\n"
        
        for path in sorted(paths):
            if path == canonical:
                md_content += f"- ✅ **{path}** (KEEP - canonical)\n"
            else:
                md_content += f"- 🗑️ **{path}**\n"
        
        md_content += "\n"
    
    md_content += """## Consolidation Recommendations

1. **Review each group** - Ensure canonical file is most complete/current
2. **Update imports** - Replace references to deleted files with canonical
3. **Test functionality** - Verify no functionality lost
4. **Apply consolidation** - Use `tools/consolidation_apply.py` after approval

## Next Steps

1. Review this report carefully
2. Adjust canonical recommendations if needed
3. Run: `python tools/consolidation_apply.py --manifest runtime/pass3/reports/duplicates_review.json`
"""
    
    md_path = reports_dir / "duplicates_review.md"
    md_path.write_text(md_content, encoding="utf-8")
    
    print(f"📊 Duplicate review complete:")
    print(f"   - Groups found: {len(duplicates)}")
    print(f"   - Total duplicate files: {sum(len(paths) for paths in duplicates.values())}")
    print(f"   - Files to delete: {sum(len(paths) - 1 for paths in duplicates.values())}")
    print(f"   - JSON report: {json_path}")
    print(f"   - Markdown report: {md_path}")


def main():
    parser = argparse.ArgumentParser(description="Find and analyze duplicate files")
    parser.add_argument("--apply", action="store_true", 
                       help="Apply consolidation (requires manual review first)")
    
    args = parser.parse_args()
    
    if args.apply:
        print("⚠️  Consolidation application requires manual review first.")
        print("   1. Review runtime/pass3/reports/duplicates_review.md")
        print("   2. Adjust canonical recommendations if needed")
        print("   3. Run: python tools/consolidation_apply.py --manifest runtime/pass3/reports/duplicates_review.json")
        return 1
    
    print("🔍 Scanning for duplicate files...")
    duplicates = find_duplicates()
    
    if not duplicates:
        print("✅ No duplicates found!")
        return 0
    
    generate_review_report(duplicates)
    return 0


if __name__ == "__main__":
    sys.exit(main())

