#!/usr/bin/env python3
"""Database diagnostic script."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from swarm_brain import SwarmBrain, Retriever

def main():
    print("🔍 Database Diagnostic")
    print("=" * 40)
    
    # Check SwarmBrain database
    brain = SwarmBrain()
    cursor = brain.conn.cursor()
    
    # Check tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    print(f"📊 Tables: {tables}")
    
    # Check document count
    cursor.execute("SELECT COUNT(*) FROM documents")
    doc_count = cursor.fetchone()[0]
    print(f"📊 Document count: {doc_count}")
    
    # Check sample documents
    cursor.execute("SELECT id, title, agent_id, kind FROM documents LIMIT 5")
    samples = cursor.fetchall()
    print(f"📊 Sample documents:")
    for row in samples:
        print(f"  {row[0]}: {row[1]} ({row[2]}, {row[3]})")
    
    # Check retriever
    retriever = Retriever()
    docs = retriever.search("", k=1000)
    print(f"📊 Retriever search result: {len(docs)} docs")
    
    if docs:
        print(f"📊 First doc: {docs[0].get('title', 'No title')}")

if __name__ == "__main__":
    main()
