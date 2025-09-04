from ..core.unified_entry_point_system import main
#!/usr/bin/env python3
"""
Vector Database Setup Script

This script initializes the vector database and indexes all project documentation
for AI agent access.
"""

from ..core.unified_import_system import logging

# Add src to path
sys.path.insert(0, str(get_unified_utility().Path(__file__).parent.parent / "src"))


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    main()

