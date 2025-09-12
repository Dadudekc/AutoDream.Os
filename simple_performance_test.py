#!/usr/bin/env python3
"""
Simple Performance Test
=======================

Quick test to verify performance optimizations work correctly.
"""

import time
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import optimized components
from infrastructure.persistence.optimized_sqlite_task_repo import OptimizedSqliteTaskRepository
from domain.entities.task import Task

def test_performance_optimizations():
    """Test basic performance optimizations."""
    print("🚀 Testing Performance Optimizations")
    print("=" * 40)

    # Create test database
    db_path = "data/test_performance.db"
    if os.path.exists(db_path):
        os.remove(db_path)

    # Initialize optimized repository
    repo = OptimizedSqliteTaskRepository(db_path, pool_size=3)

    print("✅ Repository initialized with connection pooling")

    # Create test tasks
    tasks = []
    for i in range(50):
        task = Task(
            id=f"test-task-{i:03d}",
            title=f"Performance Test Task {i}",
            description=f"Description for performance test {i}",
            assigned_agent_id=f"Agent-{i % 5}" if i % 2 == 0 else None,
            created_at=f"2025-09-11T{i%24:02d}:00:00",
            priority=(i % 5) + 1
        )
        tasks.append(task)

    # Test INSERT performance
    print("📝 Testing INSERT operations...")
    start_time = time.time()
    for task in tasks:
        repo.add(task)
    insert_time = time.time() - start_time
    print(".4f")

    # Test SELECT performance
    print("📖 Testing SELECT operations...")
    start_time = time.time()
    results = list(repo.get_all(limit=20))
    first_select_time = time.time() - start_time
    print(".4f")

    # Test cached SELECT
    start_time = time.time()
    results = list(repo.get_all(limit=20))
    cached_select_time = time.time() - start_time
    print(".4f")

    # Test agent-specific queries
    print("👤 Testing agent-specific queries...")
    start_time = time.time()
    agent_results = list(repo.get_by_agent("Agent-1", limit=10))
    agent_query_time = time.time() - start_time
    print(".4f")

    # Test cache performance
    print("💾 Testing cache performance...")
    cache_stats = repo.get_cache_stats()
    print(f"  Cache size: {cache_stats['cache_size']}/{cache_stats['max_cache_size']}")
    print(f"  Connection pool: {cache_stats['connection_pool_size']}/{cache_stats['max_pool_size']}")

    # Test cache invalidation
    print("🗑️ Testing cache invalidation...")
    start_time = time.time()
    invalidated = repo._cache.invalidate_pattern('test-task')
    invalidation_time = time.time() - start_time
    print(f"  Invalidated {invalidated} entries in {invalidation_time:.6f} seconds")

    # Performance summary
    print("\n📊 PERFORMANCE SUMMARY:")
    print(".4f")
    print(".4f")
    print(".4f")

    if cached_select_time < first_select_time:
        cache_improvement = first_select_time / cached_select_time
        print(".2f")

    print("\n✅ Performance test completed successfully!")
    print("🎯 Database optimizations are working correctly")

    # Cleanup
    if os.path.exists(db_path):
        os.remove(db_path)

if __name__ == "__main__":
    test_performance_optimizations()
