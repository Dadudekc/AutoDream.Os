import json

with open('memory_leak_report.json') as f:
    data = json.load(f)

print("=" * 80)
print("COMPREHENSIVE MEMORY LEAK ANALYSIS - ALL TOOLS & CODEBASE")
print("=" * 80)
print()

print(f"📊 Total Files Analyzed: {data['summary']['total_files_analyzed']}")
print(f"⚠️ Files with Issues: {data['summary']['files_with_issues']}")
print(f"🚨 Total Issues: {data['summary']['total_issues']}")
print()

print("Issues by Severity:")
for sev, count in sorted(data['summary']['issues_by_severity'].items(), key=lambda x: x[1], reverse=True):
    print(f"  {sev}: {count}")
print()

print("Issues by Type:")
for issue_type, count in sorted(data['summary']['issues_by_type'].items(), key=lambda x: x[1], reverse=True):
    print(f"  {issue_type}: {count}")
print()

print("Top 10 Files with Most Issues:")
for f in data['summary']['top_files_with_issues'][:10]:
    print(f"  {f['file']}: {f['issue_count']} issues")
print()

print("=" * 80)
print("HIGH SEVERITY ISSUES (CRITICAL):")
print("=" * 80)
high_issues = [i for i in data['detailed_issues'] if i['severity'] == 'HIGH']
print(f"\nTotal HIGH severity issues: {len(high_issues)}")

issue_types = {}
for issue in high_issues:
    issue_type = issue['type']
    if issue_type not in issue_types:
        issue_types[issue_type] = []
    issue_types[issue_type].append(issue)

for issue_type, issues in sorted(issue_types.items(), key=lambda x: len(x[1]), reverse=True):
    print(f"\n{issue_type}: {len(issues)} issues")
    for issue in issues[:3]:  # Show first 3 examples
        print(f"  - {issue['file']}:{issue['line']}")
        print(f"    {issue['description']}")
        print(f"    Code: {issue.get('code', 'N/A')[:80]}")

print()
print("=" * 80)
print("RECOMMENDATIONS:")
print("=" * 80)
for rec in data['summary']['recommendations']:
    print(f"  {rec}")

