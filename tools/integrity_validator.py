"""
Integrity Validator - Cross-check task claims against actual evidence

PURPOSE: Automated integrity checking for Entry #025 compliance
PREVENTS: False credit claims, misattribution, inflated achievements
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

from git_work_verifier import GitWorkVerifier, VerificationResult
from work_attribution_tool import WorkAttributionTool


@dataclass
class IntegrityCheck:
    """Result of integrity validation"""
    agent: str
    claim: str
    validated: bool
    confidence: str  # HIGH, MEDIUM, LOW, FAILED
    evidence_type: str  # GIT, FILE, STATUS, NONE
    evidence_details: Optional[str]
    timestamp: datetime
    recommendation: str


class IntegrityValidator:
    """Validate agent task claims against evidence"""
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path)
        self.git_verifier = GitWorkVerifier(repo_path)
        self.attribution_tool = WorkAttributionTool(repo_path)
    
    def validate_task_completion(
        self,
        agent: str,
        task_id: str,
        claimed_work: str,
        files_claimed: List[str],
        hours_ago: int = 24
    ) -> IntegrityCheck:
        """
        Validate that an agent actually completed claimed work
        
        Args:
            agent: Agent ID
            task_id: Task identifier
            claimed_work: Description of work done
            files_claimed: Files allegedly modified
            hours_ago: How far back to check
        
        Returns:
            IntegrityCheck with validation result
        """
        # Check git evidence for each file
        git_checks = []
        for file_path in files_claimed:
            result = self.git_verifier.verify_claim(
                agent=agent,
                file_path=file_path,
                claimed_changes=claimed_work,
                time_window_hours=hours_ago
            )
            git_checks.append(result)
        
        # Analyze results
        verified_count = sum(1 for c in git_checks if c.verified)
        total_count = len(git_checks)
        
        if verified_count == total_count and total_count > 0:
            # All files verified
            commits = [c.evidence.commit_hash[:8] for c in git_checks if c.evidence]
            return IntegrityCheck(
                agent=agent,
                claim=f"{task_id}: {claimed_work}",
                validated=True,
                confidence="HIGH",
                evidence_type="GIT",
                evidence_details=f"Git commits: {', '.join(commits)}",
                timestamp=datetime.now(),
                recommendation="ACCEPT - Full git verification"
            )
        
        elif verified_count > 0:
            # Partial verification
            verified_files = [
                git_checks[i].claim.file_path
                for i in range(len(git_checks))
                if git_checks[i].verified
            ]
            return IntegrityCheck(
                agent=agent,
                claim=f"{task_id}: {claimed_work}",
                validated=True,
                confidence="MEDIUM",
                evidence_type="GIT",
                evidence_details=f"Verified files: {', '.join(verified_files)}",
                timestamp=datetime.now(),
                recommendation=f"ACCEPT PARTIAL - {verified_count}/{total_count} files verified"
            )
        
        else:
            # No git verification
            # Check if someone else did it
            actual_agents = []
            for file_path in files_claimed:
                agents = self.attribution_tool.who_worked_on_file(
                    file_path, hours_ago
                )
                actual_agents.extend(agents)
            
            if actual_agents:
                actual = ", ".join(set(actual_agents))
                return IntegrityCheck(
                    agent=agent,
                    claim=f"{task_id}: {claimed_work}",
                    validated=False,
                    confidence="FAILED",
                    evidence_type="GIT",
                    evidence_details=f"Work done by: {actual}",
                    timestamp=datetime.now(),
                    recommendation=f"REJECT - Attribute to {actual} instead"
                )
            else:
                return IntegrityCheck(
                    agent=agent,
                    claim=f"{task_id}: {claimed_work}",
                    validated=False,
                    confidence="FAILED",
                    evidence_type="NONE",
                    evidence_details="No git evidence found",
                    timestamp=datetime.now(),
                    recommendation="REJECT - No evidence of work"
                )
    
    def validate_agent_status(
        self,
        agent: str
    ) -> IntegrityCheck:
        """Validate agent's status.json against actual work"""
        status_path = Path(f"agent_workspaces/{agent}/status.json")
        
        if not status_path.exists():
            return IntegrityCheck(
                agent=agent,
                claim="Status validation",
                validated=False,
                confidence="FAILED",
                evidence_type="FILE",
                evidence_details="status.json not found",
                timestamp=datetime.now(),
                recommendation="CREATE status.json"
            )
        
        with open(status_path) as f:
            status = json.load(f)
        
        # Get actual work from git
        actual_work = self.attribution_tool.get_agent_work(agent, hours=24)
        
        # Compare claimed vs actual
        claimed_tasks = status.get("completed_tasks", [])
        actual_commits = len(actual_work)
        
        if actual_commits == 0 and len(claimed_tasks) > 0:
            return IntegrityCheck(
                agent=agent,
                claim=f"Status shows {len(claimed_tasks)} tasks",
                validated=False,
                confidence="FAILED",
                evidence_type="GIT",
                evidence_details=f"No git commits in 24h",
                timestamp=datetime.now(),
                recommendation="REVIEW - Status doesn't match git history"
            )
        
        return IntegrityCheck(
            agent=agent,
            claim=f"{len(claimed_tasks)} tasks claimed",
            validated=True,
            confidence="HIGH",
            evidence_type="GIT",
            evidence_details=f"{actual_commits} git commits found",
            timestamp=datetime.now(),
            recommendation="VALID - Status matches git activity"
        )
    
    def validate_points_claim(
        self,
        agent: str,
        points_claimed: int,
        work_description: str
    ) -> IntegrityCheck:
        """Validate that claimed points match actual work"""
        # Get recent work
        actual_work = self.attribution_tool.get_agent_work(agent, hours=24)
        
        if not actual_work:
            return IntegrityCheck(
                agent=agent,
                claim=f"{points_claimed} points for: {work_description}",
                validated=False,
                confidence="FAILED",
                evidence_type="GIT",
                evidence_details="No git commits in 24h",
                timestamp=datetime.now(),
                recommendation=f"REJECT - No evidence for {points_claimed} points"
            )
        
        # Calculate work magnitude
        total_lines = sum(w.lines_added + w.lines_deleted for w in actual_work)
        files_touched = len(set(w.file_path for w in actual_work))
        commits = len(actual_work)
        
        # Rough point estimation (would need real rules)
        estimated_points = (commits * 100) + (files_touched * 50)
        
        if points_claimed > estimated_points * 2:
            return IntegrityCheck(
                agent=agent,
                claim=f"{points_claimed} points",
                validated=False,
                confidence="LOW",
                evidence_type="GIT",
                evidence_details=f"Estimated: {estimated_points}pts based on {commits} commits",
                timestamp=datetime.now(),
                recommendation=f"REVIEW - Claimed {points_claimed} > estimated {estimated_points}"
            )
        
        return IntegrityCheck(
            agent=agent,
            claim=f"{points_claimed} points",
            validated=True,
            confidence="MEDIUM",
            evidence_type="GIT",
            evidence_details=f"{commits} commits, {files_touched} files, {total_lines} lines",
            timestamp=datetime.now(),
            recommendation="ACCEPT - Points reasonable for work done"
        )
    
    def generate_integrity_report(
        self,
        checks: List[IntegrityCheck]
    ) -> str:
        """Generate integrity validation report"""
        report = []
        report.append("=" * 80)
        report.append("INTEGRITY VALIDATION REPORT")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("=" * 80)
        report.append("")
        
        validated = [c for c in checks if c.validated]
        failed = [c for c in checks if not c.validated]
        
        report.append(f"SUMMARY: {len(validated)}/{len(checks)} claims validated")
        report.append("")
        
        if validated:
            report.append("✅ VALIDATED CLAIMS:")
            for check in validated:
                report.append(f"  Agent: {check.agent}")
                report.append(f"  Claim: {check.claim}")
                report.append(f"  Confidence: {check.confidence}")
                report.append(f"  Evidence: {check.evidence_details}")
                report.append(f"  → {check.recommendation}")
                report.append("")
        
        if failed:
            report.append("❌ FAILED VALIDATION:")
            for check in failed:
                report.append(f"  Agent: {check.agent}")
                report.append(f"  Claim: {check.claim}")
                report.append(f"  Issue: {check.evidence_details}")
                report.append(f"  → {check.recommendation}")
                report.append("")
        
        return "\n".join(report)


