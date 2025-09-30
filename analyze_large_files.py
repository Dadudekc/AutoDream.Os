import json

# Load compliance data
with open('final_compliance_check.json', 'r') as f:
    data = json.load(f)

# Find large files
large_files = [f for f in data['violations']['files'] if f['lines'] > 400]
large_files.sort(key=lambda x: x['lines'], reverse=True)

print("Large files (>400 lines):")
for f in large_files[:10]:
    print(f"  {f['file']}: {f['lines']} lines")
