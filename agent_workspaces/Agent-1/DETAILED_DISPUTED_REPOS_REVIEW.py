#!/usr/bin/env python3
"""
Detailed Review of 42 Disputed Repos
Agent-6 wants archive, Agent-1 says keep/review
"""

import json
from datetime import datetime, timedelta

# Load disputed repos
with open('agent_workspaces/Agent-1/DISPUTED_REPOS.json') as f:
    disputed_data = json.load(f)
    disputed_repos = disputed_data['disputed_repos']

# Load full repo data
with open('agent_workspaces/Agent-1/MY_INDEPENDENT_REPO_DATA.json') as f:
    full_data = json.load(f)
    all_repos = {r['name']: r for r in full_data['repositories']}

# Load my audit results
with open('agent_workspaces/Agent-1/MY_QA_AUDIT_RESULTS.json') as f:
    my_results = json.load(f)
    my_keep = {r['repo']: r for r in my_results['keep']['repos']}
    my_review = {r['repo']: r for r in my_results['review']['repos']}

print("=" * 80)
print(f"🔍 DETAILED REVIEW OF {len(disputed_repos)} DISPUTED REPOS")
print("=" * 80)
print(f"\nAgent-6: Wants to ARCHIVE these")
print(f"Agent-1: Says KEEP or REVIEW these")
print(f"\nAnalyzing each repo in detail...\n")

# Detailed analysis
high_confidence_keep = []
borderline_cases = []
agent6_might_be_right = []

for repo_name in disputed_repos:
    if repo_name not in all_repos:
        continue
    
    repo = all_repos[repo_name]
    
    # Get my score
    my_score = 0
    my_decision = ""
    if repo_name in my_keep:
        my_score = my_keep[repo_name]['score']
        my_decision = "KEEP"
    elif repo_name in my_review:
        my_score = my_review[repo_name]['score']
        my_decision = "REVIEW"
    
    # Detailed assessment
    print(f"\n{'='*80}")
    print(f"REPO: {repo_name}")
    print(f"{'='*80}")
    print(f"Agent-6: ARCHIVE | Agent-1: {my_decision} ({my_score} pts)")
    print(f"\nDetails:")
    print(f"  Language: {repo['language']}")
    print(f"  Size: {repo['size_kb']:,} KB")
    print(f"  Stars: {repo['stars']} | Forks: {repo['forks']} | Issues: {repo['issues']}")
    print(f"  Updated: {repo['updated'][:10]}")
    print(f"  Description: {repo['description'][:100] if repo['description'] != 'No description' else 'None'}...")
    print(f"  Private: {'Yes' if repo['is_private'] else 'No'}")
    
    # Days since update
    try:
        updated = datetime.fromisoformat(repo['updated'].replace('Z', '+00:00'))
        days_ago = (datetime.now(updated.tzinfo) - updated).days
        print(f"  Last activity: {days_ago} days ago")
    except:
        days_ago = 999
        print(f"  Last activity: Unknown")
    
    # Deep analysis
    print(f"\n  MY ANALYSIS:")
    
    concerns = []
    positives = []
    
    # Positive indicators
    if repo['language'] == 'Python':
        positives.append("Python (preferred language)")
    if 100 <= repo['size_kb'] <= 5000:
        positives.append("Good size (manageable)")
    if days_ago <= 90:
        positives.append("Recently active")
    if repo['stars'] > 0 or repo['forks'] > 0:
        positives.append(f"Community: {repo['stars']} stars, {repo['forks']} forks")
    if repo['issues'] > 0:
        positives.append(f"Engagement: {repo['issues']} open issues")
    if repo['description'] and repo['description'] != 'No description':
        positives.append("Has description")
    if not repo['is_private']:
        positives.append("Public (community value)")
    
    # Concerns
    if repo['size_kb'] < 50:
        concerns.append("Trivial size (<50KB)")
    if repo['size_kb'] > 100000:
        concerns.append("Very large (>100MB)")
    if days_ago > 365:
        concerns.append(f"Stale ({days_ago} days since update)")
    if repo['stars'] == 0 and repo['forks'] == 0:
        concerns.append("No community engagement")
    if repo['description'] == 'No description':
        concerns.append("No description")
    if repo['is_private']:
        concerns.append("Private (no public value)")
    
    if positives:
        print(f"  ✅ Positives: {', '.join(positives)}")
    if concerns:
        print(f"  ⚠️ Concerns: {', '.join(concerns)}")
    
    # Final recommendation
    print(f"\n  RECOMMENDATION:")
    
    if my_score >= 70:
        print(f"  🟢 STRONG KEEP - High quality ({my_score} pts)")
        print(f"  Reason: {' | '.join(positives[:2])}")
        high_confidence_keep.append({
            'repo': repo_name,
            'score': my_score,
            'reason': 'High quality by QA standards'
        })
    elif my_score >= 55:
        print(f"  🟡 BORDERLINE - Needs review ({my_score} pts)")
        print(f"  Reason: Mixed signals - has value but concerns exist")
        borderline_cases.append({
            'repo': repo_name,
            'score': my_score,
            'positives': len(positives),
            'concerns': len(concerns)
        })
    else:
        print(f"  🟠 AGENT-6 MIGHT BE RIGHT - Lean toward archive ({my_score} pts)")
        print(f"  Reason: {' | '.join(concerns[:2])}")
        agent6_might_be_right.append({
            'repo': repo_name,
            'score': my_score,
            'reason': 'Low quality, Agent-6 may be correct'
        })

# Summary
print(f"\n\n{'='*80}")
print(f"DETAILED REVIEW SUMMARY")
print(f"{'='*80}")
print(f"\n🟢 HIGH CONFIDENCE KEEP: {len(high_confidence_keep)} repos")
print(f"   Strong quality indicators, definitely keep")

print(f"\n🟡 BORDERLINE CASES: {len(borderline_cases)} repos")
print(f"   Mixed signals, needs stakeholder review")

print(f"\n🟠 AGENT-6 MIGHT BE RIGHT: {len(agent6_might_be_right)} repos")
print(f"   Weak indicators, lean toward archive")

print(f"\n{'='*80}")
print(f"FINAL RECOMMENDATION:")
print(f"{'='*80}")
print(f"  Keep: {len(high_confidence_keep)} repos (high confidence)")
print(f"  Review: {len(borderline_cases)} repos (needs decision)")
print(f"  Archive: {len(agent6_might_be_right)} repos (Agent-6 probably right)")
print(f"\n  Total disputed: {len(disputed_repos)} repos")

# Save detailed analysis
detailed_analysis = {
    'total_disputed': len(disputed_repos),
    'high_confidence_keep': high_confidence_keep,
    'borderline_cases': borderline_cases,
    'agent6_might_be_right': agent6_might_be_right,
    'summary': {
        'strong_keep': len(high_confidence_keep),
        'needs_review': len(borderline_cases),
        'lean_archive': len(agent6_might_be_right)
    }
}

with open('agent_workspaces/Agent-1/DETAILED_DISPUTED_ANALYSIS.json', 'w') as f:
    json.dump(detailed_analysis, f, indent=2)

print(f"\n✅ Detailed analysis saved: DETAILED_DISPUTED_ANALYSIS.json")


