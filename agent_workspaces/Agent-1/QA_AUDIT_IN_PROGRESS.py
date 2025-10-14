#!/usr/bin/env python3
"""
Agent-1 Independent QA Audit Script
NO AGENT-6 BIAS - Using MY QA criteria only!
"""

import json
from datetime import datetime, timedelta
from pathlib import Path

# Load MY independent repo data
with open('agent_workspaces/Agent-1/MY_INDEPENDENT_REPO_DATA.json') as f:
    data = json.load(f)
    repos = data['repositories']

print(f"🔍 Agent-1 Independent QA Audit Starting...")
print(f"📊 Total Repos: {len(repos)}")
print(f"🎯 Using MY QA criteria (unbiased)")
print("=" * 60)

# MY QA SCORING SYSTEM
keep_list = []
review_list = []
archive_list = []

for repo in repos:
    score = 0
    reasons = []
    
    # MY CRITERIA (defined before seeing Agent-6's work)
    
    # 1. Language quality (15 pts)
    if repo['language'] == 'Python':
        score += 15
        reasons.append("Python (preferred)")
    elif repo['language'] in ['JavaScript', 'TypeScript', 'Java']:
        score += 10
        reasons.append(f"{repo['language']} (acceptable)")
    elif repo['language']:
        score += 5
        reasons.append(f"{repo['language']} (other)")
    
    # 2. Size appropriateness (20 pts)
    size = repo['size_kb']
    if 100 <= size <= 5000:  # Sweet spot
        score += 20
        reasons.append("Good size (100-5000KB)")
    elif 50 <= size < 100 or 5000 < size <= 10000:
        score += 10
        reasons.append("Acceptable size")
    elif size < 50:
        score += 0
        reasons.append("Too small (trivial)")
    else:
        score += 5
        reasons.append("Large but manageable")
    
    # 3. Community engagement (15 pts)
    if repo['stars'] >= 5:
        score += 10
        reasons.append(f"{repo['stars']} stars")
    elif repo['stars'] >= 1:
        score += 5
        reasons.append(f"{repo['stars']} star(s)")
    
    if repo['forks'] >= 1:
        score += 5
        reasons.append(f"{repo['forks']} fork(s)")
    
    # 4. Recent activity (20 pts)
    try:
        updated = datetime.fromisoformat(repo['updated'].replace('Z', '+00:00'))
        days_ago = (datetime.now(updated.tzinfo) - updated).days
        
        if days_ago <= 90:  # 3 months
            score += 20
            reasons.append("Active (updated recently)")
        elif days_ago <= 180:  # 6 months
            score += 10
            reasons.append("Recent activity")
        elif days_ago <= 365:  # 1 year
            score += 5
            reasons.append("Some activity")
        else:
            score += 0
            reasons.append(f"Stale ({days_ago} days)")
    except:
        score += 0
        reasons.append("Unknown activity")
    
    # 5. Has description (10 pts)
    if repo['description'] and len(repo['description']) > 10:
        score += 10
        reasons.append("Good description")
    elif repo['description']:
        score += 5
        reasons.append("Has description")
    
    # 6. Open issues (10 pts - shows engagement)
    if 1 <= repo['issues'] <= 20:
        score += 10
        reasons.append(f"{repo['issues']} issues (healthy)")
    elif repo['issues'] > 20:
        score += 5
        reasons.append(f"{repo['issues']} issues (active)")
    
    # 7. Not private (10 pts - public value)
    if not repo['is_private']:
        score += 10
        reasons.append("Public (community value)")
    
    # DECISION BASED ON MY QA CRITERIA
    decision = ""
    if score >= 60:
        keep_list.append({'repo': repo['name'], 'score': score, 'reasons': reasons})
        decision = "KEEP"
    elif score >= 35:
        review_list.append({'repo': repo['name'], 'score': score, 'reasons': reasons})
        decision = "REVIEW"
    else:
        archive_list.append({'repo': repo['name'], 'score': score, 'reasons': reasons})
        decision = "ARCHIVE"
    
    print(f"{decision:8} | {score:3} pts | {repo['name']:40} | {', '.join(reasons[:2])}")

print("\n" + "=" * 60)
print(f"🎯 MY INDEPENDENT FINDINGS:")
print(f"KEEP:    {len(keep_list):2} repos ({len(keep_list)/len(repos)*100:.1f}%)")
print(f"REVIEW:  {len(review_list):2} repos ({len(review_list)/len(repos)*100:.1f}%)")
print(f"ARCHIVE: {len(archive_list):2} repos ({len(archive_list)/len(repos)*100:.1f}%)")
print("=" * 60)

# Save MY results
results = {
    'audit_date': str(datetime.now()),
    'auditor': 'Agent-1',
    'methodology': 'QA/Testing Specialist Criteria (unbiased)',
    'total_repos': len(repos),
    'keep': {
        'count': len(keep_list),
        'percentage': round(len(keep_list)/len(repos)*100, 1),
        'repos': keep_list
    },
    'review': {
        'count': len(review_list),
        'percentage': round(len(review_list)/len(repos)*100, 1),
        'repos': review_list
    },
    'archive': {
        'count': len(archive_list),
        'percentage': round(len(archive_list)/len(repos)*100, 1),
        'repos': archive_list
    },
    'criteria_used': {
        'language_quality': '15 pts',
        'size_appropriateness': '20 pts',
        'community_engagement': '15 pts',
        'recent_activity': '20 pts',
        'has_description': '10 pts',
        'open_issues': '10 pts',
        'public_value': '10 pts',
        'total_possible': '100 pts',
        'thresholds': {
            'keep': '≥60 pts',
            'review': '35-59 pts',
            'archive': '<35 pts'
        }
    }
}

with open('agent_workspaces/Agent-1/MY_QA_AUDIT_RESULTS.json', 'w') as f:
    json.dump(results, f, indent=2)

print(f"\n✅ MY audit saved: MY_QA_AUDIT_RESULTS.json")
print(f"🔒 UNBIASED - No Agent-6 data consulted!")

