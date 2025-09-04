#!/usr/bin/env python3
"""Simple test to verify messaging system is working."""

import json

# Test coordinate loading
try:
    with open('cursor_agent_coords.json', 'r', encoding='utf-8') as f:
        coords_data = json.load(f)
    print(f'✅ Coordinates loaded successfully: {len(coords_data["agents"])} agents')
except Exception as e:
    print(f'❌ Error loading coordinates: {e}')

# Test messaging imports
try:
    from src.services.unified_messaging_imports import COORDINATE_CONFIG_FILE, logging
    print(f'✅ Unified messaging imports working: {COORDINATE_CONFIG_FILE}')
except Exception as e:
    print(f'❌ Error importing messaging: {e}')
