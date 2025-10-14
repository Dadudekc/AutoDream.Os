#!/usr/bin/env python3
"""
GitHub CI/CD Automation Script
Agent-8 (QA & Autonomous Systems Specialist)

Mission: Automate CI/CD setup for 5 GitHub repositories
Value: 500-750 points
"""

import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List, Dict, Tuple

# Configuration
GITHUB_BASE = Path("D:/GitHub_Repos")
WORKFLOW_TEMPLATE = Path("scripts/ci_workflow_template.yml")

REPOS = [
    "UltimateOptionsTradingRobot",
    "trade_analyzer",
    "dreambank",
    "machinelearningmodelmaker",
    "network-scanner"
]

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


def print_header(message: str):
    """Print formatted header"""
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'='*70}")
    print(f"{message}")
    print(f"{'='*70}{Colors.END}\n")


def print_success(message: str):
    """Print success message"""
    print(f"{Colors.GREEN}✅ {message}{Colors.END}")


def print_error(message: str):
    """Print error message"""
    print(f"{Colors.RED}❌ {message}{Colors.END}")


def print_warning(message: str):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.END}")


def print_info(message: str):
    """Print info message"""
    print(f"{Colors.BLUE}ℹ️  {message}{Colors.END}")


def check_prerequisites() -> bool:
    """Check if prerequisites are met"""
    print_header("🔍 Checking Prerequisites")
    
    # Check if workflow template exists
    if not WORKFLOW_TEMPLATE.exists():
        print_error(f"Workflow template not found: {WORKFLOW_TEMPLATE}")
        return False
    print_success(f"Workflow template found: {WORKFLOW_TEMPLATE}")
    
    # Check if GitHub base directory exists
    if not GITHUB_BASE.exists():
        print_error(f"GitHub base directory not found: {GITHUB_BASE}")
        return False
    print_success(f"GitHub base directory found: {GITHUB_BASE}")
    
    # Check git is available
    try:
        subprocess.run(["git", "--version"], capture_output=True, check=True)
        print_success("Git is available")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print_error("Git is not available or not in PATH")
        return False
    
    return True


def clone_or_update_repo(repo_name: str) -> Tuple[bool, Path]:
    """Clone repo if needed, or update if exists"""
    repo_path = GITHUB_BASE / repo_name
    clone_url = f"https://github.com/Dadudekc/{repo_name}.git"
    
    if repo_path.exists():
        print_info(f"{repo_name}: Repository already exists, pulling latest")
        try:
            subprocess.run(
                ["git", "pull"],
                cwd=repo_path,
                capture_output=True,
                check=True
            )
            print_success(f"{repo_name}: Updated to latest")
            return True, repo_path
        except subprocess.CalledProcessError as e:
            print_warning(f"{repo_name}: Could not pull: {e}")
            return True, repo_path
    else:
        print_info(f"{repo_name}: Cloning from {clone_url}")
        try:
            subprocess.run(
                ["git", "clone", clone_url, str(repo_path)],
                capture_output=True,
                check=True
            )
            print_success(f"{repo_name}: Cloned successfully")
            return True, repo_path
        except subprocess.CalledProcessError as e:
            print_error(f"{repo_name}: Failed to clone: {e}")
            return False, repo_path


def add_workflow_to_repo(repo_name: str, repo_path: Path) -> bool:
    """Add CI/CD workflow to repository"""
    print_info(f"{repo_name}: Adding CI/CD workflow")
    
    # Create .github/workflows directory
    workflow_dir = repo_path / ".github" / "workflows"
    workflow_dir.mkdir(parents=True, exist_ok=True)
    print_success(f"{repo_name}: Created .github/workflows directory")
    
    # Copy workflow template
    workflow_file = workflow_dir / "ci.yml"
    shutil.copy(WORKFLOW_TEMPLATE, workflow_file)
    print_success(f"{repo_name}: Copied workflow template to ci.yml")
    
    return True


def commit_and_push(repo_name: str, repo_path: Path) -> bool:
    """Commit and push workflow changes"""
    print_info(f"{repo_name}: Committing and pushing changes")
    
    try:
        # Check if there are changes
        status_result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True
        )
        
        if not status_result.stdout.strip():
            print_warning(f"{repo_name}: No changes to commit (workflow may already exist)")
            return True
        
        # Add changes
        subprocess.run(
            ["git", "add", ".github/"],
            cwd=repo_path,
            check=True
        )
        print_success(f"{repo_name}: Staged .github/ directory")
        
        # Commit
        subprocess.run(
            ["git", "commit", "-m", "ci: Add CI/CD pipeline with GitHub Actions\n\nAdds comprehensive CI/CD workflow with:\n- Multi-version Python testing (3.10, 3.11, 3.12)\n- Code quality checks (ruff, black, isort)\n- Security scanning (bandit)\n- Test execution with coverage\n- Codecov integration\n\nGenerated by Agent-8 (QA & Autonomous Systems Specialist)"],
            cwd=repo_path,
            check=True
        )
        print_success(f"{repo_name}: Committed changes")
        
        # Push
        subprocess.run(
            ["git", "push"],
            cwd=repo_path,
            check=True
        )
        print_success(f"{repo_name}: Pushed to remote")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print_error(f"{repo_name}: Git operation failed: {e}")
        return False


