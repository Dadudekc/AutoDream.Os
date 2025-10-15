#!/usr/bin/env python3
"""
Agent-3 Independent Infrastructure Audit Scanner
=================================================

Unbiased infrastructure assessment of all GitHub repos.
NO READING OF AGENT-6 DATA UNTIL AFTER INDEPENDENT ANALYSIS!

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-10-14
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List

# Add to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.tools.github_scanner import GitHubScanner, RepositoryInfo


class InfrastructureAuditor:
    """Infrastructure-focused repository auditor."""
    
    def __init__(self):
        self.scanner = GitHubScanner()
        self.results = {
            "audit_date": datetime.now().isoformat(),
            "auditor": "Agent-3",
            "perspective": "Infrastructure & DevOps",
            "total_repos": 0,
            "classifications": {
                "keep": [],
                "needs_work": [],
                "archive": []
            },
            "detailed_scores": {}
        }
    
    def assess_infrastructure(self, repo: RepositoryInfo) -> Dict:
        """Assess repository infrastructure quality using available GitHub API data."""
        score = 0
        details = {}
        
        # Helper: check topics and description for keywords
        def has_keywords(keywords: List[str]) -> bool:
            topics_str = ' '.join(repo.topics).lower() if repo.topics else ''
            desc_str = repo.description.lower() if repo.description else ''
            return any(kw in topics_str or kw in desc_str for kw in keywords)
        
        # Category 1: Automation & CI/CD (30 points)
        automation_score = 0
        ci_cd_keywords = ['github-actions', 'ci', 'cd', 'continuous-integration', 'travis', 'jenkins']
        if has_keywords(ci_cd_keywords):
            automation_score += 15
            details["ci_cd"] = "✅ Detected (topics/desc)"
        else:
            details["ci_cd"] = "❌ Not detected"
        
        test_keywords = ['test', 'testing', 'pytest', 'jest', 'mocha', 'unittest']
        if has_keywords(test_keywords):
            automation_score += 10
            details["tests"] = "✅ Detected (topics/desc)"
        else:
            details["tests"] = "❌ Not detected"
        
        # Deployment indicators
        deploy_keywords = ['deployment', 'deploy', 'heroku', 'aws', 'kubernetes']
        if has_keywords(deploy_keywords):
            automation_score += 5
            details["auto_deploy"] = "✅ Detected"
        else:
            details["auto_deploy"] = "❌ Not detected"
        
        score += automation_score
        details["automation_score"] = automation_score
        
        # Category 2: Containerization & Deployment (25 points)
        container_score = 0
        docker_keywords = ['docker', 'dockerfile', 'container']
        if has_keywords(docker_keywords):
            container_score += 15
            details["docker"] = "✅ Detected (topics/desc)"
        else:
            details["docker"] = "❌ Not detected"
        
        orchestration_keywords = ['docker-compose', 'kubernetes', 'k8s', 'helm']
        if has_keywords(orchestration_keywords):
            container_score += 10
            details["orchestration"] = "✅ Detected"
        else:
            details["orchestration"] = "❌ Not detected"
        
        score += container_score
        details["container_score"] = container_score
        
        # Category 3: Monitoring & Observability (20 points)
        monitoring_score = 0
        monitoring_keywords = ['logging', 'monitoring', 'observability', 'metrics', 'prometheus', 'grafana']
        if has_keywords(monitoring_keywords):
            monitoring_score += 10
            details["monitoring"] = "✅ Detected (topics/desc)"
        else:
            details["monitoring"] = "❌ Not detected"
        
        health_keywords = ['health-check', 'healthcheck', 'status-page']
        if has_keywords(health_keywords):
            monitoring_score += 10
            details["health_checks"] = "✅ Detected"
        else:
            details["health_checks"] = "❌ Not detected"
        
        score += monitoring_score
        details["monitoring_score"] = monitoring_score
        
        # Category 4: Code Quality Infrastructure (15 points)
        quality_score = 0
        if has_keywords(test_keywords):  # Reuse test check
            quality_score += 10
            details["test_suite"] = "✅ Detected"
        else:
            details["test_suite"] = "❌ Not detected"
        
        lint_keywords = ['linting', 'eslint', 'pylint', 'prettier', 'black', 'flake8']
        if has_keywords(lint_keywords):
            quality_score += 5
            details["linting"] = "✅ Detected"
        else:
            details["linting"] = "❌ Not detected"
        
        score += quality_score
        details["quality_score"] = quality_score
        
        # Category 5: Dependency Management (10 points)
        dependency_score = 0
        
        # Check if has language (implies dependency management)
        if repo.language:
            dependency_score += 5
            details["dependencies"] = f"✅ {repo.language} project"
        else:
            details["dependencies"] = "❌ No language"
        
        # Check if updated recently (dependencies current)
        if repo.last_updated:
            # Make datetime timezone-aware for comparison
            now = datetime.now(repo.last_updated.tzinfo) if repo.last_updated.tzinfo else datetime.now()
            if now - repo.last_updated < timedelta(days=365):
                dependency_score += 5
                days_ago = (now - repo.last_updated).days
                details["deps_current"] = f"✅ Updated {days_ago} days ago"
            else:
                days_ago = (now - repo.last_updated).days
                details["deps_current"] = f"⚠️ Old ({days_ago} days ago)"
        else:
            details["deps_current"] = "❌ No update date"
        
        score += dependency_score
        details["dependency_score"] = dependency_score
        
        # Total score
        details["total_score"] = score
        details["max_score"] = 100
        
        return details
    
    def calculate_maintenance_burden(self, repo: RepositoryInfo, infra_details: Dict) -> int:
        """Calculate maintenance burden (0-100, higher = more burden)."""
        burden = 0
        
        # No CI/CD = manual testing needed
        if "❌" in infra_details.get("ci_cd", ""):
            burden += 20
        
        # No tests = risky changes
        if "❌" in infra_details.get("tests", ""):
            burden += 20
        
        # Complex codebase (use size as proxy)
        if repo.size_kb and repo.size_kb > 10000:  # >10MB
            burden += 15
        elif repo.size_kb and repo.size_kb > 5000:  # >5MB
            burden += 8
        
        # Outdated dependencies (not updated in >1 year)
        if repo.last_updated:
            now = datetime.now(repo.last_updated.tzinfo) if repo.last_updated.tzinfo else datetime.now()
            if now - repo.last_updated > timedelta(days=365):
                burden += 15
        
        # No documentation (check if has description)
        if not repo.description or len(repo.description) < 20:
            burden += 10
        
        return min(burden, 100)
    
    def classify_repo(self, repo: RepositoryInfo, infra_score: int, burden: int) -> str:
        """Classify repo: KEEP, NEEDS WORK, or ARCHIVE."""
        
        # Check if active (last commit <3 months)
        is_active = False
        if repo.last_updated:
            now = datetime.now(repo.last_updated.tzinfo) if repo.last_updated.tzinfo else datetime.now()
            if now - repo.last_updated < timedelta(days=90):
                is_active = True
        
        # Check if old (last commit >1 year)
        is_old = False
        if repo.last_updated:
            now = datetime.now(repo.last_updated.tzinfo) if repo.last_updated.tzinfo else datetime.now()
            if now - repo.last_updated > timedelta(days=365):
                is_old = True
        
        # Classification logic
        if infra_score >= 60:
            return "KEEP"
        elif is_active:
            return "KEEP"  # Active development trumps poor infra
        elif infra_score < 30 and burden > 60 and is_old:
            return "ARCHIVE"
        elif infra_score < 30:
            return "NEEDS WORK"
        else:
            return "NEEDS WORK"
    
    def audit_all_repos(self):
        """Run complete infrastructure audit."""
        print("🔍 Starting Independent Infrastructure Audit...")
        print("=" * 60)
        
        # Fetch all repos
        print("📡 Fetching repositories...")
        repos = self.scanner.list_user_repositories()
        self.results["total_repos"] = len(repos)
        print(f"✅ Found {len(repos)} repositories\n")
        
        # Assess each repo
        for i, repo in enumerate(repos, 1):
            print(f"[{i}/{len(repos)}] Assessing: {repo.name}")
            
            # Infrastructure assessment
            infra_details = self.assess_infrastructure(repo)
            infra_score = infra_details["total_score"]
            
            # Maintenance burden
            burden = self.calculate_maintenance_burden(repo, infra_details)
            
            # Classification
            classification = self.classify_repo(repo, infra_score, burden)
            
            # Store results
            repo_result = {
                "name": repo.name,
                "url": repo.url,
                "language": repo.language,
                "description": repo.description,
                "stars": repo.stars,
                "size_kb": repo.size_kb,
                "last_updated": repo.last_updated.isoformat() if repo.last_updated else None,
                "infrastructure_score": infra_score,
                "maintenance_burden": burden,
                "classification": classification,
                "details": infra_details
            }
            
            self.results["detailed_scores"][repo.name] = repo_result
            self.results["classifications"][classification.lower().replace(" ", "_")].append(repo.name)
            
            # Print summary
            print(f"  Score: {infra_score}/100 | Burden: {burden}/100 | → {classification}\n")
        
        print("=" * 60)
        print("✅ Infrastructure Audit Complete!\n")
        
        # Summary
        keep_count = len(self.results["classifications"]["keep"])
        needs_work_count = len(self.results["classifications"]["needs_work"])
        archive_count = len(self.results["classifications"]["archive"])
        
        print("📊 SUMMARY:")
        print(f"  KEEP: {keep_count} repos ({keep_count/len(repos)*100:.1f}%)")
        print(f"  NEEDS WORK: {needs_work_count} repos ({needs_work_count/len(repos)*100:.1f}%)")
        print(f"  ARCHIVE: {archive_count} repos ({archive_count/len(repos)*100:.1f}%)")
        print()
        
        return self.results
    
    def save_results(self, filename: str = "AGENT3_INFRASTRUCTURE_AUDIT.json"):
        """Save audit results to file."""
        filepath = Path("agent_workspaces/agent-3") / filename
        with open(filepath, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"💾 Results saved to: {filepath}")


if __name__ == "__main__":
    auditor = InfrastructureAuditor()
    results = auditor.audit_all_repos()
    auditor.save_results()
    
    print("\n🐝 Agent-3 Independent Infrastructure Audit Complete!")
    print("Next: Compare with Agent-6's findings")

