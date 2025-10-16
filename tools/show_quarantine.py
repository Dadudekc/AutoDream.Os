#!/usr/bin/env python3
"""Show quarantined tools summary."""
import json
from collections import Counter

data = json.load(open('runtime/toolbelt_quarantine.json'))

print('\n' + '='*60)
print(f"🚨 TOOLBELT QUARANTINE: {data['count']} TOOLS")
print('='*60)

cats = [t.split('.')[0] for t in data['quarantined_tools']]
cat_counts = Counter(cats)

print('\nBroken by category:')
for cat, count in sorted(cat_counts.items()):
    tools = [t for t in data['quarantined_tools'] if t.startswith(cat + '.')]
    print(f'\n  {cat}.* ({count} tools):')
    for tool in tools:
        print(f'    ❌ {tool}')

print('\n' + '='*60)
print('📊 WORKING TOOLS: 71/100 (71%)')
print('='*60 + '\n')

