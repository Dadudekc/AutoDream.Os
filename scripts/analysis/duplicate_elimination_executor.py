from ..core.unified_entry_point_system import main
from src.utils.config_core import get_config
#!/usr/bin/env python3
"""
Duplicate Elimination Executor
Execute comprehensive duplicate elimination across the entire project.
"""


# Add src to path
sys.path.insert(0, str(get_unified_utility().Path(__file__).parent / "src"))

# Direct import
sys.path.insert(0, str(get_unified_utility().Path(__file__).parent / "src" / "core" / "duplicate_elimination"))

    duplicate_elimination_system
)



if __name__ == "__main__":
    main()
