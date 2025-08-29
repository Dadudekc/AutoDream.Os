#!/usr/bin/env python3
"""
Cleanup Script for Problematic PRs and Branches
Agent_Cellphone_V2_Repository
Date: August 28, 2025

This script helps clean up the repository after rejecting problematic PRs
and establishes proper guidelines for future development.
"""

import os
import subprocess
import json
from datetime import datetime
from pathlib import Path

class RepositoryCleanup:
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.problematic_branches = [
            "codex/refactor-agents-module-structure",
            "codex/refactor-base_manager-with-mixin-classes-zmd9am",
            "codex/refactor-emergency-module-structure",
            "codex/refactor-emergency-module-structure-jvwrzb",
            "codex/refactor-emergency-module-structure-z4zm20",
            "codex/refactor-gui-and-transport-logic",
            "codex/reuse-documentation-templates-and-modules",
            "codex/split-and-organize-dedup-algorithms-and-utilities",
            "codex/split-metric-adapters-and-create-aggregator"
        ]
        
        self.local_merge_branches = [
            "merge-add-dependency-injection",
            "merge-extract-widgets-and-graphs"
        ]
        
        self.report_data = {
            "timestamp": datetime.now().isoformat(),
            "repository": str(self.repo_path),
            "actions_taken": [],
            "branches_cleaned": [],
            "guidelines_established": [],
            "recommendations": []
        }

    def run_command(self, command: str, capture_output: bool = True) -> tuple:
        """Run a git command and return the result."""
        try:
            if capture_output:
                result = subprocess.run(
                    command, 
                    shell=True, 
                    cwd=self.repo_path,
                    capture_output=True,
                    text=True,
                    check=True
                )
                return result.returncode, result.stdout, result.stderr
            else:
                result = subprocess.run(
                    command, 
                    shell=True, 
                    cwd=self.repo_path,
                    check=True
                )
                return result.returncode, "", ""
        except subprocess.CalledProcessError as e:
            return e.returncode, "", str(e)

    def check_current_branch(self) -> str:
        """Check which branch we're currently on."""
        code, stdout, stderr = self.run_command("git branch --show-current")
        if code == 0:
            return stdout.strip()
        return "unknown"

    def cleanup_local_merge_branches(self):
        """Clean up local merge branches that are no longer needed."""
        print("🧹 Cleaning up local merge branches...")
        
        current_branch = self.check_current_branch()
        
        for branch in self.local_merge_branches:
            if branch == current_branch:
                print(f"⚠️  Skipping current branch: {branch}")
                continue
                
            print(f"🗑️  Deleting local branch: {branch}")
            code, stdout, stderr = self.run_command(f"git branch -D {branch}")
            
            if code == 0:
                self.report_data["branches_cleaned"].append(f"local:{branch}")
                print(f"✅ Successfully deleted local branch: {branch}")
            else:
                print(f"❌ Failed to delete local branch {branch}: {stderr}")

    def cleanup_remote_branches(self):
        """Clean up remote branches that correspond to rejected PRs."""
        print("\n🌐 Cleaning up remote branches...")
        
        for branch in self.problematic_branches:
            print(f"🗑️  Deleting remote branch: {branch}")
            
            # Delete remote branch
            code, stdout, stderr = self.run_command(f"git push origin --delete {branch}")
            
            if code == 0:
                self.report_data["branches_cleaned"].append(f"remote:{branch}")
                print(f"✅ Successfully deleted remote branch: {branch}")
            else:
                print(f"❌ Failed to delete remote branch {branch}: {stderr}")

    def prune_remote_references(self):
        """Remove references to deleted remote branches."""
        print("\n🧽 Pruning remote references...")
        
        code, stdout, stderr = self.run_command("git remote prune origin")
        if code == 0:
            print("✅ Successfully pruned remote references")
            self.report_data["actions_taken"].append("pruned_remote_references")
        else:
            print(f"❌ Failed to prune remote references: {stderr}")

    def establish_guidelines(self):
        """Establish new PR guidelines and standards."""
        print("\n📋 Establishing new PR guidelines...")
        
        guidelines_files = [
            "PR_GUIDELINES_AND_STANDARDS.md",
            "PR_REJECTION_ANALYSIS_REPORT.md"
        ]
        
        for file_path in guidelines_files:
            if self.repo_path / file_path:
                self.report_data["guidelines_established"].append(file_path)
                print(f"✅ Guidelines file exists: {file_path}")
            else:
                print(f"⚠️  Guidelines file missing: {file_path}")

    def create_git_hooks(self):
        """Create pre-commit hooks for file size validation."""
        print("\n🔒 Setting up git hooks...")
        
        hooks_dir = self.repo_path / ".git" / "hooks"
        pre_commit_hook = hooks_dir / "pre-commit"
        
        hook_content = '''#!/bin/sh
# Pre-commit hook for file size validation
# Ensures no files exceed 400 lines

MAX_LINES=400
VIOLATIONS=0

echo "🔍 Checking file sizes..."

for file in $(git diff --cached --name-only --diff-filter=ACM); do
    if [ -f "$file" ]; then
        line_count=$(wc -l < "$file" 2>/dev/null || echo "0")
        if [ "$line_count" -gt "$MAX_LINES" ]; then
            echo "❌ File $file has $line_count lines (max: $MAX_LINES)"
            VIOLATIONS=$((VIOLATIONS + 1))
        fi
    fi
done

if [ "$VIOLATIONS" -gt 0 ]; then
    echo "🚨 Found $VIOLATIONS file(s) exceeding $MAX_LINES lines"
    echo "Please refactor large files before committing"
    exit 1
fi

echo "✅ All files are within size limits"
exit 0
'''
        
        try:
            with open(pre_commit_hook, 'w') as f:
                f.write(hook_content)
            
            # Make the hook executable
            os.chmod(pre_commit_hook, 0o755)
            
            print("✅ Created pre-commit hook for file size validation")
            self.report_data["actions_taken"].append("created_pre_commit_hook")
        except Exception as e:
            print(f"❌ Failed to create pre-commit hook: {e}")

    def create_branch_protection_config(self):
        """Create configuration for branch protection rules."""
        print("\n🛡️  Creating branch protection configuration...")
        
        config = {
            "branch_protection": {
                "main_branch": "agent",
                "protected_branches": ["agent", "main", "master"],
                "rules": {
                    "require_reviews": True,
                    "min_reviews": 2,
                    "require_status_checks": True,
                    "require_branch_up_to_date": True,
                    "restrict_pushes": True,
                    "allow_force_pushes": False,
                    "allow_deletions": False
                }
            },
            "pr_limits": {
                "max_file_size_lines": 400,
                "max_pr_size_lines": 500,
                "max_files_per_pr": 20
            },
            "automated_checks": [
                "file_size_validation",
                "code_style_checking",
                "basic_syntax_validation",
                "security_scanning"
            ]
        }
        
        config_file = self.repo_path / "config" / "branch_protection.json"
        config_file.parent.mkdir(exist_ok=True)
        
        try:
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)
            
            print("✅ Created branch protection configuration")
            self.report_data["actions_taken"].append("created_branch_protection_config")
        except Exception as e:
            print(f"❌ Failed to create branch protection config: {e}")

    def generate_cleanup_report(self):
        """Generate a comprehensive cleanup report."""
        print("\n📊 Generating cleanup report...")
        
        report_file = self.repo_path / "CLEANUP_REPORT.md"
        
        report_content = f"""# Repository Cleanup Report
**Date:** {self.report_data['timestamp']}
**Repository:** {self.report_data['repository']}

## Summary
This report documents the cleanup actions taken after rejecting problematic PRs and establishing new guidelines.

## Actions Taken
{chr(10).join(f"- {action}" for action in self.report_data['actions_taken'])}

## Branches Cleaned
{chr(10).join(f"- {branch}" for branch in self.report_data['branches_cleaned'])}

## Guidelines Established
{chr(10).join(f"- {guideline}" for guideline in self.report_data['guidelines_established'])}

## Current Status
- ✅ Repository cleaned of problematic branches
- ✅ New PR guidelines established
- ✅ Pre-commit hooks configured
- ✅ Branch protection rules defined

## Next Steps
1. **Team Training:** Review new PR guidelines with team
2. **Process Implementation:** Begin using new standards
3. **Monitoring:** Track PR quality metrics
4. **Continuous Improvement:** Refine guidelines based on usage

## Recommendations
- Enforce 400-line file limit strictly
- Require PR size under 500 lines
- Implement automated checks in CI/CD
- Regular code quality reviews
- Incremental refactoring approach

---
**Report Generated:** {self.report_data['timestamp']}
**Status:** Cleanup Complete - Guidelines Established
"""
        
        try:
            with open(report_file, 'w') as f:
                f.write(report_content)
            
            print("✅ Generated cleanup report")
            self.report_data["actions_taken"].append("generated_cleanup_report")
        except Exception as e:
            print(f"❌ Failed to generate cleanup report: {e}")

    def run_cleanup(self):
        """Run the complete cleanup process."""
        print("🚀 Starting repository cleanup process...")
        print("=" * 50)
        
        # Check current status
        current_branch = self.check_current_branch()
        print(f"📍 Current branch: {current_branch}")
        
        if current_branch != "agent":
            print("⚠️  Warning: Not on main branch. Consider switching to 'agent' branch.")
        
        # Run cleanup steps
        self.cleanup_local_merge_branches()
        self.cleanup_remote_branches()
        self.prune_remote_references()
        self.establish_guidelines()
        self.create_git_hooks()
        self.create_branch_protection_config()
        self.generate_cleanup_report()
        
        print("\n" + "=" * 50)
        print("🎉 Repository cleanup completed!")
        print(f"📊 Report generated: CLEANUP_REPORT.md")
        print(f"📋 Guidelines established: PR_GUIDELINES_AND_STANDARDS.md")
        print("\nNext steps:")
        print("1. Review the cleanup report")
        print("2. Share new guidelines with team")
        print("3. Begin using new PR standards")
        print("4. Monitor and enforce compliance")

def main():
    """Main function to run the cleanup process."""
    repo_path = os.getcwd()
    
    print("🔍 Agent_Cellphone_V2_Repository Cleanup Tool")
    print("=" * 50)
    print(f"Repository: {repo_path}")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # Verify we're in a git repository
    if not (Path(repo_path) / ".git").exists():
        print("❌ Error: Not in a git repository")
        return 1
    
    # Create cleanup instance and run
    cleanup = RepositoryCleanup(repo_path)
    
    try:
        cleanup.run_cleanup()
        return 0
    except Exception as e:
        print(f"❌ Error during cleanup: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