def main():
    """CLI for integrity validation"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Validate agent task claims with integrity checking"
    )
    parser.add_argument(
        "--agent",
        required=True,
        help="Agent ID to validate"
    )
    parser.add_argument(
        "--task",
        help="Task ID to validate"
    )
    parser.add_argument(
        "--work",
        help="Description of claimed work"
    )
    parser.add_argument(
        "--files",
        nargs="+",
        help="Files claimed to be modified"
    )
    parser.add_argument(
        "--hours",
        type=int,
        default=24,
        help="Time window (default: 24h)"
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Validate agent status"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output JSON"
    )
    
    args = parser.parse_args()
    
    validator = IntegrityValidator()
    
    if args.status:
        result = validator.validate_agent_status(args.agent)
    elif args.task and args.work and args.files:
        result = validator.validate_task_completion(
            agent=args.agent,
            task_id=args.task,
            claimed_work=args.work,
            files_claimed=args.files,
            hours_ago=args.hours
        )
    else:
        parser.print_help()
        return
    
    if args.json:
        print(json.dumps(asdict(result), default=str, indent=2))
    else:
        print("\n" + "=" * 80)
        print(f"INTEGRITY CHECK: {result.agent}")
        print("=" * 80)
        print(f"Claim: {result.claim}")
        print(f"Validated: {'✅ YES' if result.validated else '❌ NO'}")
        print(f"Confidence: {result.confidence}")
        print(f"Evidence: {result.evidence_details}")
        print(f"Recommendation: {result.recommendation}")
        print("")


if __name__ == "__main__":
    main()

