#!/usr/bin/env python3
"""
Documentation Cleanup Tool - Archive-First Policy
==================================================

Implements 5-criteria documentation cleanup with safety guards:
- C1: Unreferenced (not linked by canonical docs or code)
- C2: Ephemeral naming patterns
- C3: Duplicative content
- C4: Legacy archive
- C5: Agent chatter outside docs/

Usage:
    python tools/cleanup_documentation.py              # Dry-run (default)
    python tools/cleanup_documentation.py --execute    # Execute archive
    python tools/cleanup_documentation.py --interactive # Interactive mode
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import tempfile
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Tuple


class DocumentationCleanup:
    """Archive-first documentation cleanup with safety guards."""

    # Preserve allowlist - canonical docs that should never be archived
    PRESERVE_ALLOWLIST = {
        "README.md",
        "AGENTS.md",
        "CONTRIBUTING.md",
        "SECURITY.md",
        "CODE_OF_CONDUCT.md",
        "CHANGELOG.md",
        "ROADMAP.md",
    }

    # Preserve patterns - paths that should never be archived
    PRESERVE_PATTERNS = [
        r"^docs/handbook/",
        r"^docs/specs/",
        r"^\.github/",
    ]

    # C2: Ephemeral naming patterns (case-insensitive)
    EPHEMERAL_PATTERN = re.compile(
        r"(outdated|temp|tmp|backup|bak|old|deprecated|"
        r"consolidation_|swarm_|survey_|notes_|scratch|playground)",
        re.IGNORECASE
    )

    # Exclude patterns for file scanning
    EXCLUDE_DIRS = {".git", "node_modules", ".venv", "__pycache__", ".archive"}

    # Documentation file extensions
    DOC_EXTENSIONS = {".md", ".rst", ".txt"}

    def __init__(self, repo_root: Path, dry_run: bool = True,
                 interactive: bool = False):
        """Initialize cleanup tool.

        Args:
            repo_root: Path to repository root
            dry_run: If True, only generate reports without archiving
            interactive: If True, prompt for confirmation on each file
        """
        self.repo_root = repo_root
        self.dry_run = dry_run
        self.interactive = interactive
        self.timestamp = datetime.now().strftime("%Y%m%d")
        self.archive_dir = repo_root / ".archive" / f"docs-{self.timestamp}"
        # Use platform-appropriate temp directory
        self.tmp_dir = Path(tempfile.gettempdir())

        # Results tracking
        self.all_docs: List[Path] = []
        self.candidates: Dict[str, List[Path]] = defaultdict(list)
        self.referenced_files: Set[Path] = set()
        self.dedup_groups: Dict[str, List[Path]] = defaultdict(list)
        self.archive_set: List[Path] = []

    def run(self) -> None:
        """Execute the cleanup process."""
        print("=" * 70)
        print("DOCUMENTATION CLEANUP - ARCHIVE-FIRST POLICY")
        print("=" * 70)
        print(f"Mode: {'DRY-RUN' if self.dry_run else 'EXECUTE'}")
        print(f"Repository: {self.repo_root}")
        print(f"Archive target: {self.archive_dir}")
        print()

        # Phase 1: Scan all documentation files
        print("[1/7] Scanning documentation files...")
        self.scan_documentation_files()
        self._write_list(self.tmp_dir / "docs_scan_all.txt", self.all_docs)
        print(f"  Found {len(self.all_docs)} documentation files")

        # Phase 2: Apply criteria C2, C4, C5
        print("\n[2/7] Applying selection criteria (C2, C4, C5)...")
        self.apply_criteria()
        all_candidates = self._flatten_candidates()
        self._write_list(self.tmp_dir / "docs_candidates_raw.txt",
                        all_candidates)
        print(f"  C2 (Ephemeral): {len(self.candidates['C2'])} files")
        print(f"  C4 (Legacy archive): {len(self.candidates['C4'])} files")
        print(f"  C5 (Agent chatter): {len(self.candidates['C5'])} files")
        print(f"  Total candidates: {len(all_candidates)} files")

        # Phase 3: Subtract preserve allowlist
        print("\n[3/7] Applying preserve allowlist...")
        filtered_candidates = self.apply_preserve_allowlist(all_candidates)
        self._write_list(self.tmp_dir / "docs_candidates.txt",
                        filtered_candidates)
        print(f"  After allowlist: {len(filtered_candidates)} files")

        # Phase 4: Reference guard (C1)
        print("\n[4/7] Applying reference guard (C1)...")
        self.scan_references(filtered_candidates)
        safe_candidates = [f for f in filtered_candidates
                          if f not in self.referenced_files]
        self._write_list(self.tmp_dir / "docs_references.txt",
                        list(self.referenced_files))
        print(f"  Referenced (skipped): {len(self.referenced_files)} files")
        print(f"  Safe candidates: {len(safe_candidates)} files")

        # Phase 5: Deduplication guard (C3)
        print("\n[5/7] Applying deduplication guard (C3)...")
        self.apply_deduplication(safe_candidates)
        self._write_list(self.tmp_dir / "docs_archive_set.txt",
                        self.archive_set)
        print(f"  Duplicates to archive: "
              f"{len(safe_candidates) - len(self.archive_set)}")
        print(f"  Final archive set: {len(self.archive_set)} files")

        # Phase 6: Generate report
        print("\n[6/7] Generating cleanup report...")
        self.generate_report()

        # Phase 7: Execute archive (if not dry-run)
        if not self.dry_run:
            print("\n[7/7] Executing archive operation...")
            self.execute_archive()
            print("\n✅ Archive operation completed successfully")
        else:
            print("\n[7/7] Skipping archive (dry-run mode)")
            print(f"\n💡 To execute: python {__file__} --execute")

        print("\n" + "=" * 70)
        print("CLEANUP COMPLETE")
        print("=" * 70)

    def scan_documentation_files(self) -> None:
        """Scan repository for all documentation files."""
        for root, dirs, files in os.walk(self.repo_root):
            # Filter out excluded directories
            dirs[:] = [d for d in dirs if d not in self.EXCLUDE_DIRS]

            root_path = Path(root)
            for file in files:
                file_path = root_path / file
                if file_path.suffix in self.DOC_EXTENSIONS:
                    # Store as relative path
                    rel_path = file_path.relative_to(self.repo_root)
                    self.all_docs.append(rel_path)

    def apply_criteria(self) -> None:
        """Apply criteria C2, C4, C5 to identify candidates."""
        for doc in self.all_docs:
            doc_str = str(doc)

            # C2: Ephemeral naming
            if self.EPHEMERAL_PATTERN.search(doc.name):
                self.candidates["C2"].append(doc)

            # C4: Legacy archive
            if doc_str.startswith("docs/archive/"):
                self.candidates["C4"].append(doc)

            # C5: Agent chatter outside docs/
            if self._is_agent_chatter(doc):
                self.candidates["C5"].append(doc)

    def _is_agent_chatter(self, doc: Path) -> bool:
        """Check if file is agent coordination/chatter."""
        doc_str = str(doc)
        patterns = [
            r"^Agent-[^/]+/.*\.md$",
            r"^agent[^/]+/.*\.md$",
            r"^runtime/.*\.md$",
            r"^agent_workspaces/.*\.md$",
            r"^thea_responses/.*\.md$",
        ]
        return any(re.match(p, doc_str, re.IGNORECASE) for p in patterns)

    def apply_preserve_allowlist(self, candidates: List[Path]) -> List[Path]:
        """Filter out files in preserve allowlist."""
        filtered = []
        for doc in candidates:
            doc_str = str(doc)

            # Check exact matches
            if doc.name in self.PRESERVE_ALLOWLIST:
                continue

            # Check pattern matches
            if any(re.match(p, doc_str) for p in self.PRESERVE_PATTERNS):
                continue

            filtered.append(doc)

        return filtered

    def scan_references(self, candidates: List[Path]) -> None:
        """Scan for references to candidates in code and canonical docs."""
        # Define reference sources
        reference_sources = []

        # Canonical docs
        for pattern in ["README.md", "AGENTS.md", "docs/**/*.md",
                       "docs/**/*.rst"]:
            reference_sources.extend(self._glob_files(pattern))

        # Source code
        for pattern in ["src/**/*.py", "src/**/*.ts", "src/**/*.js"]:
            reference_sources.extend(self._glob_files(pattern))

        # CI/Build files
        for pattern in [".github/workflows/*.yml", "Makefile",
                       "pyproject.toml", "setup.py"]:
            reference_sources.extend(self._glob_files(pattern))

        # Scan each reference source for mentions of candidates
        for candidate in candidates:
            if self._is_referenced(candidate, reference_sources):
                self.referenced_files.add(candidate)

    def _glob_files(self, pattern: str) -> List[Path]:
        """Glob files matching pattern."""
        files = []
        if "**" in pattern:
            # Recursive glob
            parts = pattern.split("**")
            base = parts[0].rstrip("/")
            suffix = parts[1].lstrip("/")
            base_path = self.repo_root / base if base else self.repo_root
            if base_path.exists():
                for path in base_path.rglob(suffix):
                    if path.is_file():
                        files.append(path.relative_to(self.repo_root))
        else:
            # Simple glob
            for path in self.repo_root.glob(pattern):
                if path.is_file():
                    files.append(path.relative_to(self.repo_root))
        return files

    def _is_referenced(self, candidate: Path,
                      sources: List[Path]) -> bool:
        """Check if candidate is referenced in any source file."""
        candidate_str = str(candidate)
        candidate_name = candidate.name

        for source in sources:
            source_path = self.repo_root / source
            if not source_path.exists():
                continue

            try:
                with open(source_path, "r", encoding="utf-8",
                         errors="ignore") as f:
                    content = f.read()
                    # Check for path or filename mention
                    if candidate_str in content or candidate_name in content:
                        return True
            except Exception:
                # Skip files that can't be read
                continue

        return False

    def apply_deduplication(self, candidates: List[Path]) -> None:
        """Apply deduplication logic (C3)."""
        # Group by normalized topic
        for candidate in candidates:
            topic = self._normalize_topic(candidate)
            self.dedup_groups[topic].append(candidate)

        # For each group, select file to keep
        for topic, files in self.dedup_groups.items():
            if len(files) <= 1:
                # No duplicates
                self.archive_set.extend(files)
                continue

            # Sort by preference: docs/** > newer mtime > root
            kept = self._select_preferred_file(files)

            # Archive the rest
            for file in files:
                if file != kept:
                    self.archive_set.append(file)

    def _normalize_topic(self, path: Path) -> str:
        """Normalize path to topic name for deduplication."""
        name = path.stem.lower()

        # Strip common prefixes
        prefixes = [
            "consolidation_", "swarm_", "survey_", "notes_",
            "draft_", "old_", "backup_", "temp_", "tmp_"
        ]
        for prefix in prefixes:
            if name.startswith(prefix):
                name = name[len(prefix):]

        # Remove numbers, dashes, underscores
        name = re.sub(r"[-_0-9]+", " ", name)
        name = name.strip()

        return name

    def _select_preferred_file(self, files: List[Path]) -> Path:
        """Select preferred file from duplicate group."""
        # Prefer docs/** files
        docs_files = [f for f in files if str(f).startswith("docs/")]
        if docs_files:
            # Among docs files, prefer newer
            return max(docs_files,
                      key=lambda f: (self.repo_root / f).stat().st_mtime)

        # Otherwise, prefer newer file
        return max(files,
                  key=lambda f: (self.repo_root / f).stat().st_mtime)

    def generate_report(self) -> None:
        """Generate summary report."""
        report = {
            "timestamp": self.timestamp,
            "mode": "dry-run" if self.dry_run else "execute",
            "summary": {
                "total_docs": len(self.all_docs),
                "candidates": {
                    "C2_ephemeral": len(self.candidates["C2"]),
                    "C4_legacy_archive": len(self.candidates["C4"]),
                    "C5_agent_chatter": len(self.candidates["C5"]),
                    "total": len(self._flatten_candidates()),
                },
                "referenced_skipped": len(self.referenced_files),
                "final_archive_set": len(self.archive_set),
            },
            "archive_set": [str(f) for f in sorted(self.archive_set)],
        }

        # Write JSON report
        report_path = self.tmp_dir / f"docs_cleanup_report_{self.timestamp}.json"
        with open(report_path, "w") as f:
            json.dump(report, f, indent=2)

        print(f"\n📊 CLEANUP SUMMARY")
        print(f"  Total docs scanned:      {report['summary']['total_docs']}")
        print(f"  Candidates identified:   "
              f"{report['summary']['candidates']['total']}")
        print(f"    - C2 (Ephemeral):      "
              f"{report['summary']['candidates']['C2_ephemeral']}")
        print(f"    - C4 (Legacy archive): "
              f"{report['summary']['candidates']['C4_legacy_archive']}")
        print(f"    - C5 (Agent chatter):  "
              f"{report['summary']['candidates']['C5_agent_chatter']}")
        print(f"  Referenced (skipped):    "
              f"{report['summary']['referenced_skipped']}")
        print(f"  Final archive set:       "
              f"{report['summary']['final_archive_set']}")
        print(f"\n📄 Report saved: {report_path}")

        # Show sample files
        if self.archive_set:
            print(f"\n📋 Sample files to archive (first 20):")
            for file in sorted(self.archive_set)[:20]:
                print(f"  - {file}")
            if len(self.archive_set) > 20:
                print(f"  ... and {len(self.archive_set) - 20} more")

    def execute_archive(self) -> None:
        """Execute archive operation with git integration."""
        if not self.archive_set:
            print("  No files to archive")
            return

        # Create archive directory
        self.archive_dir.mkdir(parents=True, exist_ok=True)

        # Generate rollback script
        rollback_script = self.archive_dir / "rollback.sh"
        rollback_lines = ["#!/bin/bash", "set -euo pipefail",
                         "# Rollback script for documentation archive\n"]

        archived_count = 0
        for file in self.archive_set:
            if self.interactive:
                response = input(f"Archive {file}? [y/N] ")
                if response.lower() != "y":
                    continue

            source = self.repo_root / file
            if not source.exists():
                print(f"  ⚠️  Skipping {file} (not found)")
                continue

            # Preserve directory structure
            dest = self.archive_dir / file
            dest.parent.mkdir(parents=True, exist_ok=True)

            # Try git mv first, fallback to shutil
            try:
                result = subprocess.run(
                    ["git", "mv", str(source), str(dest)],
                    cwd=self.repo_root,
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    archived_count += 1
                    rollback_lines.append(f"git mv {dest} {source}")
                else:
                    # File not tracked, use shutil
                    shutil.move(str(source), str(dest))
                    archived_count += 1
                    rollback_lines.append(f"mv {dest} {source}")
            except Exception as e:
                print(f"  ❌ Error archiving {file}: {e}")
                continue

        # Write rollback script
        with open(rollback_script, "w") as f:
            f.write("\n".join(rollback_lines))
        rollback_script.chmod(0o755)

        print(f"  ✅ Archived {archived_count} files")
        print(f"  📜 Rollback script: {rollback_script}")

        # Create archive manifest
        manifest = {
            "timestamp": self.timestamp,
            "archived_files": [str(f) for f in self.archive_set],
            "count": archived_count,
        }
        manifest_path = self.archive_dir / "manifest.json"
        with open(manifest_path, "w") as f:
            json.dump(manifest, f, indent=2)

        # Git commit
        try:
            subprocess.run(
                ["git", "add", str(self.archive_dir)],
                cwd=self.repo_root,
                check=True
            )
            subprocess.run(
                ["git", "commit", "-m",
                 "chore(docs): archive outdated/duplicate/ephemeral docs "
                 "per policy (archive-first, refs guarded)"],
                cwd=self.repo_root,
                check=True
            )
            print("  ✅ Changes committed to git")
        except subprocess.CalledProcessError as e:
            print(f"  ⚠️  Git commit failed: {e}")
            print("  💡 You may need to commit manually")

    def _flatten_candidates(self) -> List[Path]:
        """Flatten candidates dict to unique list."""
        all_candidates = set()
        for files in self.candidates.values():
            all_candidates.update(files)
        return sorted(all_candidates)

    def _write_list(self, path: Path, items: List[Path]) -> None:
        """Write list of paths to file."""
        with open(path, "w") as f:
            for item in sorted(items):
                f.write(f"{item}\n")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Archive-first documentation cleanup tool"
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Execute archive (default is dry-run)"
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Prompt for confirmation on each file"
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path.cwd(),
        help="Repository root directory (default: current directory)"
    )

    args = parser.parse_args()

    cleanup = DocumentationCleanup(
        repo_root=args.repo_root,
        dry_run=not args.execute,
        interactive=args.interactive
    )

    cleanup.run()


if __name__ == "__main__":
    main()

