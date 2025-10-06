#!/usr/bin/env python3
import re

# Read the actual devlog file
with open("devlogs/Agent-3.md", "r", encoding="utf-8") as f:
    content = f.read()

print("File content:")
print(repr(content))
print()

# Test the regex
pattern = r"CYCLE_DONE\s+(\w+)\s+(\w+)\s+\[(.*?)\]\s+\"([^\"]+)\""
matches = re.finditer(pattern, content, re.DOTALL)

for i, match in enumerate(matches):
    print(f"Match {i+1}:")
    print("Agent:", match.group(1))
    print("Cycle ID:", match.group(2))
    print("Metrics:", match.group(3))
    print("Summary:", match.group(4))
    print()

if not list(re.finditer(pattern, content, re.DOTALL)):
    print("No matches found. Let's try a simpler pattern...")
    
    # Try to find just the CYCLE_DONE part
    simple_pattern = r"CYCLE_DONE\s+(\w+)\s+(\w+)"
    simple_matches = re.finditer(simple_pattern, content)
    for match in simple_matches:
        print("Simple match:", match.groups())
