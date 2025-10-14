#!/usr/bin/env python3
"""
Agent-1 Independent QA Audit Script
NO BIAS - Using MY QA criteria only!
"""

import json
from datetime import datetime, timedelta
from pathlib import Path

# Load MY independent repo data
with open('agent_workspaces/Agent-1/MY_INDEPENDENT_REPO_DATA.json') as f:
    data = json.load(f)
    repos = data['repositories']

print(f"🔍 AGENT-1 INDEPENDENT QA AUDIT")
print(f"=" * 60)
print(f"Total Repos: {len(repos)}")
print(f"Methodology: QA Specialist criteria (unbiased)\n")

# MY QA SCORING FUNCTION
def qa_score_repo(repo):
    """Score repo using MY QA criteria."""
    score = 0
    reasons = []
    
    # 1. Size (manageable = good)
    size_kb = repo['size_kb']
    if 50 <= size_kb <= 5000:  # 50KB - 5MB sweet spot
        score += 10
        reasons.append("Good size")
    elif size_kb < 10:
        score -= 15
        reasons.append("Too small/empty")
    
    # 2. Language (Python preferred as QA specialist)
    language = repo['language']
    if language == 'Python':
        score += 15
        reasons.append("Python (testable)")
    elif language in ['JavaScript', 'TypeScript', 'Java', 'Go']:
        score += 10
        reasons.append(f"{language} (ok)")
    elif not language or language == 'Unknown':
        score -= 10
        reasons.append("No clear language")
    
    # 3. Activity (recent = maintained)
    try:
        last_update = datetime.fromisoformat(repo['updated'].replace('Z', '+00:00'))
        days_since_update = (datetime.now() - last_update.replace(tzinfo=None)).days
        
        if days_since_update <= 180:  # 6 months
            score += 15
            reasons.append("Recently active")
        elif days_since_update <= 365:  # 1 year
            score += 5
            reasons.append("Somewhat active")
        else:
            score -= 10
            reasons.append(f"Stale ({days_since_update} days)")
    except:
        score -= 5
        reasons.append("Unknown activity")
    
    # 4. Documentation (README assumed, description quality)
    desc = repo['description']
    if desc and desc != 'No description' and len(desc) > 20:
        score += 15
        reasons.append("Good description")
    elif desc and len(desc) > 5:
        score += 5
        reasons.append("Basic description")
    else:
        score -= 10
        reasons.append("No description")
    
    # 5. Community engagement
    stars = repo['stars']
    forks = repo['forks']
    
    if stars >= 5 or forks >= 2:
        score += 10
        reasons.append(f"Community ({stars}⭐, {forks}🍴)")
    elif stars >= 1 or forks >= 1:
        score += 5
        reasons.append("Some interest")
    else:
        score -= 5
        reasons.append("No engagement")
    
    # 6. Issues (activity indicator)
    issues = repo['issues']
    if issues > 0:
        score += 5
        reasons.append(f"{issues} open issues (active)")
    
    # 7. Private repos (likely important)
    if repo['is_private']:
        score += 10
        reasons.append("Private (likely important)")
    
    return score, reasons

# AUDIT ALL REPOS
audit_results = []
keep_list = []
review_list = []
archive_list = []

for repo in repos:
    score, reasons = qa_score_repo(repo)
    
    # MY DECISION THRESHOLDS
    if score >= 40:
        decision = "KEEP"
        keep_list.append(repo['name'])
    elif score >= 20:
        decision = "REVIEW"
        review_list.append(repo['name'])
    else:
        decision = "ARCHIVE"
        archive_list.append(repo['name'])
    
    audit_results.append({
        'name': repo['name'],
        'score': score,
        'decision': decision,
        'reasons': reasons,
        'metadata': {
            'language': repo['language'],
            'size_kb': repo['size_kb'],
            'stars': repo['stars'],
            'updated': repo['updated']
        }
    })

# SAVE MY FINDINGS
my_findings = {
    'audit_date': str(datetime.now()),
    'auditor': 'Agent-1 (Testing & QA Specialist)',
    'methodology': 'QA Specialist criteria - 100% independent',
    'total_repos': len(repos),
    'keep_count': len(keep_list),
    'review_count': len(review_list),
    'archive_count': len(archive_list),
    'keep_percentage': round(len(keep_list) / len(repos) * 100, 1),
    'archive_percentage': round(len(archive_list) / len(repos) * 100, 1),
    'keep_list': keep_list,
    'review_list': review_list,
    'archive_list': archive_list,
    'detailed_audit': audit_results
}

with open('agent_workspaces/Agent-1/MY_INDEPENDENT_AUDIT_RESULTS.json', 'w') as f:
    json.dump(my_findings, f, indent=2)

# PRINT SUMMARY
print(f"\n📊 MY INDEPENDENT FINDINGS:")
print(f"=" * 60)
print(f"KEEP:    {len(keep_list):2d} repos ({my_findings['keep_percentage']}%)")
print(f"REVIEW:  {len(review_list):2d} repos ({round(len(review_list)/len(repos)*100, 1)}%)")
print(f"ARCHIVE: {len(archive_list):2d} repos ({my_findings['archive_percentage']}%)")
print(f"\n✅ Results saved to: MY_INDEPENDENT_AUDIT_RESULTS.json")
print(f"\n⚠️ Agent-6 claimed: 60% archive (45 repos)")
print(f"🔍 I found: {my_findings['archive_percentage']}% archive ({len(archive_list)} repos)")
print(f"\nReady to compare findings!")

