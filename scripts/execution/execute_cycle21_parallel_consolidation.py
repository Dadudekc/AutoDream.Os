"""
Execute Cycle 21 Parallel Consolidation
Direct execution script for Cycle 21 parallel consolidation mission

@author Agent-7 - Web Development Specialist
@version 1.0.0 - Cycle 21 Parallel Consolidation Execution
@license MIT
"""


# Add the src directory to the path
sys.path.insert(0, get_unified_utility().path.abspath(get_unified_utility().path.join(get_unified_utility().path.dirname(__file__), 'src')))

# Import the coordinator class directly with proper encoding
exec(open('src/core/cycle-21-parallel-consolidation-coordinator.py', encoding='utf-8').read())

if __name__ == "__main__":
    coordinator = Cycle21ParallelConsolidationCoordinator()
    coordinator.execute_parallel_consolidation()
