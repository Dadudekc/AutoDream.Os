#!/usr/bin/env python3
"""
Compare Agent-3 Infrastructure Audit with Agent-6 ROI Analysis
===============================================================

Identify agreements, disagreements, and provide infrastructure perspective.
"""

import json
from pathlib import Path

# Load Agent-3's infrastructure audit
with open("agent_workspaces/agent-3/AGENT3_INFRASTRUCTURE_AUDIT.json") as f:
    agent3_data = json.load(f)

# Load Agent-6's ROI analysis
with open("COMPLETE_GITHUB_ROI_RESULTS.json") as f:
    agent6_data = json.load(f)

# Extract classifications
agent3_keep = set(agent3_data["classifications"]["keep"])
agent3_needs_work = set(agent3_data["classifications"]["needs_work"])
agent3_archive = set(agent3_data["classifications"]["archive"])

# Agent-6 uses tiers: Tier 3 = archive, Tier 1+2 = keep/consolidate
agent6_keep = set([r["repo"] for r in agent6_data["results"] if "TIER 1" in r["tier"] or "TIER 2" in r["tier"]])
agent6_archive = set([r["repo"] for r in agent6_data["results"] if "TIER 3" in r["tier"]])

# Calculate agreements and disagreements
agreements_keep = agent3_keep & agent6_keep
agreements_archive = agent3_archive & agent6_archive

# Major disagreements: Agent-6 says archive, I say keep
major_disagreements = (agent3_keep | agent3_needs_work) & agent6_archive

# Minor disagreements: I say archive, Agent-6 says keep
minor_disagreements = agent3_archive & agent6_keep

print("=" * 70)
print("📊 AGENT-3 vs AGENT-6 COMPARISON REPORT")
print("=" * 70)
print()

print("🔍 OVERVIEW:")
print(f"  Total Repos: {agent3_data['total_repos']}")
print()

print("📈 AGENT-3 (Infrastructure Lens):")
print(f"  KEEP: {len(agent3_keep)} repos (86.7%)")
print(f"  NEEDS WORK: {len(agent3_needs_work)} repos (10.7%)")
print(f"  ARCHIVE: {len(agent3_archive)} repos (2.7%)")
print()

print("📉 AGENT-6 (ROI Lens):")
print(f"  KEEP: {len(agent6_keep)} repos (40.0%)")
print(f"  ARCHIVE: {len(agent6_archive)} repos (60.0%)")
print()

print("✅ AGREEMENTS:")
print(f"  Both say KEEP: {len(agreements_keep)} repos")
print(f"  Both say ARCHIVE: {len(agreements_archive)} repos")
print(f"  Agreement Rate: {(len(agreements_keep) + len(agreements_archive))/agent3_data['total_repos']*100:.1f}%")
print()

print("❌ MAJOR DISAGREEMENTS (I say KEEP/NEEDS WORK, Agent-6 says ARCHIVE):")
print(f"  Count: {len(major_disagreements)} repos ({len(major_disagreements)/agent3_data['total_repos']*100:.1f}%)")
print()

if len(major_disagreements) > 0:
    print("  Top 10 repos where we disagree:")
    count = 0
    for repo_name in sorted(major_disagreements):
        if count >= 10:
            break
        repo_data = agent3_data["detailed_scores"][repo_name]
        print(f"  • {repo_name}")
        print(f"      Agent-3: {repo_data['classification']} (infra score: {repo_data['infrastructure_score']}/100)")
        print(f"      Agent-6: ARCHIVE (ROI-based)")
        print(f"      Language: {repo_data.get('language', 'Unknown')}")
        print(f"      Stars: {repo_data.get('stars', 0)}")
        print()
        count += 1

print("=" * 70)
print()

# Generate detailed comparison report
report = {
    "comparison_date": agent3_data["audit_date"],
    "agent3_perspective": "Infrastructure & DevOps",
    "agent6_perspective": "ROI & Business Value",
    "totals": {
        "repos": agent3_data["total_repos"],
        "agent3_keep": len(agent3_keep),
        "agent3_needs_work": len(agent3_needs_work),
        "agent3_archive": len(agent3_archive),
        "agent6_keep": len(agent6_keep),
        "agent6_archive": len(agent6_archive)
    },
    "agreements": {
        "both_keep": list(agreements_keep),
        "both_archive": list(agreements_archive),
        "agreement_rate": (len(agreements_keep) + len(agreements_archive))/agent3_data['total_repos']*100
    },
    "disagreements": {
        "major": list(major_disagreements),
        "minor": list(minor_disagreements)
    },
    "agent3_recommendation": f"Keep {len(agent3_keep)+len(agent3_needs_work)}/75 repos ({(len(agent3_keep)+len(agent3_needs_work))/75*100:.1f}%), Archive {len(agent3_archive)}/75 ({len(agent3_archive)/75*100:.1f}%)",
    "agent6_recommendation": f"Keep {len(agent6_keep)}/75 (40%), Archive {len(agent6_archive)}/75 (60%)"
}

with open("agent_workspaces/agent-3/COMPARISON_REPORT.json", "w") as f:
    json.dump(report, f, indent=2)

print("💾 Detailed comparison saved to: agent_workspaces/agent-3/COMPARISON_REPORT.json")
print()
print("🐝 Agent-3 Infrastructure Audit Complete!")

