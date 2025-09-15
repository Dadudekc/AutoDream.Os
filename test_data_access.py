#!/usr/bin/env python3
"""Test data access after organization"""

import json
from pathlib import Path

def test_data_access():
    """Test data access after organization"""
    print("🔍 Testing data access after organization...")
    
    # Test data index access
    data_index_path = Path('data/data_index.json')
    if data_index_path.exists():
        with open(data_index_path, 'r') as f:
            index = json.load(f)
        print(f'✅ Data index accessible: {len(index["files"])} files, {index["total_size"]/1024/1024:.2f} MB')
    else:
        print('❌ Data index not found')
    
    # Test database access
    db_path = Path('data/databases/unified.db')
    if db_path.exists():
        print(f'✅ Database accessible: {db_path.stat().st_size} bytes')
    else:
        print('❌ Database not found')
    
    # Test vector data access
    vector_path = Path('data/vector_data')
    if vector_path.exists():
        vector_files = list(vector_path.iterdir())
        print(f'✅ Vector data accessible: {len(vector_files)} files')
    else:
        print('❌ Vector data not found')
    
    # Test semantic data access
    semantic_path = Path('data/semantic_data')
    if semantic_path.exists():
        semantic_files = list(semantic_path.iterdir())
        print(f'✅ Semantic data accessible: {len(semantic_files)} files')
    else:
        print('❌ Semantic data not found')
    
    # Test cookies access
    cookies_path = Path('data/cookies')
    if cookies_path.exists():
        cookie_files = list(cookies_path.iterdir())
        print(f'✅ Cookies accessible: {len(cookie_files)} files')
    else:
        print('❌ Cookies not found')

if __name__ == "__main__":
    test_data_access()
