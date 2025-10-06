#!/usr/bin/env python3
import re

# Read the actual devlog file
with open("devlogs/Agent-3.md", "r", encoding="utf-8") as f:
    content = f.read()

# Test different patterns
patterns = [
    r"CYCLE_DONE\s+(\w+)\s+(\w+)\s+\[(.*?)\]\s+\"([^\"]+)\"",
    r"CYCLE_DONE\s+(\w+)\s+(\w+)\s+\[(.*?)\]\s+\"([^\"]+)\"",
    r"CYCLE_DONE\s+(\w+)\s+(\w+)\s+\[(.*?)\]\s+\"([^\"]+)\"",
    r"CYCLE_DONE\s+(\w+)\s+(\w+)\s+\[(.*?)\]\s+\"([^\"]+)\"",
]

for i, pattern in enumerate(patterns):
    print(f"Testing pattern {i+1}: {pattern}")
    matches = list(re.finditer(pattern, content, re.DOTALL))
    if matches:
        print(f"✅ Pattern {i+1} found {len(matches)} matches")
        for match in matches:
            print(f"  Agent: {match.group(1)}")
            print(f"  Cycle: {match.group(2)}")
            print(f"  Metrics: {match.group(3)[:50]}...")
            print(f"  Summary: {match.group(4)}")
        break
    else:
        print(f"❌ Pattern {i+1} failed")

# If all patterns fail, let's try a very simple approach
if not any(re.finditer(p, content, re.DOTALL) for p in patterns):
    print("\nTrying simple approach...")
    simple_pattern = r"CYCLE_DONE\s+(\w+)\s+(\w+)"
    simple_matches = list(re.finditer(simple_pattern, content))
    if simple_matches:
        print(f"✅ Simple pattern found {len(simple_matches)} matches")
        for match in simple_matches:
            print(f"  Agent: {match.group(1)}")
            print(f"  Cycle: {match.group(2)}")
    else:
        print("❌ Even simple pattern failed")