def add_readme_badge(repo_name: str, repo_path: Path) -> bool:
    """Add CI/CD badge to README"""
    print_info(f"{repo_name}: Adding CI/CD badge to README")
    
    readme_path = repo_path / "README.md"
    if not readme_path.exists():
        print_warning(f"{repo_name}: README.md not found, skipping badge")
        return False
    
    # Read current README
    readme_content = readme_path.read_text(encoding='utf-8')
    
    # Check if badge already exists
    badge_marker = "![CI/CD](https://github.com/Dadudekc"
    if badge_marker in readme_content:
        print_warning(f"{repo_name}: CI/CD badge already exists in README")
        return True
    
    # Create badge markdown
    badge = f"![CI/CD](https://github.com/Dadudekc/{repo_name}/actions/workflows/ci.yml/badge.svg)\n\n"
    
    # Add badge after first heading (or at start)
    if readme_content.startswith("#"):
        # Find end of first line (heading)
        first_newline = readme_content.find("\n")
        if first_newline != -1:
            readme_content = (
                readme_content[:first_newline + 1] +
                "\n" + badge +
                readme_content[first_newline + 1:]
            )
        else:
            readme_content = readme_content + "\n\n" + badge
    else:
        readme_content = badge + readme_content
    
    # Write updated README
    readme_path.write_text(readme_content, encoding='utf-8')
    print_success(f"{repo_name}: Added CI/CD badge to README")
    
    try:
        subprocess.run(["git", "add", "README.md"], cwd=repo_path, check=True)
        subprocess.run(
            ["git", "commit", "-m", "docs: Add CI/CD pipeline badge to README"],
            cwd=repo_path,
            check=True
        )
        subprocess.run(["git", "push"], cwd=repo_path, check=True)
        print_success(f"{repo_name}: README badge committed and pushed")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"{repo_name}: Failed to commit README badge: {e}")
        return False


def process_repo(repo_name: str) -> Dict[str, any]:
    """Process a single repository"""
    print_header(f"🚀 Processing: {repo_name}")
    
    result = {
        "repo": repo_name,
        "cloned": False,
        "workflow_added": False,
        "committed": False,
        "badge_added": False,
        "success": False
    }
    
    # Clone or update repo
    cloned, repo_path = clone_or_update_repo(repo_name)
    result["cloned"] = cloned
    if not cloned:
        return result
    
    # Add workflow
    workflow_added = add_workflow_to_repo(repo_name, repo_path)
    result["workflow_added"] = workflow_added
    if not workflow_added:
        return result
    
    # Commit and push
    committed = commit_and_push(repo_name, repo_path)
    result["committed"] = committed
    if not committed:
        return result
    
    # Add README badge
    badge_added = add_readme_badge(repo_name, repo_path)
    result["badge_added"] = badge_added
    
    result["success"] = True
    print_success(f"{repo_name}: ✅ COMPLETE!")
    
    return result


def generate_report(results: List[Dict]) -> None:
    """Generate summary report"""
    print_header("📊 CI/CD Automation Report")
    
    successful = sum(1 for r in results if r["success"])
    total = len(results)
    
    print(f"\n{Colors.BOLD}Summary:{Colors.END}")
    print(f"  Total Repos: {total}")
    print(f"  {Colors.GREEN}Successful: {successful}{Colors.END}")
    print(f"  {Colors.RED}Failed: {total - successful}{Colors.END}")
    print(f"  Success Rate: {(successful/total)*100:.1f}%")
    
    print(f"\n{Colors.BOLD}Detailed Results:{Colors.END}")
    for r in results:
        status_icon = "✅" if r["success"] else "❌"
        print(f"\n{status_icon} {r['repo']}:")
        print(f"    Cloned: {'✅' if r['cloned'] else '❌'}")
        print(f"    Workflow Added: {'✅' if r['workflow_added'] else '❌'}")
        print(f"    Committed: {'✅' if r['committed'] else '❌'}")
        print(f"    Badge Added: {'✅' if r['badge_added'] else '❌'}")
    
    # Points calculation
    base_points = successful * 100
    automation_bonus = 150 if successful == total else 0
    quality_bonus = 100 if successful == total else 0
    total_points = base_points + automation_bonus + quality_bonus
    
    print(f"\n{Colors.BOLD}🏆 Points Earned:{Colors.END}")
    print(f"  Base ({successful} repos × 100): {base_points} points")
    if automation_bonus:
        print(f"  Automation Bonus: {automation_bonus} points")
    if quality_bonus:
        print(f"  Quality Bonus: {quality_bonus} points")
    print(f"  {Colors.GREEN}{Colors.BOLD}Total: {total_points} points{Colors.END}")
    
    # Save report
    report_path = Path("scripts/ci_cd_automation_report.json")
    report_data = {
        "date": "2025-10-14",
        "agent": "Agent-8",
        "mission": "GitHub CI/CD Automation",
        "results": results,
        "summary": {
            "total_repos": total,
            "successful": successful,
            "failed": total - successful,
            "success_rate": f"{(successful/total)*100:.1f}%",
            "points_earned": total_points
        }
    }
    report_path.write_text(json.dumps(report_data, indent=2))
    print_success(f"\nReport saved to: {report_path}")


def main():
    """Main execution"""
    print_header("🐝 Agent-8: GitHub CI/CD Automation Mission")
    print("Mission: Add CI/CD to 5 repositories")
    print("Value: 500-750 points")
    print("Agent: Agent-8 (QA & Autonomous Systems Specialist)")
    
    # Check prerequisites
    if not check_prerequisites():
        print_error("Prerequisites check failed. Exiting.")
        sys.exit(1)
    
    # Process all repos
    results = []
    for repo in REPOS:
        result = process_repo(repo)
        results.append(result)
    
    # Generate report
    generate_report(results)
    
    print_header("🎉 Mission Complete!")
    print("Next steps:")
    print("1. Check GitHub Actions tabs on each repo")
    print("2. Verify workflows are passing")
    print("3. Monitor for any failures")
    print("4. Share learnings to Swarm Brain")
    
    return 0 if all(r["success"] for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())

