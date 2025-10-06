#!/usr/bin/env python3
with open('devlogs/Agent-3.md', 'r') as f:
    content = f.read()

print("CYCLE_DONE found:", 'CYCLE_DONE' in content)
print("Quote characters in content:")
for i, char in enumerate(content):
    if char in ['"', "'", '`']:
        print(f"Position {i}: '{char}' (ord: {ord(char)})")

# Let's try a more flexible regex
import re
pattern = r"CYCLE_DONE\s+(\w+)\s+(\w+)\s+\[(.*?)\]\s+[\"']([^\"']+)[\"']"
matches = re.finditer(pattern, content, re.DOTALL)
for match in matches:
    print("Match found:", match.groups())
